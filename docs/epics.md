 # Applejack - Epic Breakdown
 
 **Author:** Lee
 **Date:** 2026-01-25
 **Project Level:** Level 3 (Complex System)
 **Target Scale:** BMad Method
 
 ---
 
 ## Overview
 
 This document provides the complete epic and story breakdown for Applejack, decomposing the requirements from the [PRD](./prd-applejack-v2.md) into implementable stories.
 
 **Living Document Notice:** This is the initial version. It will be updated after UX Design and Architecture workflows add interaction and technical details to stories.
 
### Context Validation
- PRD loaded: `docs/prd-applejack-v2.md`
- Architecture loaded: `docs/architecture.md`
- UX Design: not found (CLI-only; no UI required)
- Key constraints: Python 3.9+, Lark, pytest, CLI tool, no DB, hybrid I/O

### Epic Summary (Draft)
- To be finalized after epic planning and story breakdown.
 
 ---
 
 ## Functional Requirements Inventory
 
**Phase 1: Grammar Foundation**
- **FR-1.1: Grammar Definition** — Define complete EBNF grammar for 1978 Applesoft BASIC.
- **FR-1.2: Parser Implementation** — Implement Lark parser that produces ASTs.
- **FR-1.3: Grammar Validation** — Validate grammar with samples and edge cases.

**Phase 2: Modern Extensions**
- **FR-2.1: Macro System** — Support `#define` macros expanded pre-parse.
- **FR-2.2: Label Support** — Support `.label` and resolve to line numbers.
- **FR-2.3: Long Variable Names** — Support long names with frequency-based renaming.
- **FR-2.4: Unicode Support** — Support Unicode literals with Apple II mapping.
- **FR-2.5: Include Directives** — Support `#include` with path resolution and cycle detection.

**Phase 3: Compiler Pipeline**
- **FR-3.1: Preprocessor** — Implement macros/includes/labels pipeline.
- **FR-3.2: Transformer** — Convert modern features to standard Applesoft.
- **FR-3.3: Code Generator** — Generate valid Applesoft BASIC output.
- **FR-3.4: CLI Interface** — Provide `applejack input.bas output.bas` CLI.
 
 ---
 
 ## FR Coverage Map
 
**Phase 1**
- FR-1.1 → Epic 2 (Stories 2.1–2.2)
- FR-1.2 → Epic 2 (Stories 2.2–2.3)
- FR-1.3 → Epic 3 (Stories 3.2–3.4)

**Phase 2**
- FR-2.1 → Epic 4 (Story 4.1)
- FR-2.2 → Epic 4 (Story 4.3)
- FR-2.3 → Epic 4 (Story 4.4)
- FR-2.4 → Epic 4 (Story 4.5)
- FR-2.5 → Epic 4 (Story 4.2)

**Phase 3**
- FR-3.1 → Epic 4 (Stories 4.1–4.3) + Epic 5 (Story 5.1)
- FR-3.2 → Epic 5 (Story 5.1)
- FR-3.3 → Epic 5 (Story 5.2)
- FR-3.4 → Epic 1 (Story 1.2) + Epic 5 (Story 5.3)
 
 ---
 
## Epic 1: Foundation & Developer Workflow

**User Value:** Contributors can install, run, and test the CLI with a consistent project structure.

### Story 1.1: Scaffold Project Structure
As a developer, I want a standardized project layout, so that I can navigate and extend the compiler consistently.

**Acceptance Criteria:**
**Given** a new repo  
**When** I check the project tree  
**Then** `src/`, `tests/`, `grammar/`, `.github/workflows/ci.yml`, and `pyproject.toml` exist  
**And** paths align with `docs/architecture.md`  

**Prerequisites:** None  
**Technical Notes:** Use `src/applejack/` layout; no DB; hybrid CLI.

### Story 1.2: CLI Skeleton with argparse
As a developer, I want a CLI entrypoint with basic commands, so that I can invoke parsing and validation.

**Acceptance Criteria:**
**Given** the CLI is installed  
**When** I run `applejack --help`  
**Then** usage and options are shown  
**And** `applejack --version` returns a version string  

