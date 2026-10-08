# Projeto prático — analisador sem cache

Snapshot executável do código mostrado na aula 04. O endpoint classifica um ticket com saída
estruturada e chama o modelo em **toda** requisição, inclusive quando a mensagem é repetida.

## O que esta etapa implementa

```text
POST /tickets/analyze
        │
        └── prompt → modelo → TicketAnalysis → resposta HTTP
```

- `TicketRequest`, `TicketAnalysis` e `TicketResponse` definem o contrato Pydantic.
- `ChatPromptTemplate` monta as mensagens de sistema e usuário.
- `with_structured_output(TicketAnalysis)` solicita uma resposta no schema esperado.
- `ai_call_count` deixa visível que cada requisição chega ao modelo.
- `elapsed_ms` mede somente o trecho de `chain.invoke`.

Não há cache, normalização, hash, fingerprint, embeddings ou banco nesta etapa.

## Arquivos

| Arquivo | Papel |
|---|---|
| [main.py](main.py) | Aplicação completa exatamente no formato monolítico visto nos prints |
| [test.http](test.http) | Duas requisições iguais para observar o contador subir |
| [requirements.txt](requirements.txt) | Dependências mínimas para executar o código da aula |
| [.env.example](.env.example) | Variáveis esperadas, sem credenciais |

A aula ainda mantinha configuração, modelos Pydantic e logging no próprio `main.py`; por isso
este snapshot não introduz `config.py`, `models.py` ou `log_helpers.py`.

## Preparar para executar depois

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# preencher OPENAI_API_KEY no .env
python main.py
```

O servidor ficará em `http://localhost:8000`. Execute, na ordem, os blocos de
[test.http](test.http). O resultado esperado é `source: "ai_model"` nas duas respostas e
`ai_call_number` passando de `1` para `2`.

## Fidelidade aos prints

O conteúdo funcional de `main.py`, o texto do prompt, o endpoint, os nomes dos campos e a
mensagem usada no teste foram transcritos dos dez PNGs da aula. Como os prints mostram apenas os
nomes de `requirements.txt`, `.env.example` e `.gitignore`, o conteúdo desses três arquivos é a
configuração mínima inferida para deixar o exemplo preparado, sem executar chamadas agora.
