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
