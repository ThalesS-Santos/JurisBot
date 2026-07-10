import streamlit as st
import json
import time
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from typing import List, Literal, Optional
from knowledge_base import BASE_JURIDICA
from cost_tracker import calcular_custo, formatar_custo

# ─── CONFIG ────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="JurisBot",
    page_icon="⚖️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─── ESTILO VISUAL ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Serif:ital,wght@0,400;0,600;1,400&family=IBM+Plex+Mono:wght@400;500&family=Inter:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #F7F6F3;
}

/* Header */
.jb-header {
    display: flex;
    align-items: baseline;
    gap: 12px;
    border-bottom: 2px solid #1C1C1C;
    padding-bottom: 16px;
    margin-bottom: 32px;
}
.jb-logo {
    font-family: 'IBM Plex Serif', serif;
    font-size: 2.2rem;
    font-weight: 600;
    color: #1C1C1C;
    letter-spacing: -1px;
}
.jb-tagline {
    font-family: 'Inter', sans-serif;
    font-size: 0.85rem;
    color: #6B6B6B;
    font-weight: 400;
}

/* Input area */
.jb-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    font-weight: 500;
    color: #6B6B6B;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 6px;
}

/* Card de resultado */
.jb-card {
    background: #FFFFFF;
    border: 1px solid #E0DDD8;
    border-radius: 6px;
    padding: 28px 32px;
    margin-top: 24px;
}
.jb-card-header {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #9B9B9B;
    margin-bottom: 20px;
    border-bottom: 1px solid #F0EDE8;
    padding-bottom: 12px;
}

