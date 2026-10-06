# Projeto prático — cache exato com cache-aside

Snapshot executável do código mostrado na aula 06. Esta etapa evolui o analisador da aula 04 com
um cache local indexado pelo SHA-256 do texto normalizado.

## Fluxo implementado

```text
mensagem → normalizar → SHA-256 → CACHE
                                  ├── hit  → resposta salva
                                  └── miss → modelo → salvar → resposta
```

`normalize_text()` remove espaços das extremidades, transforma sequências de espaços em um único
espaço e converte o texto para minúsculas. `build_cache_key()` calcula o SHA-256 dessa string.
O dicionário `CACHE` guarda o `model_dump()` da análise.

O campo `source` torna cada caminho observável:

- `ai_model`: cache miss; a chain foi chamada e `ai_call_count` aumentou.
- `exact_cache`: cache hit; a resposta foi reconstruída como `TicketAnalysis` sem chamar a IA.

Não há fingerprint com versões, endpoint `/config`, embeddings, similaridade ou banco nesta etapa.

## Arquivos

| Arquivo | Papel |
|---|---|
| [main.py](main.py) | Aplicação monolítica transcrita dos prints da aula |
| [test.http](test.http) | Miss, hit, equivalência por normalização e novo miss |
| [requirements.txt](requirements.txt) | Dependências mínimas para executar o exemplo |
| [.env.example](.env.example) | Variáveis esperadas, sem credenciais |

A aula ainda mantinha configuração, modelos Pydantic e `log_block` no próprio `main.py`; este
snapshot não antecipa a separação em módulos auxiliares.

## Preparar para executar depois

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# preencher OPENAI_API_KEY no .env
python main.py
```

Execute os blocos de [test.http](test.http) na ordem, no mesmo processo. A primeira requisição
deve retornar `ai_model`; a segunda e a variação apenas de caixa/espaços devem retornar
`exact_cache`. O último texto contém um `a` adicional, portanto produz outra chave e outro miss.

O estado é local e volátil: reiniciar o processo esvazia `CACHE` e zera `ai_call_count`.

## Fidelidade aos prints

As funções, modelos, logs, chaves de resposta e exemplos de requisição vêm dos treze PNGs da
aula. Os prints não exibem o conteúdo completo de `requirements.txt`, `.env.example` ou
`.gitignore`; esses arquivos contêm apenas o mínimo inferido para preparar a execução.
