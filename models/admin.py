# Classe Admin - herda de Usuario

from models.usuario import Usuario

class Admin(Usuario):
    def __init__(self, nome: str, email: str, senha: str, id: int = None) -> None:
        super().__init__(nome, email, senha)
        self.id = id

    def get_tipo(self) -> str:
        return "admin"