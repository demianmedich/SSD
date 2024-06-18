import unittest
from unittest.mock import Mock

from src.ssd.shell import Shell

ADDRESS = 3
VALUE = "0xAAAABBBB"


class ShellTestCase(unittest.TestCase):
    def setUp(self):
        self.mk = Mock()
        self.sut = Shell(self.mk)

    def test_shell_write_call_SSD_write(self):
        self.assertIsNone(self.sut.write(ADDRESS, VALUE))

    def test_shell_exit(self):
        self.assertIsNone(self.sut.exit())

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


def test_shell_exit(self):
    pass


if __name__ == "__main__":
    unittest.main()
