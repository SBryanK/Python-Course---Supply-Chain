# PySC-101 build plan

Phase 1 plan for the 10-session course. Written 2 Nov 2026. Source of truth is the master build brief, version 1.0, 2 Nov 2026. This plan adjusts the brief where the real data or the real environment requires it, and lists the questions Bryan must answer before Phase 2 starts.

Status: Phase 1 deliverables are `data/EXPLORATION.md`, this file, and the untouched raw data in `data/raw/`. An independent verifier recomputed every number from the raw xlsx: it found four small defects in the first draft of the exploration report (non-product table totals, slice non-product rows, one description count, one alternative-window row count). All four are fixed here and in `data/EXPLORATION.md`. The deck toolchain was also tested end to end (build, PDF, page images, audit, five-variant preview). STOP here until Bryan answers section 9.

## 1. What changed from the brief's assumptions

Everything marked [VERIFY] in the brief is now checked against the real file. Five things need a decision or an adjustment:

1. The column names are exactly as the brief guessed: `Invoice`, `StockCode`, `Description`, `Quantity`, `InvoiceDate`, `Price`, `Customer ID`, `Country`. The price column is `Price`, not `UnitPrice`. The brief's code samples work as written.
2. The lesson slice needs a rule that avoids counting the 9-day overlap between the two yearly sheets twice. Proposal: all rows of the `Year 2010-2011` sheet from 2010-12-01 to 2011-02-28. See section 2 and open question 6.
3. The slice contains one huge cancelled order (invoice 541431, 74,215 units of stock code 23166, worth 77,183.60). The simple S4 cleaning keeps the positive line and drops the cancellation, which would make this cancelled order the number one product. Proposal: the learner finds it in the "biggest revenue rows" step and removes that one invoice with a commented line. See open question 7.
4. The brief's non-product list for S4 is too short. The slice has 588 non-product rows: postage, fees, samples, discounts, manual lines, gift vouchers and old DCGS catalogue codes. Proposal: keep the rows whose stock code starts with a digit. Every real product code starts with a digit, every charge or voucher code starts with a letter, so one line removes all 588 and cannot miss a new fee code. A hard-coded 8-code list would leave 19 of those rows in the clean table.
5. The S6 seaborn chart, done exactly as the brief drafts it, would show one huge UK bar and five tiny bars, because the UK is 84.8% of slice revenue. Proposal: show the top 5 countries outside the UK and say so on the slide. See open question 8.

Two smaller adjustments:

6. The S5 cold test "revenue by month for the top country" works but has only three months. Keep it: December 2010, January 2011, February 2011. Expected answers are in section 4, S5.
7. The brief says "ask the open items in Section 14"; the open items are in Section 15 of the brief. They are all in section 9 below, with recommendations.

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

- It starts at the first row of the 2010-2011 sheet, so the S1 to S3 hand-typed examples are the first rows the learner meets again in S4. The story stays one story.
- It contains the December peak, so the S6 "revenue per day" chart has a real finding instead of a flat line.
- It is one sheet, so the 9-day overlap between the two yearly sheets does not duplicate rows.
- It loads in Colab in about one second.
- 105,335 rows is enough to make cleaning and grouping feel real, and small enough that a beginner can re-run cells without waiting.

The slice is not cleaned. Cleaning is the learner's work in S4.

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
| Product table rows before and after the S6 merge | 3,066 and 3,066 |

## 4. Session plans

Times: 15:00 SGT, 14:00 WIB. Block 1 35 minutes, break 5, Block 2 35 minutes. Content planned for 75 minutes. Slides take at most 10 minutes of any session.

Every session pack contains: `student.ipynb`, `solution.ipynb`, `deck.pptx`, `deck.pdf`, `handout.pdf`, `teacher_card.md`, `exit_ticket.md`, `recall.md`. Notebook cap is 30 cells. Handout cap is 2 pages. Teacher card cap is 1 page. Deck is 6 to 10 slides.

Deck rules for all 10 decks, from the skill overrides: format `live`, no logo, English slide text, speaker notes in Bahasa Indonesia with English technical terms, code at most 6 lines in Consolas or DejaVu Sans Mono, theme chosen once in Phase 2 and reused. Every session pack has all eight files including an exit ticket; S10 has an exit ticket too, scored by Bryan in the last 10 minutes.

