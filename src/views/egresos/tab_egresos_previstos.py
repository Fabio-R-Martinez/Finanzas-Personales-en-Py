# src/views/egresos/tab_egresos_previstos.py
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.tab import MDTabsBase
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.clock import Clock

from src.views.egresos.dialog_categoria import DialogGestionCategoria, formatear_monto_entero

KV_TAB_EGRESOS_PREVISTOS = '''
<TabEgresosPrevistos>:
    title: "Egresos previstos"

    MDBoxLayout:
        orientation: 'vertical'
        padding: "15dp"
        spacing: "15dp"

        MDCard:
            orientation: 'vertical'
            padding: "15dp"
            spacing: "10dp"
            radius:
            elevation: 2
            size_hint_y: 1

            MDLabel:
                text: "Gastos presupuestados"
                font_style: "H6"
                bold: True
                theme_text_color: "Custom"
                text_color: 0.8, 0, 0, 1
                size_hint_y: None
                height: "30dp"

            # Encabezado de la Tabla con Alineación Izquierda
            MDBoxLayout:
                orientation: 'horizontal'
                size_hint_y: None
                height: "35dp"
                padding: ["10dp", "0dp", "10dp", "0dp"]
                md_bg_color: 0.9, 0.9, 0.9, 1

                MDLabel:
                    text: "Categoría de gastos"
                    bold: True
                    font_style: "Subtitle2"
                    halign: "left"
                    size_hint_x: 0.45

                MDLabel:
                    text: "Montos asignados"
                    bold: True
                    font_style: "Subtitle2"
                    halign: "right"
                    size_hint_x: 0.35

                MDLabel:
                    text: "Seleccionar"
                    bold: True
                    font_style: "Subtitle2"
                    halign: "center"
                    size_hint_x: 0.20

            # Lista deslizable
            ScrollView:
                MDBoxLayout:
                    id: contenedor_filas
                    orientation: 'vertical'
                    spacing: "8dp"
                    padding: ["0dp", "5dp", "0dp", "5dp"]
                    size_hint_y: None
                    height: self.minimum_height

        # Botones Inferiores Estandarizados
        MDBoxLayout:
            orientation: 'horizontal'
            spacing: "10dp"
            size_hint_y: None
            height: "50dp"

            MDFillRoundFlatButton:
                text: "Volver"
                md_bg_color: 0.5, 0.5, 0.5, 1
                text_color: 1, 1, 1, 1
                size_hint_x: 0.4
                on_release: 
                    root.cancelar_y_volver()

            MDFillRoundFlatButton:
                id: btn_modificar
                text: "Modificar"
                md_bg_color: 0.8, 0, 0, 1
                text_color: 1, 1, 1, 1
                size_hint_x: 0.6
                on_release: root.accion_modificar_confirmar()
'''

Builder.load_string(KV_TAB_EGRESOS_PREVISTOS)


