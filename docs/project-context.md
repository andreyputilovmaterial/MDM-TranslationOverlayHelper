# Project context

Living working memory for `MDM-TranslationOverlayHelper`. Read at the start of every
task and update at the end (see `.clinerules/00-project-context.md`).

## What it does

Generates an Excel workbook with the fields, labels and translations of an MDD file for
manual translation workflows (when the translation is done without LI/IPS automation).
If translations are edited in that Excel, it generates an `.mrs` script that writes the
updated translations back to the MDD.

> Writing/updating the MDD is **not** done directly by this tool — it emits an `.mrs`
> (IBM/Unicom Data Model scripting) script that the user runs against the MDD.
> `pywin32` is still required, because reading the MDD (via `mdmreadpy`) drives the
> `MDM.Document` COM object on Windows.

## Pipeline (`launcher.py` programs)

1. `read_mdd` — read MDD → JSON report (`mdmreadpy`; Windows + pywin32 + IBM/Unicom).
2. `report_html` — optional HTML render of the JSON (`mdmreportpy`, vendored inside
   `mdmreadpy`).
3. `prep_mddread_scheme` — patch the JSON scheme for the translation-overlay workflow.
4. `report_excel` — render JSON → `.xlsx` (`mdmexcelreportpy`: pandas + xlsxwriter).
5. `generate_overlays_script` — read the edited `.xlsx` (pandas + openpyxl) and emit the
   `.mrs` script.

## Submodules

- `src/lib/mdmreadpy` — MDD reader producing the JSON report; vendors `mdmreportpy`.
- `src/lib/mdmexcelreportpy` — JSON report → Excel.
- `src_dev_build/lib/pinliner` — build tool that bundles `src/` into a single
  `dist/mdmoverlayhelper_bundle.py`.

## Build

`build.bat` first builds the `mdmreadpy` submodule (regenerating its `GENERATED` files —
`_VERSION.py` and the nested `mdmreportpy` HTML template), then runs pinliner over
`src/` to produce `dist/mdmoverlayhelper_bundle.py`, copies the run `.bat` files plus
`LICENSE`, `README.md` and `requirements.txt` into `dist/`, and finally verifies the
bundle loads with `python dist/mdmoverlayhelper_bundle.py --program done`.

## Generated `.mrs` scripts

`generate_overlays_script` emits mrScriptBasic (`.mrs`) — see `docs/mrscriptbasic.md`
for the language quirks. A `--default-language` option (default `ENU`) marks the
source/default language; its translation write statements are suppressed in the
generated script because the source text is not an overlay.

## Dependencies

`requirements.txt` keeps wide floors only: `pandas>=1.2`, `xlsxwriter>=1.0`,
`openpyxl>=3.0`, `pywin32>=300` (Windows only).

## Roadmap

See `docs/roadmap.md` for TODOs and ideas.
