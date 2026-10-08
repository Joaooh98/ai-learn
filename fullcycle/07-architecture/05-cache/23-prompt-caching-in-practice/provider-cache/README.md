# Projeto prático — prompt caching do provider

Snapshot isolado da demonstração da aula 23. A API classifica tickets com uma
instrução estática longa e deixa a OpenAI reaproveitar o processamento desse
prefixo entre chamadas. Ela não mantém cache exato ou semântico na aplicação.

## O que veio das capturas

As 31 imagens da aula mostram o comportamento e a maior parte dos arquivos
[`provider_cache.py`](provider_cache.py) e
[`provider_cache.http`](provider_cache.http):

- `ChatOpenAI` recebe uma `prompt_cache_key` estável;
- `with_structured_output(..., include_raw=True)` preserva a `AIMessage`;
- `usage_metadata.input_token_details.cache_read` informa os tokens lidos do
  cache do provider;
- `ai_calls` aumenta em todas as análises, inclusive quando há hit;
- `GET /health` e `POST /tickets/analyze` são os únicos endpoints;
- alterar qualquer parte do prefixo pode produzir um novo miss.

O trecho inicial do Python não aparece nas capturas. Imports, modelos Pydantic,
nomes padrão das variáveis de ambiente e validação de `confidence` foram
reconstituídos pelo contrato observado nas respostas e pelo padrão dos projetos
anteriores do módulo. `requirements.txt`, `.env.example`, `.gitignore` e este
README são arquivos mínimos de apoio, adicionados para deixar o snapshot pronto.

## Preparar para executar depois

```bash
cd architecture/05-cache/23-prompt-caching-in-practice/provider-cache
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Preencha `OPENAI_API_KEY` no `.env`. Então inicie:

```bash
python provider_cache.py
```

A aplicação usa `http://localhost:8001`. Execute as requisições de
[`provider_cache.http`](provider_cache.http) na ordem em que aparecem. O cache
do provider é best-effort; uma execução futura pode ter números ou hits
diferentes dos prints da aula.

## Como ler o resultado

- `provider_cache_hit`: há tokens de entrada reportados em `cache_read`;
- `cached_tokens`: quantidade reaproveitada no prefixo;
- `input_tokens` e `output_tokens`: uso total normalizado pelo LangChain;
- `ai_calls`: comprova que cada request chamou o modelo;
- `result`: nova classificação gerada para a mensagem atual.

Um hit reduz o processamento cobrado para parte da entrada. Ele não devolve uma
resposta antiga e não substitui o cache exato ou semântico estudado antes.
