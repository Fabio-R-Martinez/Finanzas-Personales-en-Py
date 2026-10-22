# main.py
from kivy.config import Config

# Desactivar gestos multitáctiles en Linux para evitar congelamientos
Config.set('input', 'mouse', 'mouse,disable_multitouch')

from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from src.database.db_manager import DBManager
from src.views import DashboardScreen, FormularioGastoScreen


class FinanzasApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.theme_style = "Light"

        # Inicializar la base de datos
        db = DBManager()

        # Administrador de pantallas con instancias independientes
        sm = ScreenManager()
        sm.add_widget(DashboardScreen())
        sm.add_widget(FormularioGastoScreen())

        return sm

    def ir_a_dashboard(self):
        """Cambia la vista activa al Dashboard."""
        if self.root:
            self.root.current = "dashboard"

    def ir_a_formulario_gasto(self):
        """Cambia la vista activa al Formulario de Gastos."""
        if self.root:
            self.root.current = "formulario_gasto"

    def guardar_gasto(self):
        """Procesa el guardado del gasto y regresa al Dashboard."""
        # En el siguiente paso obtendremos los datos ingresados y los guardaremos en SQLite
        self.ir_a_dashboard()


if __name__ == "__main__":
    FinanzasApp().run()
