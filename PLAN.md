# PySC-101 build plan

Phase 1 plan for the 10-session course. Written 2 Nov 2026. Source of truth is the master build brief, version 1.0, 2 Nov 2026. This plan adjusts the brief where the real data or the real environment requires it, and lists the questions Bryan must answer before Phase 2 starts.

Status: Phase 1 deliverables are `data/EXPLORATION.md`, this file, and the untouched raw data in `data/raw/`. The numbers have been through two review rounds. An independent verifier recomputed every number from the raw xlsx and found four defects in the first draft of the exploration report. A second review added `_tools/fact_check.py`, which now re-checks 151 facts and reports 151/151 passed after the fixes. The corrected figures are the non-product row totals (6,093 rows, 62 codes), slice non-product rows, the distinct description count, the clean-table missing-customer count (35,364) and the alternative-window row count. The deck toolchain was tested end to end (build, PDF, page images, audit, five-variant preview). On 2 Nov 2026 the seven P1 fixes and the selected P2 fixes from `_review/pedagogy-review.md` were applied to this plan (micro-cycles in every outline, S4 to S7 timing, month extraction, fair exercises, scoring anchors, buffer policy), and every changed number was recomputed from the slice. STOP here until Bryan answers section 9.

## 1. What changed from the brief's assumptions

Everything marked [VERIFY] in the brief is now checked against the real file. Five things need a decision or an adjustment:

1. The column names are exactly as the brief guessed: `Invoice`, `StockCode`, `Description`, `Quantity`, `InvoiceDate`, `Price`, `Customer ID`, `Country`. The price column is `Price`, not `UnitPrice`. The brief's code samples work as written.
2. The lesson slice needs a rule that avoids counting the 9-day overlap between the two yearly sheets twice. Proposal: all rows of the `Year 2010-2011` sheet from 2010-12-01 to 2011-02-28. See section 2 and open question 6.
3. The slice contains one huge cancelled order (invoice 541431, 74,215 units of stock code 23166, worth 77,183.60). The simple S4 cleaning keeps the positive line and drops the cancellation, which would make this cancelled order the number one product. Proposal: the learner sees it at the top of the S4 "biggest revenue rows" step, and S5 opens with a 5-minute investigation that finds C541433 and removes that one invoice with a commented line. See open question 7.
4. The brief's S4 step "remove invoices starting with C" is redundant once `quantity > 0` runs: after `drop_duplicates`, both orders end at 102,257 rows. The plan drops the C step (two fewer concepts, `~` and `.str.startswith`, in the heaviest session) and keeps one line that saves the cancellation rows for project question 3.
5. The brief's non-product list for S4 is too short. The slice has 588 non-product rows: postage, fees, samples, discounts, manual lines, gift vouchers and old DCGS catalogue codes. Proposal: keep the rows whose stock code starts with a digit. Every real product code starts with a digit, every charge or voucher code starts with a letter, so one line removes all 588 and cannot miss a new fee code. A hard-coded 8-code list would leave 19 of those rows in the clean table.
6. The S6 seaborn chart, done exactly as the brief drafts it, would show one huge UK bar and five tiny bars, because the UK is 84.8% of slice revenue. Proposal: show the top 5 countries outside the UK and say so on the slide. See open question 8.

Smaller adjustments:

7. The S5 cold test "revenue by month for the top country" works but has only three months. Keep it: December 2010, January 2011, February 2011. It needs a month column, which no session in the brief teaches, so S4 adds one line: `sales_clean["month"] = sales_clean["invoice_date"].dt.to_period("M")`. Expected answers are in section 4, S5.
8. A saved CSV forgets that a column was a date. After `sales_clean.csv` is loaded again in S5 to S9, `invoice_date` is text, so every load cell converts it again with `pd.to_datetime` (checked on the slice). `invoice` comes back as a whole number because no C invoices are left.
9. The brief says "ask the open items in Section 14"; the open items are in Section 15 of the brief. They are all in section 9 below, with recommendations.

What stays fixed, so later phases do not add scope:

- 10 sessions on the fixed dates. No spare slot, no extra session.
- No separate course overview deck. The S1 deck holds the course map.
- Real public data only. No synthetic data and no second dataset in the lessons.
- The project stays 3 sessions (S7 Block 2, S8, S9) plus S10.
- No machine learning, forecasting, optimisation, SQL deep dive or Power BI deep dive. SQL and Power BI get the short intro only.
- Learner materials in English. Teacher cards in Bahasa Indonesia with English technical terms. Slide text in English with Bahasa Indonesia speaker notes.
- No NUS name, logo or photo anywhere.
- No emojis, no exclamation marks, no filler words, no em-dashes.
- Solutions, teacher cards, answer keys and exit ticket answers stay in `teacher_only/`, never in the learner folders.

## 2. The data we will teach with

Full detail and every number: `data/EXPLORATION.md`.

