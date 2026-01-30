---
stepsCompleted: [1, 2, 3, 4, 5, 6, 7, 8]
inputDocuments:
  - /Users/leefastenau/Code/applejack/docs/prd-applejack-v2.md
workflowType: 'architecture'
lastStep: 8
project_name: 'Applejack'
user_name: 'Lee'
date: '2026-01-24'
status: 'complete'
completedAt: '2026-01-24'
---

# Architecture Decision Document

_This document builds collaboratively through step-by-step discovery. Sections are appended as we work through each architectural decision together._

## Project Context Analysis

### Requirements Overview

**Functional Requirements:**
Phase 1 focuses on strict Applesoft BASIC grammar definition and Lark-based parsing with AST output and validation.  
Phase 2 adds modern language extensions (macros, labels, long variable names, Unicode strings, includes) that must remain backward compatible.  
Phase 3 completes the compiler pipeline with preprocessing, AST transformation, code generation, and a CLI interface.

**Non-Functional Requirements:**
- Performance: < 1s compile for typical programs; < 100MB memory
- Quality: > 90% test coverage; clear, actionable error messages
- Compatibility: strict 1978 Applesoft BASIC output
- Maintainability: modular design and extensibility for future phases

**Scale & Complexity:**
- Primary domain: compiler/tooling
- Complexity level: medium–high
- Estimated architectural components: 5–7 (grammar, parser, preprocessor, transformer, generator, CLI, tests)

### Technical Constraints & Dependencies
- Python 3.9+
- Lark parser library with EBNF grammar
- pytest for validation
- Strict adherence to 1978 Applesoft BASIC standard
- Whitespace-agnostic, case-insensitive parsing
- No runtime execution (compile-only)

### Cross-Cutting Concerns Identified
- Error handling and recovery across parsing and transformation
- Backward compatibility with Applesoft BASIC behavior
- Extensibility for Phase 2 features without destabilizing Phase 1
- Testability against legacy sample programs
- Deterministic output and stable transformations

### ADR Candidates (Decisions to Formalize Early)
- **ADR-001 Parser Strategy:** **Lark Earley** with ambiguity detection (Accepted; see `docs/adr/ADR-001-parser-strategy.md`)
- **ADR-002 AST Shape:** **Single canonical AST** with extension nodes/annotations (Accepted; see `docs/adr/ADR-002-ast-shape.md`)
- **ADR-003 Preprocessing Order:** Macro expansion vs include resolution vs label mapping order
- **ADR-004 Variable Optimization:** Frequency-based renaming algorithm and collision avoidance rules
- **ADR-005 Output Formatting:** Line-number assignment strategy and formatting stability guarantees

### Pre‑mortem Risk Signals (Failure Scenarios to Prevent)
- **Grammar ambiguity leads to inconsistent parse trees**, blocking downstream transformations.  
  _Mitigation: choose parser strategy up front; add ambiguity tests early._
- **PRINT parsing edge cases cause false positives/negatives**, breaking compatibility.  
  _Mitigation: explicit test corpus for PRINT edge cases from spec._
- **AST design becomes brittle for Phase 2**, forcing a rewrite.  
  _Mitigation: decide AST extensibility pattern in ADRs now._
- **Variable renaming introduces collisions**, corrupting programs.  
  _Mitigation: deterministic renaming algorithm with collision tests._
- **Error messages are unusable**, slowing development and adoption.  
  _Mitigation: define error taxonomy and sample message formats early._

### First Principles Restatement (Non‑Negotiables)
- **Correctness over convenience:** Output must be valid 1978 Applesoft BASIC, every time.  
- **Determinism:** Same input must always produce identical output.  
- **Separation of concerns:** Preprocess → Parse → Transform → Generate are distinct stages.  
- **Extensibility without regressions:** Phase 2 features cannot weaken Phase 1 compliance.  
- **Testability as a design constraint:** Every stage must be isolatable and testable.

## Starter Template Evaluation

### Primary Technology Domain
CLI tool / compiler tooling (Python-based)

### Starter Options Considered
1) **Minimal Python CLI (stdlib + setuptools in `pyproject.toml`)**
   - Low barrier to entry, no additional CLI frameworks
   - Works well with `argparse`, `pytest`, and pip-based workflows
2) **Poetry-based CLI scaffold**
   - Structured project layout and dependency management
   - Additional tooling to learn; more opinionated
