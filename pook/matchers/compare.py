import re
import functools
from ..types import isregex

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
    @functools.wraps(fn)
    def tester(expr, value):
        # If no expression value to test, pass the test
        if not expr:
            return True

        # If no value to match against, fail the test
        if expr and not value:
            return False

        if isinstance(expr, str):
            negate = str.startswith(expr, NEGATE)
            if negate:
                expr = strip_negate(expr)

        result = fn(expr, value)
        return not result if negate else result
    return tester


@comparison
def compare(expr, value):
    # Try with RegExp matching
    if isregex(expr):
        return re.match(expr, value)

    # Strict comparison equality
    return expr == value
