import unittest

from pythonscript import hash_code, de_hash_code, User, Admin, Database


class TestPt(unittest.TestCase):
    def test_hash_code(self):
        assert hash_code("Hello")

    def test_de_hash_code(self):
        assert de_hash_code(hash_code("Hello"))
