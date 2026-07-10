# Guia Completo: Imagen (Geração de Imagens)

O **Imagen** é o modelo de geração de imagens de alta fidelidade do Google, capaz de criar imagens realistas e de alta qualidade a partir de prompts de texto. Todas as imagens geradas incluem uma marca d'água digital SynthID.

> **Nota:** Você também pode gerar imagens usando as capacidades multimodais nativas do Gemini (ex: Gemini 3 Pro Image). Este guia foca nos modelos standalone da família **Imagen**.

---

## 1. Como Usar (Exemplos de Código)

### Python
```python
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO

client = genai.Client()

response = client.models.generate_images(
    model='imagen-4.0-generate-001',
    prompt='Robot holding a red skateboard',
    config=types.GenerateImagesConfig(
        number_of_images=4,
    )
)
for generated_image in response.generated_images:
  generated_image.image.show()
```

### JavaScript
```javascript
import { GoogleGenAI } from "@google/genai";
import * as fs from "node:fs";

async function main() {
  const ai = new GoogleGenAI({});
  const response = await ai.models.generateImages({
    model: 'imagen-4.0-generate-001',
    prompt: 'Robot holding a red skateboard',
    config: {
      numberOfImages: 4,
    },
  });

  let idx = 1;
  for (const generatedImage of response.generatedImages) {
    let imgBytes = generatedImage.image.imageBytes;
    const buffer = Buffer.from(imgBytes, "base64");
    fs.writeFileSync(`imagen-${idx}.png`, buffer);
    idx++;
  }
}
main();
```

### Go
```go
package main

import (
	"context"
	"log"
	"os"

	"google.golang.org/genai"
)

func main() {
	ctx := context.Background()
	client, err := genai.NewClient(ctx, nil)
	if err != nil {
		log.Fatal(err)
	}

	resp, err := client.Models.GenerateImages(
		ctx,
		"imagen-3.0-generate-002",
		"Robot holding a red skateboard",
		&genai.GenerateImagesConfig{
			NumberOfImages: 4,
		},
	)
	if err != nil {
		log.Fatal(err)
	}

	for i, img := range resp.GeneratedImages {
		fname := "imagen-" + string(rune(i)) + ".png"
		_ = os.WriteFile(fname, img.Image.ImageBytes, 0644)
	}
}
```

### REST API
```bash
curl -X POST \
    "https://generativelanguage.googleapis.com/v1beta/models/imagen-4.0-generate-001:predict" \
    -H "x-goog-api-key: $GEMINI_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
        "instances": [
          {
            "prompt": "Robot holding a red skateboard"
          }
        ],
        "parameters": {
          "sampleCount": 4
        }
      }'
```

---

## 2. Configurações Disponíveis

O Imagen suporta apenas prompts em **Inglês** no momento.

| Parâmetro | Descrição | Valores Aceitos |
|---|---|---|
| `numberOfImages` | Quantidade de imagens a gerar. | 1 a 4 (Padrão: 4) |
| `imageSize` | Resolução da imagem (apenas Standard/Ultra). | `1K`, `2K` (Padrão: `1K`) |
| `aspectRatio` | Proporção da imagem. | `"1:1"`, `"3:4"`, `"4:3"`, `"9:16"`, `"16:9"` (Padrão: `"1:1"`) |
| `personGeneration` | Controle de geração de pessoas. | `"dont_allow"`, `"allow_adult"` (Padrão), `"allow_all"`* |

*\*Nota: "allow_all" não é permitido em regiões como EU, UK, CH, MENA.*

---

## 3. Guia de Prompt (Prompt Engineering)

Um bom prompt deve considerar **Sujeito**, **Contexto** e **Estilo**.
> *Exemplo: "Um desenho (Estilo) de um prédio moderno (Sujeito) cercado por arranha-céus (Contexto)."*

### Estrutura Ideal
1.  **Sujeito**: O objeto, pessoa ou animal principal.
2.  **Contexto/Fundo**: Onde o sujeito está? (Estúdio, parque, cidade).
3.  **Estilo**: Fotorealista, pintura a óleo, sketch, 3D, pixel art.
4.  **Iteração**: Comece com a ideia central e adicione detalhes progressivamente.

### Dicas Avançadas
*   **Fotografia**: Use termos como "A photo of...", "Macro lens" (objetos pequenos), "Telephoto" (animais/esportes), "Wide-angle" (paisagens).
*   **Iluminação**: "Natural lighting", "Dramatic lighting", "Golden hour".
*   **Estilos Artísticos**: "Oil painting", "Pencil sketch", "Pop art", "Impressionist".
*   **Materiais**: "Made of origami paper", "Made of cheese".
*   **Texto na Imagem**: Mantenha frases curtas (máx 25 caracteres) e coloque entre aspas no prompt. Ex: *A poster with the text "Summerland".*

### Parametrização de Prompts
Você pode criar templates para permitir que usuários personalizem a geração:
*Template:* `A {estilo} logo for a {ramo} company. Include the text {nome_empresa}.`

---

## 4. Versões do Modelo

### Imagen 4
Modelo mais recente e capaz.
*   **Códigos**:
    *   `imagen-4.0-generate-001` (Standard)
    *   `imagen-4.0-ultra-generate-001` (Ultra - Maior qualidade)
    *   `imagen-4.0-fast-generate-001` (Fast - Menor latência)
*   **Update**: Junho 2025.

### Imagen 3
Modelo anterior, altamente capaz.
*   **Código**: `imagen-3.0-generate-002`
*   **Update**: Fevereiro 2025.
