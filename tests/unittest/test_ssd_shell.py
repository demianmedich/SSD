import unittest
from io import StringIO
from unittest.mock import Mock, patch

from src.ssd.ssd_shell import SsdShell


class TestSsdShell(unittest.TestCase):
    def setUp(self):
        self.mk = Mock()
        self.sut = SsdShell(self.mk)

    def test_write_one_arg(self):
        self.sut.onecmd("write 1")
        self.mk.help.assert_called()

    def test_write(self):
        self.sut.onecmd("write 10 0xAAAABBBB")
        self.mk.write.assert_called()

    def test_read(self):
        self.sut.onecmd("read 10")
        self.mk.read.assert_called()

    def test_exit(self):
        self.assertTrue(self.sut.onecmd("exit"))

    def test_help(self):
        self.sut.onecmd("help")
        self.mk.help.assert_called()

    def test_full_write(self):
        self.sut.onecmd("fullwrite 0xAAAABBBB")
        self.mk.fullwrite.assert_called()

    def test_full_read(self):
        self.sut.onecmd("fullread")
        self.mk.fullread.assert_called()

    def test_testapp1(self):
        self.sut.onecmd("testapp1")
        self.mk.testapp1.assert_called()

    def test_testapp2(self):
        self.sut.onecmd("testapp2")
        self.mk.testapp2.assert_called()

    def test_wrong_cmd(self):
        with patch("sys.stdout", new=StringIO()) as mock_out:
            self.sut.onecmd("get")
            self.assertEqual("INVALID COMMAND", mock_out.getvalue().strip())