### S1, Mon 16 Nov: Your first lines of Python

Business question: What is the sales value of one order line?

Shape: opening video 0 to 10, why Python 10 to 15, Colab tour 15 to 20, micro-cycles 20 to 35. Break. Block 2 as normal.

Concepts and order: `print`, variable, int and float and str, arithmetic, round, f-string, first errors. Teaching order in Block 1: print and variable together (5 min), three data types (5 min), f-string (5 min). Arithmetic, `round` and the error zoo happen in Block 2 while the worksheet is running.

| Concept | Daily life | Excel bridge | Limit to say out loud |
|---|---|---|---|
| print() | reading a label out loud | typing in a cell to see it | Python shows nothing unless you ask |
| variable | a label on a storage bin | a named cell | changing the label does not update other cells, run again |
| int / float / str | counting boxes / weighing goods / writing a product name | number vs text format | "5" is text, Python will not add text to a number |
| f-string | a fill-in-the-blank label | ="Sold "&A2&" units" | the f before the quote is easy to forget |

Real data anchors (first rows of the sheet, verified): invoice 536365, WHITE HANGING HEART T-LIGHT HOLDER, quantity 6, price 2.55, value 15.299999999999999, rounded 15.3. WHITE METAL LANTERN 6 at 3.39 gives 20.34. CREAM CUPID HEARTS COAT HANGER 8 at 2.75 gives 22.0.

Notebook plan (about 24 cells):
1. Text: what this notebook is, how to run a cell with Shift+Enter, how to read the page.
2. Code: `print("Hello, supply chain")` and a second print.
3. Text: what print does, the limit.
4. Code: `product_name = "WHITE HANGING HEART T-LIGHT HOLDER"`, then print.
5. Text: the storage bin analogy and the limit; variable names.
6. Code: `quantity = 6`, `unit_price = 2.55`, print both.
7. Code: `sales_value = quantity * unit_price`, print it. This is where 15.299999999999999 shows up.
8. Text: why the long decimal, when to round.
9. Code: `print(round(sales_value, 2))`.
10. Code: three `type()` calls with prints.
11. Text: three data types, text vs number warning.
12. Code: f-string sentence with the real values.
13. Text: f-string analogy and the forgotten f trap.
14. Text + code exercise 1 (TODO): value of WHITE METAL LANTERN (expected 20.34).
15. Text + code exercise 2 (TODO): value of CREAM CUPID HEARTS COAT HANGER (expected 22.0).
16. Text + code exercise 3 (TODO): f-string sentence about the first line (expected text shown in the answer key).
17. Text + code: error zoo, make a NameError on purpose and read the last line.
18. Text + code: SyntaxError (missing bracket).
19. Text + code: TypeError ("5" + 5).
20. Text: rule to read the last line of an error first.
21. Text + code exercise 4 (TODO): fix three broken cells.
22. Text: recap, homework, recall plan.

Deck (10 slides, special S1 order): cover; course map with 10 sessions on one timeline; how a session works (35/5/35); why Python for supply chain, three reasons; Colab tour; print and variables; types and f-strings; errors and how to read them; Now in Colab (notebook name); homework and recall. The 3 discussion questions for the opening video wait for Bryan's answer (open question 1).

Handout (2 pages, black and white): the five concepts with daily life, Excel bridge and limit; the code patterns; three common errors and their fixes; the exercise list with expected outputs.

Teacher card (Bahasa Indonesia, 1 page): the question; the order of ideas; analogies and their limits; the two likely mistakes (forgetting the f, using matching quotes); hint ladder for exercise 4; timing with the video slot marked.

Exit ticket: (1) predict the output of a 3-line cell that prints a value and a rounded value. (2) name the error type in one broken cell and fix it. Answers in `exit_ticket.md` under a section Bryan keeps.

Recall: 1 day (Tue 17 Nov), 3 questions mixing print, variables and types.

Homework: finish the three worksheet lines, make the three errors deliberately at home, write one f-string sentence about any order in the data.

### S2, Wed 18 Nov: Lists, product cards and decisions

Business question: Which orders are big orders?

