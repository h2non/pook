from wsgiref.simple_server import make_server

import falcon

import threading

import pytest


class HttpbinLikeResource:
    def on_get_status(self, req: falcon.Request, resp: falcon.Response, status: int):
        resp.set_header("x-pook-httpbinlike", "")
        resp.status = status

    on_post_status = on_get_status


class HttpbinLike:
    def __init__(self, schema: str, host: str):
        self.schema = schema
        self.host = host
        self.url = schema + host

    def __add__(self, value):
        return self.url + value


@pytest.fixture(scope="session")
def local_responder():
    app = falcon.App()
    resource = HttpbinLikeResource()
    app.add_route("/status/{status:int}", resource, suffix="status")

    with make_server("127.0.0.1", 8080, app) as httpd:

        def run():
            httpd.serve_forever()

        thread = threading.Thread(target=run)
        thread.start()
        yield HttpbinLike("http://", "127.0.0.1:8080")
        httpd.shutdown()
        thread.join(timeout=5)


@pytest.fixture
def url_404(local_responder):
    """404 httpbin URL.

    Useful in tests if pook is configured to reply 200, and the status is checked.
    If pook does not match the request (and if that was the intended behaviour)
    then the 404 status code makes that obvious!"""
    return local_responder + "/status/404"


@pytest.fixture
def url_401(local_responder):
    return local_responder + "/status/401"


@pytest.fixture
def url_500(local_responder):
    return local_responder + "/status/500"
