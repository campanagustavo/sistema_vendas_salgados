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
        
        barra_superior = self.criar_barra_superior("Cadastrar Alimento")
        
        self.page.add(
            ft.Column(
                [
                    barra_superior,
                    ft.Container(
                        content=ft.Column(
                            [
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

        barra_superior = self.criar_barra_superior("Cadastrar Bolo")

        self.sabor_field = ft.TextField(label="Sabor", autofocus=True, width=campo_largura)
        self.tamanho_field = ft.TextField(label="Tamanho", width=campo_largura)
        self.preco_field = ft.TextField(label="Preço", width=campo_largura)
        self.descricao_field = ft.TextField(label="Descrição", multiline=True, width=campo_largura)
        self.foto_field = ft.TextField(label="Foto (ex: fotos/coxinha.jpg)", width=campo_largura)

        self.salvar_bolo_button = ft.ElevatedButton("Salvar Bolo", on_click=self.salvar_bolo)
        self.msg_text = ft.Text()

        conteudo = ft.Column(
            controls=[
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

        barra_superior = self.criar_barra_superior("Cadastrar Salgado")

        self.sabor_field = ft.TextField(label="Tipo", autofocus=True, width=campo_largura)
        self.tamanho_field = ft.TextField(label="Recheio", width=campo_largura)
        self.preco_field = ft.TextField(label="Preço", width=campo_largura)
        self.descricao_field = ft.TextField(label="Descrição", multiline=True, width=campo_largura)
        self.foto_field = ft.TextField(label="Foto (ex: fotos/coxinha.jpg)", width=campo_largura)

        self.salvar_bolo_button = ft.ElevatedButton("Salvar Salgado", on_click=self.salvar_salgado)
        self.msg_text = ft.Text()

        conteudo = ft.Column(
            controls=[
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

        barra_superior = self.criar_barra_superior("Editar/Excluir Alimentos")

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
        self.alimento_controle.excluir_salgado(salgado)
        self.listar_alimentos(e)
        self.page.update()

    def excluir_bolo_handler(self, bolo, e):
        self.alimento_controle.excluir_bolo(bolo)
        self.listar_alimentos(e)
        self.page.update()

    def abrir_edicao_salgado(self, salgado):
        self.page.clean()

        barra_superior = self.criar_barra_superior("Editar Salgado")

        self.tipo_ref = ft.TextField(label="Tipo", value=salgado.tipo)
        self.recheio_ref = ft.TextField(label="Recheio", value=salgado.recheio)
        self.preco_ref = ft.TextField(label="Preço", value=str(salgado.preco))
        self.descricao_ref = ft.TextField(label="Descrição", value=salgado.descricao)
        self.foto_ref = ft.TextField(label="Foto (URL)", value=salgado.foto)

        conteudo = ft.Column(
            controls=[
                self.tipo_ref,
                self.recheio_ref,
                self.preco_ref,
                self.descricao_ref,
                self.foto_ref,
                ft.Row([
                    ft.ElevatedButton(
                        "Salvar",
                        on_click=lambda e: self.salvar_edicao_salgado(e, salgado)
                    ),
                    ft.ElevatedButton(
                        "Cancelar",
                        on_click=lambda e: self.listar_alimentos(e)
                    ),
                ])
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
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

    def salvar_edicao_salgado(self, e, salgado_antigo):
        # Obter os valores dos campos
        tipo = self.tipo_ref.value
        recheio = self.recheio_ref.value
        preco = self.preco_ref.value
        descricao = self.descricao_ref.value
        foto = self.foto_ref.value

        # Verificar se houve alterações
        if (tipo == salgado_antigo.tipo and
            recheio == salgado_antigo.recheio and
            preco == salgado_antigo.preco and
            descricao == salgado_antigo.descricao and
            foto == salgado_antigo.foto):
            
            # Mostrar mensagem se não houve alterações
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("Nenhuma alteração foi feita."),
                bgcolor=ft.Colors.ORANGE
            )
            self.page.snack_bar.open = True
            self.page.update()
            return

        # Criar o novo objeto Salgado
        salgado_novo = Salgado(tipo, recheio, preco, descricao, foto)

        # Tentar editar no banco de dados
        erro = self.alimento_controle.editar_salgado(salgado_antigo, salgado_novo)

        if erro:
            # Mostrar erro se ocorrer
            self.page.dialog = ft.AlertDialog(
                title=ft.Text("Erro ao salvar"),
                content=ft.Text(erro),
                actions=[ft.TextButton("OK", on_click=lambda _: self.page.close_dialog())]
            )
            self.page.dialog.open = True
        else:
            # Mostrar mensagem de sucesso
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("Salgado atualizado com sucesso!"),
                bgcolor=ft.Colors.GREEN
            )
            self.page.snack_bar.open = True
            
            # Voltar para a lista de alimentos
            self.listar_alimentos(None)

        self.page.update()

    def abrir_edicao_bolo(self, bolo):
        self.page.clean()

        barra_superior = self.criar_barra_superior("Editar Bolo")

        self.sabor_ref = ft.TextField(label="Sabor", value=bolo.sabor)
        self.tamanho_ref = ft.TextField(label="Tamanho", value=bolo.tamanho)
        self.preco_ref = ft.TextField(label="Preço", value=str(bolo.preco))
        self.descricao_ref = ft.TextField(label="Descrição", value=bolo.descricao)
        self.foto_ref = ft.TextField(label="Foto (URL)", value=bolo.foto)

        conteudo = ft.Column(
            controls=[
                self.sabor_ref,
                self.tamanho_ref,
                self.preco_ref,
                self.descricao_ref,
                self.foto_ref,
                ft.Row([
                    ft.ElevatedButton(
                        "Salvar",
                        on_click=lambda e: self.salvar_edicao_bolo(e, bolo)
                    ),
                    ft.ElevatedButton(
                        "Cancelar",
                        on_click=lambda e: self.listar_alimentos(e)
                    ),
                ])
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
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

    def salvar_edicao_bolo(self, e, bolo_antigo):
        sabor = self.sabor_ref.value
        tamanho = self.tamanho_ref.value
        preco = self.preco_ref.value
        descricao = self.descricao_ref.value
        foto = self.foto_ref.value

        # Verifica se houve alterações
        if (sabor == bolo_antigo.sabor and
            tamanho == bolo_antigo.tamanho and
            preco == bolo_antigo.preco and
            descricao == bolo_antigo.descricao and
            foto == bolo_antigo.foto):
            self.msg_text.value = "Nenhuma alteração foi feita."
            self.msg_text.color = ft.Colors.ORANGE
            self.page.update()
            return

        bolo_novo = Bolo(sabor, tamanho, preco, descricao, foto)
        erro = self.alimento_controle.editar_bolo(bolo_antigo, bolo_novo)

        if erro:
            self.page.dialog = ft.AlertDialog(title=ft.Text(erro))
            self.page.dialog.open = True
        else:
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

    def visualizar_pedidos(self, e) -> None:
        self.page.clean()

        barra_superior = self.criar_barra_superior("Visualizar Pedidos")

        conteudo = ft.Column(
            controls=[
                ft.Text("Funcionalidade em desenvolvimento", size=20),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
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

    def logout(self, e) -> None:
        from views.tela_inicial import TelaInicial
        self.page.clean()
        TelaInicial(self.page)