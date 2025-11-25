"""
Configuration management for LM Studio MCP Server
"""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class LMStudioConfig:
    """LM Studio server configuration"""
    url: str = "http://192.168.0.32:7002"
    timeout: float = 120.0  # Default timeout for LLM requests


@dataclass
class MCPConfig:
    """MCP server configuration"""
    host: str = "0.0.0.0"
    port: int = 8080
    log_level: str = "info"


@dataclass
class Config:
    """Main configuration"""
    lmstudio: LMStudioConfig
    mcp: MCPConfig


def get_config() -> Config:
    """Get configuration from environment variables with defaults"""

    lmstudio_config = LMStudioConfig(
        url=os.getenv("LMSTUDIO_URL", "http://192.168.0.32:7002"),
        timeout=float(os.getenv("LMSTUDIO_TIMEOUT", "120.0")),
    )

    mcp_config = MCPConfig(
        host=os.getenv("MCP_SERVER_HOST", "0.0.0.0"),
        port=int(os.getenv("MCP_SERVER_PORT", "8080")),
        log_level=os.getenv("MCP_LOG_LEVEL", "info"),
    )

    return Config(
        lmstudio=lmstudio_config,
        mcp=mcp_config,
    )
