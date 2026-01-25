# Product Requirements Document: Applejack V2

**Project:** Applejack V2  
**Version:** 1.0  
**Date:** 2025-12-05  
**Status:** Draft  
**Author:** Product Manager

---

## Executive Summary

Applejack V2 is a modern compiler and transpiler for Applesoft BASIC (1978 standard) that enables developers to write maintainable, modern Applesoft programs using contemporary development practices. The product transforms legacy Applesoft BASIC code into optimized, structured programs while maintaining full compatibility with the original 1978 Applesoft BASIC runtime.

**Key Value Propositions:**
- Write Applesoft BASIC with modern features (macros, labels, long variable names, Unicode)
- Maintain backward compatibility with 1978 Applesoft BASIC standard
- Improve code maintainability and readability
- Enable code organization through includes and modular structure
- Optimize variable usage for memory efficiency

---

## Problem Statement

### Current State (V1 Legacy)

The existing Applejack V1 implementation provides basic preprocessing capabilities but has limitations:
- Limited grammar formalization
- Ad-hoc parsing and transformation
- Difficult to extend with new features
- No strict adherence to Applesoft BASIC standard
- Limited error handling and validation

### Pain Points

1. **Legacy Code Maintenance**: Applesoft BASIC programs are difficult to maintain due to:
   - Line-number-based control flow (GOTO/GOSUB)
   - Short variable names (first 2 characters significant)
   - No code organization mechanisms (includes, modules)
   - Limited string handling (no Unicode support)

2. **Development Experience**: Modern developers struggle with:
   - No macro system for code reuse
   - No labels for readable control flow
   - No long variable names for clarity
   - No include system for modular code

3. **Technical Debt**: V1 implementation lacks:
   - Formal grammar definition
   - Comprehensive test coverage
   - Extensible architecture
   - Standard compliance validation

### Target Users

1. **Retro Computing Enthusiasts**: Developers maintaining or creating new Apple II software
2. **Game Developers**: Creating games for Apple II using modern development practices
3. **Educational Users**: Teaching programming with Applesoft BASIC while using modern tools
4. **Legacy Software Maintainers**: Teams maintaining existing Applesoft BASIC codebases

---

## Product Goals and Objectives

### Primary Goals

1. **Strict Standards Compliance**: Implement a compiler that strictly adheres to the 1978 Applesoft BASIC standard
2. **Modern Development Features**: Enable modern programming practices while maintaining compatibility
3. **Code Quality**: Improve code maintainability, readability, and organization
4. **Extensibility**: Create an architecture that supports future enhancements

### Success Metrics

- **Grammar Completeness**: 100% coverage of 1978 Applesoft BASIC statements and functions
- **Compatibility**: 100% backward compatibility with existing Applesoft BASIC programs
- **Test Coverage**: Comprehensive test suite covering all language features
- **Performance**: Compilation time < 1 second for typical programs (< 10,000 lines)
- **Error Quality**: Clear, actionable error messages for invalid syntax

---

## Product Requirements

### Phase 1: Grammar Foundation (Current Phase)

**Objective**: Establish a strict, formal grammar for 1978 Applesoft BASIC

#### Functional Requirements

**FR-1.1: Grammar Definition**
- **Priority**: P0 (Critical)
- **Description**: Define complete EBNF grammar for 1978 Applesoft BASIC standard
- **Acceptance Criteria**:
  - Grammar file `grammar/applesoft.ebnf` exists and is syntactically valid
  - Grammar covers all statements, functions, operators, and data types
  - Grammar successfully parses all sample programs from `v1_legacy/samples/`
  - Grammar rejects invalid syntax with clear error messages

**FR-1.2: Parser Implementation**
- **Priority**: P0 (Critical)
- **Description**: Implement parser using Lark library that can parse valid Applesoft programs
- **Acceptance Criteria**:
  - Parser loads and validates EBNF grammar
  - Parser produces structured parse trees (AST)
  - Parser handles all 1978 Applesoft BASIC syntax
  - Parser supports case-insensitive keywords and identifiers
  - Parser handles optional whitespace correctly

**FR-1.3: Grammar Validation**
- **Priority**: P1 (High)
- **Description**: Validate grammar against known-good Applesoft programs
- **Acceptance Criteria**:
  - Test suite validates grammar against sample programs
  - All edge cases documented in grammar spec are tested
  - Grammar handles variable naming rules (first 2 chars significant)
  - Grammar distinguishes scalar vs array variables correctly

