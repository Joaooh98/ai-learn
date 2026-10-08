# Aula 12 — Cache semântico não é RAG

> Curso: **Cache** · Duração: `04:20`

## Material e foco da aula

Os quatro prints comparam busca de resposta anterior com recuperação de conhecimento.
[02.png](02.png) mostra os dois caminhos; [03.png](03.png) distingue o que se armazena e o que
é devolvido. O módulo continua focado em evitar inferência repetida, sem pipeline de documentos.

## A diferença arquitetural

| Aspecto | Cache semântico de resposta | RAG |
| --- | --- | --- |
| Busca | Entradas anteriores com resposta reutilizável | Evidências ou documentos relevantes |
| Conteúdo recuperado | Resultado já produzido | Contexto para fundamentar geração |
| Caminho de sucesso | Devolve saída anterior sem nova inferência de chat | Usa conhecimento recuperado para gerar saída |
| Questão central | Esta resposta pode ser reutilizada? | Que informação deve fundamentar a resposta? |

```text
cache: pergunta → busca candidatos → aceita resposta anterior → devolve
                                 → rejeita → segue para geração

RAG:   pergunta → recupera evidências → prepara contexto → geração com contexto
```

Embeddings e banco vetorial podem atender aos dois fluxos, mas não são obrigatórios para toda
implementação de RAG. A recuperação também pode combinar busca textual e outros mecanismos.
[Referência: recuperação e RAG no LangChain](https://docs.langchain.com/oss/python/deepagents/retrieval).

## Complemento de estudo: combinar sem perder validade

O caminho típico de geração em RAG chama o modelo depois da recuperação. Isso não significa
que um sistema com RAG precisa gerar novamente em toda requisição: ele pode ter caches antes
ou depois da recuperação.

Um fluxo possível, como complemento arquitetural:

```text
cache exato → cache semântico elegível
  miss → recuperação de documentos → prompt com evidências → modelo → escrita elegível
```

Nesse sistema, a versão da base ou das evidências precisa participar da validade do resultado.
Se um documento muda, uma resposta antiga pode continuar próxima semanticamente e ficar
factualmente errada. RAG também não garante atualidade ou precisão apenas por recuperar um trecho:
a base pode estar antiga, a busca pode trazer evidência inadequada e a geração pode interpretá-la mal.

## O projeto do módulo

[db.py](../mba-ia-cache/db.py) armazena `input_text`, `response_json` e embedding em
`ai_response_cache`. Não há ingestão de documentos, chunking, citações ou montagem de prompt
com trechos recuperados. O conteúdo devolvido no hit é uma análise de ticket, não evidência
para uma nova geração.

## Pergunta de revisão

Se a política de cancelamento foi atualizada na base de conhecimento, o que precisa acontecer
com respostas já cacheadas? Recalcular apenas o embedding da pergunta resolveria o problema?
