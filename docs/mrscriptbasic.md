# mrScriptBasic / `.mrs` scripts

This tool generates `.mrs` scripts — the scripting format used by the IBM/Unicom Data
Model toolchain (MDM/MDD). IBM/Unicom calls the language **mrScriptBasic**. It is
effectively VBS (Basic) with a number of modifications. The differences that matter when
reading or writing generated scripts:

1. **Function calls always require parentheses** — `echo("something")`, not
   `echo "something"`.
2. **String concatenation uses `+`, not `&`** (unlike classic VBS/VBA).
3. **Some functions are zero-based** — `find()`, `mid()`, and others, whereas classic
   BASIC/VBS is typically one-based.
4. **Native access to the Document Object Model (MDD documents), weighting, and other
   IBM/Unicom tools** is built into the language.
5. **A C-style preprocessor** is supported (an old implementation): `#define`, `#if`,
   and `#if defined(...)` are common. Text comparison in preprocessor `#if` statements
   is **not** supported.

Comments start with a single quote `'` (as in VBS), so a "suppressed" line in a
generated script is simply one whose leading character is `'`.

## Why this matters here

`generate_overlays_script` emits `.mrs` text that writes updated translation overlays
back into an MDD via statements like
`objMDM.Fields[...].Labels["Label"].Text["Question"]["<lang>"] = "..."`. That script is
then run inside the IBM/Unicom tooling. The quirks above matter both for producing valid
output and for understanding how the generated script will behave.
