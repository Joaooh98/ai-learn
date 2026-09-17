# Aula 01 — Cache em aplicações com IA não é só performance

> Curso: **Cache** · Duração: `07:17`

## Observação sobre o material

Esta pasta ainda não contém prints da aula. As notas abaixo foram registradas como guia de
estudo a partir do título e da posição da aula no módulo. Quando os prints forem adicionados,
este README pode ser ajustado para refletir o fluxo exato da aula.

## Resumo

Em sistemas tradicionais, cache existe quase sempre por um motivo: performance — evitar refazer
um trabalho caro em tempo. Em aplicações com IA, esse motivo continua válido, mas deixa de ser o
único. Cada chamada a um modelo tem custo financeiro direto (tokens pagos por requisição) e
latência alta e variável, então cachear uma resposta também é uma decisão de **custo** e de
**previsibilidade**, não apenas de velocidade.

## Motivos para cachear além de performance

- **Custo por chamada**: repetir a mesma pergunta para o modelo paga o mesmo preço de novo.
- **Latência alta**: evitar uma nova inferência evita esperar novamente pelo tempo de resposta.
- **Consistência de resposta**: para perguntas repetidas, servir a mesma resposta já validada pode
  ser desejável, em vez de gerar uma resposta nova (e potencialmente diferente) a cada chamada.
- **Redução de carga no provider**: menos chamadas repetidas ajudam a não esbarrar em limites de
  rate limit.

## Ideia-chave

Cache em aplicações com IA é uma decisão arquitetural que mistura custo, latência e consistência.
As próximas aulas do módulo constroem, em camadas, do cache mais simples (hit/miss, cache-aside)
até o cache semântico e o prompt caching nativo dos providers.
