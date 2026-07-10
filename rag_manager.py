"""
RAG Manager — JurisBot
======================
Motor de retrieval sobre legislação brasileira real (PDFs oficiais).

Pipeline:
  build_index.py  PDFs em leis/ -> limpeza -> chunking por artigos ->
                  embeddings gemini-embedding-001 (768 dims, normalizados) ->
                  rag_index.npz + rag_chunks.json

  app.py          rag.buscar(client, relato) ->
                  embedding da consulta -> busca vetorizada (NumPy) ->
                  filtro de relevância -> MMR (diversidade) -> trechos citáveis

Formato do índice:
  rag_index.npz    matriz float32 (N x 768), L2-normalizada
  rag_chunks.json  {"model", "dim", "chunks": [{"lei", "artigos", "texto"}]}
"""

from __future__ import annotations

import json
import os
import re
import threading
import time
import zipfile
from dataclasses import dataclass

import numpy as np
from google.genai import errors, types

from cost_tracker import estimar_custo_embedding

_DIR = os.path.dirname(os.path.abspath(__file__))
EMBEDDINGS_PATH = os.path.join(_DIR, "rag_index.npz")
CHUNKS_PATH = os.path.join(_DIR, "rag_chunks.json")

EMBED_MODEL = "gemini-embedding-001"
# A API retorna 3072 dims por padrão; 768 (Matryoshka) mantém a qualidade de
# retrieval com 1/4 do tamanho em disco e 4x menos cálculo por consulta.
EMBED_DIM = 768
BATCH_SIZE = 50
_RETRY_STATUS = {429, 500, 502, 503, 504}


# ─── LIMPEZA E CHUNKING (usados pelo build_index.py) ──────────────────────────

def limpar_texto(texto: str) -> str:
    """Normaliza texto extraído de PDF: hifenização, sumários, espaços."""
    # Remove linhas pontilhadas de sumário ("... 275"), que viram "palavras"
    # gigantes e poluem o índice com chunks de puro ruído
    texto = re.sub(r"\.{4,}\s*\d*", " ", texto)
    texto = re.sub(r"(?:\.\s){4,}\.?\s*\d*", " ", texto)
    # Junta palavras hifenizadas em quebra de linha: "traba-\nlhador" ->
    # "trabalhador". Apenas letra minúscula dos dois lados, para preservar
    # sufixos de artigo como "Art. 18-\nA" (18-A, não 18A)
    texto = re.sub(r"([a-záàâãéêíóôõúüç])-\s*\n\s*([a-záàâãéêíóôõúüç])", r"\1\2", texto)
    # Quebras de linha viram espaço (o chunking não depende de linhas)
    texto = re.sub(r"\s*\n\s*", " ", texto)
    # Colapsa espaços repetidos
    texto = re.sub(r"[ \t]{2,}", " ", texto)
    return texto.strip()


# Aceita "Art. 5º", "Art 18-A", "Artigo 7", "ARTIGO 3" e milhares "Art. 1.048"
_ART_SPLIT = re.compile(r"(?=\bArt(?:igo)?\.?\s*\d)", re.IGNORECASE)
_ART_LABEL = re.compile(
    r"\bArt(?:igo)?\.?\s*(\d+(?:\.\d{3})*(?:[ºo°])?(?:\s*-\s*[A-Z]\b)?)",
    re.IGNORECASE,
)

# Limites em caracteres (~400 palavras ≈ 2.400 chars em português jurídico)
_MAX_CHARS = 2400
_MIN_CHARS = 200
_OVERLAP_PALAVRAS = 60


def _dividir_segmento_grande(segmento: str) -> list[str]:
    """
    Divide um segmento maior que _MAX_CHARS em partes medidas por CARACTERES
    reais (não por contagem de palavras), com sobreposição em palavras.
    Uma cauda final pequena é absorvida na última parte em vez de virar um
    chunk quase 100% duplicado.
    """
    palavras = segmento.split()
    n = len(palavras)
    partes: list[str] = []
    inicio = 0

    while inicio < n:
        # Empacota palavras até estourar o orçamento de caracteres
        chars, fim = 0, inicio
        while fim < n and chars + len(palavras[fim]) + 1 <= _MAX_CHARS:
            chars += len(palavras[fim]) + 1
            fim += 1
        if fim == inicio:  # palavra única maior que o orçamento
            fim = inicio + 1

        restante = n - fim
        if restante <= _OVERLAP_PALAVRAS:
            # O que sobra caberia quase todo na sobreposição — absorve tudo
            # aqui e evita a "cauda" duplicada
            partes.append(" ".join(palavras[inicio:n]))
            break

        partes.append(" ".join(palavras[inicio:fim]))
        # Recuo de sobreposição, garantindo progresso mínimo de 1 palavra
        inicio = max(fim - _OVERLAP_PALAVRAS, inicio + 1)

    return partes


