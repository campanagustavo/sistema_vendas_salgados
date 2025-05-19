# Classe Admin - herda de Usuario

from models.usuario import Usuario
import sqlite3
from data.database import BaseDeDados

class Admin(Usuario):
    TABELA_NOME = "admins"
    def __init__(self, nome: str, email: str, senha: str,admin_id: int = None) -> None:
        super().__init__(nome, email, senha, id_usuario=admin_id)

    def get_tipo(self) -> str:
        return "admin"
    
    @property
    def admin_id(self):
        return self.id_usuario

    @admin_id.setter
    def admin_id(self, value):
        self.id_usuario = value
        
    def salvar(self) -> bool:
        """
        Salva um NOVO admin no banco de dados.
        Retorna True se sucesso, False se erro.
        Tenta atualizar o self.admin_id (via self.id_usuario) se a inserção for bem-sucedida.
        """
        if self.admin_id is not None: # self.id_usuario também estaria preenchido
            print(f"Erro: Admin já possui ID ({self.admin_id}). Para atualizar, use um método de atualização.")
            return False

        db = BaseDeDados()
        try:
            # IMPORTANTE: A ordem dos dados na tupla deve ser a mesma ordem das colunas
            # na sua tabela 'admins', conforme retornado por "PRAGMA table_info(admins)"
            # (excluindo a coluna 'id' que é autoincremento).
            # Assumindo que sua tabela 'admins' tem (id, nome, email, senha)
            # Se tiver campos específicos de admin (ex: nivel_acesso), adicione-os aqui na ordem correta.
            dados_para_salvar = (self.nome, self.email, self.senha)
            
            db.salvar_dado(self.TABELA_NOME, dados_para_salvar)
            print(f"Admin '{self.nome}' salvo na tabela '{self.TABELA_NOME}'.")

            # Tentativa de recuperar o ID do admin recém-criado
            admin_salvo_df = db.listar_dados(self.TABELA_NOME)
            admin_encontrado = admin_salvo_df[admin_salvo_df['email'] == self.email]

            if not admin_encontrado.empty:
                self.id_usuario = admin_encontrado.iloc[0]['id'] # Assumindo coluna ID se chama 'id'
                print(f"ID do admin '{self.nome}' definido para: {self.admin_id}")
            else:
                print(f"Aviso: Não foi possível recuperar o ID do admin '{self.nome}' após salvar.")
            return True
        except ValueError as ve:
             print(f"Erro de valor ao salvar admin '{self.nome}': {ve}")
             return False
        except Exception as e:
            print(f"Erro ao salvar admin '{self.nome}': {e}")
            return False
        finally:
            db.fechar_conexao()

    @classmethod
    def criar(cls, nome: str, email: str, senha: str) -> 'Admin | None':
        """
        Método de fábrica: Cria uma instância de Admin e tenta salvá-la no banco.
        Retorna a instância do Admin (com ID, se possível) ou None se falhar.
        """
        novo_admin = cls(nome, email, senha)
        if novo_admin.salvar():
            return novo_admin
        return None

    # --- READ ---
    @classmethod
    def _converter_linha_df_para_admin(cls, linha_df: pd.Series) -> 'Admin':
        """Converte uma linha de DataFrame para um objeto Admin."""
        # Certifique-se que os nomes das colunas ('id', 'nome', 'email', 'senha')
        # no DataFrame correspondem aos da sua tabela 'admins'.
        # Se tiver campos específicos de Admin (ex: nivel_acesso), adicione-os aqui.
        return cls(
            admin_id=linha_df.get('id'), # Nome da coluna ID no seu DataFrame/tabela
            nome=linha_df.get('nome'),
            email=linha_df.get('email'),
            senha=linha_df.get('senha')
        )

    @classmethod
    def buscar_por_id(cls, id_admin: int) -> 'Admin | None':
        """Busca um admin pelo ID."""
        db = BaseDeDados()
        try:
            df_admins = db.listar_dados(cls.TABELA_NOME)
            admin_encontrado_df = df_admins[df_admins['id'] == id_admin] # Assumindo coluna ID se chama 'id'
            
            if not admin_encontrado_df.empty:
                return cls._converter_linha_df_para_admin(admin_encontrado_df.iloc[0])
            return None
        except Exception as e:
            print(f"Erro ao buscar admin por ID {id_admin}: {e}")
            return None
        finally:
            db.fechar_conexao()

    @classmethod
    def buscar_por_email(cls, email_admin: str) -> 'Admin | None':
        """Busca um admin pelo email."""
        db = BaseDeDados()
        try:
            df_admins = db.listar_dados(cls.TABELA_NOME)
            admin_encontrado_df = df_admins[df_admins['email'] == email_admin] # Assumindo coluna email se chama 'email'
            
            if not admin_encontrado_df.empty:
                return cls._converter_linha_df_para_admin(admin_encontrado_df.iloc[0])
            return None
        except Exception as e:
            print(f"Erro ao buscar admin por email '{email_admin}': {e}")
            return None
        finally:
            db.fechar_conexao()

    @classmethod
    def listar_todos(cls) -> list['Admin']:
        """Retorna uma lista com todos os admins."""
        db = BaseDeDados()
        lista_admins_obj = []
        try:
            df_todos_admins = db.listar_dados(cls.TABELA_NOME)
            for _, linha_df in df_todos_admins.iterrows():
                lista_admins_obj.append(cls._converter_linha_df_para_admin(linha_df))
            return lista_admins_obj
        except Exception as e:
            print(f"Erro ao listar todos os admins: {e}")
            return []
        finally:
            db.fechar_conexao()

    # --- UPDATE ---
    def atualizar_campo(self, nome_do_campo: str, novo_valor) -> bool:
        """
        Atualiza UM campo específico deste admin no banco.
        Ex: admin_obj.atualizar_campo('email', 'novo_admin@email.com')
        """
        if self.admin_id is None:
            print(f"Erro: Admin '{self.nome}' não tem ID, não pode ser atualizado.")
            return False

        # Se Admin tiver campos específicos além de nome, email, senha,
        # você pode adicionar validações ou lógica aqui.
        # Por enquanto, permite atualizar qualquer campo que BaseDeDados.atualizar_dado aceitar.

        db = BaseDeDados()
        try:
            condicao_where = f"id = {self.admin_id}" # Assumindo coluna ID se chama 'id'
            db.atualizar_dado(self.TABELA_NOME, nome_do_campo, novo_valor, condicao_where)
            
            if hasattr(self, nome_do_campo):
                setattr(self, nome_do_campo, novo_valor)
            print(f"Campo '{nome_do_campo}' do admin ID {self.admin_id} atualizado.")
            return True
        except Exception as e:
            print(f"Erro ao atualizar campo '{nome_do_campo}' do admin ID {self.admin_id}: {e}")
            return False
        finally:
            db.fechar_conexao()

    # --- DELETE ---
    def deletar(self) -> bool:
        """Deleta ESTE admin do banco de dados."""
        if self.admin_id is None:
            print(f"Erro: Admin '{self.nome}' não tem ID, não pode ser deletado.")
            return False
        
        return self.__class__.deletar_por_id(self.admin_id)

    @classmethod
    def deletar_por_id(cls, id_admin_para_deletar: int) -> bool:
        """Deleta um admin do banco de dados usando o ID."""
        db = BaseDeDados()
        try:
            condicao_where = f"id = {id_admin_para_deletar}" # Assumindo coluna ID se chama 'id'
            db.deletar_dado(cls.TABELA_NOME, condicao_where)
            print(f"Admin ID {id_admin_para_deletar} deletado da tabela '{cls.TABELA_NOME}'.")
            return True
        except Exception as e:
            print(f"Erro ao deletar admin ID {id_admin_para_deletar}: {e}")
            return False
        finally:
            db.fechar_conexao()
