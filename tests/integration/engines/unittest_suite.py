# -*- coding: utf-8 -*-

import unittest
import requests
import pook


class TestUnitTestEngine(unittest.TestCase):

    @pook.activate
    def test_simple_pook_request(self):
        pook.get('server.com/foo').reply(204)
        res = requests.get('http://server.com/foo')
        self.assertEqual(res.status_code, 204)

    def test_enable_engine(self):
        pook.get('server.com/foo').reply(204)
        res = requests.get('http://server.com/foo')
        self.assertEqual(res.status_code, 204)

    @pook.get('server.com/foo', reply=204)
    def test_decorator(self):
        res = requests.get('http://server.com/foo')
        self.assertEqual(res.status_code, 204)

    def test_context_manager(self):
        with pook.use():
            pook.get('server.com/bar', reply=204)
            res = requests.get('http://server.com/bar')
            self.assertEqual(res.status_code, 204)

    def test_no_match_exception(self):
        pook.get('server.com/bar', reply=204)
        try:
            requests.get('http://server.com/baz')
        except:
            pass
        else:
            raise RuntimeError('expected to fail')
