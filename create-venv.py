import pathlib
import subprocess
import sys

THIS_DIR = pathlib.Path(__file__).parent
VERSIONS_DIR = THIS_DIR / "versions"

PYTHON = sys.executable


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("version", help="Pydantic version to install")
    args = parser.parse_args()

    version = args.version
    version_dir = VERSIONS_DIR / version
    if not version_dir.exists():
        version_dir.mkdir(parents=True)

    venv_dir = version_dir / ".venv"

    subprocess.run([PYTHON, "-m", "venv", venv_dir])
    subprocess.run(
        [venv_dir / "bin" / "pip", "install", "pydantic~={}.0".format(version)]
    )


if __name__ == "__main__":
    main()
