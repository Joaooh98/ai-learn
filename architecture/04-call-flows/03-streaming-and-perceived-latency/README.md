# Aula 03 — Streaming e latência percebida

> Curso: **Fluxos de Chamada** · Duração: `05:31`

## Observação sobre o material

Esta pasta ainda não contém prints da aula. As notas abaixo foram registradas como guia de
estudo pela continuidade do módulo. Quando os prints forem adicionados, este README pode ser
ajustado para refletir o fluxo exato da aula.

## Resumo

Antes de justificar o processamento assíncrono (aula 04), o módulo apresenta uma solução
intermediária que resolve boa parte do problema de latência sem sair do modelo síncrono: o
streaming. A ideia central é separar **latência real** de **latência percebida** — a resposta
completa ainda demora o mesmo tempo, mas o usuário passa a ver o resultado sendo construído.

## Latência real vs. latência percebida

```text
Sem streaming:  aplicação -> [espera silenciosa] -> resposta completa de uma vez
Com streaming:  aplicação -> token -> token -> token -> ... -> resposta completa
```

- **Latência real**: tempo total até o último token da resposta.
- **Latência percebida**: tempo até o usuário ver o primeiro sinal de que algo está acontecendo
  (o primeiro token, o efeito "digitando").

Streaming não reduz a latência real de forma significativa, mas reduz drasticamente a latência
percebida, porque o feedback começa a chegar quase imediatamente após a chamada.

## Quando streaming resolve o problema

- Interfaces de chat e assistentes, onde o usuário está olhando ativamente para a tela.
- Respostas longas, em que esperar o texto inteiro pronto criaria uma pausa desconfortável.
- Casos em que a aplicação ainda é essencialmente síncrona do ponto de vista de fluxo, mas precisa
  parecer responsiva.

## O limite do streaming

Streaming continua sendo uma chamada síncrona do ponto de vista da conexão: o cliente (ou o
processo) permanece conectado até o fim da resposta. Ele resolve percepção de latência, não
resolve bloqueio de recursos em alto volume, chamadas que não têm um usuário olhando em tempo
real, ou fluxos que precisam continuar mesmo que a conexão original caia — cenários que empurram
a decisão para processamento assíncrono, tema da próxima aula.

## Ideia-chave

Streaming é a ponte entre "síncrono simples" e "assíncrono completo": mantém o modelo de chamada
síncrona, mas muda a forma como a resposta é entregue, atacando diretamente a percepção de
lentidão sem reestruturar a arquitetura da aplicação.