Raw file: UCI Online Retail II, kept untouched at `data/raw/online_retail_II.xlsx`. Licence CC BY 4.0. Citation: Chen, D. (2012). Online Retail II [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5CG6D. The citation goes in the data README, the first notebook that uses the data (S4), the course outline, the course home, and the GitHub README template.

The course data file is `online_retail_ii_lesson.csv`, built in Phase 2 from the `Year 2010-2011` sheet only, with this rule:

> every row whose InvoiceDate is from 2010-12-01 00:00 up to but not including 2011-03-01 00:00.

Properties of the slice, verified:

| Property | Value |
|---|---|
| Rows | 105,335 |
| Columns | 8, original names |
| Dates | 2010-12-01 08:26 to 2011-02-28 17:04 |
| File size | 9,279,397 bytes (9.28 MB) |
| Invoices | 4,894 |
| Distinct products | 3,159 |
| Countries | 31 |
| Missing Customer ID | 36,210 (34.4%) |
| Missing Description | 304 |
| Cancellation rows | 1,904 |
| Exact duplicate rows | 975 |
| Negative quantity rows | 2,118 |
| Zero price rows | 540 |
| Negative price rows | 0 |
| Non-product code rows | 588 |
| Clean rows after the S4 steps | 101,458 |
| Clean revenue | 1,876,534.04 |

Why this window:

- It starts at the first row of the 2010-2011 sheet. S1 and S2 use the first rows; S3 adds a real January order (invoice 540815) she can find again in S4. All examples in S1 to S3 come from this slice, so the story stays one story.
- It contains the December peak, so the S6 "revenue per day" chart has a real finding instead of a flat line.
- It is one sheet, so the 9-day overlap between the two yearly sheets does not duplicate rows.
- It loads in Colab in about one second.
- 105,335 rows is enough to make cleaning and grouping feel real, and small enough that a beginner can re-run cells without waiting.

The slice is not cleaned. Cleaning is the learner's work in S4.

Data caveats that must stay true in every later material:

- Prices are in pounds sterling (GBP). Do not relabel them as dollars or rupiah.
- The slice covers 1 December 2010 to 28 February 2011 only. Do not describe it as a year of data.
- Cancellation rows are removed in S4, but the original positive sale stays in the data unless it is the one giant cancelled order. This is a real limitation: a small share of clean revenue is later cancelled. Say "about 1%" in the teacher notes, never on a learner slide.
- Rows with a missing customer ID are kept for product analysis (35,364 of the 101,458 clean rows, 34.9%). Customer-level analysis has to drop them, and the course says so.
- Lowercase stock codes are not normalised, so a few products are split across two spellings. The course does not fix this; the teacher card notes it.
- Some stock codes have more than one description: 3,066 codes but 3,107 code-description pairs in the clean slice (40 codes have more than one name). S6 uses this as the real merge lesson: the first merge takes 3,066 rows to 3,107, she finds the 41 extra rows, dedupes the names table on `stock_code`, and merges again to get 3,066.
- The data is a UK retailer: 84.82% of slice revenue is the United Kingdom. Country charts must not imply a global market.
- The December peak is real and expected for giftware. It is the S6 daily chart finding.

## 3. Verified numbers shelf

These are the numbers the materials may put on a slide, in a handout or in an answer key. All are computed from the slice unless stated. Full list in `data/EXPLORATION.md` section 12 and `data/ANSWER_KEY.md` (built in Phase 2).

| Number | Value |
|---|---|
| Slice raw rows / clean rows | 105,335 / 101,458 |
| Slice clean revenue | 1,876,534.04 |
| Class A products | 671 of 3,066 (21.9%), 79.98% of revenue |
| Class B / C products | 794 (25.9%), 1,601 (52.2%) |
| Top product | REGENCY CAKESTAND 3 TIER, 51,504.85 |
| Top 10 products, cumulative revenue share | 9.62% |
| December 2010 / January 2011 / February 2011 revenue | 775,572.23 / 593,178.39 / 507,783.42 |
| UK share of slice revenue | 84.82% |
| Top country by revenue | United Kingdom, 1,591,694.50 |
| Top countries outside the UK | Netherlands 58,182.55, EIRE 43,426.19, Germany 37,365.63, France 32,392.39, Australia 24,678.48 |
| Best day | 2010-12-07, 81,454.99 |
| Germany rows, raw / clean | 1,741 / 1,514 |
| First 7 quantities | 6, 6, 8, 6, 6, 2, 6 |
| First order line value | 6 * 2.55 = 15.299999999999999, round 15.3 |
| Second and third line values | 6 * 3.39 = 20.34, 8 * 2.75 = 22.0 |
| Products with more than one description in clean data | 40 |
| Rows with a lower-case letter in the stock code (raw slice) | 541 |
| Product rows and name pairs for the S6 merge | 3,066 product rows, 3,107 code-description pairs; the merge check goes 3,066 -> 3,107 -> 3,066 after deduping names |

## 4. Session plans

Times: 15:00 SGT, 14:00 WIB. The slot is 90 minutes. Block 1 is 35 minutes, then a 5-minute break, then Block 2. Nine sessions plan 75 minutes and keep the last 15 minutes of the slot for startup, connection trouble and overrun. S4 is the one exception: it plans 80 minutes and can use 5 minutes of that buffer because it is the heaviest session, but every session hard-stops at 90 minutes. Slides take at most 10 minutes of any session.

Every session pack contains: `student.ipynb`, `solution.ipynb`, `deck.pptx`, `deck.pdf`, `handout.pdf`, `teacher_card.md`, `exit_ticket.md`, `recall.md`. Notebook cap is 30 cells. Handout cap is 2 pages. Teacher card cap is 1 page. Deck is 6 to 10 slides.

Deck rules for all 10 decks, from the skill overrides: format `live`, no logo, English slide text, speaker notes in Bahasa Indonesia with English technical terms, code at most 6 lines in Consolas or DejaVu Sans Mono, theme chosen once in Phase 2 and reused. The S1 deck is 9 slides with a 10-minute budget: 1 minute cover and course map together, 2 minutes why Python, 1.5 minutes Colab tour, then 3 concept slides at 1.5 minutes each, 1.5 minutes errors, 1 minute Now in Colab, 1 minute homework and close. Arithmetic and round are taught live in Colab, not on a slide. Every session pack has all eight files. S10's exit ticket is two written questions in the last 3 minutes of Block 2; Bryan reads them after class and uses them in the retro.

Daily recall is planned at 3 short questions for each day between sessions, 66 questions in total across 9 recall files. Each day mixes one old topic and two new ones. In class the recall is self-marked in 2 minutes: she says the answers, then explains the one she missed. Every `recall.md` has the answers in a separate section at the end.

### How every file must be written (the style contract for Phase 3)

Teaching moves, in every notebook and teacher card:

- Start each concept from a daily life situation, then the Excel version, then 3 to 6 lines of code typed live. Then one small exercise right away. Never teach all concepts first and practise at the end.
- Use the PRIMM order for exercises: Predict on paper before running, Run, Investigate why, Modify one thing, Make something new.
- The learner always types. The teacher never types for her. Slides take at most 10 minutes of a session.
- State the limit of every analogy out loud, for example "Excel recalculates by itself, a notebook does not, run the cell again".
- One story per session. The only exception is S7, which deliberately combines three short stories (SQL, Power BI, the project question) because it is the bridge to the project. Say so in the S7 teacher card.
- The hint ladder, with 10 seconds of silence before each step: 1) what do you expect this line to do, 2) point at the line, 3) give a concept hint, 4) show the syntax pattern, not the answer, 5) do it together, then she does a similar one alone.
- For an error, read the last line first.

Code rules for every cell the learner sees:

- One step per line, saved in a clear variable name. English snake_case that says what it holds: `sales_clean`, `revenue_by_country`, `is_cancelled`.
- Rename the data columns to short lowercase names in S4 and use them from then on.
- Show the output after every important step (`head()`, `shape`, `print`).
- Use `.copy()` once after filtering, before adding columns, and explain it in one line.
- Use named functions with `.apply()`, connected to S3. Use `print(f"...")` for messages. Comments say why, never what.
- Do not use lambdas, list comprehensions, classes, decorators, try/except, `*args`, method chains longer than 2 calls, `inplace=True`, chained assignment, `.loc` tricks she has not seen, `np.where` or regex. No concept before the session that teaches it.
- No code that relies on cells run out of order. No hidden helper functions.

Notebook format:

- Max 30 cells. A short text cell before every code cell. One idea per cell.
- Exercise cells start with `# TODO`, say what to do in a comment, and the text cell above gives the expected output.
- The solution notebook is the same notebook with the answers filled in.
- Every notebook runs top to bottom on its own. In S4 she saves the clean table to Drive as `sales_clean.csv`; from S5 on, the first cells load that file and then check `sales_clean.shape` against the shape in the answer key (101,458 rows and 10 columns). A wrong shape means the file is stale or the cleaning failed, and she stops and fixes it before the lesson.
- Every notebook shows a learner action after at most two concept cells. S1 demonstrates this rule, because it is the style sample. A session where the first 15 minutes are all concept cells fails the contract.

Language and layout rules:

- Learner materials in English. Teacher card in Bahasa Indonesia with English technical terms. Slide text in English, speaker notes in Bahasa Indonesia.
- No em-dashes, no emojis, no exclamation marks, no filler words. No NUS name, logo or photo anywhere.
- Handout max 2 pages black and white. Teacher card max 1 page. Deck 6 to 10 slides. Course outline max 4 pages.

AI rules for the learner, by phase (the full text goes in `ai_rules.md`):

- S1 to S5: no AI. The S1 Colab tour shows how to turn the AI features off.
- S6 to S7: AI may explain an error or a concept but must not write the solution. She uses the prompt template "Explain this error in simple words. Do not give me the fixed code."
- S8 to S10: AI may help write code. She must explain every line, test it (row counts, one value checked by hand) and record which tool and which prompt she used.

### S1, Mon 16 Nov: Your first lines of Python

Business question: What is the sales value of one order line?

New words defined on first use: order line (one row of an invoice, one product on one receipt), variable, data type, f-string, error message.

Shape, adjusted so every concept gets a learner action inside Block 1. The brief's caps are kept: at most 10 minutes of video, 3 slides for why Python, the Colab tour, then micro-cycles.

- Block 1: 0-8 opening video (if it is longer than 8 minutes, stop at 8 and send the rest as homework; never more than 10 minutes of video in class), 8-11 why Python, 11-15 Colab tour (including 1 minute to open the shared PySC-101 Drive folder and preview the CSV so "the data" is a real file she has seen), 15-35 micro-cycles.
- The Block 1 micro-cycles, each ending with a learner action: print and variable (6 minutes: print, store in a label, print the label, then predict what changes when the value changes), three data types (6 minutes: `type()` calls, then predict the `"5" + 5` error), arithmetic, round and f-string (8 minutes: the first order line, the `15.299999999999999` moment, `round`, the f-string, then modify the price and predict again).
- Block 2: 0-10 exercises 1 and 2 (two more real order lines), 10-16 the error zoo as PRIMM (predict, run, investigate), 16-22 exercise 3 (the f-string sentence) and fix three broken cells, 22-30 exit ticket, 30-35 close.

| Concept | Daily life | Excel bridge | Limit to say out loud |
|---|---|---|---|
| print() | reading a label out loud | typing in a cell to see it | Python shows nothing unless you ask |
| variable | a label on a storage bin | a named cell | changing the label does not update other cells, run again |
| int / float / str | counting boxes / weighing goods / writing a product name | number vs text format | "5" is text, Python will not add text to a number |
| arithmetic and round | adding up a receipt | =B2*C2 and ROUND | some decimals are stored inexactly, so `6 * 2.55` prints 15.299999999999999 and money is rounded |
| f-string | a fill-in-the-blank label | ="Sold "&A2&" units" | the f before the quote is easy to forget; the braces show where the value goes |

Real data anchors (first rows of the sheet, verified): invoice 536365, WHITE HANGING HEART T-LIGHT HOLDER, quantity 6, price 2.55, value 15.299999999999999, rounded 15.3. WHITE METAL LANTERN 6 at 3.39 gives 20.34. CREAM CUPID HEARTS COAT HANGER 8 at 2.75 gives 22.0.

