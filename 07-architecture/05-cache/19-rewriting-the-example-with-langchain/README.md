# Aula 19 — Refazendo exemplo utilizando LangChain

> Curso: **Cache** · Duração: `12:16`

## Material disponível e limite de evidência

Esta pasta não tem prints nem uma versão isolada da reescrita. O
[projeto consolidado](../mba-ia-cache/README.md) usa LangChain, e os prints da aula 04 já
mostram esse framework na classificação. Portanto, o título não comprova que as aulas anteriores
eram inteiramente manuais nem que esta etapa adotou um vector store pronto.

## Abstrações realmente presentes

| Componente | Uso no projeto |
| --- | --- |
| `ChatPromptTemplate` | Constrói mensagens de sistema e usuário |
| `init_chat_model` | Inicializa o modelo de chat com provedor e parâmetros |
| `with_structured_output(TicketAnalysis)` | Produz análise compatível com o schema |
| Operador `\|` | Compõe prompt e modelo em uma cadeia executável |
| `OpenAIEmbeddings` | Gera vetores com `embed_documents` e `embed_query` |
| Psycopg + SQL | Persistem entradas e buscam candidatos no pgvector |
| Funções da aplicação | Definem chave, compatibilidade, threshold e fluxo de hit/miss |

Em [main.py](../mba-ia-cache/main.py), a composição é:

```python
chain = prompt | create_chat_model().with_structured_output(TicketAnalysis)
result = chain.invoke({"message": request.message})
```

Em [config.py](../mba-ia-cache/config.py), `OpenAIEmbeddings(model=...)` é criado separadamente.
O framework abstrai a chamada e a preparação; a aplicação continua tomando a decisão de cache.
[Referências: modelos e saída estruturada](https://docs.langchain.com/oss/python/langchain/models#structured-output)
e [OpenAIEmbeddings](https://docs.langchain.com/oss/python/integrations/embeddings/openai).

## O que não foi substituído por LangChain

[db.py](../mba-ia-cache/db.py) continua executando INSERT e SELECT com Psycopg. Não há instância
de `PGVector` do LangChain, registro de cache global do framework nem componente pronto de
cache semântico. A presença de LangChain no projeto não cria TTL, invalidação ou isolamento.

## Complemento de estudo: comparar implementações

Uma reescrita futura pode adotar um vector store, mas precisa preservar comportamento e
contrato. A integração PGVector existe no ecossistema LangChain; seu uso é uma opção de estudo,
não parte deste código. [Referência: integração PGVector](https://docs.langchain.com/oss/python/integrations/vectorstores/pgvector).

Antes de trocar abstrações, confira:

1. Mesma métrica, direção do score e regra inclusiva do threshold.
2. Mesmos filtros de versão, tenant, permissão e validade.
3. Mesmo modelo, dimensão e normalização do embedding.
4. Mesma validação do objeto reutilizado e política de escrita.
5. Mesmo tratamento de falhas, origem da resposta e métricas de custo/latência.

Uma biblioteca pode chamar de “score” um valor com outra escala. Não copie o limiar 0,90 sem
verificar o contrato da operação utilizada. Execute comparação com exemplos rotulados e com
o comportamento observável da implementação existente.

## Pergunta de revisão

Quais decisões de reutilização continuam sendo responsabilidade da aplicação mesmo quando
prompt, modelo e busca vetorial são encapsulados por um framework?
