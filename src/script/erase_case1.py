import os
import sys
from pathlib import Path

from ssd.shell.api import ResultReader, Shell

sys.path.append(str(Path(__file__).parent.parent))

api = Shell(ResultReader(Path(os.getcwd())))
default_value = "0x00000000"
test_value = "0x1234567A"
api.fullwrite(test_value)
for read_value in api.fullread():
    if read_value != test_value:
        sys.exit(1)

api.erase(10, 10)
for lba in range(10, 19):
    data = api.read(lba)
    if data != default_value:
        sys.exit(1)

api.fullwrite(test_value)
data = api.fullread()

for read_value in api.fullread():
    if read_value != test_value:
        sys.exit(1)

api.erase(10, 10)
for lba in range(10, 19):
    data = api.read(lba)
    if data != default_value:
        sys.exit(1)

api.erase_range(0, 99)
for lba in range(0, 99):
    data = api.read(lba)
    if data != default_value:
        sys.exit(1)

sys.exit(0)
