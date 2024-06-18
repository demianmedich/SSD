import os
import tempfile
import unittest
from pathlib import Path

from ssd.core.impl import VirtualSSD

DEFAULT_BYTES = 0x00000000.to_bytes()


class VirtualSSDTestCase(unittest.TestCase):

    def read_data_from_temp_file(self, ssd: VirtualSSD, addr: int):
        with tempfile.TemporaryDirectory() as tmpdir:
            ssd.set_rootdir(Path(tmpdir))
            ssd.read(addr)
            data = ssd.result_file.read_bytes()
        return data

    def test_read_nand_not_exists(self):
        ssd = VirtualSSD()
        with tempfile.TemporaryDirectory() as tmpdir:
            ssd.set_rootdir(Path(tmpdir))
            ssd.result_file.unlink(missing_ok=True)

        self.assertEqual(DEFAULT_BYTES, self.read_data_from_temp_file(ssd, 0))

    def test_read_return_default_value_not_in_valid_range(self):
        ssd = VirtualSSD()

        self.assertEqual(DEFAULT_BYTES, self.read_data_from_temp_file(ssd, -1))
        self.assertEqual(DEFAULT_BYTES, self.read_data_from_temp_file(ssd, 100))

    def test_read_from_nand_init(self):
        ssd = VirtualSSD()

        self.assertEqual(DEFAULT_BYTES, self.read_data_from_temp_file(ssd, 0))

    def test_ssd_write(self):
        addr = 3
        data = 0x12345678

        ssd = VirtualSSD(Path.cwd())
        ssd.write(addr, data)

        with open(ssd.nand_file, "r") as f:
            f.seek((len(f.readline()) + 1) * addr)
            result = int(f.readline().split()[-1], 16)

        self.assertEqual(data, result)

    def test_is_exist_nand_txt(self):
        ssd = VirtualSSD(Path.cwd())
        if not ssd.nand_file.exists():
            with self.assertRaises(Exception):
                with open(ssd.nand_file, "r") as f:
                    pass


if __name__ == "__main__":
    unittest.main()
