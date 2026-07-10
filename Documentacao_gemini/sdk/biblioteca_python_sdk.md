# Documentação da Google Gen AI Python SDK

Esta documentação fornece um guia completo para integrar os modelos generativos do Google em aplicações Python, suportando tanto a **Gemini Developer API** quanto a **Vertex AI API**.

Referência Oficial: [Google Gen AI Python SDK](https://googleapis.github.io/python-genai/)
Referência de Tipos (Local): [Tipos e Configurações](./referencia_tipos_sdk.md)

---

## 1. Instalação e Configuração

### Instalação
```bash
pip install google-genai
# Ou com uv:
uv pip install google-genai
```

### Importação Básica
```python
from google import genai
from google.genai import types
```

---

## 2. Criando um Cliente (Client)

Você pode inicializar o cliente para a **Gemini Developer API** (Google AI Studio) ou para a **Vertex AI** (Google Cloud).

### Opção A: Gemini Developer API (Studio)
```python
from google import genai

# Requer API Key
client = genai.Client(api_key='SUA_GEMINI_API_KEY')
```

### Opção B: Vertex AI API (Google Cloud)
```python
from google import genai

client = genai.Client(
    vertexai=True, 
    project='seu-project-id', 
    location='us-central1'
)
```

### Uso com Variáveis de Ambiente
O cliente pode detectar configurações automaticamente do ambiente.

*   **Gemini Developer API**:
    ```bash
    export GEMINI_API_KEY='sua-api-key'
    # ou GOOGLE_API_KEY='sua-api-key' (tem precedência)
    ```

*   **Vertex AI**:
    ```bash
    export GOOGLE_GENAI_USE_VERTEXAI=true
    export GOOGLE_CLOUD_PROJECT='seu-project-id'
    export GOOGLE_CLOUD_LOCATION='us-central1'
    ```

```python
# Inicialização automática baseada nas variáveis
client = genai.Client()
```

---

## 3. Gerenciamento de Cliente (Context Managers)

É recomendado usar o cliente dentro de um bloco `with` ou fechá-lo explicitamente para liberar recursos.

### Sync Client (Síncrono)
**Manual:**
```python
client = genai.Client()
# ... operações ...
client.close()
```

**Context Manager (Recomendado):**
```python
with genai.Client() as client:
    response = client.models.generate_content(model='gemini-2.0-flash', contents='Hello')
```

### Async Client (Assíncrono)
**Manual:**
```python
client = genai.Client(...)
aclient = client.aio # Acessa a interface async
# ... operações await ...
await aclient.aclose()
```

**Async Context Manager:**
```python
async with genai.Client().aio as aclient:
    response = await aclient.models.generate_content(
        model='gemini-2.0-flash', 
        contents='Hello'
    )
```

---

## 4. Configurações de Rede (HTTP Options)

### Versão da API
Por padrão, o SDK usa a API `beta`. Para usar versões estáveis ou alpha:

```python
from google.genai import types

# Exemplo para Vertex AI (v1)
client = genai.Client(
    vertexai=True,
    project='pid', location='loc',
    http_options=types.HttpOptions(api_version='v1')
)

# Exemplo para Gemini Dev API (v1alpha)
client = genai.Client(
    api_key='KEY',
    http_options=types.HttpOptions(api_version='v1alpha')
)
```

### Proxy e Base URL
**Variáveis de Ambiente:**
```bash
export HTTPS_PROXY='http://user:pass@proxy:port'
export SSL_CERT_FILE='client.pem'
```

**Custom Base URL (ex: API Gateway):**
```python
client = genai.Client(
    vertexai=True,
    http_options={
        'base_url': 'https://gateway-proxy.com',
        'headers': {'Authorization': 'Bearer token'}
    }
)
```

**Cliente Aiohttp (Mais rápido para Async):**
Requer `pip install google-genai[aiohttp]`. O padrão é `httpx`.

---

## 5. Gerando Conteúdo (`generate_content`)

### Texto para Texto
```python
response = client.models.generate_content(
    model='gemini-2.5-flash', 
    contents='Why is the sky blue?'
)
print(response.text)
```

### Texto para Imagem
```python
from google.genai import types

response = client.models.generate_content(
    model='gemini-2.5-flash-image',
    contents='A cartoon infographic for flying sneakers',
    config=types.GenerateContentConfig(
        response_modalities=["IMAGE"],
        image_config=types.ImageConfig(aspect_ratio="9:16"),
    ),
)

for part in response.parts:
    if part.inline_data:
        part.as_image().show()
```

### Arquivos (Gemini Dev API)
Upload de arquivos e uso no prompt.

```python
# Upload
file = client.files.upload(file='arquivo.txt')

# Uso
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=['Resuma este arquivo:', file]
)
```

### Estrutura do Argumento `contents`
O SDK aceita várias formas de entrada que são convertidas internamente para `list[types.Content]`.

1.  **String Simples:** `contents='Hello'` -> Converte para UserContent.
2.  **Lista de Strings:** `contents=['Hello', 'World']` -> Um único UserContent com múltiplas partes de texto.
3.  **Tipos Específicos:**
    *   `types.Content(role='user', parts=[...])`: Controle total.
    *   `types.Part.from_text('...')`
    *   `types.Part.from_uri(file_uri='...', mime_type='...')`
4.  **Misturando Tipos:** O SDK agrupa automaticamente partes consecutivas de mesmo papel (user/model).

---

## 6. Configurações de Geração

Controle parâmetros como temperatura, tokens e instruções de sistema via `config`.

```python
from google.genai import types

response = client.models.generate_content(
    model='gemini-2.0-flash',
    contents='Explique física quântica',
    config=types.GenerateContentConfig(
        system_instruction='Você é um professor explicar para uma criança de 5 anos.',
        temperature=0.3,
        max_output_tokens=500,
        top_p=0.95,
        top_k=20,
        candidate_count=1,
        stop_sequences=['FIM'],
        safety_settings=[
            types.SafetySetting(
                category='HARM_CATEGORY_HATE_SPEECH',
                threshold='BLOCK_ONLY_HIGH'
            )
        ]
    )
)
```

### Configurações Tipadas (Pydantic)
Todos os parâmetros suportam modelos Pydantic do módulo `types`, o que facilita a validação e autocompletar em IDEs.

---

## 7. Modelos e Listagem

```python
# Listar modelos disponíveis
for model in client.models.list():
    print(model)

# Paginação Assíncrona
async for job in await client.aio.models.list():
    print(job)
```

---

## 8. Chamada de Função (Function Calling)

### Modo Automático (Padrão)
Passe uma função Python pura e o SDK lida com a chamada automaticamente.

```python
def get_current_weather(location: str) -> str:
    """Returns the current weather."""
    return 'sunny'

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents='Weather in Boston?',
    config=types.GenerateContentConfig(
        tools=[get_current_weather] # Chamada automática ativada
    )
)
print(response.text) # O modelo usa o resultado da função para responder
```

### Modo Manual
Se quiser controlar a execução da função ou desativar a chamada automática.

1.  **Desativar Automático:**
    ```python
    config=types.GenerateContentConfig(
        tools=[tool],
        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True)
    )
    ```
2.  **Fluxo Manual:**
    *   Receba a resposta com `function_calls`.
    *   Execute a função localmente.

---

## 9. Chamada de Função Avançada (Advanced Function Calling)

### Modo `ANY` (Forçar Chamada)
Força o modelo a sempre retornar uma chamada de função.

```python
config = types.GenerateContentConfig(
    tools=[get_current_weather],
    tool_config=types.ToolConfig(
        function_calling_config=types.FunctionCallingConfig(mode='ANY')
    ),
    # Desativar execução automática se desejar controlar o loop
    automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True) 
)
```

### Model Context Protocol (MCP) [Experimental]
Suporte experimental para conectar servidores MCP locais como ferramentas.

```python
from mcp import StdioServerParameters
from mcp.client.stdio import stdio_client

# ... (Configuração do servidor MCP) ...
# O SDK gerencia a conexão e chamada automática de ferramentas MCP
```

---

## 10. Respostas Estruturadas (JSON e Enums)

### JSON Schema
Defina o esquema esperado para obter respostas JSON estruturadas.

```python
user_schema = {'type': 'object', 'properties': {'username': {'type': 'string'}}}

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents='Random user',
    config={
        'response_mime_type': 'application/json',
        'response_json_schema': user_schema
    }
)
```

### Pydantic Models
Maneira mais Pythonica de definir esquemas.

```python
from pydantic import BaseModel

class CountryInfo(BaseModel):
    name: str
    population: int

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents='USA info',
    config=types.GenerateContentConfig(
        response_mime_type='application/json',
        response_schema=CountryInfo
    )
)
```

### Enums
Retorna apenas valores definidos num Enum.

```python
class Instrument(Enum):
    PERCUSSION = 'Percussion'
    STRING = 'String'

config={'response_mime_type': 'text/x.enum', 'response_schema': Instrument}
```

---

## 11. Streaming e Async

### Streaming (Sync)
Receba a resposta em pedaços (chunks) à medida que são gerados.

```python
for chunk in client.models.generate_content_stream(model='gemini-2.5-flash', contents='...'):
    print(chunk.text, end='')
```

### Async Client (Métodos `.aio`)
Todos os métodos têm equivalentes assíncronos acessíveis via `.aio`.

```python
# Geração Async
response = await client.aio.models.generate_content(...)

# Streaming Async
async for chunk in await client.aio.models.generate_content_stream(...):
    print(chunk.text)
```

---

## 12. Multimodal Avançado (Imagen e Veo)

### Imagen 3 (Geração de Imagens)
*Suporte via `generate_images`.*

```python
response = client.models.generate_images(
    model='imagen-3.0-generate-002',
    prompt='Umbrella in rain',
    config=types.GenerateImagesConfig(number_of_images=1)
)
response.generated_images[0].image.show()
```
*Disponível também: `upscale_image` e `edit_image` (Vertex AI).*

### Veo (Geração de Vídeos) [Preview]
Suporta Texto-para-Vídeo e Imagem-para-Vídeo.

```python
# Texto para Vídeo
operation = client.models.generate_videos(
    model='veo-2.0-generate-001',
    prompt='Neon cat driving',
    config=types.GenerateVideosConfig(duration_seconds=5)
)

# Polling até concluir
while not operation.done:
    time.sleep(10)
    operation = client.operations.get(operation)

video = operation.response.generated_videos[0].video
```

---

## 13. Outros Recursos (Embeddings, Caches, Tuning, Batches)

### Embeddings
```python
response = client.models.embed_content(
    model='gemini-embedding-001',
    contents='Texto para vetorizar'
)
```

### Context Caching
Cache de contexto para reduzir custos em prompts longos e repetitivos.
```python
cached = client.caches.create(
    model='gemini-2.5-flash',
    config=types.CreateCachedContentConfig(
        contents=[...], # Grandes documentos
        ttl='3600s'
    )
)
# Usar cache na geração
client.models.generate_content(..., config=types.GenerateContentConfig(cached_content=cached.name))
```

### Model Tuning (Fine-tuning)
Apenas Vertex AI. Permite ajustar modelos com datasets personalizados.
`client.tunings.tune(...)`

### Batch Jobs
Processamento em lote para grandes volumes (Vertex AI e Gemini Dev API).
`client.batches.create(...)`

---

## 14. Tratamento de Erros

Use `google.genai.errors.APIError` para capturar exceções da API.

```python
from google.genai import errors

try:
    client.models.generate_content(...)
except errors.APIError as e:
    print(f"Error {e.code}: {e.message}")
```
