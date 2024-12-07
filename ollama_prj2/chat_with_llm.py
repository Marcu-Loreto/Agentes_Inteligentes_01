import ollama

# Função fictícia para buscar informações relevantes em uma base de dados
def search_documents(query):
    # Simulação de busca na base de dados
    simulated_database = {
        "máquina não liga": "Certifique-se de que o cabo de energia está conectado corretamente. Verifique também se há energia na tomada.",
        "máquina travando": "Tente reiniciar a máquina e verifique se há atualizações pendentes no sistema.",
        "suporte técnico mais próximo": "Entre em contato com a assistência técnica mais próxima localizada no endereço Rua Principal, 123, Centro, São Paulo, SP.",
        "garantia": "Para acionar a garantia, você precisará da nota fiscal e do número de série do produto."
    }minha maquina nao funciona
    
    # Retorna o documento mais relevante baseado no query
    return simulated_database.get(query.lower(), None)

# Configuração inicial do prompt para a LLM
initial_prompt = """
Você é um assistente virtual especializado em suporte técnico para uma assistência técnica. Sua responsabilidade é:
1. Realizar atendimento ao cliente de forma clara, educada e objetiva.
2. Identificar o problema relatado pelo cliente através de perguntas detalhadas e simples.
3. Orientar o cliente a realizar testes rápidos no produto para confirmar o problema (se aplicável).
4. Coletar informações essenciais do cliente, como:
   - Nome completo
   - CPF
   - Endereço completo
   - Número de série do produto
5. Orientar o cliente sobre como enviar o produto para a assistência técnica mais próxima, fornecendo informações detalhadas, como:
   - Endereço da assistência técnica
   - Instruções para envio ou entrega do produto
   - Documentos necessários (nota fiscal, garantia, etc.).

Converse em um tom amigável, mantenha respostas curtas e diretas, e peça confirmação ao cliente antes de prosseguir para as próximas etapas. Caso o cliente precise de informações adicionais, responda de forma clara e paciente. Você está sempre pronto para ajudar!

Exemplo:
Usuário: Minha máquina não liga.
Assistente: Certifique-se de que o cabo de energia está conectado corretamente. Verifique também se há energia na tomada. O problema persiste?
"""

# Função para validar entrada do usuário
def validate_input(user_input):
    if len(user_input.strip()) == 0:
        print("Por favor, digite uma mensagem válida.")
        return False
    return True

# Função para interagir com a LLM
def chat_with_llm():
    print("Bem-vindo à Assistência Técnica Virtual!")
    print("Você pode começar a digitar suas dúvidas ou problemas. Digite 'sair' para encerrar o atendimento.\n")

    # Inicializando o histórico de mensagens
    messages = [
        {
            "role": "system",
            "content": initial_prompt
        }
    ]

    while True:
        # Entrada do usuário
        user_input = input("Você: ")
        if user_input.lower() == "sair":
            print("Obrigado por usar a Assistência Técnica Virtual. Até logo!")
            break

        if not validate_input(user_input):
            continue

        # Busca informações na base de dados antes de consultar a LLM
        relevant_info = search_documents(user_input)

        # Se houver informações relevantes, exiba ao usuário e adicione ao contexto
        if relevant_info:
            print(f"Assistente (base de dados): {relevant_info}")
            messages.append({"role": "system", "content": f"Informação relevante encontrada: {relevant_info}"})

        # Adicionando mensagem do usuário no histórico
        messages.append({"role": "user", "content": user_input})

        # Limitar o histórico a um tamanho razoável
        if len(messages) > 20:  # Ajuste conforme necessário
            messages = messages[-20:]

        # Chamando a API da LLM
        try:
            response = ollama.chat(
                model="llama3.2",
                messages=messages
            )
            # Extraindo a resposta da LLM
            llm_response = response.get("content", "Desculpe, não consegui entender sua solicitação.")
            print(f"Assistente: {llm_response}")

            # Adicionando resposta da LLM no histórico
            messages.append({"role": "assistant", "content": llm_response})
        except Exception as e:
            print("Ocorreu um erro ao se comunicar com a LLM:", str(e))
            break

# Executar o chat
if __name__ == "__main__":
    chat_with_llm()
