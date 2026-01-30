# ADR-001: Parser Strategy (Earley vs LALR)

Status: Accepted  
Date: 2026-01-28

## Context
Applesoft BASIC has whitespace-optional syntax, case-insensitive keywords, and legacy edge cases.
We need clear error diagnostics and strict rejection of ambiguous parses, while remaining extensible
for Phase 2 language features.

## Decision
Use **Lark Earley** as the parser strategy, with ambiguity detection enabled.

**Configuration guidance:**
- `parser="earley"`
- `ambiguity="explicit"` (treat any ambiguity as an error)

## Rationale (Decision Criteria)
- **Ambiguity tolerance:** Earley can parse ambiguous grammars while still surfacing ambiguity
  explicitly; we will fail on ambiguous parses per project rules.
- **Error quality:** Earley’s generalized parsing provides clearer error locations for complex
  grammar edge cases, improving diagnostics.
- **Maintainability:** Earley is more resilient while the grammar evolves and Phase 2 extensions
  are added without constant grammar conflicts.
- **Testability:** Ambiguity detection can be tested directly with targeted edge cases.
- **Performance:** Acceptable for typical Applesoft program sizes in Phase 1; monitor and optimize
  grammar if needed.

## Trade-offs
- **Slower than LALR** on large inputs; mitigated by typical program sizes and focused grammar.
- **Requires explicit ambiguity handling** to avoid silently accepting multiple parses.

## Implications
- Grammar changes must preserve determinism by failing fast on ambiguity.
- Error reporting should include ambiguity notices (when triggered).
- Parser tests must include ambiguity detection scenarios and expected failures.

## Testing Notes
- Add regression tests that confirm ambiguous inputs are rejected.
- Validate diagnostics include line/column and ambiguity context where applicable.
