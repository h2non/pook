class QueryMatcher(object):
    def __init__(self, params):
        self.params = params

    def match(self, req):
        return True
