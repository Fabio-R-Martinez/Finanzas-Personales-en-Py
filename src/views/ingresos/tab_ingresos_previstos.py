# src/views/ingresos/tab_ingresos_previstos.py
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.tab import MDTabsBase
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.clock import Clock

from src.views.egresos.dialog_categoria import DialogGestionCategoria, formatear_monto_entero

KV_TAB_INGRESOS_PREVISTOS = '''
<TabIngresosPrevistos>:
    title: "Ingresos previstos"

    MDBoxLayout:
        orientation: 'vertical'
        padding: "15dp"
        spacing: "15dp"

        MDCard:
            orientation: 'vertical'
            padding: "15dp"
            spacing: "10dp"
            radius: [15, 15, 15, 15]
            elevation: 2
            size_hint_y: 1

            MDLabel:
                text: "Ingresos Planificados / Esperados"
                font_style: "H6"
                bold: True
                theme_text_color: "Custom"
                text_color: 0, 0.6, 0, 1
                size_hint_y: None
                height: "30dp"

            # Encabezado
            MDBoxLayout:
                orientation: 'horizontal'
                size_hint_y: None
                height: "35dp"
                padding: ["10dp", "0dp", "10dp", "0dp"]
                md_bg_color: 0.9, 0.9, 0.9, 1

                MDLabel:
                    text: "Categoría de ingreso"
                    bold: True
                    font_style: "Subtitle2"
                    halign: "left"
                    size_hint_x: 0.45

                MDLabel:
                    text: "Monto previsto ($)"
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
                    id: contenedor_filas_ingresos
                    orientation: 'vertical'
                    spacing: "8dp"
                    padding: ["0dp", "5dp", "0dp", "5dp"]
                    size_hint_y: None
                    height: self.minimum_height

        # Botones Inferiores
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
                on_release: root.cancelar_y_volver()

            MDFillRoundFlatButton:
                id: btn_modificar
                text: "Modificar"
                md_bg_color: 0, 0.6, 0, 1
                text_color: 1, 1, 1, 1
                size_hint_x: 0.6
                on_release: root.accion_modificar_confirmar()
'''

Builder.load_string(KV_TAB_INGRESOS_PREVISTOS)


class TabIngresosPrevistos(MDFloatLayout, MDTabsBase):
    """Pestaña 3: Configuración de montos previstos para las 4 categorías fijas de ingresos."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.modo_edicion = False
        self.categoria_seleccionada = None
        self.gestor_dialogo = DialogGestionCategoria()

    def on_kv_post(self, base_widget):
        Clock.schedule_once(lambda dt: self.cargar_categorias(), 0.1)

    def cargar_categorias(self):
        """Consulta SQLite y muestra las 4 categorías con selección interactiva."""
        contenedor = self.ids.contenedor_filas_ingresos
        contenedor.clear_widgets()

        app = MDApp.get_running_app()
        categorias = []
        if hasattr(app, "db") and app.db:
            categorias = app.db.obtener_categorias_ingresos()

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

            lbl_monto = MDLabel(
                text=formatear_monto_entero(cat.get("monto_presupuestado", 0)),
                halign="right",
                bold=True,
                theme_text_color="Custom",
                text_color=(0, 0.6, 0, 1),
                size_hint_x=0.35
            )

            chk_seleccionar = MDCheckbox(
                size_hint_x=0.20,
                active=False,
                disabled=not self.modo_edicion,
                group="grupo_categorias_ingresos"
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

    def accion_modificar_confirmar(self):
        """Alterna entre activar la selección y abrir el diálogo de edición del monto."""
        if not self.modo_edicion:
            self.modo_edicion = True
            self.categoria_seleccionada = None
            self.ids.btn_modificar.text = "Confirmar"
            self.cargar_categorias()
        else:
            if not self.categoria_seleccionada:
                self.gestor_dialogo.abrir_alerta("Marque la casilla de la categoría cuyo monto desea modificar.")
                return

            # Abrir diálogo para editar el monto de la categoría elegida
            self.gestor_dialogo.abrir_dialogo_editar(
                categoria=self.categoria_seleccionada,
                on_modificar=self.guardar_cambios_monto,
                on_eliminar=None  # No se permite eliminar las 4 categorías base
            )

    def guardar_cambios_monto(self, id_cat, nuevo_nombre, nuevo_monto_int):
        app = MDApp.get_running_app()
        if hasattr(app, "db") and app.db:
            app.db.actualizar_categoria_ingreso(id_cat, nuevo_nombre, nuevo_monto_int)
        self.resetear_modo_edicion()

    def resetear_modo_edicion(self):
        self.modo_edicion = False
        self.categoria_seleccionada = None
        self.ids.btn_modificar.text = "Modificar"
        self.cargar_categorias()

    def cancelar_y_volver(self):
        if self.modo_edicion:
            self.resetear_modo_edicion()
        app = MDApp.get_running_app()
        if hasattr(app, "ir_a_dashboard"):
            app.ir_a_dashboard(direccion="right")