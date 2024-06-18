import unittest
from unittest.mock import Mock

from src.ssd.core import SsdShell


class TestSsdShell(unittest.TestCase):
    def setUp(self):
        self.mk = Mock()
        self.sut = SsdShell(self.mk)

    def test_read_invalid_address(self):
        pass

    def test_read_unwritten_lba(self):
        pass

    def test_read_written_lba(self):
        pass

    def test_help(self):
        pass


if __name__ == "__main__":
    unittest.main()
