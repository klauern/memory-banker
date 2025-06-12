"""Global test configuration and fixtures."""

import pytest
from click.testing import CliRunner

# Import all fixtures from fixtures/conftest.py to make them available globally
from tests.fixtures.conftest import *  # noqa: F401,F403


@pytest.fixture
def runner():
    """Click test runner fixture."""
    return CliRunner()
