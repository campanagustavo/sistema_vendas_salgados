# Classe Bolo - herda de Alimento

from models.alimento import Alimento

class Bolo(Alimento):
    def __init__(self, id, sabor: str, tamanho: str, preco: float, descricao: str, foto: str = "") -> None:
        super().__init__(preco, descricao, foto)
        self.sabor = sabor
        self.tamanho = tamanho
        self.id = id 

    def get_categoria(self) -> str:
        return "Bolo"

    def exibir_info(self) -> str:
        return f"Sabor: {self.sabor}, Tamanho: {self.tamanho}, Descrição: {self.descricao}, Preço: R${self.preco}, Foto: {self.foto}"