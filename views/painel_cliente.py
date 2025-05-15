import flet as ft
from controllers.alimento_controle import AlimentoControle
from controllers.carrinho_controle import CarrinhoControle
from models.cliente import Cliente

class PainelCliente:
    def __init__(self, page: ft.Page, cliente : Cliente) -> None:
        self.page = page
        self.page.title = "Painel do Cliente"
        self.page.clean()

        self.cliente = cliente
        self.alimento_controle = AlimentoControle()
        self.carrinho = CarrinhoControle(cliente_id=cliente.id)
        self.tela_principal()

    def tela_principal(self) -> None:
        self.page.clean()
        # Barra superior com logout no canto direito
        barra_superior = ft.Row(
            controls=[
                ft.Container(expand=True),  # empurra o botão para a direita
                ft.IconButton(
                    icon=ft.Icons.EXIT_TO_APP,
                    on_click=self.logout,
                    tooltip="Logout",
                )
            ],
            alignment=ft.MainAxisAlignment.END
        )

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

        # Barra superior com botão de voltar e logout
        barra_superior = ft.Row(
            controls=[
                ft.ElevatedButton(
                    "Voltar",
                    on_click=lambda e: self.tela_principal(),
                    icon=ft.Icons.ARROW_BACK
                ),
                ft.Container(expand=True),  # empurra o botão para a direita
                ft.IconButton(
                    icon=ft.Icons.EXIT_TO_APP,
                    on_click=self.logout,
                    tooltip="Logout",
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

        bolos = self.alimento_controle.listar_bolos()
        salgados = self.alimento_controle.listar_salgados()

        tabela_bolos = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Sabor")),
                ft.DataColumn(ft.Text("Tamanho")),
                ft.DataColumn(ft.Text("Preço")),
                ft.DataColumn(ft.Text("Descrição")),
                ft.DataColumn(ft.Text("Foto")),
                ft.DataColumn(ft.Text("Ações")),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(bolo.sabor)),
                        ft.DataCell(ft.Text(bolo.tamanho)),
                        ft.DataCell(ft.Text(str(bolo.preco))),
                        ft.DataCell(ft.Text(bolo.descricao)),
                        ft.DataCell(ft.Text(bolo.foto)),
                        ft.DataCell(
                            ft.ElevatedButton(
                                "Adicionar ao Carrinho",
                                on_click=lambda e, b=bolo: self.adicionar_ao_carrinho(b)
                            )      
                        ),
                    ]
                ) for bolo in bolos
            ]
        )

        tabela_salgados = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Tipo")),
                ft.DataColumn(ft.Text("Recheio")),
                ft.DataColumn(ft.Text("Preço")),
                ft.DataColumn(ft.Text("Descrição")),
                ft.DataColumn(ft.Text("Foto")),
                ft.DataColumn(ft.Text("Ações")),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(salgado.tipo)),
                        ft.DataCell(ft.Text(salgado.recheio)),
                        ft.DataCell(ft.Text(str(salgado.preco))),
                        ft.DataCell(ft.Text(salgado.descricao)),
                        ft.DataCell(ft.Text(salgado.foto)),
                        ft.DataCell(
                            ft.ElevatedButton(
                                "Adicionar ao Carrinho",
                                on_click=lambda e, b=salgado: self.adicionar_ao_carrinho(b)
                            )      
                        ),
                    ]
                ) for salgado in salgados
            ]
        )

        self.page.add(
            ft.Column(
                controls=[
                    barra_superior,
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text("Cardápio", size=24, weight=ft.FontWeight.BOLD),
                                ft.Text("Bolos", size=20, weight=ft.FontWeight.BOLD),
                                tabela_bolos,
                                ft.Text("Salgados", size=20, weight=ft.FontWeight.BOLD),
                                tabela_salgados,
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        ),
                        expand=True,
                        alignment=ft.alignment.center
                    )
                ],
                expand=True
            )
        )

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
            
            # Opcional: Mostrar também um SnackBar como feedback adicional
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(f"{nome_produto} adicionado ao carrinho!"),
                bgcolor=ft.Colors.GREEN_400,
                duration=2000  # 2 segundos
            )
            self.page.snack_bar.open = True
            
        except Exception as e:
            print(f"Erro ao adicionar ao carrinho: {str(e)}")
            self.msg_text.value = f"Erro: {str(e)}"
            self.msg_text.color = ft.Colors.RED
            
            # SnackBar de erro
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Erro ao adicionar: {str(e)}"),
                bgcolor=ft.Colors.RED_400
            )
            self.page.snack_bar.open = True
        
        finally:
            self.page.update()

    def acompanhar_pedidos(self, e: ft.ControlEvent) -> None:
        print("Acompanhar Pedidos clicado")

    def logout(self, e) -> None:
        from views.tela_inicial import TelaInicial
        self.page.clean()
        TelaInicial(self.page)