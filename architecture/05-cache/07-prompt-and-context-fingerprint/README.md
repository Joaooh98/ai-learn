# Aula 07 — Fingerprint de prompt e contexto

> Curso: **Cache** · Duração: `04:44`

## Material e foco da aula

Os quatro prints mostram por que a mensagem sozinha não identifica uma execução.
[O segundo](02.png) conecta prompt, regras, modelo e contexto; [o terceiro](03.png) apresenta
`PromptVersion + RulesVersion + ModelCapability + NormalizedText`.

## Conceito

Fingerprint é uma representação determinística dos fatores que definem se uma resposta pode
ser reutilizada. O hash transforma essa representação em chave compacta; não verifica se
os fatores escolhidos são suficientes.

```text
texto + contrato + contexto + escopo → representação estável → hash → chave
```

O exemplo implementa quatro campos:

```json
{
  "prompt_version": "prompt_v1",
  "rules_version": "rules_v1",
  "model_capability": "fast_model",
  "normalized_text": "tenho dúvidas sobre cobrança"
}
```

Mudar uma versão muda a chave mesmo com texto igual. Isso impede reutilizar análise sob outro
conjunto declarado de regras. A aula amplia o cache exato; não o transforma em cache semântico.

## Complemento de estudo: o que precisa entrar no contrato

Conforme o caso de uso, inclua modelo e revisão, parâmetros relevantes, system prompt, schema
de saída, versão dos dados recuperados, ferramentas disponíveis, idioma, tenant e permissões.
Esses itens podem ser representados por versões confiáveis, desde que mudem quando o
comportamento muda. Fingerprint é uma decisão sobre **equivalência da execução**.

`model_capability="fast_model"` é um rótulo do exemplo, não o identificador efetivo do modelo.
Trocar `OPENAI_MODEL` sem alterar uma versão de compatibilidade permite reutilizar registros
semânticos antigos. Mudar o prompt real sem atualizar `prompt_version` também deixa a
invalidação incompleta.

Ordenar as chaves do JSON estabiliza a serialização de um dicionário construído da mesma forma;
não equivale a canonicalização universal entre linguagens e formatos. [Referência: `json.dumps`
e `sort_keys`](https://docs.python.org/3/library/json.html#json.dumps).

## Normalização exige cuidado

Remover caixa, pontuação ou espaços pode fundir entradas que deveriam produzir respostas
diferentes. Cache exato com fingerprint ainda pode servir resposta errada por normalização
excessiva ou contexto ausente. Ele evita aproximação vetorial, mas não elimina todos os falsos hits.

Tenant e autorização devem ser filtros obrigatórios de escopo quando necessários, não apenas
palavras embutidas no texto. Hash também não criptografa nem torna anônimo o conteúdo que
permanece armazenado.

## Exercício

Monte o fingerprint para um classificador multilíngue que consulta política por cliente.
Quais campos mudam se a política for atualizada ou a permissão do usuário revogada?
