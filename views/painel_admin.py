import flet as ft
from models.bolo import Bolo
from models.salgado import Salgado
from controllers.alimento_controle import AlimentoControle
from controllers.cadastro_controle import CadastroControle


class PainelAdmin:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Painel do Admin"
        self.page.clean()

        self.cadastro_controle = CadastroControle()
        self.alimento_controle = AlimentoControle()

        self.tela_principal()

    def tela_principal(self) -> None:
        # Botão de logout no topo direito
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

        # Coluna com os botões principais centralizados vertical e horizontalmente
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
        
        self.page.add(
            ft.Container(
                content=ft.Column(
                    [
                        ft.ElevatedButton("Cadastrar Bolo", on_click=self.cadastrar_bolo),
                        ft.ElevatedButton("Cadastrar Salgado", on_click=self.cadastrar_salgado),
                        ft.ElevatedButton("Voltar", on_click=lambda e: self.__init__(self.page)),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,  # Alinha os itens verticalmente no centro
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Alinha os itens horizontalmente no centro
                ),
                alignment=ft.alignment.center,  # Centraliza o Column dentro do Container
                expand=True,  # Ocupa todo o espaço disponível
            )
        )
        self.page.update()


    def cadastrar_bolo(self, e):
        self.page.clean()

        campo_largura = 300

        self.sabor_field = ft.TextField(label="Sabor", autofocus=True, width=campo_largura)
        self.tamanho_field = ft.TextField(label="Tamanho", width=campo_largura)
        self.preco_field = ft.TextField(label="Preço", width=campo_largura)
        self.descricao_field = ft.TextField(label="Descrição", multiline=True, width=campo_largura)
        self.foto_field = ft.TextField(label="Foto (ex: fotos/coxinha.jpg)", width=campo_largura)

        self.salvar_bolo_button = ft.ElevatedButton("Salvar Bolo", on_click=self.salvar_bolo)
        self.voltar_button = ft.ElevatedButton("Voltar", on_click=self.cadastrar_novo_alimento)
        self.msg_text = ft.Text()

        conteudo = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Cadastro de Bolo", size=22, weight="bold"),
                    self.sabor_field,
                    self.tamanho_field,
                    self.preco_field,
                    self.descricao_field,
                    self.foto_field,
                    self.salvar_bolo_button,
                    self.voltar_button,
                    self.msg_text,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            alignment=ft.alignment.center,
            expand=True,
        )

        self.page.add(conteudo)
        self.page.update()


    def salvar_bolo(self, e):
        sabor = self.sabor_field.value.strip()
        preco = self.preco_field.value.strip()
        tamanho = self.tamanho_field.value.strip()
        descricao = self.descricao_field.value.strip()
        foto = self.foto_field.value.strip()

        bolo = Bolo(sabor, tamanho, preco, descricao, foto)
        erro = self.alimento_controle.adicionar_bolo(bolo)

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

        self.sabor_field = ft.TextField(label="Tipo", autofocus=True, width=campo_largura)
        self.tamanho_field = ft.TextField(label="Recheio", width=campo_largura)
        self.preco_field = ft.TextField(label="Preço", width=campo_largura)
        self.descricao_field = ft.TextField(label="Descrição", multiline=True, width=campo_largura)
        self.foto_field = ft.TextField(label="Foto (ex: fotos/coxinha.jpg)", width=campo_largura)

        self.salvar_bolo_button = ft.ElevatedButton("Salvar Bolo", on_click=self.salvar_salgado)
        self.voltar_button = ft.ElevatedButton("Voltar", on_click=self.cadastrar_novo_alimento)
        self.msg_text = ft.Text()

        conteudo = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Cadastro de Salgado", size=22, weight="bold"),
                    self.sabor_field,
                    self.tamanho_field,
                    self.preco_field,
                    self.descricao_field,
                    self.foto_field,
                    self.salvar_bolo_button,
                    self.voltar_button,
                    self.msg_text,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            alignment=ft.alignment.center,
            expand=True,
        )

        self.page.add(conteudo)
        self.page.update()

    def salvar_salgado(self, e):
        tipo = self.sabor_field.value.strip()
        preco = self.preco_field.value.strip()
        recheio = self.tamanho_field.value.strip()
        descricao = self.descricao_field.value.strip()
        foto = self.foto_field.value.strip()

        bolo = Salgado(tipo, recheio, preco, descricao, foto)
        erro = self.alimento_controle.adicionar_salgado(bolo)

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

        bolos = self.alimento_controle.listar_bolos()
        salgados = self.alimento_controle.listar_salgados()

        # Tabela de Bolos
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

        # Tabela de Salgados
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

        # Layout com tudo centralizado
        conteudo = ft.Column(
            [
                ft.Text("Bolos", size=24, weight="bold"),
                tabela_bolos,
                ft.Divider(),
                ft.Text("Salgados", size=24, weight="bold"),
                tabela_salgados,
                ft.ElevatedButton("Voltar", on_click=lambda e: self.__init__(self.page)),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO
        )

        self.page.add(conteudo)
        self.page.update()

    def excluir_salgado_handler(self, salgado, e):
        self.alimento_controle.excluir_salgado(salgado)
        self.listar_alimentos(e)  # Agora passando 'e' para o método
        self.page.update()

    def excluir_bolo_handler(self, bolo, e):
        self.alimento_controle.excluir_bolo(bolo)
        self.listar_alimentos(e)  # Agora passando 'e' para o método
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
        self.page.update()  # <--- IMPORTANTE: atualiza a UI com os novos handlers

    def salvar_edicao_salgado(self, e, salgado_antigo):
        tipo = self.tipo_ref.current.value
        recheio = self.recheio_ref.current.value
        preco = self.preco_ref.current.value
        descricao = self.descricao_ref.current.value
        foto = self.foto_ref.current.value

        print("Salvar clicado!")  # debug
        print(f"Tipo: {tipo}, Recheio: {recheio}, Preço: {preco}, Descrição: {descricao}, Foto: {foto}")  # debug

        salgado_novo = Salgado(tipo, recheio, preco, descricao, foto)
        erro = self.alimento_controle.editar_salgado(salgado_antigo, salgado_novo)
        print(f"Erro retornado: {erro}")  # DEBUG

        if erro:
            self.page.dialog = ft.AlertDialog(title=ft.Text(erro))
            self.page.dialog.open = True
            self.page.update()
        else:
            # Remove a view de edição atual da pilha de views
            if self.page.views:
                self.page.views.pop()
            # Vai para a rota da lista de alimentos (ou outra rota que queira)
            self.page.go("/painel_admin")
            self.listar_alimentos(None)  # atualiza a lista
        
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
        sabor = self.sabor_ref.current.value
        tamanho = self.tamanho_ref.current.value
        preco = self.preco_ref.current.value
        descricao = self.descricao_ref.current.value
        foto = self.foto_ref.current.value

        print("Salvar clicado!")
        print(f"Sabor: {sabor}, Tamanho: {tamanho}, Preço: {preco}, Descrição: {descricao}, Foto: {foto}")

        bolo_novo = Bolo(sabor, tamanho, preco, descricao, foto)
        erro = self.alimento_controle.editar_bolo(bolo_antigo, bolo_novo)
        print(f"Erro retornado: {erro}")  # DEBUG

        if erro:
            self.page.dialog = ft.AlertDialog(title=ft.Text(erro))
            self.page.dialog.open = True
        else:
            # Remove a view de edição atual da pilha de views
            if self.page.views:
                self.page.views.pop()
            # Vai para a rota da lista de alimentos (ou outra rota que queira)
            self.page.go("/painel_admin")
            self.listar_alimentos(None)  # atualiza a lista

        self.page.update()

    def cancelar_edicao(self, e):
        if self.page.views:
            self.page.views.pop()
        self.page.go("/painel_admin")
        self.listar_alimentos(None)
        self.page.update()

    def ver_lista_clientes(self, e) -> None:
        self.page.clean()

        cadastro_controle = CadastroControle()
        clientes = cadastro_controle.listar_clientes()

        if not clientes:
            self.page.add(
                ft.Column([
                    ft.Text("Nenhum cliente encontrado.", size=20),
                    ft.ElevatedButton("Voltar", on_click=lambda e: self.__init__(self.page))
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            )
            return

        # Cabeçalho da tabela
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

        self.page.add(
            ft.Column([
                ft.Text("Lista de Clientes", size=24, weight=ft.FontWeight.BOLD),
                ft.Column(lista_clientes, scroll=ft.ScrollMode.AUTO),
                ft.ElevatedButton("Voltar", on_click=lambda e: self.__init__(self.page))
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True)
        )

        self.page.update()

    def tornar_admin(self, cliente) -> None:
        cadastro_controle = CadastroControle()
        cadastro_controle.promover_cliente(cliente.nome, cliente.email)
        self.ver_lista_clientes(None)  # Atualiza a lista na interface

    def visualizar_pedidos(self, e) -> None:
        print("Visualizar pedidos")

    def logout(self, e) -> None:
        from views.tela_inicial import TelaInicial
        self.page.clean()
        TelaInicial(self.page)
