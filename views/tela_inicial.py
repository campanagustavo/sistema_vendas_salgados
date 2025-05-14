import flet as ft
from views.tela_login import TelaLogin
from views.tela_cadastro import TelaCadastro

class TelaInicial:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Sistema de Vendas de Salgados"
        
        # Usando uma Row e Column para garantir centralização no eixo vertical e horizontal
        self.page.add(
            ft.Row(
                [
                    ft.Column(
                        [
                            ft.Text("Salgados e Bolos da Ana", size=30, weight=ft.FontWeight.BOLD),
                            ft.ElevatedButton("Fazer Login", on_click=self.ir_para_login),
                            ft.ElevatedButton("Criar Novo Cadastro", on_click=self.ir_para_cadastro),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,  # Alinhamento vertical
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Alinhamento horizontal
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,  # Alinhamento centralizado na Row (horizontal)
                expand=True,  # Expande para preencher o espaço disponível
            )
        )

    def ir_para_login(self, e):
        # Limpa a tela e carrega a tela de login
        self.page.clean()
        TelaLogin(self.page)  # Isso vai adicionar os componentes da tela de login

    def ir_para_cadastro(self, e):
        # Limpa a tela e carrega a tela de cadastro
        self.page.clean()
        TelaCadastro(self.page)  # Isso vai adicionar os componentes da tela de cadastro

# Aqui estamos iniciando a tela inicial corretamente!
def exibir_tela_inicial(page: ft.Page):
    TelaInicial(page)  # Carrega a TelaInicial primeiro

if __name__ == "__main__":
    def exibir_tela_inicial(page: ft.Page):
        TelaInicial(page)  # Carrega a TelaInicial primeiro

    ft.app(target=exibir_tela_inicial)  # Aqui iniciamos a tela inicial