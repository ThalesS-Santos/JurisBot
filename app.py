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
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Reset e base ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Esconde label padrão do Streamlit no textarea */
.stTextArea label { display: none; }

/* ── Hero banner ── */
.jb-hero {
    background: linear-gradient(135deg, #0F172A 0%, #1E293B 60%, #0F4C81 100%);
    border-radius: 16px;
    padding: 40px 40px 36px;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
}
.jb-hero::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 240px; height: 240px;
    background: radial-gradient(circle, rgba(59,130,246,0.25) 0%, transparent 70%);
    border-radius: 50%;
}
.jb-hero::after {
    content: '';
    position: absolute;
    bottom: -40px; left: 30%;
    width: 160px; height: 160px;
    background: radial-gradient(circle, rgba(99,102,241,0.15) 0%, transparent 70%);
    border-radius: 50%;
}
.jb-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(59,130,246,0.2);
    border: 1px solid rgba(59,130,246,0.35);
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 0.72rem;
    font-weight: 500;
    color: #93C5FD;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    margin-bottom: 16px;
}
.jb-hero-title {
    font-size: 2.6rem;
    font-weight: 700;
    color: #F8FAFC;
    letter-spacing: -1.5px;
    line-height: 1.15;
    margin-bottom: 10px;
    position: relative;
    z-index: 1;
}
.jb-hero-title span {
    background: linear-gradient(90deg, #60A5FA, #818CF8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.jb-hero-sub {
    font-size: 0.97rem;
    color: #94A3B8;
    line-height: 1.6;
    max-width: 480px;
    position: relative;
    z-index: 1;
}
.jb-hero-stats {
    display: flex;
    gap: 28px;
    margin-top: 28px;
    padding-top: 24px;
    border-top: 1px solid rgba(255,255,255,0.08);
    position: relative;
    z-index: 1;
}
.jb-stat {
    display: flex;
    flex-direction: column;
    gap: 2px;
}
.jb-stat-num {
    font-size: 1.3rem;
    font-weight: 700;
    color: #F1F5F9;
}
.jb-stat-label {
    font-size: 0.72rem;
    color: #64748B;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}

/* ── Seção de input ── */
.jb-input-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    font-weight: 500;
    color: #64748B;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 10px;
}

/* Textarea override */
textarea {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.95rem !important;
    border-radius: 10px !important;
    border: 1.5px solid #334155 !important;
    background: #0F172A !important;
    color: #E2E8F0 !important;
    padding: 14px 16px !important;
    transition: border-color 0.2s !important;
    line-height: 1.65 !important;
}
textarea:focus {
    border-color: #3B82F6 !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,0.15) !important;
}

/* ── Botão principal ── */
div.stButton > button {
    background: linear-gradient(135deg, #2563EB, #4F46E5);
    color: #FFFFFF;
    border: none;
    border-radius: 10px;
    font-family: 'Inter', sans-serif;
    font-size: 0.95rem;
    font-weight: 600;
    letter-spacing: 0.02em;
    padding: 14px 32px;
    width: 100%;
    cursor: pointer;
    transition: all 0.2s;
    box-shadow: 0 4px 14px rgba(37,99,235,0.35);
}
div.stButton > button:hover {
    background: linear-gradient(135deg, #1D4ED8, #4338CA);
    box-shadow: 0 6px 20px rgba(37,99,235,0.45);
    transform: translateY(-1px);
    color: #FFFFFF;
}
div.stButton > button:active {
    transform: translateY(0);
    box-shadow: 0 2px 8px rgba(37,99,235,0.3);
}

/* ── Aviso legal ── */
.jb-aviso {
    font-size: 0.74rem;
    color: #475569;
    font-style: italic;
    margin-top: 10px;
    text-align: center;
}

/* ── Card de resultado ── */
.jb-card {
    background: #0F172A;
    border: 1px solid #1E293B;
    border-radius: 16px;
    padding: 32px 36px;
    margin-top: 28px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.4);
}
.jb-card-header {
    display: flex;
    align-items: center;
    gap: 8px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: #475569;
    margin-bottom: 24px;
    padding-bottom: 16px;
    border-bottom: 1px solid #1E293B;
}

/* ── Veredicto ── */
.jb-veredicto {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 8px 18px;
    border-radius: 8px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    font-weight: 500;
    letter-spacing: 0.04em;
    margin-bottom: 28px;
}
.jb-tem-caso {
    background: rgba(16,185,129,0.12);
    border: 1px solid rgba(16,185,129,0.3);
    color: #34D399;
}
.jb-sem-caso {
    background: rgba(245,158,11,0.12);
    border: 1px solid rgba(245,158,11,0.3);
    color: #FCD34D;
}
.jb-analise {
    background: rgba(99,102,241,0.12);
    border: 1px solid rgba(99,102,241,0.3);
    color: #A5B4FC;
}

/* ── Seções do resultado ── */
.jb-section-title {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #475569;
    margin: 28px 0 10px 0;
}
.jb-section-body {
    font-size: 0.95rem;
    color: #CBD5E1;
    line-height: 1.75;
}

/* ── Grid de duas colunas para área/resumo ── */
.jb-grid-2 {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    margin-bottom: 4px;
}
.jb-info-block {
    background: #1E293B;
    border-radius: 10px;
    padding: 16px 18px;
}
.jb-info-block .jb-section-title { margin-top: 0; }

/* ── Artigos de lei ── */
.jb-artigos-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 2px;
}
.jb-artigo {
    background: #1E293B;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 7px 14px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.76rem;
    color: #93C5FD;
    white-space: nowrap;
}

/* ── Observação ── */
.jb-obs {
    background: rgba(245,158,11,0.08);
    border: 1px solid rgba(245,158,11,0.25);
    border-radius: 10px;
    padding: 14px 18px;
    margin-top: 6px;
    font-size: 0.9rem;
    color: #FCD34D;
    line-height: 1.65;
}

/* ── Próximo passo ── */
.jb-proximo {
    background: linear-gradient(135deg, #1E3A5F, #1E2A4A);
    border: 1px solid rgba(59,130,246,0.25);
    border-radius: 12px;
    padding: 22px 24px;
    margin-top: 28px;
}
.jb-proximo-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.6rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: #60A5FA;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 6px;
}
.jb-proximo-destino {
    font-size: 1.1rem;
    font-weight: 700;
    color: #F1F5F9;
    margin-bottom: 10px;
}
.jb-proximo-body {
    font-size: 0.92rem;
    color: #94A3B8;
    line-height: 1.7;
}

/* ── Rodapé de custo ── */
.jb-custo {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    color: #334155;
    text-align: right;
    margin-top: 24px;
    padding-top: 16px;
    border-top: 1px solid #1E293B;
    display: flex;
    justify-content: flex-end;
    gap: 16px;
}
.jb-custo span {
    color: #475569;
}

/* ── Sidebar ── */
.jb-acumulado {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    color: #94A3B8;
    line-height: 2.2;
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
<div class="jb-hero">
    <div class="jb-badge">⚖️ &nbsp;Triagem Jurídica · IA</div>
    <div class="jb-hero-title">Juris<span>Bot</span></div>
    <div class="jb-hero-sub">
        Descreva sua situação em linguagem simples e receba uma orientação jurídica inicial gratuita — área do direito, artigos aplicáveis e próximo passo recomendado.
    </div>
    <div class="jb-hero-stats">
        <div class="jb-stat">
            <div class="jb-stat-num">5</div>
            <div class="jb-stat-label">Áreas do Direito</div>
        </div>
        <div class="jb-stat">
            <div class="jb-stat-num">100%</div>
            <div class="jb-stat-label">Gratuito</div>
        </div>
        <div class="jb-stat">
            <div class="jb-stat-num">Gemini 3</div>
            <div class="jb-stat-label">Motor de IA</div>
        </div>
    </div>
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
st.markdown('<div class="jb-input-label">Descreva sua situação</div>', unsafe_allow_html=True)

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

    veredicto_map = {
        "sim":               ("✓ &nbsp;Tem Fundamento Jurídico", "jb-tem-caso"),
        "nao":               ("✕ &nbsp;Sem Fundamento Aparente", "jb-sem-caso"),
        "necessita_analise": ("◎ &nbsp;Necessita Análise Profissional", "jb-analise"),
    }
    label_v, classe_v = veredicto_map.get(r.tem_caso, ("—", ""))

    artigos_html = "".join(
        f'<div class="jb-artigo">{art}</div>'
        for art in r.artigos_aplicaveis
    )

    obs_html = ""
    if r.observacao_importante:
        obs_html = f"""
        <div class="jb-section-title">⚠ &nbsp;Atenção</div>
        <div class="jb-obs">{r.observacao_importante}</div>"""

    custo_html = ""
    if custo_info:
        custo_html = f"""
        <div class="jb-custo">
            <span>entrada {custo_info.get('tokens_input', '—')} tk</span>
            <span>saída {custo_info.get('tokens_output', '—')} tk</span>
            <span>US$ {custo_info.get('custo_usd', 0):.5f}</span>
        </div>"""

    st.markdown(f"""
<div class="jb-card">
    <div class="jb-card-header">
        ◈ &nbsp;Resultado da Triagem Jurídica
    </div>

    <span class="jb-veredicto {classe_v}">{label_v}</span>

    <div class="jb-grid-2">
        <div class="jb-info-block">
            <div class="jb-section-title">Área do Direito</div>
            <div class="jb-section-body" style="font-weight:600; color:#E2E8F0;">{r.area_direito}</div>
        </div>
        <div class="jb-info-block">
            <div class="jb-section-title">Resumo do Caso</div>
            <div class="jb-section-body" style="font-size:0.85rem;">{r.resumo_caso}</div>
        </div>
    </div>

    <div class="jb-section-title">Artigos Aplicáveis</div>
    <div class="jb-artigos-grid">{artigos_html}</div>

    {obs_html}

    <div class="jb-proximo">
        <div class="jb-proximo-label">→ &nbsp;Próximo passo recomendado</div>
        <div class="jb-proximo-destino">{r.proximo_passo}</div>
        <div class="jb-proximo-body">{r.orientacao_proximo_passo}</div>
    </div>

    {custo_html}
</div>
""", unsafe_allow_html=True)
