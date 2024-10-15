import asyncio
import pytest

from pook import api


@pytest.fixture
def engine():
    return api.engine()


def test_engine(engine):
    assert engine == api._engine


def test_activate(engine):
    assert engine.active is False
    api.activate()
    assert engine.active is True
    api.disable()
    assert engine.active is False


def test_on(engine):
    assert engine.active is False
    api.on()
    assert engine.active is True
    api.off()
    assert engine.active is False


def test_use(engine):
    assert engine.active is False
    with api.use() as engine:
        assert engine.active is True
        assert engine.active is True
    assert engine.active is False


def test_mock_contructors(engine):
    assert engine.active is False
    assert engine.isdone() is True

    api.mock("foo.com")
    assert engine.isdone() is False
    assert len(engine.mocks) == 1
    api.off()

    assert len(engine.mocks) == 0
    assert engine.active is False


def test_activate_as_decorator(engine):

    @api.activate
    def test_activate():
        api.get("foo.com")
        assert engine.active is True
        assert engine.isdone() is False

    test_activate()
    assert engine.active is False
    assert engine.isdone() is True


async def test_activate_as_decorator_for_async(engine):

    @api.activate
    async def test_activate():
        await asyncio.sleep(0)
        api.get("foo.com")
        assert engine.active is True
        assert engine.isdone() is False

    await test_activate()
    assert engine.active is False
    assert engine.isdone() is True
