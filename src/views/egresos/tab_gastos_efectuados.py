#  src/views/egresos/tab_gastos_efectuados.py
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.menu import MDDropdownMenu
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.clock import Clock


def formatear_monto_entero(valor):
    """Convierte un valor numérico a entero formateado con puntos para miles ($ 1.000)."""
    try:
        val_int = int(float(valor))
        return f"$ {val_int:,}".replace(",", ".")
    except (ValueError, TypeError):
        return "$ 0"


KV_TAB_GASTOS_EFECTUADOS = '''
<TabGastosEfectuados>:
    title: "Agregar Gasto"

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
                    text: "Nuevo Gasto"
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

                    # Columna 1: Monto Gastado y Monto Presupuestado
                    MDBoxLayout:
                        orientation: 'vertical'
                        spacing: "12dp"
                        size_hint_x: 0.5
                        size_hint_y: None
                        height: self.minimum_height

                        MDTextField:
                            id: campo_monto_ejecutado
                            hint_text: "Monto Gastado ($) *"
                            helper_text: "Ingrese la cantidad gastada"
                            helper_text_mode: "on_focus"
                            input_filter: "int"
                            icon_right: "currency-usd"
                            on_text: root.evaluar_estado_concepto()

                        MDTextField:
                            id: campo_monto_esperado
                            text: "$ 0"
                            readonly: True
                            hint_text: "Monto Presupuestado ($)"
                            helper_text: "Lectura desde la Base de Datos"
                            helper_text_mode: "persistent"
                            icon_right: "calculator"

                    # Columna 2: Categoría (Desplegable) y Artículo / Servicio
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
                            hint_text: "Categoría presupuestada *"
                            helper_text: "Haga clic para desplegar lista"
                            helper_text_mode: "persistent"
                            icon_right: "menu-down"
                            on_focus: if self.focus: root.abrir_menu_categorias()

                        MDTextField:
                            id: campo_descripcion
                            disabled: True
                            hint_text: "Artículo o Servicio *"
                            helper_text: "Se activa al ingresar el monto gastado"
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
    """Pestaña 1: Registro de gastos realizados conectado a la BD."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.menu_categorias = None
        self.categoria_seleccionada = None

    def on_kv_post(self, base_widget):
        Clock.schedule_once(lambda dt: self.cargar_categoria_inicial(), 0.1)

    def cargar_categoria_inicial(self):
        """Carga la primera categoría disponible en la BD por defecto."""
        app = MDApp.get_running_app()
        if hasattr(app, "db") and app.db:
            categorias = app.db.obtener_categorias_egresos()
            if categorias:
                cat = categorias[0]
                self.seleccionar_categoria(cat)

    def abrir_menu_categorias(self):
        """Despliega la lista flotante con las categorías presupuestadas desde SQLite."""
        app = MDApp.get_running_app()
        categorias = []
        if hasattr(app, "db") and app.db:
            categorias = app.db.obtener_categorias_egresos()

        if not categorias:
            return

        items_menu = [
            {
                "text": f"{cat['nombre']} ({formatear_monto_entero(cat['monto_presupuestado'])})",
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
        """Establece la categoría elegida y actualiza el monto presupuestado correspondiente."""
        self.categoria_seleccionada = cat
        self.ids.campo_categoria.text = cat["nombre"]
        self.ids.campo_monto_esperado.text = formatear_monto_entero(
            cat["monto_presupuestado"]
        )

        if self.menu_categorias:
            self.menu_categorias.dismiss()
            self.menu_categorias = None

    def evaluar_estado_concepto(self):
        """
        Activa el campo 'Artículo o Servicio' únicamente cuando se
        ingresa un monto gastado válido (mayor a 0).
        """
        monto_str = self.ids.campo_monto_ejecutado.text.strip()
        try:
            monto_val = int(monto_str) if monto_str else 0
            if monto_val > 0:
                self.ids.campo_descripcion.disabled = False
                self.ids.campo_descripcion.helper_text = (
                    "Ingrese el nombre del artículo o servicio *"
                )
                self.ids.campo_monto_ejecutado.error = False
            else:
                self.ids.campo_descripcion.disabled = True
                self.ids.campo_descripcion.text = ""
                self.ids.campo_descripcion.helper_text = (
                    "Se activa al ingresar el monto gastado"
                )
        except ValueError:
            self.ids.campo_descripcion.disabled = True
            self.ids.campo_descripcion.text = ""

    def obtener_datos(self):
        """Retorna los datos del formulario listos para registrar."""
        return {
            "categoria": self.ids.campo_categoria.text.strip(),
            "concepto": self.ids.campo_descripcion.text.strip(),
            "monto": self.ids.campo_monto_ejecutado.text.strip(),
            "monto_presupuestado": self.ids.campo_monto_esperado.text.strip(),
        }

    def validar_formulario(self):
        """Valida que categoría, monto gastado y artículo/servicio estén completos."""
        datos = self.obtener_datos()
        es_valido = True

        if (
            not datos["categoria"]
            or datos["categoria"] == "Seleccione Categoría *"
        ):
            self.ids.campo_categoria.error = True
            es_valido = False

        try:
            monto_int = int(datos["monto"]) if datos["monto"] else 0
            if monto_int <= 0:
                self.ids.campo_monto_ejecutado.error = True
                self.ids.campo_monto_ejecutado.helper_text = (
                    "Ingrese un monto mayor a 0"
                )
                self.ids.campo_monto_ejecutado.helper_text_mode = "on_error"
                es_valido = False
        except ValueError:
            self.ids.campo_monto_ejecutado.error = True
            es_valido = False

        if not datos["concepto"]:
            self.ids.campo_descripcion.error = True
            self.ids.campo_descripcion.helper_text = (
                "Ingrese el artículo o servicio"
            )
            self.ids.campo_descripcion.helper_text_mode = "on_error"
            es_valido = False

        return es_valido

    def limpiar_campos(self):
        """Restablece los campos a su estado inicial."""
        self.ids.campo_monto_ejecutado.text = ""
        self.ids.campo_descripcion.text = ""
        self.ids.campo_descripcion.disabled = True
        self.ids.campo_monto_ejecutado.error = False
        self.ids.campo_descripcion.error = False
        self.cargar_categoria_inicial()

    def procesar_guardado(self):
        """Valida, registra la transacción en SQLite y ¿sigue en la pestaña?."""
        if self.validar_formulario():
            app = MDApp.get_running_app()
            datos = self.obtener_datos()
            if hasattr(app, "guardar_gasto"):
                app.guardar_gasto(datos)
            self.limpiar_campos()