import pytest
from urllib.request import urlopen

import pook
from pook.exceptions import PookNoMatches


@pytest.mark.pook(allow_pending_mocks=True)
def test_param_exists_empty_disallowed():
    pook.get("https://httpbin.org/404").param_exists("x").reply(200)

    with pytest.raises(PookNoMatches):
        urlopen("https://httpbin.org/404?x")


@pytest.mark.pook
def test_param_exists_empty_allowed():
    pook.get("https://httpbin.org/404").param_exists("x", allow_empty=True).reply(200)

    res = urlopen("https://httpbin.org/404?x")
    assert res.status == 200
