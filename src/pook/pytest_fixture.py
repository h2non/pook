import pytest

import pook as pook_mod


@pytest.fixture
def pook():
    """Pytest fixture for HTTP traffic mocking and testing"""
    pook_mod.on()
    yield pook_mod
    pook_mod.off()
