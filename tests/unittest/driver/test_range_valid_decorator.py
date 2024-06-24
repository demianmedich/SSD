import sys
import tempfile
import unittest
from contextlib import contextmanager
from io import StringIO
from pathlib import Path

from ssd.driver.buffered_ssd import CommandBufferedSSD
from ssd.driver.erasable_ssd import ErasableVirtualSSD
from ssd.driver.range_valid_decorator import RangeValidationDecorator
from ssd.driver.virtual import VirtualSSD


@contextmanager
def capture_stdout():
    temp_stdout = sys.stdout
    io = StringIO()
    try:
        sys.stdout = io
        yield io
    finally:
        io.close()
        sys.stdout = temp_stdout


class RangeValidationDecoratorTestCase(unittest.TestCase):
    def assert_equal_read_print_help_message(self, addr, help_msg, ssd):
        with capture_stdout() as io:
            ssd.read(addr)
            self.assertEqual(help_msg, io.getvalue().strip())

    def test_read_do_print_help(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            ssd = RangeValidationDecorator(
                CommandBufferedSSD(
                    ErasableVirtualSSD(VirtualSSD(rootdir=tmpdir)), rootdir=tmpdir
                )
            )

            help_msg = ssd.help_message.strip()
            self.assert_equal_read_print_help_message(-1, help_msg, ssd)
            self.assert_equal_read_print_help_message(100, help_msg, ssd)

    def assert_equal_write_print_help_message(self, addr, help_msg, ssd):
        with capture_stdout() as io:
            ssd.write(addr, 0x11112222)
            self.assertEqual(help_msg, io.getvalue().strip())

    def test_write_do_print_help(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            ssd = RangeValidationDecorator(
                CommandBufferedSSD(
                    ErasableVirtualSSD(VirtualSSD(rootdir=tmpdir)), rootdir=tmpdir
                )
            )

            help_msg = ssd.help_message.strip()
            self.assert_equal_write_print_help_message(-1, help_msg, ssd)
            self.assert_equal_write_print_help_message(100, help_msg, ssd)


if __name__ == "__main__":
    unittest.main()
