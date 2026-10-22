""" 
1. Código Kivy/KivyMD: Diseño de Pantallas (KV Language)
La interfaz móvil está estructurada en un gestor de pantallas (MDScreenManager) con tres vistas principales:

    DashboardScreen: Muestra las tarjetas visuales de resumen (Ingresos, Gastos, Balance/Ahorro), barras de progreso de ejecución y el banner de diagnóstico financiero.
    IngresosScreen: Lista detallada por categoría con montos planificados vs. reales de ingresos.
    GastosScreen: Lista detallada por categoría marcando en color rojo las partidas que hayan excedido el presupuesto.
 """

#:import fmt_moneda __main__.fmt_moneda

<DashboardScreen>:
    name: 'dashboard'
    BoxLayout:
        orientation: 'vertical'
        
        # Barra Superior de Navegación
        MDTopAppBar:
            title: "Gestor Financiero Familiar"
            right_action_items: [["refresh", lambda x: root.actualizar_dashboard()]]
            elevation: 3

        ScrollView:
            BoxLayout:
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height
                padding: dp(12)
                spacing: dp(12)

                # Banner de Diagnóstico cualitativo
                MDCard:
                    size_hint_y: None
                    height: dp(65)
                    padding: dp(12)
                    radius: [1]
                    md_bg_color: 0.9, 0.95, 1, 1

                    BoxLayout:
                        spacing: dp(10)
                        MDIcon:
                            icon: "information-outline"
                            theme_text_color: "Custom"
                            text_color: 0.1, 0.4, 0.8, 1
                            pos_hint: {"center_y": .5}
                        MDLabel:
                            id: lbl_diagnostico
                            text: "Cargando diagnóstico..."
                            font_style: "Caption"
                            bold: True
                            theme_text_color: "Custom"
                            text_color: 0.1, 0.4, 0.8, 1

                # Tarjeta Resumen: INGRESOS
                MDCard:
                    size_hint_y: None
                    height: dp(130)
                    padding: dp(12)
                    spacing: dp(6)
                    orientation: 'vertical'
                    radius: [1]
                    elevation: 2

                    BoxLayout:
                        size_hint_y: None
                        height: dp(24)
                        MDIcon:
                            icon: "arrow-up-bold-circle"
                            theme_text_color: "Custom"
                            text_color: 0, 0.6, 0.2, 1
                        MDLabel:
                            text: "INGRESOS DEL MES"
                            bold: True
                            font_style: "Subtitle2"
                            theme_text_color: "Custom"
                            text_color: 0, 0.6, 0.2, 1

                    BoxLayout:
                        orientation: 'horizontal'
                        MDLabel:
                            id: lbl_ingresos_esperados
                            text: "Esperado: $0"
                            font_style: "Caption"
                        MDLabel:
                            id: lbl_ingresos_ejecutados
                            text: "Real: $0"
                            bold: True
                            font_style: "Body2"

                    MDProgressBar:
                        id: bar_ingresos
                        value: 0
                        color: 0, 0.6, 0.2, 1

                # Tarjeta Resumen: GASTOS
                MDCard:
                    size_hint_y: None
                    height: dp(130)
                    padding: dp(12)
                    spacing: dp(6)
                    orientation: 'vertical'
                    radius: [1]
                    elevation: 2

                    BoxLayout:
                        size_hint_y: None
                        height: dp(24)
                        MDIcon:
                            icon: "arrow-down-bold-circle"
                            theme_text_color: "Custom"
                            text_color: 0.8, 0.2, 0.2, 1
                        MDLabel:
                            text: "GASTOS Y COMPROMISOS"
                            bold: True
                            font_style: "Subtitle2"
                            theme_text_color: "Custom"
                            text_color: 0.8, 0.2, 0.2, 1

                    BoxLayout:
                        orientation: 'horizontal'
                        MDLabel:
                            id: lbl_gastos_esperados
                            text: "Planificado: $0"
                            font_style: "Caption"
                        MDLabel:
                            id: lbl_gastos_ejecutados
                            text: "Real: $0"
                            bold: True
                            font_style: "Body2"

                    MDProgressBar:
                        id: bar_gastos
                        value: 0
                        color: 0.8, 0.2, 0.2, 1

                # Tarjeta Resumen: BALANCE DE AHORRO
                MDCard:
                    size_hint_y: None
                    height: dp(110)
                    padding: dp(12)
                    orientation: 'vertical'
                    radius: [1]
                    elevation: 3
                    md_bg_color: 0.92, 0.98, 0.92, 1

                    BoxLayout:
                        size_hint_y: None
                        height: dp(24)
                        MDIcon:
                            icon: "piggy-bank"
                            theme_text_color: "Custom"
                            text_color: 0, 0.5, 0, 1
                        MDLabel:
                            text: "AHORRO NETO CONSEGUIDO"
                            bold: True
                            font_style: "Subtitle2"

                    BoxLayout:
                        MDLabel:
                            id: lbl_balance_ejecutado
                            text: "Ahorro Real: $0"
                            bold: True
                            font_style: "H6"
                            theme_text_color: "Custom"
                            text_color: 0, 0.5, 0, 1

                # Navegación a Detalles
                BoxLayout:
                    size_hint_y: None
                    height: dp(48)
                    spacing: dp(10)
                    MDRaisedButton:
                        text: "Detalle Ingresos"
                        icon: "format-list-bulleted"
                        size_hint_x: 0.5
                        on_release: app.root.current = 'ingresos'
                    MDRaisedButton:
                        text: "Detalle Gastos"
                        icon: "cash-minus"
                        size_hint_x: 0.5
                        md_bg_color: 0.8, 0.2, 0.2, 1
                        on_release: app.root.current = 'gastos'


<IngresosScreen>:
    name: 'ingresos'
    BoxLayout:
        orientation: 'vertical'
        MDTopAppBar:
            title: "Detalle de Ingresos"
            left_action_items: [["arrow-left", lambda x: setattr(app.root, 'current', 'dashboard')]]
        ScrollView:
            MDList:
                id: lista_ingresos_container


<GastosScreen>:
    name: 'gastos'
    BoxLayout:
        orientation: 'vertical'
        MDTopAppBar:
            title: "Detalle de Gastos"
            left_action_items: [["arrow-left", lambda x: setattr(app.root, 'current', 'dashboard')]]
        ScrollView:
            MDList:
                id: lista_gastos_container