# Python for Supply Chain: build spec

This file tells a builder (a person or an AI) exactly what to make. Read all of it before you start. Every decision is already made. Do not ask questions, and do not leave placeholders.

## 1. The two audiences

| | Michella (the learner) | The teacher |
|---|---|---|
| Sees | The lesson data, student notebooks, slides (PDF), handouts, recall sheets, course home | Everything, including solutions and teacher cards |
| Goes to | Google Drive, folder `Python for Supply Chain/` | Stays local in `teacher_only/` (never committed, never shared) |

**The course is traditional.** One teacher, one learner, live on a screen share. Notebook, slides and handout. No video, no tool tours, no AI lessons. If she wants to use an AI tool while she studies, that is her own choice and is not part of the course.

**Who the learner is:** a final-year logistics and supply chain student. Never coded. Strong in Excel (formulas, filters, VLOOKUP, PivotTables). Quick, but needs repetition to remember syntax. Windows laptop, Google Colab in the browser, nothing installed. The teacher speaks Bahasa Indonesia with her; all written material for her is in English. Her English is good but it is a second language.

**Goal by 17 Dec 2026:** she cleans and analyses a real sales dataset in Python, shows it in clear charts, and presents one finding in 5 minutes. She keeps one project on GitHub.

**Not the goal:** machine learning, forecasting, optimisation, deep SQL or Power BI.

## 2. Decisions already made

| Topic | Decision |
|---|---|
| Course name | Python for Supply Chain (no course code) |
| Sessions | 10, Mon/Wed/Thu, 15:00 SGT (14:00 WIB), 90-minute slot |
| Dates | S1 Mon 16 Nov, S2 Wed 18 Nov, S3 Mon 23 Nov, S4 Thu 26 Nov, S5 Mon 30 Nov, S6 Thu 3 Dec, S7 Mon 7 Dec, S8 Thu 10 Dec, S9 Mon 14 Dec, S10 Thu 17 Dec |
| Shape | Block 1 (35 min), break (5), Block 2 (35). Nine sessions plan 75 minutes. S4 plans 80. Every session stops at 90. The spare minutes are for setup and overrun |
| Data | Real data only. Slice of UCI Online Retail II, Dec 2010 to Feb 2011 (section 3) |
| The giant cancelled order | She finds it and removes it in S4 |
| Non-product rows | Keep stock codes that start with a digit |
| Country chart | Top 5 outside the UK, with "outside the UK" in the title |
| Names in files | Write "you". Never write the teacher's or learner's name in learner files |
| Slide look | Theme `L:soft`, left aligned, regular tone, same in all decks. No logo, no photos, colour and type only |
| Learner files | Google Colab and Drive. English |
| Teacher files | Bahasa Indonesia with English technical terms |
| Charts | matplotlib first, then seaborn (seaborn is homework) |
| SQL and Power BI | A short taste in S7 (SQL 15 min, Power BI 7-minute demo) |
| Project | S7 Block 2, S8, S9, then presented in S10 |
| AI | Not part of the course. No AI rules, no AI log, no AI questions |

## 3. The data

