import re
import functools
from ..types import isregex, isregex_expr, strip_regex

# Negate is used a reserved token identifier to negate matching
NEGATE = '!!'


def compile(expr):
    try:
        return re.compile(expr, re.IGNORECASE)
    except:
        pass


def match(expr, value):
    regex = compile(expr)
    if not regex:
        return False
    return regex.match(value) is not None


def strip_negate(value):
    return value[len(NEGATE):].lstrip()


def comparison(fn):
    """
    Decorator function for comparison.

    Arguments:
        fn (function): target function to decorate.

    Returns:
        function
    """
    @functools.wraps(fn)
    def tester(expr, value):
        # If no expression value to test, pass the test
        if not expr:
            return True

        # If no value to match against, fail the test
        if expr and not value:
            return False

        # If string instance
        if isinstance(expr, str):
            negate = str.startswith(expr, NEGATE)
            if negate:
                expr = strip_negate(expr)

        result = fn(expr, value)
        return not result if negate else result
    return tester


@comparison
def compare(expr, value):
    """
    Compares an string or regular expression againast a given value.

    Arguments:
        expr (str|regex): string or regular expression value to compare.
        value (str): value to compare against to.

    Returns:
        bool
    """
    # Try with RegExp matching
    if isregex(expr):
        if isregex_expr(expr):
            expr = strip_regex(expr)
        return re.match(expr, value)

    # Strict comparison equality
    return expr == value