Concepts: list, index from 0, `len`/`sum`/`min`/`max`, dict, comparison, if/elif/else.

| Concept | Daily life | Excel bridge | Limit |
|---|---|---|---|
| list | a row of bins on one shelf | one column of values | the first bin is number 0 |
| len, sum, min, max | count, total, smallest, largest | COUNT, SUM, MIN, MAX | same idea, different spelling |
| dict | a product card: field name to value | one row with headers | look up by field name, not position |
| comparison | is this more than that | =A2>10 gives TRUE or FALSE | = stores a value, == compares |
| if/elif/else | a packing rule | =IF(...) | indentation is part of the rule |

Real data anchors: the first 7 quantities [6, 6, 8, 6, 6, 2, 6]; `len` 7, `sum` 40, `min` 2, `max` 8; index 0 is 6, index 2 is 8, index -1 is 6. The product card for the first row: stock_code 85123A, description WHITE HANGING HEART T-LIGHT HOLDER, quantity 6, price 2.55, country United Kingdom. Thresholds 100 and 12 are teaching thresholds, not business rules, and the notebook says so.

Notebook plan (about 21 cells): recall prompt in a text cell; list and print; indexes; len/sum/min/max; list analogy and limit; dict and lookup; dict analogy; comparison examples (6 > 10 is False, "United Kingdom" == "United Kingdom" is True); if/elif/else with quantity 6 (small), then quantity 12 and 100 to show the branches; indentation text; exercises (predict quantities[2], count big orders, UK or outside UK); recap and homework.

Deck (9 slides, standard order): cover; today's question; list and indexes; len/sum/min/max; dict product card; comparison; if/elif/else; Now in Colab; recap and homework.

Handout: concept table; code patterns; three errors (index out of range, key error, forgetting the colon or indentation); exercises.

Teacher card: the order; two likely mistakes (counting from 1, forgetting the colon); hint ladder for the if/else exercise; timing.

Exit ticket: (1) predict `quantities[2]` (answer 8). (2) write an if/else that prints "UK" or "Outside UK" from `order_line["country"]` (first row is United Kingdom, so it prints "UK").

Recall: 4 days (Thu 19 to Sun 22 Nov), 12 questions: one old topic (print, variables or types) and two new (list, dict, if) each day.

Homework: add 3 more real quantities to the list and compute len, sum, min, max; write one if/elif/else about prices.

### S3, Mon 23 Nov: Do it for every row

Business question: Label every order line with one function.

Concepts: for loop, function (`def`, `return`), the difference between print and return, reading a traceback.

| Concept | Daily life | Excel bridge | Limit |
|---|---|---|---|
| for loop | walking down the shelf, checking each bin | dragging a formula down a column | the body must be indented |
| function | your own reusable rule | your own named formula | nothing happens until you call it |
| return | the answer the rule gives back | the value the formula shows | print shows, return hands back |
| traceback | a delivery note listing every stop | no Excel version | read from the bottom up |

Real data anchors: the same 7 quantities; the first two order lines for the dict list; invoice 540815 as a real big order with three large lines (1930 at 2.55, 2000 at 1.85, 3114 at 2.10). `order_size(6)` is small, `order_size(250)` is big (a teaching call, not a data claim). The traceback exercise uses a real three-level error: a loop calls a function, the function compares a text quantity with a number, and Python raises a TypeError.

Notebook plan (about 21 cells): recall; for loop over quantities; loop printing values; loop with f-string labels; function definition; two calls; print vs return comparison; loop with the function; list of two real order dicts; loop over dicts; exercises: write `line_value(quantity, price)`, loop over 5 real lines and print each value, count big lines with a counter; traceback cell (run on purpose) and reading it; recap and homework.

Deck: cover; today's question; for loop; function and return; print vs return; traceback, read from the bottom; Now in Colab; recap and homework.

Handout: concept table; code patterns; three errors (forgetting indentation, forgetting return, calling before defining); exercises.

Exit ticket: (1) find the bug in a function that prints instead of returning. (2) read a 3-level traceback and say which line broke.

Recall: 2 days (Tue 24, Wed 25 Nov), 6 questions mixing S1 to S3.

Homework: write `line_value` and use it on 5 real lines; one function of her own with a return.

