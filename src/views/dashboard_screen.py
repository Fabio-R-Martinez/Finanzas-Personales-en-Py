# src/views/dashboard_screen.py
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivy.lang import Builder


def formatear_monto_entero(valor):
    """Formatea valores numéricos como enteros con puntos para miles ($ 1.000)."""
    try:
        val_int = int(float(valor))
        return f"$ {val_int:,}".replace(",", ".")
    except (ValueError, TypeError):
        return "$ 0"


KV_DASHBOARD_SCREEN = '''
<DashboardScreen>:
    name: "dashboard"

    MDBoxLayout:
        orientation: 'vertical'

        MDTopAppBar:
            title: "Gestor de Finanzas Personales"
            elevation: 4

        ScrollView:
            MDBoxLayout:
                orientation: 'vertical'
                padding: "15dp"
                spacing: "15dp"
                size_hint_y: None
                height: self.minimum_height

                # FILA HORIZONTAL: GASTOS (Izquierda) e INGRESOS (Derecha)
                MDBoxLayout:
                    orientation: 'horizontal'
                    spacing: "15dp"
                    size_hint_y: None
                    height: "150dp"

                    # TARJETA IZQUIERDA: GASTOS TOTALES
                    MDCard:
                        orientation: 'vertical'
                        padding: "15dp"
                        spacing: "12dp"
                        radius:
                        elevation: 2
                        size_hint_x: 0.5

                        # Bloque Superior: [ Botón Rojo ]  +  [ Gastos / $$$$ (Alineado a la derecha) ]
                        MDBoxLayout:
                            orientation: 'horizontal'
                            spacing: "10dp"
                            size_hint_y: None
                            height: "65dp"

                            # Botón circular rojo
                            MDIconButton:
                                icon: "minus"
                                md_bg_color: 0.8, 0, 0, 1
                                theme_icon_color: "Custom"
                                icon_color: 1, 1, 1, 1
                                pos_hint: {"center_y": 0.5}
                                on_release: app.ir_a_formulario_gasto()

                            # Textos de Gastos (Alineados a la derecha cerca del centro)
                            MDBoxLayout:
                                orientation: 'vertical'
                                spacing: "2dp"
                                pos_hint: {"center_y": 0.5}

                                MDLabel:
                                    text: "Gastos"
                                    font_style: "Subtitle1"
                                    bold: True
                                    halign: "right"
                                    theme_text_color: "Custom"
                                    text_color: 0.8, 0, 0, 1

                                MDLabel:
                                    id: lbl_total_gastado
                                    text: "$ 0"
                                    font_style: "H5"
                                    bold: True
                                    halign: "right"
                                    theme_text_color: "Custom"
                                    text_color: 0.8, 0, 0, 1

                        # Barra de Porcentaje (Gasto Rojo sobre 95% Presupuesto Verde)
                        MDProgressBar:
                            id: progreso_gastos
                            value: 0
                            max: 100
                            color: 0.8, 0, 0, 1             # Barra de gastos (Rojo)
                            back_color: 0, 0.7, 0.2, 0.35     # Indicador del 95% (Verde)
                            size_hint_y: None
                            height: "8dp"

                    # TARJETA DERECHA: INGRESOS TOTALES
                    MDCard:
                        orientation: 'vertical'
                        padding: "15dp"
                        spacing: "12dp"
                        radius:
                        elevation: 2
                        size_hint_x: 0.5

                        # Bloque Superior: [ Ingresos / $$$$ (Alineado a la izquierda) ]  +  [ Botón Verde ]
                        MDBoxLayout:
                            orientation: 'horizontal'
                            spacing: "10dp"
                            size_hint_y: None
                            height: "65dp"

                            # Textos de Ingresos (Alineados a la izquierda cerca del centro)
                            MDBoxLayout:
                                orientation: 'vertical'
                                spacing: "2dp"
                                pos_hint: {"center_y": 0.5}

                                MDLabel:
                                    text: "Ingresos"
                                    font_style: "Subtitle1"
                                    bold: True
                                    halign: "left"
                                    theme_text_color: "Custom"
                                    text_color: 0, 0.6, 0, 1

                                MDLabel:
                                    id: lbl_total_ingresos
                                    text: "$ 0"
                                    font_style: "H5"
                                    bold: True
                                    halign: "left"
                                    theme_text_color: "Custom"
                                    text_color: 0, 0.6, 0, 1

                            # Botón circular verde
                            MDIconButton:
                                icon: "plus"
                                md_bg_color: 0, 0.6, 0, 1
                                theme_icon_color: "Custom"
                                icon_color: 1, 1, 1, 1
                                pos_hint: {"center_y": 0.5}
                                on_release: if hasattr(app, "ir_a_formulario_ingreso"): app.ir_a_formulario_ingreso()

                        # Barra de Porcentaje para Ingresos
                        MDProgressBar:
                            id: progreso_ingresos
                            value: 0
                            max: 100
                            color: 0, 0.6, 0, 1
                            back_color: 0.8, 0.8, 0.8, 0.35
                            size_hint_y: None
                            height: "8dp"
'''

Builder.load_string(KV_DASHBOARD_SCREEN)


class DashboardScreen(MDScreen):
    """Pantalla Principal Dashboard."""

    def on_enter(self, *args):
        """Actualiza los datos automáticamente al ingresar a la pantalla."""
        super().on_enter(*args)
        self.actualizar_dashboard()

    def actualizar_dashboard(self):
        """Lee SQLite y actualiza el total gastado y la línea de relación con el 95% del presupuesto."""
        app = MDApp.get_running_app()
        if hasattr(app, "db") and app.db:
            resumen = app.db.obtener_resumen_gastos_dashboard()

            total_gastado = resumen["total_gastado"]
            porcentaje = resumen["porcentaje"]

            # Actualiza el monto total de gastos
            self.ids.lbl_total_gastado.text = formatear_monto_entero(total_gastado)

            # Actualiza la relación visual en la barra de progreso
            self.ids.progreso_gastos.value = min(100.0, porcentaje)