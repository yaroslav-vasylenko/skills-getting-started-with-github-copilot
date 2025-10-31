#!/bin/bash

# FastAPI Test Runner Script
# This script runs all tests with coverage reporting

echo "🚀 Running FastAPI Tests with Coverage..."
echo "==========================================="

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
    echo "✅ Virtual environment activated"
fi

# Run tests with coverage
python -m pytest tests/ --cov=src --cov-report=term-missing --cov-report=html -v

# Check if tests passed
if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 All tests passed!"
    echo "📊 Coverage report generated in htmlcov/ directory"
    echo "🌐 Open htmlcov/index.html in your browser to view detailed coverage"
else
    echo ""
    echo "❌ Some tests failed. Please check the output above."
    exit 1
fi