from abc import ABCMeta, abstractmethod


class BaseInterceptor:
    """
    BaseInterceptor provides a base class for HTTP traffic
    interceptors implementations.
    """

    __metaclass__ = ABCMeta

    def __init__(self, engine):
        self.patchers = []
        self.engine = engine

    @property
    def name(self) -> str:
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
        raise NotImplementedError("Sub-classes must implement `activate`")

    @abstractmethod
    def disable(self):
        """
        Disables the traffic interceptor.
        This method must be implemented by any interceptor.
        """
        raise NotImplementedError("Sub-classes must implement `disable`")
