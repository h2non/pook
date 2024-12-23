from urllib.request import Request, urlopen

import pytest

import pook
from pook import Engine, MockEngine
from pook.interceptors import BaseInterceptor


class Interceptor(BaseInterceptor):
    def activate(self):
        self.active = True

    def disable(self):
        self.active = False


@pytest.fixture
def engine():
    return MockEngine(Engine())


def test_mock_engine_instance(engine):
    assert isinstance(engine.engine, Engine)
    assert isinstance(engine.interceptors, list)
    assert len(engine.interceptors) >= 2


def test_mock_engine_flush(engine):
    assert len(engine.interceptors) >= 2
    engine.flush_interceptors()
    assert len(engine.interceptors) == 0


def test_mock_engine_interceptors(engine):
    engine.flush_interceptors()
    engine.add_interceptor(Interceptor)
    assert len(engine.interceptors) == 1
    assert isinstance(engine.interceptors[0], Interceptor)

    engine.remove_interceptor("Interceptor")
    assert len(engine.interceptors) == 0


def test_mock_engine_status(engine):
    engine.flush_interceptors()
    engine.add_interceptor(Interceptor)
    assert len(engine.interceptors) == 1

    interceptor = engine.interceptors[0]
    engine.activate()
    assert interceptor.active

    engine.disable()
    assert not interceptor.active


@pytest.mark.xfail(
    reason="Pook cannot disambiguate the two mocks. Ideally it would try to find the most specific mock that matches, but that's not possible yet."
)
@pytest.mark.pook(allow_pending_mocks=True)
def test_mock_specificity(url_404):
    pook.get(url_404).header_present("authorization").reply(201)
    pook.get(url_404).headers({"Authorization": "Bearer pook"}).reply(200)

    res_with_headers = urlopen(
        Request(url_404, headers={"Authorization": "Bearer pook"})
    )

    assert res_with_headers.status == 200
