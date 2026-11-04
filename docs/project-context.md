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

Plus two meta-programs on the same launcher: `done` (a dependency-free smoke test the
build uses to verify the bundle loads) and `version` (prints the git-derived version
string from `GENERATED/_VERSION.py`).

## Submodules

- `src/lib/mdmreadpy` — MDD reader producing the JSON report; vendors `mdmreportpy`.
- `src/lib/mdmexcelreportpy` — JSON report → Excel.
- `src_dev_build/lib/pinliner` — build tool that bundles `src/` into a single
  `dist/mdmoverlayhelper_bundle.py`.

## Build

`build.bat` (Windows) / `build.sh` (macOS/Linux) first update the program version
(`src/GENERATED/_VERSION.py` from `git describe --tags --dirty`), then build the
`mdmreadpy` submodule (regenerating its `GENERATED` files — `_VERSION.py` and the nested
`mdmreportpy` HTML template), then run pinliner over `src/` (with
`--main src.launcher --main-attr main`) to produce
`dist/mdmoverlayhelper_bundle.py`, copy the run `.bat` files plus `LICENSE`/`README.md`
into `dist/`, and run `src_dev_build/inline_run_init.py` to inline the venv setup plus
explicit `pip install` rows into each distributed launcher. `dist/` therefore ships a
two-file layout — the bundle plus self-contained `.bat` launchers; no `requirements.txt`,
`optional_dependencies/` or `run_init.*`. Finally the build verifies the bundle loads
with `--program done`.

## Launching (three ways)

Each program can be launched three equivalent ways (same schema as the other projects):
1. **Single-file bundle** — `python dist/mdmoverlayhelper_bundle.py --program <name>`.
2. **Direct module** — `python -m src.program_generate_overlays_script ...` /
   `python -m src.program_prep_mddread_scheme ...`.
3. **Launcher proxy** — `python -m src.launcher --program <name>`.

Plain-script invocation (without `-m`) is not supported.

## Generated `.mrs` scripts

`generate_overlays_script` emits mrScriptBasic (`.mrs`) — see `docs/mrscriptbasic.md`
for the language quirks. A `--default-language` option (default `ENU`) marks the
source/default language; its translation write statements are suppressed in the
generated script because the source text is not an overlay.

## Dependencies

`requirements.txt` keeps wide floors only for the always-installed core: `pandas>=1.2`,
`xlsxwriter>=1.0`, `openpyxl>=3.0`. The launcher imports the program modules lazily, so
`--program done` works before any third-party package is installed. Optional and
platform-specific dependencies live in each submodule's `requirements.txt` under
`src/lib/` (`mdmreadpy`: `pywin32`, Windows-only; `mdmreportpy`: `csscompressor`/`rjsmin`;
`mdmexcelreportpy`: `pandas`/`xlsxwriter`). `run_init.bat`/`run_init.sh` are the single
source of truth for the venv setup; their marked
`=== BEGIN/END GENERATED DEPENDENCIES ===` section is regenerated at build time by
`src_dev_build/inline_run_init.py` into explicit `pip install` rows that are inlined
best-effort into each distributed launcher.

## Conventions

Cross-project structural conventions (entry-point import style, bundling and call
conventions) live in `docs/maintenance-log.md`; repo-specific notes stay here and in the
commit history.

## Roadmap

See `docs/roadmap.md` for TODOs and ideas.
