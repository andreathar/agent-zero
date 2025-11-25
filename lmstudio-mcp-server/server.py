"""
LM Studio MCP Server
FastMCP-based server providing LM Studio LLM tools via MCP protocol
"""

import asyncio
import logging
import sys
from typing import Optional, List, Dict, Any
from contextlib import asynccontextmanager

from fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
import uvicorn
import httpx

from config import get_config


# Configure logging
cfg = get_config()
logging.basicConfig(
    level=getattr(logging, cfg.mcp.log_level.upper(), logging.INFO),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("lmstudio-mcp-server")


# Create MCP server
mcp = FastMCP(
    name="lmstudio",
    version="1.0.0",
)


# ============================================================================
# HTTP Client for LM Studio API
# ============================================================================

async def get_http_client() -> httpx.AsyncClient:
    """Get configured HTTP client for LM Studio API"""
    return httpx.AsyncClient(
        base_url=cfg.lmstudio.url,
        timeout=httpx.Timeout(cfg.lmstudio.timeout, connect=10.0),
        headers={"Content-Type": "application/json"},
    )


# ============================================================================
# Model Management Tools
# ============================================================================

@mcp.tool(
    name="lmstudio_list_models",
    description="List all available models in LM Studio"
)
async def tool_list_models():
    """List available models"""
    try:
        async with get_http_client() as client:
            response = await client.get("/v1/models")
            response.raise_for_status()
            data = response.json()

            models = []
            for model in data.get("data", []):
                models.append({
                    "id": model.get("id"),
                    "created": model.get("created"),
                    "owned_by": model.get("owned_by", "lmstudio"),
                })

            return {
                "status": "success",
                "models": models,
                "count": len(models)
            }
    except Exception as e:
        logger.error(f"Error listing models: {e}")
        return {
            "status": "error",
            "error": str(e)
        }


# ============================================================================
# Text Generation Tools
# ============================================================================

@mcp.tool(
    name="lmstudio_chat_completion",
    description="Generate a chat completion using LM Studio. Supports conversation history with messages array."
)
async def tool_chat_completion(
    messages: List[Dict[str, str]],
    model: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 2048,
    top_p: float = 0.95,
    stream: bool = False,
):
    """
    Generate chat completion

    Args:
        messages: List of message dicts with 'role' and 'content' keys
                 Example: [{"role": "user", "content": "Hello"}]
        model: Model ID to use (optional, uses LM Studio default if not specified)
        temperature: Sampling temperature (0.0 to 2.0)
        max_tokens: Maximum tokens to generate
        top_p: Nucleus sampling parameter
        stream: Whether to stream the response (not supported in MCP, returns full response)
    """
    try:
        async with get_http_client() as client:
            payload = {
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "top_p": top_p,
                "stream": False,  # MCP tools don't support streaming
            }

            if model:
                payload["model"] = model

            response = await client.post("/v1/chat/completions", json=payload)
            response.raise_for_status()
            data = response.json()

            return {
                "status": "success",
                "message": data["choices"][0]["message"],
                "content": data["choices"][0]["message"]["content"],
                "model": data.get("model"),
                "usage": data.get("usage", {}),
                "finish_reason": data["choices"][0].get("finish_reason"),
            }
    except Exception as e:
        logger.error(f"Error in chat completion: {e}")
        return {
            "status": "error",
            "error": str(e)
        }


@mcp.tool(
    name="lmstudio_completion",
    description="Generate a text completion using LM Studio. Simple prompt-based completion without conversation context."
)
async def tool_completion(
    prompt: str,
    model: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 2048,
    top_p: float = 0.95,
    stop: Optional[List[str]] = None,
):
    """
    Generate text completion

    Args:
        prompt: The text prompt to complete
        model: Model ID to use (optional)
        temperature: Sampling temperature (0.0 to 2.0)
        max_tokens: Maximum tokens to generate
        top_p: Nucleus sampling parameter
        stop: List of stop sequences
    """
    try:
        async with get_http_client() as client:
            payload = {
                "prompt": prompt,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "top_p": top_p,
                "stream": False,
            }

            if model:
                payload["model"] = model
            if stop:
                payload["stop"] = stop

            response = await client.post("/v1/completions", json=payload)
            response.raise_for_status()
            data = response.json()

            return {
                "status": "success",
                "text": data["choices"][0]["text"],
                "model": data.get("model"),
                "usage": data.get("usage", {}),
                "finish_reason": data["choices"][0].get("finish_reason"),
            }
    except Exception as e:
        logger.error(f"Error in completion: {e}")
        return {
            "status": "error",
            "error": str(e)
        }


# ============================================================================
# Embeddings Tools
# ============================================================================

@mcp.tool(
    name="lmstudio_create_embeddings",
    description="Generate embeddings for text using LM Studio. Returns vector representations for semantic search."
)
async def tool_create_embeddings(
    input: str | List[str],
    model: Optional[str] = None,
):
    """
    Create embeddings

    Args:
        input: Text string or list of strings to embed
        model: Model ID to use for embeddings (optional)
    """
    try:
        async with get_http_client() as client:
            payload = {
                "input": input,
            }

            if model:
                payload["model"] = model

            response = await client.post("/v1/embeddings", json=payload)
            response.raise_for_status()
            data = response.json()

            embeddings = [item["embedding"] for item in data["data"]]

            return {
                "status": "success",
                "embeddings": embeddings,
                "model": data.get("model"),
                "usage": data.get("usage", {}),
                "count": len(embeddings),
            }
    except Exception as e:
        logger.error(f"Error creating embeddings: {e}")
        return {
            "status": "error",
            "error": str(e)
        }


# ============================================================================
# Health Check Tool
# ============================================================================

@mcp.tool(
    name="lmstudio_health_check",
    description="Check LM Studio server connectivity and health"
)
async def tool_health_check():
    """Health check for LM Studio server"""
    try:
        async with get_http_client() as client:
            response = await client.get("/v1/models")
            response.raise_for_status()

            return {
                "status": "success",
                "message": "LM Studio is healthy and reachable",
                "url": cfg.lmstudio.url,
            }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "error",
            "error": str(e),
            "url": cfg.lmstudio.url,
        }


