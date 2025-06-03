from models.alimento import Alimento

class Salgado(Alimento):
    def __init__(self, tipo: str, recheio: str, preco: float, descricao: str = "", foto: str = "", id: int = None) -> None:
        super().__init__(preco, descricao, foto)
        self.tipo = tipo
        self.recheio = recheio
        self.id = id

    @property
    def categoria(self) -> str:
        # Implementação concreta do método abstrato
        return "Salgado"

    @property
    def dados_chave(self) -> tuple[str, tuple]:
        # Chave única para identificar salgado no banco (tipo+recheio+preço)
        return "tipo = ? AND recheio = ? AND preco = ?", (self.tipo, self.recheio, self.preco)

    @property
    def dados_para_salvar(self) -> list:
        # Dados que serão armazenados no banco
        return [self.tipo, self.recheio, self.preco, self.descricao, self.foto]

    @property
    def tabela(self) -> str:
        # Nome da tabela correspondente no banco
        return "salgados"

    @property
    def campos_validos(self) -> bool:
        # Validação básica de campos obrigatórios
        return all([self.tipo, self.recheio, self.preco])
