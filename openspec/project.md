# Project Context

## Purpose
To provide a comprehensive, AI-assisted development environment for creating Unity multiplayer games with integrated ML-Agents. The project, "MLcreator", leverages Agent Zero to automate tasks, manage documentation, and assist in coding complex systems like Unity Netcode for GameObjects and DOTS. It aims to bridge the gap between advanced AI agents and game development workflows.

## Tech Stack
- **Core Framework**: Agent Zero (Python)
- **Game Engine**: Unity 6000.2.10f1
- **ML/AI**: Unity ML-Agents v3+, OpenAI, Anthropic, Gemini
- **Vector Database**: Qdrant (for Knowledge Base/RAG)
- **Multiplayer**: Unity Netcode for GameObjects
- **Backend**: Supabase
- **Infrastructure**: Docker, Docker Compose
- **Scripting**: C# (Unity), Python (Automation/Agent Tools)

## Project Conventions

### Code Style
- **C# (Unity)**: Follow standard Unity C# conventions. PascalCase for public members/methods, camelCase for private fields (often with underscore prefix `_`).
- **Python**: PEP 8 style guide.
- **Documentation**: Extensive use of Foam tags and wikilinks for knowledge graph integration.

### Architecture Patterns
- **Unity**: 
    - **DOTS**: Data-Oriented Technology Stack (Entities) for performance-critical systems.
    - **Netcode**: Server-authoritative or shared-state architecture suitable for Netcode for GameObjects.
    - **ML-Agents**: Integration of learning agents within the game loop.
- **Agent Zero**: 
    - **RAG**: Retrieval-Augmented Generation using Qdrant to index code and documentation.
    - **MCP**: Model Context Protocol for server-client tool communication.

### Testing Strategy
- **Unity**: PlayMode and EditMode tests. Automated testing of Netcode scenarios.
- **ML-Agents**: Training validation and curriculum learning verification.
- **Agent**: Verification of tool execution and MCP server connectivity.

### Git Workflow
- Standard Git flow.
- **Unity Specifics**: 
    - Force Text Serialization for Assets.
    - Visible Meta Files.
    - Strict `.gitignore` for Unity generated files (Library, Temp, Obj).

## Domain Context
- **Unity Development**: Deep understanding of Unity's component system, prefabs, and asset management.
- **Multiplayer Networking**: Concepts of synchronization, state replication, RPCs, and network variables.
- **Reinforcement Learning**: Understanding of Agents, Observations, Actions, and Rewards in the context of Unity ML-Agents.

## Important Constraints
- **Unity Version**: Must strictly adhere to Unity 6000.2.10f1 to ensure compatibility with Docker containers and packages.
- **Docker**: All agent tools and servers should run within the defined Docker environment.
- **Performance**: Real-time constraints for game logic and ML inference.

## External Dependencies
- **Unity Services**: Licensing, Asset Store.
- **LLM Providers**: OpenAI, Anthropic, Google (Gemini) API access.
- **Supabase**: Database and Authentication services.
- **Docker Hub**: For pulling base images.
