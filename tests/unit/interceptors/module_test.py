from pook import interceptors


class CustomInterceptor(interceptors.BaseInterceptor):
    def activate(self):
        ...

    def disable(self):
        ...


def test_add_custom_interceptor():
    interceptors.add(CustomInterceptor)

    assert CustomInterceptor in interceptors.interceptors
