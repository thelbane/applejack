import subprocess
import sys


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "applejack", *args],
        check=False,
        capture_output=True,
        text=True,
    )


def test_cli_version():
    result = run_cli("--version")
    assert result.returncode == 0
    assert result.stdout.strip().startswith("applejack ")