3) **Cookiecutter CLI templates**
   - Fast scaffold and prewired CI/test/docs
   - Template maintenance quality varies

### Selected Starter: Minimal Python CLI (stdlib + setuptools)
**Rationale for Selection:**
- Lowest barrier to entry for contributors
- Aligns with your existing Python familiarity
- Avoids additional packaging tools while remaining maintainable
- Cross‑platform and easy to test with `pytest`

**Initialization Command:**
```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools
```

**Architectural Decisions Provided by Starter:**

**Language & Runtime:**
- Python (cross‑platform), standard library `argparse` for CLI parsing

**Build Tooling:**
- `pyproject.toml` with setuptools (pip‑native)

**Testing Framework:**
- `pytest`

**Code Organization:**
- `src/` layout for package code
- `tests/` for unit and integration tests

**Development Experience:**
- Simple onboarding: `pip install -e .`
- Compatible with GitHub Actions for CI

## Core Architectural Decisions

### Data Architecture
- **Decision:** No database; file-based inputs/outputs only.
- **Runtime model:** Ephemeral, in-memory processing per run (no persistent cache).
- **Optional artifacts:** Allow debug/learning outputs via explicit flags (e.g., AST dumps), not by default.

### Authentication & Security
- **Decision:** None (local CLI only).
- **Security model:** Rely on local filesystem permissions.
- **Safety flags:** Optional CLI flags such as `--dry-run` and `--no-overwrite` to prevent accidental writes.

### API & Communication Patterns
- **Decision:** Hybrid CLI.
- **I/O model:** File-first inputs/outputs with optional STDIN/STDOUT support for piping.

### Frontend Architecture
- **Decision:** Not applicable (CLI tool).
- **Notes:** No UI planned; revisit only if a GUI/web interface is introduced later.

### Infrastructure & Deployment
- **CI/CD:** GitHub Actions.
- **Packaging:** `pyproject.toml` with setuptools.
- **Distribution:** PyPI (install via `pip` or `pipx`).
- **Versioning:** Semantic Versioning (SemVer).
- **Optional future:** Single-file binaries via PyInstaller (deferred).

### Version Pinning (Implementation Baseline)
- **Python:** 3.9.6
- **Lark:** 1.1.9
- **pytest:** 8.2.2
- **GitHub Actions:** `actions/checkout@v4`, `actions/setup-python@v5`

## Implementation Patterns & Consistency Rules

### Pattern Categories Defined

**Critical Conflict Points Identified:** 5 areas where AI agents could make different choices

### Naming Patterns
**Code Naming Conventions (PEP 8):**
- Classes: `PascalCase`
- Functions/variables: `snake_case`
- Constants: `UPPER_SNAKE_CASE`
- Modules/files: `snake_case.py`

### Structure Patterns
**Project Organization:**
- Source code in `src/applejack/`
- Tests in `tests/`
- CLI entrypoint in `applejack/cli.py` or `applejack/__main__.py`
- Scripts only if required (optional `scripts/`)

**File Structure Patterns:**
- Config in project root (`pyproject.toml`)
- Fixtures in `tests/fixtures/`

### Format Patterns
**Debug/Artifact Output:**
- Debug artifacts emitted only via explicit flags (e.g., `--dump-ast`)
- JSON format with `snake_case` keys
- Human-readable output unless `--json` requested

### Process Patterns
**Error Handling:**
- Exceptions inside modules; catch at CLI boundary
- Errors go to `stderr`
- Non‑zero exit codes on failure

**Logging:**
- Use stdlib `logging`
- Default level: `INFO`
- Verbose mode raises to `DEBUG`

### Enforcement Guidelines
**All AI Agents MUST:**
- Follow PEP 8 naming and module conventions
- Place tests under `tests/` with `test_*.py` naming
- Emit debug artifacts only when explicitly requested

**Pattern Enforcement:**
- Review diffs for naming and structure compliance
- Add linting/formatting later if desired (optional)

### Pattern Examples
**Good Examples:**
- `src/applejack/parser.py`, `tests/test_parser.py`
- `class ParseError(Exception): ...`
- `def parse_program(source: str) -> ProgramAst: ...`

**Anti-Patterns:**
- Mixed naming styles (`parseProgram`, `Parser_test.py`)
- Writing debug artifacts by default
- Errors printed to stdout

