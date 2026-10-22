# 2. Controladores Python, POO y Conexión SQLite
# El siguiente código Python integra la base de datos local SQLite y los objetos de dominio (Ingreso, Gasto, Balance) con la interfaz KivyMD.

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.list import TwoLineAvatarIconListItem, IconLeftWidget
from kivy.lang import Builder
from typing import List
import sqlite3

# --- 1. CAPA POO DE DOMINIO (Montos Enteros) ---

class TransaccionBase:
    def __init__(self, id_categoria: int, categoria: str, monto_esperado: int = 0, monto_ejecutado: int = 0):
        self.id_categoria = id_categoria
        self.categoria = categoria
        self.monto_esperado = int(monto_esperado)
        self.monto_ejecutado = int(monto_ejecutado)

    def calcular_diferencia(self) -> int:
        return self.monto_ejecutado - self.monto_esperado


class Ingreso(TransaccionBase):
    def esta_cumplido(self) -> bool:
        return self.monto_ejecutado >= self.monto_esperado


class Gasto(TransaccionBase):
    def esta_excedido(self) -> bool:
        return self.monto_ejecutado > self.monto_esperado


class Balance:
    def __init__(self, periodo: str, ingresos: List[Ingreso] = None, gastos: List[Gasto] = None):
        self.periodo = periodo
        self.ingresos = ingresos if ingresos is not None else []
        self.gastos = gastos if gastos is not None else []

    @property
    def total_ingresos_esperados(self) -> int:
        return sum(i.monto_esperado for i in self.ingresos)

    @property
    def total_ingresos_ejecutados(self) -> int:
        return sum(i.monto_ejecutado for i in self.ingresos)

    def desviacion_ingresos(self) -> int:
        return self.total_ingresos_ejecutados - self.total_ingresos_esperados

    @property
    def total_gastos_esperados(self) -> int:
        return sum(g.monto_esperado for g in self.gastos)

    @property
    def total_gastos_ejecutados(self) -> int:
        return sum(g.monto_ejecutado for g in self.gastos)

    def desviacion_gastos(self) -> int:
        return self.total_gastos_ejecutados - self.total_gastos_esperados

    def balance_esperado(self) -> int:
        return self.total_ingresos_esperados - self.total_gastos_esperados

    def balance_ejecutado(self) -> int:
        return self.total_ingresos_ejecutados - self.total_gastos_ejecutados

    def desviacion_neto_balance(self) -> int:
        return self.balance_ejecutado() - self.balance_esperado()

    def diagnostico_resumen(self) -> str:
        desviacion = self.desviacion_neto_balance()
        if desviacion > 0:
            return f"SUPERÁVIT SUPERIOR: Ahorraste {fmt_moneda(desviacion)} más de lo planificado."
        elif desviacion == 0:
            return "CUMPLIMIENTO EXACTO: Presupuesto ejecutado al 100% según lo planeado."
        else:
            return f"DESVIACIÓN NEGATIVA: Tu ahorro quedó {fmt_moneda(abs(desviacion))} por debajo de la meta."


# --- 2. CAPA SQLite ---

class DBManager:
    def __init__(self, db_path: str = "finanzas_app.db"):
        self.db_path = db_path

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def obtener_balance_mes(self, periodo: str) -> Balance:
        query = """
        WITH 
        P AS (
            SELECT categoria_id, SUM(monto_esperado) AS total_esperado
            FROM presupuestos WHERE periodo = ? GROUP BY categoria_id
        ),
        T AS (
            SELECT categoria_id, SUM(monto_ejecutado) AS total_ejecutado
            FROM transacciones WHERE strftime('%Y-%m', fecha) = ? GROUP BY categoria_id
        )
        SELECT c.id, c.nombre, c.tipo, COALESCE(P.total_esperado, 0), COALESCE(T.total_ejecutado, 0)
        FROM categorias c
        LEFT JOIN P ON c.id = P.categoria_id
        LEFT JOIN T ON c.id = T.categoria_id
        WHERE P.categoria_id IS NOT NULL OR T.categoria_id IS NOT NULL
        ORDER BY c.tipo DESC, c.nombre ASC;
        """
        ingresos, gastos = [], []
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute(query, (periodo, periodo))
            for cat_id, cat_nom, tipo, esp, ejec in cur.fetchall():
                if tipo == 'INGRESO':
                    ingresos.append(Ingreso(cat_id, cat_nom, esp, ejec))
                else:
                    gastos.append(Gasto(cat_id, cat_nom, esp, ejec))
        return Balance(periodo, ingresos, gastos)


