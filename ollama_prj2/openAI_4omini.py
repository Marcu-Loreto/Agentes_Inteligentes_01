from openai import OpenAI
from dotenv import load_dotenv
import os

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Obtém a chave de API do ambiente
api_key = os.getenv("OPENAI_API_KEY")

# Verifica se a chave de API foi carregada corretamente
if not api_key:
    raise ValueError("A chave de API da OpenAI não foi encontrada. Verifique o arquivo .env")

# Cria o cliente OpenAI com a chave de API
client = OpenAI(api_key=api_key)

# Resto do seu código aqui
completion = client.chat.completions.create(
    model="gpt-4o-mini",  # ou outro modelo disponível
    messages=[
        {"role": "user", "content": "qual o maior oceano do mundo?"}
    ]
)

print(completion.choices[0].message.content)