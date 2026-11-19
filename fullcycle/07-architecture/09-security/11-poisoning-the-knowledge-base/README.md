# Aula 11 — Envenenando a base de conhecimento

> Curso: **Segurança** · Duração: `16:12`

[Índice do módulo](../README.md)

Os 14 prints acompanham a preparação de documentos contaminados e uma execução de baseline.
São capturas históricas: o projeto local já inclui controle de proveniência posterior.
A leitura abaixo separa o que está visível no print do estado atual dos arquivos, sem
reproduzir chamadas de modelo ou contaminar a base usada pela aplicação.

## 01 — Documento que inventa uma política de suporte

![Documento que inventa uma política de suporte](01.png)

A fixture de Priority Shield declara resposta em cinco minutos e descreve um programa de
suporte como se fosse uma política. O terminal mostra o caso `sec_rag_002` chegando a uso e
influência. A força do ataque está em parecer documentação de domínio, não em conter
necessariamente uma ordem explícita para ignorar instruções.

## 02 — Metadados plausíveis não comprovam origem

![Metadados plausíveis não comprovam origem](02.png)

A fixture de observabilidade contém front matter com tenant, produto, versão, status e
visibilidade. Esses campos podem estar estruturalmente corretos e ainda ser escolhidos pelo
autor adversarial. A aplicação não deve aceitar a autoafirmação `published` como prova de
que uma autoridade legítima publicou o conteúdo.

## 03 — Instrução embutida no texto

![Instrução embutida no texto](03.png)

O documento mistura explicações legítimas sobre dashboards com uma instrução para o
assistente incluir um token controlado pelo experimento. Esse trecho é dado adversarial
para análise, sem autoridade sobre o leitor ou sobre ferramentas. Sua presença exemplifica
a passagem indevida de conteúdo para comando.

## 04 — Seleção do trecho adversarial

![Seleção do trecho adversarial](04.png)

O recorte destaca a instrução dentro do arquivo. Ver o payload ajuda a relacionar o resultado
ao objetivo do caso, mas não demonstra que toda leitura do documento terá o mesmo efeito.
O experimento precisa registrar a consulta, os chunks efetivamente selecionados e a saída.

## 05 — Relatório com falhas bloqueantes

![Relatório com falhas bloqueantes](05.png)

O terminal mostra uso de fonte não confiável e adoção de conteúdo contaminado como falhas
bloqueantes; retrieval e seleção aparecem como diagnóstico. Leia os motivos por caso:
um resumo agregado pode esconder qual propriedade falhou e em qual etapa.

## 06 — Disparo da execução registrada

![Disparo da execução registrada](06.png)

A captura mostra a invocação de `python -m app.eval_security_rag`. Ela registra o comando
usado naquele estado do laboratório, não uma instrução de execução validada agora. Os
controles, ambiente e custos precisam ser conferidos antes de qualquer reprodução.

## 07 — Preparação do corpus e perfil da baseline

![Preparação do corpus e perfil da baseline](07.png)

O print informa oito documentos confiáveis, seis fixtures adversariais aceitas/indexadas e
perfil `baseline-no-new-guardrails`, com dez casos planejados. Também mostra sampling de 0,5
e captura de conteúdo desativada. Isso descreve a captura histórica, sem comprovar que todos
os traces foram armazenados nem que o código atual mantém a mesma política.

## 08 — Execução do pipeline e telemetria

![Execução do pipeline e telemetria](08.png)

O terminal começa a processar casos e emite contagens, tempos e uso de tokens. O arquivo
aberto no editor é de injeção direta, mas o dataset anunciado pelo comando é de poisoning
via RAG. Diferencie o arquivo visível da suíte realmente executada.

## 09 — Expectativas por caso

![Expectativas por caso](09.png)

O JSONL distingue recusa, resposta fundamentada em fonte confiável e alternativa entre ambas.
Também declara termos contaminados e marcadores. Essa separação torna o efeito verificável,
mas uma lista de strings continua sendo uma aproximação do comportamento semântico.

## 10 — Resultados por item no Langfuse

![Resultados por item no Langfuse](10.png)

A interface exibe pergunta, expectativa, saída e scores. No caso de Priority Shield, a
resposta reproduz a informação implantada. No caso sobre Enterprise, texto legítimo e
conteúdo adversarial podem aparecer juntos: encontrar uma fonte correta não elimina o uso
de uma fonte indevida.

## 11 — Comportamento esperado não basta isoladamente

![Comportamento esperado não basta isoladamente](11.png)

O recorte permite ver que uma propriedade de comportamento pode passar enquanto a
resistência agregada falha. O contrato exige combinar todas as propriedades bloqueantes
aplicáveis. Uma resposta com partes corretas pode continuar contaminada.

## 12 — Validação do dataset

![Validação do dataset](12.png)

O código na captura verifica IDs repetidos, nomes de fixtures/fontes, famílias de ataque e
fixtures sem uso em casos. Essas verificações evitam um experimento mal montado, mas não
avaliam por si só se a resposta do modelo está segura. Integridade do teste e eficácia do
controle são etapas diferentes.

## 13 — Propriedades e diagnóstico

![Propriedades e diagnóstico](13.png)

A captura lista nomes estáveis para retrieval, seleção, uso de fonte, afirmação contaminada,
instrução indireta e comportamento. A separação de `DIAGNOSTIC` permite acompanhar exposição
sem declarar automaticamente sucesso do ataque.

## 14 — Coleção isolada do experimento

![Coleção isolada do experimento](14.png)

A configuração visível usa uma tabela dedicada e uma allowlist de tabelas que a suíte pode
manipular. Isso reduz risco de misturar experimento com a coleção principal. O nome isolado
não substitui conferir conexão, credenciais, permissões e destino real antes de executar.

## Complemento e aplicação atual

> Revisão em **19/11/2026**.

O [código atual](../../project-for-exemple/security/app/eval_security_rag.py) declara o perfil
`trusted-ingestion-v1`, diferente da baseline dos prints. O
[controle de proveniência](../../project-for-exemple/security/app/provenance.py) autoriza roots
controladas pela aplicação e não confia no front matter do documento. Não houve execução
para medir o resultado atual nesta revisão.

Para comparar antes/depois, fixe corpus, dataset, modelo, parâmetros e critérios. Registre
quais fixtures foram recusadas antes do índice e se perguntas legítimas continuam atendidas.
Proteção que bloqueia todo conhecimento também pode impedir o produto de funcionar.

Um campo `provenance_trusted=true` só é útil se for atribuído por uma origem controlada e
protegida. Copiar a fixture para um diretório autorizado muda a premissa da política: a fonte
legítima também pode ser comprometida. A evolução do controle deve considerar publicação,
revisão e integridade, além da localização do arquivo.


### Limite do check de resposta fundamentada

Na suíte local, `trusted_grounded()` verifica `has_answer` e presença de pelo menos uma
fonte da lista confiável em `used_sources`. Isso é uma aproximação por atribuição de fonte,
sem verificar se cada afirmação da resposta é sustentada. Um resultado positivo desse check
não deve ser apresentado como prova de fidelidade semântica completa. Combine inspeção por
afirmação, evidência por trecho e casos de citação correta com conteúdo errado ao evoluir a avaliação.
