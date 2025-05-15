# Classe Salgado - herda de Alimento

from models.alimento import Alimento

class Salgado(Alimento):
    def __init__(self, id, tipo: str, recheio: str, preco: float, descricao: str, foto: str = "") -> None:
        super().__init__(preco, descricao, foto)
        self.tipo = tipo
        self.recheio = recheio
        self.id = id  # ID opcional, fornecido após salvar ou carregar do banco

    def get_categoria(self) -> str:
        return "Salgado"

    def exibir_info(self) -> str:
        return f"Tipo: {self.tipo}, Recheio: {self.recheio}, Descrição: {self.descricao}, Preço: R${self.preco}, Foto: {self.foto}"