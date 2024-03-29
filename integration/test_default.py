"""Test the default route"""

import sys
import requests

ROOT_URL = 'http://localhost:8000'

def run_tests():
    """Main code execution"""

    res = requests.get(f'{ROOT_URL}')
    assert res.status_code == 200, 'Default route should succeed'

try:
    run_tests()
except AssertionError as assertion_error:
    print(f'AssertionError: {str(assertion_error)}', file=sys.stderr)
    sys.exit(1)
