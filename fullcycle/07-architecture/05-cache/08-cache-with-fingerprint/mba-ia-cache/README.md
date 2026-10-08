# Projeto prático — cache exato com fingerprint

Snapshot isolado do código mostrado na aula 08. Esta etapa mantém o cache-aside da aula 06 e
passa a construir a chave com a mensagem normalizada e três versões de contexto.

## Fluxo implementado

```text
mensagem + prompt_version + rules_version + model_capability
                             │
                             ▼
                 JSON canônico → SHA-256 → CACHE
                                             ├── hit  → resposta salva
                                             └── miss → modelo → salvar
```

O fingerprint torna a identidade do resultado explícita. `PUT /config` altera os rótulos em
memória para demonstrar a mudança de chave; ele não reconfigura o prompt nem troca o modelo já
instanciado. Voltar ao fingerprint anterior reencontra a entrada antiga, pois a mudança de versão
faz invalidação lógica e não apaga o dicionário.

Esta etapa ainda não possui embeddings, busca semântica ou banco de dados.

## Arquivos

| Arquivo | Papel |
|---|---|
| [main.py](main.py) | Aplicação monolítica transcrita dos prints |
| [test.http](test.http) | Miss, hit, mudança de versão, novo miss e retorno à entrada antiga |
| [requirements.txt](requirements.txt) | Dependências mínimas do exemplo |
| [.env.example](.env.example) | Chave do provedor, modelo e versões sem credenciais reais |

## Preparar para executar depois

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# preencher OPENAI_API_KEY no .env
python main.py
```

Com o processo ativo, execute [test.http](test.http) na ordem. Os valores esperados de `source`
são `ai_model`, `exact_cache`, `ai_model` e `exact_cache`. O contador de IA deve terminar em `2`.

## Fidelidade aos registros da aula

Os 21 PNGs mostram `main.py`, o fingerprint, `GET/PUT /config`, o roteiro HTTP e as respostas.
Esses elementos foram transcritos para este snapshot. Os prints mostram somente os nomes de
`requirements.txt`, `.env.example` e `.gitignore`; o conteúdo desses arquivos é a preparação
mínima inferida para permitir a execução futura.
