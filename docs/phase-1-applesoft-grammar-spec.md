# Phase 1: Strict Applesoft Grammar Specifications

**Project:** Applejack V2  
**Phase:** Grammar Definition  
**Status:** Planning  
**Date:** 2025-12-05

---

## Overview

Phase 1 establishes the foundation for the Applejack V2 compiler by defining a strict, formal grammar for the 1978 Applesoft BASIC standard. This grammar will be implemented using EBNF (Extended Backus-Naur Form) and parsed using the Lark parser library in Python.

## Objectives

1. **Define Strict Applesoft Grammar** - Create `grammar/applesoft.ebnf` that precisely captures the 1978 Applesoft BASIC standard
2. **Establish Grammar Foundation** - Ensure the grammar is complete, unambiguous, and testable
3. **Enable Future Extensions** - Design grammar structure to support Phase 2 extensions (macros, labels, long variables, Unicode)

---

## Grammar Scope: 1978 Applesoft BASIC Standard

### Core Language Elements

#### 1. **Program Structure**
- Line numbers (0-63999)
  - **Note**: Line numbers can be floating-point but are truncated to integers
    - `GOTO 10.1` → goes to line 10
    - `GOTO 10.999` → goes to line 10
    - `GOTO 10` → goes to line 10
- Line continuation (none, no continuation character in Applesoft)
- Program termination (END, BREAK, or last line completes execution)

