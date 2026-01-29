from pathlib import Path


def test_ci_workflow_runs_pytest():
    content = Path(".github/workflows/ci.yml").read_text(encoding="utf-8")

    assert "actions/checkout@v4" in content
    assert "actions/setup-python@v5" in content
    assert "python-version: '3.9.6'" in content
    assert "python3.9 -m pip install -e \".[dev]\"" in content
    assert "python3.9 -m pytest" in content
