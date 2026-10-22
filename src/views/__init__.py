import sys
from pathlib import Path

# 1. Registrar la ruta base para que Python reconozca la carpeta 'src'
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivy.lang import Builder

# 2. Importaciones de los módulos organizados en src/
from src.database.db_manager import DBManager
from src.views.screens import DashboardScreen, IngresosScreen, GastosScreen
from src.utils.formatters import fmt_moneda

# src/views/__init__.py
from src.views.dashboard_view import DashboardScreen
from src.views.gasto_view import FormularioGastoScreen

__all__ = ["DashboardScreen", "FormularioGastoScreen"]

class FinanzasApp(MDApp):
    def build(self):
        # Estilo y tema de la aplicación
        self.theme_cls.primary_palette = "Indigo"
        self.periodo_actual = "2026-09"

        # Conexión a la base de datos local SQLite
        db_path = BASE_DIR / "finanzas_app.db"
        self.db = DBManager(str(db_path))
        self.db.seed_demo_data(self.periodo_actual)

        # Cargar el archivo de diseño KV
        kv_path = BASE_DIR / "src" / "views" / "layouts.kv"
        Builder.load_file(str(kv_path))

        # Registrar las pantallas en el gestor
        sm = MDScreenManager()
        sm.add_widget(DashboardScreen(name='dashboard'))
        sm.add_widget(IngresosScreen(name='ingresos'))
        sm.add_widget(GastosScreen(name='gastos'))

        return sm


if __name__ == "__main__":
    FinanzasApp().run()
