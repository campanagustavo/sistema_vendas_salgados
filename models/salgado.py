# Classe Salgado - herda de Alimento

from models.alimento import Alimento

class Salgado(Alimento):
    def __init__(self, tipo: str, recheio: str, preco: float, descricao: str, foto: str = "") -> None:
        super().__init__(preco, descricao, foto)  # Chamando o construtor da classe base
        self.tipo = tipo
        self.recheio = recheio

    def get_categoria(self) -> str:
        """
        Retorna a categoria do alimento.
        :return: Categoria (Salgado)
        """
        return "Salgado"

    def exibir_info(self) -> str:
        """
        Exibe as informações completas do salgado.
        :return: Informações formatadas do salgado
        """
        return f"Tipo: {self.tipo}, Recheio: {self.recheio}, Descrição: {self.descricao}, Preço: R${self.preco}, Foto: {self.foto}"