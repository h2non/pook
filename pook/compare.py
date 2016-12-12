import re
from .assertion import test

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


def compare(expr, value, regex_expr=False):
    """
    Compares an string or regular expression againast a given value.

    Arguments:
        expr (str|regex): string or regular expression value to compare.
        value (str): value to compare against to.
        regex_expr (bool, optional): enables string based regex matching.

    Raises:
        AssertionError: in case of assertion error.

    Returns:
        bool
    """
    # Strict equality comparison
    if expr == value:
        return True

    # Infer negate expression to match, if needed
    negate = False
    if isinstance(expr, str):
        negate = expr.startswith(NEGATE)
        expr = strip_negate(expr) if negate else expr

    try:
        # RegExp or strict equality comparison
        test(expr, value, regex_expr=regex_expr)
    except Exception as err:
        if negate:
            return True
        else:
            raise err

    return True
