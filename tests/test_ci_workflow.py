from pathlib import Path


def test_ci_workflow_runs_pytest():
    content = Path(".github/workflows/ci.yml").read_text(encoding="utf-8")

    assert "actions/checkout@v4" in content
    assert "actions/setup-python@v5" in content
    assert "python-version: '3.9'" in content
    assert "python -m pip install --upgrade pip" in content
    assert "python -m pip install \".[dev]\"" in content
    assert "python -m pip install \"pytest==8.2.2\"" in content
    assert "python -m pytest" in content
