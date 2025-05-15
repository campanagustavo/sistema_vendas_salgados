from models.cliente import Cliente
from models.admin import Admin
from data.database import BaseDeDados

class LoginControle:
    def __init__(self):
        self.db = BaseDeDados()

    def autenticar(self, login: Cliente):
        """
        Recebe um objeto Cliente com email e senha preenchidos.
        Verifica se ele é um admin ou cliente e autentica.
        Retorna um objeto Admin ou Cliente com todos os dados, ou string de erro.
        """
        email = login.email
        senha = login.senha

        # Tenta autenticar como admin
        admin = self.db.buscar_dado("admins", "email = ?", (email,))
        if admin:
            admin = admin[0]
            if admin[3] == senha:
                return Admin(nome=admin[1], email=admin[2], senha=admin[3], id=admin[0])
            else:
                return "Senha incorreta."

        # Tenta autenticar como cliente
        cliente_data = self.db.buscar_dado("clientes", "email = ?", (email,))
        if cliente_data:
            cliente_data = cliente_data[0]
            if cliente_data[3] == senha:
                return Cliente(
                    nome=cliente_data[1],
                    email=cliente_data[2],
                    senha=cliente_data[3],
                    id=cliente_data[0]
                )
            else:
                return "Senha incorreta."
        
        # Se chegou aqui, o email não foi encontrado nem em admins nem em clientes
        return "E-mail não cadastrado."