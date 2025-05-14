# Simulação de banco de dados
import sqlite3
import os

DB_FILENAME = "banco_dados.db"
class BasedeDados:
    def __init__(self):
        self.db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), DB_FILENAME)
        self.conn = None  # A conexão será estabelecida quando necessário

    def conectar(self):
        if self.conn is None:
            try:
                self.conn = sqlite3.connect(self.db_path)
            except sqlite3.Error as e:
                print(f"Erro ao conectar ao banco de dados: {e}")

    def criar_tabelas(self):
        self.conectar()  # Garante que há uma conexão
        if not self.conn:
            print("Não foi possível criar tabelas: sem conexão com o banco.")
            return

        sql_queries = [
            """
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                senha TEXT NOT NULL, -- Lembre-se de armazenar senhas hasheadas!
                tipo_usuario TEXT NOT NULL CHECK(tipo_usuario IN ('cliente', 'admin')),

            );
            """,
            """
            CREATE TABLE IF NOT EXISTS alimentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                descricao TEXT,
                preco REAL NOT NULL,
                tipo_alimento TEXT NOT NULL CHECK(tipo_alimento IN ('bolo', 'salgado')),
                ingredientes TEXT,
                tamanho TEXT,      -- Específico para bolo
                recheio TEXT,      -- Específico para bolo
                cobertura TEXT,    -- Específico para bolo
                tipo_massa TEXT,   -- Específico para salgado
                disponivel INTEGER DEFAULT 1, -- 1 para true, 0 para false
                imagem_path TEXT   -- Caminho para a imagem do alimento
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS pedidos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id INTEGER NOT NULL,
                data_pedido TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                status_pedido TEXT NOT NULL DEFAULT 'pendente'
                                CHECK(status_pedido IN ('pendente', 'em_preparo', 'pronto_entrega', 'entregue', 'cancelado')),
                valor_total REAL NOT NULL,
        
                FOREIGN KEY (cliente_id) REFERENCES usuarios (id) ON DELETE CASCADE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS itens_pedido (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pedido_id INTEGER NOT NULL,
                alimento_id INTEGER NOT NULL,
                quantidade INTEGER NOT NULL,
                preco_unitario REAL NOT NULL, -- Preço no momento da compra
                total REAL NOT NULL,       -- Calculado: quantidade * preco_unitario
                FOREIGN KEY (pedido_id) REFERENCES pedidos (id) ON DELETE CASCADE,
                FOREIGN KEY (alimento_id) REFERENCES alimentos (id) ON DELETE RESTRICT
            );
            """
        ]
        try:
            cursor = self.conn.cursor()
            for query in sql_queries:
                cursor.execute(query)
            self.conn.commit()
            print(f"Tabelas do banco '{DB_FILENAME}' verificadas/criadas em '{self.db_path}'.")
        except sqlite3.Error as e:
            print(f"Erro ao criar tabelas: {e}")