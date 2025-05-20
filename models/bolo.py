from models.alimento import Alimento

class Bolo(Alimento):
    def __init__(self, sabor: str, tamanho: str, preco: float, descricao: str = "", foto: str = "", id : int = None) -> None:
        super().__init__(preco, descricao, foto)
        self.sabor = sabor
        self.tamanho = tamanho
        self.id = id

    def get_categoria(self) -> str:
        # Implementação concreta do método abstrato
        return "Bolo"

    def dados_chave(self) -> tuple[str, tuple]:
        # Chave única para identificar bolo no banco (ex: sabor+tamanho+preço)
        return "sabor = ? AND tamanho = ? AND preco = ?", (self.sabor, self.tamanho, self.preco)

    def dados_para_salvar(self) -> list:
        # Dados que serão armazenados no banco
        return [self.sabor, self.tamanho, self.preco, self.descricao, self.foto]

    def tabela(self) -> str:
        # Nome da tabela correspondente no banco
        return "bolos"

    def campos_validos(self) -> bool:
        # Validação básica de campos obrigatórios
        return all([self.sabor, self.tamanho, self.preco])