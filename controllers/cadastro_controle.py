from data.database import salvar_dado, buscar_dado, deletar_dado
from models.cliente import Cliente

class CadastroControle:
    def cadastrar_cliente(self, novousuario):
        try:
            if not novousuario.nome or not novousuario.email or not novousuario.senha:
                return "Todos os campos devem ser preenchidos."

            existente = buscar_dado("clientes", condicao=f"email = '{novousuario.email}'")
            existente = buscar_dado("admins", condicao=f"email = '{novousuario.email}'")
            
            if existente:
                return "Usuário já cadastrado com este e-mail."

            salvar_dado("clientes", [novousuario.nome, novousuario.email, novousuario.senha])
            return None
        except Exception as e:
            print(f"Erro ao cadastrar cliente: {e}")
            return f"Erro: {e}"

    def listar_clientes(self):
        # Buscar os dados dos clientes
        resultados = buscar_dado("clientes", "1=1")  # Condição '1=1' para pegar todos os clientes

        # Verificar se não há resultados
        if not resultados:
            return []

        # Criar uma lista de clientes a partir dos resultados
        clientes = []
        for resultado in resultados:
            id, nome, email, senha = resultado
            cliente = Cliente(nome, email, senha)
            clientes.append(cliente)

        return clientes

    def promover_cliente(self, nome: str, email: str) -> None:
        resultados = buscar_dado("clientes", condicao=f"email = '{email}'")
        if not resultados:
            print("Cliente não encontrado!")
            return

        # Supondo que clientes tem colunas (id, nome, email, senha)
        _, nome_cliente, email_cliente, senha_cliente = resultados[0]

        salvar_dado("admins", [nome_cliente, email_cliente, senha_cliente])

        condicao = f"email = '{email}'"
        deletar_dado("clientes", condicao)
