from controllers.login_controle import LoginControle
from models.cliente import Cliente
from models.admin import Admin
import flet as ft

class TelaLogin:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Tela de Login"
        self.controle = LoginControle()

        self.email_field = ft.TextField(label="Digite seu e-mail", width=300)
        self.senha_field = ft.TextField(label="Digite sua senha", password=True, width=300)
        self.msg_text = ft.Text("", color=ft.Colors.RED)

        self.page.add(
            ft.Row(
                [
                    ft.Column(
                        [
                            ft.ElevatedButton("Voltar", on_click=self.voltar),
                            self.email_field,
                            self.senha_field,
                            self.msg_text,
                            ft.ElevatedButton("Entrar", on_click=self.entrar),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                expand=True
            )
        )

    def entrar(self, e):
        cliente = Cliente("", self.email_field.value.strip(), self.senha_field.value.strip())
        resultado = self.controle.autenticar(cliente)

        if isinstance(resultado, Cliente):
            from views.painel_cliente import PainelCliente
            self.page.clean()
            PainelCliente(self.page)
        elif isinstance(resultado, Admin):
            from views.painel_admin import PainelAdmin
            self.page.clean()
            PainelAdmin(self.page)
        else:
            self.msg_text.value = resultado
            self.msg_text.color = ft.Colors.RED
            self.page.update()

    def voltar(self, e):
        from views.tela_inicial import TelaInicial
        self.page.clean()
        TelaInicial(self.page)
