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

for lba in range(0, 20):
    api.erase(lba, 2)

for lba in range(0, 20):
    data = api.read(lba)
    if data != default_value:
        logger.print("FAIL read fail")
        sys.exit(1)

api.fullwrite(test_value)
for read_value in api.fullread():
    if read_value != test_value:
        logger.print("FAIL fullwrite fail")
        sys.exit(1)

for lba in range(0, 20):
    api.erase(lba, 9)

for lba in range(0, 29):
    data = api.read(lba)
    if data != default_value:
        logger.print("FAIL last read fail")
        sys.exit(1)

sys.exit(0)