Notebook plan (about 25 cells, each concept followed by an action):
1. Text: what this notebook is, how to run a cell with Shift+Enter, and two rules: cells run in the order you click them, so a NameError usually means run the cells above again; NaN means an empty cell.
2. Code: `print("Hello, supply chain")` and a second print.
3. Text: what print does and its limit.
4. Code: `product_name = "WHITE HANGING HEART T-LIGHT HOLDER"`, then print it.
5. Code: `quantity = 6`, `unit_price = 2.55`, print both.
6. Text + action: predict what `print(quantity)` shows after `quantity = 7`; change it, run, put it back.
7. Code: `sales_value = quantity * unit_price`, print it. This is where 15.299999999999999 shows up.
8. Text: why the long decimal and when to round.
9. Code: `print(round(sales_value, 2))`.
10. Text + action: change `unit_price` to 3.39, predict the new value, run, compare with 20.34, then put 2.55 back.
11. Code: three `type()` calls with prints.
12. Text: three data types and the text vs number warning.
13. Text + action: predict what `"5" + 5` does, then run it and read the last line.
14. Code: the f-string sentence with the real values.
15. Text: f-string analogy and the three traps (the f, the braces, the matching quotes).
16. Text + action: modify the f-string to print the units instead of the pounds, predict, run.
17. Text + code exercise 1 (TODO): value of WHITE METAL LANTERN (expected 20.34).
18. Text + code exercise 2 (TODO): value of CREAM CUPID HEARTS COAT HANGER (expected 22.0).
19. Text + code exercise 3 (TODO): f-string sentence about the first line (expected text in the answer key).
20. Code: make a NameError on purpose and read the last line.
21. Code: make a SyntaxError (missing bracket) and read it.
22. Code: make a TypeError with `"5" + 5` and read it.
23. Text: the rule, read the last line first.
24. Text + code exercise 4 (TODO): fix three broken cells.
25. Text: recap, homework, recall plan, and the prerequisite checklist (Google account, Chrome or Edge, laptop and charger, the PySC-101 Drive folder shared with her, headset).

Deck (9 slides, budget 10 minutes): 1 cover; 2 course map with 10 sessions and how a session works (35/5/35) on one slide; 3 why Python for supply chain, three reasons; 4 Colab tour; 5 print and variable; 6 three data types; 7 arithmetic, round and f-string with one short code sample; 8 errors and how to read them; 9 Now in Colab, homework and close. Arithmetic and round are demonstrated live in Colab, not read from a slide. The 3 discussion questions for the opening video wait for Bryan's answer (open question 1).

Handout (2 pages, black and white): the six concepts with daily life, Excel bridge and limit; the code patterns; the three errors and their fixes; the exercise list with expected outputs; the first 12 real order lines from the slice (invoice 536365 plus invoice 540815) so the homework has a real source before she can open the CSV.

Teacher card (Bahasa Indonesia, 1 page): the question; the order of ideas; analogies and their limits; the two likely mistakes (forgetting the f, mismatched quotes, and the NameError that comes from not running the cells above); hint ladder for exercise 4; timing with the video slot marked.

Exit ticket: (1) predict the output of a 3-line cell that prints a value and a rounded value. (2) name the error type in one broken cell and fix it. Answers in `exit_ticket.md` under a section Bryan keeps.

Recall: 1 day (Tue 17 Nov), 3 questions mixing print, variables and types.

Homework: finish the three worksheet lines, make the three errors deliberately at home, write one f-string sentence about rows 8 to 10 on the handout.

### S2, Wed 18 Nov: Lists, product cards and decisions

Business question: Which orders are big orders?

Recall (5): three S1 questions from `recall.md`; she explains the one she missed. Warm-up (5): write the Excel formula that adds two cells and rounds the result, then predict what `print(quantity)` shows after `quantity = 12`.

Concepts: list, index from 0, `len`/`sum`/`min`/`max`, dict, comparison, if/elif/else.

| Concept | Daily life | Excel bridge | Limit |
|---|---|---|---|
| list | a row of bins on one shelf | one column of values | the first bin is number 0 |
| len, sum, min, max | count, total, smallest, largest | COUNT, SUM, MIN, MAX | same idea, different spelling |
| dict | a product card: field name (the key) to value | one row with headers | look up by the key name, not by position |
| comparison | is this more than that | =A2>10 gives TRUE or FALSE | = stores a value, == compares |
| if/elif/else | a packing rule | =IF(...) | indentation is part of the rule |

Real data anchors: the first 7 quantities [6, 6, 8, 6, 6, 2, 6]; `len` 7, `sum` 40, `min` 2, `max` 8; index 0 is 6, index 2 is 8, index -1 is 6. The product card for the first row: stock_code 85123A, description WHITE HANGING HEART T-LIGHT HOLDER, quantity 6, price 2.55, country United Kingdom. Thresholds 100 and 12 are teaching thresholds, not business rules, and the notebook says so. In this course a "big order" means one big order line, because the data records lines, not whole invoices.

Notebook plan (about 21 cells): recall prompt in a text cell; list and print; indexes; len/sum/min/max; list analogy and limit; dict and lookup; dict analogy; comparison examples (6 > 10 is False, "United Kingdom" == "United Kingdom" is True); if/elif/else with quantity 6 (small), then quantity 12 and 100 to show the branches; indentation text; exercises (predict `quantities[2]` and `quantities[-1]`, label quantity 6 and then 12 with if/elif/else, UK or outside UK); recap and homework.

Deck (9 slides, standard order): cover; today's question; list and indexes; len/sum/min/max; dict product card; comparison; if/elif/else; Now in Colab; recap and homework.

Handout: concept table; code patterns; three errors (index out of range, key error, forgetting the colon or indentation); exercises.

Teacher card: the order; two likely mistakes (counting from 1, forgetting the colon); hint ladder for the if/else exercise; timing.

Exit ticket: (1) predict `quantities[2]` (answer 8). (2) write an if/else that prints "UK" or "Outside UK" from `order_line["country"]` (first row is United Kingdom, so it prints "UK").

Recall: 4 days (Thu 19 to Sun 22 Nov), 12 questions: one old topic (print, variables or types) and two new (list, dict, if) each day.

Homework: use rows 8 to 10 on the S1 handout, add their quantities to the list and compute len, sum, min, max; write one if/elif/else about prices.

### S3, Mon 23 Nov: Do it for every row

Business question: Label every order line with one function.

Recall (5): three S2 questions from `recall.md`; she explains the one she missed. Warm-up (5): predict the output of a list index and an if/elif/else cell.

Concepts: for loop, function (`def`, `return`), the difference between print and return, reading a traceback.

| Concept | Daily life | Excel bridge | Limit |
|---|---|---|---|
| for loop | walking down the shelf, checking each bin | dragging a formula down a column | the body must be indented |
| function | your own reusable rule | your own named formula | nothing happens until you call it |
| return | the answer the rule gives back | the value the formula shows | print shows, return hands back |
| traceback | a stack of plates: the last thing placed is on top | no Excel version | Python prints the error at the bottom, so read the bottom line first and work up |

Real data anchors: the same 7 quantities; the first two order lines for the dict list; invoice 540815 as a real big order with three large lines (1930 at 2.55, 2000 at 1.85, 3114 at 2.10). `order_size(6)` is small, `order_size(250)` is big (a teaching call, not a data claim). The traceback exercise uses a real three-level error: a loop calls a function, the function compares a text quantity with a number, and Python raises a TypeError.

Notebook plan (about 21 cells): recall; for loop over quantities; loop printing values; loop with f-string labels; function definition; two calls; print vs return comparison; loop with the function; list of two real order dicts; loop over dicts; exercises: write `line_value(quantity, price)`, loop over 5 real lines and print each value, label each of those lines with `order_size`, then modify the threshold from 12 to 50 and predict what changes; traceback cell (run on purpose) and reading it; recap and homework. Counting lines is not taught here; S5 counts class A products with `.sum()`.

Deck: cover; today's question; for loop; function and return; print vs return; traceback, read from the bottom; Now in Colab; recap and homework.

Handout: concept table; code patterns; three errors (forgetting indentation, forgetting return, calling before defining); exercises.

Exit ticket: (1) find the bug in a function that prints instead of returning. (2) read a 3-level traceback and say which line broke.

Recall: 2 days (Tue 24, Wed 25 Nov), 6 questions mixing S1 to S3.

Homework: write `line_value` and use it on the 5 real lines on the handout; one function of her own with a return.

### S4, Thu 26 Nov: From one row to the whole file (heaviest session)

