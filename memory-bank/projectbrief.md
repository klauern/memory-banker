# projectbrief.md

## Project Overview

**Memory Banker** is a Python command-line tool that agentically creates comprehensive Cline-style memory banks for software projects. It leverages OpenAI AI agents to perform intelligent, multi-faceted analysis of a target project’s structure, code, dependencies, and git history, automatically generating standardized documentation files that capture critical contextual knowledge and project information.

The core purpose of Memory Banker is to provide AI assistants and human developers with persistent, structured, and up-to-date project memory in the form of Markdown files. These memory banks facilitate better understanding, continuity, and context retention across development sessions and team collaborations.

### Value Proposition

- Automates generation of rich project documentation inspired by Cline’s memory management principles — reducing manual effort and increasing documentation quality.
- Enables powerful AI-assisted development workflows by maintaining granular, organized project context.
- Supports diverse project types (Python, Node.js, Go, Rust, etc.) via a language-agnostic approach focused on project metadata and architecture.
- Provides configurable and extendable tooling leveraging OpenAI’s latest models and the openai-agents framework.
- Supports continual updates of memory banks to reflect current development state and evolution.

### Primary Functionality and Features

- **AI Agent-Based Analysis:** Uses six specialized OpenAI agents, each responsible for distinct aspects — project scope, product context, active development state, system architecture, technical stack, and project progress.
- **Full Memory Bank Generation:** Creates six core Markdown files matching Cline’s memory bank taxonomy:
  - `projectbrief.md`
  - `productContext.md`
  - `activeContext.md`
  - `systemPatterns.md`
  - `techContext.md`
  - `progress.md`
- **Command-Line Interface:** Exposes intuitive CLI commands (`init`, `update`, `refresh`) for memory bank lifecycle management.
- **Configurable Parameters:** Supports customization of project path, OpenAI model selection, API key, timeouts, and other runtime options.
- **Multi-language Compatibility:** Designed to analyze and generate memory banks for projects written in multiple languages or mixed stacks.
- **Integration with OpenAI Agents & LiteLLM:** Utilizes advanced OpenAI models accessed via the openai-agents framework optimized for fast, cost-efficient, and detailed analysis.

---

## Core Requirements and Goals

### Fundamental Requirements

- Must analyze a given project directory holistically — including file structures, source code files, dependency manifests, and git history.
- Must employ multiple, distinct AI agents specialized in different cognitive domains of project understanding.
- Must generate a structured set of Markdown memory bank files under a dedicated output directory (`memory-bank/`) following Cline’s format.
- Must provide a CLI interface that enables initialization, incremental updates, and full refresh of memory banks.
- Must support configuration of API credentials, model choice, timeouts, and project path.
- Must be compatible with Python 3.13+ and leverage standard Python packaging and tooling.

### Primary Objectives and Success Criteria

- Enable creation of a meaningful, actionable `projectbrief.md` that serves as the authoritative foundation describing scope, goals, and constraints.
- Ensure each of the six core memory bank files adequately covers its intended domain with comprehensive and accurate content.
- Achieve robustness and resilience for projects of varying sizes and language types.
- Deliver fast-enough performance for real-world usage, with sensible default and customizable agent timeouts.
- Offer a clear, user-friendly CLI with helpful documentation and sane defaults.
- Seamlessly integrate OpenAI agents with minimal user setup beyond API key provisioning.
- Ensure generated memory banks facilitate AI assistant understanding and developer onboarding.

### Key Constraints and Boundaries

- The tool is designed primarily for static analysis augmented by AI agents; dynamic runtime introspection or instrumentation is out of scope.
- Deep language-specific parsing is limited—focus remains on general project metadata, structure, and annotations.
- Reliance on OpenAI API means availability and usage costs can affect real-world operation.
- Generated documentation focuses on project-level context, avoiding file-by-file granularity.
- Memory banks are Markdown text files; rich media, diagrams, or non-textual content are excluded.
- Supports primarily Python and general project types but advanced language-specific features are outside current scope.

### Non-negotiable Features and Capabilities

- Generation of all six Cline-style memory bank files in the `memory-bank/` directory.
- Robust CLI commands: `init`, `update`, and `refresh`—each with full project scan and appropriate regeneration logic.
- Configurability of core runtime parameters via CLI flags and environment variables.
- Usage of OpenAI agents framework for modular AI analysis flow.
- Clear error messaging and logging for failed or partial memory bank generations.
- Support for multi-model selection, including gpt-4.1-mini (default), gpt-4o, and gpt-4, plus LiteLLM integration.

---

## Target Users and Use Cases

### Primary User Personas

- **Software Developers:** Individuals and teams seeking to automate generation and upkeep of comprehensive project documentation and contextual memory.
- **AI-Enhanced Development Teams:** Teams leveraging AI assistants to aid coding, review, and knowledge retention requiring structured project context.
- **Project Managers & Technical Leads:** Stakeholders wanting clear, standardized summaries of project purpose, status, technical patterns, and progress.
- **DevOps and Documentation Engineers:** Specialists who maintain infrastructure and docs looking to automate context capture and reduce knowledge silos.

### Key Use Cases and Workflows

