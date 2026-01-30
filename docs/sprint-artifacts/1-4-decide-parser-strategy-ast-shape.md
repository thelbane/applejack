# Story 1.4: Decide Parser Strategy + AST Shape

Status: Ready for Review
Decision Scope: Parser strategy (Earley vs LALR) + AST shape (single canonical vs phase-specific)
Decision Criteria: ambiguity tolerance, error quality, performance, maintainability, testability

## Story

As a maintainer,
I want parser strategy and AST shape decisions recorded,
so that implementation is consistent.

## Acceptance Criteria

1. Given the architecture document, when I review decisions, then parser strategy (Earley vs LALR) and AST shape are documented.
2. ADRs exist for parser strategy and AST shape with rationale and trade-offs.
3. Architecture and project context reflect the chosen parser strategy and AST shape.
4. Parser configuration guidance and test alignment notes are documented.

## Tasks / Subtasks

- [x] Evaluate parser strategies (Earley vs LALR) using explicit criteria and select one (AC: 1,2)
  - [x] Document criteria: ambiguity tolerance, error quality, performance, maintainability, testability
  - [x] Record decision + rationale in ADR-001
- [x] Decide AST shape (single canonical vs phase-specific) and record decision (AC: 1,2)
  - [x] Document constraints for Phase 2 extensibility and stability
  - [x] Record decision + rationale in ADR-002
- [x] Update architecture and project context with final decisions (AC: 3,4)
  - [x] Add links to ADRs and summarize decisions in `docs/architecture.md`
  - [x] Update `docs/project_context.md` with parser strategy + AST shape rules
  - [x] Document parser configuration guidance and test alignment notes

## Dev Notes

### Developer Context (Current State)
- Architecture doc identifies ADR-001 (parser strategy) and ADR-002 (AST shape) as open gaps.
- Project context enforces strict parsing rules: no ambiguous parses, whitespace-optional syntax, and first-2-chars variable significance.
- Lark is the parser library (pinned 1.1.9) with Python 3.9.6 baseline.

### Technical Requirements
- Decide parser strategy: Earley vs LALR.
- Decide AST shape: single canonical AST with extension nodes vs phase-specific ASTs.
- Record ADRs with rationale, trade-offs, and implications for grammar, diagnostics, and testing.

### Architecture Compliance
- Keep decisions consistent with stage boundaries: Preprocess → Parse → Transform → Generate.
- Favor determinism and ambiguity handling per architecture and project context.
- Document decision impact on error recovery and diagnostics.

### Library/Framework Requirements
- Lark 1.1.9 (no version changes in this story).
- Python 3.9.6, pytest 8.2.2 (documentation alignment only).

### File Structure Requirements
- Add ADR docs under `docs/adr/` (new folder) or a dedicated ADR section in `docs/architecture.md`.
- Update `docs/architecture.md` to reference ADRs and summarize decisions.
- Update `docs/project_context.md` with parser strategy + AST shape rules for all agents.

### Testing Requirements
- Document how parser strategy affects error handling and ambiguity tests.
- Note any test alignment guidance (e.g., Lark parser config and ambiguity expectations).

### Previous Story Intelligence
- Story 1.3 emphasized pinned versions and minimal tooling; keep this story doc-only.

### Git Intelligence Summary
- Recent commits focused on CI workflow stabilization and story 1.3 cleanup; no parser changes yet.

### Latest Technical Information
- No external research required; versions and constraints are pinned in project context.

### Project Structure Notes
- Keep ADRs and decision summaries within `docs/` and linked from `docs/architecture.md`.
- No source or test files should be modified in this story.

### References
- `docs/epics.md` — Epic 1, Story 1.4 ACs and technical notes.
- `docs/architecture.md` — ADR candidates, parser/AST gap callout.
- `docs/project_context.md` — parser and testing rules, version pins.
- `docs/prd-applejack-v2.md` — Phase 1 parser requirements and constraints.
- `docs/sprint-artifacts/1-3-ci-gate-with-pytest.md` — previous story learnings.

### Story Completion Status
- Status: ready-for-dev
- Completion note: Ultimate context engine analysis completed - comprehensive developer guide created.

## Dev Agent Record

### Context Reference
- `docs/epics.md`
- `docs/architecture.md`
- `docs/project_context.md`
- `docs/prd-applejack-v2.md`
- `docs/sprint-artifacts/1-3-ci-gate-with-pytest.md`

### Agent Model Used

gpt-5.2-codex

### Implementation Plan
- Write ADR-001 and ADR-002 documenting decisions and trade-offs.
- Update architecture and project context to reflect decisions and guidance.
- Mark story tasks complete and update status.

### Debug Log References

None.

### Completion Notes List

### Completion Notes List
- Ultimate context engine analysis completed - comprehensive developer guide created.
- Parser strategy and AST shape decisions scoped with explicit criteria and ADR requirements.
- ADR-001 and ADR-002 created with decisions, trade-offs, and testing notes.
- Architecture and project context updated with accepted parser strategy and AST shape rules.
- Parser configuration guidance and test alignment notes documented.
- Tests: `pytest` (6 passed).

### File List
- `docs/adr/ADR-001-parser-strategy.md`
- `docs/adr/ADR-002-ast-shape.md`
- `docs/architecture.md`
- `docs/project_context.md`
- `docs/sprint-artifacts/1-4-decide-parser-strategy-ast-shape.md`
- `docs/sprint-artifacts/sprint-status.yaml`

### Change Log
- 2026-01-28: Recorded parser strategy and AST shape decisions in ADRs; updated architecture and project context.
