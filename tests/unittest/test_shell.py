import unittest
from unittest.mock import Mock

from src.ssd.shell import Shell


class ShellTestCase(unittest.TestCase):
    def setUp(self):
        self.mk = Mock()
        self.sut = Shell(self.mk)

    def test_shell_write_call_SSD_write(self):
        self.sut.write(3, "0xAAAABBBB")
        self.mk.write.assert_called_once()


def test_shell_exit(self):
    pass


if __name__ == "__main__":
    unittest.main()
