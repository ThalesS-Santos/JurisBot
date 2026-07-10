"""
Base de Conhecimento Jurídico — JurisBot
=========================================
Estrutura modular: cada área do direito é um bloco separado.
Para expandir: adicione novos blocos e inclua-os em BASE_JURIDICA.

Próximos passos para melhorar:
  - Substituir por File Search Store do Gemini (Aula 8) com PDFs reais
  - Adicionar CLT completa, CDC completo, Lei do Inquilinato etc.
  - Adicionar jurisprudência do STJ e TST
"""

# ─── DIREITO DO CONSUMIDOR ────────────────────────────────────────────────────
CONSUMIDOR = """
=== DIREITO DO CONSUMIDOR (CDC — Lei 8.078/1990) ===

Art. 6° — Direitos básicos do consumidor:
  - Proteção contra práticas abusivas
  - Informação adequada e clara sobre produtos/serviços
  - Proteção contra publicidade enganosa
  - Efetiva prevenção e reparação de danos

Art. 18 — Vícios em produtos:
  O fornecedor tem 30 dias para sanar o vício. Não o fazendo, o consumidor pode:
  - Substituição do produto
  - Restituição do valor pago
  - Abatimento proporcional do preço
  Para produtos essenciais (saúde, segurança), prazo é imediato.

Art. 26 — Prazo para reclamar vício:
  - 30 dias: produtos/serviços não duráveis
  - 90 dias: produtos/serviços duráveis (geladeira, celular, TV)
  O prazo inicia na entrega do produto.

Art. 42 — Cobranças indevidas:
  Proibida cobrança vexatória ou com ameaça. Cobrança indevida gera direito
  à repetição em dobro do valor pago (art. 42, parágrafo único).

Art. 49 — Direito de arrependimento (compras online/fora do estabelecimento):
  7 dias corridos após entrega para desistir sem custo algum.

Art. 51 — Cláusulas abusivas são nulas de pleno direito.

Prazos prescricionais (art. 27):
  5 anos para ação de reparação por danos causados por fato do produto/serviço.
  
Órgãos: PROCON (administrativo), JEC até 40 salários mínimos, Justiça Comum acima disso.
"""

# ─── DIREITO TRABALHISTA ──────────────────────────────────────────────────────
TRABALHISTA = """
=== DIREITO TRABALHISTA (CLT — Decreto-Lei 5.452/1943) ===

Art. 477 — Rescisão contratual:
  Verbas rescisórias devem ser pagas em até 10 dias após término do contrato.
  Atraso gera multa de um salário ao empregado.

Verbas na demissão sem justa causa:
  - Saldo de salário
  - Aviso prévio (trabalhado ou indenizado — mínimo 30 dias)
  - 13° salário proporcional
  - Férias proporcionais + 1/3
  - FGTS + multa de 40% sobre saldo do FGTS
  - Seguro-desemprego (se elegível)

Art. 58 — Jornada de trabalho:
  Máximo 8h/dia e 44h semanais. Horas extras: mínimo 50% sobre hora normal (art. 59).

Art. 60/61 — Intervalo intrajornada:
  Jornada acima de 6h: mínimo 1h de almoço. Supressão gera hora extra.

Acidente de trabalho (Lei 8.213/91):
  - Empregador deve emitir CAT (Comunicação de Acidente de Trabalho)
  - Após 15 dias afastado: INSS paga benefício (auxílio-doença acidentário B91)
  - Garantia de emprego por 12 meses após retorno (art. 118 da Lei 8.213)

Assédio moral: não há lei federal específica, mas é passível de indenização
por danos morais (art. 186 e 927 do Código Civil c/c art. 5°, X da CF/88).

Prazos prescricionais:
  - 2 anos para ajuizar reclamação trabalhista após demissão
  - 5 anos retroativos de verbas enquanto na empresa

Órgão: Reclamação Trabalhista na Vara do Trabalho (gratuita com advogado do sindicato
ou Defensoria Pública do Trabalho).
"""

