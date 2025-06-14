"""Integration tests focusing on CLI interface only."""

from unittest.mock import AsyncMock, Mock, patch

import pytest
from click.testing import CliRunner

from memory_banker.cli import cli


class TestCLIInterface:
    """Test CLI interface and argument handling."""

    @pytest.fixture
    def runner(self):
        """Create a Click test runner."""
        return CliRunner()

    def test_cli_help(self, runner):
        """Test CLI help command."""
        result = runner.invoke(cli, ["--help"])

        assert result.exit_code == 0
        assert (
            "Memory Banker - Agentically create Cline-style memory banks"
            in result.output
        )
        assert "--project-path" in result.output
        assert "--model" in result.output
        assert "--api-key" in result.output
        assert "--api-base" in result.output
        assert "--timeout" in result.output
        assert "init" in result.output
        assert "update" in result.output
        assert "refresh" in result.output

    def test_init_help(self, runner):
        """Test init command help."""
        result = runner.invoke(cli, ["init", "--help"])

        assert result.exit_code == 0
        assert "Initialize a new memory bank for the project" in result.output

    def test_update_help(self, runner):
        """Test update command help."""
        result = runner.invoke(cli, ["update", "--help"])

        assert result.exit_code == 0
        assert "Update existing memory bank files" in result.output

    def test_refresh_help(self, runner):
        """Test refresh command help."""
        result = runner.invoke(cli, ["refresh", "--help"])

        assert result.exit_code == 0
        assert "Completely refresh/rebuild the memory bank" in result.output

    def test_invalid_project_path(self, runner):
        """Test CLI handles invalid project path."""
        result = runner.invoke(cli, ["--project-path", "/nonexistent/path", "init"])

        assert result.exit_code != 0
        assert "does not exist" in result.output or "Invalid value" in result.output

    def test_invalid_timeout(self, runner, temp_project_dir):
        """Test CLI handles invalid timeout value."""
        result = runner.invoke(
            cli,
            ["--project-path", str(temp_project_dir), "--timeout", "invalid", "init"],
        )

        assert result.exit_code != 0
        assert "Invalid value" in result.output

    @patch("memory_banker.cli.MemoryBankerCLI")
    def test_parameter_passing(
        self, mock_cli_class, runner, temp_project_dir, monkeypatch
    ):
        """Test that CLI parameters are passed correctly to MemoryBankerCLI."""
        # Clear environment variables to test explicit parameters
        monkeypatch.delenv("OPENAI_API_BASE", raising=False)

        # Mock to prevent actual instantiation
        mock_cli_instance = Mock()
        mock_cli_instance.init = AsyncMock()
        mock_cli_class.return_value = mock_cli_instance

        runner.invoke(
            cli,
            [
                "--project-path",
                str(temp_project_dir),
                "--model",
                "gpt-4",
                "--api-key",
                "test-key",
                "--timeout",
                "600",
                "init",
            ],
        )

        # Should attempt to create CLI with correct parameters
        mock_cli_class.assert_called_once_with(
            project_path=temp_project_dir,
            model="gpt-4",
            api_key="test-key",
            api_base=None,
            timeout=600,
        )

    @patch("memory_banker.cli.MemoryBankerCLI")
    def test_environment_api_key(
        self, mock_cli_class, runner, temp_project_dir, monkeypatch
    ):
        """Test that API key is read from environment."""
        monkeypatch.setenv("OPENAI_API_KEY", "env-api-key")
        monkeypatch.delenv("OPENAI_API_BASE", raising=False)

        mock_cli_instance = Mock()
        mock_cli_instance.init = AsyncMock()
        mock_cli_class.return_value = mock_cli_instance

        runner.invoke(cli, ["--project-path", str(temp_project_dir), "init"])

        # Should use environment API key
        args, kwargs = mock_cli_class.call_args
        assert kwargs["api_key"] == "env-api-key"
        assert kwargs["api_base"] is None

    @patch("memory_banker.cli.MemoryBankerCLI")
    def test_environment_api_base(
        self, mock_cli_class, runner, temp_project_dir, monkeypatch
    ):
        """Test that API base URL is read from environment."""
        monkeypatch.setenv("OPENAI_API_KEY", "test-key")
        monkeypatch.setenv("OPENAI_API_BASE", "https://custom.api.com/v1")

        mock_cli_instance = Mock()
        mock_cli_instance.init = AsyncMock()
        mock_cli_class.return_value = mock_cli_instance

        runner.invoke(cli, ["--project-path", str(temp_project_dir), "init"])

        # Should use environment API base
        args, kwargs = mock_cli_class.call_args
        assert kwargs["api_base"] == "https://custom.api.com/v1"

    @patch("memory_banker.cli.MemoryBankerCLI")
    def test_default_values(
        self, mock_cli_class, runner, temp_project_dir, monkeypatch
    ):
        """Test CLI default values."""
        monkeypatch.setenv("OPENAI_API_KEY", "test-key")
        monkeypatch.delenv("OPENAI_API_BASE", raising=False)

        mock_cli_instance = Mock()
        mock_cli_instance.init = AsyncMock()
        mock_cli_class.return_value = mock_cli_instance

        runner.invoke(cli, ["--project-path", str(temp_project_dir), "init"])

        args, kwargs = mock_cli_class.call_args
        assert kwargs["model"] == "gpt-4.1-mini"  # Default model
        assert kwargs["timeout"] == 300  # Default timeout
        assert kwargs["api_key"] == "test-key"
        assert kwargs["api_base"] is None  # Default api_base
