from urllib.request import urlopen

import pytest

import pook
from pook.exceptions import PookNoMatches


@pytest.mark.pook(allow_pending_mocks=True)
def test_param_exists_empty_disallowed(url_404):
    pook.get(url_404).param_exists("x").reply(200)

    with pytest.raises(PookNoMatches):
        urlopen(f"{url_404}?x")


@pytest.mark.pook
def test_param_exists_empty_allowed(url_404):
    pook.get(url_404).param_exists("x", allow_empty=True).reply(200)

    res = urlopen(f"{url_404}?x")
    assert res.status == 200
