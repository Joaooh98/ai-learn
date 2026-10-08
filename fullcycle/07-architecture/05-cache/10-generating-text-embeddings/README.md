# Aula 10 — Gerando embeddings de textos

> Curso: **Cache** · Duração: `06:20`

## Material e foco da aula

Os 23 prints mostram extração de configuração/modelos, criação de `OpenAIEmbeddings` e o
endpoint `POST /embeddings/generate`. [10.png](10.png) mostra validação e chamada em lote;
[19.png](19.png) registra a dimensão retornada; [23.png](23.png) mostra três textos de teste.

O [snapshot prático desta aula](mba-ia-cache/README.md) contém exatamente esse estágio do
projeto, isolado dos recursos de PostgreSQL e busca semântica adicionados nas aulas seguintes.

## Fluxo observado

```text
{"texts": [...]} → valida lista → normaliza textos → embed_documents
                → associa texto e vetor → retorna dimensão e prévia
```

Exemplo de corpo compatível com o endpoint:

```json
{
  "texts": [
    "Como cancelo minha assinatura?",
    "Quero cancelar meu plano",
    "Não consigo acessar minha conta"
  ]
}
```

Em [main.py](mba-ia-cache/main.py), a API rejeita lista vazia e textos que ficam vazios após
normalização. `embed_documents(normalized_texts)` gera os vetores, mas a resposta HTTP expõe
somente `embedding_dimension` e os cinco primeiros componentes em `embedding_preview`.
A prévia não é suficiente para calcular similaridade ou persistir o vetor completo.

## Complemento de estudo: dimensão é um contrato

O padrão de `text-embedding-3-small` é 1536 dimensões. Modelos que aceitam redução de dimensão
precisam receber o parâmetro apropriado na geração. [Referência: dimensões na API de embeddings](https://developers.openai.com/api/docs/guides/embeddings#how-to-get-embeddings).

No projeto, `OPENAI_EMBEDDING_DIMENSIONS` configura a coluna do banco e metadados, mas
`create_embedding_model()` passa apenas `model=OPENAI_EMBEDDING_MODEL`. Portanto, mudar essa
variável **não muda automaticamente** a dimensão produzida. Confirme `len(vector)` e a
definição da coluna antes de armazenar ou migrar dados.

LangChain distingue `embed_documents()` para uma lista de textos e `embed_query()` para uma
consulta. O projeto usa a primeira no endpoint de demonstração e a segunda nas operações do
cache semântico. [Referência: integração OpenAIEmbeddings](https://docs.langchain.com/oss/python/integrations/embeddings/openai).

## O que conferir ao reproduzir

- Associação correta entre texto original, texto normalizado e vetor retornado.
- Compatibilidade entre modelo, dimensão e coluna `VECTOR(n)`.
- Limites de entrada e lote do modelo escolhido, com tratamento explícito de falha.
- Preservação de informação útil na normalização.
- Latência e custo de embedding separados da inferência de chat.

Gerar embedding via provedor é uma chamada externa e pode ter custo. Um hit semântico evita
o classificador de chat, mas pode continuar pagando pela representação da consulta.

## Exercício

Explique por que “retornou cinco números na prévia” não significa “embedding com cinco
dimensões”. Como detectar uma configuração incompatível com o banco sem chamar o classificador?
