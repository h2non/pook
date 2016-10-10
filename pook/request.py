from .headers import HTTPHeaderDict
from .utils import trigger_methods


class Request(object):
    """
    Request object representing the mock request expectation.
    """
    def __init__(self, method='GET', **args):
        self.method = method
        self.headers = HTTPHeaderDict()
        self.url = ''
        self.params = ''
        self.body = None
        # Call methods
        trigger_methods(self, args)