UCI Online Retail II, a UK online gift shop. Chen, D. (2012). Online Retail II [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5CG6D. Licence CC BY 4.0. Put this credit in `data/README.md`, the first notebook that loads the data (S4), the course outline, the course home, and the README template she writes in S9.

The raw file is `data/raw/online_retail_II.xlsx` (restore it with `data/raw/README.md`). `_tools/convert_sheets.py` turns it into CSV files in `data/work/`.

**Build the lesson file** `data/online_retail_ii_lesson.csv` with `_tools/build_slice.py`. Rule: every row of the `Year 2010-2011` sheet with InvoiceDate from 2010-12-01 00:00 up to but not including 2011-03-01 00:00. Keep the original column names, order and row order. Do not clean it. Write `InvoiceDate` as `YYYY-MM-DD HH:MM:SS`, leave Customer ID blank when missing. Check it against this table:

| Property | Value |
|---|---|
| Rows / columns | 105,335 / 8 |
| Columns | `Invoice`, `StockCode`, `Description`, `Quantity`, `InvoiceDate`, `Price`, `Customer ID`, `Country` |
| Dates | 2010-12-01 08:26 to 2011-02-28 17:04 |
| Size | about 9.3 MB |
| Missing Customer ID / Description | 36,210 / 304 |
| Cancellation rows (invoice starts with C) / exact duplicates | 1,904 / 975 |
| Zero price rows / negative price rows | 540 / 0 |
| Non-product code rows | 588 |

Why this window: it starts at the first row of the sheet, so S1 to S3 use the same first rows she meets again in S4. It has the December peak, so the daily chart has something to say. It is one sheet, so the 9-day overlap between the yearly sheets does not count twice.

**Keep these true in every file:**
- Money is in pounds. Write "pounds" or the symbol, never dollars or rupiah.
- The data covers three months, not a year.
- 34.9% of clean rows have no customer ID. That is fine for product questions, not for customer questions.
- UK is 84.82% of revenue, so country charts must not look global.
- Some stock codes come in two spellings (`85123A`, `85123a`), and 40 codes have two descriptions. We do not fix the first. The second is the S6 merge lesson.

## 4. Verified numbers

Every number in a notebook, slide or handout must come from this table or from running the code. Never type a number from memory. Computed from the slice, all in pounds.

| What | Value |
|---|---|
| Raw rows / clean rows | 105,335 / 101,458 |
| Cleaning log | 105,335 -> 104,360 (duplicates) -> 102,471 (C invoices) -> 102,257 (quantity above 0) -> 101,933 (price above 0) -> 101,459 (product codes) -> 101,458 (giant order removed) |
| Clean shape (with `revenue` and `month`) | (101458, 10) |
| Clean revenue | 1,876,534.04 |
| Products / class A / B / C | 3,066 / 671 (21.9%) / 794 (25.9%) / 1,601 (52.2%) |
| Class A share of revenue | 79.98% |
| Top product | REGENCY CAKESTAND 3 TIER, 51,504.85 |
| Top 10 products, share of revenue | 9.62% |
| Revenue Dec 2010 / Jan 2011 / Feb 2011 | 775,572.23 / 593,178.39 / 507,783.42 |
| UK revenue / UK share | 1,591,694.50 / 84.82% |
| UK revenue by month | Dec 705,166.72, Jan 468,651.61, Feb 417,876.17 |
| Top 5 outside the UK | Netherlands 58,182.55, EIRE 43,426.19, Germany 37,365.63, France 32,392.39, Australia 24,678.48 |
| Best day | 2010-12-07, 81,454.99 |
| Germany rows raw / clean | 1,741 / 1,514 |
| First 7 quantities | 6, 6, 8, 6, 6, 2, 6 |
| First three line values | 6 * 2.55 = 15.299999999999999 (rounds to 15.3), 6 * 3.39 = 20.34, 8 * 2.75 = 22.0 |
| The giant order | invoice 541431, 74,215 jars of code 23166, 77,183.60, cancelled 16 minutes later by C541433 |
| S6 merge check | 3,066 product rows -> 3,107 after a naive merge -> 3,066 after fixing |
| Trading days | 68 |
| Missing in raw slice | Description 304, Customer ID 36,210 |

The first rows of the file (use these in S1 to S3):

| Invoice | Code | Description | Quantity | Price |
|---|---|---|---|---|
| 536365 | 85123A | WHITE HANGING HEART T-LIGHT HOLDER | 6 | 2.55 |
| 536365 | 71053 | WHITE METAL LANTERN | 6 | 3.39 |
| 536365 | 84406B | CREAM CUPID HEARTS COAT HANGER | 8 | 2.75 |
| 536365 | 84029G | KNITTED UNION FLAG HOT WATER BOTTLE | 6 | 3.39 |
| 536365 | 84029E | RED WOOLLY HOTTIE WHITE HEART. | 6 | 3.39 |
| 536365 | 22752 | SET 7 BABUSHKA NESTING BOXES | 2 | 7.65 |
| 536365 | 21730 | GLASS STAR FROSTED T-LIGHT HOLDER | 6 | 4.25 |

A real big order for S3: invoice 540815 (1,930 at 2.55, 2,000 at 1.85, 3,114 at 2.10).

Write `teacher_only/ANSWER_KEY.md` with every expected answer for every exercise, each computed by running code. `python _tools/fact_check.py` must end with `155/155 checks passed, 0 failed`.

## 5. How to write for her

**Tone.** A kind, calm senior colleague. Friendly and a little playful, never loud. Light humour is fine when it helps memory (for example "the notebook does not remember what you changed in your head"). No emojis, no exclamation marks, no hype.

**Short.** The teacher explains everything live, so the notebook does not lecture. A text cell is one or two short sentences: what to do and what to look for. Nothing else.

**Self-explanatory.** She must be able to reopen the notebook alone at home and follow it. So: define each new word in one line the first time it appears, put the expected output in the cell above every exercise, and give every error a one-line "what it means".

**Plain English for a second-language reader.** Common words. Short sentences. One idea per sentence. Say "DataFrame" once in S4 as "a table in pandas", then just say "table". No idioms. Active voice.

**Sample (the level to aim for):**

> **Variable.** A variable is a label on a storage bin. You put a value in the bin and use the label to find it again.
> Run the cell. Then change `quantity` to 7 and predict what `print(quantity)` shows before you run it.

**Teaching moves**
- Daily life first, then the Excel version, then 3 to 6 lines of code that she types.
- Say the limit of every analogy ("Excel updates by itself. A notebook does not. Run the cell again.").
- After at most two concept cells she must do something: predict, change one value, or write one line. Never all theory first and all practice at the end.
- Exercises follow PRIMM: Predict, Run, Investigate, Modify, Make.
- She always types. The teacher never types for her.
- One story per session, with a business question. S7 is the only exception.
- For an error, read the last line first.
- Hint ladder, with 10 seconds of silence before each step: 1) "What do you expect this line to do?" 2) point at the line 3) a concept hint 4) show the pattern, not the answer 5) do it together, then she does a similar one alone.
- Optional "Why does this happen?" cell at the end of each notebook: 3 to 4 plain sentences ending with what it means for an analyst. No exercise depends on it. Examples: S1 why `6 * 2.55` is not exactly 15.3 (round money when you show it); S2 why counting starts at 0; S4 why a filter does not change the original table; S5 why ABC uses 80 and 95 (a habit, not a law).

**Code rules (every code cell she sees)**
- One step per line, saved in a name that says what it holds: `sales_clean`, `revenue_by_country`, `is_cancelled`.
- Short lowercase column names from S4 on.
- Show the result after each important step (`head()`, `shape`, `print`).
- `.copy()` once after filtering, explained as "Save As with a new name".
- Named functions with `.apply()`, linking back to S3. `print(f"...")` for messages. Comments say why, never what. Current pandas 2.x.
- Not allowed: lambdas, list comprehensions, classes, decorators, try/except, `*args`, chains longer than 2 calls, `inplace=True`, chained assignment, `.loc` tricks, `np.where`, regex, any concept before its session, hidden helper functions, cells that only work out of order.

