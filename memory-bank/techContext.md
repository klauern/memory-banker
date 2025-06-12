# techContext.md

## Technologies Used

### Programming Languages and Versions
- **Python 3.13+**  
  The project requires Python version 3.13 or higher as specified in `pyproject.toml`, leveraging the latest language features and standard library improvements.

### Frameworks and Libraries
- **click >= 8.2.1**  
  Command line interface creation and parsing, primary CLI framework used to implement the user interface. See `memory_banker/cli.py`.  
- **openai-agents[litellm] >= 0.0.17**  
  Core AI agent framework interacting with OpenAI API and LiteLLM integration for AI-driven project analysis and memory bank creation. Provides abstraction over OpenAI calls and agent orchestration.  
- **pytest >= 8.4.0** (dev dependency)  
  Testing framework for unit, integration, and API tests. Used extensively under `/tests` with support for async tests via `pytest-asyncio`.  
- **ruff >= 0.8.0** (dev dependency)  
  Linting and formatting to enforce code quality and style guidelines automatically. Configured in `pyproject.toml`.  

### Development Tools and Their Roles
- **Hatchling**  
  PEP 517-compliant build backend managing packaging and installation.  
- **Ruff**  
  For linting, checking imports, style errors, and enforcing consistent quote styles and line lengths.  
- **pytest + pytest-asyncio + pytest-cov + pytest-mock**  
  Test automation, async support, coverage reporting, and mocking utilities respectively.  
- **uv tool**  
  Development utility for tooling management and CLI command execution (`uv tool install` etc).  

### Runtime Environments and Platforms
- Native Python environment supporting Python 3.13 or higher on any OS that supports Python 3.13.  
- Relies on OpenAI API access which requires internet connectivity and configured API key (environment variable).  
- CLI runs on POSIX-compliant shells and Windows terminals with support for environment variables.

---

## Development Setup and Environment

### Step-by-step Environment Setup

1. **Install Python 3.13+**  
   Download from official Python site or use pyenv:  
   ```bash
   pyenv install 3.13.0
   pyenv local 3.13.0
   ```
2. **Clone the repository**  
   ```bash
   git clone https://github.com/yourusername/memory-banker.git
   cd memory-banker
   ```
3. **Install dependencies**  
   Using pip with editable mode for development:  
   ```bash
   pip install -e .
   ```
   Or use `uv` tool for sync/install:  
   ```bash
   uv sync
   ```
4. **Set environment variables**  
   Configure OpenAI API key:  
   ```bash
   export OPENAI_API_KEY="your_api_key_here"
   ```
5. **Install development dependencies**  
   Use pip or Hatch to install dev group dependencies:  
   ```bash
   pip install -r <(poetry export -f requirements.txt --dev)
   ```  
   *(Alternatively add as Hatch or Poetry groups if used.)*

### Required Tools and Installation Instructions
- **Python 3.13+**: See above.  
- **Git**: For version control and repository cloning.  
- **OpenAI API Key**: Obtain from OpenAI dashboard and export as env var.  
- **`uv` CLI tool**: Optional, for tooling convenience, installed via `pip install uv`.

### Configuration Requirements and Environment Variables
- `OPENAI_API_KEY` (required) - OpenAI authentication key.  
- Optional CLI flags for model selection `--model`, timeout `--timeout`, API key override `--api-key`.

### IDE/Editor Setup and Recommended Extensions
- **Visual Studio Code (VSCode)**  
  Recommended extensions:  
  - Python (Microsoft)  
  - Pylance for typing and linting  
  - Ruff extension for real-time linting  
  - GitLens for VCS enhancements  
- Setup `.vscode/settings.json` with:  
  ```json
  {
    "python.pythonPath": "<path to python3.13>",
    "python.linting.enabled": true,
    "python.linting.ruffEnabled": true,
    "editor.formatOnSave": true
  }
  ```
- Enable Python testing integration with pytest.

