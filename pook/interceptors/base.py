from abc import abstractmethod, ABCMeta


class BaseInterceptor(metaclass=ABCMeta):
    """
    BaseInterceptor provides a base class for HTTP traffic
    interceptors implementations.
    """

    def __init__(self, engine):
        self.patchers = []
        self.engine = engine

    @property
    def name(self):
        """
        Exposes the interceptor class name.
        """
        return type(self).__name__

    @abstractmethod
    def activate(self):
        """
        Activates the traffic interceptor.
        This method must be implemented by any interceptor.
        """
        pass

    @abstractmethod
    def disable(self):
        """
        Disables the traffic interceptor.
        This method must be implemented by any interceptor.
        """
        pass
