import re
from urllib.request import urlopen

import pytest

import pook
from pook.exceptions import PookNoMatches
from pook.matchers.query import QueryMatcher
from pook.request import Request


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


@pytest.mark.parametrize(
    ("expectation", "query"),
    [
        ("x=a&x=b", "x=a&x=b"),
        ({"x": ["a", "b"]}, "x=a&x=b"),
        ({"x": ["a", "b"]}, "x=a&other=1&x=b"),
        ({"x": ["a", "a"]}, "x=a&x=a"),
        ({"x": [re.compile("^a$"), re.compile("^b$")]}, "x=a&x=b"),
        ({"x": ["!!b", "!!a"]}, "x=a&x=b"),
        ({"x": "a"}, "x=a&x=a"),
        ({"x": re.compile("^[ab]$")}, "x=a&x=b"),
    ],
)
def test_repeated_query_values_match(expectation, query):
    request = Request(url=f"http://example.com/?{query}")

    assert QueryMatcher(expectation).match(request)


@pytest.mark.parametrize(
    ("expectation", "query"),
    [
        ({"x": ["a", "b"]}, "x=b&x=a"),
        ({"x": ["a", "b"]}, "x=a"),
        ({"x": ["a", "b"]}, "x=a&x=b&x=c"),
        ({"x": ["a", "b"]}, "x=a&x=c"),
        ({"x": ["a", "a"]}, "x=a"),
        ({"x": ["a"]}, "x=a&x=a"),
        ({"x": [re.compile("^a$"), re.compile("^b$")]}, "x=a&x=c"),
        ({"x": "a"}, "x=a&x=b"),
    ],
)
def test_repeated_query_values_mismatch(expectation, query):
    request = Request(url=f"http://example.com/?{query}")

    with pytest.raises(AssertionError):
        QueryMatcher(expectation).match(request)


def test_repeated_query_values_missing_key():
    request = Request(url="http://example.com/?other=a")

    assert not QueryMatcher({"x": ["a", "b"]}).match(request)
