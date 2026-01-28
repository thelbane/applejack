# Story 1.3: CI Gate with pytest

Status: ready-for-dev

## Story

As a maintainer,
I want CI to run tests on push,
so that regressions are caught early.

## Acceptance Criteria

1. Given a GitHub Actions workflow, when code is pushed, then `pytest` runs and fails the build on test failures.

## Tasks / Subtasks

- [ ] Update `.github/workflows/ci.yml` to run pytest on push/PR (AC: 1)
  - [ ] Use `actions/checkout@v4` and `actions/setup-python@v5`
  - [ ] Use Python 3.9.6 and install `.[dev]` deps
  - [ ] Run `python3.9 -m pytest` and fail on non-zero exit
- [ ] Ensure CI does not introduce extra tooling (AC: 1)
- [ ] Add/adjust tests only if needed for CI validation (AC: 1)

## Dev Notes

### Developer Context (Current State)
- `.github/workflows/ci.yml` exists from Story 1.1 but is a stub.
- Tests are under `tests/` and currently run with `python3.9 -m pytest`.
- Project pins Python 3.9.6, pytest 8.2.2, and uses stdlib tooling only.

### Epic Context (Epic 1: Foundation & Developer Workflow)
- Epic objective: establish a consistent developer workflow and CLI foundation for Applejack.
- Adjacent stories in Epic 1:
  - 1.1 Scaffold Project Structure (done)
  - 1.2 CLI Skeleton with argparse (done)
  - 1.4 Decide Parser Strategy + AST Shape

### Technical Requirements
- Use GitHub Actions; no extra tooling beyond what is already in the repo.
- CI must run `pytest` and fail the build on test failures.
- Use pinned versions from project context:
  - Python 3.9.6
  - pytest 8.2.2
  - `actions/checkout@v4`, `actions/setup-python@v5`
- Install dev dependencies via `pip install -e ".[dev]"`.
- Keep CI minimal; no formatting/linting tools in this story.

### Architecture Compliance
- Follow project structure and pins from `docs/architecture.md` and `docs/project_context.md`.
- Keep workflow changes confined to `.github/workflows/ci.yml`.

### Pitfalls to Avoid (Anti-Patterns)
- Do not upgrade Python, pytest, or GitHub Actions versions.
- Do not add new CI tooling (linters, formatters, coverage uploaders).
- Do not move or rename workflow files.
- Do not add unnecessary jobs or steps.

### Library/Framework Requirements
- Python: 3.9.6
- pytest: 8.2.2
- GitHub Actions: `actions/checkout@v4`, `actions/setup-python@v5`

### File Structure Requirements
- Modify only `.github/workflows/ci.yml` unless tests require change.
- Keep tests in `tests/` with `test_*.py` naming.

### Testing Requirements
- CI must run `python3.9 -m pytest`.
- CI should install dependencies using `pip install -e ".[dev]"`.

### Enhancements (Should Add)
- Trigger CI on `push` and `pull_request`.
- Cache Python dependencies if simple and already supported by setup-python (optional).

### Story Completion Status
- Status: ready-for-dev
- Completion note: Ultimate context engine analysis completed - comprehensive developer guide created.

### Previous Story Intelligence
- Story 1.2 kept scope narrow and updated `.gitignore` to ignore build/test artifacts.
- Tests are executed via `python3.9 -m pytest` and depend on optional `dev` extras.
- CI workflow remained a stub and was explicitly left for Story 1.3.

### Git Intelligence Summary
- Recent commits focused on scaffolding and CLI work (stories 1.1 and 1.2).
- No prior CI gate implemented; expect to update `.github/workflows/ci.yml`.

### Latest Technical Information
- Newer major versions exist for `actions/setup-python` and `actions/checkout`, but project pins `v5` and `v4` respectively. Stick to pinned versions for this story.

### Project Structure Notes
- Align with the architecture tree under `src/applejack/` and workflow location under `.github/workflows/`.
- No variances expected for this story.

### References
- `docs/epics.md` — Epic 1, Story 1.3 acceptance criteria and notes.
- `docs/architecture.md` — CI and version pins.
- `docs/prd-applejack-v2.md` — Phase 1 requirements and testing expectations.
- `docs/project_context.md` — non-negotiable rules and version pins.
- `docs/sprint-artifacts/1-2-cli-skeleton-with-argparse.md` — previous story learnings.

## Dev Agent Record

### Context Reference
- `docs/epics.md`
- `docs/architecture.md`
- `docs/prd-applejack-v2.md`
- `docs/project_context.md`
- `docs/sprint-artifacts/1-2-cli-skeleton-with-argparse.md`

### Agent Model Used
gpt-5.2-codex

### Debug Log References
- 2026-01-27: Story 1.3 context generated (create-story workflow).

### Completion Notes List
- Ultimate context engine analysis completed - comprehensive developer guide created.

### File List
- `docs/sprint-artifacts/1-3-ci-gate-with-pytest.md`
