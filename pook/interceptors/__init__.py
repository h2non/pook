from .urllib3 import Urllib3Interceptor

# Store built-in interceptors.
# Note: order is intentional.
store = [
    # UrllibInterceptor,
    Urllib3Interceptor,
    # AIOHTTPInterceptor,
]


def add(interceptor):
    """
    Registers a new HTTP client interceptor.
    """
    store.append(interceptor)
