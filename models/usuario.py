from abc import ABC, abstractmethod
import hashlib

class Usuario(ABC):
    def __init__(self, nome: str, email: str, senha: str, id: int = None) -> None:
        self.id = id
        self._nome = nome
        self._email = email
        self.__senha = self._hash_senha(senha)
    
    @property
    def nome(self) -> str:
        return self._nome

    @nome.setter
    def nome(self, novo_nome: str) -> None:
        self._nome = novo_nome

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, novo_email: str) -> None:
        self._email = novo_email

    @property
    def senha(self) -> str:
        raise AttributeError("Senha não pode ser acessada diretamente.")

    @senha.setter
    def senha(self, nova_senha: str) -> None:
        self.__senha = self._hash_senha(nova_senha)

    def _hash_senha(self, senha: str) -> str:
        return hashlib.sha256(senha.encode()).hexdigest()

    @abstractmethod
    def tipo(self) -> str:
        pass

    @abstractmethod
    def tabela(self) -> str:
        pass

    def campos_validos(self) -> bool:
        return all([self._nome, self._email, self.__senha])

    def validar_credenciais(self, email: str, senha: str) -> bool:
        return self._email == email and self.__senha == self._hash_senha(senha)

    def dados_para_salvar(self) -> list:
        return [self._nome, self._email, self.__senha]

    def dados_chave(self) -> tuple[str, tuple]:
        return "email = ?", (self._email,)
