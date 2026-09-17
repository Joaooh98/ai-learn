# Prompt 03 — LiteLLM in Practice

> Origem: `architecture/ai-gateway/07-litellm-in-practice`
>
> Observação: o prompt abaixo foi reconstruído a partir dos prints da aula 07 e do resultado exibido nas capturas. Os prints mostram o início, as regras, as dependências e o resultado esperado do `main.py`; os trechos não visíveis foram completados pelo contexto do próprio resultado.

Refatore o `main.py` atual para usar LiteLLM como SDK no lugar dos SDKs nativos da OpenAI e da Anthropic.

Contexto:
O código atual já suporta `openai` e `anthropic` usando SDKs nativos, com `if provider == "openai"` e `elif provider == "anthropic"`. Agora quero simplificar isso usando LiteLLM como camada de compatibilidade.

Objetivo:
Manter o mesmo comportamento da aplicação, mas remover a duplicação de clients, SDKs e formatos de chamada.

Altere apenas:

`main.py`
`requirements.txt`

Regras:
Não usar frameworks.
Não usar LiteLLM Proxy.
Não fazer fallback.
A aplicação deve chamar somente um provider/modelo por execução.

Atualize o `requirements.txt` para:

`litellm`
`python-dotenv`

Mantenha as mesmas variáveis de ambiente:

`AI_PROVIDER`
`AI_MODEL`
`OPENAI_API_KEY`
`ANTHROPIC_API_KEY`

Defaults:

- se `AI_PROVIDER` não existir, usar `openai`;
- se `AI_MODEL` não existir e `AI_PROVIDER=openai`, usar `gpt-5.4-mini`;
- se `AI_MODEL` não existir e `AI_PROVIDER=anthropic`, usar `claude-sonnet-4-6`.

Lógica de modelo:

- se `AI_MODEL` já contiver `/`, usar o valor como está;
- caso contrário, prefixar o modelo com o provider no formato esperado pelo LiteLLM:
  - `openai/gpt-5.4-mini`
  - `anthropic/claude-sonnet-4-6`

O código deve:

1. manter o mesmo prompt do sistema;
2. ler `AI_PROVIDER` e `AI_MODEL`;
3. validar a API key correspondente ao provider escolhido;
4. tratar provider inválido com erro claro;
5. usar `from litellm import completion`;
6. fazer uma única chamada `completion()` para ambos os providers;
7. enviar `messages` com `system` e `user`;
8. usar `temperature=0.7`;
9. usar `max_tokens=1024`;
10. extrair a resposta com `response.choices[0].message.content`;
11. imprimir provider usado, modelo usado, pergunta e resposta;
12. tratar erros de forma simples com um único bloco `try/except`.

Resultado esperado:

- `main.py` não deve importar `OpenAI` nem `Anthropic`;
- `main.py` não deve ter blocos separados de chamada por provider;
- a troca entre OpenAI e Anthropic deve acontecer apenas por `AI_PROVIDER` e `AI_MODEL`;
- o código deve mostrar que LiteLLM remove a duplicação de SDKs, clients e formatos de resposta.

