# Guia Completo: Live API (Interação em Tempo Real)

A **Live API** permite interações de voz e vídeo de baixa latência com o Gemini. Ela processa fluxos contínuos de áudio, vídeo ou texto para entregar respostas faladas imediatas e naturais, criando uma experiência de conversação fluida.

> **Importante:** A Live API é otimizada para diálogos bidirecionais (conversas), diferente do TTS que é para leitura de texto estático.

---

## 1. Visão Geral

### Principais Recursos
*   **Baixa Latência:** Respostas rápidas para conversação natural.
*   **Voice Activity Detection (VAD):** O modelo sabe quando você parou de falar ou se foi interrompido.
*   **Ferramentas (Function Calling):** O modelo pode chamar funções durante a conversa.
*   **Tokens Efêmeros:** Autenticação segura do lado do cliente sem expor API Keys.

### Abordagens de Implementação
1.  **Server-to-Server:** Seu backend se conecta à Live API via WebSocket. O cliente envia audio para seu server, que repassa para o Gemini.
2.  **Client-to-Server:** O frontend (browser/mobile) conecta direto via WebSocket. **Recomendado para menor latência**. Use tokens efêmeros para segurança.

---

## 2. Exemplos de Implementação (Streaming de Áudio)

### Python
Requer `pyaudio` e `google-genai`.
*Este exemplo captura áudio do microfone e reproduz a resposta em tempo real.*

```python
import asyncio
from google import genai
import pyaudio

# Configurações de Áudio
FORMAT = pyaudio.paInt16
CHANNELS = 1
SEND_SAMPLE_RATE = 16000
RECEIVE_SAMPLE_RATE = 24000
CHUNK_SIZE = 1024

client = genai.Client()
MODEL = "gemini-2.5-flash-native-audio-preview-12-2025"
CONFIG = {"response_modalities": ["AUDIO"]}

async def run():
    pya = pyaudio.PyAudio()
    # ... (Código de setup de streams de mic e speaker omitido para brevidade, ver documentação completa)
    
    async with client.aio.live.connect(model=MODEL, config=CONFIG) as live_session:
        print("Conectado! Pode falar.")
        async with asyncio.TaskGroup() as tg:
            tg.create_task(send_audio(live_session))
            tg.create_task(receive_audio(live_session))
            
if __name__ == "__main__":
    asyncio.run(run())
```
*(Nota: O código completo de microfone/speaker envolve manipulação de filas `asyncio.Queue` e threads `pyaudio`, conforme detalhado na documentação oficial).*

### JavaScript (Node.js)
Requer `mic` e `speaker`.

```javascript
import { GoogleGenAI } from '@google/genai';
import mic from 'mic';
import Speaker from 'speaker';

const ai = new GoogleGenAI({});
const model = 'gemini-2.5-flash-native-audio-preview-12-2025';

async function live() {
  const session = await ai.live.connect({
    model: model,
    config: { responseModalities: ['AUDIO'] }
  });

  // Setup Microfone
  const micInstance = mic({ rate: '16000', channels: '1' });
  const micInputStream = micInstance.getAudioStream();

  micInputStream.on('data', (data) => {
    session.sendRealtimeInput({
      audio: {
        data: data.toString('base64'),
        mimeType: "audio/pcm;rate=16000"
      }
    });
  });

  micInstance.start();
  console.log('Falando...');
}
live();
```

---

## 3. Parceiros e Integrações

Para facilitar o desenvolvimento WebRTC/WebSocket, você pode usar integrações prontas:

*   **Pipecat (Daily):** Chatbots realtime.
*   **LiveKit:** Agentes de IA com LiveKit.
*   **Fishjam:** Streaming de vídeo/áudio.
*   **Voximplant:** Chamadas telefônicas (Inbound/Outbound).

---

## 4. Próximos Passos

*   **Session Management:** Como manter o contexto em conversas longas.
*   **Tool Use na Live API:** Permitir que o modelo execute ações (buscar clima, controlar luzes) via voz.
*   **Ephemeral Tokens:** Como gerar tokens temporários para segurança no frontend.
