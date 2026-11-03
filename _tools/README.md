# Tools

Small scripts used to build and check the course. Nothing here is delivered to the learner. They run with `_tools/venv` (Python 3.12, pandas 2.3.3, matplotlib, seaborn, python-pptx, python-docx, openpyxl), which is not committed.

## Data pipeline

Run in this order from the repo root. The raw file must be restored first, see `../data/raw/README.md`.

| Script | What it does | Output |
|---|---|---|
| `convert_sheets.py` | Reads `data/raw/online_retail_II.xlsx` and converts both sheets to CSV | `data/work/sheet_2009_2010.csv`, `data/work/sheet_2010_2011.csv`, `data/work/online_retail_ii_with_sheet.csv` |
| `build_slice.py` (Phase 2) | Deterministically writes the teaching slice from the 2010-2011 sheet | `data/online_retail_ii_lesson.csv` |
| `fact_check.py` | Checks 155 values against the data as a regression test (it does not read the prose) | printed in the terminal |

`fact_check.py` is the regression test for the numbers. It reads the CSV conversions in `data/work/`, so run `convert_sheets.py` first if those files are missing. A run that does not end with `155/155 checks passed, 0 failed` means a document, a script or the data changed and one of them is now stale.

## Deck toolchain

`deck_check/RUNBOOK.txt` has the exact commands for the ppt-maker build, render, audit and theme preview, plus the two sandbox patches applied to the extracted skill copy. Read it before building or rendering any deck.
