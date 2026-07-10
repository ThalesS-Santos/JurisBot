# Guia: Compreensão de Áudio (Audio Understanding)

O Gemini não apenas fala (TTS), mas também **ouve e entende**. Ele pode analisar arquivos de áudio para gerar transcrições, resumos, identificar falantes e detectar emoções.

> **Nota:** Para transcrição em tempo real (streaming), utilize a [Live API](./recurso_live_api.md) ou Google Cloud Speech-to-Text. Este guia foca no processamento de arquivos de áudio via Gemini API.

---

## 1. Visão Geral

O Gemini pode:
*   Descrever e resumir clipes de áudio.
*   Transcrever fala para texto (Speech-to-Text) e traduzir.
*   Diarização de falantes (identificar quem está falando).
*   Detectar emoções e nuances (ironia, tom de voz).
*   Responder perguntas sobre o áudio ocm timestamps.

**Formatos Suportados:**
*   `WAV`, `MP3`, `AIFF`, `AAC`, `OGG`, `FLAC`.
*   Taxa de amostragem interna normalizada para 16kbps.

---

## 2. Como Usar (Upload de Arquivo)

Para arquivos maiores ou uso recorrente, o recomendado é usar a **Files API**.

### Python
```python
from google import genai

client = genai.Client()

# Upload do arquivo
myfile = client.files.upload(file="path/to/sample.mp3")

# Geração de conteúdo
response = client.models.generate_content(
    model="gemini-3-flash-preview", 
    contents=["Describe this audio clip", myfile]
)

print(response.text)
```

### JavaScript (Node.js)
```javascript
import { GoogleGenAI, createUserContent, createPartFromUri } from "@google/genai";

const ai = new GoogleGenAI({});
const myfile = await ai.files.upload({
    file: "path/to/sample.mp3",
    config: { mimeType: "audio/mp3" },
});

const response = await ai.models.generateContent({
    model: "gemini-3-flash-preview",
    contents: createUserContent([
        createPartFromUri(myfile.uri, myfile.mimeType),
        "Describe this audio clip",
    ]),
});
console.log(response.text);
```

### Go
```go
// Exemplo simplificado (ver código completo na doc oficial ou exemplos)
uploadedFile, _ := client.Files.UploadFromPath(ctx, "sample.mp3", nil)
// ... use uploadedFile.URI na chamada GenerateContent
```

---

## 3. Inline Audio (Dados na Requisição)

Para arquivos pequenos (< 20MB total da request), você pode enviar os bytes diretamente.

### Python
```python
from google import genai
from google.genai import types

with open('sample.mp3', 'rb') as f:
    audio_bytes = f.read()

client = genai.Client()
response = client.models.generate_content(
  model='gemini-3-flash-preview',
  contents=[
    'Describe this audio clip',
    types.Part.from_bytes(data=audio_bytes, mime_type='audio/mp3')
  ]
)
```

---

## 4. Transcrição Avançada com JSON Estruturado

Exemplo de prompt para extrair falantes, timestamps e emoções em formato JSON.

**Prompt Sugerido:**
> "Process the audio file and generate a detailed transcription.
> Requirements:
> 1. Identify distinct speakers.
> 2. Provide timestamps (MM:SS).
> 3. Detect primary language and translate if needed.
> 4. Identify primary emotion (Happy, Sad, Angry, Neutral)."

**Configuração Python (Schema):**
```python
config=types.GenerateContentConfig(
  response_mime_type="application/json",
  response_schema=types.Schema(
    type=types.Type.OBJECT,
    properties={
      "summary": types.Schema(type=types.Type.STRING),
      "segments": types.Schema(
        type=types.Type.ARRAY,
        items=types.Schema(
          type=types.Type.OBJECT,
          properties={
              "speaker": types.Schema(type=types.Type.STRING),
              "timestamp": types.Schema(type=types.Type.STRING),
              "content": types.Schema(type=types.Type.STRING),
              "emotion": types.Schema(enum=["happy", "sad", "angry", "neutral"])
          }
        )
      )
    }
  )
)
```

---

## 5. Detalhes Técnicos e Limites

*   **Tokens de Áudio:** O Gemini processa áudio a **32 tokens por segundo** (1 minuto = 1.920 tokens).
*   **Contagem de Tokens:** Utilize `client.models.count_tokens` passando o arquivo de áudio para saber o custo antes de gerar.
*   **Tamanho Máximo:** Até 9.5 horas de áudio em um único prompt (respeitando a janela de contexto do modelo).
*   **Múltiplos Arquivos:** O limite de 9.5h é para a soma total de arquivos na requisição.
