"""Test VM creation"""

import sys
import requests

ROOT_URL = 'http://localhost:8000'

def run_tests():
    """Main code execution"""

    res = requests.post(f'{ROOT_URL}/vm/test/small')
    assert res.status_code == 200, 'VM creation should work'

try:
    run_tests()
except AssertionError as assertion_error:
    print(f'AssertionError: {str(assertion_error)}', file=sys.stderr)
    sys.exit(1)
