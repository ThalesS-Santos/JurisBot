"""
Módulo de Controle de Custos — JurisBot
========================================
Rastreia tokens e custos da API Gemini por consulta.

Preços (USD por 1 milhão de tokens) — referência jun/2026:
  gemini-3-flash-preview:       input $0.50 / output $3.00
  gemini-3.1-flash-lite-preview: input $0.10 / output $0.40
"""

# Tabela de preços por modelo (USD / 1M tokens)
PRECOS = {
    "gemini-3-flash-preview": {
        "input":  0.50,
        "output": 3.00,
    },
    "gemini-3.1-flash-lite-preview": {
        "input":  0.10,
        "output": 0.40,
    },
    "gemini-3.1-flash-lite": {
        "input":  0.10,
        "output": 0.40,
    },
    "gemini-3-flash": {
        "input":  0.50,
        "output": 3.00,
    },
}

PRECO_PADRAO = {"input": 0.50, "output": 3.00}


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
            "custo_brl":        round(custo_total * 6, 5),  # cotação aproximada
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


def formatar_custo(custo: dict) -> str:
    """Retorna string formatada para exibição do custo."""
    return (
        f"Tokens: {custo['tokens_input']} entrada + "
        f"{custo['tokens_output']} saída — "
        f"Custo: US$ {custo['custo_usd']:.5f} "
        f"(≈ R$ {custo['custo_brl']:.4f})"
    )
