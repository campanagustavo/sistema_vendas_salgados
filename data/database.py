import os
import sqlite3
import pandas as pd

class BaseDeDados:
    def __init__(self, db_filename='sistema_geral.db'):
        # Caminho absoluto do banco, baseado no local do arquivo
        self.db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), db_filename)
        self.conn = None  # Lazy connection
        self.cursor = None

    def conectar(self):
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.cursor = self.conn.cursor()
        return self.conn

    def salvar_dado(self, tabela, dados):
        self.conectar()
        self.cursor.execute(f"PRAGMA table_info({tabela})")
        colunas = [info[1] for info in self.cursor.fetchall()]
        if 'id' in colunas:
            colunas.remove('id')
        if len(colunas) != len(dados):
            raise ValueError(f"Número de colunas ({len(colunas)}) diferente dos dados ({len(dados)})")
        placeholders = ', '.join(['?'] * len(dados))
        sql = f"INSERT INTO {tabela} ({', '.join(colunas)}) VALUES ({placeholders})"
        self.cursor.execute(sql, tuple(dados))
        self.conn.commit()

    def atualizar_dado(self, tabela, campo, valor, condicao):
        self.conectar()
        sql = f"UPDATE {tabela} SET {campo} = ? WHERE {condicao}"
        self.cursor.execute(sql, (valor,))
        self.conn.commit()

    def deletar_dado(self, tabela, condicao):
        self.conectar()
        sql = f"DELETE FROM {tabela} WHERE {condicao}"
        self.cursor.execute(sql)
        self.conn.commit()

    def listar_dados(self, tabela):
        self.conectar()
        df = pd.read_sql_query(f"SELECT * FROM {tabela}", self.conn)
        return df

    def buscar_dado(self, tabela, condicao, valores=None):
        self.conectar()
        sql = f"SELECT * FROM {tabela} WHERE {condicao}"
        self.cursor.execute(sql, valores or ())
        resultado = self.cursor.fetchall()
        return resultado
    
    def atualizar_dados(self, tabela: str, dados: dict, condicao: str, params_condicao: list):
        self.conectar()
        campos = ", ".join([f"{chave} = ?" for chave in dados.keys()])
        valores = list(dados.values())
        sql = f"UPDATE {tabela} SET {campos} WHERE {condicao}"
        self.cursor.execute(sql, valores + params_condicao)
        self.conn.commit()
    
    def limpar_tabela(self, tabela):
        try:
            self.conectar()
            self.cursor.execute(f"DELETE FROM {tabela}")
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Erro ao limpar tabela '{tabela}': {e}")

    def fechar_conexao(self):
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None
