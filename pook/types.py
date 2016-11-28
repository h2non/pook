from inspect import isfunction


def isregex_string(expr):
    """
    Returns ``True`` is the given expression value is a regular expression
    like string with prefix ``re/`` and suffix ``/``, otherwise ``False``.

    Arguments:
        expt (mixed): expression value to test.

    Returns:
        bool
    """
    if not isinstance(expr, str):
        return False
    return expr.startswith('re/') and expr.endswith('/')


def has_regex_methods(value):
    """
    Returns ``True`` if the input object implements the regular
    expressesion interface methods, otherwise ``False``.

    Arguments:
        value (mixed): input value to test.

    Returns:
        bool
    """
    methods = (getattr(value, 'match', None),
               getattr(value, 'search', None))
    return all(isfunction(x) for x in methods)


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
    return any([isregex_string(value), has_regex_methods(value)])