/* Veredicto */
.jb-veredicto {
    display: inline-block;
    padding: 6px 14px;
    border-radius: 4px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.78rem;
    font-weight: 500;
    letter-spacing: 0.04em;
    margin-bottom: 20px;
}
.jb-tem-caso { background: #E8F4EC; color: #1A6B35; }
.jb-sem-caso { background: #FDF3E8; color: #8B4E0F; }
.jb-analise  { background: #EEF2FB; color: #2A4A9B; }

/* Seções do resultado */
.jb-section-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #9B9B9B;
    margin: 20px 0 8px 0;
}
.jb-section-body {
    font-family: 'Inter', sans-serif;
    font-size: 0.92rem;
    color: #2C2C2C;
    line-height: 1.7;
}

/* Artigos de lei */
.jb-artigo {
    background: #F7F6F3;
    border-left: 3px solid #1C1C1C;
    padding: 10px 16px;
    margin: 6px 0;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.78rem;
    color: #3C3C3C;
    border-radius: 0 4px 4px 0;
}

/* Próximo passo — destaque */
.jb-proximo {
    background: #1C1C1C;
    color: #F7F6F3;
    border-radius: 6px;
    padding: 16px 20px;
    margin-top: 20px;
    font-size: 0.92rem;
    line-height: 1.6;
}
.jb-proximo-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.6rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #8B8B8B;
    margin-bottom: 8px;
}

/* Custo */
.jb-custo {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    color: #9B9B9B;
    text-align: right;
    margin-top: 20px;
    padding-top: 14px;
    border-top: 1px solid #F0EDE8;
}

/* Botão */
div.stButton > button {
    background: #1C1C1C;
    color: #F7F6F3;
    border: none;
    border-radius: 4px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.78rem;
    font-weight: 500;
    letter-spacing: 0.06em;
    padding: 12px 32px;
    width: 100%;
    cursor: pointer;
    transition: background 0.15s;
}
div.stButton > button:hover {
    background: #3C3C3C;
    color: #F7F6F3;
}
div.stButton > button:active {
    background: #555;
}

/* Aviso */
.jb-aviso {
    font-size: 0.75rem;
    color: #9B9B9B;
    font-style: italic;
    margin-top: 8px;
    text-align: center;
}

/* Textarea override */
textarea {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.93rem !important;
    background: #FFFFFF !important;
    border: 1px solid #D8D5D0 !important;
    border-radius: 4px !important;
}

/* Sidebar custo acumulado */
.jb-acumulado {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.75rem;
    color: #5C5C5C;
    line-height: 2;
}

/* Área de exemplos */
.jb-exemplo {
    cursor: pointer;
    background: #FFFFFF;
    border: 1px solid #E0DDD8;
    border-radius: 4px;
    padding: 10px 14px;
    font-size: 0.82rem;
    color: #4C4C4C;
    margin-bottom: 6px;
    transition: border-color 0.15s;
}
.jb-exemplo:hover {
    border-color: #1C1C1C;
}
</style>
""", unsafe_allow_html=True)


# ─── SCHEMA PYDANTIC ──────────────────────────────────────────────────────────
class TriagemJuridica(BaseModel):
    tem_caso: Literal["sim", "nao", "necessita_analise"] = Field(
        description="Se há fundamento jurídico para o caso relatado."
    )
    area_direito: str = Field(
        description="Área do direito aplicável (ex: Direito do Consumidor, Direito Trabalhista)."
    )
    resumo_caso: str = Field(
        description="Resumo claro e objetivo do que foi relatado em 2-3 frases."
    )
    artigos_aplicaveis: List[str] = Field(
        description="Lista de artigos de lei, incisos ou resoluções que fundamentam a análise."
    )
    proximo_passo: Literal[
        "Procon",
        "Defensoria Pública",
        "Juizado Especial Cível (JEC)",
        "Advogado Particular",
        "Ministério Público",
        "Delegacia ou Polícia Civil",
        "Sem ação necessária",
        "Mais informações necessárias"
    ] = Field(
        description="Órgão ou instância recomendada como próximo passo."
    )
    orientacao_proximo_passo: str = Field(
        description="Instruções práticas e objetivas sobre como dar o próximo passo — onde ir, o que levar, o que dizer."
    )
    observacao_importante: Optional[str] = Field(
        default=None,
        description="Alerta ou observação crítica sobre o caso, se houver (ex: prazo prescricional próximo)."
    )


# ─── CLIENTE GEMINI ───────────────────────────────────────────────────────────
@st.cache_resource
def get_client():
    api_key = st.secrets.get("GEMINI_API_KEY", "")
    if not api_key:
        return None
    return genai.Client(api_key=api_key)


# ─── FUNÇÃO PRINCIPAL ─────────────────────────────────────────────────────────
def analisar_caso(client, relato: str) -> tuple[TriagemJuridica, dict]:
    modelo = "gemini-3-flash-preview"

    contexto_juridico = BASE_JURIDICA

    system_prompt = f"""Você é um assistente jurídico especializado em orientar cidadãos brasileiros de baixa renda sobre seus direitos.

Sua função é analisar o relato de uma pessoa e realizar uma triagem jurídica inicial.

IMPORTANTE:
- Você NÃO é advogado e NÃO presta consultoria jurídica formal.
- Sua análise é orientativa e educacional — sempre recomende buscar um profissional.
- Seja claro, direto e use linguagem acessível.
- Base seu raciocínio na legislação brasileira vigente.

BASE DE CONHECIMENTO JURÍDICO DISPONÍVEL:
{contexto_juridico}

Analise o relato e preencha todos os campos do schema com precisão."""

    response = client.models.generate_content(
        model=modelo,
        contents=[
            types.Content(role="user", parts=[
                types.Part(text=f"Relato do cidadão:\n\n{relato}")
            ])
        ],
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            response_mime_type="application/json",
            response_schema=TriagemJuridica,
            thinking_config=types.ThinkingConfig(
                include_thoughts=False,
                thinking_level="low"
            )
        )
    )

    resultado = response.parsed
    custo = calcular_custo(response, modelo)
    return resultado, custo


# ─── INICIALIZAR ESTADO ───────────────────────────────────────────────────────
if "historico_custos" not in st.session_state:
    st.session_state.historico_custos = []
if "resultado" not in st.session_state:
    st.session_state.resultado = None
if "relato_atual" not in st.session_state:
    st.session_state.relato_atual = ""


# ─── HEADER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="jb-header">
    <div class="jb-logo">⚖️ JurisBot</div>
    <div class="jb-tagline">Triagem jurídica gratuita para cidadãos brasileiros</div>
</div>
""", unsafe_allow_html=True)


# ─── SIDEBAR — CUSTO ACUMULADO ────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 📊 Controle de Uso da API")
    if st.session_state.historico_custos:
        total_consultas = len(st.session_state.historico_custos)
        total_input = sum(c["tokens_input"] for c in st.session_state.historico_custos)
        total_output = sum(c["tokens_output"] for c in st.session_state.historico_custos)
        total_custo = sum(c["custo_usd"] for c in st.session_state.historico_custos)

        st.markdown(f"""
<div class="jb-acumulado">
📋 Consultas: <b>{total_consultas}</b><br>
🔤 Tokens entrada: <b>{total_input:,}</b><br>
📝 Tokens saída: <b>{total_output:,}</b><br>
💵 Custo total: <b>US$ {total_custo:.5f}</b><br>
🇧🇷 Em reais (≈ R$ 6/USD): <b>R$ {total_custo * 6:.4f}</b>
</div>
""", unsafe_allow_html=True)

        if st.button("🗑️ Limpar histórico"):
            st.session_state.historico_custos = []
            st.rerun()
    else:
        st.markdown("*Nenhuma consulta ainda.*")

    st.divider()
    st.markdown("**ℹ️ Sobre o JurisBot**")
    st.markdown("""
Este app é um projeto educacional que usa IA (Google Gemini) para realizar triagens jurídicas iniciais.

**Não substitui** a consulta com um advogado ou defensor público.

Desenvolvido com:
- `Google Gemini API`
- `Pydantic` (structured outputs)
- `RAG` com base jurídica embutida
- `Streamlit`
""")


