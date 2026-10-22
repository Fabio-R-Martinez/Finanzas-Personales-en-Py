# src/views/egresos/egresos_screen.py
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder

# Importar los componentes modulares
from src.views.egresos.tab_gastos_efectuados import TabGastosEfectuados
from src.views.egresos.tab_egresos_previstos import TabEgresosPrevistos

KV_EGRESOS_SCREEN = '''
<FormularioGastoScreen>:
    name: "formulario_gasto"

    MDBoxLayout:
        orientation: 'vertical'

        MDTopAppBar:
            title: "Egresos"
            elevation: 4

        MDTabs:
            id: tabs
            TabGastosEfectuados:
            TabEgresosPrevistos:
'''

Builder.load_string(KV_EGRESOS_SCREEN)


class FormularioGastoScreen(MDScreen):
    """Pantalla contenedora de Egresos."""
    pass