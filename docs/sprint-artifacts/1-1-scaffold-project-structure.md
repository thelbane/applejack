# Story 1.1: Scaffold Project Structure

Status: Ready for Review

## Story

As a developer,
I want a standardized project layout,
so that I can navigate and extend the compiler consistently.

## Acceptance Criteria

1. The repo contains `src/`, `tests/`, `grammar/`, `.github/workflows/ci.yml`, and `pyproject.toml`.
2. The Python package uses `src/applejack/` layout with the modules and subpackages defined in `docs/architecture.md`.
3. `tests/` and `tests/fixtures/` exist and follow `test_*.py` naming conventions.
4. CLI entrypoint stubs exist at `src/applejack/cli.py` and `src/applejack/__main__.py`.
5. All paths and names align with the architecture document.
6. All new modules are stubs only (no runtime logic beyond minimal placeholders).
7. No existing files are modified except to add the new scaffolded structure.
8. No database, auth, or security model is introduced in this story.
9. Performance constraints are out of scope for scaffolding and should not be implemented here.

## Tasks / Subtasks

- [x] Create root structure files: `README.md`, `LICENSE`, `.gitignore`, `pyproject.toml`.
- [x] Create directories: `src/applejack/`, `grammar/`, `tests/`, `.github/workflows/`.
- [x] Add package skeleton under `src/applejack/`:
  - [x] `__init__.py`
  - [x] `__main__.py` (CLI stub)
  - [x] `cli.py` (CLI stub)
  - [x] `config.py`
  - [x] `errors.py`
  - [x] `lexer/`, `parser/`, `preprocessor/`, `transformer/`, `generator/`, `diagnostics/`, `utils/` (each with `__init__.py`)
  - [x] Placeholder modules (stub-only; no runtime logic): `lexer/tokens.py`, `parser/grammar_loader.py`, `parser/parse.py`, `parser/ast.py`,
        `preprocessor/includes.py`, `preprocessor/macros.py`, `transformer/transform.py`, `generator/generate.py`,
        `diagnostics/reporter.py`, `utils/io.py`
- [x] Add `tests/` skeleton with placeholder files: `test_grammar.py`, `test_parser.py`, `test_preprocessor.py`,
      `test_transformer.py`, `test_generator.py`, `test_cli.py`, and `tests/fixtures/`.
- [x] Add `.github/workflows/ci.yml` stub only (placeholder to be finalized in Story 1.3).

## Dev Notes

### Developer Context (Scope)
- This story is about scaffolding only; no feature implementations or parsing logic.
- Keep modules empty or with minimal stubs that do not enforce behavior.
- Hybrid CLI I/O is the architectural direction, but no runtime logic is needed here.
- Do not invent new structure beyond `docs/architecture.md`.

### Technical Requirements
- Language: Python 3.9+.
- Follow PEP 8 naming conventions (snake_case, PascalCase, UPPER_SNAKE_CASE).
- Keep filesystem I/O limited to CLI boundary and `utils/io.py` per architecture.
- Errors should be raised internally and caught at the CLI boundary (no stdout errors).
- No database, auth, or security model is added in this story.
- Performance constraints are out of scope for scaffolding-only work.

### Architecture Compliance
- Maintain strict boundaries: Preprocessor → Parser → Transformer → Generator, no cross-layer imports.
- AST definitions centralized in `parser/ast.py`.
- Source code must live in `src/` (no top-level package modules).

### Library/Framework Requirements
- Architecture pins: Python 3.9.6, Lark 1.1.9, pytest 8.2.2.
- CI uses GitHub Actions `actions/checkout@v4` and `actions/setup-python@v5`.
- Web verification of latest versions was not conclusive; treat these pins as authoritative until explicitly updated.

### File Structure Requirements
- Must mirror the full tree documented in `docs/architecture.md` (see "Complete Project Directory Structure").
- Ensure `grammar/` exists even if empty.
- Ensure `tests/fixtures/` exists for future sample programs.

### Testing Requirements
- Provide empty test modules as placeholders; no tests required in this story.
- Use `test_*.py` naming in `tests/`.

### CI / Deployment Notes
- CI file is a stub only in this story; do not finalize workflow steps until Story 1.3.

### Latest Tech Information
- Verify version pins before changing any tooling (current pins are from architecture).

### Project Context Reference
- No `project-context.md` found in repo.

## Project Structure Notes

- Alignment target is the architecture tree; deviations require explicit rationale.
- CLI stubs should exist but remain thin until Story 1.2.
- This story should not modify any existing files beyond adding the scaffold.

### References

- `docs/epics.md` — Epic 1, Story 1.1 acceptance criteria and notes.
- `docs/architecture.md` — Project structure, boundaries, and tooling pins.
- `docs/prd-applejack-v2.md` — Tech stack (Python, Lark, pytest) and Phase 1 scope.

## Dev Agent Record

### Context Reference

- None (no context XML generated).

### Agent Model Used

gpt-5.2-codex

### Debug Log References

- 2026-01-26: Scaffolded Story 1.1 directories/files.
- 2026-01-26: Installed `pytest` with trusted-host flags; ran `PYTHONPATH=src .venv/bin/pytest`.

### Completion Notes List

- Ultimate context engine analysis completed - comprehensive developer guide created.
- Scaffold placeholders added per Story 1.1.
- Tests: `PYTHONPATH=src .venv/bin/pytest`.

## Change Log

- 2026-01-26: Scaffolded project structure and placeholder modules/tests for Story 1.1.

### File List

- `docs/sprint-artifacts/1-1-scaffold-project-structure.md`
- `docs/sprint-artifacts/sprint-status.yaml`
- `src/applejack/config.py`
- `src/applejack/errors.py`
- `src/applejack/diagnostics/__init__.py`
- `src/applejack/diagnostics/reporter.py`
- `src/applejack/generator/__init__.py`
- `src/applejack/generator/generate.py`
- `src/applejack/lexer/__init__.py`
- `src/applejack/lexer/tokens.py`
- `src/applejack/parser/__init__.py`
- `src/applejack/parser/ast.py`
- `src/applejack/parser/grammar_loader.py`
- `src/applejack/parser/parse.py`
- `src/applejack/preprocessor/__init__.py`
- `src/applejack/preprocessor/includes.py`
- `src/applejack/preprocessor/macros.py`
- `src/applejack/transformer/__init__.py`
- `src/applejack/transformer/transform.py`
- `src/applejack/utils/__init__.py`
- `src/applejack/utils/io.py`
- `tests/fixtures/.gitkeep`
- `tests/test_generator.py`
- `tests/test_grammar.py`
- `tests/test_parser.py`
- `tests/test_preprocessor.py`
- `tests/test_transformer.py`
