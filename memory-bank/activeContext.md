# activeContext.md for memory-banker

---

## Current Work Focus

- **Primary Objectives**  
  Developing an agent-driven system ("memory-banker") designed to create Cline-style memory banks tailored for projects. The system leverages AI agents to synthesize, organize, and maintain memory or knowledge components.

- **Active Features/Components**  
  - The core memory bank management logic in `memory_banker/memory_bank.py`.  
  - Agent coordination code in `memory_banker/agents.py`.  
  - Command-line interface implementation in `memory_banker/cli.py` and entry point `main.py`.  
  - Configuration and environment management driven by `pyproject.toml` and `mise.toml`.

- **Immediate Priorities**  
  - Stabilize the core memory bank API for reliable knowledge storage and retrieval.  
  - Enhance agent workflows for efficient autonomous memory generation.  
  - Improve command line usability and streamline CLI commands.  
  - Integrate with OpenAI-based agent stack as per dependencies.

- **Development Approach**  
  Agile iterative development emphasizing modular code components, leveraging existing AI agent libraries (`openai-agents[litellm]`), with Python 3.13+ features. Uses `click` library for CLI interactions.

---

## Recent Changes and Progress

- **Git Activity & Uncommitted Changes**  
  Numerous uncommitted changes present across core source files (`main.py`, `memory_banker/` source), configuration files (`pyproject.toml`, `mise.toml`), and docs (`README.md`, `CLAUDE.md`). A `.claude/` folder appears, possibly for AI conversation logs or similar usage.

- **Completed Features / Milestones**  
  - Initial setup of memory bank abstraction and agent classes established.  
  - CLI scaffolded and integrated as an entrypoint via `memory-banker` script.  
  - External dependencies and environment pinned (`pyproject.toml`).

- **Architectural Decisions**  
  - Designed modular agent and memory bank separation for clear responsibility.  
  - Use of external AI agent frameworks (`openai-agents`) to avoid reinventing core AI interactions.  
  - Command-line first approach to trigger memory-bank workflows and invoke agents.

- **Lessons Learned**  
  Encouraged incremental feature testing and proactive environment management given modern Python version and experimental dependencies. Agent abstraction complexity requires clear interface definitions.

---

## Next Steps and Priorities

- **Immediate Actions**  
  - Commit current changes with descriptive messages to stabilize baseline.  
  - Complete integration testing between agent orchestrations and memory bank logic.  
  - Finalize CLI commands and argument parsing robustness.

- **Planned Features & Improvements**  
  - Add persistent storage mechanism for memory banks (e.g. JSON file, database).  
  - Support richer agent workflows — memory summarization, priority indexing, multi-agent collaboration.  
  - Strengthen README and user documentation for easier onboarding.

- **Upcoming Decisions**  
  - Decide on final architecture for memory storage (in-memory vs persistent).  
  - Choose between synchronous or asynchronous agent communication patterns.  
  - Determine compatibility and upgrade strategies for external dependencies (`openai-agents`).

- **Dependencies & Blockers**  
  - Dependency on latest `openai-agents` package and its stable API.  
  - Python 3.13+ features may limit user environments for now.  
  - Need for explicit error handling patterns for AI agent failures to avoid cascading issues.

---

## Active Decisions and Considerations

- **Open Technical Decisions**  
  - Whether memory banks should be versioned or mutable only.  
  - Trade-offs between local vs cloud/offloaded AI agent execution.  
  - Possible architecture pattern for scaling memory banks across projects/users.

- **Design Choices Being Evaluated**  
  - CLI UX design balancing between complexity and usability.  
  - Agent task decomposition strategies: monolithic agent vs multiple specialized agents.

- **Performance & Architectural Concerns**  
  - Ensure agent calls remain performant given potential multistep reasoning.  
  - Technical debt in code organization around agent APIs to avoid tightly coupled code.

- **Integration Challenges**  
  - Synchronizing asynchronous agent outputs and memory-bank updates.  
  - Capturing and logging detailed trace for AI decision-making within memory banks.

---

## Important Patterns and Preferences

- **Coding Patterns**  
  - Modular Python packages and submodules for separation of concerns.  
  - Use of `click` decorators for CLI command definitions.  
  - Agent classes encapsulate AI interaction logic with defined input/output interfaces.

- **Architectural Patterns**  
  - Agent-oriented architecture with memory bank as a central data store.  
  - Separation of concerns between CLI interface, memory logic, and agent orchestration.

- **Tool Usage**  
  - `click` for CLI.  
  - `openai-agents[litellm]` for AI interactions.  
  - Python virtual environments managed (ignored in `.gitignore`).  
  - `pyproject.toml` for packaging and dependencies, indicating modern Python packaging practices.

- **Quality Standards & Testing**  
  - No explicit tests found yet; planned addition recommended.  
  - Emphasis on incremental functional verification through CLI commands.  
  - Suggest adopting linting and type checking (e.g. mypy) aligned with new Python version.

---

## Learnings and Project Insights

- **Key Insights**  
  - AI agent autonomy can be improved with clearer memory-bank interaction protocols.  
  - CLI-first development helps rapidly validate system workflows and user interactions.

- **Best Practices Identified**  
  - Modular design to isolate agent logic from persistent memory.  
  - Clear version pinning of dependencies for reproducibility.

- **Anti-Patterns to Avoid**  
  - Avoid monolithic agent classes mixing memory and AI logic.  
  - Steer clear of synchronous blocking calls to AI agents in CLI commands.

- **Technical Debt and Refactoring**  
  - Need to refactor agent abstractions for clearer interfaces.  
  - Improve error handling and logging across modules.

- **Performance Bottlenecks**  
  - Await profiling of AI agent calls (network I/O bound).  
  - Potential bottlenecks in memory bank query speed with large data sets.

---

## Current Context for AI Assistance

- **Areas for AI Help**  
  - Writing and refining agent orchestration code that calls and coordinates multiple AI agents.  
  - Generating detailed CLI help text and validating argument parsing robustness.  
  - Designing persistent storage schemas and serialization for memory banks.  
  - Refactoring agent and memory bank code into cleaner modular designs.  
  - Creating unit and integration test cases for system components.

- **Preferred Communication**  
  - Clear, stepwise instructions preferred to maintain coding flow.  
  - Context-aware reminders about project architecture when suggesting changes.  
  - Provide code snippets and design patterns consistent with current style.

- **Continuity Context**  
  - Leverage knowledge of Python 3.13+ environment and dependencies (`openai-agents`, `click`).  
  - Understand separation of concerns: agents, memory bank, CLI interface.  
  - Awareness of uncommitted changes that need consolidation and testing.

---

**End of activeContext.md**