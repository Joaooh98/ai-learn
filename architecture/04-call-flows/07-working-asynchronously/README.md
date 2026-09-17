# Aula 07 — Trabalhando de forma assíncrona

> Curso: **Fluxos de Chamada** · Duração: `06:18`

## Observação sobre o material

Esta pasta ainda não contém prints nem código da aula. As notas abaixo foram registradas como
guia de estudo pela continuidade do módulo. Quando o material prático for adicionado (prints,
projeto de exemplo), este README pode ser ajustado para refletir o conteúdo exato da aula.

## Resumo

Fechando o módulo "Fluxos de Chamada", esta aula implementa o terceiro fluxo apresentado na parte
teórica (aula 04 —
[`04-when-to-turn-ai-into-async-processing`](../04-when-to-turn-ai-into-async-processing/README.md)):
processamento assíncrono. A chamada ao modelo deixa de bloquear o fluxo principal da aplicação —
o pedido é aceito, colocado para processar em segundo plano, e o resultado é entregue depois.

## O que a aula deve cobrir

- Separação entre o ponto que **recebe o pedido** e o ponto que **processa a chamada ao modelo**
  (ex.: fila, worker ou tarefa em background).
- Resposta imediata da aplicação ao cliente (ex.: um identificador de job/tarefa), sem esperar o
  modelo responder.
- Alguma forma de entregar o resultado depois: consulta por polling, callback, webhook ou evento.
- Estados do pedido ao longo do processamento (`pendente`, `processando`, `concluído`, `falhou`).

## Fluxo conceitual

```text
Cliente    -> aplicação: pede execução
Aplicação  -> enfileira -> responde imediatamente com um id de job
Worker     -> consome a fila -> chama o modelo -> grava o resultado
Cliente    -> consulta o resultado pelo id (polling/callback/webhook)
```

## Ideia-chave

Esta aula fecha o ciclo do módulo mostrando, na prática, o custo de infraestrutura descrito na
aula 04 em troca de escalar sem bloquear recursos por chamada. Com os três fluxos implementados —
síncrono (aula 05), streaming (aula 06) e assíncrono (aula 07) — o módulo entrega uma base
comparável para decidir qual usar em cada cenário real.
