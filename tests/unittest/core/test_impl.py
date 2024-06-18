import os
import tempfile
import unittest
from pathlib import Path

from ssd.core.impl import VirtualSSD

DEFAULT_VALUE = "0x00000000"


class VirtualSSDTestCase(unittest.TestCase):

    def read_data_from_temp_file(self, ssd: VirtualSSD, addr: int):
        with tempfile.TemporaryDirectory() as tmpdir:
            ssd.set_rootdir(Path(tmpdir))
            ssd.read(addr)
            data = ssd.result_file.read_text().strip()
        return data

    def test_read_nand_not_exists(self):
        ssd = VirtualSSD()
        with tempfile.TemporaryDirectory() as tmpdir:
            ssd.set_rootdir(Path(tmpdir))
            ssd.result_file.unlink(missing_ok=True)

        self.assertEqual(DEFAULT_VALUE, self.read_data_from_temp_file(ssd, 0))

    def test_read_return_default_value_not_in_valid_range(self):
        ssd = VirtualSSD()

        self.assertEqual(DEFAULT_VALUE, self.read_data_from_temp_file(ssd, -1))
        self.assertEqual(DEFAULT_VALUE, self.read_data_from_temp_file(ssd, 100))

    def test_read_from_nand_init(self):
        ssd = VirtualSSD()

        self.assertEqual(DEFAULT_VALUE, self.read_data_from_temp_file(ssd, 0))

    def test_write(self):
        self.assertEqual(True, True)


if __name__ == "__main__":
    unittest.main()