**Prerequisites:** 1.1  
**Technical Notes:** Use stdlib `argparse`; errors to stderr; non‑zero exit codes.

### Story 1.3: CI Gate with pytest
As a maintainer, I want CI to run tests on push, so that regressions are caught early.

**Acceptance Criteria:**
**Given** a GitHub Actions workflow  
**When** code is pushed  
**Then** `pytest` runs and fails the build on test failures  

**Prerequisites:** 1.1  
**Technical Notes:** Use GitHub Actions; no extra tooling.

### Story 1.4: Decide Parser Strategy + AST Shape
As a maintainer, I want parser strategy and AST shape decisions recorded, so that implementation is consistent.

**Acceptance Criteria:**
**Given** the architecture document  
**When** I review decisions  
**Then** parser strategy (Earley vs LALR) and AST shape are documented  

**Prerequisites:** 1.1  
**Technical Notes:** Record ADRs; align tests and parser config accordingly.

---

## Epic 2: Strict Applesoft Grammar & Parsing

**User Value:** Users can parse and validate strict 1978 Applesoft BASIC syntax.

### Story 2.1: Implement applesoft.ebnf
As a developer, I want the full Applesoft grammar defined, so that parsing is standards‑compliant.

**Acceptance Criteria:**
**Given** `grammar/applesoft.ebnf`  
**When** it is loaded by Lark  
**Then** it parses valid samples and rejects invalid syntax  

**Prerequisites:** 1.1  
**Technical Notes:** Respect case‑insensitive keywords and optional whitespace.

### Story 2.2: Grammar Loader + Parser Wiring
As a developer, I want a parser pipeline wired to the grammar, so that code can be parsed into ASTs.

**Acceptance Criteria:**
**Given** a valid Applesoft program  
**When** I run the parser  
**Then** I receive a structured AST  
**And** syntax errors produce clear diagnostics  

**Prerequisites:** 2.1  
**Technical Notes:** Lark config per grammar spec (case‑insensitive, optional whitespace).

### Story 2.3: Canonical AST Model
As a developer, I want a stable AST structure, so that future transformations are predictable.

**Acceptance Criteria:**
**Given** parsed programs  
**When** AST nodes are produced  
**Then** node types and fields are consistent and documented  

**Prerequisites:** 1.4, 2.2  
**Technical Notes:** AST definitions live in `parser/ast.py`.

---

## Epic 3: Validation & Diagnostics

**User Value:** Users receive clear errors and can validate programs against the spec.

### Story 3.1: Diagnostics Reporter
As a developer, I want standardized diagnostics, so that errors are clear and actionable.

**Acceptance Criteria:**
**Given** a syntax error  
**When** parsing fails  
**Then** an error with line/column is printed to stderr  

**Prerequisites:** 2.2  
**Technical Notes:** Exceptions internal, caught at CLI boundary.

### Story 3.2: Sample Program Validation
As a developer, I want sample programs to validate grammar correctness.

**Acceptance Criteria:**
**Given** `v1_legacy/samples/`  
**When** tests run  
**Then** all samples parse successfully  

**Prerequisites:** 2.2  
**Technical Notes:** Use pytest; fixtures in `tests/fixtures/`.

### Story 3.3: Edge Case Test Suite
As a developer, I want edge cases covered, so that behavior matches Applesoft.

**Acceptance Criteria:**
**Given** PRINT edge cases and line‑number truncation cases  
**When** tests run  
**Then** outputs match expected behavior  

**Prerequisites:** 2.2  
**Technical Notes:** Include implicit semicolons, variable significance.

### Story 3.4: Golden AST Fixtures
As a developer, I want golden AST outputs, so that parser changes are regression‑safe.

**Acceptance Criteria:**
**Given** fixed input programs  
**When** ASTs are produced  
**Then** they match golden fixtures  

**Prerequisites:** 2.3  
**Technical Notes:** Store fixtures under `tests/fixtures/`.

---

## Epic 4: Modern Extensions (Phase 2)

**User Value:** Users can write modernized Applesoft with macros, labels, includes, and better names.

### Story 4.1: Macro Expansion
As a developer, I want `#define` macros expanded pre‑parse.

