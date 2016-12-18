# -*- coding: utf-8 -*-

import pytest
from pook import MockEngine, Engine
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

    engine.remove_interceptor('Interceptor')
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
