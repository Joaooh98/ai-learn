# Aula 01 — O problema de execução em aplicações com IA

> Curso: **Fluxos de Chamada** · Duração: `04:44`

Esta aula abre o módulo mostrando que chamadas de IA não se comportam como chamadas HTTP tradicionais. O ponto central não é apenas "a IA demora"; é que a aplicação precisa escolher conscientemente se vai esperar, transmitir em partes ou delegar a execução para background.

## Resumo

Em uma integração tradicional, o fluxo costuma ser previsível: usuário aciona a interface, frontend chama backend, backend consulta API/banco e devolve uma resposta completa. Em IA, a resposta pode vir rápido, demorar vários segundos, chegar em partes via streaming, dar timeout ou nem chegar.

Isso muda tanto a arquitetura quanto a experiência do usuário. O sistema precisa dar feedback imediato, lidar com falhas, permitir retry/cancelamento e escolher o fluxo certo para cada tipo de tarefa.

## Integrações com IA e abstração

O primeiro diagrama reforça a importância de uma camada intermediária entre a aplicação e os modelos:

```text
Aplicação -> Abstração -> AI Gateway -> modelos/providers
```

Essa abstração centraliza interface, normalização de requests/responses, compatibilidade entre modelos, roteamento, limites e políticas. O objetivo é reduzir acoplamento: a aplicação não deve depender diretamente de detalhes de cada provider.

## Chamada tradicional vs chamada de IA

Uma chamada tradicional geralmente retorna uma resposta única e completa. Já uma chamada de IA tem latência variável e pode assumir vários formatos de entrega:

- resposta completa e rápida;
- resposta completa depois de vários segundos;
- streaming em pedaços;
- timeout;
- falha no meio do processamento.

Por isso, tratar IA como uma request comum costuma gerar UX ruim e riscos operacionais.

## Quando síncrono ainda serve

O material já antecipa uma regra importante: chamadas síncronas fazem sentido quando a entrada é pequena, a saída é curta e estruturada, e a resposta tende a voltar rápido. Exemplo: classificar um ticket e devolver JSON com categoria, prioridade e resumo.

Para respostas longas, abertas ou variáveis, streaming melhora a percepção de progresso. Para tarefas pesadas, com várias etapas, o fluxo deve sair da request original e virar processamento assíncrono.

## Fluxo para workloads pesados

O desenho final apresenta a direção recomendada para tarefas caras:

```text
request pesada -> cria job -> fila -> worker -> IA -> resultado/status -> usuário acompanha
```

O usuário recebe um `job_id`, acompanha status/progresso e busca o resultado quando estiver pronto. Isso evita conexões presas, reduz timeout e permite escalar workers separadamente.

## Regra prática

| Situação | Fluxo indicado |
|---|---|
| Resposta simples e rápida | Síncrono |
| Texto longo que o usuário pode ler aos poucos | Streaming |
| Tarefa longa, pesada ou com várias etapas | Job assíncrono |

## Ideia-chave

O tempo percebido pelo usuário importa tanto quanto o tempo real de execução. Feedback rápido, estados explícitos e escolha correta do fluxo tornam aplicações com IA mais confiáveis e mais agradáveis de usar.
