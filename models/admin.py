from models.usuario import Usuario

class Admin(Usuario):
    def __init__(self, nome: str, email: str, senha: str, id: int = None, senha_ja_hasheada = False) -> None:
        super().__init__(nome, email, senha, id,senha_ja_hasheada = senha_ja_hasheada)
    
    @property
    def tipo(self) -> str:
        return "admin"

    @property
    def tabela(self) -> str:
        # Retorna o nome da tabela para Admins no banco
        return "admins"