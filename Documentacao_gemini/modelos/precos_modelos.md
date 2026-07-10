# Tabela de Preços (Gemini Models Pricing)

Esta tabela resume os custos para os principais modelos. Todos os valores são em **USD por 1 Milhão de Tokens**, salvo indicação em contrário.

## Gemini 3 Series (Preço de Pré-lançamento)

| Modelo | Entrada (Input) | Saída (Output) | Cache (Contexto) | Armazenamento de Cache |
| :--- | :--- | :--- | :--- | :--- |
| **Gemini 3 Pro** <br> `gemini-3-pro-preview` | **$2.00** (<= 200k) <br> **$4.00** (> 200k) | **$12.00** (<= 200k) <br> **$18.00** (> 200k) | $0.20 (<= 200k) <br> $0.40 (> 200k) | $4.50 / 1M / hora |
| **Gemini 3 Flash** <br> `gemini-3-flash-preview` | **$0.50** (Texto/Img/Vid) <br> **$1.00** (Áudio) | **$3.00** | $0.05 (Texto) <br> $0.10 (Áudio) | $1.00 / 1M / hora |
| **Gemini 3 Pro Image** <br> `gemini-3-pro-image-preview` | **$2.00** (Texto/Img) | **$12.00** (Texto) <br> **$120.00** (Imagens)* | N/A | N/A |

*\*Nota para Imagens (Gemini 3 Pro):* A saída de imagem custa aprox. **$0.134** por imagem (1K/2K) e **$0.24** por imagem (4K).

---

## Gemini 2.5 Series

| Modelo | Entrada (Input) | Saída (Output) | Cache (Contexto) | Armazenamento de Cache |
| :--- | :--- | :--- | :--- | :--- |
| **Gemini 2.5 Pro** <br> `gemini-2.5-pro` | **$1.25** (<= 200k) <br> **$2.50** (> 200k) | **$10.00** (<= 200k) <br> **$15.00** (> 200k) | $0.125 (<= 200k) <br> $0.25 (> 200k) | $4.50 / 1M / hora |

| **Gemini 2.5 Flash** <br> `gemini-2.5-flash` <br> `gemini-2.5-flash-preview-09-2025` | **$0.30** (Texto/Img/Vid) <br> **$1.00** (Áudio) | **$2.50** | $0.03 (Texto) <br> $0.10 (Áudio) | $1.00 / 1M / hora |
| **Gemini 2.5 Flash-Lite** <br> `gemini-2.5-flash-lite` <br> `gemini-2.5-flash-lite-preview-09-2025` | **$0.10** (Texto/Img/Vid) <br> **$0.30** (Áudio) | **$0.40** | $0.01 (Texto) <br> $0.03 (Áudio) | $1.00 / 1M / hora |

## Gemini 2.5 Specialized Models

| Modelo | Entrada (Input) | Saída (Output) | Cache |
| :--- | :--- | :--- | :--- |
| **Gemini 2.5 Flash Image** <br> `gemini-2.5-flash-image` | **$0.30** (Texto/Img) | **$0.039 / imagem** * | N/A |
| **Gemini 2.5 Flash Live (Audio/Video)** <br> `native-audio-preview-12-2025` | **$0.50** (Texto) <br> **$3.00** (Áudio/Vídeo) | **$2.00** (Texto) <br> **$12.00** (Áudio) | N/A |
| **Gemini 2.5 Flash TTS** <br> `gemini-2.5-flash-preview-tts` | **$0.50** (Texto) | **$10.00** (Áudio) | N/A |
| **Gemini 2.5 Pro TTS** <br> `gemini-2.5-pro-preview-tts` | **$1.00** (Texto) | **$20.00** (Áudio) | N/A |

*\*Nota para Imagens (2.5 Flash Image):* $30/1M tokens. 1 Imagem (1024x1024) ≈ 1.290 tokens ≈ $0.039.

---

## Gemini 2.0 Series

| Modelo | Entrada (Input) | Saída (Output) | Cache (Contexto) | Armazenamento de Cache |
| :--- | :--- | :--- | :--- | :--- |
| **Gemini 2.0 Flash** <br> `gemini-2.0-flash` | **$0.10** (Texto/Img/Vid) <br> **$0.70** (Áudio) | **$0.40** | $0.025 (Texto) <br> $0.175 (Áudio) | $1.00 / 1M / hora |
| **Gemini 2.0 Flash-Lite** <br> `gemini-2.0-flash-lite` | **$0.075** | **$0.30** | N/A | N/A |

*Nota Gemini 2.0 Flash:* Geração de imagens custa **$0.039** por imagem.

---


## Imagen Models (Geração de Imagens)

| Modelo | Preço por Imagem |
| :--- | :--- |
| **Imagen 4 Fast** (`imagen-4.0-fast-generate-001`) | **$0.02** |
| **Imagen 4 Standard** (`imagen-4.0-generate-001`) | **$0.04** |
| **Imagen 4 Ultra** (`imagen-4.0-ultra-generate-001`) | **$0.06** |
| **Imagen 3** (`imagen-3.0-generate-002`) | **$0.03** |

---

## Veo Models (Geração de Vídeo)

| Modelo | Preço por Segundo (USD) |
| :--- | :--- |
| **Veo 3.1 Standard** (com áudio) <br> `veo-3.1-generate-preview` | **$0.40** (720p/1080p) <br> **$0.60** (4k) |
| **Veo 3.1 Fast** (com áudio) <br> `veo-3.1-fast-generate-preview` | **$0.15** (720p/1080p) <br> **$0.35** (4k) |
| **Veo 3 Standard** (com áudio) <br> `veo-3.0-generate-001` | **$0.40** |
| **Veo 3 Fast** (com áudio) <br> `veo-3.0-fast-generate-001` | **$0.15** |
| **Veo 2** <br> `veo-2.0-generate-001` | **$0.35** |

---

## Embeddings (Incorporação)

| Modelo | Preço por 1 Milhão de Tokens |
| :--- | :--- |
| **Gemini Embedding** <br> `gemini-embedding-001` | **$0.15** |


---

### Notas Adicionais
*   **Google Search Grounding:**
    *   **Gemini 3 Pro/Flash:** 5.000 comandos/mês gratuitos. Depois, $14 / 1.000 consultas.
    *   **Gemini 2.5 Pro:** 1.500 RPD gratuitos. Depois, $35 / 1.000 comandos.
    *   **Gemini 2.5 Flash / Flash-Lite:** 1.500 RPD gratuitos. Depois, $35 / 1.000 comandos.
    *   **Google Maps (Flash/Lite):** 1.500 RPD gratuitos. Depois, $25 / 1.000 comandos. (Flash-Lite: 500 RPD limit for specific tiers)
