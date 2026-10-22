# main.py
import os
from kivy.config import Config

# Desactivar gestos multitáctiles en Linux para evitar congelamientos
Config.set('input', 'mouse', 'mouse,disable_multitouch')

from kivymd.app import MDApp
from kivy.lang import Builder
from src.database.db_manager import DBManager

# Diseño de la interfaz gráfica actualizado
KV_LAYOUT = '''
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

        Widget:
'''

class FinanzasApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.theme_style = "Light"

        # Inicializar la base de datos
        db = DBManager()

        # Cargar y retornar la interfaz gráfica
        return Builder.load_string(KV_LAYOUT)


if __name__ == "__main__":
    FinanzasApp().run()