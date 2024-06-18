import sys
from pathlib import Path

from ssd.core.impl import VirtualSSD


def get_args():
    cmd = sys.argv[1]
    addr = int(sys.argv[2])
    if cmd == "R" or cmd == "r":
        return cmd, addr, None
    if cmd == "W" or cmd == "w":
        data = sys.argv[3]
        return cmd, addr, data


def main():
    cmd, addr, data = get_args()
    ssd = VirtualSSD(Path.cwd())

    if cmd == "R" or cmd == "r":
        ssd.read(addr)
    if cmd == "W" or cmd == "w":
        ssd.write(addr, data)
    return


if __name__ == "__main__":
    main()
