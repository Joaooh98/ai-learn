# Provider Selection Example

[Índice do módulo](../../README.md) · [Aula correspondente](../README.md)

Esta pasta concentra os prompts e artefatos do projeto prático que evolui de chamada direta com SDKs nativos para uma camada de compatibilidade com LiteLLM.

## Prompts

| # | Arquivo | Origem |
|---|---------|--------|
| 02 | [adding-anthropic-as-option.md](adding-anthropic-as-option.md) | Aula 03 — Adicionando Anthropic como opção |
| 03 | [litellm-in-practice.md](litellm-in-practice.md) | Aula 07 — LiteLLM na prática |

## Execução do artefato presente

Execute os comandos nesta pasta. Copie `.env.example` para `.env`, preencha a chave do provider e configure `AI_MODEL` com um identificador de modelo disponível para sua conta.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Depois de preencher o `.env`, execute:

```bash
python main.py "Explique AI Gateway em uma aplicação de suporte"
```

O prompt é um registro da aula, e o código presente pode ter defaults diferentes. Confira [main.py](main.py), [requirements.txt](requirements.txt) e [.env.example](.env.example). As dependências não estão fixadas; anote as versões usadas ao comparar resultados.

## Seleção coerente de provider e modelo

```bash
AI_PROVIDER=openai AI_MODEL=gpt-4.1-mini python main.py "O que é AI Gateway?"
AI_PROVIDER=anthropic AI_MODEL=claude-sonnet-4-6 python main.py "O que é AI Gateway?"
```

Os identificadores acima ilustram overrides encontrados na trilha; verifique disponibilidade e acesso na sua conta. O default `claude-3-5-sonnet-20241022` presente no código foi aposentado em 28 de outubro de 2025. [Histórico oficial de deprecações Anthropic](https://platform.claude.com/docs/en/about-claude/model-deprecations).

Trocar `AI_PROVIDER` mantendo um `AI_MODEL` incompatível não faz seleção automática de um modelo equivalente. No LiteLLM, o prefixo de um valor já qualificado deve concordar com o provider escolhido.
