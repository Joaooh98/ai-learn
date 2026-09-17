# Aula 05 — Trabalhando de forma síncrona na prática

> Curso: **Fluxos de Chamada** · Duração: `04:51`

## Observação sobre o material

Esta pasta ainda não contém prints nem código da aula. As notas abaixo foram registradas como
guia de estudo pela continuidade do módulo. Quando o material prático for adicionado (prints,
projeto de exemplo), este README pode ser ajustado para refletir o conteúdo exato da aula.

## Resumo

O módulo passa da teoria (aulas 01 a 04) para a prática. Esta aula implementa o primeiro dos três
fluxos discutidos: uma chamada síncrona clássica a um modelo de IA, sem streaming e sem fila —
o padrão mais simples possível, usado como base de comparação para as próximas aulas.

## O que a aula deve cobrir

- Uma chamada direta ao modelo, aguardando a resposta completa antes de continuar o fluxo.
- Observação do tempo de resposta e do comportamento da aplicação enquanto espera (bloqueio da
  thread/processo durante a chamada).
- Tratamento básico de erro e timeout — o mínimo necessário para uma chamada síncrona não travar
  a aplicação indefinidamente.

## Fluxo conceitual

```text
Aplicação -> chama modelo (aguarda) -> recebe resposta completa -> segue o fluxo
```

## Ideia-chave

Implementar o caso síncrono primeiro serve como linha de base: é o comportamento mais simples de
entender e depurar, e é contra ele que as aulas seguintes — streaming (aula 06) e assíncrono
(aula 07) — vão comparar ganhos em latência percebida e em uso de recursos.
