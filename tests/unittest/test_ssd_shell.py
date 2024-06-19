import unittest
from unittest.mock import Mock

from src.ssd.ssd_shell import SsdShell


class TestSsdShell(unittest.TestCase):
    def setUp(self):
        self.mk = Mock()
        self.sut = SsdShell(self.mk)

    def test_read(self):
        self.sut.do_read("0")
        self.mk.read.assert_called()

    def test_write(self):
        self.sut.do_write("0 0")
        self.mk.write.assert_called()

    def test_exit(self):
        self.assertTrue(self.sut.do_exit(""))

    def test_help(self):
        self.sut.do_help("")
        self.mk.help.assert_called()

    def test_full_read(self):
        self.sut.do_fullread("")
        self.mk.fullread.assert_called()

    def test_full_write(self):
        self.sut.do_fullwrite("0x0")
        self.mk.fullwrite.assert_called()
