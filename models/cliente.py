# Classe Cliente - herda de Usuario

from models.usuario import Usuario

class Cliente(Usuario):
    def __init__(self, nome: str, email: str, senha: str, id: int = None) -> None:
        super().__init__(nome, email, senha)
        self.id = id

    def get_tipo(self) -> str:
        return "cliente"