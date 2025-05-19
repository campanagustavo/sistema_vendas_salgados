from models.cliente import Cliente # Certifique-se que este caminho de importação está correto

class CadastroControle:
    def cadastrar_cliente(self, novo_cliente_obj: Cliente) -> str | None:
        """
        Tenta cadastrar um novo cliente no sistema.
        Recebe um objeto Cliente já instanciado com nome, email e senha pela View.
        Retorna uma string contendo uma mensagem de erro se a operação falhar,
        ou None se o cadastro for bem-sucedido.
        """

        # 1. Validações básicas (podem ser mais detalhadas se necessário)
        if not novo_cliente_obj.nome or not novo_cliente_obj.email or not novo_cliente_obj.senha:
            return "Todos os campos (Nome, Email, Senha) são obrigatórios."
        
        # Adicionar aqui outras validações, como formato de email, força da senha, etc., se desejar.
        # Exemplo simples de validação de email (pode ser mais robusto):
        if "@" not in novo_cliente_obj.email or "." not in novo_cliente_obj.email.split('@')[-1]:
            return "Formato de email inválido."

        # 2. Verificar se o cliente (ex: por email) já existe
        # Usamos o método de classe Cliente.buscar_por_email()
        cliente_existente = Cliente.buscar_por_email(novo_cliente_obj.email)
        if cliente_existente:
            return f"O email '{novo_cliente_obj.email}' já está cadastrado no sistema."

        # 3. Se tudo estiver OK, tentar salvar o novo cliente
        # O método salvar_novo() da classe Cliente já contém a lógica
        # para interagir com BaseDeDados e tentar definir o ID do cliente.
        if novo_cliente_obj.salvar(): # Este é o método que definimos no modelo Cliente
            # Cadastro realizado com sucesso!
            # O objeto novo_cliente_obj pode ter sido atualizado com o cliente_id dentro do salvar_novo()
            if novo_cliente_obj.cliente_id: # ou novo_cliente_obj.id_usuario
                print(f"[Controller] Cliente '{novo_cliente_obj.nome}' cadastrado com ID: {novo_cliente_obj.cliente_id}.")
            else:
                # Isso pode acontecer se a busca por email pós-salvamento falhar em obter o ID,
                # mas o dado ainda assim foi inserido no banco.
                print(f"[Controller] Cliente '{novo_cliente_obj.nome}' cadastrado, mas ID não foi automaticamente populado na instância.")
            
            return None # Sucesso, nenhuma mensagem de erro
        else:
            # O método salvar_novo() na classe Cliente já deve ter impresso um erro mais específico no console.
            # O controller pode retornar uma mensagem mais genérica para a view.
            return "Ocorreu um erro interno ao tentar realizar o cadastro. Por favor, tente novamente."