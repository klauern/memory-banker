"""Integration tests for CLI commands."""

import pytest
from click.testing import CliRunner
from unittest.mock import patch, Mock, AsyncMock
from pathlib import Path

from main import cli


class TestCLICommands:
    """Integration tests for CLI commands."""
    
    @pytest.fixture
    def runner(self):
        """Create a Click test runner."""
        return CliRunner()
    
    @pytest.fixture
    def mock_api_key(self, monkeypatch):
        """Mock API key environment variable."""
        monkeypatch.setenv("OPENAI_API_KEY", "test-api-key")
    
    def test_cli_help(self, runner):
        """Test CLI help command."""
        result = runner.invoke(cli, ['--help'])
        
        assert result.exit_code == 0
        assert "Memory Banker - Agentically create Cline-style memory banks" in result.output
        assert "--project-path" in result.output
        assert "--model" in result.output
        assert "--api-key" in result.output
        assert "--timeout" in result.output
        assert "init" in result.output
        assert "update" in result.output
        assert "refresh" in result.output
    
    def test_init_help(self, runner):
        """Test init command help."""
        result = runner.invoke(cli, ['init', '--help'])
        
        assert result.exit_code == 0
        assert "Initialize a new memory bank for the project" in result.output
    
    def test_update_help(self, runner):
        """Test update command help."""
        result = runner.invoke(cli, ['update', '--help'])
        
        assert result.exit_code == 0
        assert "Update existing memory bank files" in result.output
    
    def test_refresh_help(self, runner):
        """Test refresh command help."""
        result = runner.invoke(cli, ['refresh', '--help'])
        
        assert result.exit_code == 0
        assert "Completely refresh/rebuild the memory bank" in result.output
    
    def test_init_no_api_key(self, runner, temp_project_dir):
        """Test init command fails without API key."""
        with runner.isolated_filesystem():
            result = runner.invoke(cli, [
                '--project-path', str(temp_project_dir),
                'init'
            ])
            
            assert result.exit_code != 0
            assert "API key must be provided" in result.output
    
    @patch('memory_banker.agents.MemoryBankAgents')
    @patch('memory_banker.memory_bank.MemoryBank') 
    @patch('agents.extensions.models.litellm_model.LitellmModel')
    def test_init_success(self, mock_model, mock_memory_bank, mock_agents, runner, temp_project_dir, mock_api_key):
        """Test successful init command."""
        # Mock the components to avoid real API calls
        mock_agents_instance = Mock()
        mock_agents_instance.analyze_project = AsyncMock(return_value={"test": "data"})
        mock_agents.return_value = mock_agents_instance
        
        mock_memory_bank_instance = Mock()
        mock_memory_bank_instance.create_directory = Mock(return_value=temp_project_dir / "memory-bank")
        mock_memory_bank_instance.create_files = AsyncMock()
        mock_memory_bank.return_value = mock_memory_bank_instance
        
        result = runner.invoke(cli, [
            '--project-path', str(temp_project_dir),
            '--model', 'gpt-4o-mini',
            '--timeout', '120',
            'init'
        ])
        
        assert result.exit_code == 0
        
        # Verify CLI was initialized with correct parameters
        mock_cli_class.assert_called_once_with(
            project_path=temp_project_dir,
            model='gpt-4o-mini',
            api_key='test-api-key',
            timeout=120
        )
        
        # Verify init method was called
        mock_cli_instance.init.assert_called_once()
    
    @patch('memory_banker.cli.MemoryBankerCLI')
    def test_update_success(self, mock_cli_class, runner, temp_project_dir, mock_api_key):
        """Test successful update command."""
        mock_cli_instance = Mock()
        mock_cli_instance.update = Mock()
        mock_cli_class.return_value = mock_cli_instance
        
        result = runner.invoke(cli, [
            '--project-path', str(temp_project_dir),
            'update'
        ])
        
        assert result.exit_code == 0
        mock_cli_instance.update.assert_called_once()
    
    @patch('memory_banker.cli.MemoryBankerCLI')
    def test_refresh_success(self, mock_cli_class, runner, temp_project_dir, mock_api_key):
        """Test successful refresh command."""
        mock_cli_instance = Mock()
        mock_cli_instance.refresh = Mock()
        mock_cli_class.return_value = mock_cli_instance
        
        result = runner.invoke(cli, [
            '--project-path', str(temp_project_dir),
            'refresh'
        ])
        
        assert result.exit_code == 0
        mock_cli_instance.refresh.assert_called_once()
    
    def test_default_project_path(self, runner, mock_api_key):
        """Test CLI uses current directory as default project path."""
        with patch('memory_banker.cli.MemoryBankerCLI') as mock_cli_class:
            mock_cli_instance = Mock()
            mock_cli_class.return_value = mock_cli_instance
            
            result = runner.invoke(cli, ['init'])
            
            # Should use current working directory
            args, kwargs = mock_cli_class.call_args
            assert kwargs['project_path'] == Path.cwd()
    
    def test_custom_model(self, runner, temp_project_dir, mock_api_key):
        """Test CLI accepts custom model parameter."""
        with patch('memory_banker.cli.MemoryBankerCLI') as mock_cli_class:
            mock_cli_instance = Mock()
            mock_cli_class.return_value = mock_cli_instance
            
            result = runner.invoke(cli, [
                '--project-path', str(temp_project_dir),
                '--model', 'gpt-4',
                'init'
            ])
            
            assert result.exit_code == 0
            args, kwargs = mock_cli_class.call_args
            assert kwargs['model'] == 'gpt-4'
    
    def test_custom_api_key(self, runner, temp_project_dir):
        """Test CLI accepts custom API key parameter."""
        with patch('memory_banker.cli.MemoryBankerCLI') as mock_cli_class:
            mock_cli_instance = Mock()
            mock_cli_class.return_value = mock_cli_instance
            
            result = runner.invoke(cli, [
                '--project-path', str(temp_project_dir),
                '--api-key', 'custom-key',
                'init'
            ])
            
            assert result.exit_code == 0
            args, kwargs = mock_cli_class.call_args
            assert kwargs['api_key'] == 'custom-key'
    
    def test_custom_timeout(self, runner, temp_project_dir, mock_api_key):
        """Test CLI accepts custom timeout parameter."""
        with patch('memory_banker.cli.MemoryBankerCLI') as mock_cli_class:
            mock_cli_instance = Mock()
            mock_cli_class.return_value = mock_cli_instance
            
            result = runner.invoke(cli, [
                '--project-path', str(temp_project_dir),
                '--timeout', '600',
                'init'
            ])
            
            assert result.exit_code == 0
            args, kwargs = mock_cli_class.call_args
            assert kwargs['timeout'] == 600
    
    def test_invalid_project_path(self, runner, mock_api_key):
        """Test CLI handles invalid project path."""
        result = runner.invoke(cli, [
            '--project-path', '/nonexistent/path',
            'init'
        ])
        
        assert result.exit_code != 0
        assert "does not exist" in result.output or "Invalid value" in result.output
    
    @patch('memory_banker.cli.MemoryBankerCLI')
    def test_cli_exception_handling(self, mock_cli_class, runner, temp_project_dir, mock_api_key):
        """Test CLI handles exceptions gracefully."""
        mock_cli_instance = Mock()
        mock_cli_instance.init.side_effect = Exception("Test error")
        mock_cli_class.return_value = mock_cli_instance
        
        result = runner.invoke(cli, [
            '--project-path', str(temp_project_dir),
            'init'
        ])
        
        assert result.exit_code != 0
        # Click should show the exception
        assert "Test error" in result.output
    
    def test_default_values(self, runner, temp_project_dir, mock_api_key):
        """Test CLI uses correct default values."""
        with patch('memory_banker.cli.MemoryBankerCLI') as mock_cli_class:
            mock_cli_instance = Mock()
            mock_cli_class.return_value = mock_cli_instance
            
            result = runner.invoke(cli, [
                '--project-path', str(temp_project_dir),
                'init'
            ])
            
            assert result.exit_code == 0
            args, kwargs = mock_cli_class.call_args
            
            # Check default values
            assert kwargs['model'] == 'gpt-4.1-mini'  # From updated main.py
            assert kwargs['api_key'] == 'test-api-key'  # From env
            assert kwargs['timeout'] == 300  # Default timeout