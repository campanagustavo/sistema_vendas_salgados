import flet as ft
from views.tela_inicial import TelaInicial
from data.database import BaseDeDados

class SistemaApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Sistema de Vendas de Salgados"
        self.iniciar()

    def iniciar(self):
        TelaInicial(self.page)

def main(page: ft.Page):
    SistemaApp(page)

if __name__ == "__main__":
    ft.app(target=main)