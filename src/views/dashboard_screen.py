# src/views/dashboard_screen.py
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivy.lang import Builder


def formatear_monto_entero(valor):
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
                        radius: [15, 15, 15, 15]
                        elevation: 2
                        size_hint_x: 0.5

                        MDBoxLayout:
                            orientation: 'horizontal'
                            spacing: "10dp"
                            size_hint_y: None
                            height: "65dp"

                            MDIconButton:
                                icon: "minus"
                                md_bg_color: 0.8, 0, 0, 1
                                theme_icon_color: "Custom"
                                icon_color: 1, 1, 1, 1
                                pos_hint: {"center_y": 0.5}
                                on_release: app.ir_a_formulario_gasto()

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

                        # Barra de Porcentaje para Gastos (Gasto Rojo sobre 95% Presupuesto Verde)
                        MDProgressBar:
                            id: progreso_gastos
                            value: 0
                            max: 100
                            color: 0.8, 0, 0, 1
                            back_color: 0, 0.7, 0.2, 0.35
                            size_hint_y: None
                            height: "8dp"

                    # TARJETA DERECHA: INGRESOS TOTALES
                    MDCard:
                        orientation: 'vertical'
                        padding: "15dp"
                        spacing: "12dp"
                        radius: [15, 15, 15, 15]
                        elevation: 2
                        size_hint_x: 0.5

                        MDBoxLayout:
                            orientation: 'horizontal'
                            spacing: "10dp"
                            size_hint_y: None
                            height: "65dp"

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

                            MDIconButton:
                                icon: "plus"
                                md_bg_color: 0, 0.6, 0, 1
                                theme_icon_color: "Custom"
                                icon_color: 1, 1, 1, 1
                                pos_hint: {"center_y": 0.5}
                                on_release: if hasattr(app, "ir_a_formulario_ingreso"): app.ir_a_formulario_ingreso()

                        # Barra de Porcentaje para Ingresos (Ingresos Realizados sobre Ingresos Esperados)
                        MDProgressBar:
                            id: progreso_ingresos
                            value: 0
                            max: 100
                            color: 0, 0.6, 0, 1
                            back_color: 0, 0.6, 0, 0.25
                            size_hint_y: None
                            height: "8dp"
'''

Builder.load_string(KV_DASHBOARD_SCREEN)


class DashboardScreen(MDScreen):
    """Pantalla principal del Dashboard."""

    def on_enter(self, *args):
        super().on_enter(*args)
        self.actualizar_dashboard()

    def actualizar_dashboard(self):
        app = MDApp.get_running_app()
        if hasattr(app, "db") and app.db:
            resumen = app.db.obtener_resumen_gastos_dashboard()

            total_gastado = resumen.get("total_gastado", 0.0)
            total_ingresos = resumen.get("total_ingresos", 0.0)
            porcentaje_gastos = resumen.get("porcentaje_gastos", 0.0)
            porcentaje_ingresos = resumen.get("porcentaje_ingresos", 0.0)

            self.ids.lbl_total_gastado.text = formatear_monto_entero(total_gastado)
            self.ids.lbl_total_ingresos.text = formatear_monto_entero(total_ingresos)

            self.ids.progreso_gastos.value = min(100.0, porcentaje_gastos)
            self.ids.progreso_ingresos.value = min(100.0, porcentaje_ingresos)