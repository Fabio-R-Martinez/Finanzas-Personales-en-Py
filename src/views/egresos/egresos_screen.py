# src/views/egresos/egresos_screen.py
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder

# Importación modular de cada pestaña
from src.views.egresos.tab_gastos_efectuados import TabGastosEfectuados
from src.views.egresos.tab_gastos_realizados import TabGastosRealizados
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
            on_tab_switch: root.al_cambiar_pestana(*args)
            TabGastosEfectuados:
                id: tab_efectuados
            TabGastosRealizados:
                id: tab_realizados
            TabEgresosPrevistos:
                id: tab_previstos
'''

Builder.load_string(KV_EGRESOS_SCREEN)


class FormularioGastoScreen(MDScreen):
    """Pantalla contenedora de Egresos con actualización automática al entrar o cambiar de pestaña."""

    def on_enter(self, *args):
        """Se ejecuta automáticamente cada vez que se abre la pantalla de Egresos."""
        super().on_enter(*args)
        self.actualizar_todas_las_pestanas()

    def al_cambiar_pestana(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        """Se ejecuta al hacer clic o deslizar a cualquier pestaña."""
        if hasattr(instance_tab, "cargar_gastos_por_categoria"):
            instance_tab.cargar_gastos_por_categoria()
        elif hasattr(instance_tab, "cargar_categorias"):
            instance_tab.cargar_categorias()

    def actualizar_todas_las_pestanas(self):
        """Fuerza la recarga de datos en las pestañas desde SQLite."""
        if "tab_realizados" in self.ids:
            self.ids.tab_realizados.cargar_gastos_por_categoria()
        if "tab_previstos" in self.ids:
            self.ids.tab_previstos.cargar_categorias()
