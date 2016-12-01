import functools
from copy import deepcopy
from abc import abstractmethod, ABCMeta
from .compare import compare
from ..types import isregex, isregex_expr, strip_regex


class BaseMatcher(object):
    """
    BaseMatcher implements the basic HTTP request matching interface.
    """

    __metaclass__ = ABCMeta

    # Negate matching if necessary
    negate = False
    # Defines if the matching supports regular expression matching
    regexp = False

    def __init__(self, expectation, negate=False):
        if not expectation:
            raise ValueError('expectation argument cannot be empty')

        self.negate = negate
        self._expectation = expectation

    @property
    def name(self):
        return type(self).__name__

    @property
    def expectation(self):
        return self._expectation if hasattr(self, '_expectation') else None

    @abstractmethod
    def match(self, request):
        """
        Match performs the value matching.
        This is an abstract method that must be implemented by child classes.

        Arguments:
            request (pook.Request): request object to match.
        """
        pass

    @expectation.setter
    def expectation(self, value):
        self._expectation = value

    def match_regexp(self, re, value):
        """
        Matches a regular expression value.

        Arguments:
            re (str|regex): regular expression value to use.
            value (str): value to match.

        Returns:
            bool
        """
        if not isregex(re):
            return False

        if isregex_expr(re):
            re = strip_regex(re)

        try:
            return bool(re.compile(re).match(value))
        except:
            return False

    def compare(self, value, expectation):
        """
        Compares two values with regular expression matching support.

        Arguments:
            value (mixed): value to compare.
            expectation (mixed): value to match.

        Returns:
            bool
        """
        if not value:
            return False

        return compare(value, expectation)

    def to_dict(self):
        """
        Returns the current matcher representation as dictionary.

        Returns:
            dict
        """
        return {self.name: deepcopy(self.expectation)}

    def __repr__(self):
        return '{}({})'.format(self.name, self.expectation)

    def __str__(self):
        return self.expectation

    @staticmethod
    def matcher(fn):
        @functools.wraps(fn)
        def wrapper(self, *args):
            result = fn(self, *args)
            return not result if self.negate else result
        return wrapper