### S4, Thu 26 Nov: From one row to the whole file (heaviest session)

Business question: Clean the data and compute revenue.

Block 1: load and look. Block 2: clean and compute.

Concepts: pandas and DataFrame, `read_csv`, `head`/`shape`/`info`/`describe`, rename with a dict, boolean filter, new column, `sort_values`.

| Concept | Daily life | Excel bridge | Limit |
|---|---|---|---|
| pandas, DataFrame | the whole warehouse list | a sheet | columns have one data type each |
| read_csv | opening the file | File, Open | the path must be exact |
| head, shape, info, describe | first page, page count, cover | scrolling, COUNTA, status bar | looking first is part of the job |
| rename with a dict | relabelling bins | editing headers | uses the dict idea from S2 |
| boolean filter | keeping only the good boxes | helper column, then Filter | the original table does not change unless you save the result |
| new column | writing the value on each box | a formula column | no auto-update, run the cell again |
| sort_values | biggest boxes in front | Sort Z to A | same as Excel |

Real data anchors:

- Load path in Colab: `/content/drive/MyDrive/PySC-101/data/online_retail_ii_lesson.csv`.
- `sales.shape` is (105335, 8).
- Missing values: Description 304, Customer ID 36,210, all other columns 0.
- Column names after rename: invoice, stock_code, description, quantity, invoice_date, price, customer_id, country.
- Cleaning steps and row counts: 105,335 start; 104,360 after `drop_duplicates`; 102,471 after removing C invoices; 102,257 after `quantity > 0`; 101,933 after `price > 0`; 101,459 after keeping only product codes; 101,458 after removing invoice 541431. The learner writes each number in the cleaning log text cell.
- Non-product rule in code: `first_character = sales_clean["stock_code"].str[0]`, then `is_product_code = first_character.str.isdigit()`, then keep the true rows with the boolean filter she already knows. Three short lines, no list to mistype.
- Cleaning log habit: one row count per step, checked against `sales_clean.shape` at the end.
- Decision to discuss: do we drop rows with a missing customer_id? For product analysis no (we keep 101,458 rows and lose 34.9% of rows if we drop). For customer analysis yes.
- The cancelled giant order investigation: `sales_clean.sort_values("revenue", ascending=False).head(10)` shows invoice 541431 at 77,183.60. She checks the raw rows, finds C541433 cancelling the same 74,215 units 16 minutes later, and removes invoice 541431 with one commented line. If Bryan chooses to keep it, the numbers are in `data/EXPLORATION.md` section 12.
- New columns: `revenue = quantity * price`, `invoice_date = pd.to_datetime(invoice_date)`.
- Exit ticket Germany filter on the clean table gives 1,514 rows.

Notebook plan (about 27 cells): import pandas and mount Drive; read the CSV; head; shape; info; describe; missing values; rename with the dict; check columns; text cell with the cleaning log table; drop duplicates and log; remove C invoices and log; quantity > 0 and log; price > 0 and log; keep only product codes and log; `.copy()` with one line of explanation; revenue column; date conversion; sort top 10; the giant order investigation (2 cells and 1 text cell); final shape and log; exercises (filter Germany, filter big revenue lines); recap and homework.

Deck (10 slides): cover; today's question; the whole sheet in Python (pandas and DataFrame); open and look; rename with a dict; keep only the good rows (boolean filter); write a new column; sort; Now in Colab (notebook name); recap and homework. The cancelled order investigation is teacher-led in the notebook and goes in the speaker notes, not on a slide.

Handout: concept table; code patterns; three errors (file not found, KeyError after rename, truth value of a Series); cleaning step checklist; exercise list.

Teacher card: the Block 1 and Block 2 split; the two likely mistakes (wrong Drive path, forgetting to reassign after filtering); hint ladder for the Germany filter; the giant order investigation script in Bahasa Indonesia; timing with a 3-minute buffer.

Exit ticket: (1) what `sales.shape` tells you (rows and columns, expected (105335, 8) at load and the clean shape after cleaning). (2) write a filter that keeps only rows from Germany (answer 1,514 rows on the clean table).

Recall: 3 days (Fri 27 to Sun 29 Nov), 9 questions mixing S2 to S4, with at least one pandas question each day.

