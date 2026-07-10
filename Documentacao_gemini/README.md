# Documentação Google Gemini

Bem-vindo à documentação organizada dos modelos e ferramentas Google Gemini.

## Índice de Documentos

### 1. Modelos de IA
*   **[Modelos Principais (Gemini 3, 2.5, 2.0)](./modelos/modelos_principais.md)**
    *   Detalhes dos modelos core (Pro, Flash, Flash-Lite).
    *   Capacidades multimodais (Texto, Imagem, Vídeo, Áudio).
    *   Limites de tokens e datas de corte.

*   **[Modelos Especializados](./modelos/modelos_especializados.md)**
    *   **Imagens**: Gemini 3 Pro Image, Gemini Flash Image.
    *   **Áudio (TTS)**: Modelos Text-to-Speech (Flash/Pro).
    *   **Live API**: Modelos para interação em tempo real.

*   **[Tabela de Preços](./modelos/precos_modelos.md)**
    *   Custos detalhados por modelo (Input/Output/Cache).
    *   Preços para Imagen, Veo e Embeddings.

### 2. Guias de Recursos
*   **[Guia: Live API (Realtime)](./guias/recurso_live_api.md)** (Novo!)
    *   WebSockets e Baixa Latência.
    *   Voice Activity Detection (VAD).
    *   Implementação Python e Node.js.

*   **[Guia: Compreensão de Áudio](./guias/guia_audio_understanding.md)** (Novo!)
    *   Speech-to-Text (Transcrição) e Tradução.
    *   Detecção de Emoções e Falantes (Diarization).
    *   Upload de arquivos e contagem de Tokens.

*   **[Guia: Geração de Vídeo (Veo)](./guias/guia_veo_video.md)** (Novo!)
    *   Veo 3.1 & Veo Fast (Prewiew).
    *   Text-to-Video e Image-to-Video.
    *   Controle de Câmera, Resolução e Áudio Nativo.

*   **[Guia: Compreensão de Imagem](./guias/guia_image_understanding.md)** (Novo!)
    *   Captioning e Visual QA.
    *   Object Detection (Bounding Boxes).
    *   Segmentation (Máscaras).

*   **[Guia Completo: Áudio e TTS](./guias/guia_audio_tts.md)** (Novo!)
    *   TTS Controle (Estilo, Ritmo, Sotaque).
    *   Exemplos Single & Multi-speaker (Python/JS).
    *   Lista de vozes e idiomas.

*   **[Guia Completo: Imagen](./guias/guia_imagen.md)** (Novo!)
    *   Exemplos de código (Python, JS, REST).
    *   Guia de Prompt Engineering e Parametrização.
    *   Detalhes do Imagen 4 e 3.

### 3. Desenvolvimento e SDK
*   **[Guia do Python SDK](./sdk/biblioteca_python_sdk.md)**
    *   Instalação e configuração.
    *   Exemplos de código (Texto, Chat, Multimodal, Funções).
    *   Tópicos avançados (Streaming, Async, Tuning).

*   **[Referência de Tipos do SDK](./sdk/referencia_tipos_sdk.md)**
    *   Lista exaustiva de objetos de configuração (`GenerateContentConfig`, `TuningJob`, etc.).
    *   Dicionários e tipos de dados.

*   **[Guia do Node.js SDK](./sdk/biblioteca_node_sdk.md)**
    *   Instalação (`@google/genai`).
    *   Exemplos Async/Await e Streams.
    *   Suporte a arquivos locais e Web.

*   **[Guia do Go SDK](./sdk/biblioteca_go_sdk.md)**
    *   Cliente oficial `google.golang.org/genai`.
    *   Contextos e tratamento de erros.
    *   Exemplos tipados.

*   **[API REST (Universal)](./sdk/biblioteca_rest_api.md)**
    *   Endpoints HTTP para qualquer linguagem (cURL, Java, C#, PHP).
    *   Estrutura JSON crua.

---
*Gerado p/ Assistente de Codificação Google Deepmind*
