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
        self.logger = Logger()

    def execute_runlist(self, run_list_path: Path | str) -> None:
        run_list_path = Path(run_list_path).absolute()
        if not run_list_path.exists():
            self.logger.print("FileNotFoundError: Run list file does not exist")
            return

        script_names = self._parse_run_list(run_list_path)

        try:
            script_paths = self._script_manager.collect(script_names)
        except FileNotFoundError as e:
            self.logger.print(f"FileNotFoundError: {e}")
            return

        for _name, _path in zip(script_names, script_paths):
            print(f"{_name}\t---\tRun...", end="", flush=True)
            test_result = self._script_manager.execute(_path)
            if not test_result:
                print("FAIL!")
                break
            print("Pass")

    @staticmethod
    def _parse_run_list(run_list: Path) -> list[str]:
        with open(run_list, "r") as file:
            return file.read().strip().split("\n")
