import pook
from urllib.request import urlopen


def test_urllib_ssl(pook_on):
    pook.get("https://example.com").reply(200).body("Hello from pook")
    res = urlopen("https://example.com")

    assert res.read() == "Hello from pook"


def test_urllib_clear(pook_on):
    pook.get("http://example.com").reply(200).body("Hello from pook")
    res = urlopen("http://example.com")

    assert res.read() == "Hello from pook"
