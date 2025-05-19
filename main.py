# Em um arquivo como views/main_app.py ou sistema_web.py
import flet as ft
from views.tela_cadastro import TelaCadastro # Ajuste o caminho se necessário
# Seus outros imports (models, controllers) podem não ser necessários aqui
# diretamente, se TelaCadastro já os importa e usa.

def main(page: ft.Page):
    page.title = "Sistema de Cadastro MVP"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER # Centraliza globalmente
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # A sua classe TelaCadastro já faz page.add() no __init__ dela.
    # Então, apenas instanciá-la deve ser suficiente para exibir.
    tela_cadastro_instance = TelaCadastro(page)

    # Se você tiver outras telas e um sistema de navegação,
    # a lógica aqui seria mais complexa (ex: page.on_route_change).
    # Mas para mostrar SÓ a tela de cadastro, isso acima basta.

    page.update() # Garante que a página inicial seja renderizada

if __name__ == "__main__":
    ft.app(target=main)