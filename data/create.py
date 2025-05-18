import sqlite3
import os
# inicializar banco e criar tabelas, ser executado uma única vez

DB_FILENAME = 'sistema_geral.db'
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), DB_FILENAME)

def criar_tabelas():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

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
            preco REAL NOT NULL,
            tipo TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_usuario INTEGER NOT NULL,
            data_pedido DATETIME DEFAULT CURRENT_TIMESTAMP,
            valor_total REAL NOT NULL,
            FOREIGN KEY (id_usuario) REFERENCES usuarios (id) ON DELETE SET NULL ON UPDATE CASCADE
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS itens_pedido (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_pedido INTEGER NOT NULL,      -- Chave estrangeira para pedidos
    id_alimento INTEGER NOT NULL,    -- Chave estrangeira para alimentos
    quantidade INTEGER NOT NULL,     -- Quantidade deste alimento específico neste pedido
    preco_unitario REAL NOT NULL,   -- Preço do alimento no momento da compra (importante, pois preços podem mudar)
    FOREIGN KEY (id_pedido) REFERENCES pedidos (id) ON DELETE CASCADE, -- Se um pedido for deletado, seus itens também são.
    FOREIGN KEY (id_alimento) REFERENCES alimentos (id)
    -- UNIQUE (id_pedido, id_alimento) -- Opcional: garante que um alimento não seja adicionado duas vezes ao mesmo pedido como linhas separadas (a menos que você queira permitir isso e somar as quantidades)
)
 """)
    

    conn.commit()
    conn.close()
    print("Tabelas criadas com sucesso!")

if __name__ == "__main__":
    criar_tabelas()
