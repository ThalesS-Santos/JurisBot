"""
RAG Manager — JurisBot
======================
Embeddings com gemini-embedding-001 + retrieval local por similaridade de cosseno.
O índice é construído uma vez via build_index.py e salvo em rag_index.json.
"""

import json
import math
import os
from typing import Optional
from google import genai

INDEX_PATH = os.path.join(os.path.dirname(__file__), "rag_index.json")
EMBED_MODEL = "gemini-embedding-001"


# ─── CHUNKING ─────────────────────────────────────────────────────────────────

def _chunk_texto(texto: str, chunk_size: int = 400, overlap: int = 80) -> list[str]:
    """Divide texto em chunks de ~chunk_size palavras com sobreposição."""
    palavras = texto.split()
    chunks = []
    i = 0
    while i < len(palavras):
        chunk = " ".join(palavras[i : i + chunk_size])
        chunks.append(chunk)
        i += chunk_size - overlap
    return chunks


# ─── EMBEDDING ────────────────────────────────────────────────────────────────

def _embed_batch(client: genai.Client, textos: list[str]) -> list[list[float]]:
    """Gera embeddings para uma lista de textos (em lote)."""
    from google.genai import types

    response = client.models.embed_content(
        model=EMBED_MODEL,
        contents=textos,
        config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT"),
    )
    return [e.values for e in response.embeddings]


def _embed_query(client: genai.Client, query: str) -> list[float]:
    """Gera embedding para a query do usuário."""
    from google.genai import types

    response = client.models.embed_content(
        model=EMBED_MODEL,
        contents=[query],
        config=types.EmbedContentConfig(task_type="RETRIEVAL_QUERY"),
    )
    return response.embeddings[0].values


# ─── SIMILARIDADE ─────────────────────────────────────────────────────────────

def _cosine(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


# ─── BUILD INDEX ──────────────────────────────────────────────────────────────

def build_index(client: genai.Client, documentos: dict[str, str], batch_size: int = 50) -> None:
    """
    Constrói o índice de embeddings e salva em rag_index.json.

    documentos: {"nome_lei": "texto completo da lei", ...}
    """
    todos_chunks = []   # {"area": str, "texto": str}
    todos_embeds = []   # list[list[float]]

    for area, texto in documentos.items():
        print(f"  Processando: {area}")
        chunks = _chunk_texto(texto)

        # Embeddings em lotes para não estourar o rate limit
        for i in range(0, len(chunks), batch_size):
            lote = chunks[i : i + batch_size]
            embeds = _embed_batch(client, lote)
            for chunk_text, embed in zip(lote, embeds):
                todos_chunks.append({"area": area, "texto": chunk_text})
                todos_embeds.append(embed)
            print(f"    {min(i + batch_size, len(chunks))}/{len(chunks)} chunks")

    index = {"chunks": todos_chunks, "embeddings": todos_embeds}
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False)

    print(f"\nÍndice salvo: {len(todos_chunks)} chunks em {INDEX_PATH}")


# ─── RETRIEVAL ────────────────────────────────────────────────────────────────

class RagManager:
    def __init__(self):
        self._chunks: list[dict] = []
        self._embeddings: list[list[float]] = []
        self._loaded = False

    def _load(self):
        if self._loaded:
            return
        if not os.path.exists(INDEX_PATH):
            raise FileNotFoundError(
                "Índice RAG não encontrado. Execute build_index.py primeiro."
            )
        with open(INDEX_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        self._chunks = data["chunks"]
        self._embeddings = data["embeddings"]
        self._loaded = True

    def get_context(
        self,
        client: genai.Client,
        query: str,
        top_k: int = 8,
    ) -> str:
        """
        Retorna os top_k chunks mais relevantes para a query,
        formatados como contexto para o prompt.
        """
        self._load()
        query_embed = _embed_query(client, query)

        scores = [
            (i, _cosine(query_embed, emb))
            for i, emb in enumerate(self._embeddings)
        ]
        scores.sort(key=lambda x: x[1], reverse=True)
        top = scores[:top_k]

        blocos = []
        for rank, (idx, score) in enumerate(top, 1):
            chunk = self._chunks[idx]
            blocos.append(
                f"[Fonte {rank} — {chunk['area']} | relevância {score:.2f}]\n{chunk['texto']}"
            )

        return "\n\n---\n\n".join(blocos)

    def index_exists(self) -> bool:
        return os.path.exists(INDEX_PATH)


# Singleton reutilizado entre requisições Streamlit
rag = RagManager()
