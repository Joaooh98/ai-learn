import json
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

MODEL = os.environ.get("AI_GATEWAY_MODEL", "support-ticket-classifier")
ALLOWED_CATEGORIES = {"billing", "technical", "account", "other"}
DEFAULT_MESSAGE = "Fui cobrado duas vezes na minha assinatura e quero resolver isso."

SYSTEM_PROMPT = (
    "Voce e um classificador de tickets de suporte. "
    "Responda ESTRITAMENTE em JSON valido, sem texto fora do JSON, "
    "SEM blocos de codigo markdown e SEM crases. "
    "Responda apenas com o objeto JSON puro, exatamente neste formato: "
    '{"category":"billing|technical|account|other","reason":"explicacao curta"}. '
    "category deve ser uma de: billing, technical, account, other."
)


def contrato_quebrado(raw: str) -> str | None:
    if not isinstance(raw, str) or not raw.strip():
        return "a resposta veio vazia."

    if raw.lstrip().startswith("```"):
        return "nao e JSON puro - veio embrulhada em markdown/crases (```)."

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        return f"nao e JSON valido ({exc.msg})."

    if not isinstance(data, dict):
        return "nao e um objeto JSON."
    if "category" not in data:
        return "falta o campo obrigatorio 'category'."
    if data["category"] not in ALLOWED_CATEGORIES:
        return f"categoria '{data['category']}' nao e permitida."

    return None


def main() -> None:
    client = OpenAI(
        base_url="http://localhost:4000",
        api_key=os.environ["LITELLM_MASTER_KEY"],
    )

    message = " ".join(sys.argv[1:]).strip() or DEFAULT_MESSAGE

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": message},
        ],
    )

    raw = response.choices[0].message.content or ""
    erro = contrato_quebrado(raw)

    print(f"Modelo interno: {MODEL}")
    print(f"Mensagem:       {message}")
    print()
    print("Resposta crua do modelo:")
    print(raw)
    print()

    if erro:
        print(f"QUEBROU: {erro}")
        print()
        print("O fallback respondeu (HTTP 200), mas a resposta nao serve para o fluxo.")
        return

    data = json.loads(raw)
    print("Resposta VALIDA para o fluxo:")
    print(f"  Categoria: {data['category']}")
    print(f"  Motivo:    {data.get('reason', '')}")


if __name__ == "__main__":
    main()
