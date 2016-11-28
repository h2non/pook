# -*- coding: utf-8 -*-

import re
import os
import subprocess

# Regular expression used to match Python files
pyfile = re.compile('.py$')

# List of allowed example to fail
allowed_errors = (
    'simulated_error.py'
)


def test_examples():
    # List of file examples
    examples = [f for f in os.listdir('examples') if pyfile.match(f)]

    # Test file example
    for example in examples:
        code = subprocess.call(['python', 'examples/{}'.format(example)])

        expected = 1 if example in allowed_errors else 0
        if code != expected:
            raise AssertionError('invalid exit code: {}'.format(example))
