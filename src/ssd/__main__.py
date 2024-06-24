import sys
from pathlib import Path

from ssd.driver.buffered_ssd import CommandBufferedSSD
from ssd.driver.erasable_ssd import ErasableVirtualSSD
from ssd.driver.range_valid_decorator import RangeValidationDecorator
from ssd.driver.virtual import VirtualSSD
from ssd.util.valid import is_8digit_hex_string


def get_args() -> (str, int, int):
    try:
        cmd = sys.argv[1].upper()
        if cmd == "F":
            return cmd, None, None
        addr = int(sys.argv[2])
        if cmd == "R":
            return cmd, addr, None
        if cmd == "W":
            if not is_8digit_hex_string(sys.argv[3]):
                raise IndexError()
            return cmd, addr, int(sys.argv[3], 16)
        if cmd == "E":
            return cmd, addr, int(sys.argv[3])
    except IndexError:
        return None, None, None


def main():
    cmd, addr, data = get_args()

    rootdir = Path.cwd()
    ssd = RangeValidationDecorator(
        CommandBufferedSSD(
            ErasableVirtualSSD((VirtualSSD(rootdir=rootdir))), rootdir=rootdir
        )
    )

    match cmd:
        case "R":
            ssd.read(addr)
        case "W":
            ssd.write(addr, data)
        case "E":
            ssd.erase(addr, data)
        case "F":
            ssd.flush()
        case _:
            ssd.print_help()


if __name__ == "__main__":
    main()
