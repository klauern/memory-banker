# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Memory Banker is a Python application configured with pyproject.toml. The project requires Python 3.12 or higher and is currently in early development stages.

## Common Commands

### Running the Application
```bash
python main.py
```

### Package Management
Since this project uses pyproject.toml, you can install dependencies with:
```bash
pip install -e .
```

## Architecture

The project currently has a minimal structure:
- `main.py`: Entry point with a simple main() function
- `pyproject.toml`: Project configuration and dependencies
- No external dependencies are currently defined

## Development Notes

This is a new project with minimal scaffolding. The main application logic is in `main.py:main()` function.