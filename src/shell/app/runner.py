"""
TODO:
    모든 검증 스크립트는 성공 실패 여부를 리턴해야 한다.
    그 검증 스크립트는 Shell에서도 실행할 수 있어야 한다.
"""

from pathlib import Path

from shell.app.util import ScriptManager
from ssd.core.logger import Logger


class SsdTestRunnerApp:
    def __init__(self):
        self._script_manager = ScriptManager()
        self.LOG = Logger()

    def execute_runlist(self, run_list_path: Path | str) -> None:
        run_list_path = Path(run_list_path).absolute()
        if not run_list_path.exists():
            self.LOG.print("FileNotFoundError: Run list file does not exist")
            return

        script_names = self._parse_run_list(run_list_path)

        try:
            script_paths = self._script_manager.collect(script_names)
            self.LOG.print(script_paths)
        except FileNotFoundError as e:
            self.LOG.print(f"FileNotFoundError: {e}")
            return

        for _name, _path in zip(script_names, script_paths):
            self.LOG.print(f"{_name}\t---\tRun...", end="")
            test_result = self._script_manager.execute(_path)
            if not test_result:
                self.LOG.print("FAIL!")
                break
            self.LOG.print("Pass")

    @staticmethod
    def _parse_run_list(run_list: Path) -> list[str]:
        with open(run_list, "r") as file:
            return file.read().strip().split("\n")