# --- 3. PANTALLAS KIVYMD ---

class DashboardScreen(MDScreen):
    def on_pre_enter(self):
        self.actualizar_dashboard()

    def actualizar_dashboard(self):
        app = MDApp.get_running_app()
        balance = app.db.obtener_balance_mes(app.periodo_actual)

        # Actualización de Labels en Dashboard
        self.ids.lbl_diagnostico.text = balance.diagnostico_resumen()
        self.ids.lbl_ingresos_esperados.text = f"Planificado: {fmt_moneda(balance.total_ingresos_esperados)}"
        self.ids.lbl_ingresos_ejecutados.text = f"Real: {fmt_moneda(balance.total_ingresos_ejecutados)}"
        self.ids.lbl_ingresos_dif.text = f"Dif: {fmt_moneda(balance.desviacion_ingresos())}"

        self.ids.lbl_gastos_esperados.text = f"Planificado: {fmt_moneda(balance.total_gastos_esperados)}"
        self.ids.lbl_gastos_ejecutados.text = f"Real: {fmt_moneda(balance.total_gastos_ejecutados)}"
        self.ids.lbl_gastos_dif.text = f"Dif: {fmt_moneda(balance.desviacion_gastos())}"

        self.ids.lbl_balance_esperado.text = f"Ahorro Meta: {fmt_moneda(balance.balance_esperado())}"
        self.ids.lbl_balance_ejecutado.text = f"Ahorro Real: {fmt_moneda(balance.balance_ejecutado())}"

        # Progreso visual
        pct_ing = min(100, int((balance.total_ingresos_ejecutados / balance.total_ingresos_esperados * 100))) if balance.total_ingresos_esperados > 0 else 0
        pct_gas = min(100, int((balance.total_gastos_ejecutados / balance.total_gastos_esperados * 100))) if balance.total_gastos_esperados > 0 else 0
        
        self.ids.bar_ingresos.value = pct_ing
        self.ids.bar_gastos.value = pct_gas


class IngresosScreen(MDScreen):
    def on_pre_enter(self):
        app = MDApp.get_running_app()
        balance = app.db.obtener_balance_mes(app.periodo_actual)
        container = self.ids.lista_ingresos_container
        container.clear_widgets()

        for item in balance.ingresos:
            icon = IconLeftWidget(icon="check-circle" if item.esta_cumplido() else "clock-outline")
            icon.theme_text_color = "Custom"
            icon.text_color = (0, 0.6, 0.2, 1) if item.esta_cumplido() else (0.8, 0.5, 0, 1)

            list_item = TwoLineAvatarIconListItem(
                text=item.categoria,
                secondary_text=f"Real: {fmt_moneda(item.monto_ejecutado)} / Meta: {fmt_moneda(item.monto_esperado)}"
            )
            list_item.add_widget(icon)
            container.add_widget(list_item)


class GastosScreen(MDScreen):
    def on_pre_enter(self):
        app = MDApp.get_running_app()
        balance = app.db.obtener_balance_mes(app.periodo_actual)
        container = self.ids.lista_gastos_container
        container.clear_widgets()

        for item in balance.gastos:
            excedido = item.esta_excedido()
            icon = IconLeftWidget(icon="alert-circle" if excedido else "check-circle")
            icon.theme_text_color = "Custom"
            icon.text_color = (0.8, 0.2, 0.2, 1) if excedido else (0, 0.6, 0.2, 1)

            list_item = TwoLineAvatarIconListItem(
                text=item.categoria,
                secondary_text=f"Real: {fmt_moneda(item.monto_ejecutado)} / Presupuesto: {fmt_moneda(item.monto_esperado)}"
            )
            list_item.add_widget(icon)
            container.add_widget(list_item)


class FinanzasApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Indigo"
        self.periodo_actual = "2026-09"
        self.db = DBManager("finanzas_app.db")
        self.db.seed_demo_data(self.periodo_actual)

        Builder.load_string(KV_LAYOUT)
        sm = MDScreenManager()
        sm.add_widget(DashboardScreen(name='dashboard'))
        sm.add_widget(IngresosScreen(name='ingresos'))
        sm.add_widget(GastosScreen(name='gastos'))
        return sm

if __name__ == "__main__":
    FinanzasApp().run()
