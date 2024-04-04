import json
import pathlib
import subprocess

THIS_DIR = pathlib.Path(__file__).parent
VERSIONS_DIR = THIS_DIR / "versions"

VERSIONS = sorted(VERSIONS_DIR.glob("*"), key=lambda p: p.name)

DATA = THIS_DIR / "data.json"

if not DATA.exists():
    from generate_data import make_filesystem_data

    DATA.write_text(json.dumps(make_filesystem_data(1_000)))

results = []

for version_dir in VERSIONS:
    version = version_dir.name
    venv_dir = version_dir / ".venv"
    print(f"Measuring version {version}")
    result = json.loads(
        subprocess.check_output([venv_dir / "bin" / "python", THIS_DIR / "sample.py"])
    )
    results.append(result)

print("version,validate,validate_json,nested_filesystem")
for result in results:
    version = result["version"]
    validate = result["validate"]
    validate_json = result["validate_json"]
    nested_filesystem = result["nested_filesystem"]
    print(f"{version},{validate:.2f},{validate_json:.2f},{nested_filesystem:.2f}")
