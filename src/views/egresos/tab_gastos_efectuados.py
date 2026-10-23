# src/views/egresos/tab_gastos_efectuados.py
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.tab import MDTabsBase
from kivy.lang import Builder

KV_TAB_GASTOS_EFECTUADOS = '''
<TabGastosEfectuados>:
    title: "Gastos efectuados"

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
                radius: [16, 16, 16, 16]
                elevation: 2
                size_hint_y: None
                height: self.minimum_height

                MDLabel:
                    text: "Gasto efectuado"
                    font_style: "H6"
                    bold: True
                    theme_text_color: "Custom"
                    text_color: 0.8, 0, 0, 1

                # Formulario en 2 Columnas
                MDBoxLayout:
                    orientation: 'horizontal'
                    spacing: "20dp"
                    size_hint_y: None
                    height: self.minimum_height

                    # Columna 1: Monto Gastado y Presupuestado
                    MDBoxLayout:
                        orientation: 'vertical'
                        spacing: "12dp"
                        size_hint_x: 0.5
                        size_hint_y: None
                        height: self.minimum_height

                        MDTextField:
                            id: campo_monto_ejecutado
                            hint_text: "Monto Gastado ($) *"
                            helper_text: "Cantidad gastada (Obligatorio)"
                            helper_text_mode: "on_focus"
                            input_filter: "float"
                            icon_right: "currency-usd"

                        MDTextField:
                            id: campo_monto_esperado
                            text: "0.00"
                            readonly: True
                            hint_text: "Monto Presupuestado ($)"
                            helper_text: "Obtenido de la Base de Datos"
                            helper_text_mode: "persistent"
                            icon_right: "calculator"

                    # Columna 2: Categoría y Artículo / Concepto
                    MDBoxLayout:
                        orientation: 'vertical'
                        spacing: "12dp"
                        size_hint_x: 0.5
                        size_hint_y: None
                        height: self.minimum_height

                        MDTextField:
                            id: campo_categoria
                            text: "Miscelánea"
                            readonly: True
                            hint_text: "Categoría *"
                            helper_text: "Seleccione una categoría (Obligatorio)"
                            helper_text_mode: "persistent"
                            icon_right: "menu-down"

                        MDTextField:
                            id: campo_descripcion
                            hint_text: "Artículo / Concepto *"
                            helper_text: "Ej: Leche, Carne, Servicio de Luz"
                            helper_text_mode: "on_focus"
                            icon_right: "text-box-outline"

            # Botones de Acción
            MDBoxLayout:
                orientation: 'horizontal'
                spacing: "10dp"
                size_hint_y: None
                height: "50dp"

                MDFlatButton:
                    text: "Cancelar"
                    size_hint_x: 0.4
                    on_release: 
                        root.limpiar_campos()
                        app.ir_a_dashboard()

                MDFillRoundFlatButton:
                    text: "Guardar Gasto"
                    md_bg_color: 0.8, 0, 0, 1
                    text_color: 1, 1, 1, 1
                    size_hint_x: 0.6
                    on_release: root.procesar_guardado()
'''

Builder.load_string(KV_TAB_GASTOS_EFECTUADOS)


class TabGastosEfectuados(MDFloatLayout, MDTabsBase):
    """Pestaña 1: Registro de gastos realizados."""

    def obtener_datos(self):
        """Retorna los datos ingresados en el formulario."""
        return {
            "categoria": self.ids.campo_categoria.text.strip(),
            "concepto": self.ids.campo_descripcion.text.strip(),
            "monto": self.ids.campo_monto_ejecutado.text.strip(),
            "monto_presupuestado": self.ids.campo_monto_esperado.text.strip(),
        }

    def validar_formulario(self):
        """Valida que los campos obligatorios no estén vacíos ni sean inválidos."""
        datos = self.obtener_datos()
        es_valido = True

        # Validar Monto
        monto_str = datos["monto"]
        if not monto_str:
            self.ids.campo_monto_ejecutado.error = True
            self.ids.campo_monto_ejecutado.helper_text = "El monto es obligatorio"
            self.ids.campo_monto_ejecutado.helper_text_mode = "on_error"
            es_valido = False
        else:
            try:
                if float(monto_str) <= 0:
                    self.ids.campo_monto_ejecutado.error = True
                    self.ids.campo_monto_ejecutado.helper_text = "El monto debe ser mayor a 0"
                    self.ids.campo_monto_ejecutado.helper_text_mode = "on_error"
                    es_valido = False
                else:
                    self.ids.campo_monto_ejecutado.error = False
            except ValueError:
                self.ids.campo_monto_ejecutado.error = True
                self.ids.campo_monto_ejecutado.helper_text = "Número inválido"
                self.ids.campo_monto_ejecutado.helper_text_mode = "on_error"
                es_valido = False

        # Validar Artículo / Concepto
        if not datos["concepto"]:
            self.ids.campo_descripcion.error = True
            self.ids.campo_descripcion.helper_text = "Ingrese un artículo o concepto"
            self.ids.campo_descripcion.helper_text_mode = "on_error"
            es_valido = False
        else:
            self.ids.campo_descripcion.error = False

        return es_valido

    def limpiar_campos(self):
        """Limpia los campos del formulario."""
        self.ids.campo_descripcion.text = ""
        self.ids.campo_monto_ejecutado.text = ""
        self.ids.campo_monto_ejecutado.error = False
        self.ids.campo_descripcion.error = False

    def procesar_guardado(self):
        """Procesa el guardado si el formulario es válido."""
        if self.validar_formulario():
            from kivymd.app import MDApp
            app = MDApp.get_running_app()
            app.guardar_gasto(self.obtener_datos())
            self.limpiar_campos()