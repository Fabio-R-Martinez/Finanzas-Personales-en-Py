# main.py
import sys
from pathlib import Path
from kivy.config import Config

Config.set('input', 'mouse', 'mouse,disable_multitouch')

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from src.database.db_manager import DBManager

from src.views.dashboard_screen import DashboardScreen
from src.views.egresos.egresos_screen import FormularioGastoScreen
from src.views.ingresos.ingresos_screen import FormularioIngresoScreen


class FinanzasApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.theme_style = "Light"

        db_path = BASE_DIR / "finanzas_app.db"
        self.db = DBManager(str(db_path))

        sm = MDScreenManager()
        sm.add_widget(DashboardScreen(name='dashboard'))
        sm.add_widget(FormularioGastoScreen(name='formulario_gasto'))
        sm.add_widget(FormularioIngresoScreen(name='formulario_ingreso'))

        return sm

    def ir_a_dashboard(self, direccion="left"):
        """Retorna al Dashboard con animación hacia la dirección especificada."""
        if self.root:
            self.root.transition.direction = direccion
            self.root.current = "dashboard"

    def ir_a_formulario_gasto(self):
        """Abre Egresos/Gastos: entra desde la IZQUIERDA hacia la derecha."""
        if self.root:
            self.root.transition.direction = "right"
            self.root.current = "formulario_gasto"

    def ir_a_formulario_ingreso(self):
        """Abre Ingresos: entra desde la DERECHA hacia la izquierda."""
        if self.root:
            self.root.transition.direction = "left"
            if self.root.has_screen("formulario_ingreso"):
                self.root.current = "formulario_ingreso"

    def guardar_gasto(self, datos=None):
        """Procesa el guardado del gasto en SQLite."""
        if datos and hasattr(self, "db") and self.db:
            self.db.registrar_gasto_efectuado(
                categoria=datos["categoria"],
                concepto=datos["concepto"],
                monto=datos["monto"]
            )

    def guardar_ingreso(self, datos=None):
        """Procesa el guardado del ingreso en SQLite."""
        if datos and hasattr(self, "db") and self.db:
            self.db.registrar_ingreso(
                categoria=datos["categoria"],
                subcategoria=datos.get("subcategoria"),
                concepto=datos["concepto"],
                monto=datos["monto"]
            )


if __name__ == "__main__":
    FinanzasApp().run()
