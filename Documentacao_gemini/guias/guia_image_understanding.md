# Guia: Compreensão de Imagem (Image Understanding)

Os modelos Gemini são multimodais nativos, capazes de realizar tarefas de Visão Computacional sem a necessidade de modelos especializados.

> **Nota:** Este guia foca em **analisar** imagens (Visão). Para **gerar** imagens, veja o [Guia Imagen](./guia_imagen.md).

---

## 1. Capacidades e Modelos
Todas as versões do Gemini podem analisar imagens para:
*   Captioning (Legendar imagens).
*   Visual Question Answering (Responder perguntas sobre a imagem).
*   Classificação.

Modelos mais recentes possuem treino adicional para precisão:
*   **Object Detection:** Gemini 2.0+ (Bounding Boxes).
*   **Segmentation:** Gemini 2.5+ (Máscaras de contorno).

---

## 2. Passando Imagens para o Modelo

### Inline Data (Pequenos Arquivos)
Para arquivos pequenos (< 20MB total), envie os bytes diretamente.

#### Python
```python
from google import genai
from google.genai import types

with open('image.jpg', 'rb') as f:
    image_bytes = f.read()

client = genai.Client()
response = client.models.generate_content(
    model='gemini-3-flash-preview',
    contents=[
        types.Part.from_bytes(data=image_bytes, mime_type='image/jpeg'),
        'Descreva esta imagem.'
    ]
)
print(response.text)
```

#### JavaScript (Node.js)
```javascript
import { GoogleGenAI } from "@google/genai";
import * as fs from "node:fs";

const ai = new GoogleGenAI({});
const base64Image = fs.readFileSync("image.jpg", { encoding: "base64" });

const response = await ai.models.generateContent({
  model: "gemini-3-flash-preview",
  contents: [
    { inlineData: { mimeType: "image/jpeg", data: base64Image } },
    { text: "Descreva esta imagem." }
  ],
});
```

### File API (Arquivos Grandes / Reutilização)
Para arquivos grandes ou múltiplas requisições, faça upload primeiro.

```python
file = client.files.upload(file="path/to/image.jpg")
response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=[file, "Legende esta imagem."]
)
```

---

## 3. Object Detection (Detecção de Objetos)

O Gemini 2.0+ pode retornar coordenadas de caixas delimitadoras (Bounding Boxes). As coordenadas `box_2d` são normalizadas `[ymin, xmin, ymax, xmax]` na escala 0-1000.

### Exemplo (Python)
```python
from PIL import Image
import json

prompt = "Detect all items. Output JSON with key 'box_2d' normalized 0-1000."
response = client.models.generate_content(
    model="gemini-2.0-flash", 
    contents=[image, prompt],
    config={"response_schema": content_schema} 
    # Configure o schema JSON para garantir a saída estruturada
)
```
*(Veja o código completo de desnormalização no exemplo oficial).*

---

## 4. Segmentation (Segmentação)

O Gemini 2.5+ pode gerar máscaras de segmentação precisas.

O modelo retorna um JSON contendo, além do Bounding Box, uma máscara (string Base64 de um PNG) que representa o contorno exato do objeto.

---

## 5. Múltiplas Imagens

Você pode enviar várias imagens no mesmo prompt para comparação.

```python
response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=[
        "Qual a diferença entre estas duas imagens?",
        img1_file,
        img2_file
    ]
)
```

---

## 6. Limites e Dicas

*   **Formatos Suportados:** PNG, JPEG, WEBP, HEIC, HEIF.
*   **Limites de Arquivos:** Até 3.600 imagens por requisição (dependendo do modelo).
*   **Tokens:** Imagens consomem tokens. Gemini 2.0/2.5 Flash usam ~258 tokens para imagens pequenas (<= 384px) ou dividem imagens maiores em tiles.
*   **Orientação:** Verifique a rotação da imagem antes de enviar.
