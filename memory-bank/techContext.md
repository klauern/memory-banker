# Technical Implementation Context for Memory Banker

This document captures the detailed technical implementation context for the **Memory Banker** project, building upon the project brief and README foundation. It provides a comprehensive overview of technologies, setup, development workflows, constraints, dependencies, operations, and troubleshooting guidelines essential for contributors and maintainers.

---

## Technologies Used

### Programming Languages and Versions

- **Python 3.13+** (minimum required version as per `pyproject.toml`)
- CLI scripting with Python

### Frameworks and Libraries

- **click >= 8.2.1** — For building the CLI interface and command parsing
- **openai-agents[litellm] >= 0.0.17** — Core AI agent framework used to analyze projects leveraging OpenAI's language models (with optional LiteLLM support)
- **pytest >= 8.4.0** (dev dependency) — Unit and integration testing framework
- **pytest-asyncio** — For async test support
- **pytest-cov** — Test coverage reporting
- **pytest-mock** — Mocking for tests
- **ruff >= 0.8.0** — Code linting, formatting, and static analysis

### Development Tools and Their Roles

- **Hatchling** — Build backend tool for Python packaging (`pyproject.toml` specifies `hatchling.build`)
- **uv CLI tool** — Optional command line environment and runner recommended for installation and execution
- **Git** — Version control
- **Ruff** — Linting and style enforcement tool
- **pytest** — Automated testing
- **Docker** (optional) — Could be used in advanced deployment scenarios though not explicitly detailed

### Runtime Environments and Platforms

- Cross-platform (Linux, macOS, Windows) as Python 3.13+ is supported widely
- Requires internet access for OpenAI API interactions
- Assumes shell environment (bash/zsh) for environment variables and CLI commands

---

## Development Setup and Environment

### Step-by-Step Environment Setup

1. **Install Python 3.13+**

   Verify installation:

   ```bash
   python3 --version
   # Python 3.13.x
   ```

2. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/memory-banker.git
   cd memory-banker
   ```

3. **Install dependencies**

   Using `uv` (recommended):

   ```bash
   uv tool install git+https://github.com/yourusername/memory-banker.git
   uv sync
   ```

   Or using `pip`:

   ```bash
   pip install -e .
   ```

4. **Set OpenAI API key**

   Export environment variable in your shell profile (`~/.bashrc`, `~/.zshrc`):

   ```bash
   export OPENAI_API_KEY="your_api_key_here"
   ```

5. **Verify CLI availability**

   ```bash
   memory-banker --help
   ```

### Required Tools and Installation

- Python 3.13+ (<https://www.python.org/downloads/>)
- `uv` CLI tool (<https://uv.sh>) — recommended but optional
- Git (<https://git-scm.com>)
- Code Editor/IDE (see below)

### Configuration Requirements and Environment Variables

- `OPENAI_API_KEY` (string, required) — OpenAI API key for agent interaction
- Optional CLI flags for:
  - `--model` (e.g., `gpt-4.1-mini`, `gpt-4o`, `gpt-4`)
  - `--project-path` to specify target project directory
  - `--timeout` for agent timeout seconds
  - `--api-key` to override environment variable temporarily

### IDE/Editor Setup and Recommended Extensions

- **Visual Studio Code (VSCode)**
  - Python extension by Microsoft (for code intelligence, linting)
  - Pylance (type checking)
  - Ruff extension or integration for linting
  - GitLens (for git insights)
- **PyCharm**
  - Built-in Python support
  - pytest configuration
- Editor configured to respect `.ruff.toml` or `pyproject.toml` linting rules
- Enable auto-format on save with `black` or `ruff` (if configured)

---

## Technical Constraints and Requirements

### System Requirements and Compatibility

- Requires Python 3.13 or newer; older versions unsupported due to language and dependency requirements
- Must have HTTP connectivity to OpenAI API endpoints
- Compatible with POSIX-compliant shells and Windows PowerShell (with minor adjustments)
- Git should be installed and available in PATH for history-based analysis and project scanning

### Performance Requirements and Limitations

- Per-agent timeout default: **300 seconds (5 min)**; configurable to max recommended **600 seconds (10 min)**
- Designed for projects of variable size with scalable analysis timeouts
- Efficiency depends on OpenAI model latency and project complexity
- CLI operations expected to run on local compute without heavy external dependencies

### Security Requirements and Considerations

- API keys must be kept secret, preferably set via environment variables, **never commit them**
- CLI avoids logging sensitive API keys or output in plain text
- Interactions over HTTPS with OpenAI API ensure encrypted communication
- Users responsible for securing local environment and API key access

### Compliance and Regulatory Requirements

- Usage of OpenAI API is subject to OpenAI’s terms of service and data privacy policies
- No PII or sensitive user data is collected or stored by the tool itself
- Generated memory banks are local markdown files, managed by the user
- Users must ensure compliance if integrating with proprietary or sensitive codebases

---

## Dependencies and External Integrations

### Core Dependencies

| Dependency               | Purpose                                          |
|--------------------------|-------------------------------------------------|
| `click` >= 8.2.1         | CLI command parsing and option handling         |
| `openai-agents[litellm]` >= 0.0.17 | Core AI agent framework to enable project analysis with OpenAI |
| `pytest` (dev)           | Running unit and integration tests              |
| `pytest-asyncio` (dev)   | Async test support                               |
| `pytest-cov` (dev)       | Coverage reporting                               |
| `pytest-mock` (dev)      | Mocking in tests                                 |
| `ruff` (dev)             | Code style linting and formatting                |

### Optional Dependencies and Feature Flags

- The `litellm` extras for `openai-agents` include lightweight LLM support (optional, depending on user preference)
- CLI options allow users to specify different OpenAI models or timeouts

### External Services and APIs

- **OpenAI API**: Used extensively via `openai-agents` to run AI models (GPT-4 variants and others) for intelligent project analysis

### Third-Party Integrations and Configuration

- OpenAI API key management as described above
- Model configuration via CLI flags or defaults in code, integrated with `openai-agents` framework

---

## Tool Usage Patterns and Conventions

### Build Systems and Automation Tools

- Uses **Hatchling** for building and packaging Python project (`pyproject.toml`)
- `uv` tool recommended to manage dependencies and run CLI commands in isolated environments
- Git for version control and source history analysis

### Testing Frameworks and Strategies

- Testing organized under `tests/` directory:
  - Unit tests under `tests/unit/`
  - Integration tests under `tests/integration/`
  - Fixtures in `tests/fixtures/`
- Test files follow `test_*.py` naming conventions
- Use `pytest` as test runner:

  ```bash
  pytest
  pytest --cov=memory_banker
  ```

- Async tests supported with `pytest-asyncio`
- Mocking using `pytest-mock`

### Deployment Tools and Processes

- As a Python CLI package, deploy via PyPI or git installation
- Use `pip install -e .` for development installs
- Use `uv tool install git+https://...` for recommended installation path
- No containerization specified but could be added if needed

### Monitoring and Debugging Tools

- Logs CLI output to console
- Common debugging via test assertions, breakpoints in IDE
- Potential for adding logging module outputs if extended

---

## Development Workflow and Standards

### Code Organization and File Structure Conventions

- Core application code inside `memory_banker/` package folder
- CLI entrypoint and commands implemented in `memory_banker/cli.py`
- AI agents defined in `memory_banker/agents.py` (one agent per contextual memory bank type)
- Memory bank file handling in `memory_banker/memory_bank.py`
- Tests clearly segregated into unit and integration categories under `tests/`
- Project root contains config files such as `pyproject.toml`, `pytest.ini`, `.gitignore`

### Coding Standards and Style Guidelines

- Follows Python code style with line length max 88 (per Ruff config)
- Uses double quotes for strings (per Ruff formatting rules)
- Avoids violations flagged by Ruff like pyflakes, pycodestyle, bugbear, flake8-comprehensions
- Complexity warnings ignored if necessary (`C901`)
- Consistent indentation with spaces
- Encourages type hints and static checks where possible

### Version Control Patterns and Branching Strategies

