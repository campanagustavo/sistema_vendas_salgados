import flet as ft
from models.bolo import Bolo
from models.salgado import Salgado
from controllers.alimento_controle import AlimentoControle
from controllers.cadastro_controle import CadastroControle
from controllers.pedido_controle import PedidoControle


class PainelAdmin:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Painel do Admin"
        self.page.clean()
        self.cadastro_controle = CadastroControle()
        self.alimento_controle = AlimentoControle()
        self.pedido_controle = PedidoControle()
        self.tela_principal()

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

    def tela_principal(self) -> None:
        self.page.clean()
        
        barra_superior = self.criar_barra_superior(mostrar_voltar=False)

        botoes = ft.Column(
            [
                ft.Text("Painel Administrador", size=24, weight=ft.FontWeight.BOLD),
                ft.ElevatedButton("Cadastrar Novo Alimento", on_click=self.cadastrar_novo_alimento),
                ft.ElevatedButton("Editar/Excluir Alimento", on_click=self.listar_alimentos),
                ft.ElevatedButton("Visualizar Pedidos", on_click=self.visualizar_pedidos),
                ft.ElevatedButton("Ver Lista de Usuários", on_click=self.ver_lista_clientes),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

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
                expand=True
            )
        )

    def cadastrar_novo_alimento(self, e):
        self.page.clean()
        
        barra_superior = self.criar_barra_superior()
        
        self.page.add(
            ft.Column(
                [
                    barra_superior,
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text("Cadastrar Alimento", size=24, weight=ft.FontWeight.BOLD),
                                ft.ElevatedButton("Cadastrar Bolo", on_click=self.cadastrar_bolo),
                                ft.ElevatedButton("Cadastrar Salgado", on_click=self.cadastrar_salgado),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        alignment=ft.alignment.center,
                        expand=True,
                    )
                ],
                expand=True
            )
        )

    def cadastrar_bolo(self, e):
        self.page.clean()

        campo_largura = 300

        barra_superior = self.criar_barra_superior()

        self.sabor_field = ft.TextField(label="Sabor", autofocus=True, width=campo_largura)
        self.tamanho_field = ft.TextField(label="Tamanho", width=campo_largura)
        self.preco_field = ft.TextField(label="Preço", width=campo_largura)
        self.descricao_field = ft.TextField(label="Descrição", multiline=True, width=campo_largura)
        self.foto_field = ft.TextField(label="Foto (ex: fotos/coxinha.jpg)", width=campo_largura)

        self.salvar_bolo_button = ft.ElevatedButton("Salvar Bolo", on_click=self.salvar_bolo)
        self.msg_text = ft.Text()

        conteudo = ft.Column(
            controls=[
                ft.Text("Cadastro de Bolo", size=24, weight=ft.FontWeight.BOLD),
                self.sabor_field,
                self.tamanho_field,
                self.preco_field,
                self.descricao_field,
                self.foto_field,
                self.salvar_bolo_button,
                self.msg_text,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        self.page.add(
            ft.Column(
                [
                    barra_superior,
                    ft.Container(
                        content=conteudo,
                        alignment=ft.alignment.center,
                        expand=True,
                    )
                ],
                expand=True
            )
        )

    def salvar_bolo(self, e):
        # preço tem que ser numero
        try:
            preco_valor = float(self.preco_field.value.strip().replace(',', '.'))
        except (ValueError, TypeError):
            self.msg_text.value = "Erro: O preço deve ser um número."
            self.msg_text.color = ft.Colors.RED
            self.page.update()
            return
            
        sabor = self.sabor_field.value.strip()
        tamanho = self.tamanho_field.value.strip()
        descricao = self.descricao_field.value.strip()
        foto = self.foto_field.value.strip()

        bolo = Bolo(sabor, tamanho, preco_valor, descricao, foto)
        erro = self.alimento_controle.adicionar_alimento(bolo)

        if erro:
            self.msg_text.value = erro
            self.msg_text.color = ft.Colors.RED
        else:
            self.msg_text.value = "Bolo cadastrado com sucesso!"
            self.msg_text.color = ft.Colors.GREEN
            self.sabor_field.value = ""
            self.tamanho_field.value = ""
            self.preco_field.value = ""
            self.descricao_field.value = ""
            self.foto_field.value = ""

        self.page.update()

    def cadastrar_salgado(self, e) -> None:
        self.page.clean()

        campo_largura = 300

        barra_superior = self.criar_barra_superior()

        self.sabor_field = ft.TextField(label="Tipo", autofocus=True, width=campo_largura)
        self.tamanho_field = ft.TextField(label="Recheio", width=campo_largura)
        self.preco_field = ft.TextField(label="Preço", width=campo_largura)
        self.descricao_field = ft.TextField(label="Descrição", multiline=True, width=campo_largura)
        self.foto_field = ft.TextField(label="Foto (ex: fotos/coxinha.jpg)", width=campo_largura)

        self.salvar_bolo_button = ft.ElevatedButton("Salvar Salgado", on_click=self.salvar_salgado)
        self.msg_text = ft.Text()

        conteudo = ft.Column(
            controls=[
                ft.Text("Cadastro de Salgado", size=24, weight=ft.FontWeight.BOLD),
                self.sabor_field,
                self.tamanho_field,
                self.preco_field,
                self.descricao_field,
                self.foto_field,
                self.salvar_bolo_button,
                self.msg_text,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        self.page.add(
            ft.Column(
                [
                    barra_superior,
                    ft.Container(
                        content=conteudo,
                        alignment=ft.alignment.center,
                        expand=True,
                    )
                ],
                expand=True
            )
        )

    def salvar_salgado(self, e):
        # preço tem que ser número
        try:
            preco_valor = float(self.preco_field.value.strip().replace(',', '.'))
        except (ValueError, TypeError):
            self.msg_text.value = "Erro: O preço deve ser um número."
            self.msg_text.color = ft.Colors.RED
            self.page.update()
            return
            
        tipo = self.sabor_field.value.strip()
        recheio = self.tamanho_field.value.strip()
        descricao = self.descricao_field.value.strip()
        foto = self.foto_field.value.strip()

        salgado = Salgado(tipo, recheio, preco_valor, descricao, foto)
        erro = self.alimento_controle.adicionar_alimento(salgado)

        if erro:
            self.msg_text.value = erro
            self.msg_text.color = ft.Colors.RED
        else:
            self.msg_text.value = "Salgado cadastrado com sucesso!"
            self.msg_text.color = ft.Colors.GREEN
            self.sabor_field.value = ""
            self.tamanho_field.value = ""
            self.preco_field.value = ""
            self.descricao_field.value = ""
            self.foto_field.value = ""

        self.page.update()

    def listar_alimentos(self, e):
        self.page.clean()

        barra_superior = self.criar_barra_superior("Editar/Excluir Alimentos")

        bolos = self.alimento_controle.listar_alimentos(Bolo, "bolos")
        salgados = self.alimento_controle.listar_alimentos(Salgado, "salgados")

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
                            ft.Row([
                                ft.ElevatedButton("Editar", on_click=lambda e, b=bolo: self.abrir_edicao_bolo(b)),
                                ft.ElevatedButton("Excluir", on_click=lambda e: self.excluir_bolo_handler(bolo, e))
                            ])
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
                            ft.Row([
                                ft.ElevatedButton("Editar", on_click=lambda e, s=salgado: self.abrir_edicao_salgado(s)),
                                ft.ElevatedButton("Excluir", on_click=lambda e: self.excluir_salgado_handler(salgado, e))
                            ])
                        ),
                    ]
                ) for salgado in salgados
            ]
        )

        conteudo = ft.Column(
            [
                ft.Text("Bolos", size=24, weight="bold"),
                tabela_bolos,
                ft.Divider(),
                ft.Text("Salgados", size=24, weight="bold"),
                tabela_salgados,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO
        )

        self.page.add(
            ft.Column(
                [
                    barra_superior,
                    ft.Container(
                        content=conteudo,
                        alignment=ft.alignment.center,
                        expand=True,
                    )
                ],
                expand=True
            )
        )

    def excluir_salgado_handler(self, salgado, e):
        condicao = "id = ?"
        parametros = (salgado.id,)
        self.alimento_controle.excluir_alimento("salgados", condicao, parametros)
        self.listar_alimentos(e)
        self.page.update()

    def excluir_bolo_handler(self, bolo, e):
        condicao = "id = ?"
        parametros = (bolo.id,)
        self.alimento_controle.excluir_alimento("bolos", condicao, parametros)
        self.listar_alimentos(e)
        self.page.update()



    def abrir_edicao_salgado(self, salgado):
        self.tipo_ref = ft.Ref()
        self.recheio_ref = ft.Ref()
        self.preco_ref = ft.Ref()
        self.descricao_ref = ft.Ref()
        self.foto_ref = ft.Ref()

        editar_view = ft.View(
            "/editar_salgado",
            controls=[
                ft.Text("Editar Salgado", size=30, weight="bold"),
                ft.TextField(label="Tipo", value=salgado.tipo, ref=self.tipo_ref),
                ft.TextField(label="Recheio", value=salgado.recheio, ref=self.recheio_ref),
                ft.TextField(label="Preço", value=str(salgado.preco), ref=self.preco_ref),
                ft.TextField(label="Descrição", value=salgado.descricao, ref=self.descricao_ref),
                ft.TextField(label="Foto (URL)", value=salgado.foto, ref=self.foto_ref),
                ft.Row([
                    ft.ElevatedButton(
                        "Salvar",
                        on_click=lambda e: self.salvar_edicao_salgado(e, salgado)
                    ),
                    ft.ElevatedButton(
                        "Cancelar",
                        on_click=lambda e: self.cancelar_edicao(e)
                    ),
                ])
            ],
            vertical_alignment=ft.MainAxisAlignment.CENTER
        )

        self.page.views.append(editar_view)
        self.page.go("/editar_salgado")
        self.page.update()  #atualiza a UI com os novos handlers

    def salvar_edicao_salgado(self, e, salgado_antigo):
        # preço tem que ser número
        try:
            preco_valor = float(self.preco_ref.current.value.strip().replace(',', '.'))
        except (ValueError, TypeError):
            self.mostrar_erro("Erro: O preço deve ser um número.")
            return

        tipo = self.tipo_ref.current.value
        recheio = self.recheio_ref.current.value
        descricao = self.descricao_ref.current.value
        foto = self.foto_ref.current.value

        print("Salvar clicado!")
        print(f"ID Antigo: {salgado_antigo.id}, Tipo: {tipo}, Recheio: {recheio}, Preço: {preco_valor}, Descrição: {descricao}, Foto: {foto}")

        # Criar o novo objeto Salgado com o ID do antigo e os novos dados
        salgado_novo = Salgado(id=salgado_antigo.id, tipo=tipo, recheio=recheio, preco=preco_valor, descricao=descricao, foto=foto)
        
        # O método editar_salgado agora deve usar o ID para encontrar o registro
        erro = self.alimento_controle.editar_alimento("salgados", salgado_antigo, salgado_novo, ["tipo", "recheio", "preco", "descricao", "foto"])
        print(f"Erro retornado: {erro}")

        if erro:
            self.page.dialog = ft.AlertDialog(title=ft.Text(erro))
            self.page.dialog.open = True
            self.page.update()
        else:
            if self.page.views:
                self.page.views.pop()
            self.page.go("/painel_admin")
            if hasattr(self, 'listar_alimentos'): # Garante que o método existe
                self.listar_alimentos(None) 
        
        self.page.update()

    def abrir_edicao_bolo(self, bolo):
        self.sabor_ref = ft.Ref()
        self.tamanho_ref = ft.Ref()
        self.preco_ref = ft.Ref()
        self.descricao_ref = ft.Ref()
        self.foto_ref = ft.Ref()

        editar_view = ft.View(
            "/editar_bolo",
            controls=[
                ft.Text("Editar Bolo", size=30, weight="bold"),
                ft.TextField(label="Sabor", value=bolo.sabor, ref=self.sabor_ref),
                ft.TextField(label="Tamanho", value=bolo.tamanho, ref=self.tamanho_ref),
                ft.TextField(label="Preço", value=str(bolo.preco), ref=self.preco_ref),
                ft.TextField(label="Descrição", value=bolo.descricao, ref=self.descricao_ref),
                ft.TextField(label="Foto (URL)", value=bolo.foto, ref=self.foto_ref),
                ft.Row([
                    ft.ElevatedButton(
                        "Salvar",
                        on_click=lambda e: self.salvar_edicao_bolo(e, bolo)
                    ),
                    ft.ElevatedButton(
                        "Cancelar",
                        on_click=lambda e: self.cancelar_edicao(e)
                    ),
                ])
            ],
            vertical_alignment=ft.MainAxisAlignment.CENTER
        )

        self.page.views.append(editar_view)
        self.page.go("/editar_bolo")
        self.page.update()


    def salvar_edicao_bolo(self, e, bolo_antigo):
        # preço tem que ser numero
        try:
            preco_valor = float(self.preco_ref.current.value.strip().replace(',', '.'))
        except (ValueError, TypeError):
            self.mostrar_erro("Erro: O preço deve ser um número.")
            return

        sabor = self.sabor_ref.current.value
        tamanho = self.tamanho_ref.current.value
        descricao = self.descricao_ref.current.value
        foto = self.foto_ref.current.value
        
        print("Salvar clicado!")
        print(f"ID Antigo: {bolo_antigo.id}, Sabor: {sabor}, Tamanho: {tamanho}, Preço: {preco_valor}, Descrição: {descricao}, Foto: {foto}")

        # Criar o novo objeto Bolo com o ID do antigo e os novos dados
        bolo_novo = Bolo(id=bolo_antigo.id, sabor=sabor, tamanho=tamanho, preco=preco_valor, descricao=descricao, foto=foto)
        
        # O método editar_bolo agora deve usar o ID para encontrar o registro
        erro = self.alimento_controle.editar_alimento("bolos", bolo_antigo, bolo_novo, ["sabor", "tamanho", "preco", "descricao", "foto"]) 
        print(f"Erro retornado: {erro}")

        if erro:
            self.page.dialog = ft.AlertDialog(title=ft.Text(erro))
            self.page.dialog.open = True
            # self.page.update() # O update já ocorre no final do método
        else:
            if self.page.views:
                self.page.views.pop()
            self.page.go("/painel_admin")
            if hasattr(self, 'listar_alimentos'): # Garante que o método existe
                self.listar_alimentos(None)

        self.page.update()

    def ver_lista_clientes(self, e) -> None:
        self.page.clean()

        barra_superior = self.criar_barra_superior("Lista de Clientes")

        cadastro_controle = CadastroControle()
        clientes = cadastro_controle.listar_clientes()

        if not clientes:
            conteudo = ft.Column([
                ft.Text("Nenhum cliente encontrado.", size=20),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        else:
            cabecalho = ft.Row(
                controls=[
                    ft.Container(ft.Text("Nome", weight=ft.FontWeight.BOLD), width=200),
                    ft.Container(ft.Text("Email", weight=ft.FontWeight.BOLD), width=250),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            )

            lista_clientes = [cabecalho]

            for cliente in clientes:
                linha = ft.Row(
                    controls=[
                        ft.Container(ft.Text(cliente.nome), width=200),
                        ft.Container(ft.Text(cliente.email), width=250),
                        ft.Container(
                            ft.ElevatedButton(
                                "Tornar Admin",
                                on_click=lambda e, c=cliente: self.tornar_admin(c)
                            ),
                            width=150
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                )
                lista_clientes.append(linha)

            conteudo = ft.Column(
                controls=[
                    ft.Column(lista_clientes, scroll=ft.ScrollMode.AUTO),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )

        self.page.add(
            ft.Column(
                [
                    barra_superior,
                    ft.Container(
                        content=conteudo,
                        alignment=ft.alignment.center,
                        expand=True,
                    )
                ],
                expand=True
            )
        )

    def tornar_admin(self, cliente) -> None:
        cadastro_controle = CadastroControle()
        cadastro_controle.promover_cliente(cliente.email)
        self.ver_lista_clientes(None)

    def visualizar_pedidos(self, e):
        """Mostra todos os pedidos centralizados SEM alterar a lógica existente"""
        self.page.clean()
        
        barra_superior = self.criar_barra_superior("Visualizar Pedidos")
        
        pedidos = self.pedido_controle.listar_todos_pedidos()
        print(f"Pedidos recuperados: {len(pedidos)}")

        if not pedidos:
            conteudo = ft.Column(
                [
                    ft.Text("Nenhum pedido encontrado.", size=20),
                    ft.ElevatedButton("Recarregar", on_click=self.visualizar_pedidos)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        else:
            # Tabela original (como estava funcionando)
            tabela_pedidos = self._criar_tabela_pedidos(pedidos)
            
            # Container centralizado (ÚNICA mudança necessária)
            conteudo = ft.Container(
                content=ft.Column([
                    ft.Text("Todos os Pedidos", size=24, weight=ft.FontWeight.BOLD),
                    tabela_pedidos
                ]),
                alignment=ft.alignment.center,
                padding=20
            )

        # Layout principal (sem alterações)
        self.page.add(
            ft.Column(
                [barra_superior, conteudo],
                expand=True
            )
        )

    def _criar_tabela_pedidos(self, pedidos):
        """Cria a tabela de pedidos com itens em lista vertical e linhas mais altas"""
        colunas = [
            ft.DataColumn(ft.Text("ID", text_align=ft.TextAlign.CENTER)),
            ft.DataColumn(ft.Text("Cliente", text_align=ft.TextAlign.CENTER)),
            ft.DataColumn(ft.Text("Itens", text_align=ft.TextAlign.LEFT)),
            ft.DataColumn(ft.Text("Total", text_align=ft.TextAlign.CENTER)),
            ft.DataColumn(ft.Text("Status", text_align=ft.TextAlign.CENTER)),
            ft.DataColumn(ft.Text("Ações", text_align=ft.TextAlign.CENTER)),
        ]
        
        linhas = []
        
        for pedido in sorted(pedidos, key=lambda p: p.id, reverse=True):
            try:
                cliente = self.cadastro_controle.obter_cliente_por_id(pedido.cliente_id)
                nome_cliente = cliente.nome if cliente else f"ID: {pedido.cliente_id}"
                
                # Formata itens com quantidades
                itens_com_quantidade = []
                for item in pedido.itens:
                    produto = item['produto']
                    if produto:
                        nome = produto.sabor if hasattr(produto, 'sabor') else produto.tipo
                        tipo = "Bolo" if hasattr(produto, 'sabor') else "Salgado"
                        quantidade = item['quantidade']
                        itens_com_quantidade.append(f"{nome} ({tipo}) x{quantidade}")
                
                # Cria coluna com itens (sem scroll)
                coluna_itens = ft.Column(
                    controls=[ft.Text(item, size=14) for item in itens_com_quantidade],
                    spacing=5,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.START,
                )
                
                dropdown_status = ft.Dropdown(
                    width=150,
                    value=pedido.status,
                    options=[
                        ft.dropdown.Option("Confirmado"),
                        ft.dropdown.Option("Em preparo"),
                        ft.dropdown.Option("Finalizado"),
                        ft.dropdown.Option("Entregue"),
                        ft.dropdown.Option("Concluído"),
                        ft.dropdown.Option("Cancelado"),
                    ],
                    text_size=14,
                )
                
                # Célula de status
                celula_status = ft.DataCell(
                    ft.Container(
                        ft.Text(
                            pedido.status,
                            color=self._obter_cor_status(pedido.status),
                            weight=ft.FontWeight.BOLD,
                            text_align=ft.TextAlign.CENTER
                        ),
                        padding=10,
                        border_radius=5,
                        alignment=ft.alignment.center,
                        bgcolor=ft.Colors.with_opacity(0.1, self._obter_cor_status(pedido.status))
                    ))
                
                # Célula de ações
                celula_acoes = ft.DataCell(
                    ft.Row(
                        controls=[
                            dropdown_status,
                            ft.ElevatedButton(
                                "Atualizar",
                                on_click=lambda e, p=pedido, d=dropdown_status: self._atualizar_status_pedido(p, d)
                            ),
                        ],
                        spacing=10
                    )
                )
                
                linha = ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(pedido.id), text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(ft.Text(nome_cliente, text_align=ft.TextAlign.CENTER)),
                        ft.DataCell(coluna_itens),
                        ft.DataCell(ft.Text(f"R$ {pedido.total:.2f}", text_align=ft.TextAlign.CENTER)),
                        celula_status,
                        celula_acoes
                    ]
                )
                linhas.append(linha)
                
            except Exception as ex:
                print(f"Erro ao processar pedido {pedido.id}: {str(ex)}")
                continue
        
        return ft.DataTable(
            columns=colunas,
            rows=linhas,
            horizontal_margin=20,
            column_spacing=20,
            heading_row_color=ft.Colors.GREY_300,
            heading_row_height=45,
            divider_thickness=1.5,
            width=float("inf"),
        )

    def _obter_cor_status(self, status):
        """Retorna a cor correspondente ao status do pedido"""
        cores = {
            "Confirmado": ft.Colors.BLUE,
            "Em preparo": ft.Colors.ORANGE,
            "Finalizado": ft.Colors.PURPLE,
            "Entregue": ft.Colors.GREEN,
            "Concluído": ft.Colors.TEAL,
            "Cancelado": ft.Colors.RED,
        }
        return cores.get(status, ft.Colors.GREY)

    def _atualizar_status_pedido(self, pedido, dropdown):
        """Atualiza o status de um pedido"""
        novo_status = dropdown.value  # Obtém o valor selecionado no dropdown
        
        if pedido.status == novo_status:
            return
        
        if self.pedido_controle.atualizar_status_pedido(pedido.id, novo_status):
            self.mostrar_mensagem(f"Status do pedido #{pedido.id} atualizado para {novo_status}!")
            self.visualizar_pedidos(None)  # Recarrega a lista
        else:
            self.mostrar_mensagem("Erro ao atualizar status do pedido!")

    def mostrar_mensagem(self, mensagem):
        """Mostra uma mensagem simples"""
        self.page.snack_bar = ft.SnackBar(ft.Text(mensagem))
        self.page.snack_bar.open = True
        self.page.update()

    def mostrar_erro(self, mensagem):
        self.page.dialog = ft.AlertDialog(
            title=ft.Text("Erro"),
            content=ft.Text(mensagem),
            actions=[ft.TextButton("OK", on_click=lambda _: self.page.close_dialog())]
        )
        self.page.dialog.open = True
        self.page.update()

    def mostrar_aviso(self, mensagem):
        self.page.dialog = ft.AlertDialog(
            title=ft.Text("Aviso"),
            content=ft.Text(mensagem),
            actions=[ft.TextButton("OK", on_click=lambda _: self.page.close_dialog())]
        )
        self.page.dialog.open = True
        self.page.update()

    def mostrar_sucesso(self, mensagem):
        self.page.dialog = ft.AlertDialog(
            title=ft.Text("Sucesso"),
            content=ft.Text(mensagem),
            actions=[ft.TextButton("OK", on_click=lambda _: self.listar_alimentos(None))]
        )
        self.page.dialog.open = True
        self.page.update()

    def cancelar_edicao(self, e):
        if self.page.views:
            self.page.views.pop()
        self.page.go("/painel_admin")
        self.page.update()

    def logout(self, e) -> None:
        from views.tela_inicial import TelaInicial
        self.page.clean()
        TelaInicial(self.page)