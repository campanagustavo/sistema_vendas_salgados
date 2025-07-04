import flet as ft
from views.tela_inicial import TelaInicial
from data.database import BaseDeDados

class SistemaApp:
    def __init__(self, page: ft.Page):
        # Inicializa a aplicação com a página do Flet
        self.page = page
        self.page.title = "Sistema de Vendas de Salgados"
        self.iniciar()

    def iniciar(self):
        # Exibe a tela inicial da aplicação
        TelaInicial(self.page)

def main(page: ft.Page):
    # unção principal que cria a instância da aplicação
    SistemaApp(page)

if __name__ == "__main__":
    # Inicia o app do Flet, passando a função main como alvo
    ft.app(target=main)
