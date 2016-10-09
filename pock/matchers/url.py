class URLMatcher(object):
    def __init__(self, expression):
        self.expression = expression

    def match(self, req):
        return True
