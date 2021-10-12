import unittest

from parameterized import parameterized


class TestStubFoo123(unittest.TestCase):

    def setUp(self) -> None:
        self.foo = "bar"

    def test_addition(self):
        self.assertEqual(1 + 1, 2)

    @parameterized.expand([
        (1, "hey"),
        ("hello", "world"),
        (True, False)
    ])
    def test_multiple_things(self, one, another):
        self.assertNotEqual(one, another)

    def test_failing(self):
        self.assertFalse(True)

    @unittest.skip("not doing this")
    def test_skipped(self):
        x = 1 / 0

    def test_error(self):
        raise Exception("aaaaaa")