Homework: re-run the notebook; write the cleaning log in her own words; bring one question about the cancelled order.

### S5, Mon 30 Nov: Which products matter, plus cold test 1

Business question: Which products drive most of the value?

Concepts: `groupby` with `sum`, `cumsum`, ABC analysis with a function, `.apply` with a named function.

| Concept | Daily life | Excel bridge | Limit |
|---|---|---|---|
| groupby + sum | sorting receipts into piles then adding each pile | PivotTable | the result has a new index, use reset_index() |
| cumsum | a running total on a receipt roll | =SUM($B$2:B2) dragged down | sort first or the running total is meaningless |
| ABC analysis | few items take most of the space and money | sort, running % column, IF | 80/95 is a rule of thumb, not a law |
| .apply(function) | using the S3 rule on every row | dragging your formula down | use a named function, not a lambda |

Real data anchors: 3,066 products; class A 671 products (21.9%) with 79.98% of revenue; class B 794 (25.9%) with 15.02%; class C 1,601 (52.2%) with 5.00%. Top product REGENCY CAKESTAND 3 TIER 51,504.85. Key finding for the deck: "22% of the products bring 80% of the revenue."

Block 2 is the cold test: 20 minutes, notes allowed, Bryan silent. Question: revenue by month for the top country. Expected answers: United Kingdom; December 2010 705,166.72; January 2011 468,651.61; February 2011 417,876.17. Rubric: runs (1), correct numbers (1), clear names (1), one sentence of meaning (1). After the test, 5 minutes to look at one solution together, then the exit ticket and close.

Notebook plan (about 21 cells): recall; revenue by product; sort; reset_index; total revenue; cumsum; cumulative share; abc_class function; apply; value_counts; revenue by country; exercises (find a B product, count A products); cold test section with the question and a blank cell; recap and homework.

Deck (9 slides): cover; today's question; groupby is a PivotTable; running total with cumsum; ABC with a function; the finding slide with the real number and one chart (22% of products, 80% of revenue); Now in Colab and cold test; recap; homework and recall.

Handout: groupby and cumsum patterns; the ABC function; the cold test rubric; three errors (forgetting reset_index, sorting after cumsum, apply with a lambda).

Teacher card: how to run the cold test (silent, notes allowed, grade after); the two likely mistakes; hint ladder; timing.

Exit ticket: (1) what class would a product with cumulative share 0.90 be (B). (2) write one sentence that explains the 80/20 finding in plain words.

Recall: 2 days (Tue 1, Wed 2 Dec), 6 questions mixing S3 to S5.

Homework: finish the country analysis; write her own abc_class sentence; prepare for the cold test discussion.

### S6, Thu 3 Dec: Show it clearly

Business question: How do we show it clearly?

Concepts: merge (VLOOKUP), matplotlib, seaborn (bonus), chart titles that state the finding.

| Concept | Daily life | Excel bridge | Limit |
|---|---|---|---|
| merge | matching a packing list to a product catalogue | VLOOKUP or XLOOKUP | check row counts before and after, a bad key adds rows |
| matplotlib | drawing a chart by hand, step by step | Insert Chart, then edit each part | every chart needs a title and axis labels |
| seaborn | a chart template on top of matplotlib | chart styles | built on matplotlib, labels and titles still work |

Real data anchors: product table rows before and after the merge are both 3,066. Top 10 products cumulative share is 9.62%. Daily revenue peaks on 2010-12-07 at 81,454.99. The top 5 countries outside the UK are Netherlands 58,182.55, EIRE 43,426.19, Germany 37,365.63, France 32,392.39, Australia 24,678.48. Chart titles should state the finding: "The biggest 10 products are still only 9.6% of revenue", "Revenue peaked in the first week of December", "22% of products bring 80% of revenue", "Outside the UK, the Netherlands and Ireland lead".

Case hunt is handed out at the end of Block 2. It is homework due in S8, one page, 5 points, and Bryan does not find cases for her.

Notebook plan (about 21 cells): recall; product names table; merge with row count check; top 10 table; horizontal bar chart; daily revenue table; line chart; product rank column; cumulative share curve with the 80% line; seaborn bar chart for non-UK countries; chart title rule; exercises (fix a chart with no title, add axis labels); recap and case hunt.

