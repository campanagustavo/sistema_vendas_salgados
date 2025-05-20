from abc import ABC, abstractmethod

class Usuario(ABC):
    def __init__(self, nome: str, email: str, senha: str, id: int = None) -> None:
        self.id = id
        self.nome = nome
        self.email = email
        self.senha = senha
    
    @abstractmethod
    def get_tipo(self) -> str:
        # Método abstrato: cada subclasse deve retornar o tipo do usuário (ex: 'cliente', 'admin')
        pass

    @abstractmethod
    def tabela(self) -> str:
        # Método abstrato: cada subclasse deve retornar o nome da tabela no banco de dados
        pass
    
    def campos_validos(self) -> bool:
        # Verifica se nome, email e senha foram preenchidos
        return all([self.nome, self.email, self.senha])

    def validar_credenciais(self, email: str, senha: str) -> bool:
        # Confere se o email e senha recebidos conferem com os do objeto
        return self.email == email and self.senha == senha
    
    def dados_para_salvar(self) -> list:
        # Retorna os dados para salvar no banco de dados
        return [self.nome, self.email, self.senha]
    
    def dados_chave(self) -> tuple[str, tuple]:
        # Retorna a condição WHERE e seus parâmetros para buscar usuário único
        return "email = ?", (self.email,)
