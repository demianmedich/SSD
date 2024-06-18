import unittest
from io import StringIO
from unittest.mock import Mock, patch

from src.ssd.shell import SsdShell


class TestSsdShell(unittest.TestCase):
    def setUp(self):
        self.ssd = Mock()
        self.shell = SsdShell(ssd_accessor=self.ssd)
        self.target_address = 3

    def test_read_api_called(self):
        self.shell.read(self.target_address)
        self.ssd.read.assert_called()

    def test_read_invalid_address(self):
        invalid_address = 100
        with self.assertRaises(ValueError):
            self.shell.read(invalid_address)

    @patch("sys.stdout", new_callable=StringIO)
    def test_read_unwritten_lba(self, mk_stdout):
        unwritten_value = "0x00000000"
        self.ssd.read.return_value = unwritten_value

        self.shell.read(self.target_address)

        self.assertEqual(unwritten_value, mk_stdout.getvalue().strip())

    @patch("sys.stdout", new_callable=StringIO)
    def test_read_written_lba(self, mk_stdout):
        written_value = "0x19930516"
        self.ssd.read.return_value = written_value

        self.shell.read(self.target_address)

        self.assertEqual(written_value, mk_stdout.getvalue().strip())

    def test_help(self):
        pass


if __name__ == "__main__":
    unittest.main()
