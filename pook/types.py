from inspect import isfunction


def isregex_string(expr):
    if not isinstance(expr, str):
        return False
    return expr.startswith('re/') and expr.endswith('/')


def has_regex_methods(value):
    methods = (getattr(value, 'match', None),
               getattr(value, 'search', None))
    return all(isfunction(x) for x in methods)


def isregex(value):
    if not value:
        return False
    return any((isregex_string(value), has_regex_methods(value)))
