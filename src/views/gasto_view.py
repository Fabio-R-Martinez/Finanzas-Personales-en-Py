# src/views/gasto_view.py
from kivymd.uix.screen import MDScreen
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDFillRoundFlatButton, MDRaisedButton
from kivy.lang import Builder


class TabGastosEfectuados(MDFloatLayout, MDTabsBase):
    """Pestaña 1: Registro de gastos realizados."""
    pass


class TabEgresosPrevistos(MDFloatLayout, MDTabsBase):
    """Pestaña 2: Planificación y presupuesto de egresos."""
    pass


KV_GASTO = '''
<FormularioGastoScreen>:
    name: "formulario_gasto"

    MDBoxLayout:
        orientation: 'vertical'

        # Título de la pantalla
        MDTopAppBar:
            title: "Egresos"
            elevation: 4

        # Pestañas de navegación
        MDTabs:
            id: tabs

            # =========================================================
            # PESTAÑA 1: GASTOS EFECTUADOS
            # =========================================================
            TabGastosEfectuados:
                title: "Gastos efectuados"

                ScrollView:
                    MDBoxLayout:
                        orientation: 'vertical'
                        padding: "20dp"
                        spacing: "15dp"
                        size_hint_y: None
                        height: self.minimum_height

                        MDCard:
                            orientation: 'vertical'
                            padding: "20dp"
                            spacing: "15dp"
                            radius: [16, 16, 16, 16]
                            elevation: 2
                            size_hint_y: None
                            height: self.minimum_height

                            MDLabel:
                                text: "Gasto efectuado"
                                font_style: "H6"
                                bold: True
                                theme_text_color: "Custom"
                                text_color: 0.8, 0, 0, 1

                            # Distribución limpia en 2 Columnas
                            MDBoxLayout:
                                orientation: 'horizontal'
                                spacing: "20dp"
                                size_hint_y: None
                                height: self.minimum_height

                                # -------------------------------------
                                # COLUMNA 1: Monto Gastado y Presupuestado
                                # -------------------------------------
                                MDBoxLayout:
                                    orientation: 'vertical'
                                    spacing: "12dp"
                                    size_hint_x: 0.5

                                    MDTextField:
                                        id: campo_monto_ejecutado
                                        hint_text: "Monto Gastado ($) *"
                                        helper_text: "Cantidad gastada (Obligatorio)"
                                        helper_text_mode: "on_focus"
                                        input_filter: "float"
                                        icon_right: "currency-usd"

                                    MDTextField:
                                        id: campo_monto_esperado
                                        text: "0.00"
                                        readonly: True
                                        hint_text: "Monto Presupuestado ($)"
                                        helper_text: "Obtenido de la Base de Datos"
                                        helper_text_mode: "persistent"
                                        icon_right: "calculator"

                                # -------------------------------------
                                # COLUMNA 2: Categoría y Artículo / Concepto
                                # -------------------------------------
                                MDBoxLayout:
                                    orientation: 'vertical'
                                    spacing: "12dp"
                                    size_hint_x: 0.5

                                    MDTextField:
                                        id: campo_categoria
                                        text: "Miscelánea"
                                        readonly: True
                                        hint_text: "Categoría *"
                                        helper_text: "Seleccione una categoría (Obligatorio)"
                                        helper_text_mode: "persistent"
                                        icon_right: "menu-down"

                                    MDTextField:
                                        id: campo_descripcion
                                        hint_text: "Artículo / Concepto *"
                                        helper_text: "Ej: Leche, Carne, Servicio de Luz"
                                        helper_text_mode: "on_focus"
                                        icon_right: "text-box-outline"

                        # Botones de Acción para Pestaña 1
                        MDBoxLayout:
                            orientation: 'horizontal'
                            spacing: "10dp"
                            size_hint_y: None
                            height: "50dp"

                            MDFlatButton:
                                text: "Cancelar"
                                size_hint_x: 0.4
                                on_release: 
                                    root.limpiar_campos()
                                    app.ir_a_dashboard()

                            MDFillRoundFlatButton:
                                text: "Guardar Gasto"
                                md_bg_color: 0.8, 0, 0, 1
                                text_color: 1, 1, 1, 1
                                size_hint_x: 0.6
                                on_release: root.procesar_guardado()

            # =========================================================
            # PESTAÑA 2: EGRESOS PREVISTOS
            # =========================================================
            TabEgresosPrevistos:
                title: "Egresos previstos"

                ScrollView:
                    MDBoxLayout:
                        orientation: 'vertical'
                        padding: "20dp"
                        spacing: "15dp"
                        size_hint_y: None
                        height: self.minimum_height

                        MDCard:
                            orientation: 'vertical'
                            padding: "20dp"
                            spacing: "15dp"
                            radius: [16, 16, 16, 16]
                            elevation: 2
                            size_hint_y: None
                            height: self.minimum_height

                            MDLabel:
                                text: "Gastos presupuestados"
                                font_style: "H6"
                                bold: True
                                theme_text_color: "Custom"
                                text_color: 0.8, 0, 0, 1

                            # Desplegable de Categorías con Monto Presupuestado
                            MDTextField:
                                id: selector_categoria_presupuesto
                                text: "Miscelánea - Presupuestado: $ 0.00"
                                readonly: True
                                hint_text: "Categoría Registrada *"
                                helper_text: "Lista desplegable con presupuesto asignado"
                                helper_text_mode: "persistent"
                                icon_right: "menu-down"

                            MDTextField:
                                id: monto_categoria_presupuesto
                                text: "0.00"
                                hint_text: "Monto Presupuestado Asignado ($)"
                                helper_text: "Monto límite o estimado para esta categoría"
                                helper_text_mode: "on_focus"
                                input_filter: "float"
                                icon_right: "calculator"

                            MDBoxLayout:
                                orientation: 'horizontal'
                                spacing: "10dp"
                                size_hint_y: None
                                height: "50dp"

                                MDFillRoundFlatButton:
                                    text: "Modificar Categoría / Presupuesto"
                                    icon: "pencil"
                                    md_bg_color: 0.8, 0, 0, 1
                                    text_color: 1, 1, 1, 1
                                    size_hint_x: 1.0
                                    on_release: root.abrir_dialogo_modificar_categoria()
'''

