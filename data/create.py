import sqlite3
import os
# inicializar banco e criar tabelas, ser executado uma única vez

DB_FILENAME = 'sistema_geral.db'
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), DB_FILENAME)

def criar_tabelas():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Tabela de usuários (exemplo)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL
        )
    """)

    # Tabela de alimentos (exemplo)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alimentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            calorias INTEGER NOT NULL,
            tipo TEXT NOT NULL
        )
    """)

    # Adicione outras tabelas aqui...

    conn.commit()
    conn.close()
    print("Tabelas criadas com sucesso!")

if __name__ == "__main__":
    criar_tabelas()
