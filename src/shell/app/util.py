import os
from pathlib import Path

from ssd.core.logger import Logger


class ScriptManager:

    script_dir = Path(__file__).parent.parent.parent.joinpath("script").absolute()

    def find(self, script_name: str):
        script_path = self.script_dir / f"{script_name}.py"
        if not script_path.exists():
            raise FileNotFoundError(f"{script_name}")
        return script_path

    def collect(self, script_name_list: list[str]) -> list[Path]:
        script_paths = []
        missing = []

        for name in script_name_list:
            try:
                script_path = self.find(name)
                script_paths.append(script_path)
            except FileNotFoundError:
                missing.append(name)

        if missing:
            raise FileNotFoundError(", ".join(map(str, missing)))

        return script_paths

    def execute(self, script_path: str) -> bool:
        # TODO!
        # 근데 어떻게? os.system 하면 결과를 받아 오기 애매해.

        # subprocessing 쓰면 되려나? stdout을 redirect하지 않는 한 콘솔 print 안되긴 하겠지.
        # 마지막 print된 것만 테스트 결과로 간주하고 파싱해서 쓸까?

        #  아님 script에서 Command를 상속한 클래스를 파싱해서 import하고 그걸 실행할까?
        # gpt야 도와줘

        os.system(f"python {script_path}")
        return True


if __name__ == "__main__":
    # just for test
    LOG = Logger()
    sm = ScriptManager()
    LOG.print(sm.script_dir)
    LOG.print(sm.script_dir.exists())
