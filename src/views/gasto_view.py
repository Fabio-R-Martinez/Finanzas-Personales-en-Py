# src/views/gasto_view.py
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder

KV_GASTO = '''
<FormularioGastoScreen>:
    name: "formulario_gasto"

    MDBoxLayout:
        orientation: 'vertical'

        MDTopAppBar:
            title: "Registrar Nuevo Gasto"
            elevation: 4

        ScrollView:
            MDBoxLayout:
                orientation: 'vertical'
                padding: "20dp"
                spacing: "20dp"
                size_hint_y: None
                height: self.minimum_height

                MDCard:
                    orientation: 'vertical'
                    padding: "20dp"
                    spacing: "15dp"
                    radius: [16, 16, 16, 16]
                    elevation: 2
                    size_hint_y: None
                    height: self.minimum_height

                    MDLabel:
                        text: "Detalle del Gasto"
                        font_style: "H6"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: 0.8, 0, 0, 1

                    MDTextField:
                        id: campo_concepto
                        hint_text: "Concepto / Descripción"
                        helper_text: "Ej: Supermercado, Alquiler, Luz"
                        helper_text_mode: "on_focus"
                        icon_right: "text-box-outline"

                    MDTextField:
                        id: campo_monto_ejecutado
                        hint_text: "Monto Gastado ($)"
                        helper_text: "Ingrese la cantidad gastada"
                        helper_text_mode: "on_focus"
                        input_filter: "float"
                        icon_right: "currency-usd"

                    MDTextField:
                        id: campo_monto_esperado
                        text: "0"
                        readonly: True
                        hint_text: "Monto Presupuestado ($)"
                        helper_text: "Obtenido de la Base de Datos"
                        helper_text_mode: "persistent"
                        icon_right: "calculator"

                    MDTextField:
                        id: campo_categoria
                        text: "Miscelánea"
                        readonly: True
                        hint_text: "Categoría"
                        helper_text: "Categoría por defecto"
                        helper_text_mode: "persistent"
                        icon_right: "tag-outline"

                MDBoxLayout:
                    orientation: 'horizontal'
                    spacing: "10dp"
                    size_hint_y: None
                    height: "50dp"

                    MDFlatButton:
                        text: "Cancelar"
                        size_hint_x: 0.4
                        on_release: app.ir_a_dashboard()

                    MDFillRoundFlatButton:
                        text: "Guardar Gasto"
                        md_bg_color: 0.8, 0, 0, 1
                        text_color: 1, 1, 1, 1
                        size_hint_x: 0.6
                        on_release: app.guardar_gasto()
'''

Builder.load_string(KV_GASTO)


class FormularioGastoScreen(MDScreen):
    """Pantalla del formulario para registrar un nuevo gasto."""
    pass
