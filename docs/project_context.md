---
project_name: 'Applejack'
user_name: 'Lee'
date: '2026-01-25'
sections_completed:
  - technology_stack
  - language_rules
  - framework_rules
  - testing_rules
  - quality_rules
  - workflow_rules
  - anti_patterns
existing_patterns_found: 5
status: 'complete'
rule_count: 25
optimized_for_llm: true
---

# Project Context for AI Agents

_This file contains critical rules and patterns that AI agents must follow when implementing code in this project. Focus on unobvious details that agents might otherwise miss._

---

## Technology Stack & Versions

- Python: 3.9.6 (from repo venv)
- Parser: Lark 1.1.9
- Tests: pytest 8.2.2
- CI: GitHub Actions `actions/checkout@v4`, `actions/setup-python@v5`

## Critical Implementation Rules

### Language-Specific Rules
- Follow PEP 8 naming (snake_case, PascalCase, etc.)
- Keep stage boundaries strict: Preprocess → Parse → Transform → Generate
- Catch exceptions at CLI boundary; internal modules raise typed exceptions
- No global mutable state across stages; pass AST/IR explicitly

### Parser Strategy Rules
- Use Lark **Earley** parser with `ambiguity="explicit"` and treat ambiguity as an error
- Keep grammar deterministic; if ambiguity appears, fix grammar or fail fast
- Preserve case-insensitive keywords and whitespace-optional syntax in parser config

### AST Shape Rules
- Maintain a single canonical AST in `src/applejack/parser/ast.py`
- Represent Phase 2 features as extension nodes or annotations, not separate ASTs

### Framework-Specific Rules
- Use stdlib `argparse` for CLI; avoid external CLI frameworks unless explicitly approved.

### Testing Rules
- Use `pytest` with `tests/` and `test_*.py` naming
- Keep golden fixtures in `tests/fixtures/`
- Add explicit edge‑case tests for PRINT parsing and line‑number truncation
- Validate grammar against legacy samples (`v1_legacy/samples/`)
- Add ambiguity tests to ensure ambiguous inputs are rejected by the parser
- Keep golden AST fixtures aligned with the canonical AST shape

### Code Quality & Style Rules
- Prefer small, pure functions per stage
- Avoid implicit I/O inside parsing/transformation stages
- Use explicit type hints for public functions
- Keep module imports within their layer (no cross‑layer imports)

### Development Workflow Rules
- Use GitHub Actions for CI (pytest as the gate)
- Prefer small, focused PRs mapped to a single story
- Do not introduce tooling (formatters/linters) without explicit approval

### Critical Don't-Miss Rules
- Do NOT accept ambiguous parses; update grammar or parser strategy to disambiguate
- Do NOT auto‑write debug artifacts unless explicitly requested
- Do NOT rely on whitespace for token separation (Applesoft is whitespace‑optional)
- Always treat only first 2 chars of variable names as significant (core standard)
- Ensure PRINT parsing handles implicit semicolons and variable ambiguity

---

## Usage Guidelines
**For AI Agents:**
- Read this file before implementing any code
- Follow ALL rules exactly as documented
- When in doubt, prefer the more restrictive option
- Update this file if new patterns emerge

**For Humans:**
- Keep this file lean and focused on agent needs
- Update when the technology stack changes
- Review quarterly for outdated rules
- Remove rules that become obvious over time

Last Updated: 2026-01-25
