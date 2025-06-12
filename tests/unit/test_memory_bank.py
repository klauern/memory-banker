"""Unit tests for MemoryBank class."""

import pytest
from pathlib import Path
from unittest.mock import patch, mock_open

from memory_banker.memory_bank import MemoryBank


class TestMemoryBank:
    """Test cases for MemoryBank class."""

    @pytest.fixture
    def memory_bank(self, temp_project_dir):
        """Create a MemoryBank instance for testing."""
        return MemoryBank(temp_project_dir)

    def test_init(self, temp_project_dir):
        """Test MemoryBank initialization."""
        memory_bank = MemoryBank(temp_project_dir)

        assert memory_bank.project_path == temp_project_dir
        assert memory_bank.memory_bank_path == temp_project_dir / "memory-bank"
        assert memory_bank.MEMORY_BANK_FILES == [
            "projectbrief.md",
            "productContext.md",
            "activeContext.md",
            "systemPatterns.md",
            "techContext.md",
            "progress.md",
        ]

    def test_exists_false_when_directory_not_exists(self, memory_bank):
        """Test exists() returns False when memory bank directory doesn't exist."""
        assert not memory_bank.exists()

    def test_exists_true_when_directory_exists(self, memory_bank):
        """Test exists() returns True when memory bank directory exists."""
        memory_bank.memory_bank_path.mkdir()
        assert memory_bank.exists()

    def test_create_directory(self, memory_bank):
        """Test create_directory() creates the memory bank directory."""
        assert not memory_bank.memory_bank_path.exists()

        result = memory_bank.create_directory()

        assert memory_bank.memory_bank_path.exists()
        assert memory_bank.memory_bank_path.is_dir()
        assert result == memory_bank.memory_bank_path

    def test_create_directory_existing(self, memory_bank):
        """Test create_directory() works when directory already exists."""
        memory_bank.memory_bank_path.mkdir()

        result = memory_bank.create_directory()

        assert memory_bank.memory_bank_path.exists()
        assert result == memory_bank.memory_bank_path

    def test_remove_existing_directory(self, memory_bank):
        """Test remove() removes existing memory bank directory."""
        memory_bank.memory_bank_path.mkdir()
        test_file = memory_bank.memory_bank_path / "test.md"
        test_file.write_text("test content")

        assert memory_bank.memory_bank_path.exists()

        memory_bank.remove()

        assert not memory_bank.memory_bank_path.exists()

    def test_remove_nonexistent_directory(self, memory_bank):
        """Test remove() handles non-existent directory gracefully."""
        assert not memory_bank.memory_bank_path.exists()

        # Should not raise an exception
        memory_bank.remove()

        assert not memory_bank.memory_bank_path.exists()

    @pytest.mark.asyncio
    async def test_create_files(self, memory_bank, sample_agent_responses):
        """Test create_files() creates all memory bank files."""
        memory_bank.create_directory()

        await memory_bank.create_files(sample_agent_responses)

        # Check that all expected files were created
        for file_key, filename in [
            ("projectbrief", "projectbrief.md"),
            ("productContext", "productContext.md"),
            ("activeContext", "activeContext.md"),
            ("systemPatterns", "systemPatterns.md"),
            ("techContext", "techContext.md"),
            ("progress", "progress.md"),
        ]:
            file_path = memory_bank.memory_bank_path / filename
            assert file_path.exists(), f"{filename} was not created"

            # Verify content was written
            content = file_path.read_text(encoding="utf-8")
            assert content == sample_agent_responses[file_key]

    @pytest.mark.asyncio
    async def test_create_files_missing_analysis(self, memory_bank):
        """Test create_files() handles missing analysis keys gracefully."""
        memory_bank.create_directory()

        partial_analysis = {
            "projectbrief": "# Test Brief\nContent here.",
            "techContext": "# Tech Context\nTech details here.",
        }

        await memory_bank.create_files(partial_analysis)

        # Check that only provided files were created
        assert (memory_bank.memory_bank_path / "projectbrief.md").exists()
        assert (memory_bank.memory_bank_path / "techContext.md").exists()

        # Check that missing files were not created
        assert not (memory_bank.memory_bank_path / "productContext.md").exists()
        assert not (memory_bank.memory_bank_path / "progress.md").exists()

    @pytest.mark.asyncio
    async def test_update_files(self, memory_bank, sample_agent_responses):
        """Test update_files() calls create_files()."""
        memory_bank.create_directory()

        # Create initial files
        await memory_bank.create_files(sample_agent_responses)

        # Modify analysis
        updated_analysis = sample_agent_responses.copy()
        updated_analysis["projectbrief"] = "# Updated Project Brief\nUpdated content."

        await memory_bank.update_files(updated_analysis)

        # Verify file was updated
        content = (memory_bank.memory_bank_path / "projectbrief.md").read_text(
            encoding="utf-8"
        )
        assert content == "# Updated Project Brief\nUpdated content."

    @pytest.mark.asyncio
    async def test_create_files_unicode_content(self, memory_bank):
        """Test create_files() handles unicode content correctly."""
        memory_bank.create_directory()

        unicode_analysis = {
            "projectbrief": "# Project Brief 🚀\n\nThis contains émojis and spéciál characters: αβγ",
            "techContext": "# Technical Context 🔧\n\n中文 русский العربية",
        }

        await memory_bank.create_files(unicode_analysis)

        # Verify unicode content was written correctly
        brief_content = (memory_bank.memory_bank_path / "projectbrief.md").read_text(
            encoding="utf-8"
        )
        assert "🚀" in brief_content
        assert "émojis" in brief_content
        assert "αβγ" in brief_content

        tech_content = (memory_bank.memory_bank_path / "techContext.md").read_text(
            encoding="utf-8"
        )
        assert "🔧" in tech_content
        assert "中文" in tech_content
        assert "русский" in tech_content
        assert "العربية" in tech_content
