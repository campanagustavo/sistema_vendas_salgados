import flet as ft
from controllers.cadastro_controle import CadastroControle
from models.cliente import Cliente

class TelaCadastro:
    def __init__(self, page):
        self.page = page
        self.page.title = "Tela de Cadastro"
        self.controle = CadastroControle()  # Instância da classe de controle

        # Adicionando botão de voltar
        self.voltar_button = ft.ElevatedButton(
            "Voltar",  # Texto do botão
            on_click=self.voltar  # Função que será chamada ao clicar no botão
        )


        self.nome_field = ft.TextField(label="Nome", autofocus=True)
        self.email_field = ft.TextField(label="Email")
        self.senha_field = ft.TextField(label="Senha", password=True)

        self.page.add(
            ft.Row(
                [
                    ft.Column(
                        [
                            self.voltar_button,  # Botão de voltar
                            ft.Text("Crie seu cadastro", size=30, weight=ft.FontWeight.BOLD),
                            self.nome_field,
                            self.email_field,
                            self.senha_field,
                            ft.ElevatedButton("Cadastrar", on_click=self.cadastrar),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                expand=True
            )
        )

    def cadastrar(self, e):
        # Criando o objeto Cliente com os dados dos campos
        novorapaz = Cliente(
            nome=self.nome_field.value,
            email=self.email_field.value,
            senha=self.senha_field.value
        )

        # Chamando o método de cadastro
        erro = self.controle.cadastrar_cliente(novorapaz)

        if erro is None:
            # Cadastro bem-sucedido: Limpar a tela e ir para a tela inicial
            self.page.clean()
            from views.tela_inicial import TelaInicial
            TelaInicial(self.page)
        else:
            # Se houver erro, mostrar o erro na interface gráfica (snack_bar)
            self.page.snack_bar = ft.SnackBar(ft.Text(erro))  # Exibir a mensagem de erro
            self.page.snack_bar.open = True
            self.page.update()

    def voltar(self, e):
        # Limpar a página atual e carregar a tela de login novamente
        self.page.clean()
        from views.tela_inicial import TelaInicial
        TelaInicial(self.page)