Builder.load_string(KV_GASTO)


class FormularioGastoScreen(MDScreen):
    """Pantalla de Egresos con pestañas de gastos efectuados y previstos."""

    dialogo_modificar = None

    def obtener_datos(self):
        """Retorna un diccionario con los datos del gasto efectuado."""
        return {
            "categoria": self.ids.campo_categoria.text.strip(),
            "concepto": self.ids.campo_descripcion.text.strip(),
            "monto": self.ids.campo_monto_ejecutado.text.strip(),
            "monto_presupuestado": self.ids.campo_monto_esperado.text.strip(),
        }

    def validar_formulario(self):
        """Valida que Categoría, Artículo/Concepto y Monto no sean nulos ni vacíos."""
        datos = self.obtener_datos()
        es_valido = True

        # Validar Monto
        monto_str = datos["monto"]
        if not monto_str:
            self.ids.campo_monto_ejecutado.error = True
            self.ids.campo_monto_ejecutado.helper_text = "El monto es obligatorio"
            self.ids.campo_monto_ejecutado.helper_text_mode = "on_error"
            es_valido = False
        else:
            try:
                if float(monto_str) <= 0:
                    self.ids.campo_monto_ejecutado.error = True
                    self.ids.campo_monto_ejecutado.helper_text = "El monto debe ser mayor a 0"
                    self.ids.campo_monto_ejecutado.helper_text_mode = "on_error"
                    es_valido = False
                else:
                    self.ids.campo_monto_ejecutado.error = False
            except ValueError:
                self.ids.campo_monto_ejecutado.error = True
                self.ids.campo_monto_ejecutado.helper_text = "Número inválido"
                self.ids.campo_monto_ejecutado.helper_text_mode = "on_error"
                es_valido = False

        # Validar Artículo / Concepto
        if not datos["concepto"]:
            self.ids.campo_descripcion.error = True
            self.ids.campo_descripcion.helper_text = "Ingrese un artículo o concepto"
            self.ids.campo_descripcion.helper_text_mode = "on_error"
            es_valido = False
        else:
            self.ids.campo_descripcion.error = False

        return es_valido

    def limpiar_campos(self):
        """Limpia los campos del formulario."""
        self.ids.campo_descripcion.text = ""
        self.ids.campo_monto_ejecutado.text = ""
        self.ids.campo_monto_ejecutado.error = False
        self.ids.campo_descripcion.error = False

    def procesar_guardado(self):
        """Valida y envía los datos a la App."""
        if self.validar_formulario():
            from kivymd.app import MDApp
            app = MDApp.get_running_app()
            datos = self.obtener_datos()
            app.guardar_gasto(datos)
            self.limpiar_campos()

    def abrir_dialogo_modificar_categoria(self):
        """Abre el diálogo de gestión con las opciones en una línea y botones inferiores."""
        if not self.dialogo_modificar:
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

            btn_modificar = MDRaisedButton(
                text="Modificar",
                size_hint_x=0.33
            )
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
            self.dialogo_modificar = MDDialog(
                title="Gestión de Categorías",
                type="custom",
                content_cls=contenido,
                buttons=[
                    MDFlatButton(
                        text="Cancelar",
                        on_release=lambda x: self.cerrar_dialogo()
                    ),
                    MDFillRoundFlatButton(
                        text="Guardar cambios",
                        md_bg_color=(0.8, 0, 0, 1),
                        text_color=(1, 1, 1, 1),
                        on_release=lambda x: self.cerrar_dialogo()
                    ),
                ],
            )
        self.dialogo_modificar.open()

    def cerrar_dialogo(self):
        """Cierra el diálogo emergente."""
        if self.dialogo_modificar:
            self.dialogo_modificar.dismiss()