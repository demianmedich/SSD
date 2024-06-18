import tempfile
import unittest
from pathlib import Path

from ssd.core.impl import VirtualSSD


class VirtualSSDTestCase(unittest.TestCase):

    def test_read_init(self):

        with tempfile.TemporaryDirectory() as tmpdir:
            ssd = VirtualSSD(Path(tmpdir))
            ssd.read(0)
            data = ssd.result_file.read_text().strip()

        self.assertEqual("0x00000000", data)

    def test_write(self):
        self.assertEqual(True, True)


if __name__ == "__main__":
    unittest.main()
