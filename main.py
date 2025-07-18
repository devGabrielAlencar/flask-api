import flet as ft
from clientes import view_clientes  # importa a view da aba CLIENTES


def main(page: ft.Page):
    page.title = 'CRM'
    page.theme_mode = 'Dark'
    page.window.width = 800
    page.scroll = ft.ScrollMode.AUTO

    # ==== ROTA: HOME ====
    def view_home(page: ft.Page):
        cabecalho = ft.Row(
            controls=[
                ft.Text('🍊DaFruta-CE', size=50, font_family='Arial',
                        color=ft.Colors.ORANGE),
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )

        # Submenu (visível ou não)
        submenu = ft.Container(
            content=ft.Row(
                controls=[
                    ft.TextButton("| CLIENTES |",
                                  on_click=lambda e: page.go("/clientes")),
                    ft.TextButton("| ESTOQUE |"),
                    ft.TextButton("| PEDIDOS |"),
                    ft.TextButton("| FINANCEIRO |")
                ]
            ),
            visible=False
        )

        def menu(e):
            submenu.visible = not submenu.visible
            page.update()

        btn_menu = ft.ElevatedButton(
            "|||",
            on_click=menu,
            width=100,
            height=50,
            style=ft.ButtonStyle(
                padding=20,
                text_style=ft.TextStyle(size=20)
            )
        )

        menu_area = ft.Column(
            controls=[btn_menu, submenu],
            alignment=ft.MainAxisAlignment.START
        )

        total_pedidos = 152
        total_clientes = 87
        total_estoque = 320
        total_rank_clientes = [
            {"nome": "Àgape", "pedidos": 16},
            {"nome": "Hotel", "pedidos": 20},
            {"nome": "Vila Verde", "pedidos": 10},
            {"nome": "Casa das Frutas", "pedidos": 25},
            {"nome": "Sabor Natural", "pedidos": 18}
        ]

        def criar_card(titulo, valor, cor):
            return ft.Container(
                content=ft.Column(
                    [
                        ft.Text(titulo, size=20, weight="bold",
                                color=ft.Colors.WHITE),
                        ft.Text(str(valor), size=30, weight="bold", color=cor),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                width=250,
                height=120,
                bgcolor=ft.Colors.with_opacity(0.1, cor),
                border_radius=15,
                padding=10
            )

        dashboard = ft.Container(
            ft.Row(
                controls=[
                    criar_card("Pedidos", total_pedidos, ft.Colors.GREEN),
                    criar_card("Clientes", total_clientes, ft.Colors.BLUE),
                    criar_card("Estoque", total_estoque, ft.Colors.ORANGE),
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            alignment=ft.alignment.top_center,
            padding=ft.padding.only(top=100)
        )

        def criar_card_clientes(cliente):
            return ft.Container(
                content=ft.Column(
                    [
                        ft.Text(cliente["nome"], size=18,
                                weight="bold", color=ft.Colors.ORANGE),
                        ft.Text(
                            f'{cliente["pedidos"]} pedidos no mês', size=14)
                    ],
                    spacing=10,
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.START
                ),
                padding=10,
                margin=5,
                bgcolor=ft.Colors.with_opacity(0.08, ft.Colors.BLUE_GREY),
                border_radius=12,
                width=200
            )

        rank = ft.Container(
            ft.Column(
                controls=[criar_card_clientes(cliente)
                          for cliente in total_rank_clientes]
            )
        )

        return ft.View(
            route="/",
            controls=[cabecalho, ft.Divider(), menu_area, dashboard, rank]
        )

    # ==== ROTEAMENTO ====
    def on_route_change(e):
        page.views.clear()

        if page.route == "/clientes":
            page.views.append(view_clientes(page))
        else:
            page.views.append(view_home(page))

        page.update()

    page.on_route_change = on_route_change
    page.go(page.route)  # inicia a rota atual


ft.app(target=main, view=ft.WEB_BROWSER)
