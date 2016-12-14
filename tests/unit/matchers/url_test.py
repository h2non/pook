# -*- coding: utf-8 -*-

import re
import pytest
from pook.request import Request
from pook.matchers.url import URLMatcher


def run_tests(cases, regex=False):
    for test in cases:
        match_url, url, matches = test
        req = Request(url=url)

        if regex:
            match_url = re.compile(match_url, re.IGNORECASE)

        if matches:
            assert URLMatcher(match_url).match(req)
        else:
            with pytest.raises(Exception):
                URLMatcher(match_url).match(req)


def test_url_matcher_urlparse():
    run_tests((
        # Valid cases
        ('http://foo.com', 'http://foo.com', True),
        ('http://foo.com:80', 'http://foo.com:80', True),
        ('http://foo.com', 'http://foo.com/foo/bar', True),
        ('http://foo.com/foo', 'http://foo.com/foo', True),
        ('http://foo.com/foo/bar', 'http://foo.com/foo/bar', True),
        ('http://foo.com/foo/bar/baz', 'http://foo.com/foo/bar/baz', True),
        ('http://foo.com/foo?x=y&z=w', 'http://foo.com/foo?x=y&z=w', True),

        # Invalid cases
        ('http://foo.com', 'http://bar.com', False),
        ('http://foo.com:80', 'http://foo.com:443', False),
        ('http://foo.com/foo', 'http://foo.com', False),
        ('http://foo.com/foo', 'http://foo.com/bar', False),
        ('http://foo.com/foo/bar', 'http://foo.com/bar/foo', False),
        ('http://foo.com/foo/bar/baz', 'http://foo.com/baz/bar/foo', False),
        ('http://foo.com/foo?x=y&z=w', 'http://foo.com/foo?x=x&y=y', False),
    ))


def test_url_matcher_regex():
    run_tests((
        # Valid cases
        ('http://foo.com', 'http://foo.com', True),
        ('http://foo.com:80', 'http://foo.com:80', True),
        ('^http://foo.com', 'http://foo.com/foo/bar', True),
        ('http://foo.com/foo', 'http://foo.com/foo', True),
        ('http://foo.com/foo/bar', 'http://foo.com/foo/bar', True),
        ('http://foo.com/foo/bar/baz', 'http://foo.com/foo/bar/baz', True),
        ('http://foo.com/foo\?x=[0-9]', 'http://foo.com/foo?x=5', True),

        # Invalid cases
        ('http://foo.com', 'http://bar.com', False),
        ('http://foo.com:80', 'http://foo.com:443', False),
        ('^http://foo.com$', 'http://foo.com/bar', False),
        ('http://foo.com/foo', 'http://foo.com/bar', False),
        ('http://foo.com/foo/bar', 'http://foo.com/bar/foo', False),
        ('http://foo.com/foo/bar/baz', 'http://foo.com/baz/bar/foo', False),
        ('http://foo.com/foo\?x=[1-3]', 'http://foo.com/foo?x=5', False),
    ), regex=True)
