# ADR-002: AST Shape (Canonical vs Phase-Specific)

Status: Accepted  
Date: 2026-01-28

## Context
Phase 1 needs a stable AST for grammar validation and diagnostics. Phase 2 introduces extensions
that must remain backward compatible without forcing a rewrite of downstream stages.

## Decision
Adopt a **single canonical AST** with **explicit extension nodes or annotations** for Phase 2
features.

## Rationale (Decision Criteria)
- **Maintainability:** One AST model avoids duplicated definitions and inconsistent invariants.
- **Testability:** Golden AST fixtures remain stable across phases with controlled extensions.
- **Extensibility:** Extension nodes/annotations allow Phase 2 features without breaking Phase 1.
- **Determinism:** A single canonical shape reduces divergent interpretations between stages.

## Trade-offs
- **Additional design rigor** is needed to keep extension nodes well-scoped and optional.
- **Potential verbosity** as extension metadata accumulates; mitigate with clear node conventions.

## Implications
- Core AST nodes must be stable and documented in `src/applejack/parser/ast.py`.
- Phase 2 features should be represented as explicit extension nodes or annotations rather than
  alternative AST schemas.
- Transformers should assume the canonical shape and handle extension nodes explicitly.

## Testing Notes
- Maintain golden fixtures for the canonical AST shape.
- Add targeted tests for extension nodes when Phase 2 work begins.
