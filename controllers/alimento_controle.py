# Lógica de cadastro, edição, exclusão e listagem de alimentos

from data.database import salvar_dado, buscar_dado, deletar_dado, atualizar_dado, _update_todos_os_campos, atualizar_dados
from models.bolo import Bolo
from models.salgado import Salgado

class AlimentoControle:
    def adicionar_bolo(self, bolo):
        # Verificar se o bolo já existe na base de dados
        condicao = "sabor = ? AND tamanho = ? AND preco = ?"
        valores = (bolo.sabor, bolo.tamanho, bolo.preco)
        resultados = buscar_dado("bolos", condicao, valores)

        # Se o bolo já existe, retorna a mensagem de erro
        if resultados:
            return "Bolo já adicionado."

        # Validação simples
        if not bolo.sabor or not bolo.tamanho or not bolo.preco:
            return "Preencha todos os campos obrigatórios!"

        try:
            salvar_dado("bolos", [bolo.sabor, bolo.tamanho, bolo.preco, bolo.descricao, bolo.foto])
            return None  # Sucesso
        except Exception as e:
            return f"Erro ao salvar no banco: {e}"



    def adicionar_salgado(self, salgado):
        # Verificar se o salgado já existe na base de dados
        condicao = f"tipo = '{salgado.tipo}' AND recheio = '{salgado.recheio}' AND preco = {salgado.preco}"
        resultados = buscar_dado("salgados", condicao)

        # Se o salgado já existe, retorna a mensagem de erro
        if resultados:
            return "Salgado já adicionado."

        # Validação simples
        if not salgado.tipo or not salgado.recheio or not salgado.preco:
            return "Preencha todos os campos obrigatórios!"

        try:
            salvar_dado("salgados", [salgado.tipo, salgado.recheio, salgado.preco, salgado.descricao, salgado.foto])
            return None  # Sucesso
        except Exception as e:
            return f"Erro ao salvar no banco: {e}"

        
    def listar_bolos(self):
        # Buscar os dados dos bolos
        resultados = buscar_dado("bolos", "1=1")  # Condição '1=1' para pegar todos os bolos

        # Verificar se não há resultados
        if not resultados:
            return []

        # Criar uma lista de bolos a partir dos resultados
        bolos = []
        for resultado in resultados:
            id, sabor, tamanho, preco, descricao, foto = resultado
            bolo = Bolo(sabor, tamanho, preco, descricao, foto)
            bolos.append(bolo)

        return bolos


    def listar_salgados(self):
        # Buscar os dados dos salgados
        resultados = buscar_dado("salgados", "1=1")  # Condição '1=1' para pegar todos os salgados

        # Verificar se não há resultados
        if not resultados:
            return []

        # Criar uma lista de salgados a partir dos resultados
        salgados = []
        for resultado in resultados:
            id, tipo, recheio, preco, descricao, foto = resultado
            salgado = Salgado(tipo, recheio, preco, descricao, foto)
            salgados.append(salgado)

        return salgados

    def excluir_bolo(self, bolo: Bolo) -> None:
        condicao = (
            f"sabor = '{bolo.sabor}' AND "
            f"tamanho = '{bolo.tamanho}' AND "
            f"preco = '{bolo.preco}'"
        )
        deletar_dado("bolos", condicao)


    def excluir_salgado(self, salgado: Salgado) -> None:
        condicao = (
            f"tipo = '{salgado.tipo}' AND "
            f"recheio = '{salgado.recheio}' AND "
            f"preco = '{salgado.preco}'"
        )
        deletar_dado("salgados", condicao)


    def editar_bolo(self, bolo_antigo, bolo_novo):
        condicao = "sabor = ? AND tamanho = ? AND preco = ? AND descricao = ? AND foto = ?"
        params_condicao = [
            bolo_antigo.sabor,
            bolo_antigo.tamanho,
            bolo_antigo.preco,
            bolo_antigo.descricao,
            bolo_antigo.foto,
        ]
        dados = {
            "sabor": bolo_novo.sabor,
            "tamanho": bolo_novo.tamanho,
            "preco": bolo_novo.preco,
            "descricao": bolo_novo.descricao,
            "foto": bolo_novo.foto,
        }

        try:
            atualizar_dados("bolos", dados, condicao, params_condicao)
            return None
        except Exception as e:
            return f"Erro ao atualizar bolo: {e}"



    def editar_salgado(self, salgado_antigo, salgado_novo):
        condicao = "tipo = ? AND recheio = ? AND preco = ? AND descricao = ? AND foto = ?"
        params_condicao = [
            salgado_antigo.tipo,
            salgado_antigo.recheio,
            salgado_antigo.preco,
            salgado_antigo.descricao,
            salgado_antigo.foto,
        ]
        dados = {
            "tipo": salgado_novo.tipo,
            "recheio": salgado_novo.recheio,
            "preco": salgado_novo.preco,
            "descricao": salgado_novo.descricao,
            "foto": salgado_novo.foto,
        }

        try:
            atualizar_dados("salgados", dados, condicao, params_condicao)
            return None
        except Exception as e:
            return f"Erro ao atualizar salgado: {e}"
