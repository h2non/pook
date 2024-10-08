from unittest import TestCase

from .regex import isregex, isregex_expr, strip_regex


def test_case():
    """
    Creates a new ``unittest.TestCase`` instance.

    Returns:
        unittest.TestCase
    """
    test = TestCase()
    test.maxDiff = None
    return test


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
    return test_case().assertEqual(x, y) or True


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

    if isinstance(getattr(x, "pattern", None), str) and hasattr(y, "decode"):
        y = y.decode("utf-8", "backslashescape")

    # Assert regular expression via unittest matchers
    return test_case().assertRegex(y, x) or True


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
