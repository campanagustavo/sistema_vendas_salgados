import sqlite3
conexao = sqlite3.connect('banco_dados.db')
cursor = conexao.cursor()
conexao.close

## adicionar criação das tabelas, criação do banco e das tabelas devem ser feitas uma única vez
