# Prompt 02 — Adding Anthropic as Option

> Origem: `architecture/ai-gateway/03-adding-anthropic-as-option`
>
> Observação: as imagens mostram integralmente o início, variáveis/defaults e regras finais do prompt. O bloco central de dependências/execução foi reconstruído seguindo o padrão do prompt anterior e o contexto visível nas capturas.

Altere o projeto anterior para permitir escolher entre OpenAI e Anthropic por variável de ambiente.

Objetivo:
Modificar o exemplo anterior para mostrar que, sem uma camada de compatibilidade, a aplicação precisa conhecer os SDKs nativos de cada provider. A ideia não é fazer fallback. A ideia é escolher apenas um provider/modelo por execução.

Altere apenas estes arquivos:

`main.py`
`requirements.txt`
`.env.example`

Não usar frameworks.
Não usar LiteLLM.

Dependências no `requirements.txt`:

`openai`
`anthropic`
`python-dotenv`

Use `.venv` para instalar as dependências:

`python -m venv .venv`
`source .venv/bin/activate`
`pip install -r requirements.txt`

Funcionamento:

`AI_PROVIDER=openai python main.py "O que é uma AI Gateway?"`
`AI_PROVIDER=anthropic python main.py "O que é uma AI Gateway?"`

Se nenhuma pergunta for enviada, usar:

`"O que é uma AI Gateway e por que ela é importante em aplicações com IA?"`

Variáveis de ambiente:

`AI_PROVIDER`
`AI_MODEL`
`OPENAI_API_KEY`
`ANTHROPIC_API_KEY`

Se `AI_PROVIDER` não existir, usar:

`openai`

Se `AI_MODEL` não existir:
usar `gpt-5.4-mini` quando `AI_PROVIDER=openai`;
usar `claude-sonnet-4-6` quando `AI_PROVIDER=anthropic`.

O código deve:

1. manter o mesmo prompt do sistema;
2. ler `AI_PROVIDER` e `AI_MODEL`;
3. se `AI_PROVIDER=openai`, validar `OPENAI_API_KEY` e chamar somente o SDK nativo da OpenAI;
4. se `AI_PROVIDER=anthropic`, validar `ANTHROPIC_API_KEY` e chamar somente o SDK nativo da Anthropic;
5. não fazer fallback;
6. não tentar outro provider se a chamada falhar;
7. tratar provider inválido com erro claro;
8. imprimir provider usado, modelo usado, pergunta e resposta;
9. tratar erros de forma simples.

Deixe comentários curtos no código mostrando que agora a aplicação conhece dois SDKs, dois clients e dois formatos de chamada.