---

## Technical Constraints and Requirements

### System Requirements and Compatibility Constraints
- Requires Python 3.13+; incompatible with earlier versions due to syntax and dependency constraints.  
- Internet connection needed to interact with OpenAI API services.  
- Compatible with any OS supporting Python 3.13 (Linux, macOS, Windows).  
- Requires git for project metadata extraction and version control awareness.

### Performance Requirements and Limitations
- Agent timeout default set to 300 seconds (5 minutes) per analysis agent; configurable up to 600s or more.  
- Performance constrained primarily by OpenAI API response times and local I/O speed.  
- Designed for scalability across small to large projects, but very large codebases may require increased timeouts.

### Security Requirements and Considerations
- OpenAI API key should be kept confidential and stored securely as environment variables.  
- No sensitive data logging.  
- Dependencies kept minimal to reduce attack surface.  
- User inputs are validated and sanitized in CLI commands during parsing (via click).  
- No network calls outside OpenAI API unless explicitly integrated.

### Compliance and Regulatory Requirements
- Complies with OpenAI API usage policies.  
- No personal data collection or processing occurring within the tool.  
- License and attribution as per repository – ensure compliance when redistributing.

---

## Dependencies and External Integrations

### Core Dependencies and Their Purposes
- **click**: CLI interface and command parsing.  
- **openai-agents**: Abstracts AI model usage and orchestrates agent workflows interacting with OpenAI. Supports LiteLLM backend.  
- **hatchling**: Packaging and build backend.  

### Optional Dependencies and Feature Flags
- Using `[litellm]` extras for openai-agents to enable LiteLLM support, allowing integration with local or custom LLM endpoints alongside OpenAI cloud.

### External Services and APIs
- **OpenAI API**: For language model interaction, underpinning intelligence in analysis and memory bank creation.

### Third-party Integrations and Their Configuration
- LiteLLM integration via openai-agents optional backend – controlled via configurations or command-line flags, enabling use of local LLMs for analysis.

---

## Tool Usage Patterns and Conventions

### Build Systems and Automation Tools
- Uses **hatchling** as build backend, commands like:  
  ```bash
  python -m build
  ```
- `uv` tool orchestrates installs and runs CLI commands for convenience.

### Testing Frameworks and Strategies
- **pytest** as standard testing framework.  
- **pytest-asyncio** to allow testing of async agent calls.  
- Tests organized into unit, integration, and API integration subfolders under `/tests`.  
- Coverage captured using `pytest-cov`.  
- Mocking done with `pytest-mock`.

### Deployment Tools and Processes
- Distributed as a Python package installable via pip or via `uv tool install`.  
- Global CLI install recommended for easy invocation.  
- Deployment is primarily local/desktop CLI usage; no server deployment required.

### Monitoring and Debugging Tools
- Logging and error messages surfaced in CLI output during commands.  
- Tests provide feedback on failures or environment issues.  
- Ruff for static code analysis to identify early errors.  
- Use Python debugger (e.g., `pdb`) for runtime diagnosis.

---

## Development Workflow and Standards

### Code Organization and File Structure Conventions
- `memory_banker/` contains core source code:  
  - `main.py`: CLI entrypoint  
  - `cli.py`: CLI command handling logic  
  - `agents.py`: AI agent definitions  
  - `memory_bank.py`: Memory bank file generation and management  
- `tests/` structured by test type: unit, integration, api_integration, fixtures.  
- Generated outputs placed under `memory-bank/` at project root when running commands.

### Coding Standards and Style Guidelines
- Line length limited to 88 characters (per Ruff config).  
- Use double quotes for strings (see Ruff `quote-style`).  
- Indentation spaces only (no tabs).  
- Avoid complex functions above 10-15 lines unless necessary (B008 and C901 ignored selectively).  
- Follow Python best practices with descriptive names, input validation, and clear comments referencing AI assistant best practices.  
- Use Ruff for linting and formatting enforcement.

