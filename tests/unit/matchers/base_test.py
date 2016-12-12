# -*- coding: utf-8 -*-

import pytest
from pook.matchers.base import BaseMatcher


def test_base_matcher_instance():
    matcher = BaseMatcher('foo')
    assert matcher.name is 'BaseMatcher'
    assert matcher.negate is False
    assert matcher.expectation == 'foo'
    assert matcher.to_dict() == {'BaseMatcher': 'foo'}
    assert matcher.__repr__() == 'BaseMatcher(foo)'
    assert matcher.__str__() == 'foo'


def test_base_matcher_compare():
    assert BaseMatcher.compare(None, 'foo', 'foo')

    assert BaseMatcher.compare(None, 'foo', 'foo')

    with pytest.raises(AssertionError):
        assert BaseMatcher.compare(None, 'foo', 'bar')


def test_base_matcher_exceptions():
    with pytest.raises(ValueError,
                       message='expectation argument cannot be empty'):
        BaseMatcher(None)

    assert BaseMatcher('foo').match(None) is None


def test_base_matcher_matcher():
    assert BaseMatcher.matcher(lambda x: True)(BaseMatcher)

    matcher = BaseMatcher('foo', negate=True)
    assert BaseMatcher.matcher(lambda x: False)(matcher)
