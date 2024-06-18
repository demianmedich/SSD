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
        self.sut.write(ADDRESS, VALUE)
        self.mk.write.assert_called_once()

    def test_shell_exit(self):
        self.assertIsNone(self.sut.exit())


def test_shell_exit(self):
    pass


if __name__ == "__main__":
    unittest.main()