#### 2. **Data Types**
- **Numeric** (floating-point): All numbers stored as floating-point
  - **Important**: Applesoft stores ALL numbers as floating-point internally
  - Integer literals: `-32768` to `32767` (stored as float)
  - Floating-point: Scientific notation support (`1.23E+5`)
  - **Truncation behavior**: Functions/statements expecting integers truncate (not round) the decimal portion
    - Example: `GOTO 10.1`, `GOTO 10.999`, and `GOTO 10` all go to line 10
    - Example: `INT(10.9)` returns `10` (truncates, doesn't round)
- **Integer**: Integer variables (suffix `%`)
  - Integer variables: `A%`, `B%`, `COUNT%`, etc.
  - Range: -32767 to 32767 inclusive
  - Values outside range will cause overflow/error
  - Distinct from numeric variables: `A%` and `A` are different variables
- **String**: Character sequences
  - String literals: `"text"` (double quotes only, straight quotes not smart quotes)
  - String variables: `A$`, `NAME$`
- **Arrays**: Multi-dimensional arrays (no enforced upper limit)
  - One-dimensional: `A(10)`, `A%(10)`, `A$(10)`
  - Two-dimensional: `B(5,5)`, `B%(5,5)`, `B$(5,5)`
  - Multi-dimensional: `C(5,5,5)`, `D(3,3,3,3)`, etc.
  - **Practical limit**: ~88 dimensions (due to memory constraints, not language specification)
  - Numeric arrays: `A(10)`, `B(5,5)`, `C(3,3,3)`
  - Integer arrays: `A%(10)`, `B%(5,5)`
  - String arrays: `A$(10)`, `B$(5,5)`

#### 3. **Variables**
- **Numeric variables** (floating-point): Letter followed by letters/digits (`A`, `B`, `A1`, `B2`, `AB`, `ABC`, etc.)
- **Integer variables**: Letter followed by letters/digits, ending with `%` (`A%`, `B%`, `A1%`, `COUNT%`, etc.)
  - Can only hold integer values between -32767 and 32767 inclusive
  - Distinct from numeric variables: `A%` and `A` are different variables
  - Values outside range will cause overflow/error
- **String variables**: Letter followed by letters/digits, ending with `$` (`A$`, `B$`, `A1$`, `NAME$`, etc.)
- **Scalar vs Array**: Scalar variables and arrays with the same name are distinct and can coexist
  - Example: `A$` (scalar) and `A$` (array accessed as `A$(index)`) are different
  - Example: `A` (scalar) and `A` (array accessed as `A(index)`) are different
  - Example: `A%` (scalar integer) and `A%` (array accessed as `A%(index)`) are different
  - Grammar must distinguish between `A$` (scalar reference) and `A$(5)` (array element)
  - Grammar must distinguish between `A%` (scalar reference) and `A%(5)` (array element)
  - **Future extensibility**: This distinction supports Phase 2 features like identifier renaming, long variable names, and code transformations
- Variable name rules:
  - First character: letter (A-Z)
  - Subsequent characters: letter or digit
  - Maximum length: 238 characters
  - **Important**: Only the first 2 characters are significant for distinguishing variables
    - `AB`, `ABC`, `ABCDEFG` are all treated as the same variable
    - `A1` and `A12` are the same (first 2 chars: `A1` in both)
    - `A1` and `A1X` are the same (first 2 chars: `A1` in both)
    - `A1` and `A2` are different (first 2 chars: `A1` vs `A2`)
  - Case-insensitive

#### 4. **Operators**

**Arithmetic:**
- `+` (addition)
- `-` (subtraction)
- `*` (multiplication)
- `/` (division)
- `^` (exponentiation)

**Comparison:**
- `=` (equality)
- `<>` or `><` (inequality)
- `<` (less than)
- `>` (greater than)
- `<=` or `=<` (less than or equal)
- `>=` or `=>` (greater than or equal)

**Logical:**
- `AND` (logical AND)
- `OR` (logical OR)
- `NOT` (logical NOT)

#### 5. **Statements**

**Control Flow:**
- `GOTO` line_number
- `GOSUB` line_number / `RETURN`
- `IF` condition `THEN` statement [`:` statement]*
- `IF` condition `THEN` line_number
- `IF` condition `GOTO` line_number (alternative form)
- `FOR` variable `=` start `TO` end [`STEP` increment] / `NEXT` [variable]
- `ON` expression `GOTO` line_list
- `ON` expression `GOSUB` line_list

**Data Manipulation:**
- `LET` variable `=` expression (optional LET keyword - `LET` can be omitted)
- `DIM` array_name(dimensions)
  - One-dimensional: `DIM A(10)` creates array with indices 0-10
  - Two-dimensional: `DIM B(5,5)` creates 6x6 array (0-5, 0-5)
  - Multi-dimensional: `DIM C(3,3,3)` creates 4x4x4 array (0-3, 0-3, 0-3)
  - **No enforced upper limit** on number of dimensions (practical limit ~88 due to memory)
  - Arrays default to 10 elements if not DIM'd (0-10 for one-dim, 0-10,0-10 for two-dim)
- `READ` variable_list (reads from DATA statements)
- `DATA` constant_list (stores constants for READ)
- `RESTORE` (resets DATA pointer to beginning of program)

**Input/Output:**
- `PRINT` [expression_list] [`;`|`,`]
- `?` (shorthand for `PRINT`)
- `PRINT` behavior:
  - **Implicit semicolons**: Semicolons are implied between expressions when omitted
    - `?"Hello, ";NM$;"!"` and `?"Hello, "NM$"!"` are equivalent
    - Semicolons are optional between expressions
  - **Explicit semicolons**: Sometimes required to prevent variable name ambiguity
    - `?N;A$` requires semicolon (without it, `NA$` would be parsed as single variable)
    - `?N A$` would be incorrect (parsed as `NA$` variable)
  - **Multiple semicolons**: Multiple semicolons are valid and equivalent
    - `?A$;" ";B$` and `?;;;A$" ";B$` are equivalent
  - **Semicolon `;` at end**: No newline (next PRINT continues on same line)
  - **Comma `,` at end**: Tab to next print zone (14 characters)
  - **No separator at end**: Newline after printing
  - **Empty `PRINT` or `?`**: Prints blank line
  - **String concatenation**: Strings can be concatenated implicitly in PRINT
    - `?"HELLO WORLD"` and `?"HELLO ""WORLD"` are equivalent
    - `?A$;" ";B$` concatenates with space between
- `INPUT` [prompt_string `;`] variable_list
- `GET` variable (waits for single character input)
  - **Implementation note**: Using `GET` with numeric variables (int/float) is not recommended
  - If user enters non-numeric character, program will produce an error
  - Best practice: Use `GET` with string variables (`GET A$`) to safely handle any input
- `POKE` address, value
- `PEEK` (address)

**Program Control:**
- `END`
- `STOP`
- `CONT`
- `REM` comment_text
- `NEW`
- `RUN` [line_number]
- `LIST` [line_range]

**Graphics/Display:**
- `HOME`
- `CLEAR`
- `TEXT`
- `GR`
- `COLOR=` expression
- `PLOT` x, y
- `HLIN` x1, x2 `AT` y
- `VLIN` y1, y2 `AT` x
- `VTAB` row
- `HTAB` column
- `INVERSE`
- `NORMAL`
- `FLASH`

#### 6. **Functions**

**Numeric Functions:**
- `ABS(x)`, `SGN(x)`, `INT(x)`, `SQR(x)`
  - **Note**: `INT(x)` truncates (doesn't round) - `INT(10.9)` = `10`
- `SIN(x)`, `COS(x)`, `TAN(x)`, `ATN(x)`
- `EXP(x)`, `LOG(x)`
- `RND(x)`, `RND(1)` for random number
- `LEN(string)`, `ASC(string)`, `CHR$(code)`
  - **Note**: `CHR$(code)` truncates code to integer before conversion
- `VAL(string)`, `STR$(number)`

**String Functions:**
- `LEFT$(string, n)`, `RIGHT$(string, n)`, `MID$(string, start, [length])`
- `LEN(string)`

**Array Functions:**
- Array access: `A(index)` or `A(row, col)` or `A(dim1, dim2, dim3, ...)`
- Multi-dimensional arrays supported (no enforced upper limit on dimensions)

#### 7. **Expressions**
- Arithmetic expressions with operator precedence
- Parenthesized sub-expressions
- Function calls
- Variable references
- Literal values

#### 8. **Statement Separators**
- Multiple statements per line separated by `:` (colon)
- Example: `IF M < T THEN GOSUB .drawFromStock : GOSUB .placeFaceDown`
- Allows combining multiple statements on a single line number

---

## Reserved Words and Keywords

All keywords listed below are **reserved** and cannot be used as variable names. The grammar must recognize these as keywords and prevent their use as identifiers.

### Statement Keywords

**Control Flow:**
- `GOTO`, `GOSUB`, `RETURN`, `IF`, `THEN`, `FOR`, `NEXT`, `ON`, `STEP`, `TO`

**Data Manipulation:**
- `LET` (optional, can be omitted), `DIM`, `READ`, `DATA`, `RESTORE`

**Input/Output:**
- `PRINT`, `INPUT`, `GET`, `POKE`, `PEEK`
- `?` (shorthand for `PRINT` - also reserved)

**Program Control:**
- `END`, `STOP`, `CONT`, `REM`, `NEW`, `RUN`, `LIST`

**Graphics/Display:**
- `HOME`, `CLEAR`, `TEXT`, `GR`, `COLOR`, `PLOT`, `HLIN`, `VLIN`, `VTAB`, `HTAB`, `INVERSE`, `NORMAL`, `FLASH`
- `AT` (used with HLIN/VLIN)

### Function Names

**Numeric Functions:**
- `ABS`, `SGN`, `INT`, `SQR`, `SIN`, `COS`, `TAN`, `ATN`, `EXP`, `LOG`, `RND`, `LEN`, `ASC`, `CHR$`, `VAL`, `STR$`

**String Functions:**
- `LEFT$`, `RIGHT$`, `MID$`, `LEN` (also numeric), `ASC`, `CHR$`, `VAL`, `STR$`

**Note:** Functions ending with `$` return strings. Functions without `$` return numeric values.

### Logical Operators

- `AND`, `OR`, `NOT`

**Note:** These are operators but are also reserved words and cannot be used as variable names.

### Special Tokens

- `?` - Shorthand for `PRINT` (reserved)
- `:` - Statement separator (not a keyword, but special syntax)
- `;` - PRINT separator (not a keyword, but special syntax)
- `,` - PRINT zone separator (not a keyword, but special syntax)

### Grammar Requirements

- All keywords are **case-insensitive** (`GOTO`, `goto`, `Goto` are equivalent)
- Keywords cannot be used as variable names
- Grammar must distinguish between keywords and identifiers
- Lexical analyzer must recognize keywords before parsing identifiers

### Validation Note

This list is compiled from the statements and functions documented in this specification. During grammar implementation, this list should be validated against the official Applesoft BASIC Reference Manual (1978) to ensure completeness.

---

## Grammar File Structure

### File: `grammar/applesoft.ebnf`

The EBNF grammar should be organized into logical sections:

1. **Lexical Tokens** (terminals)
   - Numbers (integer, float, scientific)
   - Strings (quoted)
   - Identifiers (variables - see Reserved Words section for keywords)
   - Keywords (see Reserved Words and Keywords section above)
   - Operators
   - Punctuation (including `:` statement separator, `?` PRINT shorthand)

2. **Syntax Rules** (non-terminals)
   - Program structure
   - Statements (including statement lists with `:` separator)
   - Expressions
   - Functions
   - Data types

3. **Precedence Rules**
   - Operator precedence (see Operator Precedence section below)
   - Expression evaluation order (left-to-right)

## Operator Precedence

Applesoft BASIC operator precedence (highest to lowest):

1. **Parentheses** `()` - Highest precedence
2. **Exponentiation** `^`
3. **Unary operators** `-` (negation), `NOT`
4. **Multiplication/Division** `*`, `/`
5. **Addition/Subtraction** `+`, `-`
6. **Comparison** `=`, `<>`, `<`, `>`, `<=`, `>=`
7. **Logical AND** `AND`
8. **Logical OR** `OR` - Lowest precedence

**Evaluation Order:**
- Left-to-right for operators of equal precedence
- Parentheses override precedence
- Function calls evaluated before operators

## Expression Evaluation Details

- **Left-to-right evaluation** for operators of equal precedence
- **Short-circuit evaluation**: NOT supported (all operands evaluated)
- **Number storage**: ALL numbers stored as floating-point internally
  - Integer literals are stored as floats
  - No separate integer type
- **Integer truncation**: When integer values are needed, decimal portion is truncated (not rounded)
  - Examples: `GOTO 10.9` → line 10, `INT(10.9)` → `10`, `A(10.9)` → `A(10)`
- **Type coercion**: Automatic conversion between numeric and string types in certain contexts
- **Array bounds**: Arrays are zero-based in Applesoft (first element is index 0)
  - Array indices are truncated: `A(10.9)` accesses `A(10)`
- **String indexing**: Strings are 1-based (first character is position 1)
  - String indices are truncated: `MID$(A$, 10.9, 5)` uses position 10

## String Handling

- **String literals**: Double quotes only `"text"` (straight quotes, not smart/curly quotes)
  - Single quotes `'text'` are NOT supported in Applesoft
- **Escape sequences**: Not supported in 1978 standard (no `\n`, `\t`, etc.)
- **String concatenation**: Use `+` operator (e.g., `A$ + B$`)
- **String functions**: `LEFT$`, `RIGHT$`, `MID$`, `LEN`, `ASC`, `CHR$`, `VAL`, `STR$`
- **Special characters**: All ASCII characters supported (within Apple II character set)

---

## Grammar Requirements

### Completeness
- ✅ Cover all 1978 Applesoft BASIC statements
- ✅ Support all data types (numeric, string, arrays)
- ✅ Handle all operators and functions
- ✅ Support all control flow constructs

### Correctness
- ✅ Match 1978 Applesoft BASIC behavior exactly
- ✅ Handle edge cases (empty statements, missing operands)
- ✅ Support Applesoft's line number system
- ✅ Respect Applesoft's variable naming rules (up to 238 chars, first 2 chars significant)

### Testability
- ✅ Grammar should parse valid Applesoft programs
- ✅ Grammar should reject invalid syntax
- ✅ Grammar should produce parse trees suitable for transformation

### Extensibility
- ✅ Structure should allow Phase 2 extensions
- ✅ Separate core grammar from extension points
- ✅ Design for macro expansion points
- ✅ Design for label-to-line-number mapping

---

## Reference Materials

### Primary Sources
- Apple II Applesoft BASIC Reference Manual (1978)
- Applesoft BASIC Programmer's Reference Card
- Existing V1 codebase samples (for validation)

### Sample Programs for Testing
- `v1_legacy/samples/klondike/klondike.txt` - Complex game with macros, labels, subroutines
- `v1_legacy/samples/continuity/continuity.txt` - Simple program with includes

---

## Success Criteria

Phase 1 is complete when:

1. ✅ `grammar/applesoft.ebnf` file exists and is syntactically valid EBNF
2. ✅ Grammar parses all statements from 1978 Applesoft BASIC standard
3. ✅ Grammar successfully parses sample programs from `v1_legacy/samples/`
4. ✅ Grammar produces structured parse trees (AST) suitable for transformation
5. ✅ Grammar rejects invalid syntax with clear error messages
6. ✅ Grammar is documented with comments explaining each rule
7. ✅ Test suite validates grammar against known-good Applesoft programs

---

## Next Steps After Phase 1

Once the strict Applesoft grammar is complete:

1. **Phase 2**: Define `grammar/applejack.ebnf` extending the base grammar with:
   - Macros (`#define`)
   - Labels (`.label_name`)
   - Long variable names (with frequency optimization)
   - Unicode string literals
   - Include directives (`#include`)

2. **Phase 3**: Implement parser, transformer, and code generator in `src/`

---

## Questions to Resolve - DECISIONS

1. **Line Continuation**: ✅ **DECIDED: Handle in preprocessing**
   - Keep grammar strict to 1978 Applesoft standard (no line continuation)
   - If line continuation is needed in Phase 2, handle it in preprocessing/transformation layer
   - Grammar will not support implicit or explicit line continuation

2. **Case Sensitivity**: ✅ **DECIDED: Use Lark's case-insensitive mode**
   - Leverage Lark's built-in case-insensitive parsing
   - Grammar rules will be case-insensitive by default
   - Keywords and variables can be uppercase, lowercase, or mixed case

3. **Whitespace**: ✅ **DECIDED: Grammar handles optional whitespace**
   - Whitespace is truly optional in Applesoft (e.g., "PRINTA" and "PRINT A" are equivalent)
   - Grammar rules will make whitespace optional throughout
   - This matches Applesoft's whitespace-agnostic behavior

4. **Error Recovery**: ✅ **DECIDED: Partial parsing for better error messages**
   - Grammar will attempt to parse as much as possible
   - Report multiple errors when encountered
   - Better developer experience for debugging invalid syntax

5. **Grammar Validation**: ✅ **DECIDED: Combination approach**
   - Use Lark's built-in validation (test grammar by loading it)
   - Write test suite with known-good Applesoft programs
   - Use grammar linters/validators if available
   - Manual testing with sample programs from v1_legacy/samples/

---

## Implementation Notes

### GET Statement Best Practices
- **Avoid numeric variables with GET**: Using `GET` with numeric variables (int/float) is not recommended
- **Error risk**: If user enters non-numeric character, program will produce an error
- **Best practice**: Use `GET` with string variables (`GET A$`) to safely handle any input, then convert if needed

Based on the decisions above, the grammar implementation should:

1. **Lark Configuration:**
   - Enable case-insensitive mode for keywords and identifiers
   - Configure whitespace handling to be optional throughout
   - Enable error recovery/partial parsing for better error messages

2. **Grammar Structure:**
   - No line continuation support (strict 1978 standard)
   - Whitespace optional in all rules (matches Applesoft behavior)
   - Case-insensitive keyword and identifier matching

3. **Testing Strategy:**
   - Use Lark's grammar validation during development
   - Test against known-good programs from v1_legacy/samples/
   - Validate parse tree structure for correctness
   - Test error handling with invalid syntax

4. **Preprocessing Considerations:**
   - Line continuation (if needed in Phase 2) will be handled in preprocessing
   - Keep grammar layer focused on pure Applesoft syntax

---

## Edge Cases and Special Syntax

### Statement Separators
- Multiple statements per line: `statement : statement : statement`
- Colon `:` is the statement separator
- Can combine any statements: `PRINT "A" : GOTO 100 : PRINT "B"`

### IF-THEN Variations
- `IF condition THEN statement` - Single statement
- `IF condition THEN statement : statement` - Multiple statements
- `IF condition THEN line_number` - GOTO on condition
- `IF condition GOTO line_number` - Alternative syntax

### PRINT Statement Variations
- `PRINT` or `?` - Blank line
- `PRINT expr` - Print with newline
- `PRINT expr;` - Print without newline (continues on same line)
- `PRINT expr,` - Print with tab to next zone
- `PRINT expr1; expr2` - Print multiple items (semicolon optional between expressions)
- `PRINT expr1, expr2` - Print with tab between items
- **Implicit semicolons**: `?"Hello, "NM$"!"` (semicolon implied between `"Hello, "` and `NM$`)
- **Explicit semicolons required**: `?N;A$` (prevents parsing as `NA$` variable)
- **Multiple semicolons**: `?;;;A$" ";B$` (multiple semicolons are valid)
- **String concatenation**: `?"HELLO WORLD"` and `?"HELLO ""WORLD"` are equivalent

### Variable Naming Edge Cases
- Single letter variables: `A`, `B`, `Z` (numeric), `A%`, `B%` (integer), `A$`, `B$` (string)
- Two-character variables: `A1`, `B2`, `Z9` (numeric), `A1%`, `B2%` (integer), `A1$`, `B2$` (string)
- Longer variables: `ABC`, `LONGNAME`, `VERYLONGVARIABLENAME` (up to 238 chars)
- **First 2 characters significant**: Only first 2 chars distinguish variables
  - `AB` and `ABC` are the same variable (both start with `AB`)
  - `A1` and `A12` are the same variable (both start with `A1`)
  - `A1` and `A2` are different variables (first 2: `A1` vs `A2`)
  - `AB` and `AC` are different variables (first 2: `AB` vs `AC`)
- **Type suffixes**: Variables with different suffixes are distinct
  - `A`, `A%`, and `A$` are all different variables
  - `A1`, `A1%`, and `A1$` are all different variables
- Integer variables: `A%`, `A1%`, `COUNT%`, `LONGNAME%` (range: -32767 to 32767)
- String variables: `A$`, `A1$`, `NAME$`, `LONGNAME$`
- Reserved words cannot be used as variables (keywords are reserved)

### Array Access
- Zero-based indexing: `A(0)` is first element
- Can use expressions: `A(I+1)`, `B(X*2, Y+3)`, `C(I+1, J*2, K-1)`
- Multi-dimensional: `A(5)`, `B(5,5)`, `C(3,3,3)`, `D(2,2,2,2)`, etc.
- **No enforced upper limit** on number of dimensions (practical limit ~88)
- No bounds checking in grammar (runtime behavior)
- **Scalar vs Array distinction**: Arrays and scalars with the same name are distinct
  - `A$` (scalar) and `A$(5)` (array element) refer to different variables
  - `A` (scalar) and `A(5)` (array element) refer to different variables
  - `A%` (scalar integer) and `A%(5)` (array element) refer to different variables
  - Grammar must parse `A$` differently from `A$(index)` to distinguish scalar from array
  - Grammar must parse `A%` differently from `A%(index)` to distinguish scalar from array

### Line Number Rules
- Range: 0-63999
- Can be any number in range (floating-point allowed but truncated)
- **Truncation**: Floating-point line numbers are truncated (not rounded)
  - `GOTO 10.1` → line 10
  - `GOTO 10.9` → line 10
  - `GOTO 10.999` → line 10
- Programs don't need sequential line numbers
- GOTO/GOSUB can reference any line number (even if not yet defined)

## Notes

- This is a **strict** grammar - it should not include any Applejack V2 extensions
- The grammar should be **complete** - covering all 1978 Applesoft features
- The grammar should be **testable** - we need to validate it against real programs
- The grammar should be **extensible** - Phase 2 will build upon this foundation
- Whitespace is truly optional in Applesoft - "PRINTA" and "PRINT A" are equivalent
- Statement separator `:` allows multiple statements per line
- `?` is shorthand for `PRINT` and must be supported
- **PRINT statement parsing**: Grammar must handle implicit semicolons and variable name disambiguation
  - Optional semicolons between expressions require careful parsing
  - Must distinguish between `NA$` (single variable) and `N;A$` (two expressions)
  - String concatenation in PRINT requires special handling

---

**Status:** Ready for implementation  
**Assigned To:** TBD (Architect/Developer)  
**Dependencies:** None (foundational phase)  
**Decisions Made:** 2025-12-05 - All 5 questions resolved

