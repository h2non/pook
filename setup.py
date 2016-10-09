#!/usr/bin/env python
"""
pook
====
A utility library for mocking out HTTP traffic in Python.

:copyright: (c) 2016 Tomas Aparicio
:license: MIT
"""

import sys
import logging

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import pkg_resources

setup_requires = []

if 'test' in sys.argv:
    setup_requires.append('pytest')

tests_require = [
    'pytest',
    'coverage >= 3.7.1, < 5.0.0',
    'pytest-cov',
    'flake8',
]


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['tests/']
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


setup(
    name='pook',
    version='0.0.1',
    author='Tomas Aparicio',
    description=(
        'Expressive and simple library for mocking out HTTP traffic in Python.'
    ),
    url='https://github.com/h2non/pook',
    license='MIT',
    long_description=open('README.md').read(),
    py_modules=['pook'],
    zip_safe=False,
    tests_require=tests_require,
    packages=find_packages(exclude=['tests', 'examples']),
    cmdclass={'test': PyTest},
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development'
    ],
)
