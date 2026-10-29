# src/views/ingresos/ingresos_screen.py
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder

from src.views.ingresos.tab_agregar_ingreso import TabAgregarIngreso
from src.views.ingresos.tab_ingresos_realizados import TabIngresosRealizados
from src.views.ingresos.tab_ingresos_previstos import TabIngresosPrevistos

KV_INGRESOS_SCREEN = '''
<FormularioIngresoScreen>:
    name: "formulario_ingreso"

    MDBoxLayout:
        orientation: 'vertical'

        MDTopAppBar:
            title: "Ingresos"
            elevation: 4

        MDTabs:
            id: tabs
            on_tab_switch: root.al_cambiar_pestana(*args)
            TabAgregarIngreso:
                id: tab_agregar
            TabIngresosRealizados:
                id: tab_realizados
            TabIngresosPrevistos:
                id: tab_previstos
'''

Builder.load_string(KV_INGRESOS_SCREEN)


class FormularioIngresoScreen(MDScreen):
    """Pantalla contenedora de Ingresos con 3 pestañas."""

    def on_enter(self, *args):
        super().on_enter(*args)
        self.actualizar_todas_las_pestanas()

    def al_cambiar_pestana(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        if hasattr(instance_tab, "cargar_ingresos_por_categoria"):
            instance_tab.cargar_ingresos_por_categoria()
        elif hasattr(instance_tab, "cargar_categorias"):
            instance_tab.cargar_categorias()

    def actualizar_todas_las_pestanas(self):
        if "tab_realizados" in self.ids:
            self.ids.tab_realizados.cargar_ingresos_por_categoria()
        if "tab_previstos" in self.ids:
            self.ids.tab_previstos.cargar_categorias()
        if "tab_agregar" in self.ids:
            self.ids.tab_agregar.cargar_categoria_inicial()