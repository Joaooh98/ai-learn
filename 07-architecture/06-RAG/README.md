# 06 — RAG

[Arquitetura](../README.md) · [Anterior: Cache](../05-cache/README.md)

Este módulo reúne 34 aulas sobre RAG, seguindo a ordem do curso. As pastas estão numeradas
e cada aula contém um README com título, duração e espaço para as notas e imagens.

Os prints já disponíveis das aulas 01 e 02 foram preservados nas respectivas pastas.
O item **Código-fonte** da plataforma é um recurso complementar e não entra na numeração
das aulas.

## Roteiro de estudo

| Aula | Assunto | Duração |
|---|---|---|
| 01 | [O que é RAG](01-what-is-rag/README.md) | `05:50` |
| 02 | [O que RAG não resolve](02-what-rag-does-not-solve/README.md) | `06:24` |
| 03 | [RAG vs outras estratégias arquiteturais](03-rag-vs-other-architectural-strategies/README.md) | `06:09` |
| 04 | [Entendendo o Projeto Prático](04-understanding-the-practical-project/README.md) | `05:25` |
| 05 | [Estrutura dos arquivos iniciais](05-initial-file-structure/README.md) | `03:35` |
| 06 | [Criando a base de documentos em Markdown](06-creating-the-document-base-in-markdown/README.md) | `02:17` |
| 07 | [Perguntando ao modelo sem RAG](07-asking-the-model-without-rag/README.md) | `02:16` |
| 08 | [Colocando documento inteiro no prompt e entendendo o limite](08-putting-the-entire-document-in-the-prompt-and-understanding-the-limit/README.md) | `05:13` |
| 09 | [Arquitetura do RAG - ingestão, índice, retrieval e geração](09-rag-architecture-ingestion-index-retrieval-and-generation/README.md) | `05:39` |
| 10 | [Pipeline de ingestão inicial](10-initial-ingestion-pipeline/README.md) | `06:17` |
| 11 | [Chunking, metadados e versionamento](11-chunking-metadata-and-versioning/README.md) | `06:54` |
| 12 | [Gerando chunks com metadados](12-generating-chunks-with-metadata/README.md) | `11:50` |
| 13 | [Indexando chunks no Postgres com pgvector](13-indexing-chunks-in-postgres-with-pgvector/README.md) | `12:01` |
| 14 | [Retrieval onde o RAG ganha ou perde](14-retrieval-where-rag-wins-or-loses/README.md) | `05:33` |
| 15 | [Testando retrieval isolado](15-testing-retrieval-in-isolation/README.md) | `12:20` |
| 16 | [Montagem do contexto e prompt final](16-assembling-context-and-final-prompt/README.md) | `06:30` |
| 17 | [Primeira resposta com RAG](17-first-response-with-rag/README.md) | `06:45` |
| 18 | [Resposta com fontes, recusa e debug](18-response-with-sources-refusal-and-debug/README.md) | `08:56` |
| 19 | [Por que RAG simples falha](19-why-simple-rag-fails/README.md) | `05:47` |
| 20 | [Melhorando uma busca ruim](20-improving-a-poor-search/README.md) | `08:02` |
| 21 | [Intenção da pergunta antes do retrieval](21-question-intent-before-retrieval/README.md) | `05:04` |
| 22 | [Demonstrando Query Planner](22-demonstrating-query-planner/README.md) | `10:12` |
| 23 | [Entendendo o Código do Query Planner](23-understanding-query-planner-code/README.md) | `12:09` |
| 24 | [Reranking e seleção final do contexto](24-reranking-and-final-context-selection/README.md) | `05:55` |
| 25 | [Aplicando reranking simples nos chunks recuperados](25-applying-simple-reranking-to-retrieved-chunks/README.md) | `09:27` |
| 26 | [Entendendo o código do Rerank](26-understanding-rerank-code/README.md) | `04:00` |
| 27 | [Reranking sem chamar o modelo novamente](27-reranking-without-calling-the-model-again/README.md) | `05:16` |
| 28 | [Documentos mudam - consistência e reindexação](28-documents-change-consistency-and-reindexing/README.md) | `05:41` |
| 29 | [Manifest, hash e reindexação idempotente](29-manifest-hash-and-idempotent-reindexing/README.md) | `09:30` |
| 30 | [Entendendo código de Indexação](30-understanding-indexing-code/README.md) | `06:23` |
| 31 | [Expondo o Knowledge Chat como API](31-exposing-knowledge-chat-as-an-api/README.md) | `06:11` |
| 32 | [Logs, tempos e resposta auditável](32-logs-timings-and-auditable-response/README.md) | `07:53` |
| 33 | [Soluções prontas de providers e decisão build vs buy](33-provider-solutions-and-build-vs-buy-decision/README.md) | `08:50` |
| 34 | [Checklist arquitetural de RAG](34-rag-architectural-checklist/README.md) | `06:28` |

## Como preencher as aulas

Adicione os prints na pasta da aula, na ordem em que aparecem, e preencha o README com
as notas correspondentes. Preserve os nomes das imagens que já estão no módulo.