Business question: Clean the data and compute revenue.

Recall (5): three S3 questions from `recall.md`; she explains the one she missed. Warm-up (5): predict what `sales.shape` will print and write the Excel filter that keeps only Germany.

Block 1: load and look. Block 2: clean and compute. S4 is the one session that plans 80 minutes inside the 90-minute slot; it hard-stops at 90.

- Block 1 (35): 0-5 recall, 5-10 warm-up, 10-20 load the file and look (`read_csv`, `head`, `shape`), 20-27 missing values and rename with the dict, 27-32 `info` and the new words (NaN, boolean filter, `&` not `and`), 32-35 cleaning log setup. `describe` moves to the handout and homework, where it is shown as the same "look first" habit with one summary line.
- Block 2 (40): 0-8 boolean filter and new column (two micro-cycles, she types), 8-17 she drives the cleaning steps with hints only (drop duplicates, remove C invoices, keep quantity above 0, keep price above 0, keep product codes), 17-25 revenue, date conversion, month column and sort top 10, 25-31 the cancelled order investigation, 31-37 exit ticket, 37-40 cleaning log review, homework and close.
- If the session runs late, the giant order investigation moves to the first 5 minutes of S5, where it explains the ABC ranking. The core of S4 is load, rename, clean, revenue and sort. If `describe` or the big revenue exercise is cut, they are handout and homework.

Concepts: pandas and DataFrame, `read_csv`, `head`/`shape`/`info`/`describe`, rename with a dict, boolean filter, new column, `sort_values`, dates.

| Concept | Daily life | Excel bridge | Limit |
|---|---|---|---|
| pandas, DataFrame | the whole warehouse list | a sheet | columns have one data type each |
| read_csv | opening the file | File, Open | the path must be exact |
| head, shape, info, describe | first page, page count, cover | scrolling, COUNTA, status bar | looking first is part of the job |
| rename with a dict | relabelling bins | editing headers | uses the dict idea from S2 |
| boolean filter | keeping only the good boxes | helper column, then Filter | the original table does not change unless you save the result; use `&`, not `and`, and put each condition in brackets |
| new column | writing the value on each box | a formula column | no auto-update, run the cell again |
| sort_values | biggest boxes in front | Sort Z to A | same as Excel |
| date column | a calendar column | an Excel date cell | the column must be a real date before you group by month or day |
| text column operation | the first letter of a product code | LEFT() in Excel | a code is text, so take the first character with `.str[0]` |
| copy | Save As with a new name | Save As | changing the copy cannot change the original |
| missing value (NaN) | an empty cell on the form | an empty cell | NaN means empty, and `isna()` counts it |

Real data anchors:

- Load path in Colab: `/content/drive/MyDrive/PySC-101/data/online_retail_ii_lesson.csv`.
- Raw `sales.shape` is (105335, 8).
- Missing values: Description 304, Customer ID 36,210, all other columns 0. `Customer ID` shows NaN because it is empty for those rows.
- Column names after rename: invoice, stock_code, description, quantity, invoice_date, price, customer_id, country.
- Cleaning steps and row counts: 105,335 start; 104,360 after `drop_duplicates`; 102,471 after removing C invoices; 102,257 after `quantity > 0`; 101,933 after `price > 0`; 101,459 after keeping only product codes; 101,458 after removing invoice 541431. The learner writes each number in the cleaning log text cell.
- Non-product rule in code: `first_character = sales_clean["stock_code"].str[0]`, then `is_product_code = first_character.str.isdigit()`, then keep the true rows with the boolean filter she already knows. Three short lines, no list to mistype.
- The clean table gains two columns: `revenue = quantity * price` and `month = invoice_date.dt.to_period("M")`. `pd.to_datetime` turns the text into a real date; without it the `.dt` part does not work. `dt.to_period("M")` means "make a month from a date; M keeps the year too". Final shape (101458, 10). The month column is what makes the S5 cold test and the S6 charts possible.
- Cleaning log habit: one row count per step, checked against `sales_clean.shape` at the end.
- Decision to discuss: do we drop rows with a missing customer_id? For product analysis no (we keep 101,458 rows and lose 34.9% of rows if we drop). For customer analysis yes.
- Before the C rows are dropped, save them for the project menu: `cancellations = sales[sales["invoice"].astype(str).str.startswith("C")]`. Project question 3 needs these rows later. The C prefix is the business rule for a cancellation: the invoice number starts with C.
- The cancelled giant order investigation: `sales_clean.sort_values("revenue", ascending=False).head(10)` shows invoice 541431 at 77,183.60. She checks the raw rows, finds C541433 cancelling the same 74,215 units 16 minutes later, and removes invoice 541431 with one commented line. If Bryan chooses to keep it, the numbers are in `data/EXPLORATION.md` section 12.
- Exit ticket Germany filter on the clean table gives 1,514 rows.

Notebook plan (about 28 cells): import pandas and mount Drive; read the CSV; head; shape; missing values; rename with the dict; check columns; text cell with the cleaning log table; save `cancellations` before dropping C rows; drop duplicates and log; remove C invoices and log; quantity > 0 and log; price > 0 and log; keep only product codes and log; `.copy()` with the Save As sentence; revenue column; `pd.to_datetime`; month column; sort top 10; the giant order investigation (2 cells and 1 text cell); final shape and log; save `sales_clean.csv` and `cancellations.csv` to Drive; exercises (filter Germany, filter big revenue lines); recap and homework.

Deck (10 slides): cover; today's question; the whole sheet in Python (pandas and DataFrame); open and look; rename with a dict; keep only the good rows (boolean filter); write a new column; sort; Now in Colab (notebook name); recap and homework. The cancelled order investigation is teacher-led in the notebook and goes in the speaker notes, not on a slide.

Handout: concept table; code patterns including the bracketed `&` filter; three errors (file not found, KeyError after rename, the `and` / `&` error); the cleaning step checklist; `describe` explained; exercise list.

Teacher card: the Block 1 and Block 2 split; the two likely mistakes (wrong Drive path, forgetting to reassign after filtering); hint ladder for the Germany filter; the giant order investigation points to the solved cell in `solution.ipynb` instead of repeating the script; S4 plans 80 minutes and hard-stops at 90.

Exit ticket: (1) what `sales.shape` tells you (rows and columns; expected (105335, 8) at load and (101458, 10) after cleaning, revenue and month). (2) write a filter that keeps only rows from Germany (answer 1,514 rows on the clean table).

Recall: 3 days (Fri 27 to Sun 29 Nov), 9 questions mixing S2 to S4, with at least one pandas question each day and one month question for the S5 cold test.

Homework: re-run the notebook; write the cleaning log in her own words; bring one question about the cancelled order.

### S5, Mon 30 Nov: Which products matter, plus cold test 1

Business question: Which products drive most of the value?

Recall (5): three S4 questions from `recall.md`, including one month question; she explains the one she missed. Warm-up (5): write the Excel PivotTable steps that would total revenue by product.

Block 1 (35): 0-5 recall, 5-10 warm-up, 10-20 groupby, sort and reset_index, 20-27 cumsum and cumulative share, 27-35 abc_class and apply. `value_counts` and revenue by country are 2-minute copy-alongs at the end; if the block runs late they become homework, because Block 2 is the cold test and must not be cut.

Concepts: `groupby` with `sum`, `cumsum`, ABC analysis with a function, `.apply` with a named function.

| Concept | Daily life | Excel bridge | Limit |
|---|---|---|---|
| groupby + sum | sorting receipts into piles then adding each pile | PivotTable | the result carries an extra row label (the index), like a PivotTable with one label column; reset_index() turns it back into a normal table |
| cumsum | a running total on a receipt roll | =SUM($B$2:B2) dragged down | sort first or the running total is meaningless |
| ABC analysis | few items take most of the space and money | sort, running % column, IF | 80/95 is a rule of thumb, not a law |
| .apply(function) | using the S3 rule on every row | dragging your formula down | use a named function, not a lambda |

Real data anchors: 3,066 products; class A 671 products (21.9%) with 79.98% of revenue; class B 794 (25.9%) with 15.02%; class C 1,601 (52.2%) with 5.00%. Top product REGENCY CAKESTAND 3 TIER 51,504.85. Key finding for the deck: "22% of the products bring 80% of the revenue." The slide uses the rounded 22% and 80%; the exact 21.9% and 79.98% stay in the speaker notes and the answer key.

