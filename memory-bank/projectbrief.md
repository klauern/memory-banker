# projectbrief.md

# Memory Banker — Project Brief

---

## Project Overview

**Memory Banker** is a Python command-line interface (CLI) tool designed to agentically create comprehensive, structured memory banks for software projects using Cline-style memory management principles. By leveraging AI agents based on OpenAI's language models and the openai-agents framework, Memory Banker automatically analyzes a project’s source code, dependencies, git history, and architecture to generate six key context documents. These files enable AI coding assistants to maintain rich, persistent understanding across development sessions, improving collaboration, onboarding, and automation efficiency.

The core value proposition is to empower developers and AI assistants with a persistently updated, intelligent documentation system that abstracts and codifies project knowledge in a structured, accessible format. This system aids developers in understanding project scope, design rationale, technology context, and current progress without repeated manual documentation overhead.

Primary functionalities include:
- Intelligent project analysis via modular AI agents
- Automated creation and maintenance of six canonical memory bank files
- CLI commands for initialization, updating, and refreshing memory banks
- Configurable parameters (project path, OpenAI model, timeouts, API key)
- Support for diverse project types beyond Python (Node.js, Go, Rust, etc.)
- Seamless integration with OpenAI API and advanced AI agent frameworks

---

## Core Requirements and Goals

### Fundamental Requirements
- Must perform an automated and intelligent analysis of a project by scanning source files, project structure, dependencies, and git metadata.
- Generate and maintain the full set of six Cline-style memory bank documents:
  - `projectbrief.md` (this foundational document)
  - `productContext.md`
  - `activeContext.md`
  - `systemPatterns.md`
  - `techContext.md`
  - `progress.md`
- Provide a Python CLI with commands: `init`, `update`, and `refresh` to manage memory bank lifecycle.
- Support customizable operational parameters via CLI flags and environment variables (model choice, timeout values, project path, API key).
- Ensure compatibility with Python 3.13+ and leverage the OpenAI Agents framework with Litellm integration for AI functionality.
- Support multi-language project analysis beyond just Python code.

### Primary Objectives and Success Criteria
- Accurately produce a comprehensive, up-to-date, and coherent `projectbrief.md` that thoroughly defines project scope, goals, users, constraints, and foundational decisions.
- Enable AI assistants to leverage these memory banks for enhanced contextual understanding, lowering friction in multi-session development.
- Maintain high quality and consistency in generated documentation, following Cline’s memory management principles as the canonical source of truth.
- Provide an intuitive and robust CLI experience ensuring easy adoption and integration into developer workflows.
- Demonstrate stability and maintainability of the codebase with comprehensive test coverage across unit and integration layers.
- Employ secure handling of OpenAI API keys and efficient use of API calls to minimize performance costs.

### Key Constraints and Boundaries
- The tool is currently CLI-only, no GUI or Web UI is within scope.
- Generation focuses on markdown documentation files for text-based memory banks; no binary or proprietary formats.
- Relies on OpenAI API availability; no offline or purely local AI model support.
- Project analysis emphasizes static and metadata-driven insights without deep dynamic runtime analysis.
- Does not provide direct project editing or code generation features beyond memory bank creation.

### Non-Negotiable Features
- Generation of all six core memory bank documents, each conforming to their defined roles in Cline’s memory system.
- Support for configuration of OpenAI API parameters (API key, model, timeout) to enable flexible usage contexts.
- Explicit handling and reporting of errors in CLI operations, including API failures, invalid inputs, and timeouts.
- Code organization and naming conventions consistent with established norms in the project (clear descriptive names, modular structure).
- Comprehensive automated test coverage for all public-facing functionalities.
- Secure storage and usage of user credentials and sensitive information.

---

## Target Users and Use Cases

### Primary User Personas
- **Software Developers and Architects**: Interested in generating and maintaining rich project knowledge bases to aid development and collaboration.
- **AI-Assisted Developers**: Developers leveraging AI coding assistants (Copilot, Claude, Windsurf, Cursor) who need consistent contextual documents for enhanced AI effectiveness.
- **Project Managers and Technical Leads**: Require clear, up-to-date project overviews and technical contexts for decision-making.
- **Documentation Teams**: Benefit from automated generation of baseline structured project documentation.

### Key Use Cases and Workflows
- **Initial Memory Bank Creation**: Running `memory-banker init` on a new or existing project to generate foundational memory bank files.
- **Incremental Updates**: Using `memory-banker update` to refresh memory banks in response to project evolution such as new features or refactors.
- **Full Refresh/Rebuild**: Utilizing `memory-banker refresh` to completely reconstruct memory banks, ensuring coherence after large-scale changes.
- **Configuring and Customizing Analysis**: Adjusting CLI flags or environment variables to analyze different projects or tweak AI model parameters and timeouts.
- **Integration in CI/CD or Development Pipelines**: Automate periodic memory bank generation to keep documentation current and synchronized with codebase state.

### User Experience Goals and Expectations
- Simple, predictable CLI interface with clear commands, flags, and descriptive error messages.
- Output files located within a consistent `memory-bank/` directory with standard naming conventions.
- Quick feedback on progress and success/failure of operations.
- Documentation sufficient for straightforward installation, configuration, and troubleshooting.
- Reliable and consistent generation of comprehensive memory bank files aligning with the project’s evolving context.

---

## Project Scope Definition

