# Python for Supply Chain

Repository: https://github.com/SBryanK/Python_Course_Supply_Chain

Build repository for a 10-session beginner course for one adult learner. The learner is a final-year logistics and supply chain student with no coding experience but strong Excel skills. The course runs online, one to one, from 16 November to 17 December 2026, uses Google Colab, and ends with one 5-minute presentation on a cleaned real sales dataset.

The course teaches just enough Python to be useful in supply chain work: variables, lists, functions, pandas, groupby and ABC analysis, matplotlib and seaborn, a short SQL and Power BI introduction, and one small project. It uses the real UCI Online Retail II dataset. No synthetic data.

## Status

Phase 1 is complete: the data is explored and the 10-session plan is written. The build is stopped until the five brief questions in `PLAN.md` section 10 are answered. Phase 2 is the S1 pilot: the lesson CSV, the S1 to S3 answer key, the S1 pack, the theme choice and the course outline.

## What is in the repository now

| Path | What it is |
|---|---|
| `PLAN.md` | The build plan: verified numbers, session plans S1 to S10, delivery structure, build order, review checklists, open questions |
| `data/EXPLORATION.md` | The data report: rows, dates, missing values, cancellations, duplicates, non-product codes, the proposed lesson slice and its cleaning steps |
| `data/raw/README.md` | How to restore the raw dataset and check its sha256 |
| `_tools/` | The data scripts, the fact-check script and the deck toolchain runbook (not delivered to the learner) |
| `_verify/` | The independent verification report and the scripts that produced it |

## Data

UCI Online Retail II. Chen, D. (2012). Online Retail II [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5CG6D. Licence CC BY 4.0.

The raw xlsx is not committed because it is 43.5 MiB and does not change. `data/raw/README.md` has the download URL and checksum. The course data file, `data/online_retail_ii_lesson.csv`, will be committed when Phase 2 builds it. It is an adaptation of the dataset and stays under CC BY 4.0 with the citation above.

The teaching slice is one three-month window from the `Year 2010-2011` sheet, 1 December 2010 to 28 February 2011, uncleaned: 105,335 rows, 8 columns, about 9.3 MB. Cleaning is the learner's work in session 4; the files she makes after that (sales_clean.csv, cancellations.csv, product_value.csv) live in her `Python for Supply Chain/work/` Drive folder. The full rule and the reasoning are in `data/EXPLORATION.md` section 12.

## Verification

- An independent audit recomputed every number in the exploration report from the raw xlsx. Its report is `_verify/VERIFICATION.md`.
- `_tools/fact_check.py` is the regression check: it checks 155 values against the data and must end with `155/155 checks passed, 0 failed`. It does not read the prose, so a doc typo still needs a human read.
- The deck toolchain was tested end to end: build, PDF, page images, audit and a five-variant theme preview, with Proxima Nova embedded. Commands and sandbox patches are in `_tools/deck_check/RUNBOOK.txt`.

## Repository layout

```
PLAN.md                  build plan and open questions
README.md                this file
data/
  EXPLORATION.md         data report and lesson slice proposal
  raw/README.md          restore instructions for the raw dataset
  online_retail_ii_lesson.csv   added in Phase 2
  ANSWER_KEY.md          added in Phase 2
  README.md              added in Phase 2
sessions/
  s01_.../               student.ipynb, solution.ipynb, deck.pptx, deck.pdf,
                         handout.pdf, teacher_card.md, exit_ticket.md, recall.md
  s02_.../ ... s10_.../
course_home/             course outline, course home, guides and templates
PUSH_LIST.md             what goes to Google Drive and when
_tools/                  internal scripts and the deck runbook
_verify/                 independent verification report
```

The repository is the build source; the Google Drive tree is the delivery copy. `sessions/` maps to `week_1` to `week_4` in Drive, `course_home/` maps to `00_course_home/`, and `teacher_only/` (solutions, teacher cards, answer keys, exit ticket answers) is never shared with the learner. The `_tools/ppt_maker` copy is third-party tooling, not course content; its NUS theme references and crest are unused by this course.

## Environment

Python 3.12.13 with pandas 2.3.3, matplotlib 3.11.2, seaborn 0.13.2, python-pptx 1.0.2, python-docx 1.2.0 and openpyxl 3.1.5. The environment is not committed. The exact deck commands and the two sandbox patches to the ppt-maker render script are in `_tools/deck_check/RUNBOOK.txt`.

## Licence

The course materials in this repository are copyright Bryan Kusno, 2026. They are public for reference and not for redistribution as a course. The dataset and the derived teaching slice are licensed CC BY 4.0; credit the citation above wherever they are used. The ppt-maker skill under `_tools/` is a tool included for reproducibility, not course content.

## Scope guardrails

Ten sessions on the fixed dates, no spare slot, no synthetic data, no machine learning or forecasting, no SQL or Power BI deep dive. Learner materials are in English. Teacher cards are in Bahasa Indonesia with English technical terms. No NUS branding anywhere. The repository is public because Bryan asked for it; it holds teacher-side planning material, not learner submissions.
