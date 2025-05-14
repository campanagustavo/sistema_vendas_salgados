from data.database import salvar_dado
from models.cliente import Cliente

class CadastroControle:
    def cadastrar_cliente(self, novousuario):
        try:
            # Verificação de campos vazios
            if not novousuario.nome or not novousuario.email or not novousuario.senha:
                return "Todos os campos devem ser preenchidos."
            
            # Salvar os dados no banco
            salvar_dado("clientes", [novousuario.nome, novousuario.email, novousuario.senha])
            return None  # Nenhum erro, cadastro bem-sucedido.
        except Exception as e:
            print(f"Erro ao cadastrar cliente: {e}")
            return f"Erro: {e}"  # Retorna a mensagem de erro
