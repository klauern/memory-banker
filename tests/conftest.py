"""Global test configuration and fixtures."""

# Import specific fixtures from fixtures/conftest.py to make them available globally
from tests.fixtures.conftest import (  # noqa: F401
    empty_project,
    mock_llm_model,
    nodejs_project,
    python_project,
    sample_agent_responses,
    sample_project_context,
    temp_project_dir,
)
