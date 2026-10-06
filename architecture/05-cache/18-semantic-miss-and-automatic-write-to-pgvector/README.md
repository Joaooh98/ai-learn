# Aula 18 — Miss semântico e gravação automática no pgvector

> Curso: **Cache** · Duração: `04:26`

## Material disponível e limite de evidência

Esta pasta não tem prints próprios. O título indica o foco em escrita após miss, e o
[projeto consolidado](../mba-ia-cache/README.md) contém esse fluxo. As notas abaixo explicam
o comportamento verificável no código atual; não reconstituem uma gravação da aula ausente.

## Caminho observado no código

Em [main.py](../mba-ia-cache/main.py), `analyze_ticket()` reutiliza o embedding gerado na
busca e chama `save_ai_result_to_semantic_cache()` após a inferência:

```text
miss exato → embedding + consulta → miss semântico
  → chain.invoke → TicketAnalysis → incrementa contador
  → CACHE[key] = análise
  → INSERT no pgvector com o embedding já calculado
  → retorna análise e status da escrita
```

Não é necessário gerar o embedding outra vez para a mesma entrada normalizada. A escrita
salva mensagem original, texto normalizado, versões, análise completa e vetor.

## Resultado e falha de gravação

`semantic_cache_write` informa `attempted`, `saved`, `reason`, `item_id` e dimensão:

| Situação | Comportamento atual |
| --- | --- |
| Hit exato ou semântico | Não cria nova entrada semântica |
| Miss com inferência e escrita bem-sucedidas | Retorna análise e `saved=true` |
| Inferência funciona, INSERT falha | Retorna análise e `saved=false`; cache exato já foi preenchido |
| Embedding ou leitura SQL falha | Não alcança essa captura de erro de escrita |
| Inferência falha | Não grava a análise no fluxo normal |

Memória e PostgreSQL não formam uma transação única. Uma gravação pode funcionar e a outra
falhar; o objeto de resposta torna essa diferença visível.

## Complemento de estudo: crescimento não é aprendizado do modelo

Inserir novas entradas aquece a base do cache. Isso não treina o embedding nem o classificador,
e não garante aumento contínuo de hits: tráfego, versões, expiração e qualidade podem mudar.

A tabela usa UUID novo por inserção e não tem unicidade por fingerprint. Misses simultâneos ou
inserções manuais podem gerar duplicatas. Uma evolução exige definir idempotência, política de
atualização e retenção. `INSERT ... ON CONFLICT` só resolve conflitos quando existe a restrição
ou chave adequada. [Referência: INSERT no PostgreSQL](https://www.postgresql.org/docs/current/sql-insert.html).

Outros cuidados de projeto:

- Admitir somente respostas que atendam contrato e política de qualidade.
- Registrar modelo/versão de embedding e escopo necessários para buscas futuras.
- Definir TTL ou expiração lógica também na consulta semântica.
- Distinguir falhas de leitura, inferência e escrita nas métricas.
- Escolher limpeza ou atualização para dados e respostas desatualizados.

## Exercício

Uma resposta foi devolvida com `saved=false`. Por que a repetição imediata pode virar hit
exato, mas deixar de encontrar esse resultado após reiniciar a API?
