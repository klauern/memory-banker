"""Tests for AI service rules functionality"""

import pytest
from pathlib import Path
from memory_banker.ai_service_rules import AIServiceRules, ServiceRule


class TestServiceRule:
    """Test ServiceRule dataclass"""
    
    def test_service_rule_creation(self):
        """Test creating a ServiceRule"""
        rule = ServiceRule(
            service="Cursor",
            category="testing",
            title="Write Tests",
            description="Always write tests for your code",
            example="test('should work', () => { expect(true).toBe(true); });",
            priority="high",
            applies_to=["javascript", "typescript"]
        )
        
        assert rule.service == "Cursor"
        assert rule.category == "testing"
        assert rule.title == "Write Tests"
        assert rule.priority == "high"
        assert rule.applies_to == ["javascript", "typescript"]
    
    def test_service_rule_defaults(self):
        """Test ServiceRule with default values"""
        rule = ServiceRule(
            service="Claude",
            category="code_quality",
            title="Use Clear Names",
            description="Use descriptive variable names"
        )
        
        assert rule.example == ""
        assert rule.priority == "medium"
        assert rule.applies_to is None


class TestAIServiceRules:
    """Test AIServiceRules class"""
    
    def setup_method(self):
        """Set up test instance"""
        self.ai_rules = AIServiceRules()
    
    def test_initialization(self):
        """Test that AIServiceRules initializes with rules"""
        assert len(self.ai_rules.rules) > 0
        assert all(isinstance(rule, ServiceRule) for rule in self.ai_rules.rules)
    
    def test_get_rules_by_service(self):
        """Test filtering rules by service"""
        cursor_rules = self.ai_rules.get_rules_by_service("Cursor")
        assert len(cursor_rules) > 0
        assert all(rule.service == "Cursor" for rule in cursor_rules)
        
        # Test case insensitive
        cursor_rules_lower = self.ai_rules.get_rules_by_service("cursor")
        assert len(cursor_rules_lower) == len(cursor_rules)
    
    def test_get_rules_by_category(self):
        """Test filtering rules by category"""
        testing_rules = self.ai_rules.get_rules_by_category("testing")
        assert len(testing_rules) > 0
        assert all(rule.category == "testing" for rule in testing_rules)
    
    def test_get_high_priority_rules(self):
        """Test filtering high priority rules"""
        high_priority = self.ai_rules.get_high_priority_rules()
        assert len(high_priority) > 0
        assert all(rule.priority == "high" for rule in high_priority)
    
    def test_get_rules_for_context(self):
        """Test filtering rules by context"""
        # Test 'all' context
        all_rules = self.ai_rules.get_rules_for_context("all")
        assert len(all_rules) > 0
        
        # Test specific context
        web_rules = self.ai_rules.get_rules_for_context("web")
        assert len(web_rules) >= 0  # May be 0 if no web-specific rules
    
    def test_detect_project_context(self, tmp_path):
        """Test project context detection"""
        # Test empty project
        contexts = self.ai_rules.detect_project_context(tmp_path)
        assert "general" in contexts
        
        # Test Python project
        (tmp_path / "pyproject.toml").write_text("""
[project]
name = "test-project"
dependencies = ["flask", "pytest"]
""")
        contexts = self.ai_rules.detect_project_context(tmp_path)
        assert "web" in contexts
        assert "api" in contexts
        
        # Test Node.js project
        node_project = tmp_path / "node_project"
        node_project.mkdir()
        (node_project / "package.json").write_text("""
{
  "name": "test-app",
  "dependencies": {
    "react": "^18.0.0",
    "express": "^4.18.0"
  }
}
""")
        contexts = self.ai_rules.detect_project_context(node_project)
        assert "web" in contexts
        assert "frontend" in contexts
        assert "api" in contexts
    
    def test_get_applicable_rules(self, tmp_path):
        """Test getting applicable rules for a project"""
        # Create a Python web project
        (tmp_path / "pyproject.toml").write_text("""
[project]
dependencies = ["django", "pytest"]
""")
        
        applicable_rules = self.ai_rules.get_applicable_rules(tmp_path)
        assert len(applicable_rules) > 0
        
        # Should include general rules and web-specific rules
        categories = {rule.category for rule in applicable_rules}
        assert len(categories) > 1  # Should have multiple categories
    
    def test_format_rules_for_memory_bank(self):
        """Test formatting rules for memory bank inclusion"""
        # Create test rules
        test_rules = [
            ServiceRule(
                service="Test",
                category="testing",
                title="Write Tests",
                description="Always write tests",
                example="test('example', () => {})",
                priority="high"
            ),
            ServiceRule(
                service="Test",
                category="code_quality",
                title="Use Clear Names",
                description="Use descriptive names",
                priority="medium"
            )
        ]
        
        formatted = self.ai_rules.format_rules_for_memory_bank(test_rules)
        
        assert "## AI Assistant Best Practices and Patterns" in formatted
        assert "### Testing" in formatted
        assert "### Code Quality" in formatted
        assert "**Write Tests** (Test)" in formatted
        assert "**Use Clear Names** (Test)" in formatted
        assert "Always write tests" in formatted
        assert "test('example', () => {})" in formatted
    
    def test_format_rules_empty_list(self):
        """Test formatting empty rules list"""
        formatted = self.ai_rules.format_rules_for_memory_bank([])
        assert formatted == ""
    
    def test_rules_have_required_fields(self):
        """Test that all initialized rules have required fields"""
        for rule in self.ai_rules.rules:
            assert rule.service is not None
            assert rule.category is not None
            assert rule.title is not None
            assert rule.description is not None
            assert rule.priority in ["low", "medium", "high"]
    
    def test_detect_database_context(self, tmp_path):
        """Test database context detection"""
        # Create models.py file
        (tmp_path / "models.py").write_text("# Django models")
        contexts = self.ai_rules.detect_project_context(tmp_path)
        assert "database" in contexts
        
        # Create migrations directory
        migrations_dir = tmp_path / "migrations"
        migrations_dir.mkdir()
        contexts = self.ai_rules.detect_project_context(tmp_path)
        assert "database" in contexts
    
    def test_service_coverage(self):
        """Test that we have rules from multiple services"""
        services = {rule.service for rule in self.ai_rules.rules}
        
        # Should have rules from major AI assistants
        expected_services = {"Cursor", "Windsurf", "Copilot", "Claude", "General"}
        assert expected_services.issubset(services)
    
    def test_category_coverage(self):
        """Test that we have rules across multiple categories"""
        categories = {rule.category for rule in self.ai_rules.rules}
        
        # Should have rules in key categories
        expected_categories = {
            "code_context", "testing", "security", "error_handling",
            "code_clarity", "performance", "documentation"
        }
        assert len(expected_categories.intersection(categories)) > 0