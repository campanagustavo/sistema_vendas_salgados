class Pedido:
    STATUS_VALIDOS = ["Confirmado", "Em preparo", "Entregue", "Finalizado", "Cancelado", "Concluído"]
    
    def __init__(self, id: int, cliente_id: int, itens: list[dict], metodo_pagamento: str, status: str = "Confirmado") -> None:
        self.id = id
        self.cliente_id = cliente_id
        self.itens = itens
        self.metodo_pagamento = metodo_pagamento
        self.status = status  

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, novo_status: str) -> None:
        if novo_status not in self.STATUS_VALIDOS:
            raise ValueError(f"Status inválido: {novo_status}. Status válidos: {self.STATUS_VALIDOS}")
        self._status = novo_status

    def pode_cancelar(self) -> bool:
        return self._status in ["Confirmado", "Em preparo"]
    
    @property
    def total(self) -> float:
        return sum(item['preco'] * item['quantidade'] for item in self.itens)
