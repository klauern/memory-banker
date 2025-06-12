# AI Assistant Guidelines for Memory Banker Project

---

## Table of Contents
- [Project-Specific AI Assistant Rules](#project-specific-ai-assistant-rules)
- [Interaction Patterns and Preferences](#interaction-patterns-and-preferences)
- [Context and Continuity Guidelines](#context-and-continuity-guidelines)
- [Quality Standards and Best Practices](#quality-standards-and-best-practices)
- [AI Tool Integration](#ai-tool-integration)
- [Project Evolution Guidance](#project-evolution-guidance)

---

## Project-Specific AI Assistant Rules

This project, *Memory Banker*, is a Python CLI tool that generates Cline-style memory banks via specialized AI agents. The AI assistant must align with the project's current architectural and stylistic norms to maintain consistency, reliability, and extensibility.

### Code Style and Naming Conventions
- **Language and version:** Python 3.13+
- **Formatting:** Match `ruff` and Black-compatible style as per `pyproject.toml`:
  - Max line length: 88 characters
  - Double quotes for strings unless the string contains double quotes
  - Indentation: 4 spaces (explicit from `ruff.format` settings)
  - Avoid trailing comma omissions (include trailing commas where appropriate)
- **Naming:**
  - Use descriptive, clear file and function names.
  - Module files use snake_case (e.g., `agents.py`, `memory_bank.py`).
  - Classes use `PascalCase` (e.g., `ProjectBriefAgent`).
  - Functions and variables use `snake_case`.
  - Constants in `UPPER_SNAKE_CASE`.
- **Comments:** 
  - Provide clear, explanatory comments describing *why* code exists, not only *what* it does, especially in complex logic or AI interaction workflows.
  - Docstrings for every public function/class following [PEP 257](https://peps.python.org/pep-0257/).

### Architectural Patterns and Design Principles
- **Agent-based design:** The logic is split into specialized AI agents (e.g., `ProjectBriefAgent`, `ProductContextAgent`).
- **Separation of concerns:** Each agent encapsulates a focused responsibility aligned to a particular memory bank aspect.
- **CLI entry:** The CLI interface is separate (`cli.py`), with an entry point in `main.py`.
- **Memory bank file management:** Encapsulated in `memory_bank.py`; only this module handles file I/O for memory banks.
- **Dependency minimization:** Prefer built-in libraries or minimal dependencies (e.g., only `click` and `openai-agents` required), matching Windsurf best practice.
- **Configuration declarative:** Use CLI flags or environment variables for API keys, timeouts, and model selection. Avoid hardcoded config.
- **Immutability:** Avoid mutating inputs where possible, favor pure functions, especially in agent analysis pipelines.

### Testing Approaches and Documentation Standards
- **Testing:**
  - Comprehensive unit tests required for all public functions and methods.
  - Use `pytest` for unit and integration tests.
  - Tests located under `tests/unit` and `tests/integration`.
  - Fixtures for reusable test setups in `tests/fixtures/conftest.py`.
- **Documentation:**
  - Update README when adding features or modifying CLI usage.
  - Docstrings must be thorough and consistent.
  - Use the project’s own memory bank files as living architecture documentation.
  - Add or update `CLAUDE.md`, `pytest-configs.md`, or other supporting docs if changes affect AI or testing behaviors.
  - When generating or updating memory banks, ensure explanations are clear and well-structured.

### Error Handling and Logging Patterns
- Use clear, user-friendly error messages in CLI commands.
- Catch and handle exceptions that may occur during file access, API calls, or analysis.
- Avoid silent failures; log warnings or errors via Python logging (configure as needed).
- Provide error feedback that suggests actionable next steps.
- Validate all external input parameters (CLI args, environment variables).
- Guard against partial or corrupted memory bank file states (atomic write strategies recommended).
- Prefer raising custom exceptions for domain-specific errors (e.g., `MemoryBankError`).

### Security Considerations and Validation Requirements
- Never expose or log OpenAI API keys in plain text.
- Validate file paths to prevent directory traversal or injection vulnerabilities.
- Validate CLI inputs rigorously (model names, timeouts, directory paths).
- Sanitize all data used in prompts to external AI APIs where applicable.
- Avoid storing sensitive information unintentionally in memory bank files.
- Use environment variables for sensitive config (do not commit keys to git).

---

## Interaction Patterns and Preferences

### Preferred Communication Style
- Use clear, respectful, and collaborative tone.
- Provide concise explanations with optional detailed rationale.
- When giving code suggestions, include in-line comments explaining key choices.
- Avoid jargon unless clearly defined or common in the project domain.
- Provide usage examples where helpful.

### Handling Complex Refactoring or Architectural Changes
- For major refactors:
  - Propose incremental, reversible steps.
  - Present architectural rationale referencing existing project patterns.
  - Warn about backward compatibility or integration challenges.
  - Suggest accompanying tests and documentation updates.
- Avoid large changes without prior input or confirmation.

### Guidelines for Code Review and Suggestion Formatting
- Use unified diff style code blocks for suggestions.
- Highlight only necessary changed lines to keep diffs minimal.
- Include explanation lines above or below code blocks.
- When suggesting alternative solutions, clearly enumerate pros and cons.
- Mark deprecated or legacy code clearly in comments if suggested to remain temporarily.

### When to Ask for Clarification vs. Making Assumptions
- If the instruction or code context is ambiguous or incomplete, ask clarifying questions rather than guessing.
- For well-established patterns or documented conventions, assume consistency.
- If in doubt about impact or intent of significant changes, ask before proceeding.

### Presenting Multiple Solution Options
- Present 2-3 vetted options succinctly.
- Highlight differences in complexity, performance, or maintenance.
- Recommend one solution with justification.
- Provide fallback or simpler options for quick wins.

---

## Context and Continuity Guidelines

### Information to Track Across Sessions
- Project root and key directory paths (`memory_banker/`, `tests/`, `memory-bank/`).
- Current branch (`gitbutler/workspace`) and recent commit hashes.
- Active AI model and timeout settings used for agent calls.
- Custom CLI flags or environment variables in use.
- Last generated memory bank status and content structure.
- Known architectural patterns or agent roles.

### Maintaining Awareness of Recent Changes
- Reference recent commits for new features or fixes (e.g., `153f719 fix(settings)`).
- Be aware of uncommitted changes and potentially deleted memory bank files.
- Synchronize your context with latest pushed or local changes in `memory_banker/` code.
- Track removed or renamed memory bank files (e.g., activeContext.md deleted recently).

### Key Files and Patterns to Reference Consistently
- `memory_banker/agents.py` — core AI agent implementations
- `memory_banker/memory_bank.py` — file management for memory banks
- `memory_banker/cli.py` and `main.py` — CLI interface and entry point
- Memory bank markdown files in `memory-bank/` folder:
  - `projectbrief.md`
  - `productContext.md`
  - `activeContext.md`
  - `systemPatterns.md`
  - `techContext.md`
  - `progress.md`
- `README.md` and configuration files (`pyproject.toml`, `.gitignore`)
- Test modules under `tests/unit` and `tests/integration`

### Important Constraints and Boundaries to Respect
- Python version must be >= 3.13, code must be compatible.
- Memory bank files follow the 6 Cline-style core files format exactly.
- CLI commands: `init`, `update`, `refresh` only; do not invent new commands.
- Limit external dependencies as per project config.
- Respect timeout settings for AI model API calls (default 300s, configurable).
- Do not expose sensitive config or secrets.
- Follow project’s selected AI models and agent design principles.

### Project-Specific Gotchas and Common Issues
- Memory bank files can be deleted or corrupted on disk (watch for sync issues).
- Complex AI agent timeout handling requires attention — long-running analysis may need increased timeout config.
- API keys must be valid and environment variable `OPENAI_API_KEY` set before AI calls.
- Pytest-based tests require pytest-asyncio for async agents where needed.
- Code complexity warnings exist (e.g., `C901` ignored in `ruff` because some AI logic is complex).
- The `memory-bank` directory is regenerated and should not be manually edited.

---

## Quality Standards and Best Practices

### Code Formatting and Linting Requirements
- Use `ruff` with project-specific config to lint code consistently.
- Run `ruff` and `pytest --cov` before commits.
- Follow Black-compatible formatting (use `ruff`, `black` or equivalent).
- Quote style: double quotes by default.
- Respect max 88 character line length.
- Indentation: spaces only (4 per level).
- Keep complexity warnings (`C901`) ignored only if justified with comments.

### Testing Coverage Expectations and Strategies
- Unit tests for every public function and method.
- Integration tests covering CLI commands and AI agent collaboration.
- Use mocks for OpenAI API calls to avoid cost and improve test stability.
- Coverage target: >90%, focus on agent logic and file I/O.
- Include tests for error handling and boundary cases.
- Use fixtures for common setup/teardown in tests.

### Documentation Standards and Requirements
- Update README sections for new features or CLI options.
- Maintain detailed docstrings with examples.
- Use Memory Bank markdown files to document architecture, system patterns, and progress.
- Commit message style should describe purpose clearly.
- Document any special config or environment setup.

### Performance Considerations and Optimization Approaches
- Optimize AI calls by batching or caching results where feasible.
- Minimize disk I/O by batching file writes.
- Avoid blocking calls where async is supported.
- Profile agent runtime if memory bank generation exceeds recommended timeouts; suggest tuning.
- Optimize prompt sizes to reduce token usage in AI API.

### Security Practices and Validation Patterns
- Validate environment variables before use.
- Sanitize CLI input args rigorously.
- Do not log secrets or keys.
- Handle API exceptions gracefully to avoid exposing internal info.
- Use secure file permissions on memory bank files if applicable.
- Validate project path inputs to avoid arbitrary file writes.

---

## AI Tool Integration

### Leveraging AI Assistant Capabilities Effectively
- Use AI agents (`memory_banker/agents.py`) specialization for modular code understanding and analysis.
- For code completion, focus on small, well-scoped functions (e.g., CLI options, agent helper methods).
- Use AI chat for exploratory design discussions and clarifications on architecture.
- Use refactoring AI tools for improving existing agent workflows or modularity without breaking API.
- Utilize AI to update markdown memory bank files with fresh context from code.

### When to Use Various AI Tools
- **Code Completion:** For new CLI flags, argument parsing, or filling small methods.
- **Chat Mode:** To clarify domain intent, design patterns, or collaborative problem solving.
- **Refactoring:** When bulk code structure changes, e.g., improving the agent class hierarchy or CLI redesign.
- **Testing Generation:** To help write or update tests with correct mock data or parameters.

### Workflow Patterns That Work Well
- Iterative small commits aligned with memory bank component updates.
- Use automation to trigger memory bank refresh after major merges.
- Use AI suggestions to improve human-written docstrings for clearer explanations.
- Validate AI-generated code locally with tests before merging.
- Keep AI-generated content aligned with current repository state.

### Integration With Existing Development Tools and Processes
- Use `memory-banker` CLI linked in `pyproject.toml` for test and dev workflows.
- Use `pytest` to run tests; config provided in `pytest.ini` and `pytest-configs.md`.
- Lint code with `ruff` before pushing.
- Use GitHub Actions CI (e.g., `.github/workflows/ci.yml`) to automate test and lint runs.
- Configure environment variables like `OPENAI_API_KEY` securely in CI.

---

## Project Evolution Guidance

### Handling Feature Additions and Changes
- Extend agents modularly, keep single responsibility.
- Add new CLI options using `click` following existing conventions.
- Update memory bank generators carefully; reflect changes in all 6 core files as needed.
- Document features in README and memory bank markdowns.
- Cover new features thoroughly with unit and integration tests.

### Approaches for Technical Debt and Refactoring
- Identify complexity hotspots by ruff warnings and test pain points.
- Refactor incrementally to not break AI agent pipelines.
- Clean up deprecated code, but only after ensuring backward compatibility.
- Use AI tooling to assist in safe refactors with test coverage protection.

### Guidelines for Maintaining Backwards Compatibility
- Retain CLI command names and option semantics unless explicitly versioned.
- Avoid API changes in public agent interfaces without clear migration paths.
- Preserve memory bank file format and naming, or provide migration scripts.
- Document breaking changes in README and changelog (if any).

### Strategies for Performance Optimization and Scaling
- Optimize agent analysis by:
  - Limiting scope per agent run.
  - Caching reusable analysis results.
  - Using async calls where possible.
- Use appropriate AI models balancing cost, speed, quality (defaults to `gpt-4.1-mini`).
- Allow configurable timeouts, increase for large projects.
- Monitor and keep memory bank update latency reasonable for developer flows.

---

# Appendix: Example Code Style Snippet

```python
import click
from memory_banker.agents import ProjectBriefAgent
from memory_banker.memory_bank import MemoryBankManager

@click.group()
def cli() -> None:
    """Memory Banker CLI group."""
    pass

@cli.command()
@click.option("--project-path", default=".", help="Path to target project directory.")
@click.option("--model", default="gpt-4.1-mini", help="AI model to use for analysis.")
@click.option("--timeout", default=300, help="Timeout in seconds per agent.")
def init(project_path: str, model: str, timeout: int) -> None:
    """
    Initialize a new memory bank for the specified project path.

    Args:
        project_path (str): Directory of the project to analyze.
        model (str): AI model name to use.
        timeout (int): Allowed timeout per agent in seconds.
    """
    try:
        agent = ProjectBriefAgent(project_path=project_path, model=model, timeout=timeout)
        memory_bank = MemoryBankManager(project_path)
        content = agent.analyze()
        memory_bank.write("projectbrief.md", content)
        click.echo("Memory bank initialized successfully.")
    except Exception as e:
        click.echo(f"Error initializing memory bank: {e}")
```

---

# Summary

These guidelines ensure AI assistants contribute consistent, maintainable, secure, and high-quality code aligned with Memory Banker’s architecture and development norms. Always validate assumptions with the project team as needed and provide clear rationale for any significant proposed changes.