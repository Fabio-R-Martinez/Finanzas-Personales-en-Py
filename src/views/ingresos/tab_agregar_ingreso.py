# src/views/ingresos/tab_agregar_ingreso.py
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.menu import MDDropdownMenu
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.clock import Clock


def formatear_monto_entero(valor):
    try:
        val_int = int(float(valor))
        return f"$ {val_int:,}".replace(",", ".")
    except (ValueError, TypeError):
        return "$ 0"


KV_TAB_AGREGAR_INGRESO = '''
<TabAgregarIngreso>:
    title: "Agregar Ingreso"

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
                radius: [15, 15, 15, 15]
                elevation: 2
                size_hint_y: None
                height: self.minimum_height

                MDLabel:
                    text: "Nuevo Ingreso"
                    font_style: "H6"
                    bold: True
                    theme_text_color: "Custom"
                    text_color: 0, 0.6, 0, 1

                # Formulario en 2 Columnas
                MDBoxLayout:
                    orientation: 'horizontal'
                    spacing: "20dp"
                    size_hint_y: None
                    height: self.minimum_height

                    # Columna 1: Monto Ingresado y Monto Esperado
                    MDBoxLayout:
                        orientation: 'vertical'
                        spacing: "12dp"
                        size_hint_x: 0.5
                        size_hint_y: None
                        height: self.minimum_height

                        MDTextField:
                            id: campo_monto
                            hint_text: "Monto Ingresado ($) *"
                            helper_text: "Ingrese la cantidad recibida"
                            helper_text_mode: "on_focus"
                            input_filter: "int"
                            icon_right: "currency-usd"
                            on_text: root.evaluar_estado_concepto()

                        MDTextField:
                            id: campo_monto_esperado
                            text: "$ 0"
                            readonly: True
                            hint_text: "Ingreso Esperado ($)"
                            helper_text: "Lectura desde la Base de Datos"
                            helper_text_mode: "persistent"
                            icon_right: "calculator"

                    # Columna 2: Categoría y Concepto (Opcional)
                    MDBoxLayout:
                        orientation: 'vertical'
                        spacing: "12dp"
                        size_hint_x: 0.5
                        size_hint_y: None
                        height: self.minimum_height

                        MDTextField:
                            id: campo_categoria
                            text: "Seleccione Categoría *"
                            readonly: True
                            hint_text: "Categoría de ingreso *"
                            helper_text: "Haga clic para desplegar lista"
                            helper_text_mode: "persistent"
                            icon_right: "menu-down"
                            on_focus: if self.focus: root.abrir_menu_categorias()

                        MDTextField:
                            id: campo_concepto
                            hint_text: "Concepto / Origen (Opcional)"
                            helper_text: "Ej: Sueldo de Octubre, Venta de bicicleta"
                            helper_text_mode: "persistent"
                            icon_right: "text-box-outline"

            # Botones de Acción
            MDBoxLayout:
                orientation: 'horizontal'
                spacing: "10dp"
                size_hint_y: None
                height: "50dp"

                MDFillRoundFlatButton:
                    text: "Cancelar"
                    md_bg_color: 0.5, 0.5, 0.5, 1
                    text_color: 1, 1, 1, 1
                    size_hint_x: 0.4
                    on_release:
                        root.limpiar_campos()
                        app.ir_a_dashboard(direccion="right")

                MDFillRoundFlatButton:
                    text: "Guardar Ingreso"
                    md_bg_color: 0, 0.6, 0, 1
                    text_color: 1, 1, 1, 1
                    size_hint_x: 0.6
                    on_release: root.procesar_guardado()
'''

Builder.load_string(KV_TAB_AGREGAR_INGRESO)


class TabAgregarIngreso(MDFloatLayout, MDTabsBase):
    """Pestaña 1: Registro de ingresos."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.menu_categorias = None
        self.categoria_seleccionada = None

    def on_kv_post(self, base_widget):
        Clock.schedule_once(lambda dt: self.cargar_categoria_inicial(), 0.1)

    def cargar_categoria_inicial(self):
        app = MDApp.get_running_app()
        if hasattr(app, "db") and app.db:
            categorias = app.db.obtener_categorias_ingresos()
            if categorias:
                self.seleccionar_categoria(categorias[0])

    def abrir_menu_categorias(self):
        app = MDApp.get_running_app()
        categorias = []
        if hasattr(app, "db") and app.db:
            categorias = app.db.obtener_categorias_ingresos()

        if not categorias:
            return

        items_menu = [
            {
                "text": f"{cat['nombre']} ({formatear_monto_entero(cat.get('monto_presupuestado', 0))})",
                "viewclass": "OneLineListItem",
                "on_release": lambda c=cat: self.seleccionar_categoria(c),
            }
            for cat in categorias
        ]

        self.menu_categorias = MDDropdownMenu(
            caller=self.ids.campo_categoria,
            items=items_menu,
            width_mult=4,
        )
        self.menu_categorias.open()

    def seleccionar_categoria(self, cat):
        self.categoria_seleccionada = cat
        self.ids.campo_categoria.text = cat["nombre"]
        self.ids.campo_monto_esperado.text = formatear_monto_entero(cat.get("monto_presupuestado", 0))

        if self.menu_categorias:
            self.menu_categorias.dismiss()
            self.menu_categorias = None

    def evaluar_estado_concepto(self):
        pass

    def obtener_datos(self):
        return {
            "categoria": self.ids.campo_categoria.text.strip(),
            "concepto": self.ids.campo_concepto.text.strip(),
            "monto": self.ids.campo_monto.text.strip(),
        }

    def validar_formulario(self):
        """Valida que categoría y monto sean válidos. Concepto es opcional."""
        datos = self.obtener_datos()
        es_valido = True

        if not datos["categoria"] or datos["categoria"] == "Seleccione Categoría *":
            self.ids.campo_categoria.error = True
            es_valido = False

        try:
            monto_int = int(datos["monto"]) if datos["monto"] else 0
            if monto_int <= 0:
                self.ids.campo_monto.error = True
                es_valido = False
        except ValueError:
            self.ids.campo_monto.error = True
            es_valido = False

        return es_valido

    def limpiar_campos(self):
        self.ids.campo_monto.text = ""
        self.ids.campo_concepto.text = ""
        self.ids.campo_monto.error = False
        self.cargar_categoria_inicial()

    def procesar_guardado(self):
        if self.validar_formulario():
            app = MDApp.get_running_app()
            datos = self.obtener_datos()
            if hasattr(app, "guardar_ingreso"):
                app.guardar_ingreso(datos)
            self.limpiar_campos()

