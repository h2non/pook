from .interceptors import interceptors


class MockEngine(object):
    """
    MockEngine implements the built-in `pook` mock engine based on HTTP
    interceptors strategy.

    Mock engines must implementent the following methods:

    - `engine.__init__(self, engine)`
    - `engine.activate(self)`
    - `engine.disable(self)`

    Mock engines can optionally implement the follow methods:

    - `engine.add_interceptors(self, *interceptors)`
    - `engine.flush_interceptors(self)`
    - `engine.disable_interceptor(self, name) -> bool`

    Arguments:
        engine (pook.Engine): injected pook engine to be used.

    Attributes:
        engine (pook.Engine): stores pook engine to be used.
        interceptors (list[pook.BaseInterceptor]): stores engine-level HTTP
            traffic interceptors.
    """

    def __init__(self, engine):
        # Store pook engine
        self.engine = engine
        # Store HTTP client interceptors
        self.interceptors = []
        # Self-register built-in interceptors
        self.add_interceptor(*interceptors)

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
            self.interceptors.append(interceptor(self.engine))

    def flush_interceptors(self):
        """
        Flushes registered interceptors in the current mocking engine.

        This method is low-level. Only call it if you know what you are doing.
        """
        self.interceptors = []

    def remove_interceptor(self, name):
        """
        Removes a specific interceptor by name.

        Arguments:
            name (str): interceptor name to disable.

        Returns:
            bool: `True` if the interceptor was disabled, otherwise `False`.
        """
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
        [interceptor.activate() for interceptor in self.interceptors]

    def disable(self):
        """
        Disables interceptors and stops intercepting any outgoing HTTP traffic.
        """
        # Restore HTTP interceptors
        for interceptor in self.interceptors:
            try:
                interceptor.disable()
            except RuntimeError:
                pass  # explicitely ignore runtime patch errors
