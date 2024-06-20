# coding=utf-8
import tempfile
import unittest
from pathlib import Path

from ssd.driver.buffered_decorator import CommandBufferedSSD
from ssd.driver.range_valid_decorator import RangeValidationDecorator
from ssd.driver.virtual import VirtualSSD

DEFAULT_VALUE = 0x00000000


class VirtualSSDTestCase(unittest.TestCase):

    def read_data_from_temp_file(self, ssd: VirtualSSD, addr: int) -> int:
        with tempfile.TemporaryDirectory() as tmpdir:
            ssd.set_rootdir(tmpdir)
            ssd.read(addr)
            data = ssd.result_file.read_text()
        return int(data, 16)

    def read_data_from_nand_file(self, ssd: VirtualSSD, addr: int) -> int:
        ssd.read(addr)
        data = ssd.result_file.read_text()
        return int(data, 16)

    def test_is_exist_nand_txt(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            ssd = VirtualSSD(tmpdir)

            self.assertEqual(ssd.nand_file.exists(), True)

    def test_read_nand_not_exists(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            ssd = VirtualSSD(tmpdir)
            ssd.result_file.unlink(missing_ok=True)

            self.assertEqual(DEFAULT_VALUE, self.read_data_from_nand_file(ssd, 0))

    def test_read_return_default_value_not_in_valid_range(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            ssd = VirtualSSD(tmpdir)

            self.assertEqual(DEFAULT_VALUE, self.read_data_from_nand_file(ssd, -1))
            self.assertEqual(DEFAULT_VALUE, self.read_data_from_nand_file(ssd, 100))

    def test_read_from_nand_init(self):
        ssd = VirtualSSD()

        self.assertEqual(DEFAULT_VALUE, self.read_data_from_temp_file(ssd, 0))
        (Path.cwd() / "nand.txt").unlink(missing_ok=True)
        (Path.cwd() / "result.txt").unlink(missing_ok=True)

    def test_write_to_invalid_range(self):
        addr = 3
        data = 0x12345678

        with tempfile.TemporaryDirectory() as tmpdir:
            ssd = VirtualSSD(tmpdir)
            ssd.write(addr, data)
            actual = self.read_data_from_nand_file(ssd, addr)
            self.assertEqual(data, actual)

    def test_read_write(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            ssd = VirtualSSD(tmpdir)

            expected1 = 0x1A3B
            ssd.write(1, expected1)
            actual1 = self.read_data_from_nand_file(ssd, 1)

            expected2 = 0x1111
            ssd.write(2, expected2)
            actual2 = self.read_data_from_nand_file(ssd, 2)

            expected3 = 0xA8898778
            ssd.write(99, expected3)
            actual3 = self.read_data_from_nand_file(ssd, 99)

        self.assertEqual(expected1, actual1)
        self.assertEqual(expected2, actual2)
        self.assertEqual(expected3, actual3)

    def test_buffer_read_write(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            ssd = VirtualSSD(rootdir=tmpdir)
            buffer = CommandBufferedSSD(ssd, tmpdir)

            expected = "0x12341234"
            addr = 0
            buffer.write(f"W {addr} {expected}")
            actual = buffer.read(addr)
            self.assertEqual(expected, actual)

            expected = "0x99997677"
            addr = 99
            buffer.write(f"W {addr} {expected}")
            actual = buffer.read(addr)
            self.assertEqual(expected, actual)

            for data in ssd.nand_file.read_text(encoding="utf-8").split("\n"):
                if not data:
                    continue

                self.assertEqual("0x00000000", data.split("\t")[-1].strip())


if __name__ == "__main__":
    unittest.main()
