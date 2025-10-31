# FastAPI Tests

This directory contains comprehensive tests for the Mergington High School Activities FastAPI application.

## Test Structure

### Test Files

- **`test_api.py`** - Tests for main API endpoints including activities retrieval, signup, and unregister functionality
- **`test_static.py`** - Tests for static file serving (HTML, CSS, JavaScript)
- **`test_edge_cases.py`** - Edge cases and error handling tests
- **`conftest.py`** - Test configuration and fixtures

### Test Coverage

The test suite achieves **100% code coverage** of the application code and includes:

- ✅ **24 test cases** covering all endpoints and functionality
- ✅ **API endpoint testing** (GET /activities, POST /signup, DELETE /unregister)
- ✅ **Static file serving** verification
- ✅ **Error handling** for invalid inputs and edge cases
- ✅ **Data integrity** validation
- ✅ **Workflow testing** (complete signup/unregister cycles)

## Running Tests

### Method 1: Using the Test Runner Script
```bash
./run_tests.sh
```

### Method 2: Direct pytest execution
```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=term-missing -v

# Run with HTML coverage report
pytest tests/ --cov=src --cov-report=html -v
```

### Method 3: Run specific test files
```bash
# Run only API tests
pytest tests/test_api.py -v

# Run only edge case tests
pytest tests/test_edge_cases.py -v

# Run only static file tests
pytest tests/test_static.py -v
```

## Test Categories

### 1. Core API Tests (`test_api.py`)
- Root path redirect functionality
- Activities retrieval with proper data structure
- Successful participant signup
- Participant unregistration
- Error handling for non-existent activities
- Duplicate signup prevention
- Complete workflow testing
- Data integrity validation
- URL encoding handling

### 2. Static File Tests (`test_static.py`)
- HTML file serving
- CSS file serving
- JavaScript file serving
- 404 handling for non-existent files

### 3. Edge Case Tests (`test_edge_cases.py`)
- Missing email parameters
- Invalid activity names
- Long emails and unicode characters
- Case sensitivity
- Concurrent signups
- Maximum participant limits
- Malformed requests

## Fixtures

### `client`
Provides a FastAPI test client for making HTTP requests to the application.

### `reset_activities`
Resets the activities data to the original state before each test to ensure test isolation.

## Dependencies

The tests require the following packages (automatically installed):
- `pytest` - Testing framework
- `httpx` - HTTP client for FastAPI testing
- `pytest-asyncio` - Async test support
- `pytest-cov` - Coverage reporting

## Coverage Report

After running tests with coverage, you can view the detailed HTML report:
1. Open `htmlcov/index.html` in your browser
2. View line-by-line coverage details
3. Identify any missed code paths (currently 100% coverage)

## CI/CD Integration

These tests are designed to be easily integrated into CI/CD pipelines:
- Fast execution (< 1 second)
- No external dependencies
- Clear pass/fail reporting
- Coverage metrics included