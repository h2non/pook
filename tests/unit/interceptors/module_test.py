from pook import interceptors


class CustomInterceptor(interceptors.BaseInterceptor):
    pass


def test_add_custom_interceptor():
    interceptors.add(CustomInterceptor)

    assert CustomInterceptor in interceptors.interceptors
