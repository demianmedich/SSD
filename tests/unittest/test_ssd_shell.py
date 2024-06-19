import unittest
from io import StringIO
from unittest.mock import Mock, patch

from src.ssd.ssd_shell import SsdShell


class TestSsdShell(unittest.TestCase):
    def setUp(self):
        self.mk = Mock()
        self.sut = SsdShell(self.mk)

    def test_write_one_arg(self):
        with patch("sys.stdout", new=StringIO()) as mock_out:
            with self.assertRaises(NotImplementedError):
                self.sut.onecmd("write 1")

    def test_write_none_hex_arg(self):
        with patch("sys.stdout", new=StringIO()) as mock_out:
            with self.assertRaises(ValueError):
                self.sut.onecmd("write 10 0x1G2HAAAA")

    def test_write(self):
        with patch("sys.stdout", new=StringIO()) as mock_out:
            self.sut.onecmd("write 10 0xAAAABBBB")
            self.mk.write.assert_called()

    def test_read_invalid_address(self):
        with patch("sys.stdout", new=StringIO()) as mock_out:
            with self.assertRaises(ValueError):
                self.sut.onecmd("read 1000")

    def test_read(self):
        with patch("sys.stdout", new=StringIO()) as mock_out:
            self.sut.onecmd("read 10")
            self.mk.read.assert_called()

    def test_exit(self):
        with patch("sys.stdout", new=StringIO()) as mock_out:
            self.assertTrue(self.sut.onecmd("exit"))

    def test_help(self):
        with patch("sys.stdout", new=StringIO()) as mock_out:
            self.sut.onecmd("help")
            self.mk.help.assert_called()

    def test_full_write(self):
        with patch("sys.stdout", new=StringIO()) as mock_out:
            self.sut.onecmd("fullwrite")
            self.mk.fullwrite.assert_called()

    def test_full_read(self):
        with patch("sys.stdout", new=StringIO()) as mock_out:
            self.sut.onecmd("fullread")
            self.mk.fullread.assert_called()

    def test_testapp1(self):
        with patch("sys.stdout", new=StringIO()) as mock_out:
            self.sut.onecmd("testapp1")
            self.mk.testapp1.assert_called()

    def test_testapp2(self):
        with patch("sys.stdout", new=StringIO()) as mock_out:
            self.sut.onecmd("testapp2")
            self.mk.testapp2.assert_called()

    def test_wrong_cmd(self):
        with patch("sys.stdout", new=StringIO()) as mock_out:
            self.sut.onecmd("get")

            self.assertEqual("INVALID COMMAND", mock_out.getvalue().strip())
