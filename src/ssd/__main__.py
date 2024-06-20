import sys
from pathlib import Path

from ssd.core.impl import VirtualSSD


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
    ssd = VirtualSSD(Path.cwd())

    if cmd == "R":
        ssd.read(addr)
    if cmd == "W":
        ssd.write(addr, data)
    if cmd == "E":
        ssd.erase(addr, data)
    if cmd == "F":
        ssd.flush()
    if cmd is None:
        print_help()
    return


def print_help():
    print("Invalid command!")
    print("Read:  python ssd R {addr}")
    print("Write: python ssd W {addr} {data}")
    print("Erase: python ssd E {addr} {size}")
    print("Flush: python ssd F ")
    print("addr = [0, 99], data = 0xXXXXXXXX, size = [1, 10]")


if __name__ == "__main__":
    main()
