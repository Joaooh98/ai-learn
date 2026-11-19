# Exercício proposto: atendimento com IA e resposta auditável

[Índice da revisão](README.md) · Criado em **19/11/2026**.
Este é um novo exercício de integração; não descreve uma aplicação já entregue pelo curso.

## Cenário

Um usuário pergunta sobre cobrança e pode solicitar abertura de um ticket. O sistema recupera
políticas válidas, gera uma explicação e só cria o ticket quando houver autorização na
camada de aplicação. O modelo pode propor a ação, mas não concede suas próprias permissões.

## Contratos a fechar

| Responsabilidade | Decisão proposta para o exercício | Evidência a produzir |
|---|---|---|
| Identidade | Tenant e permissões vêm do contexto autenticado | Tentativa de troca pelo texto não amplia acesso |
| Retrieval | Só usa documentos autorizados e vigentes | Documento de outro tenant não chega ao contexto |
| Proveniência | Conhecimento só entra por origem autorizada | Front matter não permite autoconceder confiança |
| Geração | A resposta identifica a evidência usada ou declara insuficiência | Afirmações importantes estão apoiadas nos trechos |
| Cache | Reutilização respeita usuário/escopo e versão das políticas | Alteração de política invalida resultado incompatível |
| Gateway | A rota alternativa atende ao mesmo contrato | Primário e backup comparados no mesmo dataset |
| Fluxo | Interface distingue parcial, final e falha | Desconexão não apresenta texto parcial como concluído |
| Tool | Criar ticket exige permissão e chave de idempotência | Retry autorizado não duplica o efeito |
| Telemetria | Correlação e tempos sem conteúdo integral por padrão | Payload exportado confere com a política de dados |
| Evaluation | Regressões críticas bloqueiam promoção | Bom score médio não encobre falha de autorização |

## Casos que precisam continuar separados

1. Pergunta legítima com documento suficiente: resposta sustentada.
2. Pergunta legítima sem fonte válida: insuficiência/recusa apropriada.
3. Documento adulterado externo: registro do ponto de bloqueio e do efeito observado.
4. Documento legítimo sem acesso para o caller: nenhuma divulgação do conteúdo.
5. Timeout depois de criação de ticket: reconciliação por ID antes de nova tentativa.
6. Resposta incompleta no stream: interface sinaliza falha e impede ação sobre dados parciais.
7. Provider alternativo retorna schema correto com regra errada: falha de qualidade registrada.

## Pacote de evidências

Guarde configuração do experimento, hash do corpus/dataset, revisão dos contratos, versão dos
prompts e do juiz, destinos efetivos e resultados por caso. Registre erros de execução à
parte. Acrescente uma decisão escrita explicando qual risco foi reduzido e o que permanece.

A entrega do exercício é o conjunto de decisões e evidências, não um dashboard bonito ou
uma afirmação genérica de que “os testes passaram”.
