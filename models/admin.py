from models.usuario import Usuario

class Admin(Usuario):
    def __init__(self, nome: str, email: str, senha: str, id: int = None) -> None:
        super().__init__(nome, email, senha, id)
    
    def get_tipo(self) -> str:
        # Retorna o tipo do usuário como 'admin'
        return "admin"

    def tabela(self) -> str:
        # Retorna o nome da tabela para Admins no banco
        return "admins"