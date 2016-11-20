from functools import partial
from inspect import isfunction
from .types import isregex
from .interceptors import interceptors
from .exceptions import PookNoMatches, PookExpiredMock


class Engine(object):
    """
    Engine represents the mock interceptor and matcher engine responsible
    of triggering interceptors and match outgoing HTTP traffic.
    """

    def __init__(self, network=False):
        # Store the engine enable/disable status
        self.active = False
        # Enables/Disables real networking
        self.networking = network
        # Stores mocks
        self.mocks = []
        # Store engine-level global filters
        self.filters = []
        # Store engine-level global mappers
        self.mappers = []
        # Store HTTP traffic interceptors
        self.interceptors = []
        # Store unmatched requests.
        self.unmatched_reqs = []
        # Store network filters used to determine when a request
        # should be filtered or not.
        self.network_filters = []
        # Register built-in interceptors
        self.add_interceptor(*interceptors)

    def enable_network(self, *hostnames):
        """
        Enables real networking mode.
        """
        def hostname_filter(hostname, req):
            if isregex(hostname):
                return hostname.match(req.url.hostname)
            return req.url.hostname == hostname

        for hostname in hostnames:
            self.use_network_filter(partial(hostname_filter, hostname))

        self.networking = True

    def disable_network(self):
        """
        Disables real networking mode.
        """
        self.networking = False

    def use_network_filter(*fn):
        self.network_filters = self.network_filters + fn

    def add_mock(self, mock):
        """
        Adds a new mock instance to the current engine.

        Arguments:
            mock (pook.Mock): mock instance to add.
        """
        self.mocks.append(mock)

    def flush_mocks(self):
        """
        Flushes the current mocks.
        """
        self.mocks = []

    def add_interceptor(self, *interceptors):
        """
        Adds one or multiple HTTP traffic interceptors to the current
        mocking engine.

        Interceptors are typically HTTP client specific wrapper classes that
        implements the pook interceptor interface.

        Arguments:
            interceptors (pook.interceptors.BaseInterceptor)
        """
        for interceptor in interceptors:
            self.interceptors.append(interceptor(self))

    def flush_interceptors(self):
        """
        Flushes registered interceptors in the current mocking engine.

        This method is low-level. Only call it if you know what you are doing.
        """
        self.interceptors = []

    def disable_interceptor(self, name):
        for index, interceptor in enumerate(self.interceptors):
            matches = (
                type(interceptor).__name__ == name or
                getattr(interceptor, 'name') == name
            )
            if matches:
                self.interceptors.pop(index)
                return True
        return False

    def activate(self):
        """
        Activates the registered interceptors in the mocking engine.

        This means any HTTP traffic captures by those interceptors will
        trigger the HTTP mock matching engine in order to determine if a given
        HTTP transaction should be mocked out or not.
        """
        if self.active:
            return None

        self.active = True
        for interceptor in self.interceptors:
            interceptor.activate()

    def disable(self):
        """
        Disables interceptors and stops intercepting any outgoing HTTP traffic.
        """
        if not self.active:
            return None

        self.reset()
        self.active = False

    def reset(self):
        """
        Resets and flushes engine state and mocks to defaults.
        """
        if self.active:
            for interceptor in self.interceptors:
                interceptor.disable()

        # Reset attributes to defaults
        Engine.__init__(self, network=self.networking)

    def unmatched_requests(self):
        """
        Returns a ``tuple`` of unmatched requests.

        Unmatched requests will be registered only if ``networking`` mode
        has been enabled.

        Returns:
            tuple: unmatched intercepted requests.
        """
        return (mock for mock in self.unmatched_reqs)

    def unmatched(self):
        """
        Returns the total number of unmatched requests intercepted by pook.

        Unmatched requests will be registered only if ``networking`` mode
        has been enabled.

        Returns:
            int: total number of unmatched requests.
        """
        return len(self.unmatched_requests())

    def isunmatched(self):
        """
        Returns ``True`` if there are unmatched requests. Otherwise ``False``.

        Unmatched requests will be registered only if ``networking`` mode
        has been enabled.

        Returns:
            bool
        """
        return len(self.unmatched()) > 0

    def pending(self):
        """
        Returns the number of pending mocks to be matched.

        Returns:
            int: number of pending mocks.
        """
        return len(self.pending_mocks())

    def pending_mocks(self):
        """
        Returns a ``tuple`` of pending mocks to be matched.

        Returns:
            tuple: pending mock instances.
        """
        return (mock for mock in self.mocks if mock.isdone())

    def pending(self):
        """
        Returns the number of pending mocks to be matched.

        Returns:
            int: number of pending mocks.
        """
        return len(self.pending_mocks())

    def ispending(self):
        """
        Returns the ``True`` if the engine has pending mocks to be matched.
        Otherwise ``False``.

        Returns:
            bool
        """
        return len(self.pending_mocks())

    def isactive(self):
        """
        Returns the current engine enabled/disabled status.

        Returns:
            bool: ``True`` if the engine is active. Otherwise ``False``.
        """
        return self.active

    def isdone(self):
        """
        Returns True if all the registered mocks has been triggered.

        Returns:
            bool: True is all the registered mocks are gone, otherwise False.
        """
        return all(mock.isdone() for mock in self.mocks)

    def _append(self, target, *fns):
        (target.append(fn) for fn in fns if isfunction(fn))

    def filter(self, *filters):
        """
        Append engine-level HTTP request filter functions.

        Arguments:
            filters*: variadic filter functions to be added.
        """
        self._append(self.filters, *filters)

    def map(self, *mappers):
        """
        Append engine-level HTTP request mapper functions.

        Arguments:
            filters*: variadic mapper functions to be added.
        """
        self._append(self.mappers, *mappers)

    def should_use_network(self, request):
        return (self.networking and
                all((fn(request) for fn in self.network_filters)))

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
        # Trigger engine-level request filters
        for test in self.filters:
            if not test(request, self):
                return False

        # Trigger engine-level request mappers
        for mapper in self.mappers:
            request = mapper(request, self)
            if not request:
                raise ValueError('map function must return a request object')

        # Try to match the request against registered mock definitions
        for mock in self.mocks:
            try:
                # Return the first matched HTTP request mock
                if mock.match(request.copy()):
                    return mock
            except PookExpiredMock:
                # Remove the mock if already expired
                self.mocks.remove(mock)

        # Validate that we have a mock
        if not self.should_use_network(request):
            raise PookNoMatches('Cannot match any mock for request:', request)

        # Register unmatched request
        self.unmatched_reqs.append(request)