**Acceptance Criteria:**
**Given** macro definitions  
**When** preprocessing runs  
**Then** expanded code parses correctly  

**Prerequisites:** 2.2  
**Technical Notes:** Preprocess before parsing.

### Story 4.2: Include Directives
As a developer, I want `#include` files merged with cycle detection.

**Acceptance Criteria:**
**Given** nested includes  
**When** preprocessing runs  
**Then** includes resolve or error on cycles  

**Prerequisites:** 4.1  
**Technical Notes:** Support search paths; no DB.

### Story 4.3: Label Support
As a developer, I want `.label` syntax resolved to line numbers.

**Acceptance Criteria:**
**Given** labels and GOTO/GOSUB  
**When** preprocessing runs  
**Then** labels map to valid line numbers  

**Prerequisites:** 4.1  
**Technical Notes:** Deterministic mapping.

### Story 4.4: Long Variable Names
As a developer, I want long variable names with optimization to Applesoft constraints.

**Acceptance Criteria:**
**Given** long names  
**When** optimization runs  
**Then** names are mapped to valid short identifiers without collisions  

**Prerequisites:** 4.1  
**Technical Notes:** Collision tests required.

### Story 4.5: Unicode String Literals
As a developer, I want Unicode literals mapped to Apple II charset.

**Acceptance Criteria:**
**Given** Unicode strings  
**When** conversion runs  
**Then** unsupported chars are handled per spec  

**Prerequisites:** 4.1  

---

## Epic 5: Compilation Output (Phase 3)

**User Value:** Users can compile modern input into runnable Applesoft BASIC output.

### Story 5.1: Transformer Pipeline
As a developer, I want transformations to convert modern features to strict Applesoft.

**Acceptance Criteria:**
**Given** extended AST  
**When** transformer runs  
**Then** output AST is valid Applesoft  

**Prerequisites:** 2.3, 4.1–4.4  

### Story 5.2: Code Generator
As a developer, I want valid Applesoft code output with correct line numbers.

**Acceptance Criteria:**
**Given** transformed AST  
**When** generator runs  
**Then** output is valid Applesoft BASIC  
**And** line numbering is deterministic  

**Prerequisites:** 5.1  

### Story 5.3: CLI Compile Command
As a user, I want `applejack input.bas output.bas`, so that I can compile files.

**Acceptance Criteria:**
**Given** input file  
**When** I run the compile command  
**Then** output file is generated  
**And** exit codes reflect success/failure  

**Prerequisites:** 5.2  

### Story 5.4: End‑to‑End Validation
As a developer, I want end‑to‑end tests, so that full compilation is verified.

**Acceptance Criteria:**
**Given** sample programs  
**When** e2e tests run  
**Then** outputs match golden results  

**Prerequisites:** 5.3  
 
 ---
 
 ## FR Coverage Matrix
 
| FR | Coverage |
| --- | --- |
| FR-1.1 | Epic 2.1 |
| FR-1.2 | Epic 2.2–2.3 |
| FR-1.3 | Epic 3.2–3.4 |
| FR-2.1 | Epic 4.1 |
| FR-2.2 | Epic 4.3 |
| FR-2.3 | Epic 4.4 |
| FR-2.4 | Epic 4.5 |
| FR-2.5 | Epic 4.2 |
| FR-3.1 | Epic 4.1–4.3 + Epic 5.1 |
| FR-3.2 | Epic 5.1 |
| FR-3.3 | Epic 5.2 |
| FR-3.4 | Epic 1.2 + Epic 5.3 |
 
 ---
 
 ## Summary
 
Five epics deliver user value from foundational setup through strict grammar parsing, diagnostics, modern extensions, and full compilation output. Phase 1 focuses on strict Applesoft grammar and parsing with clear diagnostics and tests. Phase 2 introduces modern authoring conveniences. Phase 3 completes the pipeline with transformation and code generation, wrapped in a CLI.
 
 ---
 
 _For implementation: Use the `create-story` workflow to generate individual story implementation plans from this epic breakdown._
 _This document will be updated after UX Design and Architecture workflows to incorporate interaction details and technical decisions._
