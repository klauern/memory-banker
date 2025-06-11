"""Test fixtures for memory-banker tests."""

import tempfile
from pathlib import Path
from typing import Dict, Any
import pytest
from unittest.mock import Mock

from agents.extensions.models.litellm_model import LitellmModel


@pytest.fixture
def temp_project_dir():
    """Create a temporary directory for test projects."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


@pytest.fixture
def python_project(temp_project_dir):
    """Create a minimal Python project structure."""
    project_path = temp_project_dir / "test_python_project"
    project_path.mkdir()
    
    # Create pyproject.toml
    pyproject_content = """[project]
name = "test-project"
version = "0.1.0"
description = "A test Python project"
requires-python = ">=3.13"
dependencies = [
    "click>=8.0.0",
    "requests>=2.25.0",
]

[project.scripts]
test-cli = "test_project.main:cli"
"""
    (project_path / "pyproject.toml").write_text(pyproject_content)
    
    # Create README.md
    readme_content = """# Test Project

This is a test Python project for testing memory-banker.

## Features

- Command line interface
- HTTP requests handling
- Configuration management

## Installation

```bash
pip install -e .
```

## Usage

```bash
test-cli --help
```
"""
    (project_path / "README.md").write_text(readme_content)
    
    # Create source code
    src_dir = project_path / "test_project"
    src_dir.mkdir()
    (src_dir / "__init__.py").write_text('"""Test project package."""\n__version__ = "0.1.0"')
    
    main_py_content = """\"\"\"Main CLI module for test project.\"\"\"

import click
import requests


@click.group()
def cli():
    \"\"\"Test CLI application.\"\"\"
    pass


@cli.command()
@click.option("--url", default="https://api.example.com", help="API URL")
def fetch(url):
    \"\"\"Fetch data from API.\"\"\"
    response = requests.get(url)
    click.echo(f"Status: {response.status_code}")


if __name__ == "__main__":
    cli()
"""
    (src_dir / "main.py").write_text(main_py_content)
    
    # Create .gitignore
    gitignore_content = """__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
"""
    (project_path / ".gitignore").write_text(gitignore_content)
    
    return project_path


@pytest.fixture
def nodejs_project(temp_project_dir):
    """Create a minimal Node.js project structure."""
    project_path = temp_project_dir / "test_nodejs_project"
    project_path.mkdir()
    
    # Create package.json
    package_json_content = """{
  "name": "test-nodejs-project",
  "version": "1.0.0",
  "description": "A test Node.js project",
  "main": "index.js",
  "scripts": {
    "start": "node index.js",
    "test": "jest"
  },
  "dependencies": {
    "express": "^4.18.0",
    "axios": "^1.0.0"
  },
  "devDependencies": {
    "jest": "^29.0.0"
  }
}"""
    (project_path / "package.json").write_text(package_json_content)
    
    # Create README.md
    readme_content = """# Test Node.js Project

A simple Express.js application for testing.

## Installation

```bash
npm install
```

## Usage

```bash
npm start
```
"""
    (project_path / "README.md").write_text(readme_content)
    
    # Create index.js
    index_js_content = """const express = require('express');
const axios = require('axios');

const app = express();
const port = process.env.PORT || 3000;

app.get('/', (req, res) => {
  res.json({ message: 'Hello World!' });
});

app.get('/api/data', async (req, res) => {
  try {
    const response = await axios.get('https://jsonplaceholder.typicode.com/posts/1');
    res.json(response.data);
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch data' });
  }
});

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
"""
    (project_path / "index.js").write_text(index_js_content)
    
    return project_path


@pytest.fixture
def empty_project(temp_project_dir):
    """Create an empty project directory."""
    project_path = temp_project_dir / "empty_project"
    project_path.mkdir()
    return project_path


@pytest.fixture
def mock_llm_model():
    """Create a mock LLM model for testing."""
    mock_model = Mock(spec=LitellmModel)
    mock_model.model = "gpt-4o-mini"
    mock_model.api_key = "test-api-key"
    return mock_model


@pytest.fixture
def sample_project_context():
    """Sample project context data for testing."""
    return """
PROJECT ANALYSIS CONTEXT

Project Path: /test/project
Project Name: test-project

=== PROJECT STRUCTURE ===
test-project/
├── pyproject.toml
├── README.md
├── test_project/
│   ├── __init__.py
│   └── main.py
└── .gitignore

