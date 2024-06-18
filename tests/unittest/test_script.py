import unittest
from unittest.mock import Mock


class TestScriptTestCase(unittest.TestCase):
    def test_testapp1(self):
        self.assertEqual(True, True)

    def test_testapp2(self):
        self.assertEqual(True, True)


if __name__ == "__main__":
    unittest.main()
