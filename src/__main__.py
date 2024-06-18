import sys
from pathlib import Path

from ssd.core.impl import VirtualSSD


def get_args():
    cmd = sys.argv[1]
    addr = int(sys.argv[2])
    if cmd == "R":
        return cmd, addr, None
    if cmd == "W":
        data = sys.argv[3]
        return cmd, addr, data


def main():
    cmd, addr, data = get_args()
    ssd = VirtualSSD(Path.cwd())

    if cmd == "R":
        ssd.read(addr)
    if cmd == "W":
        ssd.write(addr, data)
    return


if __name__ == "__main__":
    main()
