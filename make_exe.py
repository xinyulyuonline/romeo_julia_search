from __future__ import annotations

import subprocess
import sys
import textwrap
from pathlib import Path


ROOT = Path(__file__).resolve().parent
LAUNCHER = ROOT / "_exe_launcher.py"


def run(command: list[str]) -> None:
	subprocess.check_call(command, cwd=ROOT)


def main() -> None:
	run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "pyinstaller"])
	LAUNCHER.write_text(
		textwrap.dedent(
			"""\
			from app import app
			import uvicorn

			if __name__ == '__main__':
			    uvicorn.run(app, host='0.0.0.0', port=8000)
			"""
		),
		encoding="utf-8",
	)
	run([sys.executable, "-m", "PyInstaller", "--onefile", "--name", "romeo_julia_search", str(LAUNCHER)])
	if LAUNCHER.exists():
		LAUNCHER.unlink()


if __name__ == "__main__":
	main()