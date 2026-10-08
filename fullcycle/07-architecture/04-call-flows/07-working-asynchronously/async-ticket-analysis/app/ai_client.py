"""Cliente de IA com fluxos síncrono, streaming e análise completa."""

import json
import os
from collections.abc import Iterator

from openai import OpenAI

from .schemas import FullTicketAnalysis, TicketAnalysis

client = OpenAI()
MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

SYSTEM_PROMPT = (
    "Você é um assistente que analisa tickets de suporte. "
    "Responda SEMPRE em JSON válido, sem texto extra, com exatamente estas chaves: "
    '"category" (ex: billing, technical, account), '
    '"priority" (low, medium ou high) e '
    '"summary" (resumo curto do problema em português).'
)

FULL_SYSTEM_PROMPT = (
    "Você é um assistente que analisa tickets de suporte. "
    "Responda SEMPRE em JSON válido, sem texto extra, com exatamente estas chaves: "
    '"category" (ex: billing, technical, account), '
    '"priority" (low, medium ou high), '
    '"summary" (resumo curto do problema em português) e '
    '"recommended_action" (ação recomendada em português).'
)

EXPLAIN_SYSTEM_PROMPT = (
    "Você é um assistente de suporte. Explique, em texto corrido e em português, "
    "o que o cliente está relatando e qual a recomendação inicial de tratamento. "
    "Escreva de forma progressiva, em algumas frases curtas. Não use JSON."
)


def analyze_ticket(message: str) -> TicketAnalysis:
    completion = client.chat.completions.create(
        model=MODEL,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": message},
        ],
    )
    data = json.loads(completion.choices[0].message.content or "")
    return TicketAnalysis(**data)


def full_analysis(message: str) -> FullTicketAnalysis:
    completion = client.chat.completions.create(
        model=MODEL,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": FULL_SYSTEM_PROMPT},
            {"role": "user", "content": message},
        ],
    )
    data = json.loads(completion.choices[0].message.content or "")
    return FullTicketAnalysis(**data)


def explain_ticket(message: str) -> Iterator[str]:
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
