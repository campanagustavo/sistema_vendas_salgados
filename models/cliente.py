from models.usuario import Usuario
from models.admin import Admin

class Cliente(Usuario):
    def __init__(self, nome: str, email: str, senha: str, id: int = None, senha_ja_hasheada: bool = False) -> None:
        super().__init__(nome, email, senha, id=id, senha_ja_hasheada=senha_ja_hasheada)
    
    @property
    def tipo(self) -> str:
        return "cliente"
    
    @property
    def tabela(self) -> str:
        # Retorna o nome da tabela para Clientes no banco
        return "clientes"
    
    @property
    def virar_admin(self) -> Admin:
        # Cria um objeto Admin a partir do Cliente atual
        return Admin(nome=self.nome, email=self.email, senha=self.senha_hash, senha_ja_hasheada=True)

