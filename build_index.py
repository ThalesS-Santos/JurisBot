"""
build_index.py — JurisBot
==========================
Lê os PDFs reais da pasta leis/, extrai o texto, gera embeddings com
gemini-embedding-001 e salva o índice RAG em rag_index.json.

Execute UMA VEZ (ou sempre que adicionar novos PDFs):
    python build_index.py

Custo estimado: ~US$ 0.02–0.05 dependendo do tamanho dos PDFs.
"""

import os
import sys
import time

import pypdf

# ─── API KEY ─────────────────────────────────────────────────────────────────

def _get_api_key() -> str:
    key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if key:
        return key
    secrets_path = os.path.join(os.path.dirname(__file__), ".streamlit", "secrets.toml")
    if os.path.exists(secrets_path):
        with open(secrets_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("GEMINI_API_KEY"):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    print("ERRO: GEMINI_API_KEY não encontrada.")
    sys.exit(1)


# ─── EXTRAÇÃO DE TEXTO DOS PDFs ───────────────────────────────────────────────

def extrair_texto_pdf(caminho: str) -> str:
    """Extrai todo o texto de um PDF usando pypdf."""
    reader = pypdf.PdfReader(caminho)
    paginas = []
    for page in reader.pages:
        texto = page.extract_text()
        if texto:
            paginas.append(texto.strip())
    return "\n\n".join(paginas)


def carregar_pdfs(pasta: str) -> dict[str, str]:
    """
    Lê todos os PDFs da pasta e retorna {nome_arquivo: texto_extraido}.
    Ignora arquivos que falharem na extração.
    """
    documentos = {}
    arquivos = [f for f in os.listdir(pasta) if f.lower().endswith(".pdf")]

    if not arquivos:
        print(f"ERRO: Nenhum PDF encontrado em '{pasta}'")
        sys.exit(1)

    print(f"  {len(arquivos)} PDFs encontrados:\n")

    for nome in sorted(arquivos):
        caminho = os.path.join(pasta, nome)
        try:
            texto = extrair_texto_pdf(caminho)
            palavras = len(texto.split())
            if palavras < 100:
                print(f"  [ignorado] {nome} - muito pouco texto ({palavras} palavras)")
                continue
            documentos[nome] = texto
            print(f"  [ok] {nome} - {palavras:,} palavras")
        except Exception as e:
            print(f"  [erro] {nome} - {e}")

    return documentos


# ─── MAIN ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    from google import genai
    from rag_manager import build_index, INDEX_PATH

    PASTA_LEIS = os.path.join(os.path.dirname(__file__), "leis")

    api_key = _get_api_key()
    client = genai.Client(api_key=api_key)

    print("=" * 58)
    print("  JurisBot — Construção do Índice RAG")
    print("=" * 58)
    print(f"  Fonte     : PDFs em '{PASTA_LEIS}'")
    print(f"  Embedding : gemini-embedding-001")
    print(f"  Destino   : {INDEX_PATH}")
    print("=" * 58 + "\n")

    print("[ 1/3 ] Extraindo texto dos PDFs...\n")
    documentos = carregar_pdfs(PASTA_LEIS)

    if not documentos:
        print("ERRO: Nenhum documento válido encontrado.")
        sys.exit(1)

    total_palavras = sum(len(t.split()) for t in documentos.values())
    print(f"\n  Total: {len(documentos)} documentos | {total_palavras:,} palavras")

    print("\n[ 2/3 ] Gerando embeddings...\n")
    build_index(client, documentos)

    print("\n[ 3/3 ] Concluído!")
    print(f"\n  Agora execute: streamlit run app.py")
