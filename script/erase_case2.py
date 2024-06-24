import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from ssd.shell.api import ResultReader, Shell
from ssd.util.logger import Logger

logger = Logger()
api = Shell(ResultReader(Path(os.getcwd())))
default_value = "0x00000000"
test_value = "0x1234567A"
api.fullwrite(test_value)
for read_value in api.fullread():
    if read_value != test_value:
        logger.print("FAIL full read fail")
        sys.exit(1)

api.erase(100, 10)
for lba in range(0, 99):
    data = api.read(lba)
    if data == default_value:
        logger.print("FAIL erase addr 100 size 10")
        sys.exit(1)

api.erase(0, 1000)
for lba in range(0, 99):
    data = api.read(lba)
    if data == default_value:
        logger.print("FAIL erase addr 0 size 1000")
        sys.exit(1)

api.erase_range(0, 110)
for lba in range(0, 99):
    data = api.read(lba)
    if data == default_value:
        logger.print("FAIL erase range addr 0 size 110")
        sys.exit(1)

for lba in range(0, 99):
    data = api.read(lba)
    if data == default_value:
        logger.print("FAIL read 0 to 99 lba")
        sys.exit(1)

sys.exit(0)
