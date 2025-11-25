# LM Studio MCP Server

FastMCP-based server providing LM Studio LLM capabilities via the Model Context Protocol (MCP).

## Features

- **Model Management**: List available models in LM Studio
- **Chat Completions**: Generate conversational responses with context
- **Text Completions**: Simple prompt-based text generation
- **Embeddings**: Create vector embeddings for semantic search
- **Health Monitoring**: Built-in health checks for Docker/K8s

## Architecture

This MCP server acts as a bridge between the MCP protocol and LM Studio's OpenAI-compatible API:

```
MCP Client → LM Studio MCP Server → LM Studio API (http://192.168.0.32:7002)
```

## Available Tools

### `lmstudio_list_models`
List all available models in LM Studio.

**Returns**: Model list with IDs and metadata

### `lmstudio_chat_completion`
Generate chat completions with conversation context.

**Parameters**:
- `messages` (required): Array of message objects with `role` and `content`
- `model` (optional): Model ID to use
- `temperature` (default: 0.7): Sampling temperature (0.0-2.0)
- `max_tokens` (default: 2048): Maximum tokens to generate
- `top_p` (default: 0.95): Nucleus sampling parameter

**Example**:
```json
{
  "messages": [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is MCP?"}
  ],
  "temperature": 0.7,
  "max_tokens": 1024
}
```

### `lmstudio_completion`
Generate simple text completions.

**Parameters**:
- `prompt` (required): Text prompt to complete
- `model` (optional): Model ID to use
- `temperature` (default: 0.7): Sampling temperature
- `max_tokens` (default: 2048): Maximum tokens to generate
- `stop` (optional): Stop sequences

### `lmstudio_create_embeddings`
Create vector embeddings for text.

**Parameters**:
- `input` (required): String or array of strings to embed
- `model` (optional): Embedding model ID

**Returns**: Vector embeddings array

### `lmstudio_health_check`
Check LM Studio server connectivity.

**Returns**: Health status and connectivity information

## Configuration

Environment variables:

- `LMSTUDIO_URL`: LM Studio API URL (default: `http://192.168.0.32:7002`)
- `LMSTUDIO_TIMEOUT`: Request timeout in seconds (default: `120.0`)
- `MCP_SERVER_HOST`: MCP server bind address (default: `0.0.0.0`)
- `MCP_SERVER_PORT`: MCP server port (default: `8080`)
- `MCP_LOG_LEVEL`: Logging level (default: `info`)

## Docker Deployment

### Build
```bash
docker build -t lmstudio-mcp-server .
```

### Run Standalone
```bash
docker run -p 9070:8080 \
  -e LMSTUDIO_URL=http://192.168.0.32:7002 \
  lmstudio-mcp-server
```

### Docker Compose Integration
The server is integrated into the main docker-compose.yml:

```yaml
services:
  lmstudio-mcp-server:
    build: ./lmstudio-mcp-server
    ports:
      - "9070:8080"
    environment:
      LMSTUDIO_URL: http://192.168.0.32:7002
      LMSTUDIO_TIMEOUT: "120.0"
```

## Endpoints

- `/` - Server information
- `/health` - Health check endpoint (for Docker healthcheck)
- `/sse` - MCP Server-Sent Events endpoint
- `/messages/` - MCP messages endpoint

## Testing Connection

```bash
# Check health
curl http://localhost:9070/health

# List models via MCP
curl http://localhost:9070/sse
```

## Requirements

- Python 3.11+
- LM Studio running and accessible at configured URL
- Network connectivity to LM Studio server

## Notes

- LM Studio must have "Serve on Local Network" enabled
- LM Studio must have "Allow per-request MCPs" enabled
- The server acts as a proxy, so LM Studio availability is required
- Streaming is not supported in MCP tools (responses are complete)
