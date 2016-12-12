# -*- coding: utf-8 -*-

import pytest
from pook.matchers.base import BaseMatcher


class _BaseMatcher(BaseMatcher):

    def match(self, x):
        pass


def test_base_matcher_instance():
    matcher = _BaseMatcher('foo')
    assert matcher.name == '_BaseMatcher'
    assert matcher.negate is False
    assert matcher.expectation == 'foo'
    assert matcher.to_dict() == {'_BaseMatcher': 'foo'}
    assert matcher.__repr__() == '_BaseMatcher(foo)'
    assert matcher.__str__() == 'foo'


def test_base_matcher_compare():
    assert _BaseMatcher('foo').compare('foo', 'foo')

    assert _BaseMatcher('foo').compare('foo', 'foo')

    with pytest.raises(AssertionError):
        assert _BaseMatcher('foo').compare('foo', 'bar')


def test_base_matcher_exceptions():
    assert _BaseMatcher('foo').match(None) is None

    with pytest.raises(ValueError,
                       message='expectation argument cannot be empty'):
        _BaseMatcher(None)


def test_base_matcher_matcher():
    assert BaseMatcher.matcher(lambda x: True)(BaseMatcher)

    matcher = _BaseMatcher('foo', negate=True)
    assert BaseMatcher.matcher(lambda x: False)(matcher)