Block 2 is the cold test. Exact split: 0-20 cold test, notes allowed, Bryan silent; 20-25 look at one solution together; 25-32 exit ticket; 32-35 homework and close. Question: revenue by month for the top country, using the month column she built in S4. Expected answers: United Kingdom; December 2010 705,166.72; January 2011 468,651.61; February 2011 417,876.17. Rubric: runs (1), correct numbers (1), clear names (1), one sentence of meaning (1). Bryan grades the cold test after class and records the result next to the exit ticket scores.

Notebook plan (about 24 cells): import pandas and load `sales_clean.csv` from Drive (2 cells); recall; revenue by product; sort; reset_index; total revenue; cumsum; cumulative share; abc_class function; apply; value_counts; revenue by country; exercise (find a B product, then count class A products with `(product_value["abc_class"] == "A").sum()`); save `product_value.csv` to Drive for the S7 Power BI export; cold test section with the question and a blank cell; recap and homework.

Deck (9 slides): cover; today's question; groupby is a PivotTable; running total with cumsum; ABC with a function; the finding slide with the real number and one chart (22% of products, 80% of revenue); Now in Colab and cold test; recap; homework and recall.

Handout: groupby and cumsum patterns; the ABC function; the cold test rubric; three errors (forgetting reset_index, sorting after cumsum, apply with a lambda).

Teacher card: how to run the cold test (silent, notes allowed, grade after); the two likely mistakes; hint ladder; timing.

Exit ticket: (1) what class would a product with cumulative share 0.90 be (B). (2) write one sentence that explains the 80/20 finding in plain words. The class A count uses `.sum()`, which was taught in S2.

Recall: 2 days (Tue 1, Wed 2 Dec), 6 questions mixing S3 to S5.

Homework: finish the country analysis and the value_counts example if they were cut; write her own abc_class sentence; prepare for the cold test discussion.

### S6, Thu 3 Dec: Show it clearly

Business question: How do we show it clearly?

Recall (5): three S5 questions from `recall.md`; she explains the one she missed. Warm-up (5): sketch on paper the chart you would show a manager for "which products matter" and label its axes.

Block 1 (35): 0-5 recall, 5-10 warm-up, 10-22 merge with the real row-count lesson, 22-32 top 10 table and the horizontal bar chart, 32-35 the title rule.

Block 2 (35): 0-10 daily revenue table and the line chart, 10-18 the cumulative share curve as a copy-along pattern (this is the second cut: if the room is behind, it moves to homework), 18-22 the chart-fix exercise, 22-30 exit ticket, 30-35 close, homework and the case hunt handout.

Default plan: two matplotlib charts in class, the top 10 bar and the daily line. The cumulative curve is a copy-along if time allows. Seaborn is homework by default, with the copy-pattern and an expected image on handout page 2; it is the bonus content and the first thing the brief's cut order removes.

Concepts: merge (VLOOKUP), matplotlib, seaborn (bonus, homework by default), chart titles that state the finding.

| Concept | Daily life | Excel bridge | Limit |
|---|---|---|---|
| merge | matching a packing list to a product catalogue | VLOOKUP or XLOOKUP | check row counts before and after; if the key is not unique on the right, one row matches several and the table grows |
| matplotlib | drawing a chart by hand, step by step | Insert Chart, then edit each part | every chart needs a title and axis labels |
| seaborn | a chart template on top of matplotlib | chart styles | built on matplotlib, labels and titles still work |

Real data anchors: the clean slice has 3,066 product codes but 3,107 code-description pairs, because 40 codes have more than one name. The first merge of the 3,066-row product table with a names table built with `drop_duplicates()` (both columns) gives 3,107 rows. That is the real lesson: she finds the 41 extra rows, dedupes the names table on `stock_code`, and merges again to get 3,066. Top 10 products cumulative share is 9.62%. Daily revenue peaks on 2010-12-07 at 81,454.99. The top 5 countries outside the UK are Netherlands 58,182.55, EIRE 43,426.19, Germany 37,365.63, France 32,392.39, Australia 24,678.48. Chart titles should state the finding: "The biggest 10 products are still only 9.6% of revenue", "Revenue peaked in the first week of December", "22% of products bring 80% of revenue", "Outside the UK, the Netherlands and Ireland lead".

Case hunt is handed out and explained in the last 5 minutes. It is homework due in S8, one page, 5 points, and Bryan does not find cases for her. The teacher card has two prepared fallback cases in case she does not find one.

Notebook plan (about 25 cells): import pandas and load `sales_clean.csv` from Drive (2 cells); recall; product names table with `drop_duplicates()`; merge and row count 3,066 to 3,107; find and explain the 41 extra rows; dedupe names on `stock_code`; merge again and check 3,066; top 10 table; horizontal bar chart; daily revenue table with `.dt.date` as a 3-minute copy-along; line chart; product rank and cumulative share curve (copy-along); seaborn bar chart for non-UK countries as a homework pattern in the notebook; chart title rule; chart-fix exercise; recap, case hunt and homework.

Deck (9 slides): cover; today's question; merge is VLOOKUP, with the row-count check; matplotlib, one chart step by step; the title says the finding; seaborn template; Now in Colab; the case hunt; recap and homework.

Handout: merge check pattern; a chart recipe block (`plt.figure(figsize=...)`, the bar or line call, `plt.title`, `plt.xlabel`, `plt.ylabel`, `plt.tight_layout()`, `plt.xticks(rotation=45)` when labels are long, `plt.show()`); three chart mistakes; the seaborn homework pattern and expected image; the case hunt template on page 2.

Teacher card: the row-count lesson (3,066 to 3,107 to 3,066); two likely mistakes (forgetting the key, calling `plt.show()` twice); hint ladder for the horizontal bar chart; case hunt explanation and the two fallback cases; the cut order reminder.

Exit ticket: (1) your merge took 3,066 rows to 3,107 rows. What happened and how do you fix it? (2) write a title for the daily revenue chart that states the finding.

Recall: 3 days (Fri 4 to Sun 6 Dec), 9 questions mixing S4 to S6.

Homework: finish the top 10 chart; do the seaborn copy-pattern; start the case hunt (due S8); install Power BI Desktop on the Windows laptop before S7.

### S7, Mon 7 Dec: Other tools, then your own question

Block 1 (35): 0-5 recall S6, 5-10 paper warm-up (write one question a manager might ask about this data), 10-25 SQL taste (15 minutes: setup plus two queries; the third query lives in `sql_playground.md`), 25-32 Power BI teacher demo (7 minutes; she watches and builds the same chart at home with `intro_powerbi.md`), 32-35 exit ticket. Block 2 (35): 0-6 what makes a good analyst question, 6-12 pick from the menu, 12-24 fill `project_plan.md`, 24-32 presentation guide walk-through (3 content slides plus cover and thank-you, answer first, scoring sheet), 32-35 close and homework.

If the cut order after S4 has been triggered, the two intro guides become 1-page self-study homework: she reads `intro_sql.md` and `intro_powerbi.md` before the session and the 35-minute Block 1 slot goes to the project kickoff instead. Block 2 then continues the project plan and the first analysis.

SQL anchors from the slice: the pandas table is `sales_clean[["invoice", "stock_code", "description", "quantity", "price", "country", "revenue"]]`; the top 5 countries query returns United Kingdom 1,591,694.50, Netherlands 58,182.55, EIRE 43,426.19, Germany 37,365.63, France 32,392.39; the Germany query returns 37,365.63; the top 10 revenue rows query shows the same top rows as the pandas answer.

Power BI: installing Power BI Desktop is S6 homework, because it must happen before S7. In S7 the teacher shows the steps on the share screen for 7 minutes: open Power BI, get data from the `product_value.csv` she saved in S5, build one bar chart and one card, save the file. She repeats it at home with `intro_powerbi.md` and sends a screenshot.

Block 2: what makes a good analyst question (specific, answerable with this data, useful to a manager); she picks a question and fills `project_plan.md` (question, columns needed, steps, expected chart, what decision it helps); 8 minutes for the presentation guide walk-through.

Project menu, rescoped so every question is answerable with what she has been taught (one groupby key, one filter, one chart):
1. Is class A revenue stable month to month? Filter the class A products, group by month, draw one line chart. The slice has three months.
2. Which non-UK country buys the most, and what are its top 5 products? Filter one country, group by product, one bar chart. 30 non-UK countries are present.
3. How big are cancellations, and which products get cancelled most? She uses the `cancellations.csv` she saved in S4; the slice has 1,904 cancellation rows.
4. Reorder point for the top 5 products, with assumptions she chooses (lead time in days, safety stock percentage). The slice has 68 trading days, which goes into `project_plan.md`; the numbers are labelled as assumptions, not data.

