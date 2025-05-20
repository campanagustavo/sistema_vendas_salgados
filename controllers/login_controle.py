from models.cliente import Cliente
from models.admin import Admin
from data.database import BaseDeDados

class LoginControle:
    def __init__(self) -> None:
        # Inicializa conexão com banco de dados
        self.db = BaseDeDados()

    def autenticar(self, email: str, senha: str) -> tuple[object | None, str | None]:
        # Tenta autenticar usuário (Admin ou Cliente) pelo email e senha
        tabelas = [("admins", Admin), ("clientes", Cliente)]

        for tabela, classe_usuario in tabelas:
            # Busca usuário pelo email na tabela atual
            resultado = self.db.buscar_dado(tabela, "email = ?", (email,))
            if not resultado:
                continue  # não achou nessa tabela, tenta próxima

            usuario_data = resultado[0]
            # Cria o objeto do usuário com dados do banco
            usuario = classe_usuario(
                id=usuario_data[0],
                nome=usuario_data[1],
                email=usuario_data[2],
                senha=usuario_data[3]
            )

            # Valida as credenciais informadas
            if not usuario.validar_credenciais(email, senha):
                return None, "E-mail ou senha incorretos"

            return usuario, None  # autenticado com sucesso

        # Não encontrou email em nenhuma tabela
        return None, "E-mail não cadastrado"
