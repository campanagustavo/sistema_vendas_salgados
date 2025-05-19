# Classe Pedido - representa um pedido feito por um cliente

from typing import List, Tuple
from models.usuario import Usuario
from models.alimento import Alimento

class Pedido:
    def __init__(self, cliente: Usuario, itens: List[Tuple[Alimento, int]]) -> None:
        """
        :param cliente: instância do Cliente que fez o pedido
        :param itens: lista de tuplas (alimento, quantidade)
        """
        self.cliente: Usuario = cliente
        self.itens: List[Tuple[Alimento, int]] = itens
        self.status: str = "Confirmado"  # Status inicial do pedido
        self.pagamento: str = ""         # Ex: 'pix', 'cartao', 'dinheiro'

    def calcular_total(self) -> float:
        """
        Calcula o valor total do pedido com base nos itens.
        :return: preço total
        """
        total = 0.0
        for alimento, quantidade in self.itens:
            total += alimento.preco * quantidade
        return total

    def atualizar_status(self, novo_status: str) -> None:
        """
        Atualiza o status do pedido.
        :param novo_status: novo valor para o status
        """
        self.status = novo_status

    def definir_pagamento(self, metodo: str) -> None:
        """
        Define a forma de pagamento.
        :param metodo: 'pix', 'cartao' ou 'dinheiro'
        """
        self.pagamento = metodo
