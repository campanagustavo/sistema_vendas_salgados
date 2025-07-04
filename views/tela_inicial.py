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
        from views.tela_login import TelaLogin  # Importa aqui para evitar importação circular
        self.page.clean()
        TelaLogin(self.page)  # Isso vai adicionar os componentes da tela de login

    def ir_para_cadastro(self, e):
        from views.tela_cadastro import TelaCadastro  # Importa aqui para evitar erro importação circular
        self.page.clean()
        TelaCadastro(self.page)

def exibir_tela_inicial(page: ft.Page):
    TelaInicial(page)  

if __name__ == "__main__":
    ft.app(target=exibir_tela_inicial)
