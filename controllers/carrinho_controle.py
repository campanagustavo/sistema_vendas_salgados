# carrinho_controle.py

from typing import Union, Dict
from models.bolo import Bolo
from models.salgado import Salgado
from data.database import BaseDeDados

class CarrinhoControle:
    def __init__(self, cliente_id=None):
        self.db = BaseDeDados()
        self.cliente_id = cliente_id

    def adicionar_item(self, produto: Union[Bolo, Salgado], quantidade: int = 1):
        """Adiciona um item ao carrinho ou incrementa a quantidade se já existir"""
        try:
            if not self.cliente_id:
                raise ValueError("ID do cliente não está definido")
            
            if not hasattr(produto, 'id') or not produto.id:
                raise ValueError("Produto não possui ID válido")
            
            tipo = 'bolo' if isinstance(produto, Bolo) else 'salgado'
            
            # Verifica se o item já está no carrinho
            resultado = self.db.buscar_dado(
                "carrinho",
                "cliente_id = ? AND item_id = ? AND tipo = ?",
                (self.cliente_id, produto.id, tipo)
            )
            
            if resultado:
                # Se já existe, atualiza a quantidade
                nova_quantidade = resultado[0][3] + quantidade  # índice 3 é quantidade
                self.db.atualizar_dado(
                    "carrinho",
                    "quantidade",
                    nova_quantidade,
                    f"cliente_id = {self.cliente_id} AND item_id = {produto.id} AND tipo = '{tipo}'"
                )
            else:
                # Se não existe, insere novo item
                dados = (self.cliente_id, produto.id, tipo, quantidade)
                self.db.salvar_dado("carrinho", dados)
            
            return True
        except Exception as e:
            print(f"Erro ao adicionar item ao carrinho: {str(e)}")
            raise

    def listar_itens(self) -> Dict[int, int]:
        try:
            resultado = self.db.buscar_dado("carrinho", "cliente_id = ?", (self.cliente_id,))
            itens = {item[1]: item[3] for item in resultado}
            return itens
        except Exception as e:
            print(f"Erro ao listar itens do carrinho: {str(e)}")
            return {}