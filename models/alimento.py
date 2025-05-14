# Classe base Alimento

from abc import ABC, abstractmethod

from abc import ABC, abstractmethod

class Alimento(ABC):
    def __init__(self, nome: str, preco: float, descricao: str, foto: str = "") -> None:
        self.nome = nome
        self.preco = preco
        self.descricao = descricao
        self.foto = foto

    @abstractmethod
    def get_categoria(self) -> str:
        pass

    @abstractmethod
    def exibir_info(self) -> str:
        pass