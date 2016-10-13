class HeadersMatcher(object):
    def __init__(self, headers):
        if not isinstance(headers, dict):
            raise TypeError('headers must be a dictionary')
        self.headers = headers

    def match(self, req):
        return True
