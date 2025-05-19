# Classe abstrata Usuario
# Será herdada por Cliente e Admin

from abc import ABC, abstractmethod

class Usuario(ABC):
    def __init__(self, nome: str, email: str, senha: str, usuario_id: int = None) -> None:
        self.usuario_id = usuario_id
        self.nome = nome
        self.email = email
        self.senha = senha
        
    @abstractmethod
    def get_tipo(self) -> str:
        pass
    

    
    
    
    