#### Technical Requirements

**TR-1.1: Technology Stack**
- **Parser Library**: Lark (Python)
- **Grammar Format**: EBNF (Extended Backus-Naur Form)
- **Language**: Python 3.9+
- **Testing**: pytest

**TR-1.2: Grammar Structure**
- Lexical tokens (terminals) defined first
- Syntax rules (non-terminals) organized logically
- Operator precedence clearly defined
- Extensibility points identified for Phase 2

**TR-1.3: Error Handling**
- Partial parsing for better error messages
- Multiple error reporting when possible
- Clear error messages with line numbers
- Syntax error recovery

#### Out of Scope (Phase 1)

- Macro system (`#define`)
- Label support (`.label_name`)
- Long variable names
- Unicode string literals
- Include directives (`#include`)
- Code transformation/optimization
- Code generation

### Phase 2: Modern Extensions

**Objective**: Extend grammar with modern development features while maintaining compatibility

#### Functional Requirements

**FR-2.1: Macro System**
- **Priority**: P0 (Critical)
- **Description**: Support `#define` directives for code macros
- **Acceptance Criteria**:
  - Macros defined with `#define MACRO_NAME value`
  - Macros expanded before parsing
  - Macro expansion preserves Applesoft BASIC syntax
  - Nested macros supported

**FR-2.2: Label Support**
- **Priority**: P0 (Critical)
- **Description**: Support label-based control flow (`.label_name`)
- **Acceptance Criteria**:
  - Labels defined with `.label_name` syntax
  - Labels map to line numbers during compilation
  - `GOTO .label_name` and `GOSUB .label_name` supported
  - Labels resolve to valid line numbers

**FR-2.3: Long Variable Names**
- **Priority**: P1 (High)
- **Description**: Support variable names longer than 2 characters with frequency optimization
- **Acceptance Criteria**:
  - Variable names up to 238 characters supported
  - Automatic optimization to short names based on frequency
  - Maintains compatibility with 1978 standard (first 2 chars significant)
  - Variable renaming preserves program semantics

**FR-2.4: Unicode Support**
- **Priority**: P2 (Medium)
- **Description**: Support Unicode string literals in source code
- **Acceptance Criteria**:
  - Unicode strings converted to Apple II character set
  - Fallback handling for unsupported characters
  - Preserves ASCII compatibility

**FR-2.5: Include Directives**
- **Priority**: P1 (High)
- **Description**: Support `#include` for modular code organization
- **Acceptance Criteria**:
  - `#include "filename"` syntax supported
  - Circular include detection
  - Include path resolution
  - Included files merged before parsing

### Phase 3: Compiler Implementation

**Objective**: Implement full compiler pipeline (parse → transform → generate)

#### Functional Requirements

**FR-3.1: Preprocessor**
- **Priority**: P0 (Critical)
- **Description**: Implement preprocessing phase (macros, includes, labels)
- **Acceptance Criteria**:
  - Macro expansion
  - Include file resolution and merging
  - Label-to-line-number mapping
  - Variable name optimization

**FR-3.2: Transformer**
- **Priority**: P0 (Critical)
- **Description**: Transform AST with modern features to standard Applesoft
- **Acceptance Criteria**:
  - Label resolution to line numbers
  - Long variable name optimization
  - Unicode string conversion
  - Code cleanup and optimization

**FR-3.3: Code Generator**
- **Priority**: P0 (Critical)
- **Description**: Generate valid Applesoft BASIC code from transformed AST
- **Acceptance Criteria**:
  - Generates valid 1978 Applesoft BASIC syntax
  - Preserves program semantics
  - Optimized line number assignment
  - Proper formatting for readability

**FR-3.4: CLI Interface**
- **Priority**: P1 (High)
- **Description**: Command-line interface for compilation
- **Acceptance Criteria**:
  - `applejack input.bas output.bas` command
  - Error reporting to stderr
  - Exit codes for success/failure
  - Verbose mode for debugging

---

## User Stories

### Phase 1 User Stories

**US-1.1: Grammar Validation**
- **As a** developer
- **I want** to validate that my Applesoft BASIC program follows the 1978 standard
- **So that** I can ensure compatibility with Apple II systems

**US-1.2: Syntax Error Detection**
- **As a** developer
- **I want** clear error messages when my code has syntax errors
- **So that** I can quickly identify and fix issues

**US-1.3: Parse Tree Generation**
- **As a** developer
- **I want** the compiler to generate structured parse trees
- **So that** future transformations can be implemented

