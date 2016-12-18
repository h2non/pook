from functools import partial
from inspect import isfunction
from .mock import Mock
from .regex import isregex
from .mock_engine import MockEngine
from .exceptions import PookNoMatches, PookExpiredMock


class Engine(object):
    """
    Engine represents the mock interceptor and matcher engine responsible
    of triggering interceptors and match outgoing HTTP traffic.

    Arguments:
        network (bool, optional): enables/disables real networking mode.

    Attributes:
        debug (bool): enables/disables debug mode.
        active (bool): stores the current engine activation status.
        networking (bool): stores the current engine networking mode status.
        mocks (list[pook.Mock]): stores engine mocks.
        filters (list[function]): stores engine-level mock filter functions.
        mappers (list[function]): stores engine-level mock mapper functions.
        interceptors (list[pook.BaseInterceptor]): stores engine-level HTTP
            traffic interceptors.
        unmatched_reqs (list[pook.Request]): stores engine-level unmatched
            outgoing HTTP requests.
        network_filters (list[function]): stores engine-level real
            networking mode filters.
    """

    def __init__(self, network=False):
        # Enables/Disables debug mode.
        self.debug = True
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
        # Store unmatched requests.
        self.unmatched_reqs = []
        # Store network filters used to determine when a request
        # should be filtered or not.
        self.network_filters = []
        # Built-in mock engine to be used
        self.mock_engine = MockEngine(self)

    def set_mock_engine(self, engine):
        """
        Sets a custom mock engine, replacing the built-in one.

        This is particularly useful if you want to replace the built-in
        HTTP traffic mock interceptor engine with your custom one.

        For mock engine implementation details, see `pook.MockEngine`.

        Arguments:
            engine (pook.MockEngine): custom mock engine to use.
        """
        if not engine:
            raise TypeError('engine must be a valid object')

        # Instantiate mock engine
        mock_engine = engine(self)

        # Validate minimum viable interface
        methods = ('activate', 'disable')
        if all([hasattr(mock_engine, method) for method in methods]):
            raise NotImplementedError('engine must implementent the '
                                      'required methods')

        # Disable previous mock engine, if needed
        if self.active:
            self.disable()

        # Use the custom mock engine
        self.mock_engine = mock_engine

    def enable_network(self, *hostnames):
        """
        Enables real networking mode, optionally passing one or multiple
        hostnames that would be used as filter.

        If at least one hostname matches with the outgoing traffic, the
        request will be executed via the real network.

        Arguments:
            *hostnames: optional list of host names to enable real network
                against them. hostname value can be a regular expression.
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

    def use_network_filter(self, *fn):
        """
        Adds network filters to determine if certain outgoing unmatched
        HTTP traffic can stablish real network connections.

        Arguments:
            *fn (function): variadic function filter arguments to be used.
        """
        self.network_filters = self.network_filters + fn

    def flush_network_filters(self):
        """
        Flushes registered real networking filters in the current
        mock engine.
        """
        self.network_filters = []

    def mock(self, url=None, **kw):
        """
        Creates and registers a new HTTP mock in the current engine.

        Arguments:
            url (str): request URL to mock.
            **kw (mixed): variadic keyword arguments for ``Mock`` constructor.

        Returns:
            pook.Mock: new mock instance.
        """
        # Create the new HTTP mock expectation
        mock = Mock(url=url, **kw)
        # Expose current engine instance via mock
        mock._engine = self
        # Register the mock in the current engine
        self.add_mock(mock)
        # Activate mock engine transparently, if it was not active yet
        self.activate()
        # Return it for consumer satisfaction
        return mock

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

    def _engine_proxy(self, method, *args, **kw):
        engine_method = getattr(self.mock_engine, method, None)

        if not engine_method:
            raise NotImplementedError('current mock engine does not implements'
                                      ' required "{}" method'.format(method))

        return engine_method(self.mock_engine, *args, **kw)

    def add_interceptor(self, *interceptors):
        """
        Adds one or multiple HTTP traffic interceptors to the current
        mocking engine.

        Interceptors are typically HTTP client specific wrapper classes that
        implements the pook interceptor interface.

        Note: this method is may not be implemented if using a custom mock
        engine.

        Arguments:
            interceptors (pook.interceptors.BaseInterceptor)
        """
        self._engine_proxy('add_interceptor', *interceptors)

    def flush_interceptors(self):
        """
        Flushes registered interceptors in the current mocking engine.

        This method is low-level. Only call it if you know what you are doing.

        Note: this method is may not be implemented if using a custom mock
        engine.
        """
        self._engine_proxy('flush_interceptors')

    def remove_interceptor(self, name):
        """
        Removes a specific interceptor by name.

        Note: this method is may not be implemented if using a custom mock
        engine.

        Arguments:
            name (str): interceptor name to disable.

        Returns:
            bool: `True` if the interceptor was disabled, otherwise `False`.
        """
        return self._engine_proxy('remove_interceptor', name)

    def activate(self):
        """
        Activates the registered interceptors in the mocking engine.

        This means any HTTP traffic captures by those interceptors will
        trigger the HTTP mock matching engine in order to determine if a given
        HTTP transaction should be mocked out or not.
        """
        if self.active:
            return None

        # Activate mock engine
        self.mock_engine.activate()
        # Enable engine state
        self.active = True

    def disable(self):
        """
        Disables interceptors and stops intercepting any outgoing HTTP traffic.
        """
        if not self.active:
            return None

        # Disable current mock engine
        self.mock_engine.disable()
        # Disable engine state
        self.active = False

    def reset(self):
        """
        Resets and flushes engine state and mocks to defaults.
        """
        # Reset engine
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
        return [mock for mock in self.mocks if not mock.isdone()]

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
        """
        Verifies if real networking mode should be used for the given
        request, passing it to the registered network filters.

        Arguments:
            request (pook.Request): outgoing HTTP request to test.

        Returns:
            bool
        """
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

        # Store list of mock matching errors for further debugging
        match_errors = []

        # Try to match the request against registered mock definitions
        for mock in self.mocks[:]:
            try:
                # Return the first matched HTTP request mock
                matches, errors = mock.match(request.copy())
                if len(errors):
                    match_errors += errors
                if matches:
                    return mock
            except PookExpiredMock:
                # Remove the mock if already expired
                self.mocks.remove(mock)

        # Validate that we have a mock
        if not self.should_use_network(request):
            msg = 'Cannot match mock for request:\n{}'.format(request)

            # Compose unmatch error details, if debug mode is enabled
            if self.debug:
                err = '\n\n'.join([str(err) for err in match_errors])
                if err:
                    msg += '\n\n=> Detailed matching errors:\n{}\n'.format(err)

            # Raise no matches exception
            raise PookNoMatches(msg)

        # Register unmatched request
        self.unmatched_reqs.append(request)
