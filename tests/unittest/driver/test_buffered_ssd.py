import tempfile
import unittest
from pathlib import Path

from ssd.driver.buffered_ssd import CommandBufferedSSD
from ssd.driver.erasable_ssd import ErasableVirtualSSD
from ssd.driver.virtual import VirtualSSD


class BufferedSSDTestCase(unittest.TestCase):

    def read_from_result_file(self, rootdir: Path) -> int:
        return int((rootdir / "result.txt").read_text(), 16)

    def read_from_buffer_file(self, rootdir: Path):
        return (rootdir / "buffer.txt").read_text().split("\n")

    def extract_nand_data(self, tmpdir: Path, addr: int):
        return (tmpdir / "nand.txt").read_text().split("\n")[addr].split("\t")[-1]

    def assert_all_nand_data_zero(self, tmpdir):
        for data in (tmpdir / "nand.txt").read_text(encoding="utf-8").split("\n"):
            if not data:
                continue

            self.assertEqual("0x00000000", data.split("\t")[-1].strip())

    def test_write_read(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            ssd = CommandBufferedSSD(
                ErasableVirtualSSD(VirtualSSD(rootdir=tmpdir)), rootdir=tmpdir
            )

            addr = 0
            expected = 0x11111111
            ssd.write(addr, expected)
            ssd.read(addr)

            self.assertEqual(expected, self.read_from_result_file(tmpdir))
            self.assert_all_nand_data_zero(tmpdir)

            ssd.flush()
            actual = self.extract_nand_data(tmpdir, addr)

            self.assertEqual(expected, int(actual, 16))

    def test_overwrite(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            ssd = CommandBufferedSSD(
                ErasableVirtualSSD(VirtualSSD(rootdir=tmpdir)), rootdir=tmpdir
            )

            addr = 0
            value = 0x11111111
            ssd.write(addr, value)
            expected = 0xAAAABBBB
            ssd.write(addr, expected)
            ssd.read(addr)

            self.assertEqual(expected, self.read_from_result_file(tmpdir))
            self.assert_all_nand_data_zero(tmpdir)

            ssd.flush()
            actual = self.extract_nand_data(tmpdir, addr)

            self.assertEqual(expected, int(actual, 16))

    def test_split_erase(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            ssd = CommandBufferedSSD(
                ErasableVirtualSSD(VirtualSSD(rootdir=tmpdir)), rootdir=tmpdir
            )

            erase_addr = 0
            size = 5
            ssd.erase(erase_addr, size)

            addr = 3
            value = 0x11111111
            ssd.write(addr, value)

            expected = ["E 0 3", "E 4 1", "W 3 0x11111111", ""]

            self.assertEqual(expected, self.read_from_buffer_file(tmpdir))
            self.assert_all_nand_data_zero(tmpdir)

    def test_merge_erase(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            ssd = CommandBufferedSSD(
                ErasableVirtualSSD(VirtualSSD(rootdir=tmpdir)), rootdir=tmpdir
            )

            erase_addr = 0
            size = 5
            ssd.erase(erase_addr, size)

            erase_addr = 5
            size = 1
            ssd.erase(erase_addr, size)

            expected = ["E 0 6", ""]

            self.assertEqual(expected, self.read_from_buffer_file(tmpdir))
            self.assert_all_nand_data_zero(tmpdir)

    def test_erase(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            ssd = CommandBufferedSSD(
                ErasableVirtualSSD(VirtualSSD(rootdir=tmpdir)), rootdir=tmpdir
            )

            addr = 3
            value = 0x11111111
            ssd.write(addr, value)

            erase_addr = 0
            size = 5
            ssd.erase(erase_addr, size)

            expected = ["E 0 5", ""]
            self.assertEqual(expected, self.read_from_buffer_file(tmpdir))

            ssd.flush()
            actual = self.extract_nand_data(tmpdir, addr)
            self.assertEqual(0x00000000, int(actual, 16))

    def test_flush(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            ssd = CommandBufferedSSD(
                ErasableVirtualSSD(VirtualSSD(rootdir=tmpdir)), rootdir=tmpdir
            )

            erase_addr = 0
            size = 5
            ssd.erase(erase_addr, size)

            addr = 3
            value = 0x11111111
            ssd.write(addr, value)

            addr = 0
            value = 0x11111111
            ssd.write(addr, value)

            addr = 10
            value = 0x11111111
            ssd.write(addr, value)

            erase_addr = 20
            size = 5
            ssd.erase(erase_addr, size)

            addr = 30
            value = 0x11111111
            ssd.write(addr, value)

            addr = 22
            value = 0x11111111
            ssd.write(addr, value)

            addr = 99
            value = 0x11111111
            ssd.write(addr, value)

            addr = 89
            value = 0x11111111
            ssd.write(addr, value)

            self.assertEqual(1, len(self.read_from_buffer_file(tmpdir)))

            for i in range(100):
                actual = self.extract_nand_data(tmpdir, i)
                if i in [3, 0, 10, 30, 22, 99]:
                    self.assertEqual(value, int(actual, 16))
                elif i in [1, 2, 4, 20, 21, 23, 24]:
                    self.assertEqual(0x00000000, int(actual, 16))


if __name__ == "__main__":
    unittest.main()
