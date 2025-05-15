import flet as ft
from models.cliente import Cliente
from controllers.cadastro_controle import CadastroControle

class TelaCadastro:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Tela de Cadastro"
        self.controle = CadastroControle()

        self.nome_field = ft.TextField(label="Nome")
        self.email_field = ft.TextField(label="Email")
        self.senha_field = ft.TextField(label="Senha", password=True)
        self.msg_text = ft.Text("", color=ft.Colors.RED)
        
        self.btn_cadastrar = ft.ElevatedButton("Cadastrar", on_click=self.cadastrar)
        self.btn_voltar = ft.ElevatedButton("Voltar", on_click=self.voltar)

        self.page.add(
            ft.Row(
                [
                    ft.Column(
                        [
                            ft.Text("Cadastro de Novo Cliente", size=24, weight=ft.FontWeight.BOLD),
                            self.nome_field,
                            self.email_field,
                            self.senha_field,
                            self.msg_text,
                            self.btn_cadastrar,
                            self.btn_voltar,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                expand=True,
            )
        )

    def cadastrar(self, e):
        cliente = Cliente(
            self.nome_field.value.strip(),
            self.email_field.value.strip(),
            self.senha_field.value.strip()
        )
        erro = self.controle.cadastrar_cliente(cliente)

        if erro:
            self.msg_text.value = erro
            self.msg_text.color = ft.Colors.RED
        else:
            self.msg_text.value = "Cadastro realizado com sucesso!"
            self.msg_text.color = ft.Colors.GREEN
            self.nome_field.value = ""
            self.email_field.value = ""
            self.senha_field.value = ""

        self.page.update()

    def voltar(self, e):
        from views.tela_inicial import TelaInicial
        self.page.clean()
        TelaInicial(self.page)
