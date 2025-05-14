# Classe Cliente - herda de Usuario

from models.usuario import Usuario

class Cliente(Usuario):
    def __init__(self, nome: str, email: str, senha: str) -> None:
        super().__init__(nome, email, senha)

    def get_tipo(self) -> str:
        return "cliente"