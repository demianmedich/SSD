import unittest
from unittest.mock import Mock

from ssd.shell import SsdShell


class TestSsdShell(unittest.TestCase):
    def setUp(self):
        self.mk = Mock()
        self.sut = SsdShell(self.mk)

    def test_full_write_once(self):
        test_value = "0xFFFFFFFF"
        self.sut.full_write(test_value)
        self.mk.return_value = test_value
        self.assertEqual(test_value, self.sut.read(lba_pos=10))

    def test_full_write_multy(self):
        test_set = ["0x1111FFFF", "0X1112FFFF", "0XAAAA1234"]
        for test_value in test_set:
            self.sut.full_write(test_value)
            self.mk.return_value = test_value
            self.assertEqual(test_value, self.sut.read(lba_pos=10))
