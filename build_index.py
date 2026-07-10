"""
build_index.py — JurisBot
==========================
Constrói o índice RAG a partir dos PDFs oficiais na pasta leis/:

  1. Extrai o texto de cada PDF (pypdf)
  2. Limpa (hifenização, espaços) e divide respeitando artigos de lei
  3. Gera embeddings com gemini-embedding-001 (768 dims, normalizados)
  4. Salva rag_index.npz (matriz NumPy) + rag_chunks.json (metadados)

Execute UMA VEZ (ou sempre que adicionar/trocar PDFs):
    python build_index.py
"""

import json
import os
import sys

import numpy as np
import pypdf

from cost_tracker import PRECO_EMBEDDING_1M
from rag_manager import (
    BATCH_SIZE,
    CHUNKS_PATH,
    EMBED_DIM,
    EMBED_MODEL,
    EMBEDDINGS_PATH,
    chunk_por_artigos,
    embed_textos,
    limpar_texto,
    rotulo_artigos,
    texto_para_embedding,
)

PASTA_LEIS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "leis")

# Nome amigável de cada PDF — usado nas citações mostradas ao usuário.
# As edições do Senado incluem "normas correlatas" (outras leis anexas no
# mesmo PDF), então o nome reflete isso para a citação ser honesta.
# PDFs fora desta lista entram com o nome do arquivo (adicione-os aqui!).
NOMES_LEIS = {
    "000880424.pdf": "Lei do Inquilinato (Lei 8.245/1991) e normas correlatas",
    "CDC_e_normas_correlatas_4ed.pdf": "Código de Defesa do Consumidor (Lei 8.078/1990) e normas correlatas",
    "CF88_EC139_livro.pdf": "Constituição Federal de 1988",
    "CLT_normas_correlatas_8ed.pdf": "CLT (Decreto-Lei 5.452/1943) e normas correlatas",
    "Estatuto_crianca_adolescente_9ed.pdf": "Estatuto da Criança e do Adolescente (Lei 8.069/1990)",
    "Estatuto_pessoa_idosa_7ed.pdf": "Estatuto da Pessoa Idosa (Lei 10.741/2003)",
    "LEI Nº 8.213.pdf": "Lei de Benefícios da Previdência Social (Lei 8.213/1991)",
    "Lei_Maria_Penha_normas_correlatas_7ed.pdf": "Lei Maria da Penha (Lei 11.340/2006) e normas correlatas",
    "codigo_de_processo_penal_8ed.pdf": "Código de Processo Penal (Decreto-Lei 3.689/1941)",
}


