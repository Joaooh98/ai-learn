# Aula 17 — Integrando cache semântico no endpoint de tickets

> Curso: **Cache** · Duração: `10:12`

## Material e foco da aula

Os 21 prints mostram a integração em `POST /tickets/analyze`. [01.png](01.png) registra
o início da cascata; [05.png](05.png) valida a resposta do candidato; [13.png](13.png) mostra
hit exato; [17.png](17.png) mostra hit semântico. [21.png](21.png) mostra um corte mais alto
levando a chamada do modelo.

## Fluxo do projeto consolidado

Em [main.py](../mba-ia-cache/main.py), `analyze_ticket()`:

1. Constrói fingerprint e chave.
2. Verifica `CACHE`; no hit, retorna sem consultar pgvector.
3. No miss exato, gera embedding e busca até cinco candidatos compatíveis.
4. Avalia o primeiro candidato contra o threshold atual.
5. Tenta reconstruir `TicketAnalysis` a partir de `response_json`.
6. Retorna hit semântico se candidato e contrato forem aceitos; caso contrário, chama o chat.
7. Após inferência, grava cache exato e tenta gravação semântica, detalhada na aula 18.

## Como interpretar a resposta

| Caminho | `source` | `cache.hit` | `semantic_cache.attempted` | `semantic_cache.hit` |
| --- | --- | --- | --- | --- |
| Hit exato | `exact_cache` | `true` | `false` | `false` |
| Hit semântico | `semantic_cache` | `false` | `true` | `true` |
| Modelo de chat | `ai_model` | `false` | `true` | `false` |

`cache.hit=false` pode coexistir com `source=semantic_cache`: o campo descreve a camada
**exata**, não toda a cascata. `ai_call_number` é o contador cumulativo daquele processo,
não consumo de tokens nem quantidade de chamadas de embedding.

## Complemento de estudo: validação não prova equivalência

Se o melhor candidato tem JSON incompatível com `TicketAnalysis`, o código muda a decisão
para rejeição e segue à inferência. Ele não tenta o segundo candidato. JSON compatível
ainda pode ter motivo incorreto, dados antigos ou `confidence` fora da faixa desejada.

Pydantic oferece restrições explícitas para campos numéricos; `float` sozinho não limita
a confiança. [Referência: restrições de campos](https://pydantic.dev/docs/validation/latest/concepts/fields/#field-constraints).
Essa evolução é complementar, não uma validação já presente no exemplo.

## Cenários de verificação

- Mensagem idêntica com mesmo fingerprint: hit exato após geração bem-sucedida.
- Paráfrase elegível: hit semântico somente se score e resposta passarem nas verificações.
- Mudança de versão: candidatos da versão anterior não devem aparecer.
- Threshold acima do score observado: candidato rejeitado e inferência.
- Candidato com JSON inválido: rejeição em vez de servir a análise corrompida.
- Falha de embedding ou banco: documentar que o fluxo atual não tem contingência de leitura.

Os [exemplos HTTP](../mba-ia-cache/test.http) permitem inspeção manual. Candidatos, score e
origem dependem do estado da memória, dos dados persistidos e da configuração: não assuma
que a primeira chamada sempre será miss se a tabela já contém respostas.

## Exercício

Por que elevar o threshold pode não mudar uma resposta que já foi resolvida pelo cache exato?
