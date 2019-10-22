import pytest

from pook import Engine


@pytest.fixture
def engine():
    return Engine()


def test_engine_use_network_filter(engine):
    assert len(engine.network_filters) == 0
    engine.use_network_filter(lambda x: x)
    assert len(engine.network_filters) == 1


def test_engine_enable_network(engine):
    assert len(engine.network_filters) == 0
    engine.enable_network('http://foo', 'http://bar')
    assert len(engine.network_filters) == 2
