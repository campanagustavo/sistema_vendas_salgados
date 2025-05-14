import flet as ft

class TelaLogin:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Tela de Login"
        
                # Adicionando botão de voltar
        self.voltar_button = ft.ElevatedButton(
            "Voltar",  # Texto do botão
            on_click=self.voltar  # Função que será chamada ao clicar no botão
        )


        # Usando ft.Row para centralizar a tela de login
        self.page.add(
            ft.Row(
                [
                    ft.Column(
                        [
                            self.voltar_button,  # Botão de voltar
                            ft.Text("Email:"),
                            ft.TextField(label="Digite seu e-mail", width=300),  # Campo de email com largura ajustada
                            ft.Text("Senha:"),
                            ft.TextField(label="Digite sua senha", password=True, width=300),  # Campo de senha com largura ajustada
                            ft.ElevatedButton("Entrar", on_click=self.entrar),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,  # Alinhamento vertical dos itens dentro da coluna
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,  # Centraliza a Row na tela
                expand=True  # Expande para preencher o espaço disponível
            )
        )

    def entrar(self, e):
        # Lógica do login vai aqui
        self.page.clean()
        self.page.add(ft.Text("Login bem-sucedido!"))

    def voltar(self, e):
        # Limpar a página atual e carregar a tela de login novamente
        self.page.clean()
        from views.tela_inicial import TelaInicial
        TelaInicial(self.page)