import flet as ft
from models.cliente import Cliente
from models.admin import Admin
from controllers.login_controle import LoginControle
from views.painel_cliente import PainelCliente
from views.painel_admin import PainelAdmin

class TelaLogin:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Login"
        self.page.clean()
        
        self.login_controle = LoginControle()
        
        self.email = ft.TextField(label="Email", width=300)
        self.senha = ft.TextField(label="Senha", password=True, width=300)
        self.msg_text = ft.Text("", color=ft.Colors.RED)
        
        # Layout centralizado similar ao da tela inicial
        self.page.add(
            ft.Row(
                [
                    ft.Column(
                        [
                            ft.Text("Login", size=24, weight=ft.FontWeight.BOLD),
                            self.email,
                            self.senha,
                            self.msg_text,
                            ft.Row(
                                [
                                    ft.ElevatedButton("Entrar", on_click=self.entrar),
                                    ft.ElevatedButton("Voltar", on_click=self.voltar),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                spacing=20
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=20
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                expand=True
            )
        )

    def entrar(self, e):
        email = self.email.value
        senha = self.senha.value

        # Autentica (agora recebe email e senha diretamente)
        usuario, erro = self.login_controle.autenticar(email, senha)

        if erro:
            self.msg_text.value = erro
            self.msg_text.color = ft.Colors.RED
            self.page.update()
            return

        print(f"Bem-vindo {usuario.nome} ({usuario.tipo})")

        # Autenticação bem-sucedida
        if usuario.tipo == "admin":
            self.page.clean()
            PainelAdmin(self.page)
        else:
            self.page.clean()
            PainelCliente(self.page, usuario)

    def voltar(self, e):
        from views.tela_inicial import TelaInicial
        self.page.clean()
        TelaInicial(self.page)