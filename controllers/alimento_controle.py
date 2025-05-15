# Lógica de cadastro, edição, exclusão e listagem de alimentos

from data.database import BaseDeDados
from models.bolo import Bolo
from models.salgado import Salgado

class AlimentoControle:
    def __init__(self):
        self.db = BaseDeDados()

    def adicionar_bolo(self, bolo):
        condicao = "sabor = ? AND tamanho = ? AND preco = ?"
        valores = (bolo.sabor, bolo.tamanho, bolo.preco)
        resultados = self.db.buscar_dado("bolos", condicao, valores)

        if resultados:
            return "Bolo já adicionado."

        if not bolo.sabor or not bolo.tamanho or not bolo.preco:
            return "Preencha todos os campos obrigatórios!"

        try:
            self.db.salvar_dado("bolos", [bolo.sabor, bolo.tamanho, bolo.preco, bolo.descricao, bolo.foto])
            return None
        except Exception as e:
            return f"Erro ao salvar no banco: {e}"

    def adicionar_salgado(self, salgado):
        condicao = "tipo = ? AND recheio = ? AND preco = ?"
        valores = (salgado.tipo, salgado.recheio, salgado.preco)
        resultados = self.db.buscar_dado("salgados", condicao, valores)

        if resultados:
            return "Salgado já adicionado."

        if not salgado.tipo or not salgado.recheio or not salgado.preco:
            return "Preencha todos os campos obrigatórios!"

        try:
            self.db.salvar_dado("salgados", [salgado.tipo, salgado.recheio, salgado.preco, salgado.descricao, salgado.foto])
            return None
        except Exception as e:
            return f"Erro ao salvar no banco: {e}"

    def listar_bolos(self):
        resultados = self.db.listar_dados("bolos")
        return [Bolo(*resultado) for resultado in resultados.values.tolist()]

    def listar_salgados(self):
        resultados = self.db.listar_dados("salgados")
        return [Salgado(*resultado) for resultado in resultados.values.tolist()]

    def excluir_bolo(self, bolo):
        condicao = f"sabor = '{bolo.sabor}' AND tamanho = '{bolo.tamanho}' AND preco = '{bolo.preco}'"
        self.db.deletar_dado("bolos", condicao)

    def excluir_salgado(self, salgado):
        condicao = f"tipo = '{salgado.tipo}' AND recheio = '{salgado.recheio}' AND preco = '{salgado.preco}'"
        self.db.deletar_dado("salgados", condicao)

    def editar_bolo(self, bolo_antigo, bolo_novo):
        try:
            # Atualiza cada campo individualmente
            if bolo_antigo.sabor != bolo_novo.sabor:
                self.db.atualizar_dado("bolos", "sabor", bolo_novo.sabor, f"sabor = '{bolo_antigo.sabor}'")
            if bolo_antigo.tamanho != bolo_novo.tamanho:
                self.db.atualizar_dado("bolos", "tamanho", bolo_novo.tamanho, f"tamanho = '{bolo_antigo.tamanho}'")
            if bolo_antigo.preco != bolo_novo.preco:
                self.db.atualizar_dado("bolos", "preco", bolo_novo.preco, f"preco = '{bolo_antigo.preco}'")
            if bolo_antigo.descricao != bolo_novo.descricao:
                self.db.atualizar_dado("bolos", "descricao", bolo_novo.descricao, f"descricao = '{bolo_antigo.descricao}'")
            if bolo_antigo.foto != bolo_novo.foto:
                self.db.atualizar_dado("bolos", "foto", bolo_novo.foto, f"foto = '{bolo_antigo.foto}'")
            return None
        except Exception as e:
            return f"Erro ao atualizar bolo: {e}"

    def editar_salgado(self, salgado_antigo, salgado_novo):
        try:
            # Atualiza cada campo individualmente
            if salgado_antigo.tipo != salgado_novo.tipo:
                self.db.atualizar_dado("salgados", "tipo", salgado_novo.tipo, f"tipo = '{salgado_antigo.tipo}'")
            if salgado_antigo.recheio != salgado_novo.recheio:
                self.db.atualizar_dado("salgados", "recheio", salgado_novo.recheio, f"recheio = '{salgado_antigo.recheio}'")
            if salgado_antigo.preco != salgado_novo.preco:
                self.db.atualizar_dado("salgados", "preco", salgado_novo.preco, f"preco = '{salgado_antigo.preco}'")
            if salgado_antigo.descricao != salgado_novo.descricao:
                self.db.atualizar_dado("salgados", "descricao", salgado_novo.descricao, f"descricao = '{salgado_antigo.descricao}'")
            if salgado_antigo.foto != salgado_novo.foto:
                self.db.atualizar_dado("salgados", "foto", salgado_novo.foto, f"foto = '{salgado_antigo.foto}'")
            return None
        except Exception as e:
            return f"Erro ao atualizar salgado: {e}"