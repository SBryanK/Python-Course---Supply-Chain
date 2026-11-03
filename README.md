# Python for Supply Chain

Repository: https://github.com/SBryanK/Python_Course_Supply_Chain

Build repository for a 10-session beginner course for one adult learner. The course runs online, one to one, from 16 November to 17 December 2026, uses Google Colab, and ends with one 5-minute presentation on a cleaned real sales dataset.

The course teaches just enough Python to be useful in supply chain work: variables, lists, functions, pandas, groupby and ABC analysis, matplotlib and seaborn, a short SQL and Power BI introduction, and one small project. It uses the real UCI Online Retail II dataset. No synthetic data.

## What is in the repository

| Path | What it is |
|---|---|
| `PLAN.md` | The build plan: verified numbers, session plans S1 to S10, delivery structure, build order, review checklists, open questions |
| `data/EXPLORATION.md` | The data report: rows, dates, missing values, cancellations, duplicates, non-product codes, the proposed lesson slice and its cleaning steps |
| `data/raw/README.md` | How to restore the raw dataset and check its sha256 |

## Data

UCI Online Retail II. Chen, D. (2012). Online Retail II [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5CG6D. Licence CC BY 4.0.

The raw xlsx is not committed because it is 43.5 MiB and does not change. `data/raw/README.md` has the download URL and checksum. The course data file, `data/online_retail_ii_lesson.csv`, will be committed when Phase 2 builds it. It is an adaptation of the dataset and stays under CC BY 4.0 with the citation above.

The teaching slice is one three-month window from the `Year 2010-2011` sheet, 1 December 2010 to 28 February 2011, uncleaned: 105,335 rows, 8 columns, about 9.3 MB. Cleaning is the learner's work in session 4; the files she makes after that (sales_clean.csv, cancellations.csv, product_value.csv) live in her `Python for Supply Chain/work/` Drive folder. The full rule and the reasoning are in `data/EXPLORATION.md` section 12. The repository is the build source; the Google Drive tree is the delivery copy.


## Licence

The course materials in this repository are copyright Bryan Kusno, 2026. 
They are public for reference and not for redistribution as a course. The dataset and the derived teaching slice are licensed CC BY 4.0; credit the citation above wherever they are used.
