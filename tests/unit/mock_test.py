# -*- coding: utf-8 -*-

import pytest
from pook.mock import Mock


@pytest.fixture
def mock():
    return Mock()


def matcher(mock):
    return mock.matchers[0]


def test_mock_url(mock):
    mock.url('http://google.es')
    assert str(matcher(mock)) == 'http://google.es'


def test_mock_force_new_reply(mock):
    res = mock._response
    assert res == mock.reply()
    assert res != mock.reply(create=True)
