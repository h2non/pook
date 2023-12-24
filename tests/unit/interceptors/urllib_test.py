import pook
from urllib.request import urlopen
import pytest


@pytest.mark.pook
def test_urllib_ssl():
    pook.get("https://example.com").reply(200).body("Hello from pook")
    res = urlopen("https://example.com")

    assert res.read() == "Hello from pook"


@pytest.mark.pook
def test_urllib_clear():
    pook.get("http://example.com").reply(200).body("Hello from pook")
    res = urlopen("http://example.com")

    assert res.read() == "Hello from pook"
