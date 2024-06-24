import tempfile
import unittest
from pathlib import Path

from ssd.driver.buffered_ssd import CommandBufferedSSD
from ssd.driver.erasable_ssd import ErasableVirtualSSD
from ssd.driver.virtual import VirtualSSD


class BufferedSSDTestCase(unittest.TestCase):

    def read_from_result_file(self, rootdir: Path) -> int:
        return int((rootdir / "result.txt").read_text(), 16)

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


if __name__ == "__main__":
    unittest.main()