If a question needs a skill we did not teach, we change the question, not the skill.

An Olist note goes in `project_plan.md` as an optional idea only, with a licence check reminder.

Notebook plan (about 22 cells): import pandas and load `sales_clean.csv` from Drive (2 cells); SQL setup with sqlite3; the same table; two queries live, each next to its pandas version; the third query as a homework cell; reading the result; Power BI steps as text plus a small export cell that loads `product_value.csv`; the project question template; a checklist cell.

Deck (9 slides): cover; today's question (what question will I answer); SQL and pandas side by side; SQL query patterns; Power BI in three clicks; what makes a good question; project plan template; Now in Colab and project kickoff; homework.

Handout: SQL query sheet and pandas equivalents; Power BI steps; project plan template with the 68 trading days and the reorder formula as labelled assumptions. `intro_sql.md`, `sql_playground.md`, `intro_powerbi.md` cover the self-study path if the bonus is cut.

Teacher card: the 35/35 split with a hard stop; two likely mistakes (forgetting the connection, exporting the wrong table); how to steer a vague project question; the Power BI screenshot check for the next session.

Exit ticket: (1) read a short SQL query and say what it returns. (2) write your project question in one sentence and one column it needs. Answers in `exit_ticket.md`.

Recall: 2 days (Tue 8, Wed 9 Dec), 6 questions mixing S5 to S7 plus one SQL reading question.

Homework: build the Power BI chart at home with `intro_powerbi.md` and send a screenshot; finish the project plan; start the first analysis.

### S8, Thu 10 Dec: Project work 1

Shape from the brief: 0-10 case hunt discussion (she presents her case in 2 minutes and finds one link to our data), 10-35 project work with the hint ladder only. Break. Block 2: 0-22 project work; 22-30 exit ticket; 30-35 "what I found so far" in 3 sentences. S8 has no paper warm-up; the case discussion is the opener.

AI rule from here: AI may help, but she explains and tests every line, and records the tool and the prompt in `project_plan.md` or a small AI log.

Notebook plan (about 17 cells): load `sales_clean.csv` from Drive; project checklist; her question restated in her own words; the columns she needs; the first analysis cell; chart draft; the 3-sentence status; the AI log table.

Deck (7 slides): cover; today's question (her question); case hunt discussion; project checklist; AI rules; Now in Colab; what I found so far.

Handout: project checklist and the 3-sentence template; AI log table.

Teacher card: how to use the hint ladder without taking the keyboard; two likely mistakes (scope too big, jumping to a chart before checking the numbers); how to keep the session silent.

Exit ticket: (1) your question in one sentence. (2) one number you have checked by hand and how you checked it. The 3-sentence status is the closing.

Recall: 3 days (Fri 11 to Sun 13 Dec), 9 questions mixing S6 to S8 and her project. If the project is behind, the teacher may drop to 2 questions a day that week and say so.

Homework: continue the project analysis; create the GitHub account and an empty repository at home with the one-page guide (do not upload the notebook yet); finish the case hunt if not done.

### S9, Mon 14 Dec: Project work 2 and sharing

Block 1 (35): 0-25 final charts and the 3-sentence conclusion (answer, evidence, recommendation); 25-33 she writes the finding and recommendation sentences, which are also the exit ticket; 33-35 close and reflection handout. Block 2 (35): 0-12 GitHub in the browser using the account and empty repository she made at home (Colab File > Save a copy in GitHub for the notebook, then write the README in the browser); 12-33 start her 3 slides from `presentation_template.pptx`; 33-35 finish and homework. The self-reflection is handed out at the end of Block 1 and is due before S10.

If the project is behind, the minimum for S9 is the GitHub upload, one chart and one finding sentence. The slides can be finished as homework.

Notebook plan (about 15 cells): load `sales_clean.csv` from Drive; final chart checklist; the 3-sentence conclusion template; the GitHub steps as text; README template; the slide template walkthrough; reflection questions.

Deck (7 slides): cover; today's question (can I explain the finding in three sentences); final chart checklist; GitHub in the browser; README template; the 3 slides; reflection.

Handout: 3-sentence template, GitHub steps, README template, reflection questions.

Teacher card: GitHub in the browser, she does every click and the account already exists from S8 homework; use Colab File > Save a copy in GitHub; two likely mistakes (the repository is private when it should be public, README missing the data credit); one sentence on public versus private and why this repo can be public (public data, no personal data); how to keep the conclusion to 3 sentences.

Exit ticket: (1) write your finding in one sentence (answer first). (2) write your recommendation in one sentence. The reflection handout is the closing.

Recall: 2 days (Tue 15, Wed 16 Dec), 6 questions mixing S7 to S9 and her presentation content. If the project and slides are behind, the teacher may drop to 2 questions a day and say so.

Homework: finish slides, rehearse the 5-minute presentation once, complete the reflection.

### S10, Thu 17 Dec: Show what you can do

0 to 5 setup and nerves check. 5 to 10 her presentation (5 minutes). 10 to 25 interview-style Q&A. 25 to 35 feedback with the scoring sheet (2 strengths, 1 thing to improve). Break. Block 2: 0-15 review the reflection together; 15-25 course retro (keep, stop, start); 25-28 next steps for January (optional module outline only); 28-35 exit ticket and close, which gives the two written answers 7 minutes.

Presentation format: 3 content slides (question, finding, recommendation) plus cover and thank-you, built from `presentation_template.pptx`. 5-minute structure: 1 minute question and context, 2 minutes finding and evidence, 1 minute recommendation, 1 minute of margin. Slides are in English; she may present in English or Bahasa Indonesia. Delivery is scored on structure and pace, not accent. The 2-minute "walk me through your project" version is only for the Q&A.

Q&A questions: walk me through your project in 2 minutes; why did you remove those rows; what would you do with more time; how did you check the numbers; if you used AI, how did you check its code and what did you record.

Scoring sheet: clarity, evidence, recommendation and delivery, each 1 to 4, with one-line anchors for 1, 2, 3 and 4 in `presentation_scoring.md`. The project 30% is scored 10/10/10 on question and plan, analysis and checked numbers, chart and finding. The cold test is scored out of 4 and accepts values within 0.01 of the answer key. The reflection is complete, partial or missing across all six questions.

Notebook plan (about 10 cells): presentation checklist; Q&A notes; feedback notes; retro keep/stop/start; reflection review; next steps.

Deck (6 slides): cover; agenda; Q&A rules; retro keep, stop, start; what next; thank you.

Handout: presentation scoring sheet and the Q&A question list.

Teacher card: timing with a visible clock; two likely nerves mistakes (reading slides, apologising); feedback sentence starters.

Exit ticket: (1) what can you do now that you could not do in November. (2) one thing you would do differently in the project. Bryan reads both after class, together with the presentation scoring sheet.

Recall: no daily recall after S10. S10's `recall.md` is a short optional practice sheet for January instead, 3 questions with answers.

## 5. Course-wide deliverables

| File | Content | Phase |
|---|---|---|
| `course_home/course_outline.docx` and `.pdf` | 4 pages maximum, black and white, no NUS branding, 7 sections as brief section 11, schedule table, assessment weights, AI honesty section | 2 |
| `course_home/course_home.docx` | single page she opens: schedule, links per session, recall, case hunt, AI rules | 4 |
| `course_home/teacher_guide.md` | Bahasa Indonesia: hint ladder, feedback rules, wait 10 seconds, overload signal, cut order, cold test instructions | 4 |
| `course_home/ai_rules.md` | the three phases of AI rules and the prompt template for S6 to S7 | 4 |
| `course_home/case_hunt_template.md` | 5 points, one page | 4 |
| `course_home/reflection_template.md` | 6 questions, one page | 4 |
| `course_home/project_plan.md` | question, columns, steps, chart, decision; the rescoped project menu; 68 trading days, clean revenue and the reorder formula as labelled assumptions; Olist note | 4 |
| `course_home/presentation_guide.md` | answer first, 3 content slides plus cover and thank-you, the 5-minute structure, numbers in plain words, the 2-minute Q&A script | 4 |
| `course_home/presentation_scoring.md` | clarity, evidence, recommendation, delivery, each 1 to 4 with one-line anchors; project 10/10/10; cold test out of 4 with 0.01 tolerance; reflection complete, partial or missing | 4 |
| `course_home/intro_sql.md`, `sql_playground.md`, `intro_powerbi.md` | 1 page each, the self-study versions of the S7 bonus | 4 |
| `course_home/presentation_template.pptx` | cover, question, finding, recommendation, thank you, same theme | 2 with the theme, filled in 4 |
| `course_home/glossary.md` | about 25 English terms with a one-line Bahasa Indonesia explanation (DataFrame, index, boolean, traceback, repository, README, NaN, CSV, and the rest) | 4 |
| `course_home/optional_jan_module.md` | outline only: deeper Power BI, SQL lessons, VS Code, git command line | 4 |
| `data/online_retail_ii_lesson.csv` | the slice | 2 |
| `data/EXPLORATION.md` | this phase's report | 1 |
| `data/ANSWER_KEY.md` | every expected number for every exercise, computed from the slice | 2 (S1 to S3), extended per phase |
| `data/README.md` | source, licence, citation, columns, slice rule | 2 |
| `PUSH_LIST.md` | per session, which files to upload and by when (the day before) | 4 |

