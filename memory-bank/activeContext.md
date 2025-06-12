# activeContext.md

## Current Work Focus

- **Primary objectives:**
  Develop and improve the Memory Banker CLI tool to facilitate automatic generation of comprehensive Cline-style memory banks for software projects using OpenAI agents. The goal is to enable AI assistants to maintain rich, persistent project context across sessions.

- **Active features/components being worked on:**
  - **Agent subset functionality**: Enhanced CLI and agent system to support running only specific agents for faster testing and development workflows.
  - **Performance optimization**: Significant improvements to integration test speed by allowing subset execution instead of all 7 agents.
  - CLI interface enhancements located mainly in `memory_banker/cli.py` and coordinated by `memory_banker/main.py`.
  - The AI agent orchestration and analysis workflows within `memory_banker/agents.py`.
  - Memory bank file generation and updating logic in `memory_banker/memory_bank.py`.
  - Improved AI service rules (`memory_banker/ai_service_rules.py`) which influence agent behavior and output quality.
  - Testing coverage improvements for CLI and agents (`tests/unit/test_cli.py`, `tests/unit/test_agents.py`).

- **Immediate priorities and focus areas:**
  - **COMPLETED**: Agent subset functionality implementation for faster integration testing.
  - **COMPLETED**: CLI `--agents` flag support for all commands (init, update, refresh).
  - **COMPLETED**: Updated integration tests to use agent subsets, reducing test time from 15-35 minutes to 2-4 minutes.
  - Stabilizing multi-agent coordination for robust and consistent memory bank file generation.
  - Ensuring comprehensive and accurate capture of current project state for `activeContext.md`.
  - Fixing recent CLI interface test issues reported and improving test reliability.
  - Addressing uncommitted changes affecting workflows and memory bank files, particularly cleanup and regeneration of core memory bank documents.
  - Documenting configuration options and usage patterns clearly, facilitating easier adoption.

- **Current development approach and methodology:**
  - Iterative development using feature branches (`gitbutler/workspace`).
  - Following Python best practices with automated formatting enforced by `ruff`.
  - Unit and integration testing using `pytest` with asynchronous support (`pytest-asyncio`).
  - Incremental enhancement driven by AI agent feedback loops and refinements.
  - Strong emphasis on modular design separating CLI, agent logic, and file IO concerns.
  - Configuration and dependency management done via `pyproject.toml` and `hatchling` build backend.

## Recent Changes and Progress

- **Significant changes from git history and file analysis:**
  - Recent commits have focused on AI-related improvements, e.g., commit `2b336ce` introduced comprehensive AI service rules that guide memory bank generation (`ai_service_rules.py`).
  - The CLI's main entry point was refactored from `cli.py` into `main.py` (`c803dba`), centralizing startup logic and improving maintainability.
  - Test fixes and imports improvements were introduced (`fbbc557`), addressing flaky tests and enhancing test suite organization.
  - Addition of more robust allowed commands for git operations incorporated in agent command execution rules (`153f719`).
  - Some memory bank files (`activeContext.md`, `productContext.md`, etc.) were deleted/untracked recently, indicating an ongoing refresh or rework of these documents.

- **Recently completed features or milestones:**
  - Initial stable CLI with support for `init`, `update`, and `refresh` commands complete and tested.
  - Configuration system supporting multiple AI models and timeout settings finalized.
  - Core agent framework designed and implemented, allowing specialized agents to independently analyze project aspects and generate discrete memory bank components.

- **Code patterns and architectural decisions made recently:**
  - Modular agent design pattern: Each agent focuses on one memory bank file type (e.g., ProjectBriefAgent, ActiveContextAgent).
  - Decoupled CLI entrypoint with dependency injection to agents and memory bank management.
  - Usage of `openai-agents` Python library for AI interactions with fallback LiteLLM integration.
  - Compliance with Python 3.13 features and formatting enforced by `ruff` with a preference for double quotes and space-based indentation.

- **Lessons learned from recent work:**
  - Robust error handling around AI agent timeouts and unexpected output formats is crucial.
  - Test coverage must include edge cases such as invalid project paths or missing API keys.
  - The user documentation (README.md) needs to be comprehensive and kept in sync with CLI options and behavioral changes.
  - Memory bank files can get out of sync or corrupted if not updated atomically; tooling should consider backup/restore functionality.

## Next Steps and Priorities

