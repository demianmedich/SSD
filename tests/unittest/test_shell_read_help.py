import unittest
from unittest.mock import Mock

from src.ssd.shell import SsdShell


class TestSsdShell(unittest.TestCase):
    def setUp(self):
        self.ssd = Mock()
        self.shell = SsdShell(ssd_accessor=self.ssd)

    def test_read_api_called(self):
        pass

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
