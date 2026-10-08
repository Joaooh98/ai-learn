"""Cliente de IA com fluxo síncrono e fluxo via streaming."""

import json
import os
from collections.abc import Iterator

from openai import OpenAI

from .schemas import TicketAnalysis

client = OpenAI()
MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

SYSTEM_PROMPT = (
    "Você é um assistente que analisa tickets de suporte. "
    "Responda SEMPRE em JSON válido, sem texto extra, com exatamente estas chaves: "
    '"category" (ex: billing, technical, account), '
    '"priority" (low, medium ou high) e '
    '"summary" (resumo curto do problema em português).'
)

EXPLAIN_SYSTEM_PROMPT = (
    "Você é um assistente de suporte. Explique, em texto corrido e em português, "
    "o que o cliente está relatando e qual a recomendação inicial de tratamento. "
    "Escreva de forma progressiva, em algumas frases curtas. Não use JSON."
)


def analyze_ticket(message: str) -> TicketAnalysis:
    """Chama a IA de forma síncrona e devolve a análise já validada."""

    completion = client.chat.completions.create(
        model=MODEL,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": message},
        ],
    )

    raw = completion.choices[0].message.content or ""
    data = json.loads(raw)
    return TicketAnalysis(**data)


def explain_ticket(message: str) -> Iterator[str]:
    """Chama a IA com streaming e devolve pedaços de texto conforme chegam."""

    stream = client.chat.completions.create(
        model=MODEL,
        stream=True,
        messages=[
            {"role": "system", "content": EXPLAIN_SYSTEM_PROMPT},
            {"role": "user", "content": message},
        ],
    )

    try:
        for chunk in stream:
            delta = chunk.choices[0].delta.content
            if delta:
                yield delta
    except Exception:
        yield "\n[erro ao gerar o restante da resposta]"
