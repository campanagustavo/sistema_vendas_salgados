from data.database import BaseDeDados
from models.cliente import Cliente

class CadastroControle:
    def __init__(self):
        self.db = BaseDeDados()

    def cadastrar_cliente(self, novousuario):
        try:
            if not novousuario.nome or not novousuario.email or not novousuario.senha:
                return "Todos os campos devem ser preenchidos."

            # Verificar se o usuário já existe em 'clientes' ou 'admins'
            existente = self.db.buscar_dado("clientes", f"email = '{novousuario.email}'")
            if not existente:
                existente = self.db.buscar_dado("admins", f"email = '{novousuario.email}'")

            if existente:
                return "Usuário já cadastrado com este e-mail."

            # Inserir novo cliente
            self.db.salvar_dado("clientes", [novousuario.nome, novousuario.email, novousuario.senha])
            return None
        except Exception as e:
            print(f"Erro ao cadastrar cliente: {e}")
            return f"Erro: {e}"

    def listar_clientes(self):
        try:
            df = self.db.listar_dados("clientes")
            clientes = []
            for _, row in df.iterrows():
                cliente = Cliente(row['nome'], row['email'], row['senha'], id=row['id'])
                clientes.append(cliente)
            return clientes
        except Exception as e:
            print(f"Erro ao listar clientes: {e}")
            return []

    def promover_cliente(self, email: str) -> None:
        try:
            resultado = self.db.buscar_dado("clientes", f"email = '{email}'")
            if not resultado:
                print("Cliente não encontrado!")
                return

            # Assumindo que o retorno é uma lista de tuplas
            cliente_data = resultado[0]
            nome_cliente, email_cliente, senha_cliente = cliente_data[1], cliente_data[2], cliente_data[3]

            # Inserir em 'admins'
            self.db.salvar_dado("admins", [nome_cliente, email_cliente, senha_cliente])

            # Deletar da tabela 'clientes'
            self.db.deletar_dado("clientes", f"email = '{email}'")

        except Exception as e:
            print(f"Erro ao promover cliente: {e}")
