# src/views/ingresos/tab_ingresos_realizados.py
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.tab import MDTabsBase
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.clock import Clock


def formatear_monto_entero(valor):
    try:
        val_int = int(float(valor))
        return f"$ {val_int:,}".replace(",", ".")
    except (ValueError, TypeError):
        return "$ 0"


KV_TAB_INGRESOS_REALIZADOS = '''
<TabIngresosRealizados>:
    title: "Ingresos realizados"

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
                text: "Resumen de Ingresos por Categoría"
                font_style: "H6"
                bold: True
                theme_text_color: "Custom"
                text_color: 0, 0.6, 0, 1
                size_hint_y: None
                height: "30dp"

            # Encabezado de Tabla
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
                    size_hint_x: 0.60

                MDLabel:
                    text: "Total Ingresado ($)"
                    bold: True
                    font_style: "Subtitle2"
                    halign: "right"
                    size_hint_x: 0.40

            ScrollView:
                MDBoxLayout:
                    id: contenedor_resumen_ingresos
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
                on_release: app.ir_a_dashboard(direccion="right")

            MDFillRoundFlatButton:
                text: "Actualizar"
                md_bg_color: 0, 0.6, 0, 1
                text_color: 1, 1, 1, 1
                size_hint_x: 0.6
                on_release: root.cargar_ingresos_por_categoria()
'''

Builder.load_string(KV_TAB_INGRESOS_REALIZADOS)


class TabIngresosRealizados(MDFloatLayout, MDTabsBase):
    """Pestaña 2: Muestra el acumulado ingresado por cada categoría."""

    def on_kv_post(self, base_widget):
        Clock.schedule_once(lambda dt: self.cargar_ingresos_por_categoria(), 0.1)

    def cargar_ingresos_por_categoria(self):
        """Consulta en SQLite el total acumulado agrupado por categoría."""
        contenedor = self.ids.contenedor_resumen_ingresos
        contenedor.clear_widgets()

        app = MDApp.get_running_app()
        resumen = []
        if hasattr(app, "db") and app.db:
            resumen = app.db.obtener_ingresos_por_categoria()

        for item in resumen:
            fila = MDBoxLayout(
                orientation="horizontal",
                size_hint_y=None,
                height="40dp",
                padding=["10dp", "0dp", "10dp", "0dp"]
            )

            lbl_cat = MDLabel(
                text=str(item["categoria"]),
                halign="left",
                size_hint_x=0.60
            )

            lbl_total = MDLabel(
                text=formatear_monto_entero(item["total_ingresado"]),
                halign="right",
                bold=True,
                theme_text_color="Custom",
                text_color=(0, 0.6, 0, 1) if item["total_ingresado"] > 0 else (0.4, 0.4, 0.4, 1),
                size_hint_x=0.40
            )

            fila.add_widget(lbl_cat)
            fila.add_widget(lbl_total)
            contenedor.add_widget(fila)