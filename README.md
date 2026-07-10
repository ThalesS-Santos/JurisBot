# ⚖️ JurisBot

Triagem jurídica orientativa para cidadãos brasileiros, alimentada por Google Gemini API.

Projeto final de MATE56 — Inteligência Artificial (UFBA)

---

## 📋 O que o JurisBot faz

O cidadão descreve sua situação em linguagem natural e recebe:

- ✅ **Triagem:** tem fundamento jurídico ou não
- 📚 **Área do direito** aplicável
- 📜 **Artigos de lei** que embasam o caso
- 🧭 **Próximo passo** recomendado (Procon, Defensoria, JEC etc.)
- 💡 **Orientação prática** sobre o que fazer
- 💰 **Controle de custo** da API por consulta

---

## 🛠️ Tecnologias utilizadas

| Técnica | Aula | Uso no JurisBot |
|---------|------|-----------------|
| Prompt Engineering | Aula 2/3 | Persona de "orientador jurídico popular" |
| Thinking Mode | Aula 3 | Raciocínio jurídico no modo `low` |
| RAG (embutido) | Aula 8 | Base jurídica modular no `knowledge_base.py` |
| Structured Outputs | Aula 9 | Schema Pydantic `TriagemJuridica` |
| Controle de Custo | Aula 2 | Módulo `cost_tracker.py` |

---

## 🚀 Como rodar

### 1. Clone o projeto
```bash
git clone <seu-repo>
cd jurisbot
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Configure a chave da API
Edite `.streamlit/secrets.toml`:
```toml
GEMINI_API_KEY = "sua-chave-real-aqui"
```
Pegue sua chave em: https://aistudio.google.com/app/apikey

### 4. Rode o app
```bash
streamlit run app.py
```

---

## 📁 Estrutura do Projeto

```
jurisbot/
├── app.py              # App principal (Streamlit + Gemini)
├── knowledge_base.py   # Base jurídica modular (RAG embutido)
├── cost_tracker.py     # Controle de custos da API
├── requirements.txt    # Dependências Python
├── README.md           # Este arquivo
└── .streamlit/
    └── secrets.toml    # Chave da API (NÃO subir no Git)
```

---

## 🔮 Próximos passos (roadmap)

- [ ] **RAG real com File Search (Aula 8):** Subir PDFs das leis completas
- [ ] **Mais áreas do direito:** Direito de Família, Penal, Tributário
- [ ] **Histórico de consultas:** Salvar casos anteriores
- [ ] **Modo áudio:** Transcrever relatos por voz (acessibilidade)
- [ ] **Deploy:** Streamlit Cloud (gratuito)

---

## ⚠️ Aviso Legal

Este app é um **projeto educacional** e **não substitui** aconselhamento jurídico profissional.
As análises são orientativas. Sempre consulte um advogado ou a Defensoria Pública.