**Words not to use anywhere:** delve, leverage, seamless, journey. No em-dashes.

## 6. The files to build

Repo folders: `sessions/sNN_short_name/` for learner files, `teacher_only/sessions/sNN_short_name/` for teacher files, `course_home/`, `data/`.

**Per session**

| File | For | Rules |
|---|---|---|
| `student.ipynb` | Her | Max 30 cells. A short text cell before every code cell. One idea per cell. Exercise cells start with `# TODO`, state the task in one comment line, and the text cell above shows the expected result |
| `deck.pptx` + `deck.pdf` | Her (PDF), teacher (PPTX) | 6 to 10 slides, at most 10 minutes of class. Spec in section 7 |
| `handout.pdf` | Her | One page if possible, two at most, black and white. The concept table (daily life, Excel, limit), code patterns, 3 common errors with fixes, the exercise list with expected answers |
| `recall.md` | Her | 3 short questions per day until the next session, one old topic and two new. Answers in a separate section at the end |
| `solution.ipynb` | Teacher | Same notebook with answers, run top to bottom |
| `teacher_card.md` | Teacher | Bahasa Indonesia with English terms, one page: the question, ideas in order, analogies and limits, 2 likely mistakes, hint ladder for the hardest exercise, timing |
| `exit_ticket.md` | Teacher | 2 questions and the answers |

**Notebook rules**
- Every notebook runs top to bottom on its own, in a fresh kernel, with no error.
- S4 saves her clean table to `work/sales_clean.csv`. From S5 on, the first cells load it, run `pd.to_datetime` on `invoice_date` (a CSV forgets that it was a date), then check `sales_clean.shape` is (101458, 10). A wrong shape means stop and fix before the lesson.
- Notebooks S4 to S9 mount Drive with `from google.colab import drive` and `drive.mount("/content/drive")`. Data path: `/content/drive/MyDrive/Python for Supply Chain/data/online_retail_ii_lesson.csv`. Her files path: `.../Python for Supply Chain/work/`.
- Build with `nbformat` from a script and execute with `nbconvert` in `_tools/venv`. In Colab, mount cells will not run on a laptop, so for the test run replace the Drive path by the local file and keep the Drive cells in the final file.

**Course-wide (`course_home/`)**

| File | What it holds |
|---|---|
| `course_outline.docx` + `.pdf` | Max 4 pages, black and white, plain. Section 9 |
| `course_home.docx` | The one page she opens: schedule, a link per session, recall, case hunt |
| `glossary.md` | About 25 English words with a one-line Bahasa Indonesia meaning |
| `case_hunt_template.md` | One page, 5 points: the problem; who is affected; what data would show it; one question you could answer with data; which tool fits (Python, SQL or a dashboard) |
| `reflection_template.md` | One page, 6 questions: what can I do now that I could not do before (show one cell); my biggest mistake and how I fixed it; where I still need help; what I would change in my project; my plan for the next 30 days; one thing I am proud of |
| `project_plan.md` | Question, columns needed, steps, expected chart, the decision it helps. The project menu (S7). 68 trading days, clean revenue, a worked reorder formula labelled as assumptions. Olist (Kaggle) as a January idea only, with a licence check reminder |
| `presentation_guide.md` | Answer first. 3 content slides plus cover and thank-you. The 5-minute shape. Say numbers simply ("about 1 in 5 products"). A 2-minute "walk me through your project" version |
| `presentation_scoring.md` | Clarity, evidence, recommendation, delivery, each 1 to 4 with a one-line anchor for every score. Project 10/10/10. Cold test out of 4. Reflection complete, partial or missing |
| `intro_sql.md`, `sql_playground.md`, `intro_powerbi.md` | One page each, the self-study versions of S7 |
| `github_guide.md` | One page: make an account, make an empty public repository, save the notebook from Colab, write the README |
| `presentation_template.pptx` | Cover, question, finding, recommendation, thank-you, same theme, with a hint on each slide |
| `optional_jan_module.md` | Outline only (deeper Power BI, SQL, VS Code, git). Do not build it |

Teacher-only: `teacher_guide.md` (Bahasa Indonesia: hint ladder, feedback rules, the 10-second wait, overload signal, cut order, how to run the cold test) and `ANSWER_KEY.md`.

## 7. How to build the slides

Use the `ppt-maker` skill. Environment, patches and exact commands are in `_tools/deck_check/RUNBOOK.txt`. Always make the PDF with the patched `render.py`, then run `audit.py` and look at every slide image.

- Format `live`, theme `L:soft`, left aligned, regular tone. Same in every deck. No logo, no photos.
- 6 to 10 slides. One idea per slide. A slide is a title that says the idea in plain words, one picture or analogy, the Excel bridge, 3 to 6 lines of code (monospace, Consolas or DejaVu Sans Mono), and the limit in one line. Body text stays in the theme font.
- Slide text in English. **Speaker notes in Bahasa Indonesia** with English technical terms: what to say, the analogy in everyday words, the limit, and one question to ask her.
- A "Now in Colab" slide where live coding starts, naming the notebook.
- Every number comes from running the notebook. Never typed by hand.
- Standard order for S2 to S6: cover, today's question, one slide per concept, Now in Colab, recap (3 things you can do now), homework and recall.
- S1 deck (9 slides): cover; course map (10 sessions on one timeline, with the 35/5/35 shape); why Python (Excel struggles when the file is huge, when the steps repeat every week, or when you must show exactly what you did); Colab tour; print and variable; data types; arithmetic, round and f-string; reading errors; Now in Colab and homework.
- S5 deck includes the finding slide: one big number ("about 1 in 5 products bring 80% of the money") and one chart.
- S7 deck: SQL and pandas side by side, then "how to choose a project question".
- S10 deck: short frame only (agenda, Q&A, keep/stop/start, what next).
- `presentation_template.pptx` follows section 6.

