# Story 1.1: Scaffold Project Structure

Status: ready-for-dev

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

## Tasks / Subtasks

- [ ] Create root structure files: `README.md`, `LICENSE`, `.gitignore`, `pyproject.toml`.
- [ ] Create directories: `src/applejack/`, `grammar/`, `tests/`, `.github/workflows/`.
- [ ] Add package skeleton under `src/applejack/`:
  - [ ] `__init__.py`
  - [ ] `__main__.py` (CLI stub)
  - [ ] `cli.py` (CLI stub)
  - [ ] `config.py`
  - [ ] `errors.py`
  - [ ] `lexer/`, `parser/`, `preprocessor/`, `transformer/`, `generator/`, `diagnostics/`, `utils/` (each with `__init__.py`)
  - [ ] Placeholder modules: `lexer/tokens.py`, `parser/grammar_loader.py`, `parser/parse.py`, `parser/ast.py`,
        `preprocessor/includes.py`, `preprocessor/macros.py`, `transformer/transform.py`, `generator/generate.py`,
        `diagnostics/reporter.py`, `utils/io.py`
- [ ] Add `tests/` skeleton with placeholder files: `test_grammar.py`, `test_parser.py`, `test_preprocessor.py`,
      `test_transformer.py`, `test_generator.py`, `test_cli.py`, and `tests/fixtures/`.
- [ ] Add `.github/workflows/ci.yml` stub to be finalized in Story 1.3.

## Dev Notes

### Developer Context (Scope)
- This story is about scaffolding only; no feature implementations or parsing logic.
- Keep modules empty or with minimal stubs that do not enforce behavior.
- Hybrid CLI I/O is the architectural direction, but no runtime logic is needed here.

### Technical Requirements
- Language: Python 3.9+.
- Follow PEP 8 naming conventions (snake_case, PascalCase, UPPER_SNAKE_CASE).
- Keep filesystem I/O limited to CLI boundary and `utils/io.py` per architecture.
- Errors should be raised internally and caught at the CLI boundary (no stdout errors).

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

### Latest Tech Information
- Verify version pins before changing any tooling (current pins are from architecture).

### Project Context Reference
- No `project-context.md` found in repo.

## Project Structure Notes

- Alignment target is the architecture tree; deviations require explicit rationale.
- CLI stubs should exist but remain thin until Story 1.2.

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

- None.

### Completion Notes List

- Ultimate context engine analysis completed - comprehensive developer guide created.

### File List

- `docs/sprint-artifacts/1-1-scaffold-project-structure.md`
