import flet as ft

class PainelCliente:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Painel do Cliente"
        self.page.clean()

        self.tela_principal()

    def tela_principal(self) -> None:
        # Barra superior com logout no canto direito
        barra_superior = ft.Row(
            controls=[
                ft.Container(expand=True),  # empurra o botão para a direita
                ft.IconButton(
                    icon=ft.Icons.EXIT_TO_APP,
                    on_click=self.logout,
                    tooltip="Logout",
                )
            ],
            alignment=ft.MainAxisAlignment.END
        )

        # Botões centrais (Visualizar Cardápio e Acompanhar Pedidos)
        botoes = ft.Column(
            [
                ft.ElevatedButton("Visualizar Cardápio", on_click=self.visualizar_cardapio, width=200),
                ft.ElevatedButton("Acompanhar Pedidos", on_click=self.acompanhar_pedidos, width=200),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
            expand=True,
        )

        # Adiciona os componentes na página
        self.page.add(
            ft.Column(
                [
                    barra_superior,
                    ft.Container(
                        content=botoes,
                        expand=True,
                        alignment=ft.alignment.center,
                    )
                ],
                expand=True,
            )
        )

    def visualizar_cardapio(self, e: ft.ControlEvent) -> None:
        print("Visualizar Cardápio clicado")

    def acompanhar_pedidos(self, e: ft.ControlEvent) -> None:
        print("Acompanhar Pedidos clicado")

    def logout(self, e) -> None:
        from views.tela_inicial import TelaInicial
        self.page.clean()
        TelaInicial(self.page)
