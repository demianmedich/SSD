import unittest
from io import StringIO
from unittest import skip
from unittest.mock import Mock, patch

from ssd.shell.app.cli import SsdTestShellApp


class TestSsdShell(unittest.TestCase):
    def setUp(self):
        self.mk = Mock()
        self.sut = SsdTestShellApp(self.mk)

    def test_write_one_arg(self):
        self.sut.onecmd("write 1")
        self.mk.help.assert_called()

    def test_write(self):
        self.sut.onecmd("write 10 0xAAAABBBB")
        self.mk.write.assert_called()

    def test_write_with_not_convertible_address(self):
        self.sut.onecmd("write bug 0xAAAABBBB")
        self.mk.help.assert_called()

    def test_read(self):
        self.sut.onecmd("read 10")
        self.mk.read.assert_called()

    def test_read_two_parameters(self):
        self.sut.onecmd("read 10 0xFFFFFFFF")
        self.mk.help.assert_called()

    def test_read_with_not_convertible_address(self):
        self.sut.onecmd("read bug")
        self.mk.help.assert_called()

    def test_exit(self):
        self.assertTrue(self.sut.onecmd("exit"))

    def test_help(self):
        self.sut.onecmd("help")
        self.mk.help.assert_called()

    def test_full_write(self):
        self.sut.onecmd("fullwrite 0xAAAABBBB")
        self.mk.fullwrite.assert_called()

    def test_full_write_two_parameters(self):
        self.sut.onecmd("fullwrite 10 0xAAAABBBB")
        self.mk.help.assert_called()

    def test_emptyline(self):
        self.sut.onecmd(" ")

    def test_full_read(self):
        self.sut.onecmd("fullread")
        self.mk.fullread.assert_called()

    @skip
    def test_testapp1(self):
        self.sut.onecmd("testapp1")
        self.mk.testapp1.assert_called()

    @skip
    def test_testapp2(self):
        self.sut.onecmd("testapp2")
        self.mk.testapp2.assert_called()

    def test_wrong_cmd(self):
        with patch("sys.stdout", new=StringIO()) as mock_out:
            self.sut.onecmd("get")
            self.assertTrue(mock_out.getvalue().strip().endswith("INVALID COMMAND"))
