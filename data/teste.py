import database
import hashlib

def hash_senha(senha: str) -> str:
    return hashlib.sha256(senha.encode('utf-8')).hexdigest()

def criar_admin_teste():
    db = database.BaseDeDados()
    nome = "Admin"
    email = "1@gmail.com"
    senha = "123"
    senha_hash = hash_senha(senha)

    dados = [nome, email, senha_hash]

    try:
        admin_id = db.salvar_dado("admins", dados)
        print(f"Admin criado com ID: {admin_id}")
    except Exception as e:
        print(f"Erro ao criar admin: {e}")

if __name__ == "__main__":
    criar_admin_teste()
