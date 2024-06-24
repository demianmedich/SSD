import sys
from pathlib import Path

from ssd.driver.buffered_ssd import CommandBufferedSSD
from ssd.driver.erasable_ssd import ErasableVirtualSSD
from ssd.driver.range_valid_decorator import RangeValidationDecorator
from ssd.driver.virtual import VirtualSSD


def get_args() -> (str, int, int):
    try:
        cmd = sys.argv[1].upper()
        addr = int(sys.argv[2])
        if cmd == "R":
            return cmd, addr, None
        if cmd == "W":
            return cmd, addr, int(sys.argv[3], 16)
        if cmd == "E":
            return cmd, addr, int(sys.argv[3])
        if cmd == "F":
            return cmd, None, None
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

    if cmd == "R":
        ssd.read(addr)
    if cmd == "W":
        ssd.write(addr, data)
    if cmd == "E":
        ssd.erase(addr, data)
    if cmd == "F":
        ssd.flush()
    if cmd is None:
        ssd.print_help()
    return


if __name__ == "__main__":
    main()
