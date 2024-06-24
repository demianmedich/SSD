import os
import sys
from pathlib import Path

from ssd.shell.api import ResultReader, Shell

sys.path.append(str(Path(__file__).parent.parent))

api = Shell(ResultReader(Path(os.getcwd())))

test_value = "0xAAAAAAAA"
api.fullwrite(test_value)
data = api.fullread()

for read_value in api.fullread():
    if read_value != test_value:
        sys.exit(1)

sys.exit(0)
