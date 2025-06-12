# Testing Strategy

This project uses a comprehensive testing strategy that separates unit tests from integration tests requiring API access.

## Test Types

### Unit Tests
- **Location**: `tests/unit/`
- **Purpose**: Test individual components in isolation
- **API Calls**: All mocked/stubbed
- **Run by default**: Yes
- **Command**: `task test` or `pytest -m "not requires_api"`

### Integration Tests
- **Location**: `tests/integration/`
- **Types**:
  - CLI interface tests (mocked API calls)
  - API integration tests (real API calls - marked with `@pytest.mark.requires_api`)
- **Command**:
  - All integration: `pytest tests/integration/`
  - API only: `task test-api` or `pytest -m "requires_api"`

## Running Tests

### Local Development

```bash
# Run unit tests only (default, no API key needed)
task test
# or
pytest

# Run all tests including API tests (requires OPENAI_API_KEY)
task test-all
# or
pytest --override-ini="addopts="

# Run only API integration tests
task test-api
# or
pytest -m "requires_api"

# Run with coverage
task test-cov
```

### API Key Requirements

- **Unit tests**: No API key required (all API calls are mocked)
- **API integration tests**: Require `OPENAI_API_KEY` environment variable
- **API tests are skipped automatically** if no API key is provided

### CI/CD

The GitHub Actions workflow runs:

1. **Unit Tests** (always): All tests except those marked `requires_api`
2. **API Integration Tests** (conditional): Only if `OPENAI_API_KEY` secret is available

## Test Configuration

- **pytest.ini**: Configured to skip API tests by default with `-m "not requires_api"`
- **Markers**:
  - `requires_api`: Tests that need real OpenAI API access
  - `unit`: Unit tests
  - `integration`: Integration tests
  - `slow`: Slow-running tests

## Writing Tests

### Unit Tests
```python
# tests/unit/test_example.py
def test_something():
    # Mock all external dependencies
    with patch('module.external_call') as mock_call:
        # Test logic
        pass
```

### API Integration Tests
```python
# tests/integration/test_api_integration.py
@pytest.mark.requires_api
class TestAPIIntegration:
    def setup_method(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            pytest.skip("OPENAI_API_KEY not provided")

    async def test_real_api_call(self):
        # Test with real API calls
        pass
```

## Coverage

- Target: 80%+ coverage
- Focus: Unit tests provide the majority of coverage
- API tests validate end-to-end functionality but don't significantly impact coverage metrics
