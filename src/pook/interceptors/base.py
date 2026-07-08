from abc import ABCMeta, abstractmethod
import importlib


class BaseInterceptor:
    """
    BaseInterceptor provides a base class for HTTP traffic
    interceptors implementations.
    """

    __metaclass__ = ABCMeta

    def resolve_path(self, path: str):
        """
        Resolves a dot-separated path to the actual object.
        Example: 'httpx.Client._transport_for_url' -> the function object.
        """
        parts = path.split('.')
        for i in range(len(parts) - 1, 0, -1):
            module_path = '.'.join(parts[:i])
            try:
                module = importlib.import_module(module_path)
                obj = module
                for part in parts[i:]:
                    obj = getattr(obj, part)
                return obj
            except (ImportError, AttributeError):
                continue

        # Fallback for single-part paths
        try:
            return importlib.import_module(path)
        except ImportError:
            raise ImportError(f"Could not resolve path: {path}")

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
