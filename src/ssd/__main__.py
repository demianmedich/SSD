import sys
from pathlib import Path

from ssd.core.impl import VirtualSSD


def get_args() -> (str, int, int):
    try:
        cmd = sys.argv[1]
        addr = int(sys.argv[2])
        if cmd == "R" or cmd == "r":
            return cmd, addr, None
        if cmd == "W" or cmd == "w":
            return cmd, addr, int(sys.argv[3], 16)
        if cmd == "E" or cmd == "e":
            return cmd, addr, int(sys.argv[3])
    except IndexError:
        return None, None, None


def main():
    cmd, addr, data = get_args()
    ssd = VirtualSSD(Path.cwd())

    if cmd == "R" or cmd == "r":
        ssd.read(addr)
    if cmd == "W" or cmd == "w":
        ssd.write(addr, data)
    if cmd == "E" or cmd == "e":
        ssd.erase(addr, data)
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
