# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Memory Banker is a Python CLI tool that uses AI agents to intelligently analyze projects and generate comprehensive memory banks following Cline's memory management principles. It uses an agent-based architecture with specialized AI agents to create structured documentation that helps AI assistants maintain context across development sessions.

## Common Commands

### Development Environment
```bash
# Install dependencies for development
task install

# Complete development setup (install + checks + tests)
task setup-dev

# Install for production use
task install-prod
```

### Code Quality
```bash
# Auto-fix all linting and formatting issues
task fix

# Run all quality checks (lint + format check)
task check

# Individual quality tasks
task lint          # Check code with ruff
task lint-fix      # Auto-fix linting issues
task format        # Format code with ruff
task format-check  # Check formatting without changes
```

### Testing
```bash
# Run all tests
task test

# Run tests with coverage report
task test-cov

# Run single test file
uv run pytest tests/unit/test_cli.py

# Run specific test
uv run pytest tests/unit/test_cli.py::TestMemoryBankerCLI::test_init_success -v
```

### Application Usage
```bash
# Run the CLI tool
task run
# or directly:
uv run memory-banker --help

# Install as a global tool
uv tool install .

# Run development version
memory-banker init --project-path /path/to/project
```

### Development Workflow
```bash
# Pre-commit checks (format + lint + test)
task pre-commit

# CI checks (all quality + coverage)
task ci

# Clean build artifacts
task clean
```

## Architecture

### Core Components

**Agent-Based Architecture**: The system follows a modular, three-layer design:

1. **CLI Layer** (`memory_banker/cli.py`): Click-based interface handling commands (`init`, `update`, `refresh`) and configuration
2. **Agent Layer** (`memory_banker/agents.py`): Orchestrates 6 specialized AI agents using OpenAI Agents framework
3. **Memory Management** (`memory_banker/memory_bank.py`): Handles file operations and directory structure

### Agent Specialization

The system uses 6 specialized agents that build contextually upon each other:
- `ProjectBriefAgent`: Foundation document with scope and requirements
- `ProductContextAgent`: Problem space analysis  
- `ActiveContextAgent`: Current development state and next steps
- `SystemPatternsAgent`: Architecture and design patterns
- `TechContextAgent`: Technology stack and setup instructions
- `ProgressAgent`: Status tracking and project evolution

Each agent receives the full project context plus outputs from previous agents, creating a coherent knowledge base.

### Memory Bank Structure

Generated memory banks follow Cline's methodology with 6 interconnected files in `memory-bank/`:
```
memory-bank/
├── projectbrief.md      # Foundation and scope
├── productContext.md    # Why and problem space
├── activeContext.md     # Current state and priorities  
├── systemPatterns.md    # Architecture patterns
├── techContext.md       # Technical implementation
└── progress.md          # Status and evolution
```

### Technology Integration

- **OpenAI Agents Framework**: Provides structured agent execution with LiteLLM integration
- **Click**: Professional CLI with configuration management and environment variable support
- **Project Analysis**: Comprehensive scanning of file structure, git history, dependencies, and documentation
- **Model Flexibility**: Supports any LiteLLM-compatible model (gpt-4o-mini default, gpt-4o, gpt-4, etc.)

## Development Notes

### Project Structure
```
memory_banker/           # Core package
├── __init__.py
├── cli.py              # CLI entry point and commands
├── agents.py           # AI agent orchestration
└── memory_bank.py      # File and directory management

tests/                  # Comprehensive test suite
├── conftest.py         # Global test configuration
├── fixtures/conftest.py # Rich test fixtures (Python, Node.js, empty projects)
├── unit/               # Component testing
└── integration/        # End-to-end workflow testing
```

### Testing Strategy

- **Unit Tests**: Individual component behavior with mocking
- **Integration Tests**: Full CLI workflow testing with real fixtures
- **Mock Infrastructure**: Prevents API calls during testing with sample agent responses
- **Coverage Target**: 80%+ coverage requirement in pytest.ini
- **Async Support**: Full async/await testing for agent operations

### Configuration Management

- **pyproject.toml**: Modern Python packaging with entry points
- **Taskfile.yml**: Task runner for development automation using uv
- **pytest.ini**: Testing configuration with coverage requirements
- **mise.toml**: Python version specification

### Important Patterns

1. **Agent Timeout Handling**: All agent operations have configurable timeouts (default 300s)
2. **Error Propagation**: Agents fail gracefully with informative error messages
3. **Project Type Detection**: Automatic detection of Python, Node.js, and other project types
4. **Incremental Updates**: `update` command preserves manual edits while refreshing analysis
5. **Environment Management**: API keys via environment variables or CLI options

### Entry Point Configuration

The CLI entry point is configured in `pyproject.toml` as:
```toml
[project.scripts]
memory-banker = "memory_banker.cli:main"
```

This enables both `uv run memory-banker` and `uv tool install .` installation methods.

### Quality Standards

- **Ruff**: Used for both linting and formatting (replaces flake8 + black)
- **Type Safety**: Function signatures use type hints where appropriate
- **Error Handling**: Comprehensive error messages for user guidance
- **Documentation**: Docstrings for all public methods and classes

This codebase represents a mature Python project with professional development practices, comprehensive testing, and a well-architected agent-based approach to automated documentation generation.