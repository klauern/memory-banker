"""Integration tests that require real API access.

These tests are separated into their own directory to avoid import issues
and can be run explicitly when OPENAI_API_KEY is available.
"""

import os

import pytest

pytestmark = pytest.mark.requires_api


@pytest.fixture(scope="session")
def api_key():
    """Provide API key for tests, skip if not available."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        pytest.skip("OPENAI_API_KEY not provided - skipping API integration tests")
    return api_key


@pytest.mark.skipif(
    not os.getenv("OPENAI_API_KEY"),
    reason="OPENAI_API_KEY not provided"
)
class TestAPIIntegration:
    """Tests that require real OpenAI API access."""

    @pytest.mark.asyncio
    async def test_real_project_analysis(self, temp_project_dir, api_key):
        """Test real project analysis with API calls."""
        from memory_banker.cli import MemoryBankerCLI

        # Create a simple test project
        (temp_project_dir / "README.md").write_text("# Test Project\nA simple test project.")
        (temp_project_dir / "main.py").write_text("print('Hello World')")

        # Create CLI instance
        cli = MemoryBankerCLI(
            project_path=temp_project_dir,
            model="gpt-4o-mini",  # Use cheaper model for testing
            api_key=api_key,
            timeout=60  # Short timeout for testing
        )

        # Run real analysis
        analysis = await cli.agents.analyze_project(temp_project_dir)

        # Verify we got real results (not mocked)
        assert isinstance(analysis, dict)
        assert len(analysis) > 0

        # Check that we got actual content, not mock data
        for _key, content in analysis.items():
            assert isinstance(content, str)
            assert len(content) > 10  # Should have real content
            assert "Generation Timed Out" not in content

    @pytest.mark.asyncio
    async def test_memory_bank_creation_end_to_end(self, temp_project_dir, api_key):
        """Test complete memory bank creation workflow."""
        from memory_banker.cli import MemoryBankerCLI

        # Create a test project structure
        (temp_project_dir / "pyproject.toml").write_text("""
[project]
name = "test-project"
version = "0.1.0"
dependencies = ["click"]
""")
        (temp_project_dir / "README.md").write_text("# Test Project\nA test project for memory bank creation.")

        # Initialize CLI
        cli = MemoryBankerCLI(
            project_path=temp_project_dir,
            model="gpt-4o-mini",
            api_key=api_key,
            timeout=120
        )

        # Run full init process
        await cli.init()

        # Verify memory bank was created
        assert cli.memory_bank.exists()

        # Check that at least some memory bank files were created with real content
        memory_bank_path = temp_project_dir / "memory-bank"
        created_files = []
        for filename in cli.memory_bank.MEMORY_BANK_FILES:
            file_path = memory_bank_path / filename
            if file_path.exists():
                created_files.append(filename)
                content = file_path.read_text()
                assert len(content) > 50  # Should have substantial content
                # Should not contain mock indicators
                assert "Test Brief" not in content

        # Should have created at least some files
        assert len(created_files) > 0