## Project Structure & Boundaries

### Complete Project Directory Structure
```
applejack/
├── README.md
├── LICENSE
├── pyproject.toml
├── .gitignore
├── .github/
│   └── workflows/
│       └── ci.yml
├── src/
│   └── applejack/
│       ├── __init__.py
│       ├── __main__.py
│       ├── cli.py
│       ├── config.py
│       ├── errors.py
│       ├── lexer/
│       │   ├── __init__.py
│       │   └── tokens.py
│       ├── parser/
│       │   ├── __init__.py
│       │   ├── grammar_loader.py
│       │   ├── parse.py
│       │   └── ast.py
│       ├── preprocessor/
│       │   ├── __init__.py
│       │   ├── includes.py
│       │   └── macros.py
│       ├── transformer/
│       │   ├── __init__.py
│       │   └── transform.py
│       ├── generator/
│       │   ├── __init__.py
│       │   └── generate.py
│       ├── diagnostics/
│       │   ├── __init__.py
│       │   └── reporter.py
│       └── utils/
│           ├── __init__.py
│           └── io.py
├── grammar/
│   └── applesoft.ebnf
├── tests/
│   ├── __init__.py
│   ├── fixtures/
│   │   ├── applesoft/
│   │   └── edge_cases/
│   ├── test_grammar.py
│   ├── test_parser.py
│   ├── test_preprocessor.py
│   ├── test_transformer.py
│   ├── test_generator.py
│   └── test_cli.py
└── docs/
    ├── architecture.md
    └── prd-applejack-v2.md
```

### Architectural Boundaries
**API Boundaries:**
- CLI boundary: `cli.py`/`__main__.py`
- Public API (optional): `parse.py` and `generate.py` functions

**Component Boundaries:**
- Preprocessor → Parser → Transformer → Generator (no cross‑layer imports)

**Data Boundaries:**
- Filesystem I/O isolated to `utils/io.py` and CLI entrypoints
- AST definitions centralized in `parser/ast.py`

### Requirements to Structure Mapping
**FR Category: Grammar & Parsing**
- `grammar/`
- `src/applejack/parser/`
- `tests/test_grammar.py`, `tests/test_parser.py`

**FR Category: Preprocessing & Extensions (Phase 2)**
- `src/applejack/preprocessor/`
- `tests/test_preprocessor.py`

**FR Category: Transformation & Codegen**
- `src/applejack/transformer/`
- `src/applejack/generator/`
- `tests/test_transformer.py`, `tests/test_generator.py`

**Cross‑Cutting Concerns: Diagnostics**
- `src/applejack/diagnostics/`
- `tests/` for error cases

### Integration Points
**Internal Communication:**
- Pure Python function calls between stages; no shared global state
- AST and intermediate representations passed explicitly

**External Integrations:**
- None (CLI tool)

**Data Flow:**
- Source → Preprocess → Parse (AST) → Transform → Generate → Output

### File Organization Patterns
**Configuration Files:**
- `pyproject.toml` at repo root

**Source Organization:**
- `src/` layout with feature‑oriented subpackages

**Test Organization:**
- `tests/` with `test_*.py` naming and `fixtures/` for samples

### Development Workflow Integration
**Build Process Structure:**
- `pyproject.toml` defines build/metadata
- `ci.yml` runs `pytest`

**Deployment Structure:**
- `pip install -e .` for dev
- PyPI release for distribution

## Architecture Validation Results

### Coherence Validation ✅
**Decision Compatibility:**
- CLI-first tool choices align with Python + stdlib `argparse`.
- No DB and ephemeral processing align with cross‑platform CLI.
- Hybrid CLI I/O aligns with Unix tooling and simple workflows.

**Pattern Consistency:**
- PEP 8 naming, `src/` layout, and test structure are consistent with Python conventions.
- Error/logging patterns align with CLI boundary decisions.

**Structure Alignment:**
- Project tree supports parser pipeline and testing strategy.
- Boundaries prevent cross‑layer coupling.

### Requirements Coverage Validation ✅
**Functional Requirements Coverage:**
- Grammar parsing, preprocessing, transformation, generation all mapped to modules/tests.
- CLI interface supported.

