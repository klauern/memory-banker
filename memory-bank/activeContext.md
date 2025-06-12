# activeContext.md (Current Active Context for memory-banker)

---

## Current Work Focus

- **Primary objectives:**  
  Implement comprehensive AI-assisted generation of "activeContext.md" describing the current development state, recent progress, next steps, active technical decisions, and contextual details critical for continuing development in memory-banker projects. The focus is to enhance the `ActiveContextAgent` to intelligently analyze git history, code structure, recent changes, and TODOs to produce a detailed and actionable markdown document.

- **Active features/components:**  
  - `ActiveContextAgent` (implemented within `memory_banker.agents.py`) - responsible for collecting and synthesizing current work status.  
  - CLI integration (`memory_banker.cli.py`) for triggering init/update/refresh commands that regenerate all memory bank files including activeContext.md.  
  - `memory_bank.py` - management of memory bank files, handling reads/writes for each memory bank component.

- **Immediate priorities:**  
  - Complete robust logic for extracting relevant information from git logs, working directory state, and source code comments (e.g. TODOs).  
  - Define and codify best practices for capturing current dev methodologies, recent decisions, and architectural tradeoffs in active context.  
  - Handle uncommitted changes and incorporate them properly into the current active context.  
  - Ensure output conforms to Cline-style structured memory bank documentation expectations.

- **Current development approach and methodology:**  
  - Utilize OpenAI Agents framework to invoke specialized agents per context file.  
  - Incrementally build active context by combining:  
    - Git commit analysis (last 5-10 commits)  
    - Uncommitted file status to highlight in-progress work  
    - Parsing code changes in critical files (cli.py, agents.py)  
    - Scanning TODO and FIXMEs for outstanding tasks  
    - Capturing README and project docs as baseline context  
  - Emphasis on automation and precise, concise markdown documentation.  
  - Follow semantic versioning and maintain backwards compatibility with existing CLI commands.

---

## Recent Changes and Progress

- **Git History and file modifications:**  
  - Recent commits enhanced CLI parameter handling and introduced support for `$OPENAI_BASE_URL` environment variable for API requests.  
  - Code has been reformatted with ruff autoformatter to conform to style guidelines.  
  - Dead or outdated memory-bank markdown files deleted from the repo (`activeContext.md` and others are currently deleted/unstaged).  
  - Refactoring CI actions merged to improve build and deployment.

- **Completed features/milestones:**  
  - Base CLI commands (`init`, `update`, `refresh`) fully operational.  
  - Core agent framework stabilized; productContext, projectBrief, systemPatterns, techContext agents produce valid outputs.  
  - Integration tests for CLI workflows and agent outputs exist (in `tests/integration/test_cli_interface.py`).  
  - Unit tests for individual modules (`agents.py`, `memory_bank.py`) covering main logic.

- **Code patterns & architectural decisions:**  
  - Modular agent-based architecture dividing project analysis into single-responsibility agents.  
  - Use of dataclasses and Click context objects to share config/options.  
  - Memory bank files stored in centralized `memory-bank/` folder as markdown.  
  - Preference for immutable inputs and pure functions in agent logic for testability.

- **Lessons learned:**  
  - Explicitly handling uncommitted workstate is critical for accurate activeContext reporting.  
  - Automating git log summarization requires heuristics to filter noise and extract intent.  
  - Consistent, enforced markdown conventions improve readability and downstream AI usage.  
  - Naming and docstring clarity important in agents to facilitate debugging and maintenance.

---

## Next Steps and Priorities

- **Immediate next actions:**  
  - Implement and test logic to extract 'Current Work Focus' and 'Recent Changes' sections from git commit messages and staged files.  
  - Extend `ActiveContextAgent` to parse TODO comments and code complexity metrics for technical debt insights.  
  - Restore deleted memory-bank markdown files from backups or regenerate with updated agent logic.  
  - Create unit tests covering newly implemented active context generation sub-components.  
  - Refine integration of CLI options to allow specifying time range or depth for activity analysis.

- **Planned features and improvements:**  
  - Enhance git analysis for branch merges, rebases, and conflict resolution reporting.  
  - Introduce automatic detection of blockers via issue references and TODO tags.  
  - Add customizable verbosity levels to active context output for different audience needs.  
  - Integrate lightweight static analysis metrics (e.g. cyclomatic complexity) into learnings section.  
  - Provide actionable recommendations for refactoring and prioritization.

- **Upcoming decisions:**  
  - Choose heuristics or ML-based summarization methods for git commit abstraction.  
  - Decide on formatting conventions for multi-level lists and cross-referencing other memory bank files.  
  - Define how to manage simultaneous editing conflicts or partial updates during activeContext generation.  
  - Select metrics for "performance bottlenecks" and code quality indicators.

- **Dependencies and blockers:**  
  - Reliable OpenAI API connectivity with correct environment setup (API keys, base URLs).  
  - Stable input from other agents (productContext, progress) to triangulate active context facts.  
  - Potential refactor of CLI parameter parsing to unify options propagation.  
  - Access to latest project git repository state and history for accurate analysis.

---

## Active Decisions and Considerations

