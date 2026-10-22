# src/views/dashboard_view.py
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder

KV_DASHBOARD = '''
<DashboardScreen>:
    name: "dashboard"

    MDBoxLayout:
        orientation: 'vertical'

        MDTopAppBar:
            title: "Finanzas Personales"
            elevation: 4

        MDBoxLayout:
            orientation: 'vertical'
            padding: "20dp"
            spacing: "15dp"

            # Tarjeta Balance General
            MDCard:
                size_hint_y: None
                height: "90dp"
                padding: "15dp"
                radius: [16, 16, 16, 16]
                elevation: 2

                MDBoxLayout:
                    orientation: 'vertical'
                    MDLabel:
                        text: "Balance General"
                        font_style: "H6"
                        bold: True
                    MDLabel:
                        text: "Control presupuestario familiar"
                        theme_text_color: "Secondary"

            MDBoxLayout:
                orientation: 'horizontal'
                spacing: "10dp"
                size_hint_y: None
                height: "100dp"

                # Tarjeta de Ingresos
                MDCard:
                    padding: "10dp"
                    elevation: 1
                    radius: [16, 16, 16, 16]
                    size_hint_y: None
                    height: "100dp"

                    MDBoxLayout:
                        orientation: 'horizontal'
                        spacing: "10dp"

                        MDBoxLayout:
                            orientation: 'vertical'
                            size_hint_x: 0.7
                            pos_hint: {"center_y": 0.5}

                            MDLabel:
                                text: "Ingresos Totales"
                                theme_text_color: "Secondary"
                                font_style: "Caption"
                            MDLabel:
                                text: "$ 0.00"
                                font_style: "H5"
                                theme_text_color: "Custom"
                                text_color: 0, 0.6, 0, 1

                        MDFillRoundFlatButton:
                            text: "+"
                            font_size: "32sp"
                            bold: True
                            md_bg_color: 0, 0.6, 0, 1
                            text_color: 1, 1, 1, 1
                            size_hint: None, 0.85
                            width: self.height
                            pos_hint: {"center_y": 0.5}

                # Tarjeta de Gastos
                MDCard:
                    padding: "10dp"
                    elevation: 1
                    radius: [16, 16, 16, 16]
                    size_hint_y: None
                    height: "100dp"

                    MDBoxLayout:
                        orientation: 'horizontal'
                        spacing: "10dp"

                        MDBoxLayout:
                            orientation: 'vertical'
                            size_hint_x: 0.7
                            pos_hint: {"center_y": 0.5}

                            MDLabel:
                                text: "Gastos Totales"
                                theme_text_color: "Secondary"
                                font_style: "Caption"
                            MDLabel:
                                text: "$ 0.00"
                                font_style: "H5"
                                theme_text_color: "Custom"
                                text_color: 0.8, 0, 0, 1

                        MDFillRoundFlatButton:
                            text: "-"
                            font_size: "32sp"
                            bold: True
                            md_bg_color: 0.8, 0, 0, 1
                            text_color: 1, 1, 1, 1
                            size_hint: None, 0.85
                            width: self.height
                            pos_hint: {"center_y": 0.5}
                            on_release: app.ir_a_formulario_gasto()

            Widget:
'''

Builder.load_string(KV_DASHBOARD)


class DashboardScreen(MDScreen):
    """Pantalla principal con el resumen financiero."""
    pass