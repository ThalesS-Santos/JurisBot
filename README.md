# ⚖️ JurisBot

Triagem jurídica orientativa para cidadãos brasileiros, alimentada por Google Gemini API com **RAG sobre a legislação real** (PDFs oficiais do Planalto/Senado).

Projeto final de MATE56 — Inteligência Artificial (UFBA)

---

## 📋 O que o JurisBot faz

O cidadão descreve sua situação em linguagem natural e recebe:

- ✅ **Triagem:** tem fundamento jurídico ou não
- 📚 **Área do direito** aplicável
- 📜 **Artigos de lei** que embasam o caso — citados a partir dos textos reais das leis
- 🧭 **Próximo passo** recomendado (Procon, Defensoria, JEC etc.)
- 💡 **Orientação prática** sobre o que fazer
- 🔍 **Fontes consultadas** — os trechos exatos das leis usados na análise
- 💰 **Controle de custo** da API por consulta (geração + embeddings)

---

## 🧠 Como funciona o RAG

```
                         BUILD (uma vez)
PDFs oficiais (leis/) ──> extração (pypdf) ──> limpeza ──> chunking por
artigos de lei ──> embeddings gemini-embedding-001 (768 dims, normalizados)
──> rag_index.npz (matriz NumPy) + rag_chunks.json (metadados)

                         CONSULTA (cada uso)
relato do usuário ──> embedding da consulta ──> similaridade vetorizada
(produto escalar NumPy, ~ms) ──> corte por relevância ──> MMR (diversidade)
──> top 8 trechos citáveis ──> prompt do gemini-3-flash-preview ──> triagem
```

Detalhes técnicos:

- **Chunking jurídico:** o texto é dividido respeitando fronteiras de artigos
  (`Art. 5º`, `Art. 18`...), então cada chunk carrega metadados de lei e
  intervalo de artigos — essencial para citações corretas.
- **Cabeçalho contextual:** cada chunk é embedado prefixado com o nome da lei,
  o que aproxima consultas como "fui demitido" dos trechos da CLT.
- **MMR (Maximal Marginal Relevance):** evita que os 8 trechos recuperados
  sejam quase idênticos, balanceando relevância e diversidade.
- **Índice binário:** matriz float32 L2-normalizada em `.npz` (~6 MB) em vez
  de JSON de texto (~80 MB) — carrega em milissegundos e busca via `E @ q`.

---

## 🛠️ Tecnologias utilizadas

| Técnica            | Aula     | Uso no JurisBot                                                    |
| ------------------ | -------- | ------------------------------------------------------------------ |
| Prompt Engineering | Aula 2/3 | Persona de "orientador jurídico popular"                           |
| Thinking Mode      | Aula 3   | Raciocínio jurídico no modo `low`                                  |
| RAG real           | Aula 8   | `gemini-embedding-001` + índice vetorial NumPy sobre PDFs oficiais |
| Structured Outputs | Aula 9   | Schema Pydantic `TriagemJuridica`                                  |
| Controle de Custo  | Aula 2   | `cost_tracker.py` (geração + embeddings)                           |

---

## 🚀 Como rodar

### 1. Clone e instale

```bash
git clone <seu-repo>
cd jurisbot
pip install -r requirements.txt
```

### 2. Configure a chave da API

Crie `.streamlit/secrets.toml`:

```toml
GEMINI_API_KEY = "sua-chave-real-aqui"
```

Pegue sua chave em: https://aistudio.google.com/app/apikey

### 3. Baixe os PDFs das leis para a pasta `leis/`

Fontes oficiais (gratuitas) — a base de referência usa estas 9 leis:

- [Constituição Federal](https://www.planalto.gov.br/ccivil_03/constituicao/constituicao.htm)
- [CLT](https://www.planalto.gov.br/ccivil_03/decreto-lei/del5452.htm)
- [CDC — Lei 8.078/90](https://www.planalto.gov.br/ccivil_03/leis/l8078compilado.htm)
- [Lei 8.213/91 (Previdência)](https://www.planalto.gov.br/ccivil_03/leis/l8213cons.htm)
- [Lei do Inquilinato 8.245/91](https://www.planalto.gov.br/ccivil_03/leis/l8245.htm)
- [Lei Maria da Penha](https://www.planalto.gov.br/ccivil_03/_ato2004-2006/2006/lei/l11340.htm)
- [ECA — Lei 8.069/90](https://www.planalto.gov.br/ccivil_03/leis/l8069.htm)
- [Estatuto da Pessoa Idosa — Lei 10.741/03](https://www.planalto.gov.br/ccivil_03/leis/2003/l10.741.htm)
- [Código de Processo Penal](https://www.planalto.gov.br/ccivil_03/decreto-lei/del3689.htm)
- Edições em PDF: [Biblioteca do Senado](https://www2.senado.leg.br/bdsf/)

> Ao adicionar um PDF novo, inclua o nome amigável dele em `NOMES_LEIS`
> dentro de `build_index.py`.

### 4. Construa o índice RAG (uma vez, ~US$ 0,02)

```bash
python build_index.py
```

### 5. Rode o app

```bash
streamlit run app.py
```

---

## 📁 Estrutura do Projeto

```
jurisbot/
├── app.py              # App Streamlit (UI + chamada ao Gemini)
├── rag_manager.py      # Motor RAG: chunking, embeddings, busca vetorial, MMR
├── build_index.py      # Constrói o índice a partir dos PDFs em leis/
├── cost_tracker.py     # Preços e custos da API (geração + embeddings)
├── requirements.txt    # Dependências Python
├── leis/               # PDFs oficiais das leis (não versionados)
├── rag_index.npz       # Embeddings float32 (gerado, não versionado)
├── rag_chunks.json     # Metadados dos chunks (gerado, não versionado)
└── .streamlit/
    └── secrets.toml    # Chave da API (NÃO subir no Git)
```

## 🔮 Próximos passos (roadmap)

- [ ] **Mais leis:** Código Civil, Estatuto da Pessoa com Deficiência, CTB
- [ ] **Histórico de consultas:** Salvar casos anteriores
- [ ] **Modo áudio:** Transcrever relatos por voz (acessibilidade)
- [ ] **Deploy:** Streamlit Cloud (gratuito)

---

## ⚠️ Aviso Legal

Este app é um **projeto educacional** e **não substitui** aconselhamento jurídico profissional.
As análises são orientativas. Sempre consulte um advogado ou a Defensoria Pública.
