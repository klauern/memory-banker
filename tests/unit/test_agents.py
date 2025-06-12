"""Unit tests for MemoryBankAgents class."""

import pytest
import asyncio
from pathlib import Path
from unittest.mock import Mock, patch, AsyncMock
import subprocess

from memory_banker.agents import MemoryBankAgents


class TestMemoryBankAgents:
    """Test cases for MemoryBankAgents class."""

    @pytest.fixture
    def agents(self, mock_llm_model):
        """Create a MemoryBankAgents instance for testing."""
        return MemoryBankAgents(mock_llm_model, timeout=60)

    def test_init(self, mock_llm_model):
        """Test MemoryBankAgents initialization."""
        agents = MemoryBankAgents(mock_llm_model, timeout=120)

        assert agents.llm_model == mock_llm_model
        assert agents.timeout == 120

    def test_init_default_timeout(self, mock_llm_model):
        """Test MemoryBankAgents initialization with default timeout."""
        agents = MemoryBankAgents(mock_llm_model)

        assert agents.timeout == 300  # Default timeout

    def test_get_project_structure(self, agents, python_project):
        """Test _get_project_structure() generates correct structure."""
        structure = agents._get_project_structure(python_project)

        assert python_project.name in structure
        assert "pyproject.toml" in structure
        assert "README.md" in structure
        assert "test_project" in structure
        assert "__init__.py" in structure
        assert "main.py" in structure
        assert ".gitignore" in structure

    def test_get_project_structure_max_depth(self, agents, temp_project_dir):
        """Test _get_project_structure() respects max_depth parameter."""
        # Create a deep directory structure
        deep_path = temp_project_dir / "level1" / "level2" / "level3" / "level4"
        deep_path.mkdir(parents=True)
        (deep_path / "deep_file.txt").write_text("deep content")

        structure = agents._get_project_structure(temp_project_dir, max_depth=2)

        # Should include level1 and level2, but not level3 or level4
        assert "level1" in structure
        assert "level2" in structure
        assert "level3" not in structure
        assert "deep_file.txt" not in structure

    def test_get_project_structure_skip_dirs(self, agents, temp_project_dir):
        """Test _get_project_structure() skips common directories."""
        # Create directories that should be skipped
        for skip_dir in [
            ".git",
            "__pycache__",
            "node_modules",
            ".venv",
            ".pytest_cache",
        ]:
            (temp_project_dir / skip_dir).mkdir()
            (temp_project_dir / skip_dir / "file.txt").write_text("content")

        structure = agents._get_project_structure(temp_project_dir)

        # Should not include skipped directories
        assert ".git" not in structure
        assert "__pycache__" not in structure
        assert "node_modules" not in structure
        assert ".venv" not in structure
        assert ".pytest_cache" not in structure

    def test_read_key_files_python_project(self, agents, python_project):
        """Test _read_key_files() reads important files from Python project."""
        key_files = agents._read_key_files(python_project)

        assert "--- README.md ---" in key_files
        assert "Test Project" in key_files  # Content from README
        assert "--- pyproject.toml ---" in key_files
        assert "test-project" in key_files  # Content from pyproject.toml
        assert "--- .gitignore ---" in key_files
        assert "__pycache__" in key_files  # Content from .gitignore

    def test_read_key_files_nodejs_project(self, agents, nodejs_project):
        """Test _read_key_files() reads important files from Node.js project."""
        key_files = agents._read_key_files(nodejs_project)

        assert "--- README.md ---" in key_files
        assert "--- package.json ---" in key_files
        assert "test-nodejs-project" in key_files
        assert "express" in key_files

    def test_read_key_files_empty_project(self, agents, empty_project):
        """Test _read_key_files() handles empty project."""
        key_files = agents._read_key_files(empty_project)

        assert key_files == "[No key files found]"

    def test_read_key_files_truncation(self, agents, temp_project_dir):
        """Test _read_key_files() truncates large files."""
        large_content = "x" * 6000  # Larger than 5000 char limit
        large_file = temp_project_dir / "README.md"
        large_file.write_text(large_content)

        key_files = agents._read_key_files(temp_project_dir)

        assert "--- README.md ---" in key_files
        assert "... (truncated)" in key_files
        assert len(key_files) < len(large_content) + 1000  # Should be much smaller

    @patch("subprocess.run")
    def test_get_git_info_not_git_repo(self, mock_run, agents, temp_project_dir):
        """Test _get_git_info() handles non-git repository."""
        mock_run.return_value.returncode = 1

        git_info = agents._get_git_info(temp_project_dir)

        assert git_info == "Not a git repository"

    @patch("subprocess.run")
    def test_get_git_info_success(self, mock_run, agents, temp_project_dir):
        """Test _get_git_info() extracts git information successfully."""
        # Mock successful git commands
        mock_results = [
            Mock(returncode=0),  # git rev-parse --is-inside-work-tree
            Mock(returncode=0, stdout="main"),  # git branch --show-current
            Mock(
                returncode=0, stdout="abc123 Initial commit\ndef456 Add feature"
            ),  # git log --oneline -10
            Mock(returncode=0, stdout=""),  # git status --porcelain (clean)
        ]
        mock_run.side_effect = mock_results

        git_info = agents._get_git_info(temp_project_dir)

        assert "Current branch: main" in git_info
        assert "Recent commits:" in git_info
        assert "abc123 Initial commit" in git_info
        assert "Working directory clean" in git_info

    @patch("subprocess.run")
    def test_get_git_info_dirty_working_dir(self, mock_run, agents, temp_project_dir):
        """Test _get_git_info() handles dirty working directory."""
        mock_results = [
            Mock(returncode=0),  # git rev-parse
            Mock(returncode=0, stdout="main"),  # git branch
            Mock(returncode=0, stdout="abc123 Initial commit"),  # git log
            Mock(returncode=0, stdout="M  file1.py\n?? file2.py"),  # git status (dirty)
        ]
        mock_run.side_effect = mock_results

        git_info = agents._get_git_info(temp_project_dir)

        assert "Uncommitted changes:" in git_info
        assert "M  file1.py" in git_info
        assert "?? file2.py" in git_info

    @patch("subprocess.run")
    def test_get_git_info_exception(self, mock_run, agents, temp_project_dir):
        """Test _get_git_info() handles exceptions gracefully."""
        mock_run.side_effect = Exception("Git command failed")

        git_info = agents._get_git_info(temp_project_dir)

        assert "Could not get git info:" in git_info
        assert "Git command failed" in git_info

    def test_get_project_context(self, agents, python_project):
        """Test _get_project_context() creates comprehensive context."""
        with patch.object(agents, "_get_git_info", return_value="Git info here"):
            context = agents._get_project_context(python_project)

        assert "PROJECT ANALYSIS CONTEXT" in context
        assert f"Project Path: {python_project}" in context
        assert f"Project Name: {python_project.name}" in context
        assert "=== PROJECT STRUCTURE ===" in context
        assert "=== KEY FILES CONTENT ===" in context
        assert "=== GIT INFORMATION ===" in context
        assert "Git info here" in context
        assert "pyproject.toml" in context
        assert "README.md" in context

    def test_extract_tech_stack_python(self, agents, python_project):
        """Test _extract_tech_stack() identifies Python project."""
        tech_stack = agents._extract_tech_stack(python_project)

        assert "- Python" in tech_stack

    def test_extract_tech_stack_nodejs(self, agents, nodejs_project):
        """Test _extract_tech_stack() identifies Node.js project."""
        tech_stack = agents._extract_tech_stack(nodejs_project)

        assert "- Node.js/JavaScript" in tech_stack

    def test_extract_tech_stack_empty(self, agents, empty_project):
        """Test _extract_tech_stack() handles empty project."""
        tech_stack = agents._extract_tech_stack(empty_project)

        assert tech_stack == "Technology stack to be analyzed"

    def test_extract_dependencies_python(self, agents, python_project):
        """Test _extract_dependencies() extracts Python dependencies."""
        deps = agents._extract_dependencies(python_project)

        assert "Dependencies from pyproject.toml" in deps

    def test_extract_dependencies_nodejs(self, agents, nodejs_project):
        """Test _extract_dependencies() extracts Node.js dependencies."""
        deps = agents._extract_dependencies(nodejs_project)

        assert "Node.js dependencies:" in deps
        assert "- express" in deps
        assert "- axios" in deps

    def test_extract_dependencies_empty(self, agents, empty_project):
        """Test _extract_dependencies() handles empty project."""
        deps = agents._extract_dependencies(empty_project)

        assert deps == "Dependencies to be analyzed"

    @pytest.mark.asyncio
    async def test_analyze_project_timeout(self, agents, python_project):
        """Test analyze_project() handles timeout correctly."""
        # Set very short timeout
        agents.timeout = 0.1

        async def slow_runner(*args, **kwargs):
            await asyncio.sleep(1)  # Sleep longer than timeout
            return Mock()

        with patch("agents.Runner.run") as mock_run:
            mock_run.side_effect = slow_runner

            results = await agents.analyze_project(python_project)

            # Should have timeout messages for all agents
            for agent_type in [
                "projectbrief",
                "productContext",
                "activeContext",
                "systemPatterns",
                "techContext",
                "progress",
            ]:
                assert agent_type in results
                assert "timed out" in results[agent_type]
                assert "Generation Timed Out" in results[agent_type]

    def test_create_project_info_tool(self, agents, python_project):
        """Test _create_project_info_tool() creates a tool object."""
        tool_func = agents._create_project_info_tool(python_project)

        # Just verify the tool is created
        assert tool_func is not None

        # We can test the underlying functionality directly
        # Test dependencies extraction
        deps = agents._extract_dependencies(python_project)
        assert "Dependencies from pyproject.toml" in deps

        # Test tech stack extraction
        tech_stack = agents._extract_tech_stack(python_project)
        assert "- Python" in tech_stack
