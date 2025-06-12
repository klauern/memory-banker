"""Unit tests for MemoryBankerCLI class."""

from unittest.mock import patch

import pytest

from memory_banker.cli import MemoryBankerCLI


class TestMemoryBankerCLI:
    """Test cases for MemoryBankerCLI class."""

    @pytest.fixture
    def mock_api_key(self, monkeypatch):
        """Mock API key environment variable."""
        monkeypatch.setenv("OPENAI_API_KEY", "test-api-key")

    def test_init_success(self, temp_project_dir, mock_api_key):
        """Test MemoryBankerCLI initialization with valid parameters."""
        cli = MemoryBankerCLI(
            project_path=temp_project_dir,
            model="gpt-4o-mini",
            api_key="test-key",
            timeout=120,
        )

        assert cli.project_path == temp_project_dir
        assert cli.model == "gpt-4o-mini"
        assert cli.api_key == "test-key"
        assert cli.timeout == 120
        assert cli.llm_model is not None
        assert cli.memory_bank is not None
        assert cli.agents is not None

    def test_init_api_key_from_env(self, temp_project_dir, mock_api_key):
        """Test MemoryBankerCLI gets API key from environment."""
        cli = MemoryBankerCLI(project_path=temp_project_dir, model="gpt-4o-mini")

        assert cli.api_key == "test-api-key"

    def test_init_no_api_key_raises_error(self, temp_project_dir):
        """Test MemoryBankerCLI validates API key requirement."""
        # Clear any existing API key from environment
        import os

        old_key = os.environ.get("OPENAI_API_KEY")
        if old_key:
            del os.environ["OPENAI_API_KEY"]

        try:
            with pytest.raises(ValueError, match="API key must be provided"):
                MemoryBankerCLI(project_path=temp_project_dir, model="gpt-4o-mini")
        finally:
            # Restore the API key if it existed
            if old_key:
                os.environ["OPENAI_API_KEY"] = old_key

    def test_init_default_timeout(self, temp_project_dir, mock_api_key):
        """Test MemoryBankerCLI uses default timeout."""
        cli = MemoryBankerCLI(
            project_path=temp_project_dir, model="gpt-4o-mini", api_key="test-key"
        )

        assert cli.timeout == 300  # Default timeout

    @pytest.mark.asyncio
    @patch("agents.extensions.models.litellm_model.LitellmModel")
    @patch("click.echo")
    async def test_init_command_success(
        self, mock_echo, mock_model, temp_project_dir, mock_api_key
    ):
        """Test init command creates memory bank successfully."""
        cli = MemoryBankerCLI(
            project_path=temp_project_dir,
            model="gpt-4o-mini",
            api_key="test-key",
            timeout=60,
        )

        # Mock the agents and memory bank
        with (
            patch.object(cli.agents, "analyze_project") as mock_analyze,
            patch.object(cli.memory_bank, "create_directory") as mock_create_dir,
            patch.object(cli.memory_bank, "create_files") as mock_create_files,
        ):
            mock_analyze.return_value = {"projectbrief": "# Test Brief"}
            mock_create_dir.return_value = temp_project_dir / "memory-bank"

            await cli.init()

            # Verify calls were made
            mock_create_dir.assert_called_once()
            mock_analyze.assert_called_once_with(temp_project_dir)
            mock_create_files.assert_called_once_with({"projectbrief": "# Test Brief"})

            # Verify output messages (check key messages, not exact format)
            echo_calls = [str(call) for call in mock_echo.call_args_list]
            echo_output = " ".join(echo_calls)

            assert "Initializing memory bank" in echo_output
            assert "memory bank directory" in echo_output
            assert "Analyzing project structure" in echo_output
            assert "timeout per agent" in echo_output
            assert "Generating memory bank files" in echo_output
            assert "initialized successfully" in echo_output

    @pytest.mark.asyncio
    @patch("agents.extensions.models.litellm_model.LitellmModel")
    @patch("click.echo")
    async def test_update_command_success(
        self, mock_echo, mock_model, temp_project_dir, mock_api_key
    ):
        """Test update command updates existing memory bank."""
        cli = MemoryBankerCLI(
            project_path=temp_project_dir, model="gpt-4o-mini", api_key="test-key"
        )

        # Mock the agents and memory bank
        with (
            patch.object(cli.memory_bank, "exists", return_value=True) as mock_exists,
            patch.object(cli.agents, "analyze_project") as mock_analyze,
            patch.object(cli.memory_bank, "update_files") as mock_update_files,
        ):
            mock_analyze.return_value = {"projectbrief": "# Updated Brief"}

            await cli.update()

            # Verify calls were made
            mock_exists.assert_called_once()
            mock_analyze.assert_called_once_with(temp_project_dir)
            mock_update_files.assert_called_once_with(
                {"projectbrief": "# Updated Brief"}
            )

            # Verify output messages
            mock_echo.assert_any_call(
                f"🔄 Updating memory bank for project at: {temp_project_dir}"
            )
            mock_echo.assert_any_call("🔍 Re-analyzing project...")
            mock_echo.assert_any_call("📝 Updating memory bank files...")
            mock_echo.assert_any_call("✅ Memory bank updated successfully!")

    @pytest.mark.asyncio
    @patch("click.echo")
    async def test_update_command_no_existing_bank(
        self, mock_echo, temp_project_dir, mock_api_key
    ):
        """Test update command when no existing memory bank exists."""
        cli = MemoryBankerCLI(
            project_path=temp_project_dir, model="gpt-4o-mini", api_key="test-key"
        )

        with patch.object(cli.memory_bank, "exists", return_value=False):
            await cli.update()

            # Should show error message and return early
            mock_echo.assert_any_call(
                "❌ No existing memory bank found. Use 'init' command first."
            )

    @pytest.mark.asyncio
    @patch("click.echo")
    async def test_refresh_command_with_existing_bank(
        self, mock_echo, temp_project_dir, mock_api_key
    ):
        """Test refresh command removes existing bank and reinitializes."""
        cli = MemoryBankerCLI(
            project_path=temp_project_dir, model="gpt-4o-mini", api_key="test-key"
        )

        with (
            patch.object(cli.memory_bank, "exists", return_value=True) as mock_exists,
            patch.object(cli.memory_bank, "remove") as mock_remove,
            patch.object(cli, "init") as mock_init,
        ):
            await cli.refresh()

            # Verify existing bank was removed
            mock_exists.assert_called_once()
            mock_remove.assert_called_once()
            mock_init.assert_called_once()

            # Verify output messages
            mock_echo.assert_any_call(
                f"🔄 Refreshing memory bank for project at: {temp_project_dir}"
            )
            mock_echo.assert_any_call("🗑️  Removing existing memory bank...")

    @pytest.mark.asyncio
    @patch("click.echo")
    async def test_refresh_command_no_existing_bank(
        self, mock_echo, temp_project_dir, mock_api_key
    ):
        """Test refresh command when no existing memory bank exists."""
        cli = MemoryBankerCLI(
            project_path=temp_project_dir, model="gpt-4o-mini", api_key="test-key"
        )

        with (
            patch.object(cli.memory_bank, "exists", return_value=False),
            patch.object(cli, "init") as mock_init,
        ):
            await cli.refresh()

            # Should still call init but not try to remove
            mock_init.assert_called_once()

            # Should show refresh message but not removal message
            mock_echo.assert_any_call(
                f"🔄 Refreshing memory bank for project at: {temp_project_dir}"
            )
            # Should not have removal message
            assert not any("🗑️" in str(call) for call in mock_echo.call_args_list)

    @pytest.mark.asyncio
    async def test_init_propagates_exceptions(self, temp_project_dir, mock_api_key):
        """Test that exceptions from agents or memory bank are propagated."""
        cli = MemoryBankerCLI(
            project_path=temp_project_dir, model="gpt-4o-mini", api_key="test-key"
        )

        with patch.object(cli.agents, "analyze_project") as mock_analyze:
            mock_analyze.side_effect = Exception("Analysis failed")

            with pytest.raises(Exception, match="Analysis failed"):
                await cli.init()

    @pytest.mark.asyncio
    async def test_update_propagates_exceptions(self, temp_project_dir, mock_api_key):
        """Test that exceptions from update are propagated."""
        cli = MemoryBankerCLI(
            project_path=temp_project_dir, model="gpt-4o-mini", api_key="test-key"
        )

        with (
            patch.object(cli.memory_bank, "exists", return_value=True),
            patch.object(cli.agents, "analyze_project") as mock_analyze,
        ):
            mock_analyze.side_effect = Exception("Update failed")

            with pytest.raises(Exception, match="Update failed"):
                await cli.update()
