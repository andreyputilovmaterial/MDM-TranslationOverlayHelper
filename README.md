# MDM-TranslationOverlayHelper

Generates an Excel workbook with the fields, labels and translations of an MDD file,
and — after you edit that Excel — generates an `.mrs` script to write the updated
translations back into the MDD.

This is for **manual translation workflows**. Most of the time you don't need it: you
send files to LI and their tooling handles translations fine. But sometimes a project
needs its translations updated without any help from the LI side. Then a single Excel
file makes everyone's life easier — translators fill it in, reviewers check it, and IPS
uses it to push the updates back into the MDD.

## How it works

The tool orchestrates a few steps (each is a `--program` of the same bundle):

| Step | Program | What it does |
| --- | --- | --- |
| 1 | `read_mdd` | Reads an MDD and writes its contents as JSON (drives the `MDM.Document` COM server). |
| 2 | `report_html` | *(optional)* Renders that JSON as an HTML report. |
| 3 | `prep_mddread_scheme` | Patches the JSON scheme for the translation-overlay workflow. |
| 4 | `report_excel` | Renders the JSON as an Excel workbook. |
| 5 | `generate_overlays_script` | Reads the edited Excel and emits an `.mrs` script that updates the MDD. |

The generated `.mrs` file is **mrScriptBasic** (IBM/Unicom Data Model scripting). See
[docs/mrscriptbasic.md](docs/mrscriptbasic.md) for the language quirks.

## Requirements

- **Windows**.
- **IBM/Unicom Professional** installed (provides the `MDM.Document` COM server).
- **Python 3** with **pywin32** (`win32com.client`) — needed to read the MDD.
- Python packages: `pandas`, `xlsxwriter`, `openpyxl` (see `requirements.txt`).

> Only *reading* the MDD needs Windows + IBM/Unicom. Writing updates back is done by
> running the generated `.mrs` script inside IBM/Unicom — this tool doesn't touch the MDD
> directly.

## Usage

Download the latest release:
[Releases](../../releases/latest)

The release ships two batch files. Edit the paths at the top of each, then run them.

### 1. Generate the Excel map — `run_overlayhelper_excel.bat`

Edit `MDD_FILE` (path to your `.mdd`), and optionally `CONFIG_PRODUCE_HTML_MDD` and
`CONFIG_CLEAN_TEMP_MIDDLE_FILES`. Then run it. It reads the MDD, optionally renders an
HTML report, and produces the Excel map (`<mdd>.xlsx`).

### 2. Edit the Excel

Update the translations. Punch the `update` column for the rows you want written back.
The `comment` column is also written back to the MDD as a custom property (unless
disabled — see options).

### 3. Generate the update script — `run_overlayhelper_scripts.bat`

Edit `MDD_FILE` and `OUT_SCRIPT_FILE` (path for the resulting `.mrs`), then run. It reads
the Excel map and emits the `.mrs` script. Run that script inside IBM/Unicom to apply the
updates to the MDD.

There is no `pause` at the end of the batch files — if the window disappears, it means
everything finished successfully (failures pause before exiting).

### Options

- `--default-language` (default `ENU`): the source/default language. Its rows are not
  written back as overlays (the source text is not an overlay), so they are suppressed in
  the generated script. Change it by adding `--default-language <code>` to the batch
  command.
- Flags for `generate_overlays_script`:
  - `print_not_updated_lines_commented_out` — emit every row, but comment out the ones
    whose `update` column isn't punched (by default those rows are skipped entirely).
    Controlled by `CONFIG_PRINT_NOT_UPDATED_LINES_COMMENTED_OUT` in the batch file.
  - `dont_write_translators_comments_to_mdd` — don't emit code that writes the comment
    column back to the MDD. Controlled by `DONT_WRITE_TRANSLATORS_COMMENTS_TO_MDD`.

## The bundle is not editable

The tool is distributed as a single `.py` file produced by pinliner. Don't edit it:
Python loads parts of the file from itself at runtime, and those parts' start/end
positions are hardcoded. Any edit breaks the offsets and leads to undefined behaviour.

To change the behaviour, change the open source and rebuild (below).

## Development

Source lives in `src/`. It vendors three submodules:

- `src/lib/mdmreadpy` — MDD reader (JSON output); also vendors the HTML report generator.
- `src/lib/mdmexcelreportpy` — JSON → Excel.
- `src_dev_build/lib/pinliner` — the single-file bundler.

To rebuild the bundle:

```bat
build.bat
```

It builds the `mdmreadpy` submodule first (regenerating its generated files), bundles
`src/` with pinliner into `dist/mdmoverlayhelper_bundle.py`, copies the batch files and
`LICENSE`/`README.md`/`requirements.txt` into `dist/`, and verifies the bundle loads with
`--program done`.

## Documentation

- [.mrs / mrScriptBasic](docs/mrscriptbasic.md)
- [Roadmap / TODOs](docs/roadmap.md)

## Frequently asked questions

TBD
