#!/bin/bash

echo "$(date) - Running integration tests"

echo "$(date) - Activating virtual environment"
source venv/bin/activate

for TEST_FILE in test_*.py; do
    echo "$(date) - Running '$TEST_FILE' ... "

    if ! python "$TEST_FILE"; then
        echo "$(date) - Failed at '$TEST_FILE'"
        exit 1
    else
        echo "$(date) - Passed at '$TEST_FILE'"
    fi
done
