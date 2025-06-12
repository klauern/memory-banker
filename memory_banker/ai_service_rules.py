"""
AI Service Rules and Patterns for Memory Bank Enhancement

This module provides functionality to load and work with AI service rules
that are stored in an external JSON configuration file. This approach improves
maintainability, load performance, and allows for easier rule updates.
"""

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class ServiceRule:
    """Represents a rule or pattern from an AI service"""

    service: str
    category: str
    title: str
    description: str
    example: str = ""
    priority: str = "medium"  # low, medium, high
    applies_to: Optional[list[str]] = None  # list of file types or contexts


class AIServiceRules:
    """Collection of rules and patterns from various AI coding services"""

    def __init__(self, rules_file: Optional[Path] = None):
        """
        Initialize AI service rules from external JSON file

        Args:
            rules_file: Path to the JSON file containing rules. If None, uses default location.
        """
        if rules_file is None:
            # Use the JSON file in the same directory as this module
            rules_file = Path(__file__).parent / "ai_service_rules.json"

        self.rules_file = rules_file
        self.rules = self._load_rules()

    def _load_rules(self) -> list[ServiceRule]:
        """Load rules from the external JSON file"""
        try:
            with open(self.rules_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            return [ServiceRule.from_dict(rule_data) for rule_data in data["rules"]]

        except FileNotFoundError:
            raise FileNotFoundError(
                f"AI service rules file not found: {self.rules_file}. "
                "Please ensure the ai_service_rules.json file exists."
            )
        except json.JSONDecodeError as e:
            raise ValueError(
                f"Invalid JSON in rules file {self.rules_file}: {e}"
            )
        except KeyError as e:
            raise ValueError(
                f"Missing required key in rules file {self.rules_file}: {e}"
            )

    def reload_rules(self) -> None:
        """Reload rules from the JSON file (useful for testing or dynamic updates)"""
        self.rules = self._load_rules()

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
                with open(package_json, encoding="utf-8") as f:
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

            except (json.JSONDecodeError, FileNotFoundError):
                pass

        # Check for Python web frameworks
        if (project_path / "requirements.txt").exists() or (
            project_path / "pyproject.toml"
        ).exists():
            try:
                # Check requirements.txt
                req_file = project_path / "requirements.txt"
                if req_file.exists():
                    content = req_file.read_text(encoding="utf-8")
                    if any(
                        fw in content
                        for fw in ["django", "flask", "fastapi", "tornado"]
                    ):
                        contexts.extend(["web", "api"])

                # Check pyproject.toml
                pyproject = project_path / "pyproject.toml"
                if pyproject.exists():
                    content = pyproject.read_text(encoding="utf-8")
                    if any(
                        fw in content
                        for fw in ["django", "flask", "fastapi", "tornado"]
                    ):
                        contexts.extend(["web", "api"])

            except FileNotFoundError:
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