- **Initial Memory Bank Creation:** Run `memory-banker init` after cloning or starting a project to produce baseline memory bank files.
- **Incremental Updates:** Use `memory-banker update` to refresh parts of memory banks to reflect small changes or ongoing active development.
- **Complete Refresh:** Employ `memory-banker refresh` to force full reanalysis and rebuild of all memory bank files for large project state changes.
- **Context Injection for AI Assistants:** Memory bank files serve as input context for AI pair programmers or review assistants to understand project scope and architecture.
- **Onboarding and Knowledge Transfer:** Provide new team members ready-made, structured context documents automatically generated to accelerate ramp-up.

### User Experience Goals and Expectations

- **Simplicity:** Easy-to-understand CLI commands with clear options, minimal setup besides OpenAI API key.
- **Transparency:** Generated files written in clear, professional Markdown language with consistent formatting.
- **Reliability:** Stable operation with robust error handling and informative feedback.
- **Speed:** Reasonably fast processing with configurable timeouts to suit project size and complexity.
- **Extensibility:** Flexibility to incorporate additional agents or support custom projects with minimal changes.
- **Cross-Platform:** Functionality on any environment supporting Python 3.13 and network access to OpenAI APIs.

---

## Project Scope Definition

### Included in Scope

- Analysis of software project structure, source files, dependency manifests, and git metadata.
- Deployment of six focused AI agents for comprehensive project understanding.
- Generation of the full set of Cline-style memory bank Markdown files under `memory-bank/`.
- CLI tool encapsulating core lifecycle commands (`init`, `update`, `refresh`).
- Configuration mechanisms supporting API key, model, timeout, project path, etc.
- Use of openai-agents Python package and model integrations including LiteLLM.
- Packaging and distribution as installable Python package with entry point.
- Basic testing coverage (unit and integration tests) for core functionality.

### Explicitly Out of Scope

- Language-specific parsing or deep AST analysis beyond general context extraction.
- Automated code modification, code generation, or runtime instrumentation.
- Management of non-textual artifacts (images, diagrams, videos) within memory banks.
- Web or UI frontends; tool is strictly CLI-based.
- Handling private/internal APIs or proprietary codebases beyond standard privacy adherence.
- Integrations outside OpenAI API and openai-agents ecosystem.
- Continuous deployment or server-based hosted services.

### Success Metrics and Acceptance Criteria

- Successful generation of all six memory bank files with appropriate detailed content for diverse projects.
- CLI commands execute without error and respond correctly to standardized options.
- Generated documents demonstrate clear coverage of domain topics per file roles.
- Default setup works with minimal configuration and sensible timeout defaults.
- Tests pass successfully across unit and integration suites.
- Documentation (README, usage instructions) accurately describes usage and supported features.
- User feedback or early adopters validate usefulness and correctness of generated memory banks.

---

## Foundational Decisions

### Core Architectural and Design Principles

- **Modularity:** Functional decomposition by responsibility—each AI agent encapsulates a unique knowledge domain.
- **Agent-Based Cognitive Approach:** Leverages specialized AI models orchestrated to collectively generate holistic project memory.
- **Text-based Knowledge Representation:** All project context persisted as Markdown documents for portability and simplicity.
- **CLI-First Usage:** Prioritize command line interface for maximal environment compatibility and scriptability.
- **Configuration over Convention:** Allow users to specify runtime parameters while providing meaningful defaults.
- **Minimal Dependencies:** Use lightweight dependencies focusing on core OpenAI ecosystem and standard CLI tooling.
- **Automation and Repeatability:** Encourage regenerable memory banks that stay in sync with ongoing project changes.

### Key Technology Choices and Rationale

- **Python 3.13+:** Latest stable, forward-looking Python version ensures modern language features and type safety.
- **openai-agents framework:** Enables modular, high-level AI agent orchestration abstracting raw OpenAI API calls.
- **click for CLI:** Industry-standard Python CLI framework providing composable commands and option parsing.
- **Markdown for output:** Universally supported human-readable format ideal for documentation and AI context.
- **pytest and pytest-asyncio:** Robust testing framework aligned with asynchronous operations required by OpenAI APIs.
- **uv tool for management:** Supports easy installation and execution especially with advanced dependency management.
- **Light dependency set:** Limits external dependencies to reduce maintenance burden and security surface.

### Important Patterns and Conventions to Follow

- Use clear separation between AI agent logic (`agents.py`), CLI entrypoints (`cli.py`), and memory bank file management (`memory_bank.py`).
- Standardize generated Markdown to match Cline’s memory bank naming, structure, and content guidelines.
- Implement robust error and timeout handling around OpenAI agent calls to ensure graceful degradation.
- Support layered configuration loading (CLI flags, environment variables, default constants).
- Write idiomatic, type-annotated Python code styled according to Ruff and black formatting rules.
- Design tests to cover incremental and full regeneration flows for memory bank files.
- Keep user messages and logging informative but non-intrusive.

---

This **projectbrief.md** document serves as the foundational specification for the Memory Banker project, guiding subsequent elaborations in productContext.md, systemPatterns.md, and techContext.md by establishing the core purpose, requirements, user context, scope, and architectural choices for all further design and implementation efforts.