# ─── INPUT ────────────────────────────────────────────────────────────────────
st.markdown('<div class="jb-label">Descreva sua situação</div>', unsafe_allow_html=True)

EXEMPLOS = [
    "Comprei um celular na loja e veio com defeito. A loja se recusa a trocar dizendo que tenho que mandar para a assistência técnica.",
    "Fui demitido sem justa causa após 3 anos de empresa e não recebi meu FGTS nem as verbas rescisórias corretamente.",
    "Meu senhorio quer me despejar sem aviso prévio e sem motivo justo. Tenho contrato até o ano que vem.",
    "Sofri um acidente de trabalho e meu empregador não quer registrar o acidente nem pagar o afastamento.",
]

with st.expander("💡 Ver exemplos de relatos"):
    for ex in EXEMPLOS:
        if st.button(f'"{ex[:80]}…"', key=ex):
            st.session_state.relato_atual = ex

relato = st.text_area(
    label="relato",
    label_visibility="collapsed",
    value=st.session_state.relato_atual,
    placeholder="Conte o que aconteceu com suas próprias palavras. Quanto mais detalhes, melhor a análise...",
    height=160,
    key="input_relato"
)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    analisar = st.button("⚖️  Analisar meu caso")

st.markdown(
    '<div class="jb-aviso">Esta análise é orientativa e não substitui aconselhamento jurídico profissional.</div>',
    unsafe_allow_html=True
)

# ─── PROCESSAMENTO ────────────────────────────────────────────────────────────
if analisar:
    if not relato or len(relato.strip()) < 20:
        st.warning("Por favor, descreva sua situação com mais detalhes.")
    else:
        client = get_client()
        if not client:
            st.error("⚠️ Chave de API não configurada. Adicione `GEMINI_API_KEY` em `.streamlit/secrets.toml`.")
        else:
            with st.spinner("Analisando seu caso..."):
                try:
                    resultado, custo = analisar_caso(client, relato)
                    st.session_state.resultado = resultado
                    st.session_state.historico_custos.append(custo)
                except Exception as e:
                    st.error(f"Erro ao processar: {e}")
                    st.session_state.resultado = None


# ─── RESULTADO ────────────────────────────────────────────────────────────────
if st.session_state.resultado:
    r: TriagemJuridica = st.session_state.resultado
    custo_info = st.session_state.historico_custos[-1] if st.session_state.historico_custos else {}

    # Veredicto
    veredicto_map = {
        "sim":               ("TEM FUNDAMENTO JURÍDICO", "jb-tem-caso"),
        "nao":               ("SEM FUNDAMENTO JURÍDICO APARENTE", "jb-sem-caso"),
        "necessita_analise": ("NECESSITA ANÁLISE PROFISSIONAL", "jb-analise"),
    }
    label_v, classe_v = veredicto_map.get(r.tem_caso, ("—", ""))

    artigos_html = "".join(
        f'<div class="jb-artigo">{art}</div>'
        for art in r.artigos_aplicaveis
    )

    obs_html = ""
    if r.observacao_importante:
        obs_html = f"""
        <div class="jb-section-title">⚠️ Atenção</div>
        <div class="jb-section-body" style="color:#8B4E0F; background:#FDF3E8; padding:12px; border-radius:4px;">
            {r.observacao_importante}
        </div>"""

    custo_html = ""
    if custo_info:
        custo_html = f"""
        <div class="jb-custo">
            tokens entrada: {custo_info.get('tokens_input', '—')} ·
            tokens saída: {custo_info.get('tokens_output', '—')} ·
            custo: US$ {custo_info.get('custo_usd', 0):.5f}
        </div>"""

    st.markdown(f"""
<div class="jb-card">
    <div class="jb-card-header">RESULTADO DA TRIAGEM JURÍDICA</div>

    <span class="jb-veredicto {classe_v}">{label_v}</span>

    <div class="jb-section-title">Área do Direito</div>
    <div class="jb-section-body"><b>{r.area_direito}</b></div>

    <div class="jb-section-title">Resumo do Caso</div>
    <div class="jb-section-body">{r.resumo_caso}</div>

    <div class="jb-section-title">Artigos Aplicáveis</div>
    {artigos_html}

    {obs_html}

    <div class="jb-proximo">
        <div class="jb-proximo-label">Próximo passo recomendado → {r.proximo_passo}</div>
        {r.orientacao_proximo_passo}
    </div>

    {custo_html}
</div>
""", unsafe_allow_html=True)
