from .base import BaseMatcher
from .url import URLMatcher
from .body import BodyMatcher
from .query import QueryMatcher
from .method import MethodMatcher
from .headers import HeadersMatcher
from .path import PathMatcher
from .xml import XMLMatcher
from .json import JSONMatcher
from .json_schema import JSONSchemaMatcher

# Explicit symbols to export
__all__ = (
    'init',
    'add',
    'get',
    'matchers',
    'BaseMatcher',
    'MethodMatcher',
    'URLMatcher',
    'HeadersMatcher',
    'QueryMatcher',
    'PathMatcher',
    'BodyMatcher',
    'XMLMatcher',
    'JSONMatcher',
    'JSONSchemaMatcher',
    'QueryMatcher',
)

# List of built-in matchers
# This is intended to be mutable.
matchers = [
    MethodMatcher,
    URLMatcher,
    HeadersMatcher,
    QueryMatcher,
    PathMatcher,
    BodyMatcher,
    XMLMatcher,
    JSONMatcher,
    JSONSchemaMatcher,
    QueryMatcher,
]


def add(*matcher):
    """
    Registers one or multiple matchers to be used by default from
    mocking engine.

    Arguments:
        *matcher (list[pook.BaseMatcher]): variadic matchers to add.
    """
    [matchers.append(m) for m in matcher]


def get(name):
    """
    Returns a matcher instance by class or alias name.

    Arguments:
        name (str): matcher class name or alias.

    Returns:
        matcher: found matcher instance, otherwise ``None``.
    """
    for matcher in matchers:
        if matcher.__name__ == name or getattr(matcher, 'name', None) == name:
            return matcher


def init(name, *args):
    """
    Initializes a matcher instance passing variadic arguments to
    its constructor. Acts as a delegator proxy.

    Arguments:
        name (str): matcher class name or alias to execute.
        *args (mixed): variadic argument

    Returns:
        matcher: matcher instance.

    Raises:
        ValueError: if matcher was not found.
    """
    matcher = get(name)
    if not matcher:
        raise ValueError('Cannot find matcher: {}'.format(name))
    return matcher(*args)
