# Classe abstrata base para alimentos (bolos, salgados, etc)
from abc import ABC, abstractmethod

class Alimento(ABC):
    def __init__(self, preco: float, descricao: str, foto: str = "", id : int = None) -> None:
        self.id = id
        self.preco = preco
        self.descricao = descricao
        self.foto = foto

    @property
    @abstractmethod
    def categoria(self) -> str:
        # Método abstrato: cada subclasse deve informar sua categoria (ex: 'Bolo')
        pass
    
    @property
    @abstractmethod
    def dados_chave(self) -> tuple[str, tuple]:
        # Método abstrato: cada subclasse deve informar como buscar o alimento no banco
        pass

    @property
    @abstractmethod
    def dados_para_salvar(self) -> list:
        # Método abstrato: cada subclasse deve informar os dados a serem salvos no banco
        pass

    @property
    @abstractmethod
    def tabela(self) -> str:
        # Método abstrato: cada subclasse deve informar o nome da tabela no banco
        pass

    @property
    @abstractmethod
    def campos_validos(self) -> bool:
        # Método abstrato: cada subclasse deve validar seus campos
        pass