# ============================================================================
# HTTP Health Endpoint (for Docker healthcheck)
# ============================================================================

async def health_endpoint(request):
    """HTTP health check endpoint for Docker/k8s"""
    result = await tool_health_check()
    if result.get("status") == "success":
        return JSONResponse({"status": "healthy"}, status_code=200)
    return JSONResponse({"status": "unhealthy", "error": result.get("error")}, status_code=503)


async def root_endpoint(request):
    """Root endpoint with server info"""
    return JSONResponse({
        "name": "lmstudio-mcp",
        "version": "1.0.0",
        "status": "running",
        "lmstudio_url": cfg.lmstudio.url,
        "endpoints": {
            "health": "/health",
            "mcp_sse": "/sse",
            "mcp_messages": "/messages/",
        },
    })


# ============================================================================
# Application Lifespan and Setup
# ============================================================================

@asynccontextmanager
async def lifespan(app):
    """Application lifespan context manager"""
    logger.info(f"Starting LM Studio MCP Server on {cfg.mcp.host}:{cfg.mcp.port}")
    logger.info(f"LM Studio URL: {cfg.lmstudio.url}")
    yield
    logger.info("Shutting down LM Studio MCP Server")


# Build the application
routes = [
    Route("/", root_endpoint),
    Route("/health", health_endpoint),
]

# Create the Starlette app
app = Starlette(
    routes=routes,
    lifespan=lifespan,
)

# Mount MCP SSE endpoint
app.mount("/", mcp.sse_app())


if __name__ == "__main__":
    uvicorn.run(
        app,
        host=cfg.mcp.host,
        port=cfg.mcp.port,
        log_level=cfg.mcp.log_level,
    )
