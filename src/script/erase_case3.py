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

for lba in range(0, 20):
    api.erase(lba, 2)

for lba in range(0, 20):
    data = api.read(lba)
    if data != default_value:
        sys.exit(1)

api.fullwrite(test_value)
for read_value in api.fullread():
    if read_value != test_value:
        sys.exit(1)

for lba in range(0, 20):
    api.erase(lba, 9)

for lba in range(0, 29):
    data = api.read(lba)
    if data != default_value:
        sys.exit(1)

sys.exit(0)
