# Prompt 01 — Calling OpenAI with SDK

> Origem: `architecture/ai-gateway/02-calling-openai-with-sdk`

Crie um exemplo simples em Python usando o SDK nativo da OpenAI.

Objetivo:
Gerar um projeto mínimo para demonstrar uma chamada direta à OpenAI. Esse exemplo será usado em aula para mostrar o cenário mais simples, onde a aplicação conhece diretamente o provider, o SDK, o modelo e o prompt.

Crie apenas estes arquivos:

`main.py`
`requirements.txt`
`.env.example`

Não usar frameworks.

Dependências no `requirements.txt`:

`openai`
`python-dotenv`

Use `.venv` para instalar as dependências:

`python -m venv .venv`
`source .venv/bin/activate`
`pip install -r requirements.txt`

Funcionamento:

`python main.py "O que é uma AI Gateway?"`

Se nenhuma pergunta for enviada, usar:

`"O que é uma AI Gateway e por que ela é importante em aplicações com IA?"`

Variáveis de ambiente:

`OPENAI_API_KEY`
`OPENAI_MODEL`

Se `OPENAI_MODEL` não existir, usar:

`gpt-5.4-mini`

Prompt do sistema dentro do `main.py`:

`Você é um arquiteto de software explicando IA para desenvolvedores. Responda de forma didática, prática e objetiva. O tema é AI Gateway. Explique o conceito conectando com problemas reais de aplicações que chamam modelos de IA em produção.`

O código deve:

1. carregar variáveis de ambiente com `python-dotenv`;
2. validar `OPENAI_API_KEY`;
3. ler a pergunta via `sys.argv`;
4. chamar diretamente o SDK nativo da OpenAI;
5. imprimir modelo usado, pergunta e resposta;
6. tratar erros de forma simples.

