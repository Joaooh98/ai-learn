import sys
import os
from dotenv import load_dotenv

load_dotenv()

# Application now knows two SDKs: OpenAI and Anthropic
from openai import OpenAI
from anthropic import Anthropic

provider = os.getenv("AI_PROVIDER", "openai").lower()
model = os.getenv("AI_MODEL")

if len(sys.argv) > 1:
    question = " ".join(sys.argv[1:])
else:
    question = "O que é uma AI Gateway e por que ela é importante em aplicações com IA?"

system_prompt = """Você é um arquiteto de software explicando IA para desenvolvedores. Responda de forma didática, prática e objetiva. O tema é AI Gateway. Explique o conceito conectando com problemas reais de aplicações que chamam modelos de IA em produção."""

if provider == "openai":
    # Application knows how to instantiate OpenAI client
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Erro: OPENAI_API_KEY não configurada")
        sys.exit(1)

    if not model:
        model = "gpt-4-mini"

    try:
        client = OpenAI(api_key=api_key)

        # Application knows OpenAI's message format
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ]
        )

        print(f"Provider: {provider}")
        print(f"Modelo: {model}")
        print(f"Pergunta: {question}")
        print(f"Resposta:\n{response.choices[0].message.content}")

    except Exception as e:
        print(f"Erro ao chamar OpenAI: {e}")
        sys.exit(1)

elif provider == "anthropic":
    # Application knows how to instantiate Anthropic client
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("Erro: ANTHROPIC_API_KEY não configurada")
        sys.exit(1)

    if not model:
        model = "claude-3-5-sonnet-20241022"

    try:
        client = Anthropic(api_key=api_key)

        # Application knows Anthropic's different message format
        response = client.messages.create(
            model=model,
            max_tokens=1024,
            system=system_prompt,
            messages=[
                {"role": "user", "content": question}
            ]
        )

        print(f"Provider: {provider}")
        print(f"Modelo: {model}")
        print(f"Pergunta: {question}")
        print(f"Resposta:\n{response.content[0].text}")

    except Exception as e:
        print(f"Erro ao chamar Anthropic: {e}")
        sys.exit(1)

else:
    print(f"Erro: Provider inválido '{provider}'. Use 'openai' ou 'anthropic'")
    sys.exit(1)
