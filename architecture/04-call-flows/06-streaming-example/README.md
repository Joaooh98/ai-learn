# Aula 06 — Exemplificando com streaming

> Curso: **Fluxos de Chamada** · Duração: `05:29`

## Observação sobre o material

Esta pasta ainda não contém prints nem código da aula. As notas abaixo foram registradas como
guia de estudo pela continuidade do módulo. Quando o material prático for adicionado (prints,
projeto de exemplo), este README pode ser ajustado para refletir o conteúdo exato da aula.

## Resumo

Dando sequência à implementação prática iniciada na aula 05, esta aula troca a chamada síncrona
simples por streaming, aplicando o conceito apresentado na aula 03
([`03-streaming-and-perceived-latency`](../03-streaming-and-perceived-latency/README.md)). O
objetivo é mostrar, na prática, como a resposta passa a ser consumida token a token em vez de
esperada por inteiro.

## O que a aula deve cobrir

- Ativação do modo streaming na chamada ao modelo (ex.: flag `stream=true` da API/SDK usada).
- Consumo incremental da resposta (chunks/tokens) conforme eles chegam.
- Exibição incremental do resultado (ex.: efeito de texto sendo "digitado" em tempo real).
- Comparação direta com o comportamento síncrono da aula anterior: mesma operação, latência real
  parecida, latência percebida bem menor.

## Fluxo conceitual

```text
Aplicação -> chama modelo (stream=true)
Modelo    -> token -> token -> token -> ... -> fim do stream
Aplicação -> exibe/processa cada token assim que chega
```

## Ideia-chave

O código muda pouco em relação à versão síncrona — a diferença está em como a resposta é
consumida. Essa aula reforça que streaming é uma mudança de baixo custo de implementação com alto
impacto na experiência percebida, o que explica por que costuma ser a primeira otimização antes de
se considerar processamento assíncrono.
