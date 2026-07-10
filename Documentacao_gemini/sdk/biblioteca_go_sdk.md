# Biblioteca Google GenAI SDK para Go

O SDK oficial para Go permite construir aplicações robustas e performáticas utilizando os modelos Gemini.

## Instalação

```bash
go get google.golang.org/genai
```

## Configuração Básica

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
	// Busca API Key da variável GEMINI_API_KEY
	client, err := genai.NewClient(ctx, nil)
	if err != nil {
		log.Fatal(err)
	}
    // ...
}
```

## Exemplos de Uso

### 1. Geração de Texto
```go
result, err := client.Models.GenerateContent(
    ctx,
    "gemini-2.0-flash",
    genai.Text("Por que o céu é azul?"),
    nil,
)
if err != nil {
    log.Fatal(err)
}
println(result.Text())
```

### 2. Multimodal (Inline Data)
```go
imgData, _ := os.ReadFile("image.jpg")

result, err := client.Models.GenerateContent(
    ctx,
    "gemini-2.0-flash",
    []genai.Part{
        genai.ImageData("jpeg", imgData),
        genai.Text("Descreva a imagem."),
    },
    nil,
)
```

### 3. Configurações (Generation Config)
```go
config := &genai.GenerateContentConfig{
    Temperature: 0.7,
    TopP:        0.95,
}

result, err := client.Models.GenerateContent(
    ctx,
    "gemini-2.0-flash",
    genai.Text("Crie uma história criativa."),
    config,
)
```
