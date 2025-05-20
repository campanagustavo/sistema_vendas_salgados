class Pedido:
    STATUS_VALIDOS = ["Confirmado", "Em preparo", "Entregue", "Finalizado", "Cancelado", "Concluído"]
    
    def __init__(self, id: int, cliente_id: int, itens: list[dict], metodo_pagamento: str, status: str = "Confirmado") -> None:
        self.id = id
        self.cliente_id = cliente_id
        self.itens = itens
        self.metodo_pagamento = metodo_pagamento
        self.status = status if status in self.STATUS_VALIDOS else "Confirmado"
        self.total = self.calcular_total()

    def atualizar_status(self, novo_status: str) -> bool:
        # Atualiza o status do pedido, retornando True se válido, False caso contrário
        if novo_status not in self.STATUS_VALIDOS:
            return False
        self.status = novo_status
        return True
    
    def pode_cancelar(self) -> bool:
        # Retorna True se o pedido estiver em um status que permite cancelamento
        return self.status in ["Confirmado", "Em preparo"]
    
    def calcular_total(self) -> float:
        # Calcula o total do pedido com base nos itens
        total = 0.0
        for item in self.itens:
            total += item['preco'] * item['quantidade']
        return total