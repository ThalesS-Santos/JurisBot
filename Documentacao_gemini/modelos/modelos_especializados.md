# Modelos Gemini Especializados (Imagem, Áudio, Live)

Além dos modelos principais, a família Gemini inclui variantes especializadas para geração de imagens, áudio e interações em tempo real.

## Geração e Edição de Imagens
> **Dica:** Para um guia completo com exemplos de código, configurações e dicas de prompt, consulte o [Guia Completo de Imagens (Imagen)](../guias/guia_imagen.md).

### Imagen 4 (Standard / Ultra / Fast)
A geração mais recente e poderosa de modelos de imagem do Google.

| Propriedade | Descrição |
|---|---|
| **Códigos dos Modelos** | `imagen-4.0-generate-001` (Standard) <br> `imagen-4.0-ultra-generate-001` (Ultra) <br> `imagen-4.0-fast-generate-001` (Fast) |
| **Tipos de Dados** | **Entrada:** Texto <br> **Saída:** Imagem |
| **Limites** | **Input de Texto:** 480 tokens <br> **Imagens por requisição:** 1 a 4 |
| **Última Atualização** | Junho 2025 |

### Imagen 3
Modelo anterior de alta qualidade, base para muitas gerações.

| Propriedade | Descrição |
|---|---|
| **Código do Modelo** | `imagen-3.0-generate-002` |
| **Tipos de Dados** | **Entrada:** Texto <br> **Saída:** Imagem |
| **Última Atualização** | Fevereiro 2025 |

### Gemini 3 Pro Image (Preview)
Modelo multimodial nativo com preview de geração de imagens.


| Propriedade | Descrição |
|---|---|
| **Código do Modelo** | `gemini-3-pro-image-preview` |
| **Tipos de Dados** | **Entrada:** Texto, Imagem <br> **Saída:** Texto, Imagem |
| **Limites de Tokens** | **Entrada:** 65.536 <br> **Saída:** 32.768 |
| **Capacidades** | **Geração de Imagem:** Suportado |

### Gemini 2.5 Flash Image
Variante rápida e eficiente para tarefas de visão e geração de imagens.

| Propriedade | Descrição |
|---|---|
| **Código do Modelo** | `gemini-2.5-flash-image` |
| **Tipos de Dados** | **Entrada:** Texto, Imagem <br> **Saída:** Texto, Imagem |
| **Limites de Tokens** | **Entrada:** 65.536 <br> **Saída:** 32.768 |
| **Capacidades** | **Geração de Imagem:** Suportado |

### Gemini 2.0 Flash Image
Versão anterior da capacidade de geração de imagens do Flash.

| Propriedade | Descrição |
|---|---|
| **Código do Modelo** | `gemini-2.0-flash-preview-image-generation` |
| **Tipos de Dados** | **Entrada:** Áudio, Imagem, Vídeo, Texto <br> **Saída:** Texto, Imagem |
| **Limites de Tokens** | **Entrada:** 32.768 <br> **Saída:** 8.192 |

---

## Áudio e Voz (TTS)
> **Dica:** Para um guia completo com exemplos Single/Multi-speaker (Python e JS), lista de vozes e dicas de direção de áudio, consulte o [Guia Completo de Áudio e TTS](../guias/guia_audio_tts.md).

### Gemini 2.5 Flash TTS
Modelo Text-to-Speech otimizado para latência e velocidade.

| Propriedade | Descrição |
|---|---|
| **Código do Modelo** | `gemini-2.5-flash-preview-tts` |
| **Tipos de Dados** | **Entrada:** Texto <br> **Saída:** Áudio |
| **Limites de Tokens** | **Entrada:** 8.192 <br> **Saída:** 16.384 |

### Gemini 2.5 Pro TTS
Modelo Text-to-Speech de alta qualidade.

| Propriedade | Descrição |
|---|---|
| **Código do Modelo** | `gemini-2.5-pro-preview-tts` |
| **Tipos de Dados** | **Entrada:** Texto <br> **Saída:** Áudio |
| **Limites de Tokens** | **Entrada:** 8.192 <br> **Saída:** 16.384 |

---

## Interação em Tempo Real (Live API)
> **Referência:** Veja o [Guia da Live API](../guias/recurso_live_api.md) para detalhes de implementação (WebSocket, Client/Server).

### Gemini 2.5 Flash Live
Modelo desenhado para suporte nativo a áudio e vídeo em tempo real via WebSocket (Live API).

| Propriedade | Descrição |
|---|---|
| **Código do Modelo** | `gemini-2.5-flash-native-audio-preview-12-2025` |
| **Tipos de Dados** | **Entrada:** Áudio, Vídeo, Texto <br> **Saída:** Áudio, Texto |
| **Limites de Tokens** | **Entrada:** 131.072 <br> **Saída:** 8.192 |
| **Capacidades** | **Geração de Áudio:** Suportado <br> **Live API:** Suportado |

---

## Geração de Vídeo (Veo)
> **Dica:** Para um guia completo com exemplos de geração de vídeo, image-to-video, e controle de câmera, consulte o [Guia Completo de Vídeo (Veo)](../guias/guia_veo_video.md).

### Veo 3.1 (Preview)
Modelo de vídeo state-of-the-art com geração de áudio nativa.

| Propriedade | Descrição |
|---|---|
| **Código do Modelo** | `veo-3.1-generate-preview` |
| **Tipos de Dados** | **Entrada:** Texto, Imagem <br> **Saída:** Vídeo (com áudio) |
| **Limites** | **Input Texto:** 1.024 tokens <br> **Output:** 1 vídeo |
| **Resoluções** | 720p, 1080p, 4K |
| **Atualizado** | Jan 2026 |

### Veo 3.1 Fast (Preview)
Variante otimizada para velocidade.

| Propriedade | Descrição |
|---|---|
| **Código do Modelo** | `veo-3.1-fast-generate-preview` |
| **Resolução** | 720p apenas |