### Course outline content plan (built in Phase 2)

Header fields: course code PySC-101; title Python for Supply Chain Analytics; class dates 16/11/2026 to 17/12/2026; online, 10 sessions, 15:00 SGT (14:00 WIB), 90-minute slot; instructor Bryan Kusno; email placeholder until open question 4 is answered. No NUS name, logo or branding. Black and white, plain, 4 pages maximum.

Five objectives and where they are taught:

| Objective | Sessions |
|---|---|
| Read and fix common Python errors | S1, S3, every session's error habit |
| Load, inspect and clean a real CSV with pandas | S4 |
| Summarise with groupby and classify products with ABC | S5 |
| Build clear charts with matplotlib and seaborn | S6 |
| Present a finding in 5 minutes, answer first | S7 to S10 |

Assessment table as the brief fixes it: class participation and daily recall 20%, cold test 15%, project 30%, final presentation 20%, self-reflection 15%, total 100%. One line says the course is not graded and the weights show what matters most. The scoring detail: presentation criteria with one-line anchors, project 10/10/10 (question and plan, analysis and checked numbers, chart and finding), cold test out of 4 with a 0.01 tolerance, reflection complete, partial or missing. The outline states that slides are in English, she may present in English or Bahasa Indonesia, and delivery is scored on structure and pace, not accent.

Schedule table: 10 rows, one per session, with lesson number, date, session summary and objectives, resources and indicative deadlines. Resources are only what we really provide: notebook, handout, deck, the S1 opening video, the dataset citation, sql-practice.com for S7, and the templates. Deadlines: cold test in S5; case hunt handed out in S6 and due in S8; project plan in S7; project and GitHub in S9; reflection before S10; presentation in S10.

## 6. Delivery structure

```
PySC-101/
  00_course_home/   course_home, course_outline, learner guides, templates
  data/             online_retail_ii_lesson.csv only (never the raw file)
  week_1/           S1, S2: student notebook, deck PDF, handout, recall
  week_2/           S3, S4
  week_3/           S5, S6
  week_4/           S7, S8, S9, S10
teacher_only/       solutions, teacher cards, answer keys, deck PPTX, exit ticket
                    answers, raw data for Bryan, PUSH_LIST source
```

Week mapping: week 1 = 16 and 18 Nov; week 2 = 23 and 26 Nov; week 3 = 30 Nov and 3 Dec; week 4 = 7, 10, 14, 17 Dec.

PUSH_LIST dates, always the day before the session: S1 by 15 Nov, S2 by 17 Nov, S3 by 22 Nov, S4 by 25 Nov, S5 by 29 Nov, S6 by 2 Dec, S7 by 6 Dec, S8 by 9 Dec, S9 by 13 Dec, S10 by 16 Dec. Course home and course outline and the data slice by 14 Nov.

The raw xlsx never goes to Drive for the learner. The lesson CSV is the only data file in her folders. Internal scratch is not delivered: `_tools/` (venv, extracted skill, scripts, runbook), `_verify/` (independent verification), `data/work/` (full CSV conversions and the slice working copy).

## 7. Build order and quality gates

Phase 2, S1 pilot:
1. Lead writes `_tools/build_slice.py`, generates `data/online_retail_ii_lesson.csv` from the raw sheet with it, checks the row count and first rows against `data/EXPLORATION.md`, and writes `data/README.md`.
2. Lead writes `data/ANSWER_KEY.md` for S1 to S3 with every expected value, computed from the slice.
3. Lead builds S1 `student.ipynb` and `solution.ipynb` and runs both top to bottom in a fresh kernel.
4. Deck builder runs the ppt-maker theme preview with 3 real S1 slides in 5 variants: L, L:soft, D, M:center, E:hard. Bryan picks theme, tone and alignment once.
5. Lead builds the S1 deck with the chosen variant, renders and audits it, and looks at every page image.
6. Lead builds S1 handout, teacher card, exit ticket, recall.
7. Lead builds `course_outline.docx` and `.pdf` with the placeholder email until Bryan answers.
8. STOP. Bryan reviews S1 as the style sample. His feedback applies to every later session.

### Phase 2 acceptance checklist (what Bryan should be able to check in 20 minutes)

Data and numbers:
- `data/online_retail_ii_lesson.csv` exists, 105,335 rows, 8 columns, same column names as the raw file, uncleaned.
- `data/README.md` has the citation, licence, download URL, checksum and the slice rule.
- `data/ANSWER_KEY.md` covers every S1, S2 and S3 exercise with the expected value and the exact code that produces it.

S1 learner files:
- `student.ipynb` runs top to bottom in a fresh Colab or Jupyter kernel, has at most 30 cells, and has a short text cell before each code cell.
- Exercise cells are marked `# TODO`, state what to do, and show the expected output in the text cell above them.
- `solution.ipynb` is the same notebook with the answers filled in; every output matches the answer key.
- The opening video section says the video link, where to stop, and (once Bryan answers) the 3 discussion questions.
- The Colab section says how to open the notebook from Drive, how to run a cell, and how to turn off the AI features.
- The error zoo has the three errors from the brief and the rule "read the last line first".

S1 materials:
- `deck.pptx` and `deck.pdf`: 6 to 10 slides, theme, tone and alignment from the Phase 2 choice, no NUS logo, English slide text, Bahasa Indonesia speaker notes, code at most 6 lines per slide. `render.py` embeds Proxima Nova and `audit.py --format live` is clean except word-count warnings we have already cut.
- `handout.pdf`: 2 pages maximum, black and white, concept table, Excel bridge and limit, code patterns, 3 errors with fixes, exercise list.
- `teacher_card.md`: 1 page, Bahasa Indonesia with English terms, the question, key ideas in order, analogies and limits, 2 likely mistakes, hint ladder, timing.
- `exit_ticket.md`: 2 questions and an answers section Bryan keeps.
- `recall.md`: 3 questions for Tue 17 Nov, answers in a separate section at the end.
- Every file uses only concepts from S1, has no em-dash, no emoji, no exclamation mark and no banned filler word.

Course outline:
- `course_outline.docx` and `.pdf`: 4 pages maximum, black and white, the 7 sections, the assessment weights, the schedule table and the email placeholder visible if open question 4 is still unanswered.

Bryan's style decision at this STOP:
- Is the density right for a first session?
- Is the code style the one he wants for all 10 sessions?
- Are the analogies and their limits the right level?
- Is the tone of the teacher card right?
- Anything to change before the other 9 sessions repeat it?

The answer to these five questions is the style contract for Phase 3.

Phase 3, S2 to S10, one session at a time, each with the master brief section 13 checks and the quality gate below. After S4, show S2 to S4 together and STOP for a quick check.

Phase 4, course-wide files, then Phase 5, final check and summary.

Environment notes for every deck session (verified on 2 Nov 2026 by the deck toolchain check):
- PATH must include /opt/homebrew/bin so `soffice`, `pdftoppm` and `pdffonts` are found.
- Our copy of `_tools/ppt_maker/ppt-maker/scripts/render.py` is patched in two places: the LibreOffice profile comes from `PPT_MAKER_PROFILE` and defaults inside the repo, and the profile URL uses `as_uri()` because the repo path contains spaces. Do not revert these.
- Always make the PDF with the patched `render.py`, not with the `--pdf` option inside a build script. `render.py` also embeds Proxima Nova and prints the font check.
- Set `MPLCONFIGDIR` to a repo folder only when a build draws a matplotlib figure.
- The exact commands and outputs are in `_tools/deck_check/RUNBOOK.txt`.
- The theme preview test built 15 pages in 5 variants (L, L:soft, D, M, E:hard) and rendered them with Proxima Nova embedded. For the real S1 preview in Phase 2 use L, L:soft, D, M:center, E:hard: the brief asks for at least one centered variant, so M is replaced by M:center.

