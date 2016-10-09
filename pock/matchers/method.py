class MethodMatcher(object):
    def __init__(self, method):
        self.method = method

    def match(self, req):
        return self.method == '*' or req.method == self.method
