from data.database import BaseDeDados
from models.bolo import Bolo
from models.salgado import Salgado
from models.alimento import Alimento

class AlimentoControle:
    def __init__(self):
        self.db = BaseDeDados()

    def adicionar_alimento(self, alimento: Alimento) -> str | None:
        # Obtém condição para busca no banco, para evitar duplicidade
        condicao, valores = alimento.dados_chave
        resultados = self.db.buscar_dado(alimento.tabela, condicao, valores)

        # Se já existir alimento com mesma chave, retorna aviso
        if resultados:
            return f"{alimento.get_categoria} já adicionado."

        # Verifica se os campos obrigatórios estão preenchidos
        if not alimento.campos_validos:
            return "Preencha todos os campos obrigatórios!"

        try:
            # Tenta salvar o novo alimento no banco
            self.db.salvar_dado(alimento.tabela, alimento.dados_para_salvar)
            return None  # Sucesso
        except Exception as e:
            # Retorna mensagem de erro em caso de exceção
            return f"Erro ao salvar no banco: {e}"

    def listar_alimentos(self, classe: type, tabela: str) -> list[Alimento]:
        # Lista todos os alimentos de uma determinada tabela e converte em objetos
        resultados = self.db.listar_dados(tabela)
        alimentos = []
        for resultado in resultados.values.tolist():
            # Extrai os campos do resultado
            id_ = resultado[0]
            sabor = resultado[1]
            tamanho = resultado[2]
            preco = resultado[3]
            descricao = resultado[4]
            foto = resultado[5]
            # Cria o objeto alimento da classe específica e adiciona à lista
            alimentos.append(classe(sabor, tamanho, preco, descricao, foto, id_))
        return alimentos

    def excluir_alimento(self, tabela: str, condicao: str, parametros: tuple) -> None:
        # Remove um alimento da tabela com base na condição e parâmetros
        print(f"Excluindo de {tabela} onde {condicao} com {parametros}")
        self.db.deletar_dado(tabela, condicao, parametros)

    def editar_alimento(self, tabela: str, alimento_antigo, alimento_novo, campos: list) -> str | None:
        # Edita um alimento existente na tabela, atualizando os campos indicados
        if not alimento_novo.campos_validos:
            return "Por favor, preencha todos os campos obrigatórios!"

        # Condição para localizar o alimento antigo no banco pelo ID
        condicao = "id = ?"
        params_condicao = [alimento_antigo.id]

        # Cria um dicionário com os campos a serem atualizados e seus novos valores
        dados = {campo: getattr(alimento_novo, campo) for campo in campos}

        try:
            # Atualiza os dados no banco
            self.db.atualizar_dados(tabela, dados, condicao, params_condicao)
            return None  # Sucesso
        except Exception as e:
            # Em caso de erro, imprime e retorna mensagem
            print(f"Exceção ao atualizar {tabela[:-1]}: {e}")
            return f"Erro ao atualizar {tabela[:-1]}: {e}"

    def obter_alimento_por_id(self, classe: type, tabela: str, alimento_id: int) -> Alimento | None:
        # Busca um alimento específico pelo ID dentro da lista de alimentos da tabela
        alimentos = self.listar_alimentos(classe, tabela)
        for alimento in alimentos:
            if alimento.id == alimento_id:
                return alimento
        return None  
