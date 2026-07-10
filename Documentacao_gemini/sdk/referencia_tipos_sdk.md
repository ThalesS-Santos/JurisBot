# Referência de Tipos e Configurações - Google Gen AI Python SDK

Este documento serve como referência rápida para os objetos de configuração, tipos e dicionários disponíveis no SDK `google-genai`.

## 1. Geração e Tipos Básicos

### Configuração de Geração
*   `GenerateContentConfig`: Configuração principal.
    *   Parâmetros: `temperature`, `top_p`, `top_k`, `candidate_count`, `max_output_tokens`, `stop_sequences`, `safety_settings`, `response_schema`.
*   `GenerationConfig`: Alias comum para configurações de geração.
*   `ThinkingConfig`: Controle de "pensamento" (`include_thoughts`, `thinking_budget`).
*   `LogprobsResult`: Detalhes de probabilidades (`top_candidates`, `chosen_candidates`).

### Modelos e Esquemas
*   `Model`: Metadados do modelo (`name`, `supported_actions`, `input_token_limit`, `tuned_model_info`).
*   `Schema` / `JSONSchema`: Definição de esquema para respostas estruturadas (`type`, `properties`, `enum`, `required`).
*   `Type`: Enum de tipos de dados (`STRING`, `INTEGER`, `OBJECT`, `ARRAY`).

### Conteúdo (Content & Parts)
*   `Content`: (`role`, `parts`).
*   `Part`: Container polimórfico.
    *   Tipos: `text`, `inline_data`, `file_data`, `function_call`, `function_response`, `executable_code`.
*   `user_content`, `model_content`: Helpers para criar conteúdo com papéis específicos.

---

## 2. Visão e Vídeo (Multimodal)

### Imagens (Imagen)
*   `GenerateImagesConfig`:
    *   `number_of_images`, `aspect_ratio`, `person_generation` (ALLOW_ADULT, ALLOW_ALL), `safety_filter_level`.
*   `EditImageConfig`: Edição/Inpainting.
    *   `edit_mode` (INPAINT_INSERTION, INPAINT_REMOVAL, OUTPAINT), `mask`, `reference_images`.
*   `UpscaleImageConfig`: Upsaling (`upscale_factor`).
*   `MaskReferenceConfig`: Configuração de máscara (`mask_mode`, `segmentation_classes`).
*   `ScribbleImage`: Input para controle via rabisco.

### Vídeos (Veo)
*   `GenerateVideosConfig`:
    *   `duration_seconds`, `fps`, `resolution` (1080p/4k), `aspect_ratio`, `generate_audio`.
*   `VideoGenerationMask`: Máscara para edição de vídeo (`mask_mode`).
*   `VideoMetadata`: Metadados como `fps`, `start_offset`, `end_offset`.

---

## 3. Áudio e Live API (Realtime)

### Live API
*   `LiveConnectConfig`: Início de sessão.
    *   `response_modalities`, `speech_config`, `system_instruction`, `generation_config`.
*   `LiveSendRealtimeInputParameters`: Envio de input de streaming.
    *   Campos: `audio`, `video`, `text`, `activity_start`, `activity_end`.
*   `LiveServerMessage`: Mensagens do servidor.
    *   Tipos: `server_content`, `tool_call`, `setup_complete`, `session_resumption_update`.
*   `LiveServerContent`: Conteúdo da resposta (`model_turn`, `turn_complete`, `interrupted`).
*   `VoiceActivity`: Detecção de voz (`ACTIVITY_START`, `ACTIVITY_END`).

### Música
*   `LiveMusicGenerationConfig`: `bpm`, `temperature`, `top_k`, `music_generation_mode`.

---

## 4. Fine-Tuning e Jobs

### Especificações de Tuning
*   `CreateTuningJobConfig`: Configuração global.
*   `SupervisedTuningSpec`: Fine-tuning supervisionado (`training_dataset_uri`, `hyper_parameters`).
*   `VeoTuningSpec`: Tuning para modelos de vídeo.
*   `PartnerModelTuningSpec`: Tuning para modelos de parceiros.

### Jobs
*   `TuningJob`: Estado e metadados (`state`, `tuned_model`, `tuning_data_stats`).
*   `TuningDataStats`: Estatísticas (`supervised_tuning_data_stats`, `distillation_data_stats`).

---

## 5. RAG e Retrieval

### Configuração de Retrieval
*   `RagRetrievalConfig`: Configuração de RAG.
    *   `top_k`, `filter` (metadados), `ranking` (LLM Ranker).
*   `VertexRagStore`: Store no Vertex AI (`rag_corpora`, `vector_distance_threshold`).
*   `GoogleSearchRetrieval`: Configuração de busca dinâmica (`mode`, `dynamic_threshold`).

### Grounding
*   `GroundingMetadata`: Informações de fonte (`web_search_queries`, `retrieval_queries`, `grounding_chunks`).
*   `GroundingChunk`: Pedaço de texto referenciado (`web`, `retrieved_context`).

---

## 6. Avaliação e Métricas

### Métricas
*   `Metric`: Definição de métrica personalizada.
*   `BleuSpec` / `RougeSpec`: Métricas de similaridade de texto padrão.
*   `PairwiseMetricSpec`: Comparação entre dois candidatos.
*   `PointwiseMetricSpec`: Avaliação de um único candidato.
*   `EvaluationConfig`: Configuração de tarefa de avaliação (`metrics`, `autorater_config`).

---

## 7. Segurança

*   `SafetySetting`: (`category`, `threshold`).
*   `HarmCategory`:
    *   `HARM_CATEGORY_HATE_SPEECH`, `HARM_CATEGORY_DANGEROUS_CONTENT`, `HARM_CATEGORY_SEXUALLY_EXPLICIT`, `HARM_CATEGORY_HARASSMENT`.
*   `HarmBlockThreshold`:
    *   `BLOCK_NONE`, `BLOCK_LOW_AND_ABOVE`, `BLOCK_ONLY_HIGH`.
*   `PhishBlockThreshold`: Específico para phishing.

---

## 8. Gerenciamento de Dados

*   `BatchJob`: Jobs de processamento em lote (`src`, `dest`, `completion_stats`).
*   `File`: Arquivos gerenciados pela API (`state`, `uri`, `expiration_time`).
*   `CachedContent`: Cache de contexto (`ttl`, `usage_metadata`).

---

## Nota sobre Dicionários (`*Dict`)
Para cada classe listada acima (ex: `TuningJob`), existe um `TypedDict` correspondente (ex: `TuningJobDict`). Eles permitem o uso de dicionários puros do Python compatíveis com a estrutura, o que pode ser útil para serialização ou input direto.
