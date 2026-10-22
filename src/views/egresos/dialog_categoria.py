# src/views/egresos/dialog_categoria.py
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFlatButton, MDFillRoundFlatButton, MDRaisedButton


class DialogGestionCategoria:
    """Clase encargada de construir y mostrar el diálogo emergente para gestionar categorías."""

    def __init__(self):
        self.dialogo = None

    def abrir(self):
        if not self.dialogo:
            contenido = MDBoxLayout(
                orientation="vertical",
                spacing="15dp",
                size_hint_y=None,
                height="100dp"
            )

            lbl_instruccion = MDLabel(
                text="Seleccione la acción a realizar sobre la categoría:",
                font_style="Body2",
                theme_text_color="Secondary",
                size_hint_y=None,
                height="25dp"
            )

            # Línea superior: Modificar | Nueva | Borrar
            linea_opciones = MDBoxLayout(
                orientation="horizontal",
                spacing="8dp",
                size_hint_y=None,
                height="45dp"
            )

            btn_modificar = MDRaisedButton(text="Modificar", size_hint_x=0.33)
            btn_nueva = MDRaisedButton(
                text="Nueva",
                md_bg_color=(0, 0.6, 0, 1),
                text_color=(1, 1, 1, 1),
                size_hint_x=0.33
            )
            btn_borrar = MDRaisedButton(
                text="Borrar",
                md_bg_color=(0.8, 0, 0, 1),
                text_color=(1, 1, 1, 1),
                size_hint_x=0.33
            )

            linea_opciones.add_widget(btn_modificar)
            linea_opciones.add_widget(btn_nueva)
            linea_opciones.add_widget(btn_borrar)

            contenido.add_widget(lbl_instruccion)
            contenido.add_widget(linea_opciones)

            # Línea inferior: Cancelar | Guardar cambios
            self.dialogo = MDDialog(
                title="Gestión de Categorías",
                type="custom",
                content_cls=contenido,
                buttons=[
                    MDFlatButton(
                        text="Cancelar",
                        on_release=lambda x: self.cerrar()
                    ),
                    MDFillRoundFlatButton(
                        text="Guardar cambios",
                        md_bg_color=(0.8, 0, 0, 1),
                        text_color=(1, 1, 1, 1),
                        on_release=lambda x: self.cerrar()
                    ),
                ],
            )
        self.dialogo.open()

    def cerrar(self):
        if self.dialogo:
            self.dialogo.dismiss()