## 8. The sessions

Each session lists: the question, timing, concepts, the code she types, the notebook flow, exit ticket, recall and homework. Build the deck, handout and teacher card from these.

### S1, Mon 16 Nov: Hello, Python

**Question:** What is one order line worth?
**New words (define on first use):** order line (one product on one receipt), variable, data type, f-string, error message.

**Timing.** Block 1: 0-5 hello and why Python (2 slides), 5-12 Colab tour (open the notebook from Drive, text cell vs code cell, run with Shift+Enter, the order of running matters, peek at the CSV in Drive), 12-35 three micro-cycles: print and variable 6, data types 6, arithmetic, round and f-string 8, then 3 for a short recap. Block 2: 0-10 exercises 1 and 2, 10-16 error zoo (predict, run, investigate), 16-22 exercise 3 and fix three broken cells, 22-30 exit ticket, 30-35 close.

| Concept | Daily life | Excel | Say the limit |
|---|---|---|---|
| `print()` | reading a label out loud | typing in a cell to see it | Python shows nothing unless you ask |
| variable | a label on a storage bin | a named cell | change it and other cells do not update; run again |
| int / float / str | counting boxes / weighing goods / a product name | number vs text format | `"5"` is text; Python will not add text to a number |
| arithmetic, `round` | adding up a receipt | `=B2*C2`, `ROUND` | `6 * 2.55` gives 15.299999999999999; round money when you show it |
| f-string | a fill-in-the-blank label | `="Sold "&A2&" units"` | easy to forget the `f`; braces mark where the value goes |

```python
product_name = "WHITE HANGING HEART T-LIGHT HOLDER"
quantity = 6
unit_price = 2.55

sales_value = quantity * unit_price
print(sales_value)
print(round(sales_value, 2))
print(f"We sold {quantity} units of {product_name} for {round(sales_value, 2)} pounds.")
```

**Notebook (about 25 cells).** Start with how to run a cell and one rule: cells run in the order you click, so a NameError usually means "run the cells above". Then: print, variable, *predict what changes if quantity is 7*, multiply (the 15.299999999999999 moment), round, *change the price to 3.39, predict, check 20.34*, `type()`, *predict `"5" + 5`*, f-string, *change it to print units*, exercises 1 to 3 (WHITE METAL LANTERN 20.34, CREAM CUPID HEARTS COAT HANGER 22.0, one f-string sentence about the first line), error zoo (NameError from a typo, SyntaxError from a missing bracket, TypeError from `"5" + 5`, read the last line first), exercise 4 (fix three broken cells), recap, homework, and a checklist (Google account, Chrome or Edge, charger, headset, the Drive folder opens). End with the optional "Why does this happen?" cell.

**Handout:** the concepts table, code patterns, the three errors and fixes, exercises with answers, and the first 12 real order lines (invoice 536365 plus 540815) for homework.
**Exit ticket:** (1) predict a 3-line cell that prints a value and its rounded value. (2) name the error in one broken cell and fix it.
**Recall:** Tue 17 Nov. **Homework:** finish the worksheet, make the three errors on purpose, write one f-string about rows 8 to 10 on the handout.

### S2, Wed 18 Nov: Shelves, cards and choices

**Question:** Which order lines are big?
**Recall (5):** three S1 questions. **Warm-up (5):** write the Excel formula that multiplies and rounds; predict `print(quantity)` after `quantity = 12`. Then micro-cycles 25, break, worksheet 22, exit ticket 8, close 5.

| Concept | Daily life | Excel | Say the limit |
|---|---|---|---|
| list | a row of bins on one shelf | one column | the first bin is number 0 |
| `len`, `sum`, `min`, `max` | count, total, smallest, largest | COUNT, SUM, MIN, MAX | same idea, new spelling |
| dict | a product card: field name to value | one row with headers | look up by name, not position |
| comparison | "is this more than that?" | `=A2>10` | `=` stores, `==` asks |
| if / elif / else | a packing rule | `=IF(...)` | the indent is part of the rule |

```python
quantities = [6, 6, 8, 6, 6, 2, 6]
print(quantities[0])
print(len(quantities), sum(quantities), min(quantities), max(quantities))

order_line = {"stock_code": "85123A", "quantity": 6, "price": 2.55, "country": "United Kingdom"}
print(order_line["quantity"])
```

```python
quantity = order_line["quantity"]
if quantity >= 100:
    print("Big order line")
elif quantity >= 12:
    print("Medium order line")
else:
    print("Small order line")
```

Answers: len 7, sum 40, min 2, max 8; `[0]` 6, `[2]` 8, `[-1]` 6. The numbers 100 and 12 are teaching numbers, not business rules; the notebook says so. "Big" means one big line, because the data records lines, not whole invoices.
**Exercises:** predict `quantities[2]` and `quantities[-1]`; label 6 and then 12 with the if rule; print "UK" or "Outside UK" from the card.
**Handout errors:** index out of range, KeyError, missing colon or indent.
**Exit ticket:** (1) predict `quantities[2]` (8). (2) write the UK / Outside UK rule (prints "UK").
**Recall:** Thu 19 to Sun 22 Nov (4 days). **Homework:** add rows 8 to 10 from the S1 handout to the list and redo len, sum, min, max; one if rule about prices.

