# src/views/egresos/tab_egresos_previstos.py
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.tab import MDTabsBase
from kivy.lang import Builder
from src.views.egresos.dialog_categoria import DialogGestionCategoria

KV_TAB_EGRESOS_PREVISTOS = '''
<TabEgresosPrevistos>:
    title: "Egresos previstos"

    ScrollView:
        MDBoxLayout:
            orientation: 'vertical'
            padding: "20dp"
            spacing: "15dp"
            size_hint_y: None
            height: self.minimum_height

            MDCard:
                orientation: 'vertical'
                padding: "20dp"
                spacing: "15dp"
                radius:
                elevation: 2
                size_hint_y: None
                height: self.minimum_height

                MDLabel:
                    text: "Gastos presupuestados"
                    font_style: "H6"
                    bold: True
                    theme_text_color: "Custom"
                    text_color: 0.8, 0, 0, 1

                MDTextField:
                    id: selector_categoria_presupuesto
                    text: "Miscelánea - Presupuestado: $ 0.00"
                    readonly: True
                    hint_text: "Categoría Registrada *"
                    helper_text: "Lista desplegable con presupuesto asignado"
                    helper_text_mode: "persistent"
                    icon_right: "menu-down"

                MDTextField:
                    id: monto_categoria_presupuesto
                    text: "0.00"
                    hint_text: "Monto Presupuestado Asignado ($)"
                    helper_text: "Monto límite o estimado para esta categoría"
                    helper_text_mode: "on_focus"
                    input_filter: "float"
                    icon_right: "calculator"

                MDBoxLayout:
                    orientation: 'horizontal'
                    spacing: "10dp"
                    size_hint_y: None
                    height: "50dp"

                    MDFillRoundFlatButton:
                        text: "Modificar Categoría / Presupuesto"
                        icon: "pencil"
                        md_bg_color: 0.8, 0, 0, 1
                        text_color: 1, 1, 1, 1
                        size_hint_x: 1.0
                        on_release: root.abrir_dialogo_modificar()
'''

Builder.load_string(KV_TAB_EGRESOS_PREVISTOS)


class TabEgresosPrevistos(MDFloatLayout, MDTabsBase):
    """Pestaña 2: Planificación y presupuesto de egresos."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.gestor_dialogo = DialogGestionCategoria()

    def abrir_dialogo_modificar(self):
        self.gestor_dialogo.abrir()
