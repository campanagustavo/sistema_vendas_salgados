from models.alimento import Alimento

class Bolo(Alimento):
    def __init__(self, sabor: str, tamanho: str, preco: float, descricao: str = "", foto: str = "", id : int = None) -> None:
        super().__init__(preco, descricao, foto)
        self.sabor = sabor
        self.tamanho = tamanho
        self.id = id

    @property
    def categoria(self) -> str:
        # Implementação concreta do método abstrato
        return "Bolo"

    @property
    def dados_chave(self) -> tuple[str, tuple]:
        # Chave única para identificar bolo no banco (ex: sabor+tamanho+preço)
        return "sabor = ? AND tamanho = ? AND preco = ?", (self.sabor, self.tamanho, self.preco)

    @property
    def dados_para_salvar(self) -> list:
        # Dados que serão armazenados no banco
        return [self.sabor, self.tamanho, self.preco, self.descricao, self.foto]

    @property
    def tabela(self) -> str:
        # Nome da tabela correspondente no banco
        return "bolos"

    @property
    def campos_validos(self) -> bool:
        # Validação básica de campos obrigatórios
        return all([self.sabor, self.tamanho, self.preco])