### Phase 2 User Stories

**US-2.1: Macro Usage**
- **As a** developer
- **I want** to define macros for repeated code patterns
- **So that** I can reduce code duplication and improve maintainability

**US-2.2: Label-Based Control Flow**
- **As a** developer
- **I want** to use labels instead of line numbers for control flow
- **So that** my code is more readable and maintainable

**US-2.3: Long Variable Names**
- **As a** developer
- **I want** to use descriptive variable names longer than 2 characters
- **So that** my code is self-documenting and easier to understand

**US-2.4: Modular Code Organization**
- **As a** developer
- **I want** to organize my code into multiple files using includes
- **So that** I can build larger, more maintainable programs

### Phase 3 User Stories

**US-3.1: Compilation Pipeline**
- **As a** developer
- **I want** to compile my modern Applesoft code to standard Applesoft
- **So that** I can run it on Apple II systems

**US-3.2: Code Optimization**
- **As a** developer
- **I want** the compiler to optimize variable usage
- **So that** my programs use memory efficiently

---

## Technical Architecture

### System Components

1. **Grammar Layer** (`grammar/applesoft.ebnf`)
   - EBNF definition of 1978 Applesoft BASIC
   - Extensible for Phase 2 features

2. **Parser Layer** (`src/parser/`)
   - Lark-based parser
   - AST generation
   - Error handling

3. **Preprocessor Layer** (`src/preprocessor/`)
   - Macro expansion
   - Include resolution
   - Label mapping

4. **Transformer Layer** (`src/transformer/`)
   - AST transformation
   - Variable optimization
   - Code cleanup

5. **Generator Layer** (`src/generator/`)
   - Code generation
   - Line number assignment
   - Formatting

### Data Flow

```
Source Code (Applejack)
    ↓
Preprocessor (macros, includes, labels)
    ↓
Parser (EBNF grammar → AST)
    ↓
Transformer (modern features → standard Applesoft)
    ↓
Generator (AST → Applesoft BASIC code)
    ↓
Output (Standard Applesoft BASIC)
```

### Technology Decisions

- **Parser**: Lark (Python) - Modern, flexible parser generator
- **Grammar Format**: EBNF - Standard, readable format
- **Language**: Python 3.9+ - Matches existing codebase
- **Testing**: pytest - Industry standard for Python

---

## Non-Functional Requirements

### Performance

- **Compilation Time**: < 1 second for programs < 10,000 lines
- **Memory Usage**: < 100MB for typical programs
- **Error Recovery**: Partial parsing with multiple error reporting

### Quality

- **Test Coverage**: > 90% for core functionality
- **Error Messages**: Clear, actionable with line numbers
- **Documentation**: Comprehensive grammar documentation

### Compatibility

- **Input**: Applejack V2 syntax (Phase 2) and standard Applesoft BASIC
- **Output**: Valid 1978 Applesoft BASIC standard
- **Platform**: macOS, Linux, Windows (Python 3.9+)

### Maintainability

- **Code Organization**: Modular structure with clear separation of concerns
- **Extensibility**: Grammar designed for Phase 2 extensions
- **Documentation**: Inline comments and comprehensive specs

---

## Success Criteria

### Phase 1 Success Criteria

1. ✅ `grammar/applesoft.ebnf` file exists and is syntactically valid
2. ✅ Grammar parses all statements from 1978 Applesoft BASIC standard
3. ✅ Grammar successfully parses sample programs from `v1_legacy/samples/`
4. ✅ Grammar produces structured parse trees (AST) suitable for transformation
5. ✅ Grammar rejects invalid syntax with clear error messages
6. ✅ Grammar is documented with comments explaining each rule
7. ✅ Test suite validates grammar against known-good Applesoft programs

### Phase 2 Success Criteria

1. ✅ Extended grammar (`grammar/applejack.ebnf`) supports all Phase 2 features
2. ✅ Preprocessor handles macros, includes, and labels correctly
3. ✅ Variable optimization produces efficient code
4. ✅ All Phase 1 tests pass with extended grammar

### Phase 3 Success Criteria

1. ✅ Full compilation pipeline works end-to-end
2. ✅ Generated code runs correctly on Apple II systems
3. ✅ CLI interface is user-friendly and robust
4. ✅ Performance meets requirements (< 1s for typical programs)

---

## Risks and Mitigations

### Technical Risks

