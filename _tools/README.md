# Tools

Small scripts used to build and check the course. Nothing here is delivered to the learner. They run with `_tools/venv` (Python 3.12, pandas 2.3.3, matplotlib, seaborn, python-pptx, python-docx, openpyxl), which is not committed.

## Data pipeline

Run in this order from the repo root. The raw file must be restored first, see `../data/raw/README.md`.

| Script | What it does | Output |
|---|---|---|
| `convert_sheets.py` | Reads `data/raw/online_retail_II.xlsx` and converts both sheets to CSV | `data/work/sheet_2009_2010.csv`, `data/work/sheet_2010_2011.csv`, `data/work/online_retail_ii_with_sheet.csv` |
| `build_slice.py` | Deterministically writes the teaching slice from the raw 2010-2011 sheet and checks it against the build spec | `data/online_retail_ii_lesson.csv` |
| `fact_check.py` | Checks 155 values against the data as a regression test (it does not read the prose) | `_tools/fact_check_results.json`, printed in the terminal |

`fact_check.py` is the regression test for the numbers. It reads the CSV conversions in `data/work/`, so run `convert_sheets.py` first if those files are missing. A run that does not end with `155/155 checks passed, 0 failed` means a document, a script or the data changed and one of them is now stale.

## Deck toolchain

`deck_check/RUNBOOK.txt` has the exact commands for the ppt-maker build, render, audit and theme preview, plus the sandbox patches applied to the extracted skill copy. Read it before building or rendering any deck.

The decks are built from scripts, all in the same look (theme L:soft, live format, left aligned, regular tone, no logo, no photos):

| Script | Output |
|---|---|
| `deck_builds/deckkit.py` | shared helpers: cover, question, concept slide with code panel, code compare, table, chart, Now in Colab, recap, homework |
| `deck_builds/deck_data.json` | the real numbers and chart data, computed from `data/online_retail_ii_lesson.csv` |
| `deck_builds/s01_deck.py` ... `s10_deck.py` | `sessions/sNN_<name>/deck.pptx` and `deck.pdf` |
| `deck_builds/presentation_template.py` | `course_home/presentation_template.pptx` |

Run a build with `_tools/venv/bin/python _tools/deck_builds/s01_deck.py`, then render and audit it with the commands in `deck_check/RUNBOOK.txt`. Code is set in DejaVu Sans Mono from `fonts/`; see `fonts/README.md`.
