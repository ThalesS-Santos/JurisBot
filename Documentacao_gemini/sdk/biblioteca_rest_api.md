# API REST do Google Gemini

A API REST é universal e pode ser usada por qualquer linguagem capaz de fazer requisições HTTP (cURL, Java, C#, PHP, Rust, etc).

## Endpoint Base
`https://generativelanguage.googleapis.com/v1beta`

## Autenticação
Passe a API Key via query parameter `?key=YOUR_API_KEY` ou header `x-goog-api-key`.

## Exemplos (cURL)

### 1. Texto Simples
```bash
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=$GEMINI_API_KEY" \
    -H 'Content-Type: application/json' \
    -X POST \
    -d '{
      "contents": [{
        "parts": [{"text": "Escreva uma história sobre um robô mágico."}]
      }]
    }'
```

### 2. Multimodal (Base64)
```bash
# Converta imagem para base64 primeiro
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=$GEMINI_API_KEY" \
    -H 'Content-Type: application/json' \
    -X POST \
    -d '{
      "contents": [{
        "parts":[
          {"text": "O que é isso?"},
          {
            "inline_data": {
              "mime_type":"image/jpeg",
              "data": "'$(base64 -w0 image.jpg)'"
            }
          }
        ]
      }]
    }'
```

## Estrutura JSON Importante
*   **`contents`**: Lista de mensagens.
*   **`parts`**: Lista de partes da mensagem (texto, imagem, blob).
*   **`generationConfig`**: Parâmetros como `temperature`, `topK`.
*   **`systemInstruction`**: Instruções de sistema (System Prompt).
