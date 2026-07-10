# Biblioteca Google GenAI SDK para Node.js

O SDK do Google GenAI para Node.js permite que desenvolvedores JavaScript/TypeScript integrem facilmente os modelos Gemini em suas aplicações.

## Instalação

```bash
npm install @google/genai
```

## Configuração Básica

Para usar o SDK, você precisa de uma API Key.

```javascript
import { GoogleGenAI } from "@google/genai";

const ai = new GoogleGenAI({});
// O SDK busca automaticamente a variável de ambiente GOOGLE_API_KEY ou GEMINI_API_KEY
```

## Exemplos de Uso

### 1. Geração de Texto (Text-only)
```javascript
const response = await ai.models.generateContent({
  model: 'gemini-2.0-flash',
  contents: [{ parts: [{ text: 'Explique como funciona a gravidade para uma criança.' }] }],
});

console.log(response.text);
```

### 2. Stream de Resposta (Streaming)
```javascript
const result = await ai.models.generateContentStream({
  model: 'gemini-2.0-flash',
  contents: [{ parts: [{ text: 'Escreva um poema longo sobre o mar.' }] }],
});

for await (const chunk of result.stream) {
  process.stdout.write(chunk.text());
}
```

### 3. Chat (Multiturn)
O SDK não possui uma classe `ChatSession` com histórico automático como o Python, você deve gerenciar o histórico manualmente ou usar frameworks de nível superior.
*Nota: A versão mais recente do SDK pode introduzir abstrações de chat. Verifique a documentação oficial.*

### 4. Multimodal (Texto + Imagem)
```javascript
import * as fs from "node:fs";

const imageBase64 = fs.readFileSync("imagem.jpg", { encoding: "base64" });

const response = await ai.models.generateContent({
  model: 'gemini-2.0-flash',
  contents: [
    {
        inlineData: {
            mimeType: "image/jpeg",
            data: imageBase64
        }
    },
    { parts: [{ text: 'O que há nesta imagem?' }] }
  ],
});
console.log(response.text);
```