Quality gate per session, from the brief section 13:
1. Run `student.ipynb` and `solution.ipynb` top to bottom in a fresh kernel; no errors.
2. Every expected output matches `ANSWER_KEY.md`.
3. Every exercise uses only concepts taught so far, and the notebook has a learner action after at most two concept cells; exceptions listed.
4. Caps: notebook cells (30), handout pages (2), teacher card (1 page), deck (6 to 10 slides, one idea per slide, at most 10 minutes of class).
5. `render.py` and `audit.py` run; every slide image is looked at. Code slides may warn on visible word count; we cut words or lines until the warning is gone, we do not ignore it.
6. Read the learner material as a non-programmer; remove anything a layperson would not understand.
7. No em-dashes, no emojis, no banned filler words, no exclamation marks.
8. No NUS branding anywhere.

## 8. Team build plan

The workspace is shared. Write scopes are disjoint and recorded on the task board.

| Member | Owns | Write scope |
|---|---|---|
| Lead | data slice, ANSWER_KEY, S1 notebook and style sample, course outline, final QA, decisions | `data/`, `sessions/s01_*`, `course_home/course_outline*`, `PLAN.md`, `PUSH_LIST.md` |
| Notebook builder (after S1 approved) | `student.ipynb` and `solution.ipynb` for S2 to S10, from the Lead's outline and the answer key, run top to bottom | `sessions/sXX_*/student.ipynb`, `sessions/sXX_*/solution.ipynb` |
| Deck builder | theme preview, all 10 decks and PDFs, `presentation_template.pptx` | `sessions/sXX_*/deck*`, `course_home/presentation_template*` |
| Materials writer | handouts, teacher cards, exit tickets, recall files, learner guides and templates | `sessions/sXX_*/handout*`, `teacher_card.md`, `exit_ticket.md`, `recall.md`, `course_home/*.md` |
| Verifier | independent run of every notebook, cap check, number check against the answer key, `_tools/fact_check.py` run, deck render check | read only, reports to Lead |

Rules for the team: the Lead does not present a session as done until the quality gate passes. Results, numbers and code cells come from the Lead. Styles (fonts, titles, code comments) come from the S1 style sample. No teammate downloads images without Bryan's approval.

## 9. Open questions for Bryan

These block or shape Phase 2. Recommendations are in the last column.

| # | Question | Recommendation | Needed by |
|---|---|---|---|
| 1 | Opening video: what is it about and how long is it? We cannot watch it and must not guess its content. The link is https://youtu.be/Nxy_UROEkd4?si=a7To3M4s_K6fd9Z4 | Send topic and length. If it is longer than 10 minutes, we show the first 10 in class and send the rest as homework, and we write 3 discussion questions from the topic | Phase 2, S1 deck |
| 2 | S2 is Wed 18 Nov, not Thu 19 Nov. Confirm | Confirm. All 10 dates are checked against the 2026 calendar and the weekdays match | Phase 2 |
| 3 | Is 14:00 WIB safe for her schedule (public speaking class, family)? | Confirm | Phase 2 |
| 4 | Which email goes in the course outline header? | Reply with the address | Phase 2, outline |
| 5 | May we search and download openly licensed photos (Wikimedia Commons, Openverse) for the decks? We would credit each photo on the slide and use no NUS logo | Yes, with credit, only where a photo teaches something (warehouse, shelves, shipping, receipts). If no, decks use colour and typography only | Phase 2 |
| 6 | Lesson slice rule: 2010-12-01 to 2011-02-28 from the 2010-2011 sheet, 105,335 rows, 9.28 MB. Alternative: 2011-02-01 to 2011-04-30, 94,371 rows | Take the December to February window: it contains the first rows of the sheet, the December peak, and 22,523 rows of sheet overlap are avoided. The alternative has no cancelled large order but loses the story continuity and the seasonal chart | Phase 2 |
| 7 | The cancelled giant order (invoice 541431, 77,183.60, cancelled 16 minutes later). Remove it in S4 or keep it? | Remove it in S4 as part of the "look at the biggest rows" investigation. It teaches that cleaning needs judgment, and it stops a cancelled order from becoming the number one product. All numbers in this plan assume it is removed | Phase 2, S4 |
| 8 | S6 seaborn chart: top 5 countries including the UK (one huge bar, 84.8% of revenue) or top 5 countries outside the UK? | Exclude the UK from the chart and say "outside the UK" on the slide and in the title | Phase 3, S6 |
| 9 | Should learner-facing files use her first name or stay neutral ("you")? The brief does not name her | Neutral "you" in files, and her name only on the GitHub template if she wants it. Confirm | Phase 2 |
| 10 | Colab's AI settings screen changes over time. Can you send or confirm the exact menu path to turn off Colab AI features, so the S1 notebook matches the real screen? | Send a screenshot or the current path. If not, the notebook says "Tools, Settings, AI features" and you correct it live | Phase 2 |
| 11 | S4 non-product cleaning: keep stock codes whose first character is a digit, instead of a hard-coded list of charge codes | Use the one-character rule: it removes all 588 non-product rows in the slice and cannot miss a new fee code. The hard-coded list would leave 19 rows and 11 non-product codes in the clean table | Phase 2, S4 |

The theme choice is a Phase 2 question, asked after the preview (5 variants, 3 slides each), not now.

Which answers block which Phase 2 output:

| Answer | Blocks |
|---|---|
| Q1 video topic and length | The 3 discussion questions and the video timing strip in the S1 deck |
| Q2 and Q3 dates and time | The final schedule in the course outline and the course home; the recall dates |
| Q4 email | The course outline header |
| Q5 photo permission | The S1 deck cover and any photo in later decks; without it the decks use colour and typography only |
| Q6 slice rule | `data/online_retail_ii_lesson.csv`, `data/ANSWER_KEY.md`, and every session anchor |
| Q7 giant order | The S4 cleaning steps, the S5 ABC numbers and the S6 product chart |
| Q8 seaborn country chart | The S6 notebook and deck |
| Q9 learner name | The course home, the GitHub README template and every learner-facing file header |
| Q10 Colab AI menu | The Colab tour section in the S1 notebook |
| Q11 non-product rule | The S4 cleaning steps and all downstream numbers |

If an answer is still missing when Phase 2 starts, build the part that does not depend on it and leave a visible placeholder, for example `[BRYAN: email]` in the outline. Do not guess.

## 10. Risks and how we handle them

| Risk | Handling |
|---|---|
| The opening video content is unknown, so the S1 discussion questions cannot be written | Open question 1. The rest of S1 does not depend on it |
| The cancelled giant order distorts the product finding | Open question 7, and the answer key records both numbers |
| The UK dominates the country charts | Open question 8, and teacher notes explain the choice |
| Colab's pandas version differs from our test environment (pandas 2.3.3) | Notebooks use only stable pandas 2.x calls; the verifier runs them on 2.3.3, and S4 is checked live |
| Proxima Nova is not installed on the learner's Windows laptop | Decks are shown as PDF in the screen share; the PPTX gets the standard note to embed fonts for Windows |
| S4 is the heaviest session | It plans 80 minutes inside the 90-minute slot and hard-stops at 90; the giant order investigation has a fallback in S5; the cleaning log is the core habit; the brief's cut order is in the teacher guide |
| The learner falls behind after S4 | Cut order from the brief section 6: S7 intros become 1-page self-study guides, seaborn becomes homework, project shrinks to 2 sessions |
| Photos cannot be downloaded (no permission) | Decks designed to work with colour and typography; photos only as an optional extra |
| A teammate edits a file another needs | Write scopes on the task board, and the Lead owns the final diff and runs the quality gate |
| Numbers drift between notebook, deck, handout and answer key | One source: `data/ANSWER_KEY.md`, computed from the slice. Deck and handout writers copy from it, and the verifier checks it |
| She misses a session (S4 or S6 is the dangerous one) | Send the notebook plus the one-page solution walkthrough the same day. The next session's recall and warm-up (10 minutes) become the catch-up. If S4 is missed, the project drops to the 2-session minimum and the teacher builds the clean table on the share screen with her |
| Colab disconnects or restarts in the middle | Every notebook after S4 starts with the load and shape check, so a restart costs one cell. S4's teacher card says run all from the top. The CSV is on Drive, so nothing is lost |
| Two different buffer stories confuse the teacher on the day | One policy only: the 90-minute slot, 75 planned minutes for nine sessions, 80 for S4, hard stop at 90 |

Next action: STOP for Bryan's answers to section 9. On his reply, start Phase 2 with the data slice and the S1 pilot.