=== KEY FILES CONTENT ===

--- pyproject.toml ---
[project]
name = "test-project"
version = "0.1.0"

--- README.md ---
# Test Project
This is a test project.

=== GIT INFORMATION ===
Current branch: main
Working directory clean

Please analyze this project thoroughly to understand its purpose, architecture, current state, and context.
"""


@pytest.fixture
def sample_agent_responses():
    """Sample responses from different agents."""
    return {
        "projectbrief": """# Project Brief: Test Project

## Project Overview
Test project for memory banker validation.

## Core Requirements and Goals
- Validate memory bank generation
- Test agent functionality
- Ensure proper structure

## Target Users and Use Cases
- Developers testing memory banker
- Quality assurance validation

## Project Scope Definition
- Limited to testing functionality
- No production use intended

## Foundational Decisions
- Use minimal viable structure
- Focus on core validation patterns
""",
        
        "productContext": """# Product Context

## Why This Project Exists
This project exists to validate memory banker functionality.

## Problem Statement
Need to test memory bank generation processes.

## How It Should Work
Should generate comprehensive memory banks from minimal input.

## User Experience Goals
- Clear validation of functionality
- Comprehensive test coverage

## Market and Ecosystem Context
- Testing tool in development
- Part of memory banker validation suite

## Business and Strategic Value
- Ensures quality of memory banker tool
- Validates agent-based approach
""",
        
        "activeContext": """# Active Context

## Current Work Focus
Testing memory banker functionality and validation.

## Recent Changes and Progress
- Set up test project structure
- Configured basic dependencies
- Created minimal viable codebase

## Next Steps and Priorities
- Complete test validation
- Verify all memory bank files generated correctly
- Ensure agent responses are comprehensive

## Active Decisions and Considerations
- Testing approach and coverage
- Validation criteria for success

## Important Patterns and Preferences
- Minimal viable test structures
- Comprehensive validation approaches

## Learnings and Project Insights
- Memory banker requires structured input
- Agent responses depend on project complexity

## Current Context for AI Assistance
- Focus on validation and testing
- Ensure comprehensive coverage
""",
        
        "systemPatterns": """# System Patterns

## System Architecture Overview
Simple test project with minimal dependencies.

## Key Technical Decisions
- Use Python packaging standards
- Minimal external dependencies
- Focus on testability

## Component Relationships and Dependencies
- Core module with CLI interface
- Standard Python project structure

## Design Patterns in Use
- Command pattern for CLI
- Module-based organization

## Critical Implementation Paths
- CLI command processing
- Basic functionality validation

## Integration and Extension Points
- Standard Python packaging
- Click-based CLI interface

## Quality and Maintainability Patterns
- Standard project structure
- Clear module organization
""",
        
        "techContext": """# Technical Context

## Technologies Used
- Python 3.13+
- Click for CLI
- Standard packaging with pyproject.toml

## Development Setup and Environment
1. Create virtual environment
2. Install dependencies
3. Run tests

## Technical Constraints and Requirements
- Python 3.13+ required
- Minimal external dependencies

## Dependencies and External Integrations
- Click for CLI interface
- Standard Python libraries

## Tool Usage Patterns and Conventions
- Standard Python development practices
- pytest for testing
- pyproject.toml for packaging

## Development Workflow and Standards
- Standard Python conventions
- Clear module organization
- Comprehensive testing

## Operational Context
- Local development only
- No production deployment

## Troubleshooting and Debugging
- Use standard Python debugging tools
- Check dependency versions
- Validate environment setup
""",
        
        "progress": """# Progress Tracker

## What Works (Completed and Functional)
- Basic project structure established
- Core dependencies configured
- Minimal CLI interface implemented

## What's Left to Build
- Additional features as needed
- Extended test coverage
- Documentation improvements

## Current Status and Development Stage
- Prototype/testing phase
- Basic functionality validated
- Ready for extended testing

## Known Issues and Limitations
- Minimal feature set
- Limited to testing purposes
- No production readiness

## Evolution of Project Decisions
- Started with minimal requirements
- Focused on testing needs
- Evolved based on validation requirements

## Technical Debt and Refactoring Needs
- None identified for test project
- Maintain minimal scope

## Success Metrics and Progress Indicators
- All tests pass
- Memory bank generation successful
- Validation criteria met

## Risk Assessment and Mitigation
- Low risk due to testing scope
- No production dependencies
- Contained validation environment
"""
    }