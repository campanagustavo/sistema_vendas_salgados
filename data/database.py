import os
import sqlite3
import pandas as pd

class BaseDeDados:
    def __init__(self, db_filename: str = 'sistema_geral.db') -> None:
        # Caminho absoluto do banco de dados com base na localização do arquivo atual
        self.db_path: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), db_filename)
        self.conn: sqlite3.Connection | None = None  # Conexão será aberta sob demanda
        self.cursor: sqlite3.Cursor | None = None

    def conectar(self) -> sqlite3.Connection:
        """Estabelece a conexão com o banco de dados se ainda não estiver conectada."""
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.cursor = self.conn.cursor()
        return self.conn

    def salvar_dado(self, tabela: str, dados: list) -> int:
        """Insere um novo registro na tabela e retorna o ID gerado."""
        self.conectar()
        self.cursor.execute(f"PRAGMA table_info({tabela})")
        colunas = [info[1] for info in self.cursor.fetchall()]
        if 'id' in colunas:
            colunas.remove('id')  # Remove o campo 'id' se for autoincrementável
        if len(colunas) != len(dados):
            raise ValueError(f"Número de colunas ({len(colunas)}) diferente dos dados ({len(dados)})")
        placeholders = ', '.join(['?'] * len(dados))
        sql = f"INSERT INTO {tabela} ({', '.join(colunas)}) VALUES ({placeholders})"
        self.cursor.execute(sql, tuple(dados))
        self.conn.commit()
        return self.cursor.lastrowid

    def atualizar_dado(self, tabela: str, campo: str, valor: any, condicao: str) -> None:
        """Atualiza um único campo de um registro com base em uma condição."""
        self.conectar()
        sql = f"UPDATE {tabela} SET {campo} = ? WHERE {condicao}"
        self.cursor.execute(sql, (valor,))
        self.conn.commit()

    def deletar_dado(self, tabela: str, condicao: str, parametros: tuple = ()) -> None:
        """Deleta registros da tabela com base em uma condição."""
        self.conectar()
        sql = f"DELETE FROM {tabela} WHERE {condicao}"
        print(f"Executando SQL: {sql} | Parâmetros: {parametros}")
        self.cursor.execute(sql, parametros)
        self.conn.commit()
        print(f"{self.cursor.rowcount} linha(s) afetada(s)")

    def listar_dados(self, tabela: str) -> pd.DataFrame:
        """Retorna todos os dados da tabela como um DataFrame do Pandas."""
        self.conectar()
        df = pd.read_sql_query(f"SELECT * FROM {tabela}", self.conn)
        return df

    def buscar_dado(self, tabela: str, condicao: str, valores: tuple | None = None) -> list:
        """Busca registros com base em uma condição SQL personalizada."""
        self.conectar()
        sql = f"SELECT * FROM {tabela} WHERE {condicao}"
        self.cursor.execute(sql, valores or ())
        resultado = self.cursor.fetchall()
        return resultado

    def atualizar_dados(self, tabela: str, dados: dict, condicao: str, params_condicao: list) -> None:
        """Atualiza múltiplos campos de um registro com base em uma condição."""
        self.conectar()
        campos = ", ".join([f"{chave} = ?" for chave in dados.keys()])
        valores = list(dados.values())
        sql = f"UPDATE {tabela} SET {campos} WHERE {condicao}"
        self.cursor.execute(sql, valores + params_condicao)
        self.conn.commit()

    def limpar_tabela(self, tabela: str) -> None:
        """Remove todos os registros de uma tabela."""
        try:
            self.conectar()
            self.cursor.execute(f"DELETE FROM {tabela}")
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Erro ao limpar tabela '{tabela}': {e}")

    def fechar_conexao(self) -> None:
        """Fecha a conexão com o banco de dados, se estiver aberta."""
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None
