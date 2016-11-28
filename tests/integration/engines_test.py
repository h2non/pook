# -*- coding: utf-8 -*-

import subprocess

# List of engine specific test commands to run
engine_tests = (
    'py.test tests/integration/engines/pytest_suite.py',
    'nosetests tests/integration/engines/nose_suite.py',
    'python -m unittest tests.integration.engines.unittest_suite',
)


def test_engines():
    for cmd in engine_tests:
        args = cmd.split(' ')
        code = subprocess.call(args)

        if code != 0:
            raise AssertionError('invalid exit code for: {}'.format(cmd))
