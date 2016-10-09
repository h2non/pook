class AIOHTTPInterceptor(object):
    """
    aiohttp HTTP client traffic interceptor.
    """
    def __init__(self, engine):
        self.patchers = []
        self.engine = engine

    def activate(self):
        """
        Activates the traffic interceptor.
        This method must be implemented by any interceptor.
        """
        raise NotImplemented('not implemented yet')

    def disable(self):
        """
        Disables the traffic interceptor.
        This method must be implemented by any interceptor.
        """
        raise NotImplemented('not implemented yet')