class TabEgresosPrevistos(MDFloatLayout, MDTabsBase):
    """Pestaña 2: Planificación y presupuesto de egresos."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.modo_edicion = False
        self.categoria_seleccionada = None
        self.gestor_dialogo = DialogGestionCategoria()

    def on_kv_post(self, base_widget):
        Clock.schedule_once(lambda dt: self.cargar_categorias(), 0.1)

    def cargar_categorias(self):
        """Consulta SQLite y renderiza los montos encolumnados a la izquierda."""
        contenedor = self.ids.contenedor_filas
        contenedor.clear_widgets()

        app = MDApp.get_running_app()
        categorias = []
        if hasattr(app, "db") and app.db:
            categorias = app.db.obtener_categorias_egresos()

        for cat in categorias:
            fila = MDBoxLayout(
                orientation="horizontal",
                size_hint_y=None,
                height="40dp",
                padding=["10dp", "0dp", "10dp", "0dp"]
            )

            lbl_nombre = MDLabel(
                text=str(cat.get("nombre", "")),
                halign="left",
                size_hint_x=0.45
            )

            # Encolumnado a la derecha
            lbl_monto = MDLabel(
                text=formatear_monto_entero(cat.get("monto_presupuestado", 0)),
                halign="right",
                size_hint_x=0.35
            )

            chk_seleccionar = MDCheckbox(
                size_hint_x=0.20,
                active=False,
                disabled=not self.modo_edicion,
                group="grupo_categorias"
            )

            def on_check(checkbox, value, c=cat):
                if value:
                    self.categoria_seleccionada = c
                elif self.categoria_seleccionada == c:
                    self.categoria_seleccionada = None

            chk_seleccionar.bind(active=on_check)

            fila.add_widget(lbl_nombre)
            fila.add_widget(lbl_monto)
            fila.add_widget(chk_seleccionar)
            contenedor.add_widget(fila)

        # Fila 'Nueva' al activar Modificar
        if self.modo_edicion:
            fila_nueva = MDBoxLayout(
                orientation="horizontal",
                size_hint_y=None,
                height="40dp",
                padding=["10dp", "0dp", "10dp", "0dp"]
            )

            lbl_nombre_nueva = MDLabel(
                text="Nueva",
                bold=True,
                theme_text_color="Custom",
                text_color=(0, 0.6, 0, 1),
                halign="left",
                size_hint_x=0.45
            )
            lbl_monto_nueva = MDLabel(
                text="$ 0",
                halign="left",
                size_hint_x=0.35
            )

            chk_seleccionar_nueva = MDCheckbox(
                size_hint_x=0.20,
                active=False,
                disabled=False,
                group="grupo_categorias"
            )

            def on_check_nueva(checkbox, value):
                if value:
                    self.categoria_seleccionada = "NUEVA"
                elif self.categoria_seleccionada == "NUEVA":
                    self.categoria_seleccionada = None

            chk_seleccionar_nueva.bind(active=on_check_nueva)

            fila_nueva.add_widget(lbl_nombre_nueva)
            fila_nueva.add_widget(lbl_monto_nueva)
            fila_nueva.add_widget(chk_seleccionar_nueva)
            contenedor.add_widget(fila_nueva)

    def accion_modificar_confirmar(self):
        """Alterna entre Modificar y Confirmar."""
        if not self.modo_edicion:
            self.modo_edicion = True
            self.categoria_seleccionada = None
            self.ids.btn_modificar.text = "Confirmar"
            self.cargar_categorias()
        else:
            if not self.categoria_seleccionada:
                self.gestor_dialogo.abrir_alerta("Marque la casilla de la categoría que desea gestionar.")
                return

            if self.categoria_seleccionada == "NUEVA":
                self.gestor_dialogo.abrir_dialogo_nueva(
                    on_guardar=self.guardar_nueva_categoria
                )
            else:
                self.gestor_dialogo.abrir_dialogo_editar(
                    categoria=self.categoria_seleccionada,
                    on_modificar=self.guardar_cambios_categoria,
                    on_eliminar=self.eliminar_categoria
                )

    def guardar_nueva_categoria(self, nombre, monto_int):
        app = MDApp.get_running_app()
        if hasattr(app, "db") and app.db:
            app.db.agregar_categoria_egreso(nombre, monto_int)
        self.resetear_modo_edicion()

    def guardar_cambios_categoria(self, id_cat, nuevo_nombre, nuevo_monto_int):
        app = MDApp.get_running_app()
        if hasattr(app, "db") and app.db:
            app.db.actualizar_categoria_egreso(id_cat, nuevo_nombre, nuevo_monto_int)
        self.resetear_modo_edicion()

    def eliminar_categoria(self, id_cat):
        app = MDApp.get_running_app()
        if hasattr(app, "db") and app.db:
            app.db.eliminar_categoria_egreso(id_cat)
        self.resetear_modo_edicion()

    def cancelar_y_volver(self):
        self.resetear_modo_edicion()
        app = MDApp.get_running_app()
        app.ir_a_dashboard()

    def resetear_modo_edicion(self):
        self.modo_edicion = False
        self.categoria_seleccionada = None
        self.ids.btn_modificar.text = "Modificar"
        self.cargar_categorias()