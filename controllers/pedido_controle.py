from models.pedido import Pedido
from data.database import BaseDeDados
from models.salgado import Salgado
from models.bolo import Bolo
from controllers.alimento_controle import AlimentoControle
from controllers.cadastro_controle import CadastroControle

class PedidoControle:
    def __init__(self) -> None:
        # Inicializa conexões e controles necessários
        self.db = BaseDeDados()
        self.alimento_controle = AlimentoControle()
        self.cadastro_controle = CadastroControle()
        
    def criar_pedido(self, cliente_id: int, itens: list[dict], metodo_pagamento: str) -> Pedido:
        # Salva o pedido no banco e seus itens
        dados_pedido = [cliente_id, metodo_pagamento, "Confirmado"]
        self.db.salvar_dado("pedidos", dados_pedido)
        pedido_id = self.db.cursor.lastrowid  # id gerado pelo banco
        
        # Para cada item, salva no banco indicando se é bolo ou salgado
        for item in itens:
            produto = item['produto']
            tipo_produto = 'bolo' if hasattr(produto, 'sabor') else 'salgado'
            self.db.salvar_dado("itens_pedido", [
                pedido_id,
                produto.id,
                tipo_produto,
                item['quantidade']
            ])
        
        # Retorna objeto Pedido criado
        return Pedido(pedido_id, cliente_id, itens, metodo_pagamento)
    
    def buscar_pedido(self, pedido_id: int) -> Pedido | None:
        # Busca um pedido pelo id, junto com seus itens
        try:
            resultado_db = self.db.buscar_dado("pedidos", "id = ?", [pedido_id])
            if not resultado_db:
                return None
            
            pedido_data = resultado_db[0]
            
            # Busca os itens desse pedido
            itens_data = self.db.buscar_dado("itens_pedido", "pedido_id = ?", [pedido_id])
            itens = []
            for item in itens_data:
                produto_id = item[2]
                tipo = item[3]
                quantidade = item[4]
                # Obtém objeto do alimento correto conforme tipo
                produto = (self.alimento_controle.obter_alimento_por_id(Bolo, "bolos", produto_id) 
                        if tipo == 'bolo' else self.alimento_controle.obter_alimento_por_id(Salgado, "salgados", produto_id))
                if produto:
                    itens.append({'produto': produto, 'quantidade': quantidade, 'preco': produto.preco})
            
            # Retorna objeto Pedido preenchido
            return Pedido(
                id=pedido_data[0],
                cliente_id=pedido_data[1],
                itens=itens,
                metodo_pagamento=pedido_data[2],
                status=pedido_data[3]
            )
        except Exception as e:
            print(f"Erro ao buscar pedido com itens: {e}")
            return None

    def listar_pedidos_por_cliente(self, cliente_id: int) -> list[Pedido]:
        # Retorna todos os pedidos feitos por um cliente específico
        resultados = self.db.buscar_dado("pedidos", "cliente_id = ?", [cliente_id])
        pedidos = []
        
        for pedido_data in resultados:
            pedido_id = pedido_data[0]
            pedido = self.buscar_pedido(pedido_id)
            if pedido:
                pedidos.append(pedido)
                
        return pedidos
    
    def atualizar_status_pedido(self, pedido_id: int, novo_status: str) -> bool:
        # Atualiza o status de um pedido, retorna True se sucesso
        pedido = self.buscar_pedido(pedido_id)
        if not pedido:
            return False
        
        if not pedido.atualizar_status(novo_status):
            return False

        # Atualiza no banco de dados
        try:
            self.db.atualizar_dado(
                tabela="pedidos",
                campo="status",
                valor=pedido.status,
                condicao=f"id = {pedido_id}"
            )
            return True  # Assume sucesso
        except Exception as e:
            print(f"Erro ao atualizar status: {e}")
            return False
        
    def listar_todos_pedidos(self) -> list[Pedido]:
        # Retorna todos os pedidos cadastrados no sistema
        try:
            pedidos_data = self.db.buscar_dado("pedidos", "1=1")  # busca todos
            
            pedidos = []
            
            for pedido_data in pedidos_data:
                pedido_id = pedido_data[0]
                try:
                    pedido = self.buscar_pedido(pedido_id)
                    if pedido:
                        pedidos.append(pedido)
                except Exception as e:
                    print(f"Erro ao carregar pedido {pedido_id}: {str(e)}")
                    continue
            
            return pedidos
        
        except Exception as e:
            print(f"Erro ao listar pedidos: {e}")
            return []
