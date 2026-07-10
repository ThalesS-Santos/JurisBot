"""
Módulo de Controle de Custos — JurisBot
========================================
Rastreia tokens e custos da API Gemini por consulta.

Preços (USD por 1 milhão de tokens) — fonte: precos_modelos.md (jun/2026):
  gemini-3-flash-preview:   input $0.50 / output $3.00
  gemini-embedding-001:     input $0.15
"""

# Tabela de preços por modelo de geração (USD / 1M tokens)
PRECOS = {
    # Gemini 3 Series
    "gemini-3-flash-preview": {
        "input":  0.50,
        "output": 3.00,
    },
    "gemini-3-pro-preview": {
        "input":  2.00,
        "output": 12.00,
    },
    # Gemini 2.5 Series
    "gemini-2.5-flash": {
        "input":  0.30,
        "output": 2.50,
    },
    "gemini-2.5-flash-preview-09-2025": {
        "input":  0.30,
        "output": 2.50,
    },
    "gemini-2.5-flash-lite": {
        "input":  0.10,
        "output": 0.40,
    },
    "gemini-2.5-flash-lite-preview-09-2025": {
        "input":  0.10,
        "output": 0.40,
    },
    "gemini-2.5-pro": {
        "input":  1.25,
        "output": 10.00,
    },
    # Gemini 2.0 Series
    "gemini-2.0-flash": {
        "input":  0.10,
        "output": 0.40,
    },
    "gemini-2.0-flash-lite": {
        "input":  0.075,
        "output": 0.30,
    },
}

PRECO_PADRAO = {"input": 0.50, "output": 3.00}

# Embeddings (USD / 1M tokens de entrada)
PRECO_EMBEDDING_1M = 0.15

# Heurística de tokenização para estimativas sem usage_metadata
# (a API de embeddings não retorna contagem de tokens)
_CHARS_POR_TOKEN = 4

COTACAO_BRL = 6  # cotação aproximada USD -> BRL


def estimar_custo_embedding(texto: str) -> float:
    """Estima o custo (USD) de embedar um texto, a ~4 chars/token."""
    tokens_estimados = max(1, len(texto) // _CHARS_POR_TOKEN)
    return (tokens_estimados / 1_000_000) * PRECO_EMBEDDING_1M


def calcular_custo(response, modelo: str) -> dict:
    """
    Recebe a resposta da API Gemini e o nome do modelo.
    Retorna um dicionário com tokens e custo estimado.
    """
    try:
        meta = response.usage_metadata
        tokens_input  = getattr(meta, "prompt_token_count", 0) or 0
        tokens_output = getattr(meta, "candidates_token_count", 0) or 0
        tokens_think  = getattr(meta, "thoughts_token_count", 0) or 0

        # Tokens de thinking são cobrados como output
        tokens_output_total = tokens_output + tokens_think

        preco = PRECOS.get(modelo, PRECO_PADRAO)

        custo_input  = (tokens_input  / 1_000_000) * preco["input"]
        custo_output = (tokens_output_total / 1_000_000) * preco["output"]
        custo_total  = custo_input + custo_output

        return {
            "modelo":         modelo,
            "tokens_input":   tokens_input,
            "tokens_output":  tokens_output_total,
            "tokens_thinking": tokens_think,
            "custo_input_usd":  round(custo_input,  6),
            "custo_output_usd": round(custo_output, 6),
            "custo_usd":        round(custo_total,  6),
            "custo_brl":        round(custo_total * COTACAO_BRL, 5),
        }

    except Exception as e:
        return {
            "modelo": modelo,
            "tokens_input": 0,
            "tokens_output": 0,
            "tokens_thinking": 0,
            "custo_input_usd": 0,
            "custo_output_usd": 0,
            "custo_usd": 0,
            "custo_brl": 0,
            "erro": str(e),
        }
