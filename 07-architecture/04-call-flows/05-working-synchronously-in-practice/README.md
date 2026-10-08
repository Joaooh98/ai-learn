# Aula 05 — Trabalhando de forma síncrona na prática

[Índice do módulo](../README.md)

> Curso: **Fluxos de Chamada** · Duração: `04:51`

Esta aula implementa a primeira versão prática: uma API FastAPI que recebe um ticket de suporte, chama a IA de forma bloqueante e devolve um JSON estruturado somente quando a resposta completa chega.

## Resumo

O fluxo implementado é:

```text
request entra -> backend chama IA -> backend espera a resposta -> devolve JSON
```

Esse é o comportamento tradicional de uma chamada síncrona. Ele é simples e serve bem para entradas pequenas e respostas curtas, como classificação de ticket.

## Estrutura vista na aula

```text
app/
  __init__.py
  ai_client.py
  main.py
  schemas.py
main.py
requests.http
requirements.txt
.env.example
```

Arquivos principais:

- `schemas.py`: define `TicketRequest` e `TicketAnalysis` com Pydantic.
- `ai_client.py`: encapsula a chamada bloqueante para OpenAI.
- `app/main.py`: expõe `POST /tickets/analyze`.
- `main.py`: roda o Uvicorn apontando para `app.main:app`.

## Prompt usado

O prompt solicita uma resposta JSON com exatamente três campos:

```text
Você é um assistente que analisa tickets de suporte.
Responda SEMPRE em JSON válido, sem texto extra, com exatamente estas chaves:
"category" (ex: billing, technical, account),
"priority" (low, medium ou high) e
"summary" (resumo curto do problema em português).
```

## O que observar

- A rota só responde depois que a IA termina.
- `response_format={"type": "json_object"}` ativa JSON mode; isso não garante o schema do ticket.
- O JSON ainda precisa ser parseado e validado com Pydantic.
- Erros de JSON, validação ou provider viram HTTP 500.
- Validação de entrada vazia vira HTTP 422 automaticamente pelo FastAPI/Pydantic.

## Projeto prático

O projeto reproduzível está em [sync-ticket-analysis](./sync-ticket-analysis/README.md).

## Ideia-chave

O fluxo síncrono é a linha de base do módulo: fácil de entender, direto de testar, mas bloqueante. As próximas aulas mostram como streaming e jobs assíncronos mudam esse comportamento.

## Complemento — Formato JSON e validação do domínio

JSON mode garante formato JSON nos casos suportados, com exceções como saída incompleta, mas não impõe o schema do ticket. Structured Outputs com schema é outra configuração; o código desta aula usa somente `json_object`. [Guia oficial de saídas estruturadas](https://developers.openai.com/api/docs/guides/structured-outputs).

O [schemas.py](sync-ticket-analysis/app/schemas.py) usa `str` para `category` e `priority`. As descrições não são enums; uma categoria desconhecida ou prioridade `urgent` ainda podem passar na validação. `min_length=1` rejeita `""`, mas não uma mensagem composta apenas por espaços, e não há limite máximo de tamanho no exemplo.

O client é bloqueante, mas a rota `def` é executada em thread pool pelo FastAPI. Muitas chamadas lentas ainda consomem slots desse pool e conexões ao provider. A implementação não define timeout ou retry explícitos; veja os [limites dos demos](../README.md#limites-verificados-no-código).

**Evolução sugerida:** definir categorias e prioridades enumeradas, normalizar entrada, limitar tamanho, tratar recusas e truncamento, e avaliar acerto da classificação além do parse.
