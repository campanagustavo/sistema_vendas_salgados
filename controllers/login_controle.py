# controllers/login_controle.py

from models.cliente import Cliente
from models.admin import Admin
from data.database import buscar_dado

class LoginControle:
    def autenticar(self, login: Cliente):
        """
        Recebe um objeto Cliente com email e senha preenchidos.
        Verifica se ele é um admin ou cliente e autentica.
        Retorna um objeto Admin ou Cliente, ou string de erro.
        """
        email = login.email
        senha = login.senha

        # Tenta autenticar como admin
        admin = buscar_dado("admins", condicao=f"email = '{email}'")
        if admin:
            admin = admin[0]
            if admin[3] == senha:
                return Admin(admin[1], admin[2], admin[3])
            else:
                return "Senha incorreta."

        # Tenta autenticar como cliente
        cliente = buscar_dado("clientes", condicao=f"email = '{email}'")
        if cliente:
            cliente = cliente[0]
            if cliente[3] == senha:
                return Cliente(cliente[1], cliente[2], cliente[3])
            else:
                return "Senha incorreta."

        return "E-mail não encontrado."