### Included in Scope
- Development and maintenance of Python CLI tool named `memory-banker`.
- Agent-driven project analysis leveraging OpenAI Agents framework.
- Automated generation of the six canonical memory bank markdown files.
- Support for multi-language codebases with initial emphasis on Python.
- Configurable CLI handling project path, AI model, API key, and timeouts.
- Comprehensive unit, integration, and end-to-end testing.
- Documentation covering installation, usage, and configuration.

### Explicitly Out of Scope
- Real-time or interactive GUI interface.
- Runtime code instrumentation or dynamic analysis beyond static files and git metadata.
- AI-powered code writing, code review, or refactoring within this tool.
- Management of AI assistant sessions beyond generating memory bank files.
- Handling of non-software projects or non-code assets such as design files, databases, etc.
- Offline or non-OpenAI model AI support.
- Custom storage backend beyond local filesystem.

### Success Metrics and Acceptance Criteria
- All six memory bank files are generated correctly, present in the `memory-bank/` folder, and pass format validation.
- CLI commands respond correctly with proper exit codes and user feedback.
- Memory bank contents contain accurate and comprehensive descriptions aligned with project structure and state.
- Test suites achieve >90% code coverage without flaky tests.
- Users are able to generate and update memory banks on sample projects following README instructions without errors.
- Sensitive data like OpenAI API keys remain secure and are not logged or exposed inadvertently.
- Performance benchmarks meet reasonable expectations (typical init command completes within 2-5 minutes on moderate projects).

---

## Foundational Decisions

### Core Architectural and Design Principles
- **Modular Agent-Based Architecture**: Separate AI agent components responsible for each memory bank document, allowing focused and extensible analysis.
- **Separation of Concerns**: Independent layers for CLI interface (`cli.py`, `main.py`), AI agent logic (`agents.py`), and file management (`memory_bank.py`).
- **Idempotent Operations**: Commands such as `init`, `update`, and `refresh` should produce consistent outputs without side effects causing divergence.
- **Configurable & Extensible**: Parameters via CLI and environment variables to support different models, timeouts, and project paths.
- **Robust Error Handling & Logging**: Capture and report errors gracefully to aid debugging and user clarity.
- **High Test Coverage**: Ensure correctness and maintainability via unit and integration tests.

### Key Technology Choices and Rationale
- **Python 3.13+**: Latest Python stable release ensures modern language features and compatibility.
- **Click for CLI**: Robust, well-supported CLI framework for command parsing and help generation.
- **openai-agents framework with Litellm**: Enables lightweight AI agent orchestration and broad model access.
- **Ruff for linting and formatting**: Maintain high code quality and consistency with established Python tooling.
- **Pytest and pytest-asyncio**: Comprehensive test framework with async support.
- **Markdown file output**: Portable, human-readable documentation format compatible across tools.
- **Git metadata usage**: Leverage existing VCS data for enriched analysis without extra dependencies.

### Important Patterns and Conventions to Follow
- **Clear Descriptive Naming**: Use explicit file and function names (e.g., `ProjectBriefAgent`, `generate_project_brief`).
- **Context-Rich Comments**: Include rationale and explanation in code per AI assistant best practices.
- **Validate All Inputs**: Sanitize and verify user CLI inputs to prevent invalid states.
- **Consistent Logging and Error Messages**: Uniform format for logging, user feedback, and exception texts.
- **Single Responsibility Principle**: Agents have focused responsibilities to simplify logic and testing.
- **Use Built-in Libraries Preferentially**: Avoid unnecessary third-party packages unless essential.
- **Optimize for Typical Use Cases**: Balance detail and performance for medium-sized software projects.

---

## AI Assistant Integration Guidelines

To align with best practices observed from AI coding assistants Cursor, Windsurf, Copilot, and Claude, the following patterns and standards are incorporated into Memory Banker:

### Code Organization and Naming Conventions
- Public functions and classes have descriptive, intention-revealing names.
- Separate logic into modules by concern: `cli.py` for interface, `agents.py` for analysis logic, `memory_bank.py` for file management.
- Use snake_case for functions, PascalCase for classes, consistent across the codebase.
- Include high-level docstrings for modules, classes, and functions summarizing purpose and usage.
- Organize agent classes by the document they generate (e.g., `ProjectBriefAgent`).

### Error Handling and Logging Patterns
- Catch and handle anticipated errors such as API failures, timeouts, and invalid input gracefully.
- Provide meaningful, user-friendly error messages with suggestions or remediation steps.
- Log detailed error context internally to assist in debugging without overwhelming users.
- Fail fast on critical missing configuration (e.g., API key) with explicit error.
- Use exception hierarchies to classify errors logically.

### Testing and Documentation Standards
- Unit tests cover all public functions and core edge cases.
- Integration tests simulate CLI commands and end-to-end memory bank generation.
- Use fixtures and mocks for external dependencies like OpenAI API to ensure test reliability.
- Document test expectations and usage in code and supplementary markdown files.
- Maintain code coverage metrics and address uncovered paths proactively.

### Security and Performance Considerations
- Validate and sanitize all user input to prevent injection or misuse.
- Do not log or expose sensitive API keys or credential information.
- Respect OpenAI API rate limits with configurable timeouts and concurrency controls.
- Optimize agent execution order and resource usage for fast turnaround on typical project sizes.
- Allow users to configure model choice for cost vs quality tradeoffs.
- Minimize unnecessary file I/O or API calls by caching or incremental updates where feasible.

---

*This Project Brief serves as the definitive foundation guiding all associated Memory Banker documentation and development activities.*