# ─── DIREITO DO INQUILINO ─────────────────────────────────────────────────────
LOCACAO = """
=== DIREITO DO INQUILINO (Lei do Inquilinato — Lei 8.245/1991) ===

Art. 46 — Contrato por prazo determinado:
  O locador NÃO pode retomar o imóvel antes do fim do contrato, salvo:
  - Descumprimento contratual pelo inquilino
  - Acordo entre as partes

Art. 47 — Contrato por prazo indeterminado (ou renovado após 30 meses):
  O locador pode pedir retomada, mas deve dar:
  - 30 dias de aviso prévio se for uso próprio/família (com ação judicial)

Art. 9° — Rescisão imediata pelo locador apenas por:
  - Mútuo acordo
  - Infração legal ou contratual
  - Falta de pagamento
  - Para realização de reparações urgentes determinadas pelo Poder Público

Art. 22 — Obrigações do locador:
  - Entregar o imóvel em condições de uso
  - Responder por vícios ocultos
  - Pagar taxas extraordinárias de condomínio

Art. 23 — Obrigações do locatário:
  - Pagar aluguel no prazo
  - Conservar o imóvel
  - Comunicar danos ao locador

Despejo ilegal: O locador NÃO pode cortar água/luz ou colocar cadeado para forçar saída.
Isso configura crime (Lei 4.591/64 e art. 168 do Código Penal — estelionato).

Órgãos: Se despejo ilegal, acionar Polícia Civil. Para disputas contratuais: JEC ou Vara Cível.
"""

# ─── DIREITO PREVIDENCIÁRIO ───────────────────────────────────────────────────
PREVIDENCIARIO = """
=== DIREITO PREVIDENCIÁRIO (Lei 8.213/1991) ===

Benefícios principais:
  - Auxílio-doença (B31): afastamento por doença por mais de 15 dias
  - Auxílio-doença acidentário (B91): afastamento por acidente de trabalho
  - Aposentadoria por invalidez: incapacidade permanente
  - Salário-maternidade: 120 dias (gestante com contribuições)
  - Pensão por morte: dependentes do segurado falecido

Carência mínima para auxílio-doença: 12 contribuições mensais
(exceção: acidentes não exigem carência)

Como solicitar benefício:
  - Pelo app/site Meu INSS (gov.br/meuinss)
  - Pelo telefone 135 (gratuito)
  - Agendamento em agência do INSS

Negativa do INSS:
  - Recurso administrativo no Conselho de Recursos da Previdência Social (CRPS)
  - Ação judicial no Juizado Especial Federal (JEF) — gratuito, sem advogado até 60 salários mínimos

Prazo para recorrer da negativa: 30 dias da ciência da decisão.
"""

# ─── VIOLÊNCIA DOMÉSTICA ──────────────────────────────────────────────────────
VIOLENCIA_DOMESTICA = """
=== VIOLÊNCIA DOMÉSTICA (Lei Maria da Penha — Lei 11.340/2006) ===

Tipos de violência cobertos:
  - Física, psicológica, sexual, patrimonial e moral

Art. 12 — Ao registrar o boletim de ocorrência, a autoridade policial deve:
  - Encaminhar para IML se necessário
  - Comunicar ao Ministério Público
  - Encaminhar para abrigo se necessário

Medidas protetivas de urgência (art. 22):
  - Afastamento do agressor do lar
  - Proibição de contato com a vítima e filhos
  - Suspensão de posse de armas
  Devem ser concedidas em até 48h pelo juiz.

Central de atendimento: Ligue 180 (24h, gratuito, sigiloso)
Emergência: 190 (Polícia Militar) ou 192 (SAMU)

Órgão: Delegacia de Atendimento à Mulher (DEAM) ou qualquer delegacia.
"""

# ─── BASE COMPLETA (adicione novos módulos aqui) ─────────────────────────────
BASE_JURIDICA = "\n\n".join([
    CONSUMIDOR,
    TRABALHISTA,
    LOCACAO,
    PREVIDENCIARIO,
    VIOLENCIA_DOMESTICA,
])

# ─── ROADMAP DE EXPANSÃO ─────────────────────────────────────────────────────
"""
Para expandir no futuro (usando RAG real com File Search — Aula 8):
  1. Baixar PDFs das leis completas (CLT, CDC, etc.)
  2. Criar File Search Store no Gemini
  3. Fazer upload dos PDFs
  4. Substituir BASE_JURIDICA por chamadas ao File Search Store
  
Leis prioritárias para adicionar:
  - Código de Defesa do Consumidor completo
  - CLT completa
  - Lei 8.213 (Previdência) completa
  - Lei do Inquilinato completa
  - Código Civil (arts. relevantes)
  - Estatuto do Idoso
  - Lei Brasileira de Inclusão (PCD)
"""
