import asyncio
import os
from pathlib import Path
from typing import Dict, Any, List

from agents import Agent, Runner, function_tool
from agents.extensions.models.litellm_model import LitellmModel

from .ai_service_rules import AIServiceRules


class MemoryBankAgents:
    """Agents for analyzing projects and generating memory bank content"""

    def __init__(self, llm_model: LitellmModel, timeout: int = 300):
        self.llm_model = llm_model
        self.timeout = timeout
        self.ai_rules = AIServiceRules()

    async def analyze_project(self, project_path: Path) -> Dict[str, Any]:
        """Analyze a project and generate memory bank content using specialized agents"""

        # Get project context
        project_context = self._get_project_context(project_path)

        # Create specialized agents for each memory bank file
        agents_tasks = [
            ("projectbrief", self._create_project_brief_agent(), "Generate a comprehensive project brief"),
            ("productContext", self._create_product_context_agent(), "Analyze the product context and problem space"),
            ("activeContext", self._create_active_context_agent(), "Determine current development context"),
            ("systemPatterns", self._create_system_patterns_agent(), "Analyze system architecture and patterns"),
            ("techContext", self._create_tech_context_agent(), "Document technical context and setup"),
            ("progress", self._create_progress_agent(), "Assess project progress and status")
        ]

        # Run all agents with timeout
        results = {}
        for file_type, agent, description in agents_tasks:
            print(f"🤖 {description}...")
            try:
                # Apply timeout to the agent execution
                result = await asyncio.wait_for(
                    Runner.run(agent, project_context), timeout=self.timeout
                )

                # Extract the actual text content from the RunResult
                if hasattr(result, "text"):
                    content = result.text
                elif hasattr(result, "value"):
                    content = result.value
                else:
                    # Parse the string representation to extract the content
                    result_str = str(result)
                    if "Final output (str):" in result_str:
                        lines = result_str.split("\n")
                        content_lines = []
                        in_content = False
                        for line in lines:
                            if "Final output (str):" in line:
                                in_content = True
                                continue
                            elif in_content and (
                                line.startswith("- ") or line.startswith("(See")
                            ):
                                break
                            elif in_content:
                                # Remove the leading spaces that are part of the indentation
                                if line.startswith("    "):
                                    content_lines.append(line[4:])
                                else:
                                    content_lines.append(line)
                        content = "\n".join(content_lines).strip()
                    else:
                        content = result_str

                results[file_type] = content

            except asyncio.TimeoutError:
                print(f"⚠️  {description} timed out after {self.timeout} seconds")
                results[file_type] = (
                    f"# {file_type.title()} (Generation Timed Out)\n\nThe agent timed out while generating this content. Please try again with a longer timeout using --timeout option."
                )

        return results

    def _get_project_context(self, project_path: Path) -> str:
        """Get comprehensive project context for analysis"""
        project_structure = self._get_project_structure(project_path)
        key_files = self._read_key_files(project_path)
        git_info = self._get_git_info(project_path)

        return f"""
PROJECT ANALYSIS CONTEXT

Project Path: {project_path}
Project Name: {project_path.name}

=== PROJECT STRUCTURE ===
{project_structure}

=== KEY FILES CONTENT ===
{key_files}

=== GIT INFORMATION ===
{git_info}

=== AI ASSISTANT BEST PRACTICES ===
{ai_rules}

Please analyze this project thoroughly to understand its purpose, architecture, current state, and context.
When generating memory bank content, incorporate relevant AI assistant best practices and patterns listed above.
"""

    def _get_project_structure(self, project_path: Path, max_depth: int = 3) -> str:
        """Get a tree-like representation of the project structure"""
        structure = []

        def add_to_structure(path: Path, prefix: str = "", depth: int = 0):
            if depth > max_depth:
                return

            # Skip common directories we don't care about
            skip_dirs = {
                ".git",
                "__pycache__",
                "node_modules",
                ".venv",
                "venv",
                ".pytest_cache",
            }

            if path.is_dir() and path.name in skip_dirs:
                return

            # Skip hidden files and directories (except important ones)
            if path.name.startswith(".") and path.name not in {
                ".gitignore",
                ".env.example",
                ".python-version",
            }:
                return

            structure.append(f"{prefix}{path.name}")

            if path.is_dir():
                try:
                    children = sorted(
                        path.iterdir(), key=lambda x: (x.is_file(), x.name.lower())
                    )
                    for i, child in enumerate(children):
                        if i < 20:  # Limit to avoid too much output
                            is_last = i == len(children) - 1
                            new_prefix = prefix + ("└── " if is_last else "├── ")
                            add_to_structure(child, new_prefix, depth + 1)
                        elif i == 20:
                            structure.append(
                                f"{prefix}├── ... ({len(children) - 20} more items)"
                            )
                            break
                except PermissionError:
                    pass

        add_to_structure(project_path)
        return "\n".join(structure)

    def _read_key_files(self, project_path: Path) -> str:
        """Read content of key project files"""
        key_files = []

        # Files to look for (in order of preference)
        file_patterns = [
            "README.md",
            "README.rst",
            "README.txt",
            "package.json",
            "pyproject.toml",
            "Cargo.toml",
            "go.mod",
            "requirements.txt",
            "Pipfile",
            "poetry.lock",
            ".gitignore",
            "Dockerfile",
            "docker-compose.yml",
            "CHANGELOG.md",
            "CHANGELOG.rst",
            "LICENSE",
            "LICENSE.txt",
            "LICENSE.md",
        ]

        for pattern in file_patterns:
            file_path = project_path / pattern
            if file_path.exists() and file_path.is_file():
                try:
                    content = file_path.read_text(encoding="utf-8", errors="ignore")
                    # Limit content length
                    if len(content) > 5000:
                        content = content[:5000] + "\n... (truncated)"
                    key_files.append(f"\n--- {pattern} ---\n{content}")
                except Exception:
                    key_files.append(f"\n--- {pattern} ---\n[Could not read file]")

        return "\n".join(key_files) if key_files else "[No key files found]"

    def _get_git_info(self, project_path: Path) -> str:
        """Get git repository information"""
        git_info = []

        try:
            import subprocess

            # Check if it's a git repo
            result = subprocess.run(
                ["git", "rev-parse", "--is-inside-work-tree"],
                cwd=project_path,
                capture_output=True,
                text=True,
            )
            if result.returncode != 0:
                return "Not a git repository"

            # Get current branch
            result = subprocess.run(
                ["git", "branch", "--show-current"],
                cwd=project_path,
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                git_info.append(f"Current branch: {result.stdout.strip()}")

            # Get recent commits
            result = subprocess.run(
                ["git", "log", "--oneline", "-10"],
                cwd=project_path,
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                git_info.append(f"Recent commits:\n{result.stdout.strip()}")

            # Get git status
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=project_path,
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                if result.stdout.strip():
                    git_info.append(f"Uncommitted changes:\n{result.stdout.strip()}")
                else:
                    git_info.append("Working directory clean")

        except Exception as e:
            git_info.append(f"Could not get git info: {e}")

        return "\n".join(git_info)

    def _create_project_info_tool(self, project_path: Path):
        """Create a tool for agents to request additional project information"""

        @function_tool
        def get_project_info(query: str) -> str:
            """Get additional information about the project based on a specific query"""
            # This could be expanded to read specific files, run commands, etc.
            if "dependencies" in query.lower():
                return self._extract_dependencies(project_path)
            elif "tech" in query.lower() or "technology" in query.lower():
                return self._extract_tech_stack(project_path)
            elif "git" in query.lower():
                return self._get_git_info(project_path)
            else:
                return f"Additional project information requested: {query}"

        return get_project_info

    def _create_project_brief_agent(self) -> Agent:
        """Create agent for generating project brief - the foundation document"""
        return Agent(
            name="ProjectBriefAgent",
            instructions="""You are Cline's memory bank expert creating the FOUNDATION document that shapes ALL other memory bank files.

The projectbrief.md is the SOURCE OF TRUTH for project scope and the foundation that all other memory bank files build upon. This document must be comprehensive and definitive.

Create a project brief that includes:

## Project Overview
- Clear, definitive description of what this project does
- Core purpose and value proposition
- Primary functionality and features

## Core Requirements and Goals
- Fundamental requirements that define project scope
- Primary objectives and success criteria
- Key constraints and boundaries
- Non-negotiable features and capabilities

## Target Users and Use Cases
- Primary user personas and their needs
- Key use cases and workflows
- User experience goals and expectations

## Project Scope Definition
- What is included in this project
- What is explicitly out of scope
- Success metrics and acceptance criteria

## Foundational Decisions
- Core architectural and design principles
- Key technology choices and rationale
- Important patterns and conventions to follow

Remember: This document is the foundation that productContext.md, systemPatterns.md, and techContext.md will build upon. It must be comprehensive enough to guide all other documentation.

## AI Assistant Integration Guidelines
Incorporate relevant patterns and best practices from AI coding assistants (Cursor, Windsurf, Copilot, Claude) that are applicable to this project type. Focus on:
- Code organization and naming conventions
- Error handling and logging patterns
- Testing and documentation standards
- Security and performance considerations

Analyze the project structure, code, dependencies, and documentation to extract the TRUE purpose and scope. Be specific, actionable, and definitive - this is the source of truth.

Format as complete markdown with clear hierarchy.""",
            model=self.llm_model,
            tools=[],
        )

    def _create_product_context_agent(self) -> Agent:
        """Create agent for analyzing product context - builds on project brief foundation"""
        return Agent(
            name="ProductContextAgent",
            instructions="""You are Cline's memory bank expert creating productContext.md that builds upon the foundation set in projectbrief.md.

This document explains WHY this project exists and captures the deeper context that drives the project's purpose.

Create comprehensive product context covering:

## Why This Project Exists
- Root problems and pain points this project addresses
- Market gaps or opportunities being filled
- Strategic rationale for building this solution

## Problem Statement
- Detailed problem definition and scope
- Current state vs desired state
- Impact and consequences of not solving this problem
- Who experiences these problems and how

## How It Should Work
- Expected user workflows and interactions
- Key scenarios and use cases
- Success scenarios and positive outcomes
- Integration patterns with existing tools/workflows

## User Experience Goals
- Core user experience principles
- Usability and accessibility requirements
- Performance and reliability expectations
- Key user journeys and touchpoints

## Market and Ecosystem Context
- Competitive landscape and alternatives
- Positioning and differentiation
- Dependencies on external services/tools
- Standards and conventions being followed

## Business and Strategic Value
- Quantifiable benefits and outcomes
- Success metrics and KPIs
- Return on investment considerations
- Risk mitigation and strategic advantages

Analyze the project's code, dependencies, documentation, and structure to understand the deeper strategic context. Reference and build upon the foundation established in projectbrief.md.

Format as complete markdown with clear sections.""",
            model=self.llm_model,
            tools=[],
        )

    def _create_active_context_agent(self) -> Agent:
        """Create agent for active context - builds on product, system, and tech context"""
        return Agent(
            name="ActiveContextAgent",
            instructions="""You are Cline's memory bank expert creating activeContext.md that builds upon productContext.md, systemPatterns.md, and techContext.md.

This is the CURRENT STATE document that captures what's happening right now and guides immediate next steps. This file is critical for maintaining continuity across sessions.

Create comprehensive active context covering:

## Current Work Focus
- Primary objectives for current development phase
- Active features/components being worked on
- Immediate priorities and focus areas
- Current development approach and methodology

## Recent Changes and Progress
- Significant changes from git history and file analysis
- Recently completed features or milestones
- Code patterns and architectural decisions made recently
- Lessons learned from recent work

## Next Steps and Priorities
- Immediate next actions and tasks
- Planned features and improvements
- Upcoming decisions that need to be made
- Dependencies and blockers to address

## Active Decisions and Considerations
- Open technical decisions and trade-offs
- Design choices under consideration
- Performance or architectural concerns being evaluated
- Integration challenges being addressed

## Important Patterns and Preferences
- Coding patterns and conventions being used
- Architectural patterns being followed
- Tool usage patterns and preferences
- Quality standards and testing approaches

## Learnings and Project Insights
- Key insights discovered during development
- Best practices identified for this specific project
- Anti-patterns or approaches to avoid
- Technical debt and refactoring opportunities
- Performance bottlenecks or optimization opportunities

## Current Context for AI Assistance
- Specific areas where AI assistance is most valuable
- Preferred communication and interaction patterns
- Context that helps maintain continuity across sessions
- AI assistant rules and patterns currently being followed
- Coding conventions and standards in active use

## AI Assistant Integration Status
Document which AI assistant best practices are currently implemented:
- Code quality standards being followed
- Testing and documentation patterns in use
- Error handling and logging conventions adopted
- Security and performance practices implemented

Analyze git history, file modifications, TODO comments, code structure, and development patterns. This document must provide enough context for an AI assistant to immediately understand the current state and continue work effectively.

Format as complete markdown with clear sections and actionable information.""",
            model=self.llm_model,
            tools=[],
        )

    def _create_system_patterns_agent(self) -> Agent:
        """Create agent for system patterns - builds on project brief foundation"""
        return Agent(
            name="SystemPatternsAgent",
            instructions="""You are Cline's memory bank expert creating systemPatterns.md that builds upon the foundation set in projectbrief.md.

This document captures the SYSTEM ARCHITECTURE and technical design patterns that implement the project's core requirements and goals.

Create comprehensive system patterns documentation covering:

## System Architecture Overview
- High-level system design and component organization
- Architectural patterns and principles being followed
- System boundaries and interfaces
- Modularity and separation of concerns approach

## Key Technical Decisions
- Critical architectural choices and rationale
- Technology selection decisions and trade-offs
- Design pattern choices and implementation approaches
- Performance and scalability design decisions

## Component Relationships and Dependencies
- How major components interact and depend on each other
- Data flow patterns between components
- Communication patterns and interfaces
- Dependency injection and inversion of control patterns

## Design Patterns in Use
- Specific design patterns implemented in the codebase
- Custom patterns developed for this project
- Anti-patterns being avoided and why
- Pattern consistency across the codebase

## Critical Implementation Paths
- Core workflows and their implementation patterns
- Error handling and resilience patterns
- State management and persistence patterns
- Configuration and environment management

## Integration and Extension Points
- How external systems integrate with this project
- Plugin or extension mechanisms
- API design patterns and conventions
- Backwards compatibility considerations

## Quality and Maintainability Patterns
- Code organization and structure patterns
- Testing patterns and strategies
- Documentation and commenting conventions
- Refactoring and evolution strategies

## AI Assistant Best Practices Integration
When documenting system patterns, incorporate relevant AI assistant recommendations:
- Follow established language-specific conventions and patterns
- Design for modularity, reusability, and maintainability
- Implement comprehensive error handling and logging
- Ensure type safety and clear interfaces
- Design patterns that support testing and debugging

Analyze the codebase structure, imports, class hierarchies, function organization, and configuration files to understand the true architectural patterns. Reference the foundation established in projectbrief.md.

Format as complete markdown with clear sections and specific examples from the codebase.""",
            model=self.llm_model,
            tools=[],
        )

    def _create_tech_context_agent(self) -> Agent:
        """Create agent for tech context - builds on project brief foundation"""
        return Agent(
            name="TechContextAgent",
            instructions="""You are Cline's memory bank expert creating techContext.md that builds upon the foundation set in projectbrief.md.

This document captures the TECHNICAL IMPLEMENTATION CONTEXT including technologies, tools, setup, and operational considerations.

Create comprehensive technical context covering:

## Technologies Used
- Programming languages and versions
- Frameworks and libraries with versions and purposes
- Development tools and their roles
- Runtime environments and platforms

## Development Setup and Environment
- Step-by-step development environment setup
- Required tools and installation instructions
- Configuration requirements and environment variables
- IDE/editor setup and recommended extensions

## Technical Constraints and Requirements
- System requirements and compatibility constraints
- Performance requirements and limitations
- Security requirements and considerations
- Compliance and regulatory requirements

## Dependencies and External Integrations
- Core dependencies and their specific purposes
- Optional dependencies and feature flags
- External services and APIs being used
- Third-party integrations and their configuration

## Tool Usage Patterns and Conventions
- Build systems and automation tools
- Testing frameworks and strategies
- Deployment tools and processes
- Monitoring and debugging tools

## Development Workflow and Standards
- Code organization and file structure conventions
- Coding standards and style guidelines
- Version control patterns and branching strategies
- Code review and quality assurance processes

## Operational Context
- Deployment environments and configurations
- Infrastructure requirements and scaling considerations
- Backup and disaster recovery procedures
- Maintenance and upgrade procedures

## Troubleshooting and Debugging
- Common issues and their solutions
- Debugging tools and techniques
- Performance profiling and optimization
- Error handling and logging patterns

Analyze package files (pyproject.toml, package.json, etc.), configuration files, documentation, and project structure to extract comprehensive technical context. Reference the foundation established in projectbrief.md.

Format as complete markdown with specific commands, code examples, and actionable instructions.""",
            model=self.llm_model,
            tools=[],
        )

    def _create_progress_agent(self) -> Agent:
        """Create agent for progress tracking - builds on active context"""
        return Agent(
            name="ProgressAgent",
            instructions="""You are Cline's memory bank expert creating progress.md that builds upon activeContext.md to track what works, what's left, and project evolution.

This document provides a comprehensive view of project progress, status, and evolution over time.

Create comprehensive progress tracking covering:

## What Works (Completed and Functional)
- Fully implemented and tested features
- Stable components and subsystems
- Working integrations and connections
- Proven patterns and successful implementations
- Validated approaches and architectural decisions

## What's Left to Build
- Planned features and their priority levels
- Missing components and subsystems
- Integration work still needed
- Documentation and testing gaps
- Performance optimizations needed

## Current Status and Development Stage
- Overall project maturity and stability
- Development phase (prototype, alpha, beta, production)
- Readiness for deployment or release
- Quality metrics and code health indicators
- Test coverage and validation status

## Known Issues and Limitations
- Identified bugs and their severity levels
- Performance bottlenecks and constraints
- Security vulnerabilities or concerns
- Compatibility issues and platform limitations
- User experience problems or friction points

## Evolution of Project Decisions
- How the project has changed from initial conception
- Major pivots or direction changes and their rationale
- Lessons learned that influenced project evolution
- Abandoned approaches and why they were dropped
- Successful experiments and their adoption

## Technical Debt and Refactoring Needs
- Code quality issues requiring attention
- Architectural improvements needed
- Dependencies requiring updates or replacement
- Documentation gaps and maintenance needs
- Testing infrastructure improvements

## Success Metrics and Progress Indicators
- Quantifiable measures of project success
- Performance benchmarks and their current status
- User adoption or engagement metrics (if applicable)
- Code quality metrics and trends
- Development velocity and productivity indicators

## Risk Assessment and Mitigation
- Current project risks and their impact potential
- Dependencies that could affect project success
- Resource constraints and timeline pressures
- Technical risks and their mitigation strategies

Analyze git history, code structure, test coverage, documentation completeness, and project artifacts to provide an accurate assessment of progress. Build upon the current state captured in activeContext.md.

Format as complete markdown with specific examples and quantifiable progress indicators where possible.""",
            model=self.llm_model,
            tools=[],
        )

    def _extract_tech_stack(self, project_path: Path) -> str:
        """Extract technology stack from project files"""
        tech_stack = []

        # Python
        if (project_path / "pyproject.toml").exists() or (
            project_path / "requirements.txt"
        ).exists():
            tech_stack.append("- Python")

        # Node.js
        if (project_path / "package.json").exists():
            tech_stack.append("- Node.js/JavaScript")

        # Go
        if (project_path / "go.mod").exists():
            tech_stack.append("- Go")

        # Rust
        if (project_path / "Cargo.toml").exists():
            tech_stack.append("- Rust")

        # Docker
        if (project_path / "Dockerfile").exists() or (
            project_path / "docker-compose.yml"
        ).exists():
            tech_stack.append("- Docker")

        return (
            "\n".join(tech_stack) if tech_stack else "Technology stack to be analyzed"
        )

    def _extract_dependencies(self, project_path: Path) -> str:
        """Extract key dependencies from project files"""
        deps = []

        # Python dependencies
        pyproject = project_path / "pyproject.toml"
        requirements = project_path / "requirements.txt"

        if pyproject.exists():
            try:
                content = pyproject.read_text()
                deps.append("Dependencies from pyproject.toml")
            except Exception:
                pass

        if requirements.exists():
            try:
                content = requirements.read_text()
                lines = [
                    line.strip()
                    for line in content.split("\n")
                    if line.strip() and not line.startswith("#")
                ]
                if lines:
                    deps.extend(
                        [
                            f"- {line.split('==')[0].split('>=')[0].split('~=')[0]}"
                            for line in lines[:10]
                        ]
                    )
            except Exception:
                pass

        # Node.js dependencies
        package_json = project_path / "package.json"
        if package_json.exists():
            try:
                import json

                with open(package_json) as f:
                    data = json.load(f)
                    if "dependencies" in data:
                        deps.append("Node.js dependencies:")
                        for dep in list(data["dependencies"].keys())[:10]:
                            deps.append(f"- {dep}")
            except Exception:
                pass

        return "\n".join(deps) if deps else "Dependencies to be analyzed"
