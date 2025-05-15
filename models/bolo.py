# Classe Bolo - herda de Alimento

from models.alimento import Alimento

class Bolo(Alimento):
    def __init__(self, sabor: str, tamanho: str, preco: float, descricao: str, foto: str = "") -> None:
        super().__init__(preco, descricao, foto)  # Chamando o construtor da classe base
        self.sabor = sabor
        self.tamanho = tamanho

    def get_categoria(self) -> str:
        """
        Retorna a categoria do alimento.
        :return: Categoria (Bolo)
        """
        return "Bolo"

    def exibir_info(self) -> str:
        """
        Exibe as informações completas do bolo.
        :return: Informações formatadas do bolo
        """
        return f"Sabor: {self.sabor}, Tamanho: {self.tamanho}, Descrição: {self.descricao}, Preço: R${self.preco}, Foto: {self.foto}"