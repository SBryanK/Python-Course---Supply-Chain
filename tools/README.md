# Tools

The scripts that build the course. Nothing here goes to Michella. One folder per part of the build, in the order you run them.

| Folder | What it builds | Main script |
|---|---|---|
| `1_data/` | The lesson CSV from the raw xlsx, and a check of 155 numbers | `build_slice.py`, `fact_check.py` |
| `2_notebooks/` | `student.ipynb` per session and `teacher_only/.../solution.ipynb` | `build.py` |
| `3_slides/` | `deck.pptx` and `deck.pdf` per session, and the presentation template | `s01_deck.py` ... `s10_deck.py`, `check_decks.py` |
| `4_handouts_and_docs/` | Handouts, recall, exit tickets, teacher cards, course outline, course home, answer key | `build_materials.py`, `build_course_docs.py` |
| `5_drive/` | The learner-only folder to drag into Google Drive (`drive_package/`) | `assemble_drive.py` |

## Set up once

Keep the venv outside the repo so the folder stays clean:

```bash
uv venv ~/.venvs/python-course --python 3.12
uv pip install --python ~/.venvs/python-course -r tools/requirements.txt
source ~/.venvs/python-course/bin/activate
```

Run every script from the repo root, for example `python tools/2_notebooks/build.py s04`.

## Notes per part

- **1_data.** The raw file must be restored first (`data/raw/README.md`). Run `convert_sheets.py`, then `build_slice.py`, then `fact_check.py`. It must end with `155/155 checks passed, 0 failed`. The CSV conversions in `data/work/` are temporary and can be deleted after.
- **2_notebooks.** `sessions_sNN.py` holds the cells for one session. `build.py` writes the student and solution notebooks and runs both. `test_env.py` runs every saved notebook again in the current Python.
- **3_slides.** Read `RUNBOOK.txt` before you build or render. `deckkit.py` has the shared slide types, and `deck_data.json` has the real numbers for the charts. `ppt_maker/` is a patched copy of the ppt-maker skill.
- **4_handouts_and_docs.** The text lives in `content_a.py` (S1 to S5) and `content_b.py` (S6 to S10).
- **5_drive.** It copies only learner files and renames each notebook to the name on its slide.