### S3, Mon 23 Nov: Let the loop do the walking

**Question:** Can one rule label every order line?
**Recall (5):** three S2 questions. **Warm-up (5):** predict a list index and an if cell.

| Concept | Daily life | Excel | Say the limit |
|---|---|---|---|
| for loop | walking down the shelf, checking each bin | dragging a formula down | the body must be indented |
| function | your own reusable rule | your own named formula | does nothing until you call it |
| `return` | the answer the rule hands back | the value the formula shows | `print` only shows; `return` hands it back |
| traceback | a stack of plates, newest on top | none | read the bottom line first, then go up |

```python
def order_size(quantity):
    if quantity >= 100:
        return "big"
    elif quantity >= 12:
        return "medium"
    else:
        return "small"

for quantity in quantities:
    label = order_size(quantity)
    print(f"{quantity} units -> {label}")
```

The traceback cell is a real three-level error: a loop calls a function that compares text with a number (TypeError). Run it on purpose, then read it from the bottom.
**Exercises:** write `line_value(quantity, price)` with `return`; loop over 5 real lines and print each value; label each line with `order_size`; change the threshold from 12 to 50 and predict what changes. No counting here (S5 counts with `.sum()`).
**Handout errors:** missing indent, missing `return` (you get `None`), calling a function before defining it.
**Exit ticket:** (1) fix a function that prints instead of returning. (2) read a 3-level traceback and say which line broke.
**Recall:** Tue 24 and Wed 25 Nov. **Homework:** `line_value` on the 5 handout lines; one function of her own with a return; open a blank Colab notebook, run `drive.mount("/content/drive")` once and accept the permission screen, so the pop-up does not surprise her in S4.

### S4, Thu 26 Nov: Cleaning day

**Question:** What does the data look like when it is clean, and how much did we sell?
The heaviest session. It plans 80 minutes and stops at 90.
**Recall (5):** three S3 questions. **Warm-up (5):** predict what `sales.shape` prints; write the Excel filter for Germany.

**Timing.** Block 1 (35): recall 5, warm-up 5, load and look 10 (`read_csv`, `head`, `shape`), missing values and rename 7, `info` and new words 5 (NaN, filter, `&` not `and`), cleaning log setup 3. Block 2 (40): filter and new column 8, she does the cleaning 9, revenue, date, month and sort 8, giant order 6, exit ticket 6, log review and close 3. If late, the giant order moves to the start of S5. `describe` is homework.

| Concept | Daily life | Excel | Say the limit |
|---|---|---|---|
| pandas, DataFrame | the whole warehouse list | a sheet | each column holds one type |
| `read_csv` | opening the file | File > Open | the path must be exact |
| `head`, `shape`, `info` | first page, page count, cover | scrolling, COUNTA | looking first is part of the job |
| rename with a dict | relabelling bins | editing headers | uses the S2 dict |
| filter | keeping only the good boxes | Filter | the original does not change unless you save the result; use `&`, with brackets |
| new column | writing a value on each box | a formula column | no auto-update; run again |
| `sort_values` | biggest boxes in front | Sort Z to A | same as Excel |
| date column | a calendar column | a date cell | must be a real date before you group by month |
| `.str[0]` | the first letter of a code | `LEFT()` | codes are text |
| `.copy()` | Save As with a new name | Save As | changing the copy cannot hurt the original |
| NaN | an empty box on a form | an empty cell | `isna()` counts them |

```python
import pandas as pd
from google.colab import drive

drive.mount("/content/drive")
sales = pd.read_csv("/content/drive/MyDrive/Python for Supply Chain/data/online_retail_ii_lesson.csv")
sales.head()
```

```python
new_names = {
    "Invoice": "invoice", "StockCode": "stock_code", "Description": "description",
    "Quantity": "quantity", "InvoiceDate": "invoice_date", "Price": "price",
    "Customer ID": "customer_id", "Country": "country",
}
sales = sales.rename(columns=new_names)
```

```python
is_cancelled = sales["invoice"].str.startswith("C")
cancellations = sales[is_cancelled]          # kept for the project

sales_clean = sales.drop_duplicates()
sales_clean = sales_clean[~sales_clean["invoice"].str.startswith("C")]   # ~ means NOT
sales_clean = sales_clean[sales_clean["quantity"] > 0]
sales_clean = sales_clean[sales_clean["price"] > 0]

first_character = sales_clean["stock_code"].str[0]
sales_clean = sales_clean[first_character.str.isdigit()]   # real products start with a digit
sales_clean = sales_clean.copy()
```

```python
sales_clean["revenue"] = sales_clean["quantity"] * sales_clean["price"]
sales_clean["invoice_date"] = pd.to_datetime(sales_clean["invoice_date"])
sales_clean["month"] = sales_clean["invoice_date"].dt.to_period("M")   # M = month, keeps the year
sales_clean.sort_values("revenue", ascending=False).head(10)
```

