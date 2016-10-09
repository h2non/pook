from .exceptions import PockNoMatches, PockExpiredMock
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

    def on_request(self, request):
        for mock in self.mocks:
            try:
                # If mock matches, return the response object
                if mock.match(request):
                    return mock.response
            except PockExpiredMock:
                self.mocks.remove(mock)

        if not self.networking:
            raise PockNoMatches('Cannot match any mock for request:', request)
