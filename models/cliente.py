# Classe Cliente - herda de Usuario
from data.database import BaseDeDados
import sqlite3
from models.usuario import Usuario
import pandas as pd

class Cliente(Usuario):
    TABELA_NOME = "clientes"
    def __init__(self, nome: str, email: str, senha: str, cliente_id: int = None) -> None:
        super().__init__(nome, email, senha)
        self.cliente_id = cliente_id

    def get_tipo(self) -> str:
        return "cliente"
    
    @property # Permite acessar self.usuario_id como self.cliente_id
    def cliente_id(self):
        return self.id_usuario
    
    @cliente_id.setter # Permite definir self.cliente_id e atualizar self.usuario_id
    def cliente_id(self, value):
        self.id_usuario = value
    
    def salvar(self) -> bool:
        """
        Salva um NOVO cliente no banco de dados.
        Retorna True se sucesso, False se erro.
        Tenta atualizar o self.cliente_id (via self.id_usuario) se a inserção for bem-sucedida.
        """
        if self.cliente_id is not None: # self.id_usuario também estaria preenchido
            print(f"Erro: Cliente já possui ID ({self.cliente_id}). Para atualizar, use um método de atualização.")
            return False

        db = BaseDeDados() # Cria uma instância da sua classe de banco de dados
        try:
            # IMPORTANTE: A ordem dos dados na tupla deve ser a mesma ordem das colunas
            # na sua tabela 'clientes', conforme retornado por "PRAGMA table_info(clientes)"
            # (excluindo a coluna 'id' que é autoincremento).
            # Exemplo: se sua tabela 'clientes' tem (id, nome, email, senha)
            dados_para_salvar = (self.nome, self.email, self.senha)
            
            db.salvar_dado(self.TABELA_NOME, dados_para_salvar)
            print(f"Cliente '{self.nome}' salvo na tabela '{self.TABELA_NOME}'.")

            # Tentativa de recuperar o ID do cliente recém-criado
            # Sua BaseDeDados.salvar_dado não retorna o ID, então buscamos pelo email (se for único)
            cliente_salvo_df = db.listar_dados(self.TABELA_NOME) # Pega todos os clientes
            cliente_encontrado = cliente_salvo_df[cliente_salvo_df['email'] == self.email]

            if not cliente_encontrado.empty:
                # Assumindo que a coluna de ID no seu banco/DataFrame se chama 'id'
                self.id_usuario = cliente_encontrado.iloc[0]['id']
                print(f"ID do cliente '{self.nome}' definido para: {self.cliente_id}")
            else:
                print(f"Aviso: Não foi possível recuperar o ID do cliente '{self.nome}' após salvar.")
            return True
        except ValueError as ve: # Erro específico do seu BaseDeDados.salvar_dado
             print(f"Erro de valor ao salvar cliente '{self.nome}': {ve}")
             return False
        except Exception as e:
            print(f"Erro ao salvar cliente '{self.nome}': {e}")
            return False
        finally:
            db.fechar_conexao()
            
    @classmethod
    def criar(cls, nome: str, email: str, senha: str) -> 'Cliente | None':
        """
        Método de fábrica: Cria uma instância de Cliente e tenta salvá-la no banco.
        Retorna a instância do Cliente (com ID, se possível) ou None se falhar.
        """
        novo_cliente = cls(nome, email, senha)
        if novo_cliente.salvar():
            return novo_cliente
        return None
    
    @classmethod
    def _converter_linha_df_para_cliente(cls, linha_df: pd.Series) -> 'Cliente':
        """Converte uma linha de DataFrame para um objeto Cliente."""
        # Certifique-se que os nomes das colunas ('id', 'nome', 'email', 'senha')
        # no DataFrame correspondem aos da sua tabela.
        return cls(
            cliente_id=linha_df.get('id'), # Nome da coluna ID no seu DataFrame/tabela
            nome=linha_df.get('nome'),
            email=linha_df.get('email'),
            senha=linha_df.get('senha') # Lembre-se da segurança de senhas!
        )
        
    @classmethod
    def buscar_por_id(cls, id_cliente: int) -> 'Cliente | None':
        """Busca um cliente pelo ID."""
        db = BaseDeDados()
        try:
            df_clientes = db.listar_dados(cls.TABELA_NOME)
            # A coluna de ID no DataFrame deve se chamar 'id' (ou o nome que você usa)
            cliente_encontrado_df = df_clientes[df_clientes['id'] == id_cliente]
            
            if not cliente_encontrado_df.empty:
                return cls._converter_linha_df_para_cliente(cliente_encontrado_df.iloc[0])
            return None
        except Exception as e:
            print(f"Erro ao buscar cliente por ID {id_cliente}: {e}")
            return None
        finally:
            db.fechar_conexao()
            
    @classmethod
    def buscar_por_email(cls, email_cliente: str) -> 'Cliente | None': # 'cls' é o primeiro argumento para classmethods
        """Busca um cliente pelo email."""
        db = BaseDeDados() # Instancia BaseDeDados aqui dentro ou passe como argumento se preferir
        try:
            df_clientes = db.listar_dados(cls.TABELA_NOME) # Usa cls.TABELA_NOME
            # A coluna de email no DataFrame deve se chamar 'email'
            if 'email' not in df_clientes.columns:
                print(f"Aviso: Coluna 'email' não encontrada na tabela '{cls.TABELA_NOME}'. Verifique o nome da coluna.")
                return None
            
            cliente_encontrado_df = df_clientes[df_clientes['email'] == email_cliente]
            
            if not cliente_encontrado_df.empty:
                # Usa cls._converter_linha_df_para_cliente para criar a instância correta
                return cls._converter_linha_df_para_cliente(cliente_encontrado_df.iloc[0])
            return None
        except Exception as e:
            print(f"Erro ao buscar cliente por email '{email_cliente}': {e}")
            return None
        finally:
            db.fechar_conexao()
    @classmethod
    def listar_todos(cls) -> list['Cliente']:
        """Retorna uma lista com todos os clientes."""
        db = BaseDeDados()
        lista_clientes_obj = []
        try:
            df_todos_clientes = db.listar_dados(cls.TABELA_NOME)
            for _, linha_df in df_todos_clientes.iterrows(): # _ ignora o índice da linha
                lista_clientes_obj.append(cls._converter_linha_df_para_cliente(linha_df))
            return lista_clientes_obj
        except Exception as e:
            print(f"Erro ao listar todos os clientes: {e}")
            return []
        finally:
            db.fechar_conexao()
            
    def atualizar_campo(self, nome_do_campo: str, novo_valor) -> bool:
        """
        Atualiza UM campo específico deste cliente no banco.
        Ex: cliente_obj.atualizar_campo('email', 'novo@email.com')
        """
        if self.cliente_id is None: # Ou self.id_usuario
            print(f"Erro: Cliente '{self.nome}' não tem ID, não pode ser atualizado.")
            return False

        db = BaseDeDados()
        try:
            # A condição para o WHERE. Assumindo que sua coluna ID se chama 'id'.
            condicao_where = f"id = {self.cliente_id}"
            db.atualizar_dado(self.TABELA_NOME, nome_do_campo, novo_valor, condicao_where)
            
            # Atualiza também o atributo na instância do objeto, se ele existir
            if hasattr(self, nome_do_campo):
                setattr(self, nome_do_campo, novo_valor)
            print(f"Campo '{nome_do_campo}' do cliente ID {self.cliente_id} atualizado.")
            return True
        except Exception as e:
            print(f"Erro ao atualizar campo '{nome_do_campo}' do cliente ID {self.cliente_id}: {e}")
            return False
        finally:
            db.fechar_conexao()
            
    def deletar(self) -> bool:
        """Deleta ESTE cliente do banco de dados."""
        if self.cliente_id is None: # Ou self.id_usuario
            print(f"Erro: Cliente '{self.nome}' não tem ID, não pode ser deletado.")
            return False
        
        return self.__class__.deletar_por_id(self.cliente_id) # Chama o método de classe
    
    @classmethod
    def deletar_por_id(cls, id_cliente_para_deletar: int) -> bool:
        """Deleta um cliente do banco de dados usando o ID."""
        db = BaseDeDados()
        try:
            # A condição para o WHERE. Assumindo que sua coluna ID se chama 'id'.
            condicao_where = f"id = {id_cliente_para_deletar}"
            db.deletar_dado(cls.TABELA_NOME, condicao_where)
            print(f"Cliente ID {id_cliente_para_deletar} deletado da tabela '{cls.TABELA_NOME}'.")
            return True
        except Exception as e:
            print(f"Erro ao deletar cliente ID {id_cliente_para_deletar}: {e}")
            return False
        finally:
            db.fechar_conexao()