Deck (9 slides): cover; today's question; merge is VLOOKUP; matplotlib, one chart step by step; the title says the finding; seaborn template; Now in Colab; the case hunt; recap and homework.

Handout: merge check pattern; matplotlib pattern; three chart mistakes; the case hunt template on page 2.

Teacher card: the row-count check habit; two likely mistakes (forgetting the key, calling show twice); hint ladder for the horizontal bar chart; case hunt explanation.

Exit ticket: (1) what does it mean if the row count changes after a merge (a key is not unique or a many-to-many match). (2) write a title for the daily revenue chart that states the finding.

Recall: 3 days (Fri 4 to Sun 6 Dec), 9 questions mixing S4 to S6.

Homework: finish the top 10 chart; start the case hunt (due S8).

### S7, Mon 7 Dec: Other tools, then your own question

Block 1: SQL intro 20 minutes, Power BI intro 15 minutes (bonus content). Block 2: project kickoff 35 minutes.

SQL anchors from the slice: the pandas table is `sales_clean[["invoice", "stock_code", "description", "quantity", "price", "country", "revenue"]]`; the top 5 countries query returns United Kingdom 1,591,694.50, Netherlands 58,182.55, EIRE 43,426.19, Germany 37,365.63, France 32,392.39; the Germany query returns 37,365.63; the top 10 revenue rows query shows the same top rows as the pandas answer.

Power BI: homework before S7 is to install Power BI Desktop. In the session she exports `product_value` (or a small country table) to CSV, imports it, builds one bar chart and one card, and saves the file. Bryan guides, she clicks.

Block 2: what makes a good analyst question (specific, answerable with this data, useful to a manager); she picks a question and fills `project_plan.md` (question, columns needed, steps, expected chart, what decision it helps); 10 minutes for the presentation guide walk-through (3 slides, answer first, scoring sheet).

Project menu, all feasible on the slice:
1. Which products are class A, and how stable are they month to month? The slice has three months, enough to compare December, January and February.
2. Which countries buy most outside the UK, and which products do they buy? 30 non-UK countries are present.
3. How big are cancellations, and which products get cancelled most? 1,904 cancellation rows are in the slice and removed in S4.
4. Reorder point for the top 5 products, with assumptions she chooses (lead time in days, safety stock percentage). The numbers are labelled as assumptions, not data.

An Olist note goes in `project_plan.md` as an optional idea only, with a licence check reminder.

Notebook plan (about 20 cells): SQL setup with sqlite3; the same table; three queries, each next to its pandas version; reading the result; Power BI steps as text plus a small export cell; the project question template; a checklist cell.

Deck (9 slides): cover; today's question (what question will I answer); SQL and pandas side by side; SQL query patterns; Power BI in three clicks; what makes a good question; project plan template; Now in Colab and project kickoff; homework.

Handout: SQL query sheet and pandas equivalents; Power BI steps; project plan template. `intro_sql.md`, `sql_playground.md`, `intro_powerbi.md` cover the self-study path if the bonus is cut.

Teacher card: 20/15/35 split with a hard stop; two likely mistakes (forgetting the connection, exporting the wrong table); how to steer a vague project question.

Exit ticket: (1) read a short SQL query and say what it returns. (2) write your project question in one sentence and one column it needs. Answers in `exit_ticket.md`.

Recall: 2 days (Tue 8, Wed 9 Dec), 6 questions mixing S5 to S7 plus one SQL reading question.

Homework: install Power BI Desktop before S7 (brief), finish the project plan, start the first analysis.

### S8, Thu 10 Dec: Project work 1

0 to 10: case hunt discussion, she presents her case in 2 minutes and finds one link to our data. 10 to 35: project work, Bryan uses the hint ladder only. Break. Block 2: project work, last 5 minutes "what I found so far" in 3 sentences.

AI rule from here: AI may help, but she explains and tests every line, and records the tool and the prompt in `project_plan.md` or a small AI log.

Notebook plan (about 16 cells): project checklist; her question restated in her own words; the columns she needs; the first analysis cell; chart draft; the 3-sentence status; the AI log table.

