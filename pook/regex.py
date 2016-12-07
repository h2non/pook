import re

# Little hack to extra the regexp object type at runtime
retype = type(re.compile(''))


def isregex_expr(expr):
    """
    Returns ``True`` is the given expression value is a regular expression
    like string with prefix ``re/`` and suffix ``/``, otherwise ``False``.

    Arguments:
        expr (mixed): expression value to test.

    Returns:
        bool
    """
    if not isinstance(expr, str):
        return False

    return all([
        len(expr) > 3,
        expr.startswith('re/'),
        expr.endswith('/')
    ])


def isregex(value):
    """
    Returns ``True`` if the input argument object is a native
    regular expression object, otherwise ``False``.

    Arguments:
        value (mixed): input value to test.

    Returns:
        bool
    """
    if not value:
        return False
    return any((isregex_expr(value), isinstance(value, retype)))


def strip_regex(expr):
    """
    Strips regular expression notation syntax characters from the given
    string expression.

    Arguments:
        expr (str): regular expression expression to strip

    Returns:
        str
    """
    return expr.replace[3:-1] if isregex_expr(expr) else expr
