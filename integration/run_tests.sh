#!/bin/bash

echo "$(date) - Running integration tests"

echo "$(date) - Activating virtual environment"
source venv/bin/activate

for TEST_FILE in test_*.py; do
    echo "$(date) - Running '$TEST_FILE'"
done