def _get_api_key() -> str:
    key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if key:
        return key
    secrets_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), ".streamlit", "secrets.toml"
    )
    if os.path.exists(secrets_path):
        with open(secrets_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("GEMINI_API_KEY"):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    print("ERRO: GEMINI_API_KEY nao encontrada (env ou .streamlit/secrets.toml).")
    sys.exit(1)


def extrair_texto_pdf(caminho: str) -> str:
    reader = pypdf.PdfReader(caminho)
    paginas = [p.extract_text() or "" for p in reader.pages]
    return "\n".join(paginas)


def main() -> None:
    from google import genai

    client = genai.Client(api_key=_get_api_key())

    print("=" * 62)
    print("  JurisBot - Construcao do Indice RAG")
    print("=" * 62)
    print(f"  Fonte     : PDFs em {PASTA_LEIS}")
    print(f"  Embedding : {EMBED_MODEL} ({EMBED_DIM} dims)")
    print(f"  Destino   : {os.path.basename(EMBEDDINGS_PATH)} + {os.path.basename(CHUNKS_PATH)}")
    print("=" * 62 + "\n")

    if not os.path.isdir(PASTA_LEIS):
        print(f"ERRO: pasta '{PASTA_LEIS}' nao existe. Crie-a e coloque os PDFs das leis.")
        sys.exit(1)

    arquivos = sorted(
        f for f in os.listdir(PASTA_LEIS) if f.lower().endswith(".pdf")
    )
    if not arquivos:
        print(f"ERRO: nenhum PDF encontrado em {PASTA_LEIS}")
        sys.exit(1)

    # ── 1. Extração + chunking ──────────────────────────────────────────────
    print("[ 1/3 ] Extraindo e dividindo por artigos...\n")
    chunks_meta: list[dict] = []

    for nome in arquivos:
        lei = NOMES_LEIS.get(nome, nome)
        if nome not in NOMES_LEIS:
            print(f"  [aviso] {nome} sem nome amigavel em NOMES_LEIS")
        try:
            texto = limpar_texto(extrair_texto_pdf(os.path.join(PASTA_LEIS, nome)))
        except Exception as e:
            print(f"  [erro]  {nome} - {e}")
            continue
        if len(texto) < 1000:
            print(f"  [ignorado] {nome} - texto insuficiente ({len(texto)} chars)")
            continue

        pedacos = chunk_por_artigos(texto)
        for p in pedacos:
            chunks_meta.append({"lei": lei, "artigos": rotulo_artigos(p), "texto": p})
        print(f"  [ok] {lei} - {len(pedacos)} chunks")

    if not chunks_meta:
        print("ERRO: nenhum chunk gerado.")
        sys.exit(1)

    # Cabeçalho contextual: a lei e os artigos entram no texto embedado
    # (melhora o retrieval), mas o texto exibido fica limpo nos metadados
    textos = [
        texto_para_embedding(c["lei"], c["artigos"], c["texto"])
        for c in chunks_meta
    ]

    # Estimativa sobre o que será DE FATO embedado (texto com cabeçalho)
    total_chars = sum(len(t) for t in textos)
    custo_estimado = (total_chars / 4 / 1_000_000) * PRECO_EMBEDDING_1M
    print(f"\n  Total: {len(chunks_meta)} chunks | ~{total_chars // 4:,} tokens")
    print(f"  Custo estimado dos embeddings: US$ {custo_estimado:.4f}")

    # ── 2. Embeddings ───────────────────────────────────────────────────────
    print("\n[ 2/3 ] Gerando embeddings...\n")
    blocos: list[np.ndarray] = []

    for i in range(0, len(textos), BATCH_SIZE):
        lote = textos[i : i + BATCH_SIZE]
        blocos.append(embed_textos(client, lote, "RETRIEVAL_DOCUMENT"))
        feito = min(i + BATCH_SIZE, len(textos))
        print(f"  {feito}/{len(textos)} chunks embedados")

    matriz = np.vstack(blocos)

    # ── 3. Persistência (escrita atômica: tmp + os.replace) ─────────────────
    print("\n[ 3/3 ] Salvando indice...")
    tmp_npz = EMBEDDINGS_PATH + ".tmp.npz"
    np.savez_compressed(tmp_npz, embeddings=matriz)
    os.replace(tmp_npz, EMBEDDINGS_PATH)

    tmp_json = CHUNKS_PATH + ".tmp"
    with open(tmp_json, "w", encoding="utf-8") as f:
        json.dump(
            {"model": EMBED_MODEL, "dim": EMBED_DIM, "chunks": chunks_meta},
            f,
            ensure_ascii=False,
        )
    os.replace(tmp_json, CHUNKS_PATH)

    # Remove o índice legado em JSON gigante, se existir
    legado = os.path.join(os.path.dirname(EMBEDDINGS_PATH), "rag_index.json")
    if os.path.exists(legado):
        os.remove(legado)
        print("  (indice legado rag_index.json removido)")

    mb = os.path.getsize(EMBEDDINGS_PATH) / 1_048_576
    print(f"\n  Indice: {matriz.shape[0]} chunks x {matriz.shape[1]} dims ({mb:.1f} MB)")

    leis = sorted({c["lei"] for c in chunks_meta})
    print(f"  Leis indexadas ({len(leis)}):")
    for lei in leis:
        n = sum(1 for c in chunks_meta if c["lei"] == lei)
        print(f"    - {lei}: {n} chunks")

    print("\n  Concluido! Agora execute: streamlit run app.py")


if __name__ == "__main__":
    main()
