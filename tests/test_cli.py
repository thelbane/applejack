import shutil
import subprocess
import sys


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    applejack = shutil.which("applejack")
    if applejack is not None:
        command = [applejack, *args]
    else:
        command = [sys.executable, "-m", "applejack", *args]
    return subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
    )


def test_cli_version():
    result = run_cli("--version")
    assert result.returncode == 0
    assert result.stdout.strip().startswith("applejack ")
    assert result.stderr == ""


def test_cli_help():
    result = run_cli("--help")
    assert result.returncode == 0
    assert "usage:" in result.stdout
    assert "--version" in result.stdout
    assert result.stderr == ""


def test_cli_missing_command_error():
    result = run_cli()
    assert result.returncode == 2
    assert "error: missing command" in result.stderr


def test_cli_parse_not_implemented():
    result = run_cli("parse", "example.bas")
    assert result.returncode == 2
    assert "error: parse not implemented yet" in result.stderr


def test_cli_validate_not_implemented():
    result = run_cli("validate", "example.bas")
    assert result.returncode == 2
    assert "error: validate not implemented yet" in result.stderr
