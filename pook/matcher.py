class MatcherEngine(list):
    """
    HTTP request matcher engine used by `pook.Mock` to test if an
    intercepted outgoing HTTP request must be mocked out or not.
    """

    def add(self, matcher):
        """
        Adds a new matcher function to the current engine.

        Arguments:
            matcher (function): matcher function to be added.
        """
        self.append(matcher)

    def flush(self):
        """
        Flushes the current matcher engine, removing all the registered
        matcher functions.
        """
        self.clear()

    def match(self, request):
        """
        Match the given HTTP request instance against the registered
        matcher functions in the current engine.

        Arguments:
            request (pook.Request): outgoing request to match.

        Returns:
            bool: `True` if all the matcher tests passes, otherwise `False`.
        """
        return all([matcher.match(request) for matcher in self])

    def __repr__(self):
        """
        Returns an human friendly readable instance data representation.

        Returns:
            str
        """
        matchers = [repr(matcher) for matcher in self]
        return 'MatcherEngine([\n  {}\n])'.format(',\n  '.join(matchers))
