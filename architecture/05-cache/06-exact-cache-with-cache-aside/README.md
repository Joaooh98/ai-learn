# Aula 06 — Cache exato com cache-aside

> Curso: **Cache** · Duração: `04:56`

## Material e foco da aula

Os treze prints mostram cache em memória. A aula **já normaliza o texto** e calcula SHA-256,
como se vê em [03.png](03.png). As aulas 07 e 08 acrescentam contexto de execução à chave.

## Fluxo observado

```text
mensagem → normalização → SHA-256 → consulta CACHE
  hit  → reconstrói TicketAnalysis → retorna source=exact_cache
  miss → chain.invoke → incrementa contador → grava análise → retorna source=ai_model
```

A normalização usa minúsculas, remoção de espaços nas extremidades e colapso de sequências de
espaços. A igualdade é exata sobre essa representação. Uma transformação considerada irrelevante
pode preservar o hit; reformular a mensagem ou mudar pontuação ainda pode gerar outra chave.

Exemplo ilustrativo:

```text
"  Tenho DÚVIDAS   sobre cobrança  " → "tenho dúvidas sobre cobrança"
"tenho dúvidas sobre cobrança"    → "tenho dúvidas sobre cobrança"
"Preciso entender minha fatura"   → outro texto normalizado → outra chave
```

## Complemento de estudo: limites do cache exato

Chave derivada só da mensagem ignora mudanças de prompt, regras, modelo e dados. A mensagem
pode continuar produzindo a mesma chave quando a análise correta já mudou. Essa é a motivação
do fingerprint contextual da aula 07.

Normalizar é decisão de domínio: caixa, espaços e pontuação podem alterar código, senhas,
identificadores ou citações. Teste as transformações escolhidas. Hash preserva a identidade
fornecida; não recupera informação descartada nem avalia significado.

O cache em memória tem quatro limites observáveis:

- Reiniciar ou recarregar o processo apaga os dados.
- Não há compartilhamento entre processos ou réplicas.
- Não há TTL, limite de tamanho ou política de descarte.
- Dois misses concorrentes podem executar a mesma inferência.

Caches locais e sincronização entre instâncias também aparecem na
[referência de Cache-Aside](https://learn.microsoft.com/en-us/azure/architecture/patterns/cache-aside#problems-and-considerations).

## Conferência no snapshot

O [projeto desta aula](mba-ia-cache/README.md) mantém `normalize_text()`, `build_cache_key()` e
`CACHE` em um único [main.py](mba-ia-cache/main.py), como aparece nos prints. O roteiro em
[test.http](mba-ia-cache/test.http) separa miss, hit, equivalência por normalização e uma mensagem
que produz nova chave. Fingerprint contextual e cache semântico ainda não fazem parte desta etapa.

## Exercício

Explique por que trocar `rules_v1` por `rules_v2` deveria causar miss com a mesma mensagem.
Depois descreva um caso em que converter o texto para minúsculas mudaria uma resposta legítima.
