
# Instale as bibliotecas necessárias antes de executar:
# pip install guardrails-ai openai
#from guardrails import Guard
#from guardrails.validators import (register_validator, PassResult, FailResult)
#import guardrails.validators as gv
from guardrails import Guard
from guardrails.validators import (
    register_validator, FailResult, PassResult
)
#print(dir(gv))

@register_validator(name="is-haiku", data_type="string")
def is_haiku(value, metadata):
    if not value or len(value.split("\n")) != 3:
        return FailResult(error_message="This is not a haiku")
    return PassResult()

response = Guard().use(is_haiku)(
    model='gpt-3.5-turbo',
    messages=[{"role": "user", "content": "Write a haiku about AI"}],
)
print(response.validated_output)