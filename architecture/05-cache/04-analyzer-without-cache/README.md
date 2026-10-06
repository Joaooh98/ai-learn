# Aula 04 — Analisador sem cache

> Curso: **Cache** · Duração: `07:11`

## Material e foco da aula

Há dez prints do analisador em FastAPI, do prompt e de requisições ao modelo. A versão da aula
chama o modelo em toda requisição; [o endpoint](06.png) e [a segunda chamada](10.png) registram
essa linha de base. O [projeto compartilhado](../mba-ia-cache/README.md) é uma versão posterior
com as camadas integradas, não uma cópia isolada desta etapa.

## O caso de uso observado

`POST /tickets/analyze` recebe uma mensagem de suporte e retorna análise estruturada:

```json
{
  "category": "billing",
  "confidence": 0.95,
  "reason": "A mensagem descreve uma dúvida sobre cobrança."
}
```

Esse JSON ilustra o contrato, não valores que o modelo sempre retornará. As categorias previstas
são `billing`, `technical_support`, `account`, `cancellation` e `other`. Os prints mostram
`ChatPromptTemplate`, `init_chat_model` e `with_structured_output(TicketAnalysis)`; LangChain
já aparece nessa etapa.

```text
mensagem → prompt de classificação → modelo de chat → TicketAnalysis → resposta HTTP
```

`source`, `ai_call_number` e `elapsed_ms` tornam visíveis origem, contador e tempo medido
na aplicação. Repetir a mensagem nesta versão incrementa o contador novamente.

## Complemento de estudo: medir uma linha de base útil

Compare o mesmo conjunto de entradas, prompt, modelo e regras. Registre latência mediana e p95,
erros, consumo real de tokens e qualidade da classificação. Um único tempo no print não
representa a distribuição de latência, e contar chamadas não calcula o custo financeiro.

Temperatura zero reduz uma fonte de variação, mas não garante que inferências repetidas sempre
serão idênticas. Cache de resposta fixa uma saída já gerada.

Saída estruturada valida formato e tipos conforme o schema, não a verdade da análise.
O campo `confidence: float` do exemplo não impõe o intervalo de 0 a 1, embora o prompt o peça;
restrições como `Field(ge=0, le=1)` seriam um complemento. [Referências: saída estruturada
no LangChain](https://docs.langchain.com/oss/python/langchain/models#structured-output)
e [restrições de campos no Pydantic](https://pydantic.dev/docs/validation/latest/concepts/fields/#field-constraints).

## Leitura do código consolidado

A inferência permanece em `chain.invoke({"message": request.message})` de
[main.py](../mba-ia-cache/main.py). No código atual ela só ocorre depois dos misses exato e
semântico. Para estudar a baseline, compare o bloco de inferência com os prints; uma chamada
ao endpoint atual não executa automaticamente o fluxo sem cache.

## Pergunta de revisão

Como demonstrar que a redução de latência veio do cache se o tempo do provedor varia entre
requisições? Quais métricas precisam acompanhar o número de chamadas evitadas?
