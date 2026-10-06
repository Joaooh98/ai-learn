# Registro da revisão de arquitetura

Revisão técnica e editorial em **1 de outubro de 2026**. O trabalho começou pelo aprofundamento
do módulo de cache e depois percorreu os quatro módulos de `architecture`: **66 aulas**, notas
de apoio e documentação dos exemplos. O objetivo é tornar o material fiel às evidências locais
e útil para estudo e decisões de projeto.

## Critérios usados

- Confrontar notas com imagens existentes e, nos exemplos, com código/configuração disponíveis.
- Distinguir o que foi observado na aula, o estado final do projeto e complementos de estudo.
- Conferir regras atuais de APIs e bibliotecas em fontes oficiais, vinculadas nas notas.
- Preservar imagens, durações e exemplos históricos; corrigir interpretações no texto.
- Organizar índices e referências locais para permitir leitura por trilha ou por tema.

## Principais correções e aprofundamentos

| Módulo | Problemas encontrados | Resultado da revisão |
|---|---|---|
| [Acoplamento](02-coupling-and-application-health/README.md) | Direção das dependências, contagem inconsistente de setas, instabilidade confundida com volatilidade, gráfico tratado como certificado de saúde | Fórmulas e convenções explicitadas; correções junto aos prints; limites de análise estática e perguntas de estudo |
| [AI Gateway](03-ai-gateway/README.md) | Promessas amplas de compatibilidade, política de retry confundida com defaults de SDK, modelos/arquivos históricos descritos como atuais | Distinção entre contrato, transporte e capacidade; limites de timeout/retry/fallback e execução documentados |
| [Fluxos de chamada](04-call-flows/README.md) | Streaming confundido com SSE, `async` confundido com trabalho durável, respostas/status descritos além do que o demo oferece | Transporte e contrato reais identificados; limites de tarefas em memória, recuperação e erros no stream |
| [Cache](05-cache/README.md) | Avisos incorretos de falta de material, ausência de critérios de validade, similaridade interpretada como certeza, etapas antigas misturadas ao projeto final | 23 aulas aprofundadas; cascata confrontada com código; custo, calibração, invalidação e APIs de provider explicados |

No cache, a revisão também identifica que hit semântico não promove resposta para o cache exato,
`PUT /config` muda rótulos e não a implementação do prompt/modelo, o índice criado é B-tree,
`created_at` não implementa TTL e a dimensão configurada não é passada ao gerador de embeddings.
O [README do projeto](05-cache/mba-ia-cache/README.md) registra esses comportamentos e um roteiro
manual que não promete hits semânticos determinísticos.

A comparação de providers separa Gemini Interactions de GenerateContent, cache implícito de
objeto explícito e controles OpenAI por geração de modelo. Os prints da aula 23 são usados como
evidência de tokens reutilizados e chamadas novas; a latência de poucas requisições não é tratada
como benchmark universal. Veja [aula 22](05-cache/22-how-openai-anthropic-and-gemini-handle-prompt-caching/README.md)
e [aula 23](05-cache/23-prompt-caching-in-practice/README.md).

## Lacunas do acervo

- **Acoplamento, aulas 05–18:** faltam os materiais originais locais. As notas identificam essa
  condição e oferecem perguntas editoriais, sem afirmar resultados de refatorações não observadas.
- **Cache, aulas 18–19:** não há prints próprios. O projeto final permite estudar gravação e
  uso de LangChain, mas não comprova a sequência exata dessas aulas.
- **Prompt caching, aula 23:** existem 31 prints; os fontes `provider_cache.py` e
  `provider_cache.http` vistos neles não estão no repositório.

Essas lacunas exigem o material original para reconstruir a aula. Os complementos existentes
servem para estudar os conceitos enquanto o acervo permanece incompleto.

## Limites dos exemplos executáveis

A revisão documenta o estado dos exemplos sem transformar demos em serviços de produção.
Algumas dependências usam versões abertas/tags móveis; determinados defaults históricos podem
exigir override por ambiente. Os READMEs explicam como conferir a configuração efetiva.

No analisador de cache faltam expiração, isolamento por cliente, política de qualidade para
escrita e coordenação entre workers. No processamento assíncrono, tarefas/dicionários locais
não garantem recuperação após reinício. Nos gateways, fallback configurado precisa ser
observado em logs de execução e validado quanto à qualidade do modelo alternativo.

## Verificação da revisão

A validação documental cobre destinos de links e imagens locais, fechamento de blocos de código,
exemplos JSON e whitespace do diff. Também confere que os PNGs previamente adicionados pelo usuário
continuam idênticos aos arquivos staged. As fontes e snippets são confrontados com as referências
e os arquivos locais; essa verificação não equivale a uma execução integrada dos demos.

Não foram realizadas inferências pagas nem iniciados serviços externos para validar estas notas.
Os roteiros de execução permanecem disponíveis nos projetos para uma reprodução com ambiente
e credenciais apropriados.