### Version Control Patterns and Branching Strategies
- Git used for versioning.  
- Branching strategy seen in use: feature branches such as `gitbutler/workspace`.  
- Frequent commits with clear concise messages describing changes.  
- PRs encouraged for code reviews before merge.

### Code Review and Quality Assurance Processes
- PR-based development with automated testing via GitHub Actions (CI workflow seen).  
- Ruff and pytest run automatically on commits/pushes.  
- Code reviews to ensure adherence to style and best practices.  
- Tests must cover all public functions and critical paths.  
- All inputs validated and edge cases handled.

---

## Operational Context

### Deployment Environments and Configurations
- Command line tool primarily deployed on local developer machines or CI environments with Python 3.13+.  
- Requires environment variables for OpenAI API key.  
- Supports configuration overrides via CLI options.  

### Infrastructure Requirements and Scaling Considerations
- Minimal local resource needs: CPU, memory for Python processes.  
- Network bandwidth and latency affect OpenAI API response times significantly.  
- Scalability primarily handled by agent timeout configurations rather than infrastructure scaling.

### Backup and Disaster Recovery Procedures
- No persistent backend or database; all generated documentation backed up and managed via git version control.  
- Users advised to commit generated memory bank files regularly to git or preferred VCS.  
- Accidental deletions can be recovered from version history.

### Maintenance and Upgrade Procedures
- Upgrade Python dependencies with pip:  
  ```bash
  pip install --upgrade memory-banker
  ```
- Regularly update `pyproject.toml` dependencies to patch bugs and security flaws.  
- Run tests and lint before releases.  
- Follow semantic versioning (currently 0.1.0).

---

## Troubleshooting and Debugging

### Common Issues and Their Solutions

| Issue | Possible Cause | Solution |
|-------|----------------|----------|
| `OPENAI_API_KEY` not detected | Environment variable not set | Export `OPENAI_API_KEY` in shell before running CLI |
| Timeout errors during analysis | Agent timeout too low for project size | Increase timeout with `--timeout 600` or higher |
| Lint errors reported by ruff | Code style deviations | Run `ruff . --fix` or follow lint output to fix manually |
| API authentication errors | Invalid or expired API key | Obtain valid key from OpenAI and set env var again |
| CLI command not found | Tool not installed globally | Use local `uv run memory-banker` or install globally via `uv tool install .` |

### Debugging Tools and Techniques
- Use `pdb` or similar Python debugger to step through `memory_banker/` source code.  
- Add detailed logging temporarily in `memory_banker/cli.py` or `agents.py`.  
- Enable verbose output if available in CLI to trace API calls.  
- Use pytest with verbosity flag:  
  ```bash
  pytest -v tests/unit
  ```

### Performance Profiling and Optimization
- Profiling can be done with `cProfile` during CLI runs for identifying bottlenecks in local execution.  
- Optimize API calls by increasing timeout or reducing analyzed file scope if needed.  
- Use cached results or file exclusions to speed repeated runs (to be implemented or extended).

### Error Handling and Logging Patterns
- CLI commands implemented using `click` support exception catching and user-friendly error messages.  
- Agent failures gracefully handled with retry or fallback mechanisms in `agents.py`.  
- Logging minimal but can be extended with standard Python `logging` module if troubleshooting needed.  

---

# Summary

This project uses modern Python 3.13+, leveraging `click` for CLI interactions and OpenAI Agents for AI-powered analysis. The development environment is simple to set up with pip and `uv` tooling. Standardized code style and testing frameworks ensure maintainable, quality code. Security focuses on safely handling OpenAI credentials and validating inputs. Operationally, it is a pure CLI tool designed for local deployments, with git version control used for backup. Debugging uses Python-native tools complemented by robust automated tests. Following these guidelines and context enables efficient development, usage, and maintenance of the Memory Banker project.