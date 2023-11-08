import pytest

import pook


@pytest.fixture
def pook_on():
    """
    Safely toggle pook on before a test, then off afterwards.

    @pook.on does not mix with pytest marks. This works around
    that limitation.
    """
    pook.on()
    yield
    pook.off()
