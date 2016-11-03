from .exceptions import PookNoMatches, PookExpiredMock
from .interceptors import store


class Engine(object):
    """
    Engine represents the mock interceptor
    and matcher engine responsible of triggering
    interceptors and match outgoing HTTP traffic.
    """
    def __init__(self):
        # Enable real networking
        self.networking = False
        # Stores mocks
        self.mocks = []
        # Store interceptors
        self.interceptors = []
        # Register built-in interceptors
        self.add_interceptor(*store)

    def add_mock(self, mock):
        self.mocks.append(mock)

    def flush_mocks(self):
        self.mocks = []

    def add_interceptor(self, *interceptors):
        for interceptor in interceptors:
            self.interceptors.append(interceptor(self))

    def flush_interceptors(self):
        self.interceptors = []

    def activate(self):
        for interceptor in self.interceptors:
            interceptor.activate()

    def disable(self):
        for interceptor in self.interceptors:
            interceptor.disable()

    def match(self, request):
        """
        Matches a given Request instance contract against the registered mocks.

        If a mock passes all the matchers, its response will be returned.

        Arguments:
            request (pook.Request): Request contract to match.

        Raises:
            pook.PookNoMatches: if networking is disabled and no mock matches
                with the given request contract.

        Returns:
            pook.Response: the mock response to be used by the interceptor.
        """
        for mock in self.mocks:
            try:
                # If mock matches, return the response object
                if mock.match(request):
                    return mock.response
            except PookExpiredMock:
                self.mocks.remove(mock)

        if not self.networking:
            raise PookNoMatches('Cannot match any mock for request:', request)
