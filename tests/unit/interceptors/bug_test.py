import unittest
import pook
import requests as req


class TestPookBug(unittest.TestCase):
    @pook.get("http://google.com", reply=201)
    def test_1_with_pook(self):
        self.assertEqual(req.get("http://google.com").status_code, 201)

    def test_2_no_pook(self):
        req.get("http://google.com")

    def test_3_no_force_pook(self):
        pook.on()
        pook.off()
        req.get("http://google.com")
