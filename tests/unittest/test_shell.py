import os
import unittest
from io import StringIO
from pathlib import Path
from unittest.mock import Mock, patch

from src.ssd.shell import ReadResultAccessor, Shell

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
        self.mk.fetch_read_result.return_value = test_value
        self.assertEqual(test_value, self.sut.read(address=10))

    def test_full_write_real(self):
        test_value = "0xFFFFFFF"
        real = Shell(ReadResultAccessor(Path(os.getcwd())))
        real.fullwrite(test_value)
        self.assertEqual(test_value, real.read(address=55))

    def test_full_write_multi(self):
        test_set = ["0x1111FFFF", "0x1112FFFF", "0xAAAA1234"]
        self.mk.fetch_read_result.side_effect = test_set
        for test_value in test_set:
            self.sut.fullwrite(test_value)
            self.assertEqual(test_value, self.sut.read(address=10))

    def test_full_read_once(self):
        self.sut.fullread()
        self.assertEqual(self.mk.fetch_read_result.call_count, 100)

    def test_full_read_multi(self):
        self.sut.fullread()
        self.sut.fullread()
        self.assertEqual(self.mk.fetch_read_result.call_count, 200)

    @patch("sys.stdout", new_callable=StringIO)
    def test_read_invalid_address(self, mk_stdout):
        invalid_address = 100

        self.sut.read(invalid_address)

        self.assertEqual(self.sut.HELP_MESSAGE, mk_stdout.getvalue().strip())

    def test_read_unwritten_lba(self):
        unwritten_value = "0x00000000"
        self.mk.fetch_read_result.return_value = unwritten_value

        self.assertEqual(unwritten_value, self.sut.read(ADDRESS))

    def test_read_written_lba(self):
        self.mk.fetch_read_result.return_value = VALUE

        self.assertEqual(VALUE, self.sut.read(ADDRESS))

    @patch("sys.stdout", new_callable=StringIO)
    def test_help(self, mk_stdout):
        self.sut.help()

        self.assertEqual(self.sut.HELP_MESSAGE, mk_stdout.getvalue().strip())


if __name__ == "__main__":
    unittest.main()
