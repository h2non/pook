# -*- coding: utf-8 -*-

import pook
import pytest
import requests
from unittest import TestCase


# class TestMock(TestCase):
#     def test_api():
#         m = pook.get('http://foobar.com')
#         m.type('application/json')
#         # m.body({"error": "not found"})
#         m.reply(404).json({'error': 'foo'})
#
#         pook.activate()
#
#         print('Response:', requests.get('http://foobar.com'))
#         assert pook.mock('http://python.org') == 0
#
# def assert_response(resp, body=None, content_type='text/plain'):
#     assert resp.status_code == 200
#     assert resp.headers['Content-Type'] == content_type
#     assert resp.text == body