def chunk_por_artigos(texto: str) -> list[str]:
    """
    Divide o texto respeitando a estrutura de artigos das leis brasileiras.
    Artigos inteiros são agrupados em chunks de até _MAX_CHARS; artigos
    maiores que isso são subdivididos por palavras com sobreposição.
    """
    segmentos = [s.strip() for s in _ART_SPLIT.split(texto) if s.strip()]
    chunks: list[str] = []
    atual = ""

    for seg in segmentos:
        if len(seg) > _MAX_CHARS:
            if atual:
                chunks.append(atual)
                atual = ""
            chunks.extend(_dividir_segmento_grande(seg))
        elif len(atual) + len(seg) + 1 <= _MAX_CHARS:
            atual = f"{atual} {seg}".strip()
        else:
            chunks.append(atual)
            atual = seg

    if atual:
        chunks.append(atual)

    return [c for c in chunks if len(c) >= _MIN_CHARS]


def _numero_artigo(label: str) -> int:
    m = re.match(r"(\d+(?:\.\d{3})*)", label)
    return int(m.group(1).replace(".", "")) if m else 0


def rotulo_artigos(chunk: str) -> str:
    """
    Extrai o intervalo de artigos do chunk (ex: 'Arts. 18 a 26').

    Mantém apenas a subsequência NÃO-DECRESCENTE a partir do primeiro rótulo:
    cross-referências ("... nos termos do Art. 5º da CF") e reinícios de
    numeração (normas correlatas anexas no mesmo PDF) são ignorados, evitando
    intervalos absurdos como 'Arts. 191 a 49'.
    """
    labels = [l.replace(" ", "") for l in _ART_LABEL.findall(chunk)]
    if not labels:
        return "trecho geral"

    inicio = labels[0]
    fim = labels[0]
    for label in labels[1:]:
        if _numero_artigo(label) >= _numero_artigo(fim):
            fim = label

    if inicio == fim:
        return f"Art. {inicio}"
    return f"Arts. {inicio} a {fim}"


def texto_para_embedding(lei: str, artigos: str, texto: str) -> str:
    """
    Cabeçalho contextual: embedar o chunk prefixado com a lei e os artigos
    melhora o retrieval (a consulta "fui demitido" aproxima-se de "CLT")
    sem alterar o texto exibido ao usuário.
    """
    return f"{lei} — {artigos}: {texto}"


# ─── EMBEDDINGS ───────────────────────────────────────────────────────────────

def _normalizar(matriz: np.ndarray) -> np.ndarray:
    normas = np.linalg.norm(matriz, axis=-1, keepdims=True)
    normas[normas == 0] = 1.0
    return matriz / normas


def embed_textos(client, textos: list[str], task_type: str) -> np.ndarray:
    """
    Gera embeddings (float32, L2-normalizados) com retry exponencial para
    rate limit (429) e erros transitórios de servidor.
    """
    for tentativa in range(5):
        try:
            response = client.models.embed_content(
                model=EMBED_MODEL,
                contents=textos,
                config=types.EmbedContentConfig(
                    task_type=task_type,
                    output_dimensionality=EMBED_DIM,
                ),
            )
            matriz = np.array(
                [e.values for e in response.embeddings], dtype=np.float32
            )
            return _normalizar(matriz)
        except errors.APIError as e:
            codigo = getattr(e, "code", None)
            if tentativa == 4 or codigo not in _RETRY_STATUS:
                raise
            time.sleep(2**tentativa)

    raise RuntimeError("embed_textos: esgotou as tentativas")  # inalcançável


# ─── RESULTADO DE BUSCA ───────────────────────────────────────────────────────

@dataclass
class Trecho:
    lei: str        # nome amigável da lei de origem
    artigos: str    # ex: "Arts. 18 a 26"
    texto: str
    score: float    # similaridade de cosseno com a consulta


# ─── ÍNDICE ───────────────────────────────────────────────────────────────────

