# Aula 06 — Exemplificando com streaming

> Curso: **Fluxos de Chamada** · Duração: `05:29`

Esta aula evolui a API síncrona da aula anterior adicionando um endpoint de streaming para explicação textual. A ideia é comparar dois fluxos no mesmo backend: JSON completo para máquina e texto progressivo para experiência humana.

## Resumo

A aplicação passa a ter dois caminhos:

```text
Fluxo 1: /tickets/analyze -> espera a IA terminar -> devolve JSON
Fluxo 2: /tickets/explain -> IA gera chunks -> devolve texto em partes
```

O endpoint de streaming não tenta devolver JSON. Ele usa um prompt próprio para texto corrido, em português, com frases curtas e progressivas.

## Prompt de explicação

```text
Você é um assistente de suporte. Explique, em texto corrido e em português,
o que o cliente está relatando e qual a recomendação inicial de tratamento.
Escreva de forma progressiva, em algumas frases curtas. Não use JSON.
```

## Implementação vista na aula

No cliente de IA:

- `stream=True` faz o SDK devolver um iterável de chunks.
- Cada `chunk.choices[0].delta.content` é repassado com `yield`.
- Se houver erro no meio do stream, a aplicação não consegue mais trocar o status HTTP; por isso envia uma mensagem simples no próprio texto.

Na rota FastAPI:

- `POST /tickets/explain` retorna `StreamingResponse`.
- A rota tenta puxar o primeiro chunk antes de começar a resposta, para transformar falha inicial em HTTP 500.
- Depois do primeiro byte enviado, o restante é entregue com `yield from chunks`.

## Teste com curl

O print usa `curl -N` para não bufferizar a resposta:

```bash
curl -N -w "\nTempo total: %{time_total}s\n" \
  -X POST http://127.0.0.1:8000/tickets/explain \
  -H "Content-Type: application/json" \
  -d '{"message": "Fui cobrado duas vezes e preciso de ajuda com meu pagamento."}'
```

## Projeto prático

O projeto reproduzível está em [streaming-ticket-explanation](./streaming-ticket-explanation/README.md).

## Ideia-chave

Streaming não é para dados estruturados finais. Ele é para respostas textuais em que o usuário ganha algo vendo o conteúdo aparecer antes da conclusão completa.
