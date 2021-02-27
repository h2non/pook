from abc import abstractmethod, ABCMeta
import inspect
# Support Python 2/3
try:
    import mock
except Exception:
    from unittest import mock


class BaseInterceptor(object):
    """
    BaseInterceptor provides a base class for HTTP traffic
    interceptors implementations.
    """

    __metaclass__ = ABCMeta
    _static_patchers = {}

    def __init__(self, engine):
        self.patchers = []
        self.engine = engine

    @property
    def name(self):
        """
        Exposes the interceptor class name.
        """
        return type(self).__name__

    @staticmethod
    def _get_real_import_path(path):
        # inspired (a.k.a copy pasted)
        # by unittest.mock module and functions:
        # _get_target, _importer, _dot_lookup

        def _dot_lookup(thing, comp, import_path):
            try:
                return getattr(thing, comp)
            except AttributeError:
                __import__(import_path)
                return getattr(thing, comp)

        target, attribute = path.rsplit('.', 1)

        components = target.split('.')
        import_path = components.pop(0)
        thing = __import__(import_path)

        for comp in components:
            import_path += ".%s" % comp
            thing = _dot_lookup(thing, comp, import_path)
        thing_module_path = inspect.getmodule(thing).__name__
        thing_module_path += "." + ".".join(path.rsplit(".", 2)[1:])

        return thing_module_path

    def _patch(self, path):
        def _decorator(fn):
            def wrapped(*args, **kwargs):
                return fn(request, path, *args, **kwargs)
            return wrapped

        try:
            real_module_path = self._get_real_import_path(path)
            if real_module_path in BaseInterceptor._static_patchers:
                # TODO: add warning here
                return
            # Create a new patcher for `request` function
            # used as entry point for all the HTTP communications
            patcher = mock.patch(path, _decorator(self._patch_handler))
            patcher._real_module_path = real_module_path
            # Retrieve original patched function that we might need for real
            # networking
            request = patcher.get_original()[0]
            # Start patching function calls
            patcher.start()
        except AssertionError:
            raise
        except Exception:
            # Exceptions may accur due to missing package
            # Ignore all the exceptions for now
            pass
        else:
            self.patchers.append(patcher)
            BaseInterceptor._static_patchers[real_module_path] = patcher

    def _patch_handler(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def activate(self):
        """
        Activates the traffic interceptor.
        This method must be implemented by any interceptor.
        """
        [self._patch(patch) for patch in self.PATCHES]

    def disable(self):
        """
        Disables the traffic interceptor.
        This method must be implemented by any interceptor.
        """
        for patch in reversed(self.patchers):
            patch.stop()
            if patch._real_module_path in BaseInterceptor._static_patchers:
                del BaseInterceptor._static_patchers[patch._real_module_path]