Deck (7 slides): cover; today's question (her question); case hunt discussion; project checklist; AI rules; Now in Colab; what I found so far.

Handout: project checklist and the 3-sentence template; AI log table.

Teacher card: how to use the hint ladder without taking the keyboard; two likely mistakes (scope too big, jumping to a chart before checking the numbers); how to keep the session silent.

Exit ticket: (1) your question in one sentence. (2) one number you have checked by hand and how you checked it. The 3-sentence status is the closing.

Recall: 3 days (Fri 11 to Sun 13 Dec), 9 questions mixing S6 to S8 and her project.

Homework: continue the project analysis; finish the case hunt if not done.

### S9, Mon 14 Dec: Project work 2 and sharing

Block 1: final charts and the 3-sentence conclusion (answer, evidence, recommendation). Block 2 first 15 minutes: GitHub in the browser, she creates the account herself, a new repository, uploads the notebook, writes a short README (question, data source with credit, finding, how to run). Block 2 last 20 minutes: start her 3 slides from `presentation_template.pptx`.

Self-reflection is handed out at the end, due before S10.

Notebook plan (about 14 cells): final chart checklist; the 3-sentence conclusion template; the GitHub steps as text; README template; the slide template walkthrough; reflection questions.

Deck (7 slides): cover; today's question (can I explain the finding in three sentences); final chart checklist; GitHub in the browser; README template; the 3 slides; reflection.

Handout: 3-sentence template, GitHub steps, README template, reflection questions.

Teacher card: GitHub without an account, she does every click; two likely mistakes (wrong repo visibility, README without the data credit); how to keep the conclusion to 3 sentences.

Exit ticket: (1) write your finding in one sentence (answer first). (2) write your recommendation in one sentence. The reflection handout is the closing.

Recall: 2 days (Tue 15, Wed 16 Dec), 6 questions mixing S7 to S9 and her presentation content.

Homework: finish slides, rehearse the 5-minute presentation once, complete the reflection.

### S10, Thu 17 Dec: Show what you can do

0 to 5 setup and nerves check. 5 to 10 her presentation (5 minutes). 10 to 25 interview-style Q&A. 25 to 35 feedback with the scoring sheet (2 strengths, 1 thing to improve). Break. Block 2: review the reflection together, course retro (keep, stop, start), next steps for January (optional module outline only).

Q&A questions: walk me through your project in 2 minutes; why did you remove those rows; what would you do with more time; how did you check the AI's code.

Scoring sheet: clarity, evidence, recommendation, delivery, each 1 to 4.

Notebook plan (about 10 cells): presentation checklist; Q&A notes; feedback notes; retro keep/stop/start; reflection review; next steps.

Deck (6 slides): cover; agenda; Q&A rules; retro keep, stop, start; what next; thank you.

Handout: presentation scoring sheet and the Q&A question list.

Teacher card: timing with a visible clock; two likely nerves mistakes (reading slides, apologising); feedback sentence starters.

Exit ticket: (1) what can you do now that you could not do in November. (2) one thing you would do differently in the project. Bryan reads both in the feedback slot.

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
| `course_home/project_plan.md` | question, columns, steps, chart, decision; project menu; Olist note | 4 |
| `course_home/presentation_guide.md` | answer first, 3 slides, numbers simply, 2-minute script | 4 |
| `course_home/presentation_scoring.md` | clarity, evidence, recommendation, delivery, 1 to 4 | 4 |
| `course_home/intro_sql.md`, `sql_playground.md`, `intro_powerbi.md` | 1 page each, the self-study versions of the S7 bonus | 4 |
| `course_home/presentation_template.pptx` | cover, question, finding, recommendation, thank you, same theme | 2 with the theme, filled in 4 |
| `course_home/optional_jan_module.md` | outline only: deeper Power BI, SQL lessons, VS Code, git command line | 4 |
| `data/online_retail_ii_lesson.csv` | the slice | 2 |
| `data/EXPLORATION.md` | this phase's report | 1 |
| `data/ANSWER_KEY.md` | every expected number for every exercise, computed from the slice | 2 (S1 to S3), extended per phase |
| `data/README.md` | source, licence, citation, columns, slice rule | 2 |
| `PUSH_LIST.md` | per session, which files to upload and by when (the day before) | 4 |

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
1. Lead builds `data/online_retail_ii_lesson.csv` from the raw sheet and writes `data/README.md`.
2. Lead writes `data/ANSWER_KEY.md` for S1 to S3 with every expected value, computed from the slice.
3. Lead builds S1 `student.ipynb` and `solution.ipynb` and runs both top to bottom in a fresh kernel.
4. Deck builder runs the ppt-maker theme preview with 3 real S1 slides in 5 variants: L, L:soft, D, M:center, E:hard. Bryan picks theme, tone and alignment once.
5. Lead builds the S1 deck with the chosen variant, renders and audits it, and looks at every page image.
6. Lead builds S1 handout, teacher card, exit ticket, recall.
7. Lead builds `course_outline.docx` and `.pdf` with the placeholder email until Bryan answers.
8. STOP. Bryan reviews S1 as the style sample. His feedback applies to every later session.

