import re
import sys
from unittest import TestCase
from .regex import isregex, strip_regex, isregex_expr

# If running Python 3
PY_3 = sys.version_info >= (3,)


def equal(x, y):
    """
    Shortcut function for ``unittest.TestCase.assertEqual()``.

    Arguments:
        x (mixed)
        y (mixed)

    Raises:
        AssertionError: in case of assertion error.

    Returns:
        bool
    """
    if PY_3:
        return TestCase().assertEqual(x, y) or True

    assert x == y


def matches(x, y, regex_expr=False):
    """
    Tries to match a regular expression value ``x`` against ``y``.
    Aliast``unittest.TestCase.assertEqual()``

    Arguments:
        x (regex|str): regular expression to test.
        y (str): value to match.
        regex_expr (bool): enables regex string based expression matching.

    Raises:
        AssertionError: in case of mismatching.

    Returns:
        bool
    """
    # Parse regex expression, if needed
    x = strip_regex(x) if regex_expr and isregex_expr(x) else x

    # Run regex assertion
    if PY_3:
        # Retrieve original regex pattern
        x = x.pattern if isregex(x) else x
        # Assert regular expression via unittest matchers
        return TestCase().assertRegexpMatches(y, x) or True

    # Primitive regex matching for Python 2.7
    if isinstance(x, str):
        x = re.compile(x, re.IGNORECASE)

    assert x.match(y) is not None


def test(x, y, regex_expr=False):
    """
    Compares to values based on regular expression matching or
    strict equality comparison.

    Arguments:
        x (regex|str): string or regular expression to test.
        y (str): value to match.
        regex_expr (bool): enables regex string based expression matching.

    Raises:
        AssertionError: in case of matching error.

    Returns:
        bool
    """
    return matches(x, y, regex_expr=regex_expr) if isregex(x) else equal(x, y)
