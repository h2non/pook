import functools
from copy import deepcopy
from abc import abstractmethod, ABCMeta


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
        This method must be implemented by child classes.
        """
        pass

    @expectation.setter
    def expectation(self, value):
        self._expectation = value

    def match_regexp(self, re, value):
        try:
            return bool(re.compile(re).match(value))
        except re.error:
            return False

    def to_dict(self):
        return {self.name: deepcopy(self.expectation)}

    def __repr__(self):
        return '{}({})'.format(self.name, self.expectation)

    @staticmethod
    def matcher(fn):
        @functools.wraps(fn)
        def wrapper(self, *args):
            result = fn(self, *args)
            return not result if self.negate else result
        return wrapper
