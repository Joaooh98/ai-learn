# Aula 01 — Cache em aplicações com IA não é só performance

> Curso: **Cache** · Duração: `07:17`

## Material e foco da aula

Os seis prints apresentam cache como uma decisão de **performance, custo e resiliência**.
A sequência compara aplicações tradicionais e chamadas de IA, questiona quando uma inferência
precisa ser repetida e introduz identidade de contexto, TTL, invalidação e fingerprint.
Veja [os três papéis do cache](03.png) e [validade e identidade de contexto](04.png).

## Resumo

Cache guarda um resultado para reutilizá-lo quando uma nova requisição permite a mesma resposta.
Evitar uma inferência pode reduzir latência, consumo de tokens e pressão nos limites do
provedor. Reutilizar uma saída aprovada também preserva a consistência daquela resposta.
Esses ganhos dependem de a resposta continuar correta para o contexto atual.

No exemplo do módulo, o resultado é uma classificação de ticket com `category`, `confidence`
e `reason`. Uma mensagem sobre cobrança pode ser repetida, mas deixar de ser equivalente se
mudar o prompt, a política de classificação ou o contexto do cliente.

| Papel | Ganho esperado | Condição para obter o ganho |
| --- | --- | --- |
| Performance | Evitar nova inferência | Consulta ao cache mais barata que o trabalho evitado |
| Custo | Reduzir chamadas de chat | Economia maior que armazenamento, busca e embeddings |
| Resiliência | Reduzir dependência do provedor no hit | Entrada existente, válida e acessível |
| Consistência | Reutilizar a mesma saída | Contrato e contexto compatíveis com a resposta |

## Complemento de estudo: decidir o que pode ser reutilizado

Um hit significa encontrar uma entrada **e aprová-la para uso**. Uma resposta antiga, de outro
cliente ou produzida sob outras regras não deve virar hit apenas porque está armazenada.
Cache-aside não garante sincronização automática com a fonte; a aplicação precisa definir
validade e invalidação. [Referência: Cache-Aside da Microsoft](https://learn.microsoft.com/en-us/azure/architecture/patterns/cache-aside).

Antes de cachear um caso de uso, registre:

- Qual entrada e contexto determinam a resposta: texto, regras, modelo, dados e permissões.
- Qual mudança exige recalcular: nova política, documento, estado ou contrato.
- Qual erro é tolerável: uma classificação incorreta pode encaminhar o ticket ao time errado.
- Como medir o resultado: latência por origem, custo por requisição e qualidade dos hits.

Uma explicação geral de uma política pode ser compartilhável entre clientes; o saldo da conta
exige identidade e estado da conta na política de reutilização. Para ações que mudam estado,
reaproveitar texto de resposta não substitui executar ou verificar a ação.

## Ponte com o projeto

O [projeto consolidado](../mba-ia-cache/README.md) implementa uma cascata de cache exato,
cache semântico e modelo de chat. Ele ajuda a observar os benefícios, mas não implementa TTL,
autorização ou isolamento por cliente. Esses pontos são evoluções arquiteturais, não garantias
do exemplo didático.

## Pergunta de revisão

Se a mensagem não mudou, mas a política de classificação mudou, por que retornar a mesma
resposta pode ser um erro mesmo com uma taxa de hit alta?
