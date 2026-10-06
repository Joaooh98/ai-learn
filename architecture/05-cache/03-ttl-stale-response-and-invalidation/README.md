# Aula 03 — TTL, resposta stale e invalidação

> Curso: **Cache** · Duração: `03:47`

## Material e foco da aula

Os três prints relacionam tempo de vida, resposta desatualizada e invalidação.
[O problema de uma resposta stale](02.png) usa mudanças de regra, prompt e contexto do ticket;
[o último print](03.png) distingue TTL, remoção manual e versão/fingerprint.

## Conceitos

- **TTL (*time to live*)**: prazo de reutilização definido para uma entrada. A política deve
  especificar se começa na escrita e se acessos o renovam.
- **Resposta stale**: resultado que já não representa a fonte, as regras ou o contexto atuais.
  Pode ficar desatualizado antes de o TTL vencer.
- **Invalidação**: deixar de aceitar uma entrada após uma mudança relevante, por remoção,
  atualização ou mudança da identidade usada na consulta.

```text
09:00 → resposta gerada sob rules_v1; TTL ilustrativo de 1 hora
09:05 → regra muda para rules_v2
09:06 → entrada ainda não expirou, mas já não serve sob a regra nova
```

TTL limita por quanto tempo se permite reutilizar; não prova que a resposta está atualizada.
A escolha depende da volatilidade dos dados e do custo de uma resposta incorreta.

## Complemento de estudo: três mecanismos diferentes

| Mecanismo | Efeito | Limite |
| --- | --- | --- |
| Expiração | Recusa entrada depois de um prazo | Mudanças anteriores podem gerar stale |
| Invalidação por evento | Reage a alteração conhecida | Depende da entrega e do processamento do evento |
| Versionamento | Consulta passa a usar outra identidade | Entradas antigas continuam armazenadas |

Quando a origem muda, uma estratégia comum é atualizar a fonte e depois invalidar o cache;
inverter a ordem permite que uma leitura recarregue o valor antigo. [Referência: consistência
no Cache-Aside](https://learn.microsoft.com/en-us/azure/architecture/patterns/cache-aside#problems-and-considerations).

`stale-while-revalidate` é uma política opcional: servir uma entrada antiga por um prazo definido
enquanto outra tarefa atualiza o resultado. Só cabe quando o domínio aceita essa defasagem.
Ela não está implementada neste projeto.

## O que o projeto realmente implementa

Em [main.py](../mba-ia-cache/main.py), mudar `prompt_version` ou `rules_version` altera o
fingerprint; em [db.py](../mba-ia-cache/db.py), essas versões filtram a busca semântica. Isso é
invalidação **lógica**: deixa de consultar o conjunto anterior, sem apagá-lo.

Não há TTL em `CACHE`, campo `expires_at`, filtro de expiração no SQL nem rotina de limpeza.
`created_at` registra a criação; sozinho não faz uma entrada expirar. Voltar para uma versão
anterior pode tornar entradas antigas acessíveis novamente.

## Exercício

Escolha uma política de validade para classificação estável de tickets e outra para resposta
sobre uma cobrança que acabou de mudar de status. Justifique os eventos que invalidam cada uma.
