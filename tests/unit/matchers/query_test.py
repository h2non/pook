from urllib.request import urlopen

import pytest

import pook
from pook.exceptions import PookNoMatches


@pytest.fixture
def URL(httpbin):
    return f"{httpbin.url}/status/404"


@pytest.mark.pook(allow_pending_mocks=True)
def test_param_exists_empty_disallowed(URL):
    pook.get(URL).param_exists("x").reply(200)

    with pytest.raises(PookNoMatches):
        urlopen(f"{URL}?x")


@pytest.mark.pook
def test_param_exists_empty_allowed(URL):
    pook.get(URL).param_exists("x", allow_empty=True).reply(200)

    res = urlopen(f"{URL}?x")
    assert res.status == 200
