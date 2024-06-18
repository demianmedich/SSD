import unittest
from io import StringIO
from unittest.mock import Mock, patch

from src.ssd.shell import SsdShell


class TestSsdShell(unittest.TestCase):
    def setUp(self):
        self.read_res = Mock()
        self.shell = SsdShell(read_res_accessor=self.read_res)
        self.target_address = 3

    @patch("sys.stdout", new_callable=StringIO)
    def test_read_invalid_address(self, mk_stdout):
        invalid_address = 100

        self.shell.read(invalid_address)

        self.assertEqual(self.shell.HELP_MESSAGE, mk_stdout.getvalue().strip())

    @patch("sys.stdout", new_callable=StringIO)
    def test_read_unwritten_lba(self, mk_stdout):
        unwritten_value = "0x00000000"
        self.read_res.fetch_read_result.return_value = unwritten_value

        self.shell.read(self.target_address)

        self.assertEqual(unwritten_value, mk_stdout.getvalue().strip())

    @patch("sys.stdout", new_callable=StringIO)
    def test_read_written_lba(self, mk_stdout):
        written_value = "0x19930516"
        self.read_res.fetch_read_result.return_value = written_value

        self.shell.read(self.target_address)

        self.assertEqual(written_value, mk_stdout.getvalue().strip())

    @patch("sys.stdout", new_callable=StringIO)
    def test_help(self, mk_stdout):
        self.shell.help()

        self.assertEqual(self.shell.HELP_MESSAGE, mk_stdout.getvalue().strip())


if __name__ == "__main__":
    unittest.main()