**Cleaning log:** she writes the row count after each step (section 4). Final shape (101458, 10).
**The giant order (detective moment):** the top row is invoice 541431 at 77,183.60. She looks at the raw rows, finds C541433 cancelling the same 74,215 jars 16 minutes later, and removes 541431 with one commented line.
**Notes in the notebook:** the filled customer IDs print as `17850.0` because a number column with empty cells is stored as decimals. Talk point: do we drop rows with no customer ID? For products no, for customers yes.
**Save at the end:** `sales_clean.csv` and `cancellations.csv` to `work/`.
**Exercises:** keep only Germany (1,514 rows); keep only lines with revenue above a value she picks.
**Handout:** the `&` filter pattern, a cleaning checklist, `describe`, errors (file not found, KeyError after rename, `and` instead of `&`).
**Exit ticket:** (1) what `shape` tells you ((105335, 8) at load, (101458, 10) at the end). (2) the Germany filter (1,514 rows).
**Recall:** Fri 27 to Sun 29 Nov, one pandas question a day and one about months. **Homework:** re-run the notebook, write the cleaning log in her own words, try `describe`, bring one question about the giant order.

### S5, Mon 30 Nov: Who are the star products?

**Question:** Which products bring most of the money?
**Recall (5):** three S4 questions (one about months). **Warm-up (5):** the PivotTable steps for revenue by product.
**Timing.** Block 1: recall 5, warm-up 5, groupby and sort 10, running total and share 7, ABC function 6, counting and country as copy-alongs 2. Block 2 is the cold test and is never cut: test 20 (notes allowed, teacher silent), look at one solution 5, exit ticket 7, close 3.

| Concept | Daily life | Excel | Say the limit |
|---|---|---|---|
| `groupby` + `sum` | sorting receipts into piles, then adding each pile | PivotTable | the result has a row label column; `reset_index()` makes it a normal table again |
| `cumsum` | a running total on a receipt roll | `=SUM($B$2:B2)` dragged down | sort first, or the total means nothing |
| ABC analysis | a few items take most of the space and money | sort, running %, IF | 80/95 is a habit, not a law |
| `.apply(function)` | using your S3 rule on every row | dragging your formula down | use a named function |

```python
revenue_by_product = sales_clean.groupby("stock_code")["revenue"].sum()
revenue_by_product = revenue_by_product.sort_values(ascending=False)
product_value = revenue_by_product.reset_index()

total_revenue = product_value["revenue"].sum()
product_value["cumulative_share"] = product_value["revenue"].cumsum() / total_revenue
```

```python
def abc_class(cumulative_share):
    if cumulative_share <= 0.80:
        return "A"
    elif cumulative_share <= 0.95:
        return "B"
    else:
        return "C"

product_value["abc_class"] = product_value["cumulative_share"].apply(abc_class)
(product_value["abc_class"] == "A").sum()
```

**Finding:** 671 of 3,066 products (21.9%) bring 79.98% of revenue. On the slide: "About 1 in 5 products bring 80% of the money." Class B has 794 products, class C 1,601.
**Cold test:** revenue by month for the top country, using her month column. Answers: United Kingdom; Dec 705,166.72; Jan 468,651.61; Feb 417,876.17. Score out of 4: it runs, the numbers are right (within 0.01), the names are clear, one sentence says what it means.
**Save:** `product_value.csv` to `work/` (used for Power BI in S7).
**Handout errors:** forgetting `reset_index`, cumsum before sorting, using a lambda.
**Exit ticket:** (1) which class is a product at 0.90? (B). (2) the 80/20 finding in one plain sentence.
**Recall:** Tue 1 and Wed 2 Dec. **Homework:** finish any copy-alongs, write her own ABC sentence.

### S6, Thu 3 Dec: Make the numbers talk

**Question:** How do we show the finding so a manager gets it in five seconds?
**Recall (5):** three S5 questions. **Warm-up (5):** sketch on paper the chart you would show a manager, with labelled axes.
**Timing.** Block 1: recall 5, warm-up 5, merge and the row-count lesson 12, top 10 bar chart 10, the title rule 3. Block 2: daily line chart 10, cumulative curve as a copy-along 8 (homework if late), fix-a-chart exercise 4, exit ticket 8, close and case hunt 5.

| Concept | Daily life | Excel | Say the limit |
|---|---|---|---|
| `merge` | matching a packing list to the catalogue | VLOOKUP / XLOOKUP | count rows before and after; a repeated key makes the table grow |
| matplotlib | drawing a chart step by step | Insert Chart, then edit | every chart needs a title and axis labels |
| seaborn | a chart template on top of matplotlib | chart styles | the same titles and labels still work |

**The merge lesson.** First she builds a names table with `drop_duplicates()` on both columns (3,107 rows) and merges: the table grows from 3,066 to 3,107. She finds the 41 extra rows (40 codes with two names), then dedupes on `stock_code` and merges again: 3,066.

```python
product_names = sales_clean[["stock_code", "description"]].drop_duplicates(subset="stock_code")

print(len(product_value))
product_value = product_value.merge(product_names, on="stock_code", how="left")
print(len(product_value))   # must match the line above
```

```python
import matplotlib.pyplot as plt

top10 = product_value.head(10).sort_values("revenue")

plt.figure(figsize=(10, 5))
plt.barh(top10["description"], top10["revenue"])
plt.title("The top 10 products are only 9.6% of revenue")
plt.xlabel("Revenue (pounds)")
plt.tight_layout()
plt.show()
```