- **Open technical decisions:**  
  - Trade-offs between real-time analysis candidate vs batch processing of git logs for active context freshness.  
  - Whether to prioritize shallow git history analysis (faster, less detail) vs deep history (more comprehensive).  
  - Balancing verbosity and conciseness in markdown output to maximize readability without information overload.  
  - Selection of code parsing libraries or regex heuristics for TODO and code comment extraction.

- **Design choices under consideration:**  
  - Using Python `gitpython` or CLI `git` commands invoked via subprocess for git history querying.  
  - Formatting active context with collapsible markdown sections for large output.  
  - Embedding links/references to other memory bank files to improve navigability.  
  - Deciding on multi-agent collaboration model: should `ActiveContextAgent` query results from other agents or operate independently?

- **Performance or architectural concerns:**  
  - Scaling analysis to very large repositories with extensive git histories.  
  - Minimizing latency in CLI commands to keep client developer flow smooth.  
  - Handling partial/incomplete states, for example uncommitted changes or large binary files in repo.

- **Integration challenges:**  
  - Synchronizing state with other memory bank files during updates and refreshes.  
  - Managing file system race conditions or permission issues when writing markdown files.  
  - Consistent handling of config options across CLI and agent layers.

---

## Important Patterns and Preferences

- **Coding patterns and conventions:**  
  - Use of type annotations and docstrings for all public functions/classes.  
  - Strict adherence to ruff and black formatting rules combined with click for CLI ergonomics.  
  - Modular, testable components with clear separation of concerns.  
  - Functional style favored for pure data transformation functions.

- **Architectural patterns:**  
  - Agent orchestration pattern — discrete specialized agents run sequentially or in parallel for different memory bank files.  
  - Use of context objects in CLI commands to share configuration seamlessly.  
  - Filesystem-centric persistence model using markdown as canonical output format.  
  - Dependency injection of environment variables and options into agents.

- **Tool usage patterns:**  
  - CLI interface built with `click` for commands/options.  
  - Use of HSV standard logging and debug statements selectively during development.  
  - Testing with pytest covering unit and integration scopes.  
  - Use of `git` CLI or `gitpython` for project repo introspection.

- **Quality standards and testing:**  
  - Coverage emphasis on edge cases and error handling (e.g. missing API key).  
  - Automated formatting checks on pull requests using ruff config.  
  - Tests include mocking for external API calls to OpenAI.  
  - Documentation updated synchronously with features to maintain coherency.

---

## Learnings and Project Insights

- **Key insights:**  
  - Structured memory banks significantly improve AI assistant context retention across sessions.  
  - Git commit summaries offer rich semantic information about recent development focus and blockers.  
  - Parsing and including uncommitted changes critical to reflect true current state.  
  - Modular agent design allows iterative enhancement and easier debugging.

- **Best practices identified:**  
  - Capture explicit development objectives and priorities in activeContext.md to guide developers and AI.  
  - Integrate instructions on development methodology (e.g., branching strategies) as part of current context.  
  - Use consistent markdown syntax for headings, lists, and code blocks.  
  - Include detailed active decisions and considerations for transparency.

- **Anti-patterns or approaches to avoid:**  
  - Avoid overly verbose dumps of git logs or code diffs disrupting reader comprehension.  
  - Do not rely solely on commit messages; validate with actual code or TODO states.  
  - Avoid tight coupling between agents to maintain flexibility.

- **Technical debt and refactoring opportunities:**  
  - Refactor `ActiveContextAgent` to modularize git analysis, TODO parsing, and markdown formatting.  
  - Remove deprecated memory bank files or merge outdated content.  
  - Centralize CLI option handling to prevent duplication in multiple agents.

- **Performance bottlenecks / optimization:**  
  - Cache repeated git queries where possible during a single agent run.  
  - Parallelize analysis steps cautiously considering rate limits with OpenAI API.  
  - Optimize text processing routines for markdown synthesis.

---

## Current Context for AI Assistance

- **Specific areas for AI assistance:**  
  - Summarizing git commit messages into coherent recent changes narratives.  
  - Parsing and extracting actionable TODO comments and deducing blockers.  
  - Generating concise yet informative markdown sections about active development focus and priorities.  
  - Formatting complex information into readable structured markdown conforming to Cline memory bank style.  
  - Suggesting next steps based on current repo state and open issues.

- **Preferred communication and interaction patterns:**  
  - Provide answers and code snippets with clear explanations in markdown code blocks.  
  - Offer iterative refinements and reasoning steps when generating summaries or recommendations.  
  - Maintain context of previous conversation to build upon existing analysis and avoid repetition.  
  - Validate output format compliance with existing memory bank conventions.

- **Context helping maintain continuity:**  
  - Awareness of recent commit IDs, branch name (`main`), and deleted memory bank files signaling regeneration effort.  
  - Knowledge of project structure centered around `memory_banker` package and six memory bank core markdown files.  
  - Understanding of agent-based architecture with each memory bank file having dedicated agent.  
  - Familiarity with CLI tooling via `click` commands and configured environment variables like `OPENAI_API_KEY`.  
  - Insight into preferred tooling (ruff + black), testing framework (pytest), and development best practices.

---

*This document should enable any developer or AI assistant to immediately understand the current active development landscape of the memory-banker project and proceed effectively with coding, testing, and documentation tasks.*