**Non‑Functional Requirements Coverage:**
- Performance and simplicity supported by file‑only, in‑memory processing.
- Maintainability addressed via structure + patterns.

### Implementation Readiness Validation ✅ (with minor gaps)
**Decision Completeness:**
- Core toolchain and CI decisions set.
- **Resolved:** Parser strategy decided (see ADR-001).
- **Resolved:** AST shape decided (see ADR-002).

**Structure Completeness:**
- Complete project tree defined.

**Pattern Completeness:**
- Naming, structure, error/logging patterns defined.

### Gap Analysis Results
**Important Gaps:**
- Version pins for Python/pytest/CI actions (not verified here).

### Validation Issues Addressed
- None blocking; gaps are actionable before implementation.

### Architecture Completeness Checklist
**✅ Requirements Analysis**
- [x] Project context analyzed
- [x] Scale and complexity assessed
- [x] Technical constraints identified
- [x] Cross‑cutting concerns mapped

**✅ Architectural Decisions**
- [x] Core decisions documented
- [x] Stack specified
- [x] Integration patterns defined

**✅ Implementation Patterns**
- [x] Naming conventions established
- [x] Structure patterns defined
- [x] Process patterns documented

**✅ Project Structure**
- [x] Complete directory structure defined
- [x] Boundaries established
- [x] Integration points mapped

### Architecture Readiness Assessment
**Overall Status:** READY WITH MINOR GAPS  
**Confidence Level:** High  
**Key Strengths:** Clear CLI focus, strong structure/patterns, low‑risk architecture  
**Areas for Future Enhancement:** Parser strategy, AST shape, version pinning

### Implementation Handoff
**AI Agent Guidelines:**
- Follow documented decisions and patterns exactly
- Respect project boundaries and I/O flow
- Use tests/fixtures as the source of truth for correctness

**First Implementation Priority:**
- Settle parser strategy + AST shape, then scaffold project tree and tests

## Architecture Completion Summary

### Workflow Completion

**Architecture Decision Workflow:** COMPLETED ✅  
**Total Steps Completed:** 8  
**Date Completed:** 2026-01-24  
**Document Location:** `docs/architecture.md`

### Final Architecture Deliverables

**📋 Complete Architecture Document**
- All architectural decisions documented (versions to be pinned during implementation)
- Implementation patterns ensuring AI agent consistency
- Complete project structure with all files and directories
- Requirements to architecture mapping
- Validation confirming coherence and completeness

**🏗️ Implementation Ready Foundation**
- Core architectural decisions made
- Implementation patterns defined
- Architectural components specified
- Requirements supported

**📚 AI Agent Implementation Guide**
- Technology stack and conventions documented
- Consistency rules that prevent implementation conflicts
- Project structure with clear boundaries
- Integration patterns and communication standards

### Implementation Handoff
**For AI Agents:**
This architecture document is your guide for implementing Applejack. Follow all decisions, patterns, and structures exactly as documented.

**First Implementation Priority:**
Settle parser strategy + AST shape, then scaffold the project tree and tests.

**Development Sequence:**
1. Initialize project structure
2. Set up development environment
3. Implement core architectural foundations
4. Build features following established patterns
5. Maintain consistency with documented rules

### Quality Assurance Checklist
**✅ Architecture Coherence**
- [x] All decisions work together without conflicts
- [x] Patterns support the architectural decisions
- [x] Structure aligns with all choices

**✅ Requirements Coverage**
- [x] Functional requirements are supported
- [x] Non-functional requirements are addressed
- [x] Cross-cutting concerns are handled

**✅ Implementation Readiness**
- [x] Decisions are actionable
- [x] Patterns prevent agent conflicts
- [x] Structure is complete and unambiguous
- [x] Examples are provided for clarity

### Project Success Factors
**🎯 Clear Decision Framework**
Every technology choice was made collaboratively with clear rationale.

**🔧 Consistency Guarantee**
Implementation patterns ensure that multiple AI agents produce compatible code.

**📋 Complete Coverage**
All project requirements are architecturally supported with clear mapping.

**🏗️ Solid Foundation**
The chosen architecture provides a production-ready foundation following best practices.

---

**Architecture Status:** READY FOR IMPLEMENTATION ✅  
**Next Phase:** Begin implementation using the architectural decisions and patterns documented herein.  
**Document Maintenance:** Update this architecture when major technical decisions are made during implementation.
