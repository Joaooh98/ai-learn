# Aula 02 — Quando uma chamada síncrona ainda faz sentido

> Curso: **Fluxos de Chamada** · Duração: `04:17`

Esta aula delimita o espaço em que a chamada síncrona continua sendo uma boa escolha. Nem toda integração com IA precisa de streaming ou fila; o problema é usar síncrono para tudo.

## Resumo

Uma chamada síncrona faz sentido quando a aplicação precisa da resposta agora, a entrada é pequena, a saída é pequena e o tempo esperado é baixo. O exemplo da aula é uma análise de ticket de suporte: a aplicação envia uma mensagem curta e recebe uma classificação estruturada.

```http
POST /tickets/analisar
```

Entrada:

```json
{
  "message": "Fui cobrado duas vezes preciso de ajuda"
}
```

Saída esperada:

```json
{
  "category": "billing",
  "priority": "high",
  "summary": "Cobrança duplicada"
}
```

## Fluxo síncrono

```text
Usuário -> Web app -> IA -> resposta imediata
```

O backend espera a IA terminar e só então responde ao cliente. Esse modelo é simples, fácil de entender e adequado para tarefas pequenas.

## Onde o síncrono começa a falhar

O segundo diagrama mostra o risco de tratar toda chamada de IA da mesma forma:

```text
Usuário -> aplicação segura conexão -> IA demora -> timeout/falha
```

Problemas comuns:

- a request expira antes da IA terminar;
- a aplicação fica esperando sem dar feedback útil;
- o usuário fecha a tela e perde o resultado;
- o usuário repete cliques e dispara a mesma tarefa várias vezes;
- tarefas simples e tarefas longas competem pelo mesmo padrão de execução.

## Regra rápida

| Pergunta | Decisão |
|---|---|
| Precisa responder agora e costuma voltar rápido? | Use síncrono |
| Pode demorar, dar timeout ou envolver várias etapas? | Use outro fluxo |
| O usuário ganha vendo a resposta aos poucos? | Streaming pode ser melhor |
| O usuário só precisa do resultado final depois? | Job assíncrono |

## Ideia-chave

Síncrono não é errado. Ele só precisa ser reservado para tarefas pequenas, previsíveis e de baixo risco. O erro arquitetural é deixar trabalho longo preso na mesma request.
