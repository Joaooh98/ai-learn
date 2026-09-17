# Aula 04 — Quando transformar IA em processamento assíncrono

> Curso: **Fluxos de Chamada** · Duração: `03:52`

## Observação sobre o material

Esta pasta ainda não contém prints da aula. As notas abaixo foram registradas como guia de
estudo pela continuidade do módulo. Quando os prints forem adicionados, este README pode ser
ajustado para refletir o fluxo exato da aula.

## Resumo

Depois de síncrono (aula 02) e streaming (aula 03), esta aula fecha a parte conceitual do módulo
definindo o terceiro caminho: processamento assíncrono. A chamada de IA deixa de bloquear o
fluxo principal da aplicação — a aplicação dispara o trabalho, segue com outras tarefas, e a
resposta chega depois, por um outro canal.

## Sinais de que é hora de sair do síncrono/streaming

- **A resposta não precisa ser imediata**: geração de relatórios, resumos em lote, enriquecimento
  de dados, processamento de documentos.
- **Não há um usuário esperando em tempo real**: jobs, integrações entre sistemas, pipelines de
  dados.
- **Alto volume concorrente**: manter uma conexão aberta por chamada não escala quando há milhares
  de execuções simultâneas.
- **Tolerância a falha e reprocessamento**: assíncrono normalmente já convive com fila, retry e
  reprocessamento — mais fácil de absorver falha de um provider de IA.

## Fluxo conceitual

```text
Aplicação -> enfileira pedido -> segue seu fluxo normal
Worker     -> consome fila -> chama o modelo -> grava resultado
Aplicação  -> consulta resultado (polling, callback, webhook ou evento)
```

## O custo de ir assíncrono

Processamento assíncrono resolve o bloqueio de recursos e a escala, mas troca simplicidade por
infraestrutura: é preciso fila, worker, forma de entregar o resultado (callback, webhook, evento)
e tratamento de estado ("pendente", "processando", "concluído", "falhou"). Esse custo só se paga
quando o problema real é volume, escala ou ausência de usuário esperando em tempo real — não deve
ser a escolha padrão.

## Ideia-chave

Síncrono, streaming e assíncrono não são um ranking de "melhor para pior": são três respostas
diferentes para o mesmo problema de latência, cada uma correta em um contexto. As próximas aulas
do módulo colocam essas três opções em prática.
