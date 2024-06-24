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

lba = 10
test_value = "0x12312312"
api.write(lba, test_value)
api.flush()
data = api.read(lba)
if data != test_value:
    logger.print("FAIL flush test fail lba = 10")
    sys.exit(1)

lba = 20
test_value = "0x12312312"
for i in range(20, 25):
    api.write(i, test_value)
api.flush()
data = api.read(lba)
if data != test_value:
    logger.print("FAIL flush test fail lba = 20")
    sys.exit(1)

api.flush()
data = api.read(lba)
if data != test_value:
    logger.print("FAIL flush and read test")
    sys.exit(1)

sys.exit(0)
