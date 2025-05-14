import sqlite3
import pandas as pd

# Conectar ao banco (mantendo a conexão aberta durante o tempo de uso)
def conectar():
    return sqlite3.connect('sistema_geral.db', check_same_thread=False)

def salvar_dado(tabela, dados):
    # Criar a conexão
    conn = conectar()
    cursor = conn.cursor()

    # Obter as colunas da tabela
    cursor.execute(f"PRAGMA table_info({tabela})")
    colunas = [info[1] for info in cursor.fetchall()]

    # Verificar se o 'id' está nas colunas e removê-lo, se necessário
    if 'id' in colunas:
        colunas.remove('id')  # Remover a coluna 'id' para que o banco insira automaticamente

    # Verificar se o número de colunas e dados é igual
    if len(colunas) != len(dados):
        raise ValueError(f"O número de colunas ({len(colunas)}) não corresponde ao número de dados ({len(dados)}).")

    # Gerar a consulta SQL para inserção
    placeholders = ', '.join(['?'] * len(dados))
    sql = f"INSERT INTO {tabela} ({', '.join(colunas)}) VALUES ({placeholders})"
    
    # Depuração: Imprimir a consulta SQL antes de executar
    print(f"SQL gerado: {sql}")
    print(f"Valores a serem inseridos: {dados}")

    # Inserir os dados
    cursor.execute(sql, tuple(dados))
    conn.commit()

    print(f"Registro salvo em '{tabela}': {dict(zip(colunas, dados))}")

    # Fechar conexão
    conn.close()


def listar_dados(tabela):
    # Criar a conexão
    conn = conectar()
    df = pd.read_sql_query(f"SELECT * FROM {tabela}", conn)

    print(f"\nDados da tabela '{tabela}':")
    print(df)

    # Fechar conexão
    conn.close()

def atualizar_dado(tabela, campo, valor, condicao):
    # Criar a conexão
    conn = conectar()
    cursor = conn.cursor()

    sql = f"UPDATE {tabela} SET {campo} = ? WHERE {condicao}"
    cursor.execute(sql, (valor,))
    conn.commit()

    print(f"Atualizado '{campo}' em '{tabela}' para '{valor}' onde {condicao}")

    # Fechar conexão
    conn.close()

def deletar_dado(tabela, condicao):
    # Criar a conexão
    conn = conectar()
    cursor = conn.cursor()

    # Gerar a consulta SQL para deletar
    sql = f"DELETE FROM {tabela} WHERE {condicao}"

    # Executar a exclusão
    cursor.execute(sql)
    conn.commit()

    print(f"Registro(s) deletado(s) de '{tabela}' onde {condicao}")

    # Fechar conexão
    conn.close()

def limpar_tabela_clientes():
    try:
        # Conectar ao banco de dados
        conn = sqlite3.connect('sistema_geral.db')
        cursor = conn.cursor()

        # Apagar todos os registros da tabela 'clientes'
        cursor.execute("DELETE FROM clientes")

        # Confirmar a exclusão no banco de dados
        conn.commit()

        print("Tabela 'clientes' limpa com sucesso!")

    except sqlite3.Error as e:
        print(f"Erro ao limpar tabela 'clientes': {e}")

    finally:
        # Fechar a conexão com o banco de dados
        conn.close()

