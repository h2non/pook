import unittest

import requests

import pook


class TestUnitTestEngine(unittest.TestCase):
    @pook.on
    def test_request(self):
        pook.get("server.com/foo").reply(204)
        res = requests.get("http://server.com/foo")
        self.assertEqual(res.status_code, 204)

    def test_request_with_context_manager(self):
        with pook.use():
            pook.get("server.com/bar", reply=204)
            res = requests.get("http://server.com/bar")
            self.assertEqual(res.status_code, 204)

    @pook.on
    def test_no_match_exception(self):
        pook.get("server.com/bar", reply=204)
        try:
            requests.get("http://server.com/baz")
        except Exception:
            pass
        else:
            raise RuntimeError("expected to fail")
