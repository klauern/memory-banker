# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Memory Banker is a Python CLI tool that uses AI agents to automatically generate "Cline-style memory banks" for software projects. It requires Python 3.13+ and uses OpenAI's models through the openai-agents framework to analyze codebases and create structured documentation.

## Common Commands

### Development Setup
```bash
# Install dependencies (using uv - preferred)
uv sync --dev

# Alternative with pip
pip install -e .[dev]
```

### Task Automation (using Taskfile)
```bash
# Install and run all development checks
task setup-dev

# Code quality
task check          # Run lint + format checks
task fix            # Auto-fix all issues
task lint           # Linting only
task format         # Format code

# Testing
task test           # Run all tests
task test-cov       # Run with coverage
task test-verbose   # Verbose output

# Pre-commit workflow
task pre-commit     # Format, lint, and test

# Application
task run            # Run the CLI app
```

### CLI Usage
```bash
# Local development
uv run memory-banker init
uv run memory-banker update

# If installed globally
memory-banker init --project-path /path/to/project --model gpt-4
```

### Testing Individual Components
```bash
# Run specific test files
pytest tests/unit/test_agents.py -v
pytest tests/integration/ -v

# Run tests with coverage
pytest --cov=memory_banker --cov-report=html

# Run only unit tests
pytest -m unit

# Run only integration tests  
pytest -m integration
```

## Architecture

### Core Components

**CLI Layer** (`memory_banker/main.py` and `memory_banker/cli.py`):
- Click-based CLI with commands: `init`, `update`, `refresh`
- `MemoryBankerCLI` class orchestrates the entire process
- Handles global options (project-path, model, api-key, timeout)

**Agent System** (`memory_banker/agents.py`):
- `MemoryBankAgents` coordinates 6 specialized AI agents
- Each agent analyzes different aspects: ProjectBrief, ProductContext, ActiveContext, SystemPatterns, TechContext, Progress
- Built on `openai-agents` framework with LiteLLM model integration

**Memory Bank Management** (`memory_banker/memory_bank.py`):
- `MemoryBank` class handles file I/O and directory management
- Generates 6 core markdown files following Cline's memory system
- Manages memory-bank/ directory structure

### Data Flow
1. CLI parses commands and options
2. `MemoryBankerCLI` initializes LiteLLM model and agents
3. `MemoryBankAgents` analyzes project structure and content
4. Each specialized agent generates content for their memory bank file
5. `MemoryBank` persists results to filesystem

### Testing Architecture
- **Unit tests**: Mock external dependencies (LLM calls, file system)
- **Integration tests**: Test full CLI workflows end-to-end
- **Fixtures**: Provide realistic project structures (Python, Node.js, empty)
- **Async support**: Full pytest-asyncio integration for async/await patterns

## Key Files and Locations

- **Entry point**: `memory_banker/main.py:cli()` (Click command group)
- **Main orchestration**: `memory_banker/cli.py:MemoryBankerCLI` 
- **Agent definitions**: `memory_banker/agents.py` (6 specialized agent classes)
- **File management**: `memory_banker/memory_bank.py:MemoryBank`
- **Test configuration**: `pytest.ini` (test markers and coverage settings)
- **Task automation**: `Taskfile.yml` (development workflow)
- **Package config**: `pyproject.toml` (deps, scripts, tool config)

## Development Environment

### Required Tools
- **Python 3.13+** (cutting edge requirement)
- **uv** for fast dependency management (preferred over pip)
- **mise** for development environment management
- **Task** for automation (via Taskfile.yml)

### Configuration Files
- `pyproject.toml`: Modern Python packaging, dependencies, ruff configuration
- `mise.toml`: Development environment tool management  
- `uv.lock`: Dependency lock file for reproducible builds
- `pytest.ini`: Test configuration with custom markers
- `Taskfile.yml`: Comprehensive development task automation

### Code Quality Setup
- **Ruff**: Combined linting and formatting (replaces black, flake8, isort)
- **Coverage target**: 80% minimum with HTML reports
- **Pre-commit workflow**: Integrated via task automation