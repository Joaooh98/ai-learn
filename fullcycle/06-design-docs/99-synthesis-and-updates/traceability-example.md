# Exemplo proposto: rastrear um contrato de rate limiting

[Índice da revisão](README.md) · **Exercício novo**, elaborado em 19/11/2026.
Os valores abaixo não são requisitos confirmados da aula nem desempenho medido.

## Contexto e decisão em aberto

As notas locais descrevem alternativas de serviço dedicado e SDK in-process. Antes de
implementar, escolha uma delas e alinhe produto, HLD e FDD. Neste exercício, suponha que
foi escolhido SDK in-process com Redis compartilhado para o estado e fixed window de 60 segundos.
A quota de 100 requisições por tenant é um valor didático para testar o contrato.

## Rastreabilidade mínima

| ID | Afirmação proposta | Decisão/contrato | Evidência esperada |
|---|---|---|---|
| REQ-01 | Cada tenant tem quota independente | Chave derivada de tenant autenticado e política | TEST-01: A excede quota sem bloquear B |
| REQ-02 | A janela aceita no máximo 100 operações de custo unitário | Operação atômica no estado compartilhado | TEST-02: janela inicialmente vazia, sem tráfego externo na mesma chave: 200 chamadas concorrentes admitem exatamente 100, sem falha de infraestrutura |
| REQ-03 | Bloqueio informa espera | Resposta 429 com Retry-After em segundos | TEST-03: valor não negativo e consistente com o reset |
| REQ-04 | Falha do estado não parece excesso de quota | Erro de dependência separado da decisão de bloqueio | TEST-04: Redis indisponível não fabrica remaining/reset |
| REQ-05 | A política de falha é explícita | ADR define fail-open ou fail-closed por classe de rota | TEST-05: o modo escolhido é observável e recuperável |

TEST-02 exige controlar o relógio/janela do cenário. Se as chamadas atravessarem um reset,
a expectativa de 100 admissões deixa de ser válida para a amostra inteira. Essa condição
precisa constar do teste, não só do texto do requisito.

## Contrato de bloqueio ilustrativo

A [RFC 6585](https://www.rfc-editor.org/rfc/rfc6585.html#section-4) define `429` para excesso
de requisições e permite informar `Retry-After`. Um exemplo proposto, usando
[Problem Details da RFC 9457](https://www.rfc-editor.org/rfc/rfc9457.html), seria:

```http
HTTP/1.1 429 Too Many Requests
Retry-After: 12
Content-Type: application/problem+json
Cache-Control: no-store

{
  "type": "about:blank",
  "title": "Too Many Requests",
  "status": 429,
  "detail": "A quota desta janela foi excedida. Tente novamente após o intervalo informado."
}
```

A unidade e o cálculo da espera fazem parte do contrato. Não use um valor fixo de 12 segundos
em todas as respostas: ele representa apenas um instante hipotético. Não exponha chave de
API, identificador sensível ou configuração interna no corpo.

## Minuta de ADR, sem decisão fingida

**Estado:** proposta para o exercício.

**Questão:** priorizar continuidade ou enforcement em falha de Redis?

**Opções:** permitir temporariamente, negar temporariamente ou usar uma política local limitada.

**Consequências a avaliar:** disponibilidade, abuso, custo, justiça entre réplicas, duração da
degradação e operação de recuperação. Um limite local por processo não equivale a quota global.

**Confirmação necessária:** responsáveis pelo produto e pelo serviço escolhem a política
para cada classe de rota e verificam os cenários de indisponibilidade. Até essa decisão,
o FDD deve manter a questão aberta.
