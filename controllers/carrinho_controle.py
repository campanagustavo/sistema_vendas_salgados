from typing import Union, Dict
from models.bolo import Bolo
from models.salgado import Salgado
from data.database import BaseDeDados

class CarrinhoControle:
    def __init__(self, cliente_id: int = None) -> None:
        # Inicializa conexão com banco e armazena cliente atual
        self.db = BaseDeDados()
        self.cliente_id = cliente_id

    def adicionar_item(self, produto: Union[Bolo, Salgado], quantidade: int = 1) -> bool:
        # Adiciona item ao carrinho ou incrementa quantidade se já existir
        try:
            if not self.cliente_id:
                raise ValueError("ID do cliente não está definido")
            
            if not hasattr(produto, 'id') or not produto.id:
                raise ValueError("Produto não possui ID válido")
            
            tipo = 'bolo' if isinstance(produto, Bolo) else 'salgado'
            
            # Verifica se o item já existe no carrinho
            resultado = self.db.buscar_dado(
                "carrinho",
                "cliente_id = ? AND item_id = ? AND tipo = ?",
                (self.cliente_id, produto.id, tipo)
            )
            
            if resultado:
                # Atualiza quantidade existente
                nova_quantidade = resultado[0][3] + quantidade  # índice 3 = quantidade
                self.db.atualizar_dado(
                    "carrinho",
                    "quantidade",
                    nova_quantidade,
                    f"cliente_id = {self.cliente_id} AND item_id = {produto.id} AND tipo = '{tipo}'"
                )
            else:
                # Insere novo item no carrinho
                dados = (self.cliente_id, produto.id, tipo, quantidade)
                self.db.salvar_dado("carrinho", dados)
            
            return True
        except Exception as e:
            print(f"Erro ao adicionar item ao carrinho: {str(e)}")
            raise

    def listar_itens(self) -> list[Dict]:
        # Retorna todos os itens do carrinho do cliente atual, com detalhes dos produtos
        try:
            resultados = self.db.buscar_dado(
                "carrinho", 
                "cliente_id = ?", 
                (self.cliente_id,)
            )
            
            print(f"Resultados brutos do banco: {resultados}")  # Debug
            
            itens = []
            for item in resultados:
                item_id = item[1]
                tipo = item[2]
                quantidade = item[3]
                
                print(f"Processando item ID: {item_id}, Tipo: {tipo}")  # Debug
                
                produto = self.obter_produto_por_id(item_id, tipo)
                if produto:
                    print(f"Produto encontrado: {produto.sabor if hasattr(produto, 'sabor') else produto.tipo}")  # Debug
                    itens.append({
                        'id': item_id,
                        'produto': produto,
                        'quantidade': quantidade,
                        'tipo': tipo,
                        'preco': produto.preco 
                    })
                else:
                    print(f"Produto não encontrado para ID: {item_id}, Tipo: {tipo}")  # Debug
            
            print(f"Total de itens processados: {len(itens)}")  # Debug
            return itens
            
        except Exception as e:
            print(f"Erro ao buscar itens do carrinho: {str(e)}")
            return []

    def obter_produto_por_id(self, produto_id: int, tipo_produto: str) -> Union[Bolo, Salgado, None]:
        # Busca um produto (Bolo ou Salgado) pelo ID e tipo no banco
        try:
            if tipo_produto.lower() == "bolo":
                resultado = self.db.buscar_dado("bolos", "id = ?", (produto_id,))
                if resultado and len(resultado) > 0:
                    bolo_data = resultado[0]
                    preco = float(bolo_data[3]) if bolo_data[3] and str(bolo_data[3]).strip() else 0.0
                    return Bolo(
                        id=bolo_data[0],
                        sabor=bolo_data[1],
                        tamanho=bolo_data[2],
                        preco=preco,
                        descricao=bolo_data[4],
                        foto=bolo_data[5] if len(bolo_data) > 5 else ""
                    )
            
            elif tipo_produto.lower() == "salgado":
                resultado = self.db.buscar_dado("salgados", "id = ?", (produto_id,))
                if resultado and len(resultado) > 0:
                    salgado_data = resultado[0]
                    preco = float(salgado_data[3]) if salgado_data[3] and str(salgado_data[3]).strip() else 0.0
                    return Salgado(
                        id=salgado_data[0],
                        tipo=salgado_data[1],
                        recheio=salgado_data[2],
                        preco=preco,
                        descricao=salgado_data[4],
                        foto=salgado_data[5] if len(salgado_data) > 5 else ""
                    )
        
        except Exception as e:
            print(f"Erro ao obter produto: {str(e)}")
        
        return None

    def remover_item(self, item_id: int, tipo: str) -> bool:
        # Remove um item do carrinho pelo ID e tipo usando deletar no banco
        try:
            return self.db.deletar_dado(
                "carrinho",
                f"cliente_id = {self.cliente_id} AND item_id = {item_id} AND tipo = '{tipo}'"
            )
        except Exception as e:
            print(f"Erro ao remover item: {str(e)}")
            return False

    def limpar_carrinho(self) -> bool:
        # Remove todos os itens do carrinho do cliente atual
        return self.db.deletar_dado("carrinho", f"cliente_id = {self.cliente_id}")
