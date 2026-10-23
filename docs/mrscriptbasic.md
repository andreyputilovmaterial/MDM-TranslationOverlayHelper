# mrScriptBasic / `.mrs` scripts

This tool generates `.mrs` scripts — the scripting format used by the IBM/Unicom Data
Model toolchain (MDM/MDD). IBM/Unicom calls the language **mrScriptBasic**.

## What it is

mrScriptBasic is a programming language based on Microsoft **Visual Basic** and
**VBScript** that provides scriptable access to IBM/Unicom Intelligence components (the
Data Model, the Tables object model, and so on).

`.mrs` files are the pure-mrScriptBasic script type. The other script types — `.dms`
(data-management) and `.mdd` (interview) — embed mrScriptBasic in their non-metadata
sections. mrScriptMetadata is a separate language and cannot be embedded in `.mrs`
files.

On top of plain VBScript, mrScriptBasic adds native support for the things survey data
needs: categorical variables, expression evaluation on categoricals, a
market-research-oriented function library, object-collection iteration, dynamic property
expansion, and an enhanced `Err` object.

## Key differences from VBScript / VB

### Variables

- **Explicit declaration by default.** Declare variables with `Dim`. Add
  `Option Implicit` to allow implicit declaration (not recommended). VBScript is the
  other way round.
- Script variables are **not** visible inside `Function`/`Sub` procedures by default.
  Add `Option GlobalVariables` to make them visible (VBScript-style).

### Arrays and categoricals

- Array variables use **square brackets `[]`**, not parentheses `()`:

  | | mrScriptBasic | VBScript |
  | --- | --- | --- |
  | 1-D, 10 elements | `Dim myArray[10]` | `Dim myArray(10)` |
  | 2-D, 5×10 | `Dim myArray[5][10]` | `Dim myArray(5, 10)` |
  | dynamic | `Dim myArray[]` | `Dim myArray()` |
  | array parameter | `Sub MySub(myArray[])` | `Sub MySub(myArray)` |

- Unless a variable is `Dim`-declared as an array, a value assigned with `{...}` is a
  **categorical**, and its elements are read-only.

### Objects and collections

- Reference a collection member through its default property (usually `Item`) with `[]`:
  `MyDocument.Fields["age"].Label` (not `Fields("age").Label`). This matches MDM full
  names.
- Pass object-property parameters in brackets, one pair per parameter:
  `Labels["Label"].Text["Question"]["ENU"]` (VBScript: `Text("Question", "ENU")`).
- A call **always** requires parentheses, even for a `Sub` that returns nothing, and the
  `Call` keyword is not valid syntax: `MdmDoc.Save("C:\...")`.
- mrScriptBasic does **not** expand an object's default method — write the method name
  explicitly.
- Clear an object reference with `Null` (not `Nothing`); test with `IsNullObject()`.

### Operators

- **String concatenation is `+`, not `&`.** With `+`, every operand must be `Text`; use
  `CText()` or `MakeString()` to convert.
- **Multi-line strings** start with `"!` and end with `!"`.
- **Integer arithmetic stays integer:** `12/5` is `2` (both operands are `Long`). Use
  `12.0/5.0` to get `2.4`.
- `And`, `Not`, `Or`, `Xor` are **not** bitwise operators; use the bitwise functions from
  the Function Library (e.g. `BitOr`).
- **`And` and `Or` have equal precedence** — an expression using both is evaluated
  left-to-right rather than giving `And` higher precedence. This is unusual, so use
  parentheses to make the intended grouping explicit.

### Control flow and statements

- `While ... End While` (not `Wend`).
- You **cannot** put multiple statements on one line, nor a `GoTo` label and a statement
  on the same line.

### Error handling

- `On Error Goto <label>` adds an error-handling section; put an `Exit` immediately
  before it.
- The `Err` object exposes the **description and line number** (`Err.Description`,
  `Err.LineNumber`).
- `Err.Clear` runs automatically on `On Error Resume Next`, but **not** on
  `Exit Sub`/`Exit Function` (unlike VBScript).

### Functions

mrScriptBasic uses the IBM/Unicom **Function Library** rather than the VBScript/VB
built-ins, so some familiar functions are missing or renamed. Some functions are
zero-based (`Find`, `Mid`, and others), whereas classic BASIC/VBS is typically one-based.

### Comments and preprocessor

- Comments start with a single quote `'` (as in VBS), so a "suppressed" line in a
  generated script is one whose leading character is `'`.
- **Multi-line comments** start with `'!` and end with `!'`.
- A C-style preprocessor is supported (an old implementation): `#include`, `#define`,
  `#if`, `#if defined(...)`. Text comparison in preprocessor `#if` statements is **not**
  supported.

## Running `.mrs` scripts

`.mrs` files can be run in IBM/Unicom Professional (open the file, press F5) or from the
command line with the mrScript Command Line Runner (`mrScriptCL`), e.g.
`mrScriptCl Functions.mrs`. The runner's `/v` option prints the final values of all
variables.

## Why this matters here

`generate_overlays_script` emits `.mrs` text that writes updated translation overlays
back into an MDD via statements like
`objMDM.Fields[...].Labels["Label"].Text["Question"]["<lang>"] = "..."`. That script is
then run inside the IBM/Unicom tooling. The quirks above matter both for producing valid
output and for understanding how the generated script will behave.