**Risk 1: Grammar Complexity**
- **Impact**: High - Core functionality depends on grammar
- **Probability**: Medium
- **Mitigation**: Incremental development, comprehensive testing, reference documentation

**Risk 2: Applesoft Standard Ambiguity**
- **Impact**: Medium - May misinterpret standard requirements
- **Probability**: Medium
- **Mitigation**: Reference official 1978 manual, test with real programs, community validation

**Risk 3: Performance Issues**
- **Impact**: Low - May affect user experience
- **Probability**: Low
- **Mitigation**: Profile early, optimize critical paths, set performance targets

### Project Risks

**Risk 4: Scope Creep**
- **Impact**: Medium - May delay core features
- **Probability**: Medium
- **Mitigation**: Strict phase boundaries, prioritize P0 features, defer enhancements

**Risk 5: Testing Coverage**
- **Impact**: High - Bugs may reach users
- **Probability**: Medium
- **Mitigation**: Comprehensive test suite, edge case documentation, automated testing

---

## Dependencies

### External Dependencies

- **Lark Parser Library**: Python package for parsing
- **pytest**: Testing framework
- **Python 3.9+**: Runtime environment

### Internal Dependencies

- **Phase 1 → Phase 2**: Grammar foundation required before extensions
- **Phase 2 → Phase 3**: Extended grammar required before compiler implementation
- **Sample Programs**: Required for validation and testing

### Documentation Dependencies

- **1978 Applesoft BASIC Reference Manual**: Primary specification source
- **V1 Legacy Code**: Reference implementation and test cases

---

## Out of Scope

### Explicitly Out of Scope (All Phases)

- **Runtime Implementation**: Applejack does not execute programs, only compiles them
- **IDE Integration**: No editor plugins or IDE support (future consideration)
- **Debugging Tools**: No debugger or debugging support
- **Performance Profiling**: No runtime performance analysis
- **Code Formatting**: Basic formatting only, not full code beautification
- **Documentation Generation**: No automatic documentation from code

### Future Considerations (Post-V2)

- **Additional Language Extensions**: More modern features beyond Phase 2
- **Optimization Passes**: Advanced code optimization
- **Cross-Platform Support**: Compilation for other 8-bit platforms
- **Interactive Development**: REPL or interactive mode

---

## Timeline and Milestones

### Phase 1: Grammar Foundation (Current)

**Target Completion**: TBD  
**Deliverables**:
- `grammar/applesoft.ebnf` - Complete grammar definition
- Parser implementation
- Test suite
- Documentation

**Milestones**:
- [ ] Grammar file created and validated
- [ ] Parser implemented and tested
- [ ] Sample programs parse successfully
- [ ] Test suite complete
- [ ] Documentation complete

### Phase 2: Modern Extensions (Future)

**Target Completion**: TBD  
**Deliverables**:
- `grammar/applejack.ebnf` - Extended grammar
- Preprocessor implementation
- Variable optimization
- Test suite updates

**Milestones**:
- [ ] Extended grammar defined
- [ ] Preprocessor implemented
- [ ] All Phase 2 features working
- [ ] Tests passing

### Phase 3: Compiler Implementation (Future)

**Target Completion**: TBD  
**Deliverables**:
- Full compiler pipeline
- CLI interface
- Code generator
- End-to-end tests

**Milestones**:
- [ ] Transformer implemented
- [ ] Code generator implemented
- [ ] CLI interface complete
- [ ] End-to-end compilation working

---

## Appendices

### Appendix A: Reference Materials

- Apple II Applesoft BASIC Reference Manual (1978)
- Applesoft BASIC Programmer's Reference Card
- V1 Legacy codebase (`v1_legacy/`)
- Sample programs (`v1_legacy/samples/`)

### Appendix B: Glossary

- **AST**: Abstract Syntax Tree
- **EBNF**: Extended Backus-Naur Form
- **Applesoft BASIC**: The BASIC interpreter for Apple II computers (1978 standard)
- **Lark**: Python parsing library
- **Preprocessor**: Phase that handles macros, includes, and labels before parsing
- **Transformer**: Phase that converts modern features to standard Applesoft
- **Generator**: Phase that produces final Applesoft BASIC code

### Appendix C: Related Documents

- `docs/phase-1-applesoft-grammar-spec.md` - Detailed grammar specification
- `README.md` - Project overview
- Test files in `test/` directory

---

**Document Status**: Draft  
**Last Updated**: 2025-12-05  
**Next Review**: TBD  
**Approved By**: TBD


