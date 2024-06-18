import unittest
from pathlib import Path

from ssd.core.impl import VirtualSSD


class VirtualSSDTestCase(unittest.TestCase):
    def test_read(self):
        self.assertEqual(True, True)  # add assertion here

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
