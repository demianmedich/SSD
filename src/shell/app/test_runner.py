"""
TODO:
    모든 검증 스크립트는 성공 실패 여부를 리턴해야 한다.
    그 검증 스크립트는 Shell에서도 실행할 수 있어야 한다.
"""

import os
from pathlib import Path


class SsdTestRunnerApp:
    script_dir_path = Path(__file__).parent.parent.parent.joinpath("script")

    def execute_runlist(self, run_list_path: Path | str) -> None:
        run_list_path = Path(run_list_path).absolute()
        if not run_list_path.exists():
            print("FileNotFoundError: Run list file does not exist")
            return

        script_names = self._parse_run_list(run_list_path)

        try:
            script_paths = self._collect_scripts(script_names)
            print(script_paths)
        except FileNotFoundError:
            print(
                "FileNotFoundError: 존재하지 않는 시나리오가 있으니 list와 /script를 확인해 보세요"
            )
            return

        for _name, _path in zip(script_names, script_paths):
            print(f"{_name}\t---\tRun...", end="")
            test_result = self._run_script(_path)
            if not test_result:
                print("FAIL!")
                break
            print("Pass")

    def _parse_run_list(self, run_list: Path) -> list[str]:
        with open(run_list, "r") as file:
            return file.read().strip().split("\n")

    def _collect_scripts(self, script_names: list[str]) -> list[Path]:
        script_paths = []

        for name in script_names:
            script_path = self.script_dir_path / f"{name}.py"
            if not script_path.exists():
                raise FileNotFoundError
            script_paths.append(script_path)

        return script_paths

    def _run_script(self, script_path: Path) -> bool:
        # TODO!
        # 근데 어떻게? os.system 하면 결과를 받아 오기 애매해.

        # subprocessing 쓰면 되려나? stdout을 redirect하지 않는 한 콘솔 print 안되긴 하겠지.
        # 마지막 print된 것만 테스트 결과로 간주하고 파싱해서 쓸까?

        #  아님 script에서 Command를 상속한 클래스를 파싱해서 import하고 그걸 실행할까?
        # gpt야 도와줘

        os.system(f"python {script_path}")
        return True
