class MatcherEngine(list):
    """
    HTTP request matcher engine.
    """
    def add(self, matcher):
        self.append(matcher)

    def flush(self):
        self.clear()

    def match(self, req):
        for matcher in self:
            if not matcher.match(req):
                return False
        return True

    def __repr__(self):
        matchers = [matcher.__repr__() for matcher in self]
        return '[{}]'.format(', '.join(matchers))
