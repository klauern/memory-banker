# Memory Banker

**Agentically create Cline-style memory banks for your projects**

Memory Banker is a Python CLI tool that uses OpenAI Agents to intelligently analyze your projects and generate comprehensive memory banks following Cline's memory management principles. These memory banks help AI assistants maintain context and understanding across development sessions.

## Features

- **Agent-Based Analysis**: Uses specialized AI agents to analyze different aspects of your project
- **Complete Memory Bank Structure**: Generates all 6 core Cline-style memory bank files
- **Fast & Intelligent**: Leverages OpenAI's models through the openai-agents framework
- **Configurable**: Customizable timeouts, models, and project paths
- **Any Project Type**: Works with Python, Node.js, Go, Rust, and other project types
- **Update & Refresh**: Keep your memory banks current as your project evolves

## What are Memory Banks?

Memory banks are structured documentation files that help AI assistants understand your project's context, architecture, and current state. Inspired by [Cline's memory management system](https://docs.cline.bot/), they include:

- **`projectbrief.md`** - Foundation document with project scope and requirements
- **`productContext.md`** - Why the project exists and problem space analysis
- **`activeContext.md`** - Current development state and next steps
- **`systemPatterns.md`** - Architecture and design patterns
- **`techContext.md`** - Technology stack and development setup
- **`progress.md`** - What works, what's left, and project evolution

## Installation

### Prerequisites

- Python 3.13 or higher
- OpenAI API key

### Global Installation (Recommended)

For global access to the `memory-banker` command from anywhere:

```bash
git clone https://github.com/yourusername/memory-banker.git
cd memory-banker
uv tool install .
```

After this, `memory-banker` will be available globally. To uninstall later:
```bash
uv tool uninstall memory-banker
```

### Local Development Installation

For local development and testing:

```bash
git clone https://github.com/yourusername/memory-banker.git
cd memory-banker
uv sync
```

### Alternative: Using pip

```bash
git clone https://github.com/yourusername/memory-banker.git
cd memory-banker
pip install -e .
```

## Quick Start

1. **Set your OpenAI API key:**
   ```bash
   export OPENAI_API_KEY=your_api_key_here
   ```

2. **Initialize a memory bank for your project:**
   ```bash
   # If installed globally (recommended)
   memory-banker init

   # If using local development setup
   uv run memory-banker init
   ```

3. **Check the generated files:**
   ```bash
   ls memory-bank/
   # projectbrief.md  productContext.md  activeContext.md
   # systemPatterns.md  techContext.md  progress.md
   ```

## Usage

### Commands

```bash
# Initialize a new memory bank
memory-banker init

# Update existing memory bank files
memory-banker update

# Completely refresh/rebuild the memory bank
memory-banker refresh
```

### Options

```bash
# Use a different project directory
memory-banker --project-path /path/to/project init

# Use a different model
memory-banker --model gpt-4 init

# Set custom timeout (in seconds)
memory-banker --timeout 600 init

# Use custom API key
memory-banker --api-key your_key_here init
```

### Full Example

```bash
# Generate memory bank for a large project with 10-minute timeout
memory-banker --project-path ~/my-big-project --timeout 600 --model gpt-4 init
```

## Configuration

### Environment Variables

- `OPENAI_API_KEY` - Your OpenAI API key (required)

### Supported Models

Any model supported by the OpenAI Agents framework:
- `gpt-4.1-mini` (default) - Fast and cost-effective
- `gpt-4o` - More comprehensive analysis
- `gpt-4` - High-quality detailed analysis
- And many others via LiteLLM integration

### Timeout Settings

- **Default**: 300 seconds (5 minutes) per agent
- **Recommended**: 600 seconds (10 minutes) for complex projects
- **Quick test**: 120 seconds (2 minutes) for simple projects

## Project Structure

```
memory-banker/
├── memory_banker/       # Core package
│   ├── __init__.py     # Package exports
│   ├── main.py         # CLI entry point
│   ├── cli.py          # CLI implementation
│   ├── agents.py       # AI agents for analysis
│   └── memory_bank.py  # Memory bank file management
├── tests/              # Test suite
│   ├── unit/           # Unit tests
│   └── integration/    # Integration tests
├── pyproject.toml      # Project configuration
└── README.md          # This file
```

## How It Works

1. **Project Analysis**: Scans your project structure, files, git history, and dependencies
2. **Specialized Agents**: Six specialized AI agents analyze different aspects:
   - **ProjectBriefAgent**: Creates foundation document with scope and requirements
   - **ProductContextAgent**: Analyzes why the project exists and problem space
   - **ActiveContextAgent**: Determines current development state and next steps
   - **SystemPatternsAgent**: Documents architecture and design patterns
   - **TechContextAgent**: Captures technology stack and setup instructions
   - **ProgressAgent**: Tracks what works, what's left, and project evolution
3. **Memory Bank Generation**: Creates structured markdown files in `memory-bank/` directory

## Keeping Memory Banks Updated

Memory banks should be updated as your project evolves:

```bash
# Quick update of existing files
memory-banker update

# Complete regeneration (recommended after major changes)
memory-banker refresh
```

## Example Output

After running `memory-banker init`, you'll get a `memory-bank/` directory with comprehensive documentation like:

**projectbrief.md**:
```markdown
# Project Brief: My Awesome Project

## Project Overview
A comprehensive web application that solves X problem by providing Y solution...

## Core Requirements and Goals
- Implement user authentication and authorization
- Provide real-time data synchronization
- Support scalable microservices architecture
...
```

**activeContext.md**:
```markdown
# Active Context

## Current Work Focus
Currently implementing the user authentication system using JWT tokens...

## Recent Changes
- Added user registration endpoint
- Implemented password hashing with bcrypt
- Set up JWT token generation and validation
...
```

## Troubleshooting

### Common Issues

**Import Errors**:
```bash
# If installed globally
memory-banker --help

# If using local development setup
uv run memory-banker --help
```

**API Errors**:
```bash
# Check your API key
echo $OPENAI_API_KEY
```

**Timeout Issues**:
```bash
# Increase timeout for complex projects
memory-banker --timeout 900 init
```

**Permission Errors**:
```bash
# Make sure the directory is writable
ls -la
```

## Development

### Installing for Development

```bash
git clone https://github.com/yourusername/memory-banker.git
cd memory-banker
uv sync --dev
```

### Running Tests

```bash
uv run pytest
```

### Local Testing

Test the CLI locally during development:
```bash
uv run memory-banker --help
uv run memory-banker init
```

### Global Installation for Testing

To test the global installation:
```bash
uv tool install .
memory-banker --help
uv tool uninstall memory-banker  # When done testing
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by [Cline's memory management system](https://docs.cline.bot/)
- Built with [OpenAI Agents](https://github.com/openai/openai-agents-python)
- Uses [Click](https://click.palletsprojects.com/) for the CLI interface

## Support

- [Report bugs](https://github.com/yourusername/memory-banker/issues)
- [Request features](https://github.com/yourusername/memory-banker/issues)
- [Read the docs](https://github.com/yourusername/memory-banker/wiki)

---

**Happy memory banking!**
