import os
import sys
from pathlib import Path

from ssd.shell.api import ResultReader, Shell

sys.path.append(str(Path(__file__).parent.parent))

api = Shell(ResultReader(Path(os.getcwd())))
default_value = "0x00000000"
test_value = "0x1234567A"
api.fullwrite(test_value)
data = api.fullread()
for read_value in api.fullread():
    if read_value != test_value:
        sys.exit(1)

test_lba = 50
test_value = "0x99999999"
for i in range(0, 3):
    api.write(test_lba + i, test_value)

for i in range(0, 3):
    api.erase(test_lba + i, 1)

for i in range(0, 3):
    data = api.read(test_lba + i)
    if data != default_value:
        sys.exit(1)

sys.exit(0)
