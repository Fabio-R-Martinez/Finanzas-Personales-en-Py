# main.py
import sys
from pathlib import Path
from kivy.config import Config

# Desactivar gestos multitáctiles en Linux para evitar congelamientos
Config.set('input', 'mouse', 'mouse,disable_multitouch')

# Registrar la ruta base del proyecto
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from src.database.db_manager import DBManager
from src.views import DashboardScreen, FormularioGastoScreen


class FinanzasApp(MDApp):
    def build(self):
        # Tema y paleta de la aplicación
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.theme_style = "Light"

        # Conexión a la base de datos local SQLite
        db_path = BASE_DIR / "finanzas_app.db"
        self.db = DBManager(str(db_path))

        # Registrar las pantallas en el gestor de pantallas
        sm = MDScreenManager()
        sm.add_widget(DashboardScreen(name='dashboard'))
        sm.add_widget(FormularioGastoScreen(name='formulario_gasto'))

        return sm

    def ir_a_dashboard(self):
        """Cambia la vista activa al Dashboard."""
        if self.root:
            self.root.current = "dashboard"

    def ir_a_formulario_gasto(self):
        """Cambia la vista activa al Formulario de Gastos/Egresos."""
        if self.root:
            self.root.current = "formulario_gasto"

    def guardar_gasto(self, datos=None):
        """Procesa el guardado del gasto y regresa al Dashboard."""
        if datos:
            print(f"Gasto a guardar en BD: {datos}")
        self.ir_a_dashboard()


if __name__ == "__main__":
    FinanzasApp().run()