- **Immediate next actions and tasks:**
  - Rebuild all core memory bank files in `memory-bank/` to ensure the latest analysis is reflected, as several files are currently deleted/untracked.
  - Fix CI pipeline YAML files (`.github/workflows/ci.yml`) to correctly handle current branch naming and testing steps.
  - Complete unit and integration tests for newly introduced AI service rules and CLI commands.
  - Address flaky tests such as `test_cli_interface.py` and `test_end_to_end.py` to stabilize test suite.
  - Document AI agent output expectations and error handling for maintainability.

- **Planned features and improvements:**
  - Implement finer-grained project analysis with incremental updates for large projects to reduce timeout risks.
  - Add support for additional language runtimes beyond Python (e.g., Node.js, Go, Rust) fully leveraging current multi-language intent.
  - Introduce caching and memoization for repeated AI requests where project structure has not changed.
  - Enhance user configuration options for memory bank file customization and output formatting.
  - Provide a visual dashboard or report summarizing memory bank generation results.

- **Upcoming decisions that need to be made:**
  - Decide on the approach for multi-agent concurrency (e.g., async parallel execution vs sequential processing) given timeout trade-offs.
  - Establish a strategy for memory bank file versioning and collaboration support within teams.
  - Determine default AI model configurations balancing speed, cost, and output quality for different user tiers.
  - Define strict API key management and environment validation logic to avoid runtime failures.
  - Consider integration with existing project management or CI/CD pipelines.

- **Dependencies and blockers to address:**
  - OpenAI API key must be provided; otherwise, agent execution is blocked.
  - Uncommitted changes related to memory bank files and test cases must be resolved.
  - CI workflows currently need fixes to run tests properly on the new branch strategy.
  - Potential dependency upgrades (e.g., `openai-agents`) should be evaluated for compatibility.

## Active Decisions and Considerations

- **Open technical decisions and trade-offs:**
  - Balancing thoroughness of project analysis against operational timeouts and API usage costs.
  - Choice of default AI model: `gpt-4.1-mini` for cost-efficiency vs `gpt-4` for maximum detail.
  - Selecting the best concurrency model for running multiple agents without overwhelming system resources.
  - How to handle deprecated or legacy project files when generating memory bank content.

- **Design choices under consideration:**
  - Memory bank file atomic update patterns to prevent partial writes or corruption.
  - Standardized format for agent prompts and their response validation for consistent parsing.
  - Inclusion of project git history and commit metadata in `activeContext.md` to reflect current state.
  - Support for user-defined agent extensions or plugins.

- **Performance or architectural concerns being evaluated:**
  - Minimizing latency of interactive CLI commands by optimizing agent workflows.
  - Efficient file system scanning and dependency detection to reduce analysis overhead.
  - Managing API call volume through request batching and result caching.
  - Scalability of the tool for massive codebases and monorepos.

- **Integration challenges being addressed:**
  - Compatibility with multiple Python versions above 3.13 as specified.
  - Smooth integration with different terminal environments and shells on macOS/Linux.
  - Handling API quota exhaustion or rate-limiting gracefully.
  - Maintaining test consistency across local and CI environments.

## Important Patterns and Preferences

- **Coding patterns and conventions being used:**
  - Strict Python typing hints and docstrings for all public functions.
  - Modular design with single responsibility principle applied across agents and CLI commands.
  - Usage of click library for CLI argument parsing and option groups.
  - Separation of AI service rules into dedicated module for configurable behavior.
  - Consistent formatting enforced by ruff with specific ignore rules (e.g., ignoring line-length for black compatibility).

- **Architectural patterns being followed:**
  - Agent-based architecture with each specialized agent focused on a domain-specific memory bank file.
  - CLI orchestrator pattern controlling invocation flow, error handling, and user feedback.
  - Configuration-driven development allowing environment variables and CLI flags to override defaults.
  - Layered architecture separating presentation (CLI), business logic (agents), and persistence (file IO).

- **Tool usage patterns and preferences:**
  - Hatchling as build backend and dependency management via `pyproject.toml`.
  - pytest chosen as test framework with asynchronous test support for agents.
  - Ruff as linter for enforcing code style and catching errors before commit.
  - Usage of openai-agents library as the AI interaction layer.
  - Shell and environment variable usage for handling API keys and configuration.

- **Quality standards and testing approaches:**
  - Every public function has unit tests covering expected behavior and edge cases.
  - Integration tests validate full workflow from CLI command to memory bank file output.
  - Mocking and fixtures used extensively for AI agent interactions to isolate tests from live API calls.
  - Consistent use of descriptive error messages and exception handling.
  - Coverage reports generated and verified in HTML format (`htmlcov/` directory).

## Learnings and Project Insights

