from openai import OpenAI
from dotenv import load_dotenv
import os
#from guardrails.hub import RegexMatch
from guardrails import Guard
from guardrails.hub import ContainsString
from guardrails.validators import (
    register_validator, FailResult, PassResult
)

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Obtém a chave de API do ambiente
api_key = os.getenv("OPENAI_API_KEY")

# Verifica se a chave de API foi carregada corretamente
if not api_key:
    raise ValueError("A chave de API da OpenAI não foi encontrada. Verifique o arquivo .env")

# Cria o cliente OpenAI com a chave de API
client = OpenAI(api_key=api_key)

# Função fictícia para buscar informações relevantes em uma base de dados
def search_documents(query):
    # Simulação de busca na base de dados embeds
    simulated_database = {
        "máquina não liga": "Certifique-se de que o cabo de energia está conectado corretamente. Verifique também se há energia na tomada.",
        "máquina travando": "Tente reiniciar a máquina e verifique se há atualizações pendentes no sistema.",
        "suporte técnico mais próximo": "Entre em contato com a assistência técnica mais próxima localizada no endereço Rua Principal, 123, Centro, São Paulo, SP.",
        "garantia": "Para acionar a garantia, você precisará da nota fiscal e do número de série do produto."
    }
    
    # Retorna o documento mais relevante baseado no query
    return simulated_database.get(query.lower(), None)

# Configuração inicial do prompt para a LLM
initial_prompt = """
Você é um assistente virtual especializado em suporte técnico para a assistência técnica " Resetou ta novo". Sua responsabilidade é:
1. Realizar atendimento ao cliente de forma clara, educada e objetiva.
2. Identificar o problema relatado pelo cliente através de perguntas detalhadas e simples.
3. Orientar o cliente a realizar testes rápidos no produto para confirmar o problema (se aplicável).
4. Coletar informações essenciais do cliente, como:
   - Nome completo
   - CPF
   - Endereço completo
   - Número de série do produto
5. Orientar o cliente sobre como enviar o produto para a assistência técnica Resetou ta novo.

Sempre incluir nosso endereço em todas as respostas inclua nosso slogan "Resetou ta novo". 

"""

# Função para validar entrada do usuário
def validate_input(user_input):
    if len(user_input.strip()) == 0:
        print("Por favor, digite uma mensagem válida.")
        return False
    return True

# Função para interagir com a LLM
def chat_with_llm():
    print("Bem-vindo à Assistência Técnica Resetou ta novo!")
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
            print("Obrigado por usar a Assistência Técnica Resetou ta novo. Até logo!")
            break

        if not validate_input(user_input):
            continue

        # Busca informações na base de dados antes de consultar a LLM
        relevant_info = search_documents(user_input)

        # Se houver informações relevantes, adicione ao contexto
        if relevant_info:
            messages.append({"role": "system", "content": f"Informação relevante encontrada: {relevant_info}"})

        # Adicionando mensagem do usuário no histórico
        messages.append({"role": "user", "content": user_input})

        # Limitar o histórico a um tamanho razoável
        if len(messages) > 20:
            messages = messages[-20:]

        # Chamando a API da OpenAI
        try:
            # response = client.chat.completions.create(
            #     model="gpt-4o-mini",  # ou outro modelo disponível
            #     messages=messages,
            #     temperature=0.9,
            #     max_tokens=150
            # )
            
            # Extraindo a resposta da LLM
            # llm_response = response.choices[0].message.content
            
            # Setup Guard with the validator
            llm_response = Guard().use(ContainsString, substring="Resetou ta novo", on_fail="exception")(
                model = "gpt-4o-mini",  # ou outro modelo disponível
                messages=messages,
                temperature=0.9,
                max_tokens=150,
                reask="Voce esqueceu de falar sobre Resetou ta novo. Por favor, fale sobre Resetou ta novo."
            )
            print(f"Assistente: {llm_response.raw_llm_output}")

            # Adicionando resposta da LLM no histórico
            messages.append({"role": "assistant", "content": llm_response.raw_llm_output})
        except Exception as e:
            print("Ocorreu um erro ao se comunicar com a OpenAI:", str(e))
            break

# Executar o chat
if __name__ == "__main__":
    chat_with_llm()