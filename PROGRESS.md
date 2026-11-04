# Progress

Where each part of the course stands, and where its materials are. Update the status column when something changes.

Status: `built` = made and checked, `uploaded` = in her Drive, `taught` = class done.

## Course-wide

| Part | Status | Materials | Upload by |
|---|---|---|---|
| Data | built | `data/online_retail_ii_lesson.csv`, `data/README.md`, `data/EXPLORATION.md` | 14 Nov |
| Course home | built | `course_home/` (outline, course home, glossary, guides, templates) | 14 Nov |
| Presentation template | built | `course_home/presentation_template.pptx` | 7 Dec |
| Tech check | to do | Colab link, `print("hello")`, Drive folder, screen share | 13 Nov |

## Sessions

Each folder in `sessions/` has `student.ipynb`, `deck.pptx`, `deck.pdf`, `handout.pdf` and `recall.md`.

| # | Session | Date | Folder | Status | Upload by | Drive folder |
|---|---|---|---|---|---|---|
| 1 | Hello, Python | Mon 16 Nov | `sessions/s01_hello_python/` | built | 15 Nov | week_1 |
| 2 | Shelves, cards and choices | Wed 18 Nov | `sessions/s02_shelves_cards_choices/` | built | 17 Nov | week_1 |
| 3 | Let the loop do the walking | Mon 23 Nov | `sessions/s03_let_loop_walk/` | built | 22 Nov | week_2 |
| 4 | Cleaning day | Thu 26 Nov | `sessions/s04_cleaning_day/` | built | 25 Nov | week_2 |
| 5 | Who are the star products? | Mon 30 Nov | `sessions/s05_star_products/` | built | 29 Nov | week_3 |
| 6 | Make the numbers talk | Thu 3 Dec | `sessions/s06_numbers_talk/` | built | 2 Dec | week_3 |
| 7 | New tools, your own question | Mon 7 Dec | `sessions/s07_new_tools/` | built | 6 Dec | week_4 |
| 8 | Detective work | Thu 10 Dec | `sessions/s08_detective_work/` | built | 9 Dec | week_4 |
| 9 | Polish and publish | Mon 14 Dec | `sessions/s09_polish_publish/` | built | 13 Dec | week_4 |
| 10 | Showtime | Thu 17 Dec | `sessions/s10_showtime/` | built | 16 Dec | week_4 |

## Drive upload

`python tools/5_drive/assemble_drive.py` makes `drive_package/Python for Supply Chain/` with only the learner files. Each notebook is renamed to the name on its slide, for example `s1_hello_python.ipynb`. Upload by the day before each session. Never upload `teacher_only/`, `tools/`, `data/raw/` or the `deck.pptx` files.

## Where else to look

- `PLAN.md`: the build spec for every session.
- `tools/README.md`: the build scripts, one folder per part.
- `teacher_only/` (local, not in git): solutions, teacher cards, exit tickets, answer key, teaching tracker, next steps.

## Checks last run (4 Nov 2026)

All 10 sessions are in the lecture style: decks with one visual anchor per slide, lean notebooks with an exercise ladder and Expected values. Handouts, answer key and teacher cards now read their exercise lists from the notebooks (`tools/4_handouts_and_docs/exercises.py`), so they always match. Notebooks 10/10 pass `build.py`, decks 11/11 pass `check_decks.py` with 0 audit warnings, handouts are 1 or 2 pages, the Drive package is refreshed.

Open: `fact_check.py` cannot run until `data/work/sheet_2009_2010.csv` is regenerated (`data/raw/README.md`). Recall questions and exit tickets are unchanged. Nothing is opened in real Colab yet.