Phase 3, S2 to S10, one session at a time, each with the section 13 checks. After S4, show S2 to S4 together and STOP for a quick check.

Phase 4, course-wide files, then Phase 5, final check and summary.

Environment notes for every deck session (verified on 2 Nov 2026 by the deck toolchain check):
- PATH must include /opt/homebrew/bin so `soffice`, `pdftoppm` and `pdffonts` are found.
- Our copy of `_tools/ppt_maker/ppt-maker/scripts/render.py` is patched in two places: the LibreOffice profile comes from `PPT_MAKER_PROFILE` and defaults inside the repo, and the profile URL uses `as_uri()` because the repo path contains spaces. Do not revert these.
- Always make the PDF with the patched `render.py`, not with the `--pdf` option inside a build script. `render.py` also embeds Proxima Nova and prints the font check.
- Set `MPLCONFIGDIR` to a repo folder only when a build draws a matplotlib figure.
- The exact commands and outputs are in `_tools/deck_check/RUNBOOK.txt`.
- The theme preview test built 15 pages in 5 variants (L, L:soft, D, M, E:hard) and rendered them with Proxima Nova embedded. Use those five variants for the real S1 preview in Phase 2.

Quality gate per session, from the brief section 13:
1. Run `student.ipynb` and `solution.ipynb` top to bottom in a fresh kernel; no errors.
2. Every expected output matches `ANSWER_KEY.md`.
3. Every exercise uses only concepts taught so far; exceptions listed.
4. Caps: notebook cells (30), handout pages (2), teacher card (1 page), deck (6 to 10 slides, at most 10 minutes of class).
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
| Verifier | independent run of every notebook, cap check, number check against the answer key, deck render check | read only, reports to Lead |

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

## 10. Risks and how we handle them

| Risk | Handling |
|---|---|
| The opening video content is unknown, so the S1 discussion questions cannot be written | Open question 1. The rest of S1 does not depend on it |
| The cancelled giant order distorts the product finding | Open question 7, and the answer key records both numbers |
| The UK dominates the country charts | Open question 8, and teacher notes explain the choice |
| Colab's pandas version differs from our test environment (pandas 2.3.3) | Notebooks use only stable pandas 2.x calls; the verifier runs them on 2.3.3, and S4 is checked live |
| Proxima Nova is not installed on the learner's Windows laptop | Decks are shown as PDF in the screen share; the PPTX gets the standard note to embed fonts for Windows |
| S4 is the heaviest session | Taught in two blocks, cleaning log habit, and the brief's cut order is in the teacher guide |
| The learner falls behind after S4 | Cut order from the brief section 6: S7 intros become 1-page self-study guides, seaborn becomes homework, project shrinks to 2 sessions |
| Photos cannot be downloaded (no permission) | Decks designed to work with colour and typography; photos only as an optional extra |
| A teammate edits a file another needs | Write scopes on the task board, and the Lead owns the final diff and runs the quality gate |
| Numbers drift between notebook, deck, handout and answer key | One source: `data/ANSWER_KEY.md`, computed from the slice. Deck and handout writers copy from it, and the verifier checks it |

Next action: STOP for Bryan's answers to section 9. On his reply, start Phase 2 with the data slice and the S1 pilot.
