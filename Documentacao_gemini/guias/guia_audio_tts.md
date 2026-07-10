# Guia Completo: Áudio e Text-to-Speech (TTS) no Gemini

A API do Gemini permite transformar texto em áudio de alta qualidade com um ou múltiplos falantes. Diferente de sistemas tradicionais, a geração de áudio do Gemini é **controlável** via prompts em linguagem natural, permitindo ajustar estilo, sotaque, ritmo e tom.

> **Nota:** O TTS nativo é diferente da [Live API](./recurso_live_api.md), que é focada em conversação bidirecional em tempo real. O TTS é ideal para podcasts, audiobooks e recitação precisa.

---

## 1. Visão Geral e Modelos

### Modelos Suportados
| Modelo | Código | Single Speaker | Multi Speaker |
|---|---|---|---|
| **Gemini 2.5 Flash TTS** | `gemini-2.5-flash-preview-tts` | ✔️ | ✔️ |
| **Gemini 2.5 Pro TTS** | `gemini-2.5-pro-preview-tts` | ✔️ | ✔️ |

**Limites:** Janela de contexto de 32k tokens. Entrada apenas texto, saída apenas áudio.

---

## 2. Geração com Único Falante (Single-Speaker)

Gera áudio para uma única voz predefinida.

### Python
```python
from google import genai
from google.genai import types
import wave

client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash-preview-tts",
    contents="Say cheerfully: Have a wonderful day!",
    config=types.GenerateContentConfig(
        response_modalities=["AUDIO"],
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(
                    voice_name='Kore',
                )
            )
        ),
    )
)

# Salvar o arquivo
data = response.candidates[0].content.parts[0].inline_data.data
with wave.open("output.wav", "wb") as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(24000)
    wf.writeframes(data)
```

### JavaScript (Node.js)
```javascript
import { GoogleGenAI } from "@google/genai";
import * as fs from "node:fs";

async function main() {
  const ai = new GoogleGenAI({});
  const response = await ai.models.generateContent({
    model: "gemini-2.5-flash-preview-tts",
    contents: [{ parts: [{ text: 'Say cheerfully: Have a wonderful day!' }] }],
    config: {
      responseModalities: ['AUDIO'],
      speechConfig: {
        voiceConfig: {
          prebuiltVoiceConfig: { voiceName: 'Kore' },
        },
      },
    },
  });

  const data = response.candidates[0].content.parts[0].inlineData.data;
  const buffer = Buffer.from(data, 'base64');
  // Nota: O buffer raw é PCM. Para salvar como WAV válido em JS, 
  // pode ser necessário adicionar o cabeçalho WAV manual ou usar lib 'wav'.
  fs.writeFileSync('output.pcm', buffer);
}
main();
```

### Go
```go
config := &genai.GenerateContentConfig{
    ResponseModalities: []string{"AUDIO"},
    SpeechConfig: &genai.SpeechConfig{
        VoiceConfig: &genai.VoiceConfig{
            PrebuiltVoiceConfig: &genai.PrebuiltVoiceConfig{
                VoiceName: "Kore",
            },
        },
    },
}
resp, err := client.Models.GenerateContent(ctx, "gemini-2.5-flash-preview-tts", genai.Text("Hello!"), config)
// Process resp.Candidates[0].Content.Parts[0].InlineData.Data...
```

### REST API
```bash
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-tts:generateContent?key=$GEMINI_API_KEY" \
-H 'Content-Type: application/json' \
-d '{
    "contents": [{"parts":[{"text": "Hello world!"}]}],
    "generationConfig": {
        "responseModalities": ["AUDIO"],
        "speechConfig": {
            "voiceConfig": { "prebuiltVoiceConfig": { "voiceName": "Kore" } }
        }
    }
}'
```

---

## 3. Geração com Múltiplos Falantes (Multi-Speaker)

Permite simular conversas entre duas vozes distintas.

### Python
```python
prompt = """TTS the following conversation between Joe and Jane:
         Joe: How's it going today Jane?
         Jane: Not too bad, how about you?"""

response = client.models.generate_content(
   model="gemini-2.5-flash-preview-tts",
   contents=prompt,
   config=types.GenerateContentConfig(
      response_modalities=["AUDIO"],
      speech_config=types.SpeechConfig(
         multi_speaker_voice_config=types.MultiSpeakerVoiceConfig(
            speaker_voice_configs=[
               types.SpeakerVoiceConfig(
                  speaker='Joe', # Nome deve bater com o prompt
                  voice_config=types.VoiceConfig(
                     prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name='Kore')
                  )
               ),
               types.SpeakerVoiceConfig(
                  speaker='Jane',
                  voice_config=types.VoiceConfig(
                     prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name='Puck')
                  )
               ),
            ]
         )
      )
   )
)
```

---

## 4. Vozes Disponíveis

Existem 30 opções de vozes, cada uma com um perfil de tom. Os nomes são baseados em luas e estrelas.

| Nome | Tom (Inglês) | | Nome | Tom (Inglês) | | Nome | Tom (Inglês) |
|---|---|---|---|---|---|---|---|
| **Zephyr** | Bright | | **Puck** | Upbeat | | **Charon** | Informative |
| **Kore** | Firm | | **Fenrir** | Excitable | | **Leda** | Youthful |
| **Orus** | Firm | | **Aoede** | Breezy | | **Callirrhoe** | Easy-going |
| **Enceladus** | Breathy | | **Iapetus** | Clear | | **Gacrux** | Mature |

*Consulte a documentação oficial para a lista completa.*

---

## 5. Guia de Prompt (Direção de Áudio)

O Gemini TTS entende "notas de direção". Você pode atuar como um diretor definindo o cenário e o estilo da voz.

### Estrutura do Prompt

1.  **Audio Profile**: Quem está falando? (Nome, Arquétipo, Idade).
2.  **Scene**: Onde eles estão? Qual a "vibe" do ambiente?
3.  **Director's Notes**: (Importante) Estilo, Ritmo (Pacing), Sotaque (Accent).
4.  **Transcript**: O texto a ser falado.

### Exemplo de Prompt Completo

```markdown
# AUDIO PROFILE: Jaz R.
## "The Morning Hype"

## THE SCENE: The London Studio
It is 10:00 PM in a glass-walled studio overlooking the moonlit London skyline.
Jaz is bouncing to the rhythm. It is a chaotic, caffeine-fueled cockpit.

### DIRECTOR'S NOTES
Style:
* The "Vocal Smile": You must hear the grin in the audio.
* Dynamics: High projection without shouting.

Pace: Fast, energetic, "bouncing" cadence.
Accent: Jaz is from Brixton, London.

#### TRANSCRIPT
Yes, massive vibes in the studio! You are locked in and it is absolutely popping off...
```

### Idiomas Suportados
O modelo detecta automaticamente o idioma. Suporta 24 línguas, incluindo:
*   `pt-BR` (Português Brasil)
*   `en-US` (Inglês EUA)
*   `es-US` (Espanhol EUA)
*   `ja-JP` (Japonês)
*   Entre outros (`fr`, `de`, `it`, `ru`, `hi`, etc).
