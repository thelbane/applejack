# Story 1.2: CLI Skeleton with argparse

Status: ready-for-dev
Story Key: 1-2-cli-skeleton-with-argparse
Epic: 1 (Foundation & Developer Workflow)
Prerequisites: 1.1 (done)

## Story

As a developer,
I want a CLI entrypoint with basic commands,
so that I can invoke parsing and validation from the terminal.

## Acceptance Criteria

1. Running `applejack --help` displays usage and options.
2. Running `applejack --version` returns a version string.
3. The CLI uses stdlib `argparse` (no external CLI framework).
4. Errors are written to stderr and return non-zero exit codes.

## Tasks / Subtasks

- [ ] Implement CLI argument parser in `src/applejack/cli.py` (AC: 1, 2, 3)
  - [ ] Wire `--help` and `--version` flags
  - [ ] Ensure `main()` returns exit codes
- [ ] Ensure module entrypoint calls `main()` in `src/applejack/__main__.py` (AC: 1, 2)
- [ ] Add/adjust tests in `tests/test_cli.py` for help/version output (AC: 1, 2)
- [ ] Add error handling path that writes to stderr and uses non-zero exit (AC: 4)

## Dev Notes

### Developer Context (Current State)
- `src/applejack/cli.py` already exists with a minimal argparse parser and `--version` flag.
- `src/applejack/__main__.py` calls `main()` for `python -m applejack`.
- `src/applejack/__init__.py` defines `__version__`.
- `tests/test_cli.py` exists as a placeholder for CLI tests.

### Epic Context (Epic 1: Foundation & Developer Workflow)
- Epic objective: establish a consistent developer workflow and CLI foundation for Applejack.
- Adjacent stories in Epic 1:
  - 1.1 Scaffold Project Structure (done)
  - 1.3 CI Gate with pytest
  - 1.4 Decide Parser Strategy + AST Shape

### Technical Requirements
- Use stdlib `argparse`; do not add external CLI frameworks.
- `applejack --help` must display usage and options.
- `applejack --version` must print a version string.
- Errors must go to stderr and return non-zero exit codes.
- Define at least one explicit error path for invalid usage (e.g., missing required args) that writes a short message to stderr and returns exit code 2.
- Keep CLI minimal; do not implement parsing/validation logic in this story.
- Do not emit debug artifacts unless explicitly requested.
- Reuse the existing `build_parser()`/`main()` shape in `cli.py`; extend it rather than replacing it.
- Prefer `argparse.ArgumentParser(add_help=True)` and `parser.error(...)` for consistent stderr formatting and exit code 2.

### Architecture Compliance
- CLI is the boundary: catch exceptions here; internal modules raise typed exceptions.
- Preserve stage boundaries (Preprocess → Parse → Transform → Generate); no cross-layer imports.
- Keep filesystem I/O at CLI boundary or `utils/io.py` only (no new I/O needed here).

### Pitfalls to Avoid (Anti-Patterns)
- Do not add external CLI frameworks or new dependencies.
- Do not move files outside `src/applejack/` or `tests/`.
- Do not print errors to stdout.
- Do not implement parsing/validation logic in the CLI for this story.
- Do not add debug artifact outputs by default.

### Library/Framework Requirements
- Pinned stack: Python 3.9.6, Lark 1.1.9, pytest 8.2.2 (do not upgrade in this story).
- CI uses GitHub Actions `actions/checkout@v4` and `actions/setup-python@v5`.
- Latest versions exist (Lark 1.3.1, pytest 9.0.2 requires Python 3.10+); keep pins unchanged.
 - Performance work is out of scope for this story (CLI should stay minimal).

### File Structure Requirements
- Modify only `src/applejack/cli.py`, `src/applejack/__main__.py`, and `tests/test_cli.py`.
- Keep source under `src/applejack/` and tests under `tests/`.
- Do not add new top-level packages or files.

### Testing Requirements
- Add pytest coverage for `--help` and `--version`.
- Validate stderr usage and non-zero exit code for an error path.

### Critical Issues (Must Fix)
- Ensure error-path behavior is explicit (stderr + exit code 2 example).
- Preserve and extend existing CLI stubs; avoid rewrites.
- Follow anti-patterns list to avoid scope creep.

### Enhancements (Should Add)
- Include a focused test for the explicit error path.
- Keep CLI behavior minimal and predictable (no hidden defaults).

### Story Completion Status
- Status: ready-for-dev
- Completion note: Ultimate context engine analysis completed - comprehensive developer guide created.

### Previous Story Intelligence
- Story 1.1 established the scaffold; keep changes confined to CLI files/tests.
- CI workflow is a stub until Story 1.3; avoid touching it here.
- Architecture tree and module boundaries are the source of truth.
- Story 1.1 explicitly required stub-only modules and no runtime logic beyond placeholders.
- 1.1 review fixes added CI stub and fixtures subdirs; avoid editing unrelated files.

### Git Intelligence Summary
- Recent commits focused on scaffolding and review fixes (structure + fixtures + CI stub).
- Avoid unrelated file edits; keep scope to CLI and tests.
 - Notable recent files: `src/applejack/cli.py`, `src/applejack/__main__.py`, `docs/sprint-artifacts/1-1-scaffold-project-structure.md`,
   `docs/sprint-artifacts/sprint-status.yaml`, `.github/workflows/ci.yml`, `tests/fixtures/**`.

### Project Structure Notes
- Align with the architecture tree under `src/applejack/`.
- No variances expected for this story.

### References
- `docs/epics.md` — Epic 1, Story 1.2 acceptance criteria and notes.
- `docs/architecture.md` — CLI boundary, structure, and pinned versions.
- `docs/prd-applejack-v2.md` — Phase 1 scope and CLI requirements.
- `docs/project_context.md` — non-negotiable rules and version pins.

## Dev Agent Record

### Context Reference
- `docs/epics.md`
- `docs/architecture.md`
- `docs/prd-applejack-v2.md`
- `docs/project_context.md`
- `docs/sprint-artifacts/1-1-scaffold-project-structure.md`

### Agent Model Used
gpt-5.2-codex

### Debug Log References
- 2026-01-26: Story 1.2 context generated (create-story workflow).

### Completion Notes List
- Ultimate context engine analysis completed - comprehensive developer guide created.

### File List
- `docs/sprint-artifacts/1-2-cli-skeleton-with-argparse.md`
- `docs/sprint-artifacts/sprint-status.yaml`
