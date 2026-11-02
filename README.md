# PySC-101 build workspace

Build repository for a 1-on-1 beginner course: Python for Supply Chain Analytics, 10 sessions from 16 November to 17 December 2026.

The learner is a final-year logistics and supply chain student with no coding experience. The course uses the real UCI Online Retail II dataset and finishes with one 5-minute presentation on a cleaned sales dataset.

## Status

Phase 1 is complete: the dataset is explored and the build plan is written. The next phase starts after Bryan answers the open questions in `PLAN.md` section 9.

- `PLAN.md`: session plans S1 to S10 with verified numbers, build order, team plan, delivery structure, open questions.
- `data/EXPLORATION.md`: data report on the raw file, including the proposed lesson slice.

## What will be added

- `sessions/s01_...` to `sessions/s10_...`: student notebook, solution, deck, handout, teacher card, exit ticket, recall.
- `course_home/`: course outline, course home, teacher guide and learner templates.
- `data/online_retail_ii_lesson.csv`: the cleaned teaching slice, and `data/ANSWER_KEY.md`.
- `PUSH_LIST.md`: what goes to Google Drive and when.

## Repository notes

- This is a teacher-side repository. Learner-facing files are uploaded to Google Drive, not here. The raw dataset is never sent to the learner because of its size.
- The repository is public. It holds teacher-side planning and build materials; learner-facing files are delivered through Google Drive.
- Internal tools and scratch data are not versioned: the Python environment, the full CSV conversions, the raw xlsx and the deck toolchain test output are covered by `.gitignore`. See `data/raw/README.md` to restore the raw file.

## Data

UCI Online Retail II. Chen, D. (2012). Online Retail II [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5CG6D. Licence CC BY 4.0.

The course slice comes from the `Year 2010-2011` sheet, 1 December 2010 to 28 February 2011, uncleaned (see `data/EXPLORATION.md` section 12). The raw file is not committed; download and checksum instructions are in `data/raw/README.md`.

## Environment

Python 3.12.13 with pandas 2.3.3, matplotlib 3.11.2, seaborn 0.13.2, python-pptx 1.0.2, python-docx 1.2.0. Decks are built with the ppt-maker skill; LibreOffice renders the PDF and Proxima Nova is embedded. The exact commands are in `_tools/deck_check/RUNBOOK.txt`.
