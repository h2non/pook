import pytest

import pook as pook_mod


@pytest.fixture
def pook():
    """Pytest fixture for HTTP traffic mocking and testing"""
    with pook_mod.use():
        yield pook_mod