def _mmr(
    matriz: np.ndarray,
    scores: np.ndarray,
    candidatos: list[int],
    k: int,
    lamb: float,
) -> list[int]:
    """
    Maximal Marginal Relevance: seleciona k chunks balanceando relevância
    com diversidade (evita k trechos quase idênticos do mesmo artigo).
    """
    selecionados: list[int] = []
    restantes = list(candidatos)

    while restantes and len(selecionados) < k:
        if not selecionados:
            melhor = max(restantes, key=lambda i: scores[i])
        else:
            sel = matriz[selecionados]

            def valor_mmr(i: int) -> float:
                redundancia = float(np.max(sel @ matriz[i]))
                return lamb * float(scores[i]) - (1 - lamb) * redundancia

            melhor = max(restantes, key=valor_mmr)
        selecionados.append(melhor)
        restantes.remove(melhor)

    return selecionados


class RagIndex:
    def __init__(self):
        self._matriz: np.ndarray | None = None
        self._chunks: list[dict] = []
        self._lock = threading.Lock()

    @property
    def disponivel(self) -> bool:
        return os.path.exists(EMBEDDINGS_PATH) and os.path.exists(CHUNKS_PATH)

    def _carregar(self) -> None:
        # Double-checked locking: o Streamlit atende cada sessão numa thread
        if self._matriz is not None:
            return
        with self._lock:
            if self._matriz is not None:
                return
            if not self.disponivel:
                raise FileNotFoundError(
                    "Índice RAG não encontrado. Execute: python build_index.py"
                )
            try:
                with np.load(EMBEDDINGS_PATH) as dados:
                    matriz = dados["embeddings"].astype(np.float32)
                with open(CHUNKS_PATH, encoding="utf-8") as f:
                    meta = json.load(f)
            except (json.JSONDecodeError, KeyError, ValueError, OSError, zipfile.BadZipFile) as e:
                raise ValueError(
                    f"Índice RAG corrompido ({e}). Reconstrua com: python build_index.py"
                ) from e
            chunks = meta.get("chunks", [])
            if (
                not chunks
                or meta.get("dim") != matriz.shape[1]
                or len(chunks) != len(matriz)
            ):
                raise ValueError(
                    "Índice RAG vazio ou inconsistente. "
                    "Reconstrua com: python build_index.py"
                )
            self._chunks = chunks
            self._matriz = matriz  # atribuição por último: sinaliza carga completa

    def stats(self) -> dict | None:
        """Estatísticas do índice para exibição na UI (sem custo de API)."""
        if not self.disponivel:
            return None
        try:
            self._carregar()
        except (ValueError, FileNotFoundError, KeyError):
            return None
        leis = {c["lei"] for c in self._chunks}
        return {
            "chunks": len(self._chunks),
            "leis": len(leis),
            "dim": int(self._matriz.shape[1]),
        }

    def buscar(
        self,
        client,
        consulta: str,
        top_k: int = 8,
        candidatos: int = 24,
        lambda_mmr: float = 0.7,
        score_minimo: float = 0.50,
    ) -> tuple[list[Trecho], float]:
        """
        Retorna (trechos mais relevantes, custo estimado do embedding em USD).

        Etapas: embedding da consulta -> similaridade vetorizada contra todo o
        índice -> corte por score mínimo (garantindo ao menos 3) -> MMR.
        """
        self._carregar()

        vetor = embed_textos(client, [consulta], "RETRIEVAL_QUERY")[0]
        scores = self._matriz @ vetor

        ordem = np.argsort(scores)[::-1][:candidatos]
        aprovados = [int(i) for i in ordem if scores[i] >= score_minimo]
        if len(aprovados) < 3:
            aprovados = [int(i) for i in ordem[:3]]

        escolhidos = _mmr(self._matriz, scores, aprovados, top_k, lambda_mmr)

        trechos = [
            Trecho(
                lei=self._chunks[i]["lei"],
                artigos=self._chunks[i]["artigos"],
                texto=self._chunks[i]["texto"],
                score=float(scores[i]),
            )
            for i in escolhidos
        ]
        return trechos, estimar_custo_embedding(consulta)

    @staticmethod
    def montar_contexto(trechos: list[Trecho]) -> str:
        """Formata os trechos como fontes numeradas para o prompt."""
        blocos = [
            f"[Fonte {n} — {t.lei} | {t.artigos} | relevância {t.score:.2f}]\n{t.texto}"
            for n, t in enumerate(trechos, 1)
        ]
        return "\n\n---\n\n".join(blocos)


# Singleton reutilizado entre reruns do Streamlit
rag = RagIndex()
