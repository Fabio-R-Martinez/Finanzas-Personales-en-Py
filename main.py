# main.py
import sys
from pathlib import Path
from kivy.config import Config

# Desactivar gestos multitáctiles en Linux
Config.set('input', 'mouse', 'mouse,disable_multitouch')

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from src.database.db_manager import DBManager

# Importaciones directas sin pasar por __init__.py
from src.views.dashboard_screen import DashboardScreen
from src.views.egresos.egresos_screen import FormularioGastoScreen


class FinanzasApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.theme_style = "Light"

        db_path = BASE_DIR / "finanzas_app.db"
        self.db = DBManager(str(db_path))

        sm = MDScreenManager()
        sm.add_widget(DashboardScreen(name='dashboard'))
        sm.add_widget(FormularioGastoScreen(name='formulario_gasto'))

        return sm

    def ir_a_dashboard(self, direccion="left"):
        """Retorna al Dashboard con animación hacia la izquierda."""
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
        """Procesa el guardado del gasto en SQLite sin abandonar la pantalla actual."""
        if datos and hasattr(self, "db") and self.db:
            self.db.registrar_gasto_efectuado(
                categoria=datos["categoria"],
                concepto=datos["concepto"],
                monto=datos["monto"]
            )
            print(f"Gasto registrado en SQLite: {datos}")


if __name__ == "__main__":
    FinanzasApp().run()