**Chart rule:** the title says the finding, not the chart type. Examples: "Revenue peaked in the first week of December" (best day 2010-12-07), "About 1 in 5 products bring 80% of revenue", "Outside the UK, the Netherlands and Ireland lead". The daily table uses `.dt.date`, taught as a 3-minute copy-along. The seaborn chart (top 5 countries outside the UK) is homework.
**Case hunt:** explained in the last 5 minutes, due S8. She finds the case herself. The teacher card has two backup cases.
**Handout:** the chart recipe (`figure`, `barh` or `plot`, `title`, `xlabel`, `ylabel`, `tight_layout`, `xticks(rotation=45)` for long labels, `show`), three chart mistakes, the seaborn pattern with its expected picture, and the case hunt template.
**Exit ticket:** (1) your merge went from 3,066 to 3,107 rows. What happened and how do you fix it? (2) a finding-title for the daily chart.
**Recall:** Fri 4 to Sun 6 Dec. **Homework:** finish the top 10 chart, the seaborn pattern, start the case hunt, install Power BI Desktop.

### S7, Mon 7 Dec: New tools, your own question

**Question:** What question will you answer in your project?
**Timing.** Block 1: recall 5, warm-up 5 (write one question a manager might ask), SQL taste 15, Power BI demo 7 (she watches and builds it at home), exit ticket 3. Block 2: what makes a good question 6, pick from the menu 6, fill `project_plan.md` 12, presentation guide 8, close 3. If she is behind, SQL and Power BI become the two self-study pages and all 70 minutes go to the project.

```python
import sqlite3

columns_for_sql = ["invoice", "stock_code", "description", "quantity", "price", "country", "revenue"]
sql_table = sales_clean[columns_for_sql]

connection = sqlite3.connect(":memory:")
sql_table.to_sql("sales", connection, index=False)

query = """
SELECT country, SUM(revenue) AS total_revenue
FROM sales
GROUP BY country
ORDER BY total_revenue DESC
LIMIT 5
"""
pd.read_sql_query(query, connection)
```

Answers: UK 1,591,694.50, Netherlands 58,182.55, EIRE 43,426.19, Germany 37,365.63, France 32,392.39. Second query: Germany only (37,365.63). Third query (top 10 rows) is homework in `sql_playground.md`. Each query is shown next to its pandas version. MySQL is another SQL database that runs on a server; we do not install it. Free practice: sql-practice.com.
**Power BI demo:** open, load `product_value.csv`, one bar chart, one card, save. She repeats it at home with `intro_powerbi.md`.
**A good question is** specific, answerable with this data, and useful to a manager. If a question needs a skill we did not teach, change the question, not the skill.
**Project menu:**
1. Is class A revenue steady month to month? (filter A, group by month, one line chart)
2. Which country outside the UK buys most, and what are its top 5 products? (one filter, one groupby, one bar chart)
3. How big are cancellations, and which products get cancelled most? (`cancellations.csv`, 1,904 rows)
4. A reorder point for the top 5 products, using lead time and safety stock she chooses. Label every assumption as an assumption.
**Exit ticket:** (1) read a short SQL query and say what it returns. (2) your project question in one sentence, plus one column it needs.
**Recall:** Tue 8 and Wed 9 Dec, with one SQL reading question. **Homework:** Power BI at home, finish the project plan, start the analysis.

### S8, Thu 10 Dec: Detective work

**Question:** her own.
**Timing.** Block 1: case hunt talk 10 (2 minutes, linked to our data), project work 25. Block 2: project work 22, exit ticket 8, "what I found so far" in 3 sentences 5. The teacher uses the hint ladder only. No warm-up today.
**Notebook (about 17 cells):** load `sales_clean.csv` and check the shape; a project checklist; her question in her own words; the columns she needs; the first analysis; a draft chart; the 3-sentence status.
**Deck (7 slides):** cover, her question, case hunt talk, project checklist, how to check a number, Now in Colab, what I found so far.
**Exit ticket:** (1) your question in one sentence. (2) one number you checked by hand, and how.
**Recall:** Fri 11 to Sun 13 Dec (2 questions a day if she is behind). **Homework:** keep going; make a GitHub account and an empty public repository with `github_guide.md`; finish the case hunt.

### S9, Mon 14 Dec: Polish and publish

**Question:** Can you say your finding in three sentences?
**Timing.** Block 1: final charts and the 3-sentence conclusion (answer, evidence, recommendation) 25, write the finding and recommendation 8 (this is the exit ticket), hand out the reflection 2. Block 2: GitHub 12 (Colab File > Save a copy in GitHub, then the README in the browser), start the 3 slides from `presentation_template.pptx` 21, close 2.
**README contents:** her question, the data credit, her finding, how to run it. Minimum if behind: the upload, one chart and one finding sentence.
**Notebook (about 15 cells):** load and shape check; final chart checklist; the 3-sentence template; GitHub steps; README template; the slide template walk-through; the reflection questions.
**Deck (7 slides):** cover, today's question, final chart checklist, GitHub in the browser, README template, the 3 slides, reflection.
**Recall:** Tue 15 and Wed 16 Dec. **Homework:** finish the slides, rehearse once out loud, write the reflection.

### S10, Thu 17 Dec: Showtime

**Question:** Can you explain it like an analyst?
**Timing.** Block 1: settle in 5, her presentation 5, interview-style Q&A 15, feedback 10 (two strengths, one thing to improve). Block 2: reflection review 15, retro (keep, stop, start) 10, January ideas 3, exit ticket 7.
**Presentation:** cover, question, finding, recommendation, thank-you. In 5 minutes: 1 question and context, 2 finding and evidence, 1 recommendation, 1 spare. She presents in English, and may answer questions in Bahasa Indonesia. Delivery is scored on structure and pace, not accent.
**Q&A questions:** "Walk me through your project in 2 minutes." "Why did you remove those rows?" "What would you do with more time?" "How did you check your numbers?"
**Deck (6 slides):** cover, agenda, Q&A, keep/stop/start, what next, thank-you.
**Exit ticket:** (1) what can you do now that you could not do in November? (2) one thing you would do differently.
**Recall:** none. `recall.md` is an optional January practice sheet with 3 questions and answers.

