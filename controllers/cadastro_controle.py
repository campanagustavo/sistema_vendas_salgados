from data.database import BaseDeDados
from models.cliente import Cliente
from models.usuario import Usuario
from typing import List

class CadastroControle:
    def __init__(self) -> None:
        # Inicializa a conexão com o banco de dados
        self.db = BaseDeDados()

    def cadastrar_cliente(self, usuario: Usuario) -> str | None:
        # LÓGICA SIMPLES ADICIONADA AQUI:
        if "@" not in usuario.email or "." not in usuario.email:
            return "Formato de e-mail inválido."

        # RESTANTE DO SEU CÓDIGO ORIGINAL:
        # Verifica se os campos do usuário estão preenchidos corretamente
        if not usuario.campos_validos:
            return "Todos os campos devem ser preenchidos."
        
        # Obtém a condição e os valores para a busca (exemplo: "email = ?")
        condicao, valores = usuario.dados_chave()

        # Verifica se o usuário já existe nas tabelas 'clientes' ou 'admins'
        if self.db.buscar_dado("clientes", condicao, valores) or self.db.buscar_dado("admins", condicao, valores):
            return "Usuário já cadastrado com este e-mail."

        try:
            # Tenta salvar os dados do novo cliente no banco
            self.db.salvar_dado(usuario.tabela, usuario.dados_para_salvar())
            return None  # Cadastro realizado com sucesso
        except Exception as e:
            # Caso ocorra erro, imprime no console e retorna mensagem
            print(f"Erro ao cadastrar cliente: {e}")
            return f"Erro: {e}"

    def listar_clientes(self) -> List[Cliente]:
        # Tenta buscar todos os clientes no banco de dados
        try:
            df = self.db.listar_dados("clientes")  # Recebe os dados em DataFrame
            clientes = []
            for _, row in df.iterrows():
                # Para cada linha do DataFrame, cria objeto Cliente
                cliente = Cliente(row['nome'], row['email'], row['senha'], id=row['id'])
                clientes.append(cliente)
            return clientes  # Retorna lista de objetos Cliente
        except Exception as e:
            # Se erro, imprime e retorna lista vazia
            print(f"Erro ao listar clientes: {e}")
            return []

    def promover_cliente(self, email: str) -> None:
        # Tenta promover cliente a admin pelo email
        try:
            resultado = self.db.buscar_dado("clientes", "email = ?", (email,))
            cliente_data = resultado[0]
            # Cria objeto Cliente com dados retornados
            cliente = Cliente(nome=cliente_data[1], email=cliente_data[2], senha=cliente_data[3], senha_ja_hasheada=True)

            # Converte Cliente para Admin
            admin = cliente.virar_admin
            # Salva novo admin e remove cliente da tabela clientes
            self.db.salvar_dado("admins", admin.dados_para_salvar())
            self.db.deletar_dado("clientes", "email = ?", (email,))
        except Exception as e:
            print(f"Erro ao promover cliente: {e}")

    def obter_cliente_por_id(self, cliente_id: int) -> Cliente | None:
        # Busca cliente no banco pelo ID
        resultado = self.db.buscar_dado("clientes", "id = ?", [cliente_id])
        if resultado:
            # Retorna objeto Cliente com os dados encontrados
            return Cliente(
                id=resultado[0][0],
                nome=resultado[0][1],
                email=resultado[0][2],
                senha=resultado[0][3]
            )
        # Se não encontrar, retorna None
        return None