- **Key insights discovered during development:**
  - Agentic analysis greatly improves memory bank completeness but requires precise prompt tuning and output parsing.
  - Effective multi-agent coordination is the cornerstone for scalable analysis across diverse project aspects.
  - Users benefit from flexibility in model and timeout configuration to tailor analysis based on project size and resource constraints.
  - Automated generation of memory bank files reduces onboarding time for AI assistants significantly.

- **Best practices identified for this specific project:**
  - Always validate API key presence early to avoid mid-process failures.
  - Maintain robust logging to trace agent operations and failures.
  - Provide detailed CLI help and usage examples to improve user experience.
  - Use clear, descriptive commit messages and consistent branching conventions.
  - Prioritize atomic writes to prevent partial memory bank document states.

- **Anti-patterns or approaches to avoid:**
  - Mixing synchronous blocking IO with asynchronous AI calls causing performance bottlenecks.
  - Hard-coding model names or timeouts without user override possibilities.
  - Kept stale or deleted memory bank files in the repository causing confusion.
  - Overly verbose or complex agent outputs that challenge parsing logic.
  - Ignoring edge cases, e.g., empty projects or projects without git histories.

- **Technical debt and refactoring opportunities:**
  - Consolidate overlapping code in CLI initialization and flag parsing.
  - Simplify error handling pathways for AI agent exceptions.
  - Extract repeated prompt templates into a common resource for ease of maintenance.
  - Enhance test fixture reuse and parameterization to reduce duplication.
  - Improve documentation around memory bank file format specifications.

- **Performance bottlenecks or optimization opportunities:**
  - Optimize file scanning by caching file metadata and incremental analysis.
  - Parallelize agent runs where safe to reduce CLI command latency.
  - Reduce number of API calls by aggregating requests or using batched inputs.
  - Profiling agent prompt crafting to minimize token usage without losing context.

## Current Context for AI Assistance

- **Specific areas where AI assistance is most valuable:**
  - Generating detailed and contextually accurate `activeContext.md` reflecting the current state and next steps.
  - Writing robust CLI logic for options, error handling, and user prompts.
  - Creating and refining AI service rules and agent prompt templates for better output quality.
  - Adding meaningful, comprehensive comments and documentation inline within code.
  - Enriching test cases with edge scenarios and integration flows.

- **Preferred communication and interaction patterns:**
  - Clear, stepwise instructions and explanations for changes or suggestions.
  - Context-rich requests that specify file, function, or feature scope.
  - Use of markdown with syntax highlighting for code samples.
  - Emphasis on maintainability, readability, and adhering to existing conventions.

- **Context that helps maintain continuity across sessions:**
  - Awareness that the project uses a six-file Cline memory bank structure.
  - The tool integrates with OpenAI agents via the `openai-agents` framework.
  - Current active development is on the `gitbutler/workspace` branch with ongoing test fixes.
  - Recent deletes of memory bank files indicate regeneration is underway.
  - The codebase uses modern Python 3.13 features with automated formatting tools (`ruff`).

- **AI assistant rules and patterns currently being followed:**
  - Provide detailed context in code comments.
  - Use descriptive names for files, functions, and variables.
  - Validate all external inputs, including CLI arguments and environment variables.
  - Write tests for all new public code paths.
  - Follow existing architectural and coding patterns for consistency.

- **Coding conventions and standards in active use:**
  - Double quotes for strings.
  - Line length capped at 88 characters (enforced but with some ignores).
  - Space indentation, no tab characters.
  - Docstrings for public API.
  - Use of type hints throughout codebase.

## AI Assistant Integration Status

- **Code quality standards being followed:**
  - Automated formatting and linting with `ruff`, checking for errors, warnings, complexity, and style issues.
  - Consistent docstring and typing usage.

- **Testing and documentation patterns in use:**
  - Unit and integration tests with `pytest` and `pytest-asyncio`.
  - Tests organized by type in `tests/unit` and `tests/integration`.
  - Fixtures and mocks to isolate tests from external dependencies.

- **Error handling and logging conventions adopted:**
  - Meaningful exceptions with clear messages.
  - Graceful handling of edge cases and missing configuration.
  - Logging is in place but may require expansion for fine-grained agent diagnostics.

- **Security and performance practices implemented:**
  - API keys must be passed via environment variables or CLI parameters; no hardcoded keys.
  - User inputs validated in CLI commands to prevent invalid states.
  - Timeout settings configurable to prevent excessive resource use.
  - Prefer minimal external dependencies bundled with the project.

---

*This activeContext.md should enable immediate onboarding of AI assistants to continue development, debugging, and enhancement work on the memory-banker project by providing a detailed snapshot of current status, recent changes, challenges, and ongoing priorities.*
