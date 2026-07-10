# Guia Completo: Geração de Vídeo (Veo 3.1)

O **Veo 3.1** é o modelo de estado da arte do Google para gerar vídeos de alta fidelidade (720p, 1080p ou 4k) com áudio nativo. Ele suporta estilos realistas e criativos, movimentos de câmera e controle preciso via prompt.

---

## 1. Visão Geral e Modelos

| Modelo | Código | Resolução | Áudio |
|---|---|---|---|
| **Veo 3.1** | `veo-3.1-generate-preview` | 720p, 1080p, 4k | ✔️ Sim |
| **Veo 3.1 Fast** | `veo-3.1-fast-generate-preview` | 720p | ✔️ Sim |

### Recursos Principais
*   **Audio Nativo:** Gera sons e diálogos sincronizados.
*   **Controle de Aspect Ratio:** Landscape (`16:9`) ou Portrait (`9:16`).
*   **Image-to-Video:** Anime imagens estáticas.
*   **Imagens de Referência:** Use até 3 imagens para guiar personagens ou objetos.
*   **Edição e Extensão:** Estenda vídeos existentes.

---

## 2. Text-to-Video (Texto para Vídeo)

Geração básica a partir de um prompt textual. A operação é assíncrona (Long-Running Operation).

### Python
```python
import time
from google import genai
from google.genai import types

client = genai.Client()

prompt = "A close up of two people staring at a cryptic drawing on a wall, torchlight flickering. A man murmurs, 'This must be it.' The woman looks at him and whispering excitedly, 'What did you find?'"

# Inicia a geração
operation = client.models.generate_videos(
    model="veo-3.1-generate-preview",
    prompt=prompt,
    config=types.GenerateVideosConfig(
        aspect_ratio="16:9",
        resolution="1080p" # Nota: 4k/1080p pode ter maior latência
    )
)

# Aguarda o processamento (Polling)
while not operation.done:
    print("Gerando vídeo...")
    time.sleep(10)
    operation = client.operations.get(operation)

# Salva o resultado
video = operation.response.generated_videos[0]
client.files.download(file=video.video)
video.video.save("resultado_veo.mp4")
```

### JavaScript (Node.js)
```javascript
import { GoogleGenAI } from "@google/genai";

const ai = new GoogleGenAI({});
const prompt = "A cinematic shot of a majestic lion in the savannah.";

// Inicia operação
let operation = await ai.models.generateVideos({
  model: "veo-3.1-generate-preview",
  prompt: prompt,
  config: { aspectRatio: "16:9" }
});

// Polling
while (!operation.done) {
    console.log("Aguardando...");
    await new Promise(r => setTimeout(r, 10000));
    operation = await ai.operations.getVideosOperation({ operation });
}

// Download
ai.files.download({
    file: operation.response.generatedVideos[0].video,
    downloadPath: "lion.mp4",
});
```

---

## 3. Image-to-Video (Imagem para Vídeo)

Anime uma imagem existente gerada pelo Imagen ou Nano Banana.

### Python
```python
# Supondo que 'image_response' seja um objeto Image já gerado ou carregado
operation = client.models.generate_videos(
    model="veo-3.1-generate-preview",
    prompt="Panning wide shot of the kitten waking up.",
    image=image_response.parts[0].as_image(),
)
```

### Imagens de Referência (Character Consistency)
Você pode passar até 3 imagens para manter a consistência de personagens ou produtos.
```python
dress_ref = types.VideoGenerationReferenceImage(image=dress_img, reference_type="asset")
woman_ref = types.VideoGenerationReferenceImage(image=woman_img, reference_type="asset")

operation = client.models.generate_videos(
    model="veo-3.1-generate-preview",
    prompt="The woman walks wearing the dress...",
    config=types.GenerateVideosConfig(
      reference_images=[dress_ref, woman_ref],
    ),
)
```

---

## 4. Guia de Prompt para Vídeo

O Veo entende termos cinematográficos.

*   **Subject (Sujeito):** O foco principal (ex: "Alien spaceships").
*   **Action (Ação):** O que está acontecendo (ex: "landing on a futuristic city").
*   **Camera (Câmera):** Movimentos ("Drone shot", "Dolly zoom", "Tracking shot").
*   **Lighting (Luz):** Atmosfera ("Cyberpunk neon", "Golden hour", "Cinematic lighting").
*   **Style (Estilo):** "Photorealistic", "Cartoon", "Claymation", "Noir".

**Dica de Áudio no Prompt:**
Inclua descrições sonoras para o áudio nativo.
> *"A man murmurs 'Hello', tires screeching loudly, engine roaring."*

---

## 5. Limites e Especificações

*   **Duração:** 4s, 6s ou 8s. (8s obrigatório para 4k/extensão).
*   **Retenção:** Vídeos ficam nos servidores do Google por 2 dias. Faça o download imediatamente.
*   **Segurança:** Filtros de segurança e marca d'água **SynthID** aplicados automaticamente.
*   **Extensão:** Vídeos podem ser estendidos em +7s (apenas 720p).

> **Aviso de Preço:** 4K e resoluções maiores custam mais e têm maior latência. Consulte a tabela de preços oficial.
