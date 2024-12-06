from guardrails.hub import RegexMatch
from guardrails import Guard

guard = Guard().use(
    RegexMatch(regex=r"^([A-Z][a-z]*|de|da|do)(\s([A-Z][a-z]*|de|da|do))*$")
)

try:
    result = guard.validate("Joao da Silva")  # Passa na validação
    print("Validação bem-sucedida:", result)
except:
    print("Deu pau")