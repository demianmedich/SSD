"""
TODO:
    모든 검증 스크립트는 성공 실패 여부를 리턴해야 한다.
    그 검증 스크립트는 Shell에서도 실행할 수 있어야 한다.
"""

from pathlib import Path


class SsdTestRunnerApp:
    script_dir_path = Path(__file__).parent.parent.parent.joinpath("script")

    def execute_runlist(self, run_list_path: Path | str) -> None:
        run_list_path = Path(run_list_path).absolute()
        if not run_list_path.exists():
            print("FileNotFoundError: Run list file does not exist")
            return

        try:
            test_scripts = self._collect_scripts(run_list_path)
            print(test_scripts)
        except FileNotFoundError:
            print(
                "FileNotFoundError: 존재하지 않는 시나리오가 있으니 list와 /script를 확인해 보세요"
            )
            return

        # TODO: run 구현

    def _collect_scripts(self, run_list: Path) -> list[Path]:
        with open(run_list, "r") as file:
            script_names = file.read().strip().split("\n")

        script_paths = []
        for name in script_names:
            script_path = self.script_dir_path / f"{name}.py"
            if not script_path.exists():
                raise FileNotFoundError
            script_paths.append(script_path)

        return script_paths
