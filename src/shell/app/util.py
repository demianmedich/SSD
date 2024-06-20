import subprocess
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

    @staticmethod
    def execute(script_path: Path | str) -> bool:
        ret = subprocess.run(["python", str(script_path)], capture_output=True)
        return ret.returncode == 0


if __name__ == "__main__":
    # just for test
    logger = Logger()
    sm = ScriptManager()
    logger.print(sm.script_dir)
    logger.print(sm.script_dir.exists())
