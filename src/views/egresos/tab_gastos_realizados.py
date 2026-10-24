# src/views/egresos/tab_gastos_realizados.py
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.tab import MDTabsBase
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


KV_TAB_GASTOS_REALIZADOS = '''
<TabGastosRealizados>:
    title: "Gastos realizados"

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
                text: "Resumen de Gastos por Categoría"
                font_style: "H6"
                bold: True
                theme_text_color: "Custom"
                text_color: 0.8, 0, 0, 1
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
                    text: "Categoría"
                    bold: True
                    font_style: "Subtitle2"
                    halign: "left"
                    size_hint_x: 0.60

                MDLabel:
                    text: "Total Gastado ($)"
                    bold: True
                    font_style: "Subtitle2"
                    halign: "right"
                    size_hint_x: 0.40

            # Contenedor con scroll para las categorías y sus totales
            ScrollView:
                MDBoxLayout:
                    id: contenedor_resumen
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
                on_release: app.ir_a_dashboard()

            MDFillRoundFlatButton:
                text: "Actualizar"
                md_bg_color: 0.8, 0, 0, 1
                text_color: 1, 1, 1, 1
                size_hint_x: 0.6
                on_release: root.cargar_gastos_por_categoria()
'''

Builder.load_string(KV_TAB_GASTOS_REALIZADOS)


class TabGastosRealizados(MDFloatLayout, MDTabsBase):
    """Pestaña 2: Muestra el acumulado gastado por cada categoría."""

    def on_kv_post(self, base_widget):
        Clock.schedule_once(lambda dt: self.cargar_gastos_por_categoria(), 0.1)

    def cargar_gastos_por_categoria(self):
        """Consulta en la BD el total ejecutado agrupado por categoría."""
        contenedor = self.ids.contenedor_resumen
        contenedor.clear_widgets()

        app = MDApp.get_running_app()
        resumen = []
        if hasattr(app, "db") and app.db:
            resumen = app.db.obtener_gastos_por_categoria()

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
                text=formatear_monto_entero(item["total_gastado"]),
                halign="right",
                bold=True,
                theme_text_color="Custom",
                text_color=(0.8, 0, 0, 1) if item["total_gastado"] > 0 else (0.4, 0.4, 0.4, 1),
                size_hint_x=0.40
            )

            fila.add_widget(lbl_cat)
            fila.add_widget(lbl_total)
            contenedor.add_widget(fila)