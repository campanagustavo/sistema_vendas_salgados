from models.usuario import Usuario
from models.admin import Admin

class Cliente(Usuario):
    def __init__(self, nome: str, email: str, senha: str, id: int = None) -> None:
        super().__init__(nome, email, senha, id)
    
    @property
    def tipo(self) -> str:
        # Retorna o tipo do usuário como 'cliente'
        return "cliente"
    
    @property
    def tabela(self) -> str:
        # Retorna o nome da tabela para Clientes no banco
        return "clientes"
    
    @property
    def virar_admin(self) -> Admin:
        # Cria um objeto Admin a partir do Cliente atual
        return Admin(nome=self.nome, email=self.email, senha=self.senha)