## 9. Course outline (`course_home/course_outline.docx` + `.pdf`)

Max 4 pages. Black and white. Plain and professional. No logo, no school name, no instructor name, no email.

1. **Header:** Course: Python for Supply Chain. Class dates 16/11/2026 to 17/12/2026. Online, 10 sessions, 15:00 SGT (14:00 WIB), 90-minute slot.
2. **Overview:** one short paragraph: why Python for supply chain, and what she will do (clean real sales data, find which products matter, show it in clear charts, present one finding).
3. **Objectives (5, testable):** read and fix common Python errors; load, check and clean a real CSV with pandas; summarise with groupby and sort products with ABC; make clear charts with matplotlib and seaborn; present a finding in 5 minutes, answer first.
4. **Assessment:** participation and daily recall 20%, cold test 15%, project 30%, final presentation 20%, self-reflection 15%. One line: "This course is not graded. The weights show what matters most."
5. **Schedule table:** Lesson, Date, Session (summary and objectives), Resources (only what we provide: notebook, handout, slides, the dataset credit, sql-practice.com in S7, templates), Deadlines (cold test S5; case hunt handed out S6, due S8; project plan S7; project and GitHub S9; reflection before S10; presentation S10). Note in the S4 row that it may use 5 of the spare minutes.
6. **General guide:** the dataset citation, how to use the course home page, how and when to ask for help, how daily recall works.
7. **Academic honesty:** short. Her work must show her own understanding. Credit every source and the dataset.

## 10. Google Drive (what she sees)

```
Python for Supply Chain/
  00_course_home/   course home, outline, glossary, templates and guides
  data/             online_retail_ii_lesson.csv only
  work/             her own files from S4: sales_clean.csv, cancellations.csv, product_value.csv
  week_1/           S1, S2: student notebook, deck PDF, handout, recall
  week_2/           S3, S4
  week_3/           S5, S6
  week_4/           S7, S8, S9, S10
```

Upload the day before each session: S1 by 15 Nov, S2 by 17 Nov, S3 by 22 Nov, S4 by 25 Nov, S5 by 29 Nov, S6 by 2 Dec, S7 by 6 Dec, S8 by 9 Dec, S9 by 13 Dec, S10 by 16 Dec. Course home, outline and data by 14 Nov. Write `PUSH_LIST.md` with this schedule.

**Never upload:** `teacher_only/` (solutions, teacher cards, exit ticket answers, answer key, PPTX of decks, the tracker), the raw xlsx, `_tools/`, `data/work/`.

## 11. Build order

1. Build the slice (`_tools/build_slice.py`), write `data/README.md`, and check the slice against section 3.
2. Write `teacher_only/ANSWER_KEY.md` for S1 to S3. Run `fact_check.py`.
3. Build S1 completely (notebook, solution, deck, handout, recall, teacher card, exit ticket). This is the style sample. Re-read it as a non-programmer with English as a second language.
4. Build the course outline.
5. Build S2 to S10, one at a time, copying the S1 style. After S4, re-check S2 to S4 together.
6. Build the course-wide files, `presentation_template.pptx` and `PUSH_LIST.md`.
7. Final check (section 12).

## 12. Checks before calling anything done

1. Every notebook runs top to bottom in a fresh kernel with no error, and every output matches `ANSWER_KEY.md`.
2. Every exercise uses only concepts taught so far. List any exception.
3. She has something to do after every two concept cells.
4. Caps: 30 cells, 2 pages per handout, 1 page per teacher card, 6 to 10 slides (10 minutes max).
5. Run `render.py` and `audit.py` and look at every slide.
6. Read each learner file as a non-programmer who reads English as a second language. Shorten or replace any sentence that needs a second read.
7. No em-dashes, emojis, exclamation marks, or the words delve, leverage, seamless, journey.
8. No school name, logo, or person's name in learner files.
9. No AI instructions in any file.

## 13. If she falls behind

Cut in this order: (1) S7 SQL and Power BI become the two self-study pages. (2) Seaborn stays homework and the cumulative curve moves to homework. (3) The project shrinks from 3 sessions to 2.
**Overload signal:** two exit tickets in a row under 50%. Slow down and drop the bonus parts.
**She misses a session:** send the notebook and the solution walkthrough the same day. The next recall and warm-up (10 minutes) become the catch-up. If S4 is missed, build the clean table together on the shared screen.
**Colab restarts:** every notebook from S5 starts with a load and shape check, so a restart costs one cell.
**Before S1:** a 10-minute check by 13 Nov. She opens a shared Colab link, runs `print("hello")`, opens the Drive folder, and tests screen share.

## 14. Environment

Python 3.12 with pandas 2.3.3, matplotlib 3.11.2, seaborn 0.13.2, python-pptx 1.0.2, python-docx 1.2.0, openpyxl 3.1.5, in `_tools/venv` (not committed). Colab may run a newer pandas, so use only stable pandas 2.x calls. Deck commands, the `/opt/homebrew/bin` PATH requirement and the two patches to `render.py` are in `_tools/deck_check/RUNBOOK.txt`. Set `MPLCONFIGDIR` only when a deck draws a chart.
