# AI Learn

Material de estudo, exercícios e projetos práticos de inteligência artificial.

Este repositório foi separado do antigo `ai` para que conteúdo didático não se misture com
as ferramentas usadas no fluxo de desenvolvimento. O repositório de origem foi mantido intacto.

## Conteúdo

| Pasta | Conteúdo |
|---|---|
| `architecture/` | Material sobre acoplamento e saúde de aplicações |
| `cli-lang/` | Exercício de ingestão e busca semântica com LangChain e PostgreSQL/pgVector |
| `design-docs/` | Módulos do MBA sobre documentação, design e arquitetura |
| `prompt-engineering/` | Exercícios de prompting, agentes, versionamento e avaliação |

Cada projeto ou capítulo declara as próprias dependências. Não existe um ambiente Python
compartilhado na raiz.

## Começar

Entre no módulo desejado e siga o README ou `AGENTS.md` mais próximo. Para os exercícios Python,
crie um ambiente virtual dentro do próprio módulo:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

Nunca versione chaves ou arquivos `.env`; mantenha somente os modelos `.env.example`.

## Origem

Separado em 5 de setembro de 2026 a partir do commit `40d0a93` de `ai`.

O projeto `cli-lang/mba-ia-desafio-ingestao-busca` era um clone local de material do curso. Seu
conteúdo foi incorporado aqui como arquivos normais, sem o repositório Git aninhado. A origem do
template permanece documentada no README do próprio projeto.
