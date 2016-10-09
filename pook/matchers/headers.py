class HeadersMatcher(object):
    def __init__(self, headers):
        self.headers = {}

    def match(self, req):
        return True
