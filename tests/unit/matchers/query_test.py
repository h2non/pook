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


@pytest.mark.parametrize("expectation", [{"cursor": ""}, "cursor="])
@pytest.mark.parametrize(
    "query, matches",
    [
        ("?cursor=", True),
        ("?cursor", True),
        ("", False),
        ("?other=", False),
        ("?cursor=next", False),
    ],
)
def test_blank_query_value(expectation, query, matches):
    request_mock = pook.Mock()
    request_mock.url("http://example.test/")
    request_mock.add_matcher(QueryMatcher(expectation))
    request = Request(url="http://example.test/" + query)
    assert request_mock.matchers.match(request)[0] is matches


@pytest.mark.pook
@pytest.mark.parametrize("query", ["?cursor", "?cursor="])
def test_blank_query_value_request(url_404, query):
    pook.get(url_404).params({"cursor": ""}).reply(200)
    assert urlopen(url_404 + query).status == 200
