# Aula 17 — Integrando cache semântico no endpoint de tickets

> Curso: **Cache** · Duração: `10:12`

## Resultado da aula

Nesta etapa, a busca e a decisão semântica deixam de existir apenas em endpoints auxiliares e
passam a fazer parte de `POST /tickets/analyze`. O [snapshot executável](mba-ia-cache/README.md)
representa exatamente esse ponto da evolução.

```text
requisição
   │
   ├─ fingerprint idêntico ────────────────> exact_cache
   │
   └─ miss exato → embedding → pgvector → threshold
                     │                    │
                     │ aceito             └─ rejeitado/ausente
                     ▼                                  ▼
               semantic_cache                      ai_model
                                                       │
                                                       └─ grava apenas no cache exato
```

Ainda não existe escrita automática no pgvector após a chamada à IA. Esse é o delta da aula
18 e foi mantido fora deste snapshot para que cada prática conserve seu próprio estágio.

## Leitura dos 21 prints

- [01.png](01.png) a [03.png](03.png): início da cascata, hit exato e preparação do miss.
- [04.png](04.png) a [07.png](07.png): validação do candidato, metadados e retorno do hit
  semântico.
- [08.png](08.png) e [09.png](09.png): caminho do miss semântico, chamada ao modelo e retorno.
- [10.png](10.png) a [15.png](15.png): roteiro HTTP, miss inicial, hit exato, configuração e
  estado do banco.
- [16.png](16.png) a [19.png](19.png): inserção manual e hit semântico com uma paráfrase.
- [20.png](20.png) e [21.png](21.png): alteração do threshold e miss semântico forçado.

Os prints também evidenciam a separação em `main.py`, `models.py`, `config.py`, `db.py` e
`log_helpers.py`; a mesma estrutura foi preservada no projeto local.

## Como a decisão é exposta

| Caminho | `source` | `cache.hit` | `semantic_cache.attempted` | `semantic_cache.hit` |
| --- | --- | --- | --- | --- |
| Hit exato | `exact_cache` | `true` | `false` | `false` |
| Hit semântico | `semantic_cache` | `false` | `true` | `true` |
| Modelo | `ai_model` | `false` | `true` | `false` |

`cache.hit` descreve somente o cache exato. Portanto, ele continua `false` quando a resposta
vem do cache semântico. `similarity = 1 - distance` é um score de cosseno; não representa
probabilidade de a resposta estar correta.

## Prática preparada

O snapshot inclui ambiente de exemplo, dependências, PostgreSQL/pgvector e um
[roteiro HTTP](mba-ia-cache/test.http). Quando for executar a aula, siga a preparação no
[README do projeto](mba-ia-cache/README.md) e rode os blocos na ordem.

O roteiro demonstra:

1. diagnóstico do banco;
2. inserção manual de uma análise válida;
3. hit semântico por mensagem parecida;
4. miss seguido de hit exato;
5. aumento do threshold para observar rejeição.

## Pontos para revisar

- O melhor candidato só é servido se superar o threshold e validar como `TicketAnalysis`.
- Um JSON estruturalmente válido ainda pode conter uma classificação inadequada.
- O fluxo não tenta o segundo candidato quando o primeiro tem JSON inválido.
- O cache exato e o contador existem apenas no processo atual.
- Falhas de embedding ou leitura do banco ainda interrompem o caminho do miss exato.

## Exercício

Por que elevar o threshold não altera uma resposta que já pode ser resolvida pelo cache exato?
