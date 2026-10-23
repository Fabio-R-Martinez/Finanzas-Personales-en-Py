# src/views/egresos/dialog_categoria.py
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDFillRoundFlatButton
from kivy.uix.widget import Widget


def formatear_monto_entero(valor):
    """Convierte un valor numérico a entero formateado con puntos para miles ($ 1.000)."""
    try:
        val_int = int(float(valor))
        return f"$ {val_int:,}".replace(",", ".")
    except (ValueError, TypeError):
        return "$ 0"


class DialogGestionCategoria:
    """Maneja los cuadros modales para agregar, modificar y eliminar categorías."""

    def __init__(self):
        self.dialogo = None

    def abrir_alerta(self, mensaje):
        """Muestra una alerta si no se ha marcado ninguna casilla."""
        self.cerrar()
        self.dialogo = MDDialog(
            title="Selección Requerida",
            text=mensaje,
            buttons=[
                MDFillRoundFlatButton(
                    text="Entendido",
                    md_bg_color=(0, 0.5, 0.8, 1),
                    text_color=(1, 1, 1, 1),
                    on_release=lambda x: self.cerrar()
                )
            ]
        )
        self.dialogo.open()

    def abrir_dialogo_nueva(self, on_guardar):
        """Modal para crear una nueva categoría."""
        self.cerrar()

        contenido = MDBoxLayout(
            orientation="vertical",
            spacing="12dp",
            size_hint_y=None,
            height="130dp"
        )

        tf_nombre = MDTextField(
            hint_text="Nombre de la categoría *",
            helper_text="Ej: Alimentación, Salud, Educación",
            helper_text_mode="on_focus"
        )
        tf_monto = MDTextField(
            text="0",
            hint_text="Monto Presupuestado ($) *",
            helper_text="Solo números enteros mayores a 0",
            helper_text_mode="on_focus",
            input_filter="int"
        )

        contenido.add_widget(tf_nombre)
        contenido.add_widget(tf_monto)

        def aceptar_accion(x):
            nombre = tf_nombre.text.strip()
            monto_str = tf_monto.text.strip()

            try:
                monto_int = int(monto_str) if monto_str else 0
            except ValueError:
                monto_int = 0

            # Descartar si es 'Nueva', vacía o con monto 0
            if not nombre or nombre.lower() == "nueva" or monto_int <= 0:
                self.cerrar()
                return

            self.cerrar()
            on_guardar(nombre, monto_int)

        btn_cancelar = MDFillRoundFlatButton(
            text="Cancelar",
            md_bg_color=(0.5, 0.5, 0.5, 1),
            text_color=(1, 1, 1, 1),
            on_release=lambda x: self.cerrar()
        )

        btn_aceptar = MDFillRoundFlatButton(
            text="Aceptar",
            md_bg_color=(0, 0.6, 0, 1),
            text_color=(1, 1, 1, 1),
            on_release=aceptar_accion
        )

        self.dialogo = MDDialog(
            title="Agregar Nueva Categoría",
            type="custom",
            content_cls=contenido,
            buttons=[
                btn_cancelar,
                btn_aceptar
            ]
        )
        self.dialogo.open()

    def abrir_dialogo_editar(self, categoria, on_modificar, on_eliminar):
        """Modal con Eliminar a la izquierda, Cancelar y Aceptar a la derecha."""
        self.cerrar()

        contenido = MDBoxLayout(
            orientation="vertical",
            spacing="12dp",
            size_hint_y=None,
            height="130dp"
        )

        monto_actual_int = int(float(categoria.get("monto_presupuestado", 0)))

        tf_nombre = MDTextField(
            text=categoria.get("nombre", ""),
            hint_text="Nombre de la categoría *",
            helper_text="Modifique el nombre de la categoría",
            helper_text_mode="on_focus"
        )
        tf_monto = MDTextField(
            text=str(monto_actual_int),
            hint_text="Monto Presupuestado ($) *",
            helper_text="Modifique el monto entero asignado",
            helper_text_mode="on_focus",
            input_filter="int"
        )

        contenido.add_widget(tf_nombre)
        contenido.add_widget(tf_monto)

        def aceptar_accion(x):
            nuevo_nombre = tf_nombre.text.strip()
            nuevo_monto_str = tf_monto.text.strip()

            try:
                monto_int = int(nuevo_monto_str) if nuevo_monto_str else 0
            except ValueError:
                monto_int = 0

            if not nuevo_nombre or monto_int <= 0:
                self.cerrar()
                return

            self.cerrar()
            on_modificar(categoria["id"], nuevo_nombre, monto_int)

        def eliminar_accion(x):
            self.cerrar()
            on_eliminar(categoria["id"])

        btn_eliminar = MDFillRoundFlatButton(
            text="Eliminar",
            md_bg_color=(0.8, 0, 0, 1),
            text_color=(1, 1, 1, 1),
            on_release=eliminar_accion
        )

        btn_cancelar = MDFillRoundFlatButton(
            text="Cancelar",
            md_bg_color=(0.5, 0.5, 0.5, 1),
            text_color=(1, 1, 1, 1),
            on_release=lambda x: self.cerrar()
        )

        btn_aceptar = MDFillRoundFlatButton(
            text="Aceptar",
            md_bg_color=(0, 0.6, 0, 1),
            text_color=(1, 1, 1, 1),
            on_release=aceptar_accion
        )

        # Distribuir: Eliminar (izq) | Spacer | Cancelar + Aceptar (der)
        self.dialogo = MDDialog(
            title=f"Gestionar: {categoria.get('nombre', '')}",
            type="custom",
            content_cls=contenido,
            buttons=[
                btn_eliminar,
                Widget(size_hint_x=1),
                btn_cancelar,
                btn_aceptar
            ]
        )
        self.dialogo.open()

    def cerrar(self):
        if self.dialogo:
            self.dialogo.dismiss()
            self.dialogo = None