- Git used as VCS
- Main development happens on `main` branch (current branch)
- Feature or bugfix branches created for Pull Requests/merges
- Commit messages follow imperative style with scope prefix (e.g., `feat:`, `fix:`, `refactor:`)
- Code auto-formatting applied before commits (via Ruff or pre-commit hooks may be added)

### Code Review and Quality Assurance Processes

- Pull requests reviewed by maintainers for code quality, tests, and docs
- Automated tests run before merging
- Linting and formatting ensured
- Emphasis on documentation update (README, CLAUDE.md)

---

## Operational Context

### Deployment Environments and Configurations

- Local CLI tool for developer machines
- No server or cloud environment required
- User specifies project directory to analyze via CLI options or defaults to current directory

### Infrastructure Requirements and Scaling Considerations

- Minimal requirements: Python runtime and network connectivity
- Scalability dependent on API limits and project size
- Larger projects may require increasing agent timeouts (up to recommended 600s)

### Backup and Disaster Recovery Procedures

- Generated files stored in `memory-bank/` folder - user should back up along with project
- Version control natural backup via Git for source code, but `memory-bank` directory may be excluded by user choice
- No automated backup mechanism implemented

### Maintenance and Upgrade Procedures

- Update dependencies regularly via `pip` or `uv` tool
- Follow semantic versioning `0.1.x` moving to `1.x`
- Update `openai-agents` as new versions release
- Add new features via modular agent additions
- Keep API key updated as per OpenAI requirements

---

## Troubleshooting and Debugging

### Common Issues and Solutions

| Issue                                  | Potential Cause                               | Solution                                      |
|---------------------------------------|----------------------------------------------|-----------------------------------------------|
| `memory-banker` command not found     | Not installed or PATH missing                 | Install via `uv tool install` or `pip install -e .` and ensure PATH set |
| OpenAI API key missing or invalid     | `OPENAI_API_KEY` not set or incorrect          | Export valid API key, check `.bashrc` or `.zshrc` |
| Agent timeout errors                  | Default timeout too short for large projects | Increase timeout via CLI flag `--timeout 600` |
| Python version incompatible            | Running on Python < 3.13                       | Upgrade Python to 3.13+                        |
| Linting errors on code                 | Ruff violation detected                         | Fix per error details or adjust `.ruff.toml`  |
| Tests failing                         | Code or environment issues                       | Run `pytest -v`, check test logs, fix accordingly |

### Debugging Tools and Techniques

- Use IDE debugger (e.g., VSCode Debugger, PyCharm) with breakpoints
- Enable verbose logging calls if implemented
- Run isolated unit tests to isolate problem areas
- Use `pytest` with `-s` and `--tb=short` for focused output

### Performance Profiling and Optimization

- Profile long-running agent calls by increasing timeout only as needed
- Inspect calls to OpenAI API for possible batching or caching improvements (future enhancements)
- Optimize local code with profiling tools (`cProfile` in Python)
- Reduce CLI startup time by lazy-loading heavy components if needed

### Error Handling and Logging Patterns

- CLI commands raise clear error messages on invalid input or API failures
- Exceptions caught and user informed with next-step suggestions
- Logging currently to console; future enhancements may add configurable log levels and files

---

# Summary

The **Memory Banker** project is a modern Python CLI tool leveraging AI agent frameworks centered around OpenAI's API to generate comprehensive Cline-style memory banks that capture a project's technical, architectural, and contextual details in markdown. It emphasizes extensibility, modularity, and developer usability with clear setup instructions, tested code, and configuration management.

This document should serve as a practical guide for developers to setup, contribute, troubleshoot, and operate the project efficiently.

---

# Appendices

### Sample CLI Initialization Command

```bash
export OPENAI_API_KEY="sk-xxxxxx"
memory-banker --project-path ~/my-python-project --model gpt-4 --timeout 600 init
```

### List of Generated Memory Bank Files

- `projectbrief.md`
- `productContext.md`
- `activeContext.md`
- `systemPatterns.md`
- `techContext.md`
- `progress.md`

Each corresponds to an AI agent’s analysis domain.

---

If any clarifications or expansions are needed on specific sections, please reach out.
