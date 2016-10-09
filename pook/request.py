from .headers import HTTPHeaderDict


class Request(object):
    """
    Request object represents.
    """
    def __init__(self, method='GET'):
        self.method = method
        self.headers = HTTPHeaderDict()
        self.url = ''
        self.params = ''
        self.body = None
