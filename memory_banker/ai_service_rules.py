"""
AI Service Rules and Patterns for Memory Bank Enhancement

This module contains common rules, patterns, and best practices from various AI
coding assistants (Windsurf, Cursor, Copilot, Claude, etc.) that can be integrated
into memory bank generation to provide better context and guidance.
"""

from dataclasses import dataclass
from pathlib import Path


@dataclass
class ServiceRule:
    """Represents a rule or pattern from an AI service"""

    service: str
    category: str
    title: str
    description: str
    example: str = ""
    priority: str = "medium"  # low, medium, high
    applies_to: list[str] = None  # list of file types or contexts


class AIServiceRules:
    """Collection of rules and patterns from various AI coding services"""

    def __init__(self):
        self.rules = self._initialize_rules()

    def _initialize_rules(self) -> list[ServiceRule]:
        """Initialize the comprehensive set of AI service rules"""
        return [
            # === CURSOR RULES ===
            ServiceRule(
                service="Cursor",
                category="code_context",
                title="Provide Clear Context in Comments",
                description="Always include context about what code does and why, especially for complex logic",
                example="// This function handles user authentication by validating JWT tokens\n// and checking against our Redis cache for session management",
                priority="high",
                applies_to=["all"],
            ),
            ServiceRule(
                service="Cursor",
                category="file_organization",
                title="Use Descriptive File and Function Names",
                description="Names should clearly indicate purpose and functionality",
                example="getUserAuthenticationStatus() instead of checkUser()",
                priority="medium",
                applies_to=["all"],
            ),
            ServiceRule(
                service="Cursor",
                category="error_handling",
                title="Implement Comprehensive Error Handling",
                description="Always handle edge cases and provide meaningful error messages",
                example="try {\n  // operation\n} catch (error) {\n  logger.error('Failed to process user data:', error);\n  throw new ProcessingError('User data validation failed', error);\n}",
                priority="high",
                applies_to=["all"],
            ),
            # === WINDSURF RULES ===
            ServiceRule(
                service="Windsurf",
                category="code_consistency",
                title="Follow Established Patterns",
                description="Maintain consistency with existing codebase patterns and conventions",
                example="If the codebase uses async/await pattern, continue using it consistently",
                priority="high",
                applies_to=["all"],
            ),
            ServiceRule(
                service="Windsurf",
                category="dependency_management",
                title="Minimize External Dependencies",
                description="Prefer built-in solutions over external libraries when reasonable",
                example="Use native JSON parsing instead of adding a JSON library",
                priority="medium",
                applies_to=["all"],
            ),
            ServiceRule(
                service="Windsurf",
                category="performance",
                title="Optimize for Common Use Cases",
                description="Design code to perform well for the most frequent operations",
                example="Cache frequently accessed data, use efficient data structures",
                priority="medium",
                applies_to=["all"],
            ),
            # === COPILOT RULES ===
            ServiceRule(
                service="Copilot",
                category="testing",
                title="Write Tests for All Public Functions",
                description="Every public function should have corresponding unit tests",
                example="test('should authenticate valid user', async () => {\n  const result = await authenticateUser(validCredentials);\n  expect(result.success).toBe(true);\n});",
                priority="high",
                applies_to=["all"],
            ),
            ServiceRule(
                service="Copilot",
                category="documentation",
                title="Document Function Parameters and Return Values",
                description="Use JSDoc, docstrings, or similar to document function interfaces",
                example="/**\n * Authenticates a user with provided credentials\n * @param {Object} credentials - User credentials\n * @param {string} credentials.username - Username\n * @param {string} credentials.password - Password\n * @returns {Promise<AuthResult>} Authentication result\n */",
                priority="medium",
                applies_to=["all"],
            ),
            ServiceRule(
                service="Copilot",
                category="security",
                title="Validate All User Inputs",
                description="Never trust user input; always validate and sanitize",
                example="if (!username || typeof username !== 'string' || username.length > 100) {\n  throw new ValidationError('Invalid username');\n}",
                priority="high",
                applies_to=["all"],
            ),
            # === CLAUDE RULES ===
            ServiceRule(
                service="Claude",
                category="code_clarity",
                title="Prefer Explicit Over Implicit",
                description="Make code intentions clear and avoid implicit behaviors",
                example="Use explicit type annotations, clear variable names, and obvious control flow",
                priority="high",
                applies_to=["all"],
            ),
            ServiceRule(
                service="Claude",
                category="modularity",
                title="Design for Reusability",
                description="Create modular, composable functions that can be easily reused",
                example="Break large functions into smaller, focused functions with single responsibilities",
                priority="medium",
                applies_to=["all"],
            ),
            ServiceRule(
                service="Claude",
                category="configuration",
                title="Use Configuration Files for Settings",
                description="Externalize configuration to make code more flexible and maintainable",
                example="Use .env files, config.json, or similar for environment-specific settings",
                priority="medium",
                applies_to=["all"],
            ),
            # === GENERAL AI ASSISTANT RULES ===
            ServiceRule(
                service="General",
                category="code_review",
                title="Follow Language-Specific Best Practices",
                description="Adhere to established conventions for the programming language in use",
                example="Python: Use snake_case, follow PEP 8. JavaScript: Use camelCase, follow ESLint rules",
                priority="high",
                applies_to=["all"],
            ),
            ServiceRule(
                service="General",
                category="git_practices",
                title="Write Meaningful Commit Messages",
                description="Commit messages should explain what and why, not just what",
                example="'Add user authentication validation' instead of 'Update auth.js'",
                priority="medium",
                applies_to=["all"],
            ),
            ServiceRule(
                service="General",
                category="logging",
                title="Implement Structured Logging",
                description="Use consistent logging levels and structured data for better debugging",
                example="logger.info('User authenticated', { userId, timestamp, method: 'oauth' })",
                priority="medium",
                applies_to=["all"],
            ),
            # === FRAMEWORK-SPECIFIC RULES ===
            ServiceRule(
                service="General",
                category="api_design",
                title="Design RESTful APIs",
                description="Follow REST principles for API design when building web services",
                example="GET /users/:id for retrieval, POST /users for creation, PUT /users/:id for updates",
                priority="medium",
                applies_to=["web", "api"],
            ),
            ServiceRule(
                service="General",
                category="database",
                title="Use Database Migrations",
                description="Version control database schema changes with migration files",
                example="Create migration files for schema changes, never modify existing migrations",
                priority="high",
                applies_to=["database"],
            ),
            ServiceRule(
                service="General",
                category="frontend",
                title="Implement Responsive Design",
                description="Ensure UI works across different screen sizes and devices",
                example="Use CSS Grid/Flexbox, media queries, and mobile-first design principles",
                priority="medium",
                applies_to=["frontend", "web"],
            ),
            # === COLLABORATION RULES ===
            ServiceRule(
                service="General",
                category="collaboration",
                title="Use Type Annotations",
                description="Provide type information to help other developers understand interfaces",
                example="TypeScript interfaces, Python type hints, or language-specific type systems",
                priority="medium",
                applies_to=["all"],
            ),
            ServiceRule(
                service="General",
                category="collaboration",
                title="Include Setup Instructions",
                description="Provide clear instructions for setting up the development environment",
                example="README with prerequisites, installation steps, and getting started guide",
                priority="high",
                applies_to=["all"],
            ),
        ]

    def get_rules_for_context(self, context: str) -> list[ServiceRule]:
        """Get rules that apply to a specific context"""
        return [
            rule
            for rule in self.rules
            if rule.applies_to is None
            or "all" in rule.applies_to
            or context in rule.applies_to
        ]

    def get_rules_by_service(self, service: str) -> list[ServiceRule]:
        """Get all rules from a specific service"""
        return [rule for rule in self.rules if rule.service.lower() == service.lower()]

    def get_rules_by_category(self, category: str) -> list[ServiceRule]:
        """Get all rules in a specific category"""
        return [rule for rule in self.rules if rule.category == category]

    def get_high_priority_rules(self) -> list[ServiceRule]:
        """Get all high priority rules"""
        return [rule for rule in self.rules if rule.priority == "high"]

    def detect_project_context(self, project_path: Path) -> list[str]:
        """Detect project context based on files and structure"""
        contexts = []

        # Check for web/frontend indicators
        if (project_path / "package.json").exists():
            contexts.append("web")
            package_json = project_path / "package.json"
            try:
                import json

                with open(package_json) as f:
                    data = json.load(f)
                    deps = {
                        **(data.get("dependencies", {})),
                        **(data.get("devDependencies", {})),
                    }

                    # Frontend frameworks
                    if any(fw in deps for fw in ["react", "vue", "angular", "svelte"]):
                        contexts.append("frontend")

                    # API frameworks
                    if any(fw in deps for fw in ["express", "fastify", "koa", "hapi"]):
                        contexts.append("api")

            except Exception:
                pass

        # Check for Python web frameworks
        if (project_path / "requirements.txt").exists() or (
            project_path / "pyproject.toml"
        ).exists():
            try:
                # Check requirements.txt
                req_file = project_path / "requirements.txt"
                if req_file.exists():
                    content = req_file.read_text()
                    if any(
                        fw in content
                        for fw in ["django", "flask", "fastapi", "tornado"]
                    ):
                        contexts.extend(["web", "api"])

                # Check pyproject.toml
                pyproject = project_path / "pyproject.toml"
                if pyproject.exists():
                    content = pyproject.read_text()
                    if any(
                        fw in content
                        for fw in ["django", "flask", "fastapi", "tornado"]
                    ):
                        contexts.extend(["web", "api"])

            except Exception:
                pass

        # Check for database indicators
        db_files = ["models.py", "schema.sql", "migrations", "alembic"]
        if any((project_path / f).exists() for f in db_files):
            contexts.append("database")

        # Check for mobile development
        mobile_files = ["android", "ios", "flutter", "react-native"]
        if any((project_path / f).exists() for f in mobile_files):
            contexts.append("mobile")

        return contexts if contexts else ["general"]

    def get_applicable_rules(self, project_path: Path) -> list[ServiceRule]:
        """Get all rules applicable to the given project"""
        contexts = self.detect_project_context(project_path)
        applicable_rules = []

        for context in contexts:
            applicable_rules.extend(self.get_rules_for_context(context))

        # Remove duplicates while preserving order
        seen = set()
        unique_rules = []
        for rule in applicable_rules:
            rule_id = (rule.service, rule.category, rule.title)
            if rule_id not in seen:
                seen.add(rule_id)
                unique_rules.append(rule)

        return unique_rules

    def format_rules_for_memory_bank(self, rules: list[ServiceRule]) -> str:
        """Format rules for inclusion in memory bank files"""
        if not rules:
            return ""

        sections = {}
        for rule in rules:
            if rule.category not in sections:
                sections[rule.category] = []
            sections[rule.category].append(rule)

        formatted = ["## AI Assistant Best Practices and Patterns\n"]
        formatted.append(
            "*The following patterns and practices are recommended by various AI coding assistants to improve code quality, maintainability, and collaboration.*\n"
        )

        for category, category_rules in sections.items():
            formatted.append(f"### {category.replace('_', ' ').title()}")

            for rule in category_rules:
                formatted.append(f"**{rule.title}** ({rule.service})")
                formatted.append(f"{rule.description}")

                if rule.example:
                    formatted.append("```")
                    formatted.append(rule.example)
                    formatted.append("```")

                formatted.append("")

        return "\n".join(formatted)
