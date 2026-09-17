# Aula 01 — O problema de execução em aplicações com IA

> Curso: **Fluxos de Chamada** · Duração: `04:44`

## Observação sobre o material

Esta pasta ainda não contém prints da aula. As notas abaixo foram registradas como guia de
estudo a partir do título e da posição da aula no módulo. Quando os prints forem adicionados,
este README pode ser ajustado para refletir o fluxo exato da aula.

## Resumo

Toda chamada a um modelo de IA tem um custo de execução que não existe (ou é irrelevante) em
uma chamada tradicional a um banco de dados ou a um serviço interno: o tempo de resposta é alto,
variável e nem sempre previsível. Um modelo pode levar de alguns milissegundos a dezenas de
segundos para responder, dependendo do tamanho do prompt, do modelo escolhido e da carga do
provider.

Essa aula abre o módulo "Fluxos de Chamada" apresentando o problema central: se a aplicação trata
toda chamada de IA como se fosse uma chamada síncrona comum — "chama e espera" — ela herda essa
variabilidade de latência diretamente na experiência do usuário e na saúde do próprio sistema
(threads presas, timeouts, filas cheias).

## Por que isso é diferente de uma chamada comum

```text
Chamada tradicional:  aplicação -> serviço -> resposta        (latência baixa e estável)
Chamada de IA:         aplicação -> modelo  -> resposta        (latência alta e variável)
```

Os fatores que tornam a execução de IA um problema arquitetural, não apenas de implementação:

- **Latência alta**: gerar uma resposta é um processo de inferência, não uma consulta.
- **Latência variável**: prompts maiores, modelos maiores ou picos de demanda no provider mudam o
  tempo de resposta de forma imprevisível.
- **Custo por chamada**: cada execução tem custo financeiro, o que muda a forma como se lida com
  retries e re-execuções.
- **Bloqueio de recursos**: se a chamada é síncrona, o processo, a thread ou a conexão que espera
  a resposta fica ocupado durante todo esse tempo.

## Ideia-chave

O problema de execução em aplicações com IA não é "a IA é lenta". É que a arquitetura da aplicação
precisa decidir, de forma consciente, *como* esperar (ou não esperar) por essa resposta. As
próximas aulas do módulo tratam exatamente dessa decisão: quando uma chamada síncrona ainda é
aceitável, quando usar streaming e quando migrar para processamento assíncrono.
