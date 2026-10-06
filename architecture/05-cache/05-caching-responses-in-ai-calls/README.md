# Aula 05 — Cache de resposta em chamadas de IA

> Curso: **Cache** · Duração: `03:57`

## Material e foco da aula

Os três prints comparam classificação sem cache com reutilização da saída final.
[O primeiro](01.png) destaca o objeto de resposta; [o segundo](02.png) organiza hit e miss;
[o terceiro](03.png) antecipa fingerprint com versão do prompt e regras.

## O que é armazenado

O cache de resposta guarda o resultado do processamento: no analisador, `category`,
`confidence` e `reason`. A aplicação procura esse objeto antes de chamar novamente o modelo.

```text
identidade da entrada + contrato de execução → chave → análise já gerada
```

No cache exato do [projeto](../mba-ia-cache/main.py), a gravação é
`CACHE[key] = result.model_dump()`. O dicionário guarda a análise, e a API monta metadados
novos ao retorná-la. Assim, tempo e origem descrevem a requisição atual.

## Complemento de estudo: resposta completa e equivalência

Não basta verificar se duas entradas receberiam a mesma **categoria**. Como o objeto inclui
motivo e confiança, reutilizar tudo pode devolver uma justificativa sobre uma entidade ausente
do ticket novo. A política precisa avaliar equivalência para todos os campos servidos.

| Saída reutilizada | Exemplo de risco |
| --- | --- |
| Categoria | Encaminhar reunião cancelada ao fluxo de cancelamento de assinatura |
| Motivo | Mencionar cobrança duplicada quando o ticket trata de outro problema |
| Confiança | Reutilizar estimativa produzida para outra entrada |

`confidence` é a estimativa emitida pelo classificador; não é a similaridade do embedding
e não se transforma automaticamente em probabilidade calibrada de acerto.

Só grave resultados válidos e adequados à reutilização. Erros, recusas e respostas parciais
precisam de política própria. Hit de resposta evita inferência de chat; hit semântico ainda
pode precisar gerar embedding e consultar o banco.

## Limite em relação a prompt caching

Nesta camada a aplicação devolve uma saída anterior. Prompt caching do provedor reutiliza
processamento de partes da **entrada** durante uma nova chamada ao modelo; são mecanismos
diferentes, retomados nas aulas 20 a 23. [Referência: Prompt Caching](https://developers.openai.com/api/docs/guides/prompt-caching).

## Exercício

Compare armazenar apenas a categoria com armazenar a análise completa. Quais critérios de
qualidade mudam quando o `reason` também é reutilizado?
