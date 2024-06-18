import unittest
from unittest.mock import Mock

from ssd.shell import SsdShell


class TestSsdShell(unittest.TestCase):
    def setUp(self):
        self.mk = Mock()
        self.sut = SsdShell(self.mk)

    def test_full_write_once(self):
        test_value = "0xFFFFFFFF"
        self.sut.fullwrite(test_value)
        self.mk.read.return_value = test_value
        self.assertEqual(test_value, self.sut.read(address=10))

    def test_full_write_multy(self):
        test_set = ["0x1111FFFF", "0x1112FFFF", "0xAAAA1234"]
        self.mk.read.side_effect = test_set
        for test_value in test_set:
            self.sut.fullwrite(test_value)
            self.assertEqual(test_value, self.sut.read(address=10))

    def test_full_read_once(self):
        self.sut.fullread()
        self.assertEqual(self.mk.read.call_count, 100)
