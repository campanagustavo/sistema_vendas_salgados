import flet as ft
from controllers.alimento_controle import AlimentoControle
from controllers.carrinho_controle import CarrinhoControle
from controllers.pedido_controle import PedidoControle
from models.cliente import Cliente
from models.pedido import Pedido
from models.salgado import Salgado
from models.bolo import Bolo

class PainelCliente:
    def __init__(self, page: ft.Page, cliente : Cliente) -> None:
        self.page = page
        self.page.title = "Painel do Cliente"
        self.page.clean()

        self.pedido_controle = PedidoControle()
        self.dialogo_pagamento = None
        self.cliente = cliente
        self.alimento_controle = AlimentoControle()
        self.carrinho = CarrinhoControle(cliente_id=cliente.id)
        self.tela_principal()

    def tela_principal(self) -> None:
        self.page.clean()

        barra_superior = self.criar_barra_superior(mostrar_voltar=False)
        # Botões centrais (Visualizar Cardápio e Acompanhar Pedidos)
        botoes = ft.Column(
            [
                ft.Text("Painel Cliente", size=24, weight=ft.FontWeight.BOLD),
                ft.ElevatedButton("Visualizar Cardápio", on_click=self.visualizar_cardapio, width=200),
                ft.ElevatedButton("Acompanhar meus Pedidos", on_click=self.acompanhar_pedidos, width=200),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
            expand=True,
        )

        # Adiciona os componentes na página
        self.page.add(
            ft.Column(
                [
                    barra_superior,
                    ft.Container(
                        content=botoes,
                        expand=True,
                        alignment=ft.alignment.center,
                    )
                ],
                expand=True,
            )
        )

    def visualizar_cardapio(self, e: ft.ControlEvent) -> None:
        self.page.clean()
        
        # Dicionário para armazenar as quantidades temporárias
        self.quantidades = {produto.id: 0 for produto in self.alimento_controle.listar_alimentos(Bolo, "bolos") + self.alimento_controle.listar_alimentos(Salgado, "salgados")}

        # Barra superior com botões
        barra_superior = ft.Row(
            controls=[
                ft.ElevatedButton(
                    "Voltar",
                    on_click=lambda e: self.tela_principal(),
                    icon=ft.Icons.ARROW_BACK
                ),
                ft.Container(expand=True),
                ft.ElevatedButton(
                    "Ir para Carrinho",
                    on_click=self.ir_para_carrinho,
                    icon=ft.Icons.SHOPPING_CART
                ),
                ft.IconButton(
                    icon=ft.Icons.EXIT_TO_APP,
                    on_click=self.logout,
                    tooltip="Logout",
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

        bolos = self.alimento_controle.listar_alimentos(Bolo, "bolos")
        salgados = self.alimento_controle.listar_alimentos(Salgado, "salgados")

        def criar_controle_quantidade(produto):
            quantidade_text = ft.Text("0", width=30, text_align=ft.TextAlign.CENTER)
            
            def diminuir(e):
                if self.quantidades[produto.id] > 0:
                    self.quantidades[produto.id] -= 1
                    quantidade_text.value = str(self.quantidades[produto.id])
                    self.page.update()
            
            def aumentar(e):
                self.quantidades[produto.id] += 1
                quantidade_text.value = str(self.quantidades[produto.id])
                self.page.update()
            
            def adicionar_carrinho(e):
                if self.quantidades[produto.id] > 0:
                    for _ in range(self.quantidades[produto.id]):
                        self.carrinho.adicionar_item(produto)
                    self.quantidades[produto.id] = 0
                    quantidade_text.value = "0"
                    self.mostrar_mensagem(f"{self.quantidades[produto.id]}x {produto.sabor if hasattr(produto, 'sabor') else produto.tipo} adicionado(s) ao carrinho!")
                    self.page.update()
            
            return ft.Row(
                [
                    ft.IconButton(
                        icon=ft.Icons.REMOVE,
                        on_click=diminuir,
                        icon_size=20,
                        tooltip="Diminuir quantidade",
                    ),
                    quantidade_text,
                    ft.IconButton(
                        icon=ft.Icons.ADD,
                        on_click=aumentar,
                        icon_size=20,
                        tooltip="Aumentar quantidade",
                    ),
                    ft.ElevatedButton(
                        "Adicionar",
                        on_click=adicionar_carrinho,
                        width=100,
                        height=30
                    )
                ],
                spacing=0,
                alignment=ft.MainAxisAlignment.CENTER,
                width=200
            )

        # Criar as tabelas
        tabela_bolos = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Sabor", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Tamanho", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Preço", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Descrição", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Quantidade", weight=ft.FontWeight.BOLD)),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(bolo.sabor)),
                        ft.DataCell(ft.Text(bolo.tamanho)),
                        ft.DataCell(ft.Text(bolo.preco)),
                        ft.DataCell(ft.Text(bolo.descricao)),
                        ft.DataCell(criar_controle_quantidade(bolo)),
                    ]
                ) for bolo in bolos
            ],
            width=900
        )

        tabela_salgados = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Tipo", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Recheio", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Preço", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Descrição", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Quantidade", weight=ft.FontWeight.BOLD)),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(salgado.tipo)),
                        ft.DataCell(ft.Text(salgado.recheio)),
                        ft.DataCell(ft.Text(salgado.preco)),
                        ft.DataCell(ft.Text(salgado.descricao)),
                        ft.DataCell(criar_controle_quantidade(salgado)),
                    ]
                ) for salgado in salgados
            ],
            width=900
        )

        # Container principal
        container_principal = ft.Container(
            content=ft.Column(
                [
                    ft.Text("Cardápio", size=28, weight=ft.FontWeight.BOLD),
                    
                    ft.Text("Bolos", size=22, weight=ft.FontWeight.BOLD),
                    ft.Container(
                        content=tabela_bolos,
                        height=300,
                        border=ft.border.all(1, ft.Colors.GREY_300),
                        border_radius=10,
                        alignment=ft.alignment.center,
                        padding=10,
                    ),
                    
                    ft.Text("Salgados", size=22, weight=ft.FontWeight.BOLD),
                    ft.Container(
                        content=tabela_salgados,
                        height=300,
                        border=ft.border.all(1, ft.Colors.GREY_300),
                        border_radius=10,
                        alignment=ft.alignment.center,
                        padding=10,
                    ),
                ],
                spacing=20,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                scroll=ft.ScrollMode.AUTO,
            ),
            alignment=ft.alignment.top_center,
            padding=20,
            expand=True
        )

        self.page.add(
            ft.Column(
                [
                    barra_superior,
                    container_principal
                ],
                expand=True,
                scroll=ft.ScrollMode.AUTO
            )
        )

    def mostrar_mensagem(self, mensagem):
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(mensagem),
            bgcolor=ft.Colors.GREEN_400,
            duration=2000
        )
        self.page.snack_bar.open = True

    def adicionar_ao_carrinho(self, produto):
        # Cria um componente de mensagem (se ainda não existir)
        if not hasattr(self, 'msg_text'):
            self.msg_text = ft.Text("", size=16)
            # Adiciona o componente à sua interface (ajuste conforme sua estrutura)
            self.page.add(self.msg_text)  # Ou adicione ao container apropriado
        
        try:
            # Verifica se o produto tem ID
            if not hasattr(produto, 'id') or not produto.id:
                raise ValueError("Produto sem ID válido")
            
            # Adiciona ao carrinho
            self.carrinho.adicionar_item(produto)
            
            # Mensagem de sucesso
            nome_produto = produto.sabor if hasattr(produto, 'sabor') else produto.tipo
            self.msg_text.value = f"{nome_produto} adicionado ao carrinho com sucesso!"
            self.msg_text.color = ft.Colors.GREEN
        
        finally:
            self.page.update()

    def ir_para_carrinho(self, e):

        print(self.carrinho.obter_produto_por_id(3, 'bolo'))
        print(self.carrinho.obter_produto_por_id(4, 'bolo'))
        print(self.carrinho.obter_produto_por_id(5, 'salgado'))
        print(self.carrinho.obter_produto_por_id(6, 'bolo'))

        self.page.clean()
        
        # Barra superior
        barra_superior = ft.Row(
            controls=[
                ft.ElevatedButton(
                    "Voltar ao Cardápio",
                    on_click=self.visualizar_cardapio,
                    icon=ft.Icons.ARROW_BACK
                ),
                ft.Container(expand=True),
                ft.IconButton(
                    icon=ft.Icons.EXIT_TO_APP,
                    on_click=self.logout,
                    tooltip="Logout",
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )
        
        # Obter itens do carrinho
        itens_carrinho = self.carrinho.listar_itens()
        
        # Criar lista de itens
        lista_itens = ft.Column(spacing=10)
        total_pedido = 0.0
        
        if itens_carrinho:
            for item in itens_carrinho:
                produto = item['produto']
                quantidade = item['quantidade']
                subtotal = produto.preco * quantidade
                total_pedido += subtotal
                
                def criar_callback(item_id=item['id'], tipo=item['tipo']):
                    return lambda e: self.remover_item_carrinho(item_id, tipo)
                
                nome = f"{produto.sabor} ({produto.tamanho})" if hasattr(produto, 'sabor') else f"{produto.tipo} ({produto.recheio})"
                
                lista_itens.controls.append(
                    ft.Card(
                        content=ft.Container(
                            content=ft.Column([
                                ft.ListTile(
                                    title=ft.Text(nome, weight=ft.FontWeight.BOLD),
                                    subtitle=ft.Text(f"Preço unitário: R$ {produto.preco:.2f}"),
                                ),
                                ft.Row([
                                    ft.Text(f"Quantidade: {quantidade}", width=150),
                                    ft.Text(f"Subtotal: R$ {subtotal:.2f}", weight=ft.FontWeight.BOLD),
                                    ft.IconButton(
                                        icon=ft.Icons.DELETE,
                                        on_click=criar_callback(),
                                        icon_color=ft.Colors.RED,
                                        tooltip="Remover item"
                                    )
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                            ]),
                            padding=10
                        )
                    )
                )
        
        # Área de finalização (só aparece se houver itens)
        area_finalizacao = ft.Column([
            ft.Divider(),
            ft.Row([
                ft.Text("Total do Pedido:", size=18, weight=ft.FontWeight.BOLD),
                ft.Text(f"R$ {total_pedido:.2f}", size=18, weight=ft.FontWeight.BOLD),
            ], alignment=ft.MainAxisAlignment.END),
            ft.ElevatedButton(
                "Finalizar Pedido",
                on_click=self.finalizar_pedido,
                icon=ft.Icons.CHECK_CIRCLE,
                bgcolor=ft.Colors.GREEN,
                color=ft.Colors.WHITE,
                width=200
            )
        ], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.END) if itens_carrinho else None
        
        # Conteúdo principal
        conteudo_principal = ft.Column([
            ft.Text("Meu Carrinho", size=24, weight=ft.FontWeight.BOLD),
            lista_itens if itens_carrinho else ft.Text(
                "Seu carrinho está vazio",
                size=18,
                color=ft.Colors.GREY
            ),
            area_finalizacao if area_finalizacao is not None else ft.Container()  # Container vazio se não houver itens
        ], scroll=ft.ScrollMode.AUTO)
        
        # Layout completo
        self.page.add(
            ft.Column([
                barra_superior,
                ft.Container(
                    content=conteudo_principal,
                    padding=20,
                    expand=True
                )
            ], expand=True)
        )

    def remover_item_carrinho(self, item_id, tipo):
        """Remove um item do carrinho e atualiza a tela"""
        try:
            if self.carrinho.remover_item(item_id, tipo):
                self.mostrar_mensagem("Item removido do carrinho!")
            else:
                self.mostrar_mensagem("Erro ao remover item!")
            
            # Recarrega a tela do carrinho
            self.ir_para_carrinho(None)
        except Exception as e:
            self.mostrar_mensagem(f"Erro: {str(e)}")


    def finalizar_pedido(self, e):
        """Versão centralizada da tela de pagamento"""
        print("Botão finalizar pedido clicado!")
        
        # Verifica se há itens no carrinho
        itens = self.carrinho.listar_itens()
        if not itens:
            self.mostrar_mensagem("Seu carrinho está vazio!")
            return
        
        # Cria uma nova página de pagamento
        self.page.clean()
        
        # Barra superior
        barra_superior = ft.Row(
            controls=[
                ft.ElevatedButton(
                    "Voltar ao Carrinho",
                    on_click=self.ir_para_carrinho,
                    icon=ft.Icons.ARROW_BACK
                ),
                ft.Container(expand=True),
                ft.IconButton(
                    icon=ft.Icons.EXIT_TO_APP,
                    on_click=self.logout,
                    tooltip="Logout",
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )
        
        # Calcula o total
        total = sum(item['produto'].preco * item['quantidade'] for item in itens)
        
        # Container centralizado
        container_central = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(f"Total do Pedido: R$ {total:.2f}", 
                        size=24, 
                        weight="bold",
                        text_align="center"),
                    ft.Divider(height=20),
                    ft.Text("Selecione a forma de pagamento:", 
                        size=20,
                        text_align="center"),
                    ft.Column(
                        controls=[
                            ft.ElevatedButton(
                                "PIX",
                                icon=ft.Icons.PAYMENT,
                                on_click=lambda e: self.processar_pagamento("PIX"),
                                width=200
                            ),
                            ft.ElevatedButton(
                                "Cartão de Crédito",
                                icon=ft.Icons.CREDIT_CARD,
                                on_click=lambda e: self.processar_pagamento("Cartão de Crédito"),
                                width=200
                            ),
                            ft.ElevatedButton(
                                "Cartão de Débito",
                                icon=ft.Icons.CREDIT_CARD_OUTLINED,
                                on_click=lambda e: self.processar_pagamento("Cartão de Débito"),
                                width=200
                            ),
                        ],
                        spacing=15,
                        horizontal_alignment="center"
                    )
                ],
                spacing=20,
                horizontal_alignment="center",
                alignment="center"
            ),
            alignment=ft.alignment.center,
            expand=True
        )
        
        # Layout principal
        self.page.add(
            ft.Column(
                controls=[
                    barra_superior,
                    container_central
                ],
                expand=True
            )
        )

    def _abrir_dialogo(self):
        """Abre o diálogo de pagamento"""
        if not hasattr(self, 'dialogo_pagamento'):
            print("Erro: Diálogo não foi criado!")
            return
        
        self.page.dialog = self.dialogo_pagamento
        self.dialogo_pagamento.open = True
        self.page.update()
        print("Diálogo aberto com sucesso")

    def _fechar_dialogo(self):
        """Fecha o diálogo de pagamento"""
        if hasattr(self, 'dialogo_pagamento') and self.dialogo_pagamento:
            self.dialogo_pagamento.open = False
            self.page.update()

    def processar_pagamento(self, metodo: str):
        """Versão corrigida que limpa tudo e mostra a confirmação"""
        print(f"Processando pagamento: {metodo}")
        
        itens_carrinho = self.carrinho.listar_itens()

        if not itens_carrinho:
            self.mostrar_mensagem("Seu carrinho está vazio!")
            return
        
        try:
            pedido = self.pedido_controle.criar_pedido(
                cliente_id=self.cliente.id,
                itens=itens_carrinho,
                metodo_pagamento=metodo
            )
            print(f"Pedido #{pedido.id} criado - Total: R${pedido.total:.2f}")
        except Exception as e:
            print(f"Erro ao criar pedido: {str(e)}")
            self.mostrar_mensagem("Erro ao processar pagamento!")
            return
        
        # 1. Limpa o carrinho
        self.carrinho.limpar_carrinho()
        
        # 2. Limpa a página completamente
        self.page.clean()
        
        # 3. Cria a tela de confirmação
        barra_superior = ft.Row(
            controls=[
                ft.Container(expand=True),
                ft.IconButton(
                    icon=ft.Icons.EXIT_TO_APP,
                    on_click=self.logout,
                    tooltip="Logout",
                )
            ],
            alignment=ft.MainAxisAlignment.END
        )
        
        conteudo = ft.Column(
            [
                ft.Icon(ft.Icons.CHECK_CIRCLE, size=100, color="green"),
                ft.Text("Pedido Confirmado!", size=30, weight="bold"),
                ft.Text(f"Método: {metodo}", size=20),
                ft.ElevatedButton(
                    "Voltar ao Início",
                    on_click=lambda e: self.tela_principal(),
                    icon=ft.Icons.HOME,
                    width=200
                )
            ],
            spacing=30,
            alignment="center",
            horizontal_alignment="center"
        )
        
        # Adiciona à página
        self.page.add(
            ft.Column(
                [
                    barra_superior,
                    ft.Container(
                        content=conteudo,
                        alignment=ft.alignment.center,
                        expand=True
                    )
                ],
                expand=True
            )
        )
        
        # Atualiza a página
        self.page.update()
        print("Tela de confirmação exibida!")


    def acompanhar_pedidos(self, e):
        """Mostra pedidos centralizados na tela"""
        self.page.clean()
        
        barra_superior = self.criar_barra_superior()
        
        # Conteúdo centralizado
        conteudo = ft.Column(
            [
                ft.Text(
                    "Meus Pedidos",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER
                ),
                self._construir_lista_pedidos()
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )
        
        # Layout principal
        self.page.add(
            ft.Column(
                [
                    barra_superior,
                    ft.Container(
                        content=conteudo,
                        alignment=ft.alignment.center,
                        expand=True,
                        padding=20
                    )
                ],
                expand=True
            )
        )
        self.page.update()

    def _construir_lista_pedidos(self):
        """Constroi a lista de pedidos"""
        from controllers.pedido_controle import PedidoControle
        pedidos = PedidoControle().listar_pedidos_por_cliente(self.cliente.id)
        pedidos.sort(key=lambda p: p.id, reverse=True)
        
        if not pedidos:
            return ft.Column(
                [
                    ft.Icon(ft.Icons.SHOPPING_BAG_OUTLINED, size=48),
                    ft.Text("Você não possui pedidos ainda.", size=18),
                    ft.ElevatedButton(
                        "Ver Cardápio",
                        on_click=self.visualizar_cardapio,
                        icon=ft.Icons.RESTAURANT_MENU
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                height=300,
                alignment=ft.MainAxisAlignment.CENTER
            )
        
        return ft.Column(
            controls=[self._criar_card_pedido(pedido) for pedido in pedidos],
            spacing=15,
            width=600
        )

    def _criar_card_pedido(self, pedido):
        """Cria um card para cada pedido"""
        status_color = {
            "Confirmado": ft.Colors.BLUE_400,
            "Em preparo": ft.Colors.ORANGE_400,
            "Cancelado": ft.Colors.RED_400,
            "Entregue": ft.Colors.GREEN_400
        }.get(pedido.status, ft.Colors.GREY_400)
        
        # Ações condicionais
        acoes = ft.Container()  # Vazio por padrão
        
        if pedido.pode_cancelar():
            acoes = ft.ElevatedButton(
                "Cancelar",
                on_click=lambda e, p=pedido: self.cancelar_pedido(p),
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.RED_700,
                tooltip="Cancelar este pedido"
            )
        else:
            acoes = ft.Text(
                f"Status: {pedido.status}",
                color=status_color,
                italic=True
            )
        
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Text(f"Pedido #{pedido.id}", 
                                    weight=ft.FontWeight.BOLD,
                                    size=18),
                                ft.Container(expand=True),
                                ft.Text(
                                    pedido.status,
                                    color=status_color,
                                    weight=ft.FontWeight.BOLD
                                )
                            ]
                        ),
                        ft.Divider(height=1),
                        ft.Column(
                            [ft.Text(f"Total: R$ {pedido.total:.2f}")],
                            spacing=5
                        ),
                        ft.Divider(height=1),
                        ft.Row(
                            [
                                ft.Text(f"Total: R$ {pedido.total:.2f}", 
                                    weight=ft.FontWeight.BOLD),
                                ft.Container(expand=True),
                                ft.Text(f"Pagamento: {pedido.metodo_pagamento}"),
                            ]
                        ),
                        ft.Row([ft.Container(expand=True), acoes]) if acoes else None
                    ],
                    spacing=10,
                    width=550
                ),
                padding=15,
            ),
            elevation=3,
            width=600
        )

    def cancelar_pedido(self, pedido: Pedido):
        from controllers.pedido_controle import PedidoControle
        
        # Verifica se o pedido pode ser cancelado
        if not pedido.pode_cancelar():
            self.mostrar_mensagem(f"Não é possível cancelar pedido {pedido.status.lower()}")
            return
        
        pedido_controle = PedidoControle()
        if pedido_controle.atualizar_status_pedido(pedido.id, "Cancelado"):
            self.mostrar_mensagem(f"Pedido #{pedido.id} cancelado com sucesso!")
            # Atualiza a lista de pedidos
            self.acompanhar_pedidos(None)
        else:
            self.mostrar_mensagem("Erro ao cancelar pedido!")

    def logout(self, e) -> None:
        from views.tela_inicial import TelaInicial
        self.page.clean()
        TelaInicial(self.page)


    def criar_barra_superior(self, titulo=None, mostrar_voltar=True):
        """Método para criar a barra superior padrão com título centralizado"""
        controles = []
        
        if mostrar_voltar:
            controles.append(
                ft.ElevatedButton(
                    "Voltar",
                    on_click=lambda e: self.tela_principal(),
                    icon=ft.Icons.ARROW_BACK
                )
            )
        else:
            controles.append(ft.Container(width=100))  # Espaço vazio para alinhamento
            
        # Container central para o título
        titulo_container = ft.Container(
            content=ft.Text(
                titulo if titulo else "", 
                size=50, 
                weight=ft.FontWeight.BOLD
            ),
            alignment=ft.alignment.center,
            expand=True
        )
        
        controles.append(titulo_container)
            
        controles.append(
            ft.IconButton(
                icon=ft.Icons.EXIT_TO_APP,
                on_click=self.logout,
                tooltip="Logout",
            )
        )
        
        return ft.Row(
            controls=controles,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )
    