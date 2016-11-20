class MatcherEngine(list):
    """
    HTTP request matcher engine.
    """

    def add(self, matcher):
        self.append(matcher)

    def flush(self):
        self.clear()

    def match(self, req):
        return all([matcher.match(req) for matcher in self])

    def __repr__(self):
        matchers = [repr(matcher) for matcher in self]
        return 'MatcherEngine([\n  {}\n])'.format(',\n  '.join(matchers))
