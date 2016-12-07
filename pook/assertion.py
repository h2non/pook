from unittest import TestCase
from .regex import isregex, strip_regex, isregex_expr


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
    return TestCase().assertEqual(x, y) or True


def matches(x, y):
    """
    Tries to match a regular expression value ``x`` against ``y``.
    Aliast``unittest.TestCase.assertEqual()``

    Arguments:
        x (regex|str): regular expression to test.
        y (str): value to match.

    Raises:
        AssertionError: in case of mismatching.

    Returns:
        bool
    """
    x = strip_regex(x) if isregex_expr(x) else x
    return TestCase().assertRegexpMatches(x, y) or True


def test(x, y):
    """
    Compares to values based on regular expression matching or
    strict equality comparison.

    Arguments:
        x (regex|str): string or regular expression to test.
        y (str): value to match.

    Raises:
        AssertionError: in case of mismatching.

    Returns:
        bool
    """
    return matches(x, y) if isregex(x) else equal(x, y)
