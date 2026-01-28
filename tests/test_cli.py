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


def test_cli_help():
    result = run_cli("--help")
    assert result.returncode == 0
    assert "usage:" in result.stdout
    assert "--version" in result.stdout


def test_cli_missing_command_error():
    result = run_cli()
    assert result.returncode == 2
    assert "error: missing command" in result.stderr
