import sys
import os
from dotenv import load_dotenv
from litellm import completion

load_dotenv()

provider = os.getenv("AI_PROVIDER", "openai").lower()
model = os.getenv("AI_MODEL")

if len(sys.argv) > 1:
    question = " ".join(sys.argv[1:])
else:
    question = "O que é uma AI Gateway e por que ela é importante em aplicações com IA?"

system_prompt = """Você é um arquiteto de software explicando IA para desenvolvedores. Responda de forma didática, prática e objetiva. O tema é AI Gateway. Explique o conceito conectando com problemas reais de aplicações que chamam modelos de IA em produção."""

# Validate provider and set defaults
valid_providers = ["openai", "anthropic"]
if provider not in valid_providers:
    print(f"Erro: Provider inválido '{provider}'. Use 'openai' ou 'anthropic'")
    sys.exit(1)

# Set default model per provider
if not model:
    if provider == "openai":
        model = "gpt-4-mini"
    elif provider == "anthropic":
        model = "claude-3-5-sonnet-20241022"

# Format model for LiteLLM (add provider prefix if not present)
if "/" not in model:
    model = f"{provider}/{model}"

# Validate corresponding API key
if provider == "openai":
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Erro: OPENAI_API_KEY não configurada")
        sys.exit(1)
elif provider == "anthropic":
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("Erro: ANTHROPIC_API_KEY não configurada")
        sys.exit(1)

try:
    # LiteLLM abstraction: single unified call for all providers
    response = completion(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ],
        temperature=0.7,
        max_tokens=1024
    )

    print(f"Provider: {provider}")
    print(f"Modelo: {model}")
    print(f"Pergunta: {question}")
    print(f"Resposta:\n{response.choices[0].message.content}")

except Exception as e:
    print(f"Erro ao chamar LiteLLM: {e}")
    sys.exit(1)
