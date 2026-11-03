# Python for Supply Chain: build plan

This is the working plan for a 10-session beginner course, built from Bryan's master brief (v1.0, 2 Nov 2026). It turns the brief into real lessons on real data, and lists the questions Bryan still needs to answer.

**Where we are:** Phase 1 is done. The data is explored, every number here was computed from the real file, and `_tools/fact_check.py` re-checks them (155/155 pass). The independent pedagogy review (`_review/pedagogy-review.md`) is applied. **Next step: Bryan answers section 10, then we build the Session 1 pilot.**

## 1. What we changed from the brief, and why

1. **Same column names as the brief guessed.** `Invoice`, `StockCode`, `Description`, `Quantity`, `InvoiceDate`, `Price`, `Customer ID`, `Country`. The brief's code works.
2. **One three-month slice, from one sheet.** The raw file has two yearly sheets that overlap for 9 days. Taking Dec 2010 to Feb 2011 from the second sheet avoids double counting.
3. **One giant cancelled order.** Invoice 541431 sold 74,215 jars (£77,183.60) and was cancelled 16 minutes later. Simple cleaning would make it the number one product. She finds it in S4 and removes it, which teaches that cleaning needs judgment.
4. **A better rule for non-products.** The brief lists 4 fee codes, but the slice has many more (postage, samples, vouchers, old catalogue codes). Rule: keep codes that start with a digit. One line, catches all 588 rows.
5. **The country chart leaves out the UK.** The UK is 84.8% of revenue, so with it the chart is one huge bar and five tiny ones.
6. **A month column in S4.** The S5 cold test asks for revenue by month, so S4 adds one line to make a month from the date.
7. **Dates come back as text.** After saving and reloading `sales_clean.csv`, `invoice_date` is text again, so every load cell from S5 runs `pd.to_datetime` once more.

What stays fixed: 10 sessions on the fixed dates, real data only, no machine learning or forecasting, short SQL and Power BI intros only, a 3-session project, learner files in English, teacher cards and speaker notes in Bahasa Indonesia, no NUS name or logo, no emojis.

## 2. The data

UCI Online Retail II, a UK online gift shop. Chen, D. (2012). Online Retail II [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5CG6D. Licence CC BY 4.0. The citation goes in the data README, the S4 notebook, the course outline, the course home and her GitHub README.

**Lesson file:** `online_retail_ii_lesson.csv`. Every row of the `Year 2010-2011` sheet from 2010-12-01 up to (not including) 2011-03-01. Not cleaned: cleaning is her job in S4.

| Property | Value |
|---|---|
| Rows / columns | 105,335 / 8 |
| Dates | 2010-12-01 08:26 to 2011-02-28 17:04 |
| File size | 9.28 MB, loads in about 1 second |
| Invoices / products / countries | 4,894 / 3,159 / 31 |
| Missing Customer ID / Description | 36,210 (34.4%) / 304 |
| Cancellation rows / duplicates | 1,904 / 975 |
| Negative quantity / zero price rows | 2,118 / 540 |
| Non-product code rows | 588 |
| Clean rows / clean revenue | 101,458 / £1,876,534.04 |

**Why this window:** S1 to S3 use the very first rows by hand, and she meets them again in the full file in S4, so it is one story. It has the December peak, so the daily chart has something to say. It is small enough to re-run without waiting.

**Keep these true in every file:**
- Money is GBP (pounds). Never dollars or rupiah.
- The data covers three months, not a year.
- A few cancelled sales stay in the clean table (about 1% of revenue). Mention it in teacher notes only.
- 35,364 clean rows (34.9%) have no customer ID. Fine for product questions, not for customer questions.
- Some codes appear in two spellings (`85123A` and `85123a`). We do not fix this; the teacher card mentions it.
- 40 codes have more than one description. S6 uses this for the merge lesson.
- The UK is 84.82% of revenue. Country charts must not look global.

## 3. Numbers we may use

All from the slice, all GBP. Copy from here or from `data/ANSWER_KEY.md`, never from memory.

| What | Value |
|---|---|
| Raw rows / clean rows | 105,335 / 101,458 |
| Clean revenue | 1,876,534.04 |
| Class A / B / C products | 671 (21.9%) / 794 (25.9%) / 1,601 (52.2%) of 3,066 |
| Class A share of revenue | 79.98% |
| Top product | REGENCY CAKESTAND 3 TIER, 51,504.85 |
| Top 10 products, share of revenue | 9.62% |
| Revenue Dec 2010 / Jan 2011 / Feb 2011 | 775,572.23 / 593,178.39 / 507,783.42 |
| UK share / UK revenue | 84.82% / 1,591,694.50 |
| Top 5 outside the UK | Netherlands 58,182.55, EIRE 43,426.19, Germany 37,365.63, France 32,392.39, Australia 24,678.48 |
| Best day | 2010-12-07, 81,454.99 |
| Germany rows raw / clean | 1,741 / 1,514 |
| First 7 quantities | 6, 6, 8, 6, 6, 2, 6 |
| First line value | 6 * 2.55 = 15.299999999999999, rounded 15.3 |
| Second and third line values | 6 * 3.39 = 20.34, 8 * 2.75 = 22.0 |
| Products with more than one description | 40 |
| Rows with a lower-case stock code (raw slice) | 541 |
| S6 merge check | 3,066 product rows, 3,107 code-name pairs: 3,066 -> 3,107 -> 3,066 after fixing |

## 4. How we write everything

### Tone

- **Friendly and a little playful.** Write like a kind senior colleague, not a textbook. Session titles can be fun ("Cleaning day", "Showtime"). Small jokes are welcome when they help memory. No emojis, no hype, no exclamation marks.
- **Short.** Bryan explains live, so the notebook does not lecture. A text cell is one or two short sentences: what to do and what to look for. The longer "why" lives in Bryan's voice and, if needed, in one optional cell.
- **Still self-explanatory.** If she opens the notebook at home, she can follow it: every new word gets a one-line meaning the first time, and `glossary.md` has them all.
- **Plain English for a non-native reader.** Common words, short sentences, one idea per sentence. Say "pounds", not "GBP", in learner text.

### Teaching moves

- Daily life first, then Excel, then 3 to 6 lines of code she types herself.
- Every concept ends with something she does (predict, change one value, write one line) before the next concept. Never all theory first.
- PRIMM for exercises: Predict, Run, Investigate, Modify, Make.
- She always types. Bryan never types for her. Slides take at most 10 minutes.
- Say the limit of every analogy, for example "Excel recalculates by itself. A notebook does not. Run the cell again."
- One story per session. S7 is the only exception (SQL, Power BI, then her question).
- Errors: read the last line first.
- Hint ladder, with 10 seconds of quiet before each step: 1) "What do you expect this line to do?" 2) point at the line 3) a concept hint 4) the pattern, not the answer 5) do it together, then she does a similar one alone.

### Code rules

- One step per line, saved in a name that says what it holds: `sales_clean`, `revenue_by_country`, `is_cancelled`.
- Short lowercase column names from S4 on.
- Show the result after each important step (`head()`, `shape`, `print`).
- `.copy()` once after filtering, explained as "Save As with a new name".
- Named functions with `.apply()`, linking back to S3. `print(f"...")` for messages. Comments say why, not what.
- Not allowed: lambdas, list comprehensions, classes, decorators, try/except, `*args`, chains longer than 2 calls, `inplace=True`, chained assignment, `.loc` tricks, `np.where`, regex, anything not taught yet, hidden helper functions, cells that only work out of order.

### Notebook format

- Max 30 cells. A short text cell before each code cell. One idea per cell.
- Something for her to do after at most two concept cells. S1 shows this, because it is the style sample.
- Exercise cells start with `# TODO`, say the task in one comment line, and the text cell above shows the expected result.
- One optional cell per notebook, "Why does this happen?", in plain words, ending with what it means for an analyst. Examples: why `6 * 2.55` is not exactly 15.3 (round money at the end), why counting starts at 0 (steps from the start), why a filter does not change the original, why ABC uses 80 and 95 (a habit, not a law). No exercise depends on it.
- Every notebook runs top to bottom on its own. In S4 she saves `sales_clean.csv` to her `work/` folder. From S5 on, the first cells load it, run `pd.to_datetime` on `invoice_date`, and check `sales_clean.shape` is (101458, 10). Wrong shape means stop and fix first.

### Files per session

`student.ipynb`, `solution.ipynb`, `deck.pptx` + `deck.pdf`, `handout.pdf` (max 2 pages, aim for 1, black and white), `teacher_card.md` (1 page, Bahasa Indonesia), `exit_ticket.md` (2 questions, answers kept by Bryan), `recall.md` (3 questions a day until the next session, answers at the end).

Decks: 6 to 10 slides, theme chosen once in Phase 2, no logo, English slides, Bahasa Indonesia speaker notes, code at most 6 lines in Consolas or DejaVu Sans Mono.

Daily recall: 3 short questions a day between sessions (one old topic, two new), 66 questions in 9 files. In class she answers them in 2 minutes and explains the one she missed.

### Time

The slot is 90 minutes. Nine sessions plan 75 minutes (35, break 5, 35) and keep 15 minutes for setup, connection trouble and overrun. S4 plans 80 minutes. Every session stops at 90.

Normal shape (S2 to S6): recall 5, paper warm-up 5, micro-cycles 25, break, worksheet 22 (she drives), exit ticket 8, close 5.

### AI rules for her

- S1 to S5: no AI. S1 shows how to turn Colab's AI off.
- S6 and S7: AI may explain an error or idea, but not write the answer. Prompt: "Explain this error in simple words. Do not give me the fixed code."
- S8 to S10: AI may help write code. She must explain every line, test it (row counts, one value by hand) and write down the tool and prompt.

## 5. The sessions

### S1, Mon 16 Nov: Hello, Python

**Question:** What is one order line worth?

**New words:** order line (one product on one receipt), variable, data type, f-string, error message.

**Timing.** Block 1: 0-8 opening video (stop at 8 minutes, rest is homework), 8-11 why Python, 11-15 Colab tour (open the Drive folder and peek at the CSV, so "the data" is real), 15-35 three micro-cycles: print and variable (6), data types (6), arithmetic, round and f-string (8). Block 2: 0-10 exercises 1 and 2, 10-16 the error zoo (predict, run, investigate), 16-22 exercise 3 and fix three broken cells, 22-30 exit ticket, 30-35 close.

| Concept | Daily life | Excel | Say the limit |
|---|---|---|---|
| `print()` | reading a label out loud | typing in a cell to see it | Python shows nothing unless you ask |
| variable | a label on a storage bin | a named cell | change it and other cells do not update; run again |
| int / float / str | counting boxes / weighing goods / a product name | number vs text format | `"5"` is text; Python will not add text to a number |
| arithmetic, `round` | adding up a receipt | `=B2*C2`, `ROUND` | `6 * 2.55` gives 15.299999999999999; round money when you show it |
| f-string | a fill-in-the-blank label | `="Sold "&A2&" units"` | easy to forget the `f`; braces mark where the value goes |

**Code she types:**

```python
product_name = "WHITE HANGING HEART T-LIGHT HOLDER"
quantity = 6
unit_price = 2.55

sales_value = quantity * unit_price
print(sales_value)
print(round(sales_value, 2))
print(f"We sold {quantity} units of {product_name} for {round(sales_value, 2)} pounds.")
```

**Notebook (about 25 cells).** How to run a cell, and two rules: cells run in the order you click, so a NameError usually means "run the cells above"; NaN means empty. Then: print -> variables -> *predict what changes if quantity is 7* -> multiply (the 15.299999999999999 moment) -> round -> *change the price to 3.39, predict, check 20.34* -> `type()` -> *predict `"5" + 5`* -> f-string -> *change it to print units* -> exercises 1 to 3 (WHITE METAL LANTERN 20.34, CREAM CUPID HEARTS COAT HANGER 22.0, one f-string sentence) -> error zoo (NameError, SyntaxError, TypeError, read the last line) -> exercise 4, fix three broken cells -> recap, homework, and a checklist (Google account, Chrome or Edge, charger, Drive folder, headset).

**Deck (9 slides, 10 minutes):** cover; course map and session shape; why Python (Excel struggles when the file is huge, the steps repeat every week, or you must show exactly what you did); Colab tour; print and variable; data types; arithmetic, round, f-string; reading errors; Now in Colab and homework. Video discussion questions wait for Bryan.

**Handout:** the concepts table, code patterns, three errors and fixes, exercises with answers, and the first 12 real order lines (invoice 536365 plus 540815) for homework.

**Teacher card:** likely mistakes: forgetting the `f`, mismatched quotes, NameError from skipped cells. Hint ladder for exercise 4.

**Exit ticket:** (1) predict a 3-line cell that prints a value and its rounded value. (2) name the error in one broken cell and fix it.

**Recall:** Tue 17 Nov. **Homework:** finish the worksheet, make the three errors on purpose, write one f-string about rows 8 to 10 on the handout.

### S2, Wed 18 Nov: Shelves, cards and choices

**Question:** Which order lines are big?

**Recall:** three S1 questions. **Warm-up:** write the Excel formula that multiplies and rounds; predict `print(quantity)` after `quantity = 12`.

| Concept | Daily life | Excel | Say the limit |
|---|---|---|---|
| list | a row of bins on one shelf | one column | the first bin is number 0 |
| `len`, `sum`, `min`, `max` | count, total, smallest, largest | COUNT, SUM, MIN, MAX | same idea, new spelling |
| dict | a product card: field name -> value | one row with headers | look up by name, not position |
| comparison | "is this more than that?" | `=A2>10` | `=` stores, `==` asks |
| if / elif / else | a packing rule | `=IF(...)` | the indent is part of the rule |

**Code she types:**

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

Answers: len 7, sum 40, min 2, max 8; `[0]` 6, `[2]` 8, `[-1]` 6. The 100 and 12 are teaching numbers, not business rules; the notebook says so. "Big" means one big line, because the data records lines, not whole invoices.

**Exercises:** predict `quantities[2]` and `quantities[-1]`; label 6 and then 12 with the if rule; print "UK" or "Outside UK" from the card.

**Deck (9):** cover, question, list, len/sum/min/max, dict, comparison, if, Now in Colab, recap. **Handout errors:** index out of range, KeyError, missing colon or indent.

**Exit ticket:** (1) predict `quantities[2]` (8). (2) write the UK / Outside UK rule (prints "UK").

**Recall:** Thu 19 to Sun 22 Nov. **Homework:** add rows 8 to 10 from the handout to the list and redo len, sum, min, max; one if rule about prices.

### S3, Mon 23 Nov: Let the loop do the walking

**Question:** Can one rule label every order line?

**Recall:** three S2 questions. **Warm-up:** predict a list index and an if cell.

| Concept | Daily life | Excel | Say the limit |
|---|---|---|---|
| for loop | walking down the shelf, checking each bin | dragging a formula down | the body must be indented |
| function | your own reusable rule | your own named formula | does nothing until you call it |
| `return` | the answer the rule hands back | the value the formula shows | `print` only shows; `return` hands it back |
| traceback | a stack of plates, newest on top | none | read the bottom line first, then go up |

**Code she types:**

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

Real big order for practice: invoice 540815 (1,930 at 2.55, 2,000 at 1.85, 3,114 at 2.10). The traceback cell is a real three-level error: a loop calls a function that compares text with a number.

**Exercises:** write `line_value(quantity, price)` with `return`; loop over 5 real lines and print each value; label each line; change the threshold from 12 to 50 and predict. No counting here (S5 counts with `.sum()`).

**Deck (8):** cover, question, loop, function and return, print vs return, traceback, Now in Colab, recap. **Handout errors:** missing indent, missing return (`None`), calling before defining.

**Exit ticket:** (1) fix a function that prints instead of returning. (2) read a 3-level traceback and say which line broke.

**Recall:** Tue 24 and Wed 25 Nov. **Homework:** `line_value` on the 5 handout lines; one function of her own; **mount Google Drive once** in a blank notebook and accept the permission screen, so it does not surprise her in S4.

### S4, Thu 26 Nov: Cleaning day

**Question:** What does the data look like once it is clean, and how much did we sell?

The heaviest session. It plans 80 minutes and stops at 90.

**Recall:** three S3 questions. **Warm-up:** predict what `sales.shape` prints; write the Excel filter for Germany.

**Timing.** Block 1 (35): recall 5, warm-up 5, load and look 10 (`read_csv`, `head`, `shape`), missing values and rename 7, `info` and new words 5 (NaN, filter, `&` not `and`), cleaning log setup 3. Block 2 (40): filter and new column 8, she drives the cleaning 9, revenue, date, month and sort 8, giant order 6, exit ticket 6, log review and close 3. If late, the giant order moves to the start of S5. `describe` is homework.

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

**Code she types (core):**

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
cancellations = sales[is_cancelled]          # keep these for the project

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

**Cleaning log (she writes each number):** start 105,335 -> drop duplicates 104,360 -> remove C invoices 102,471 -> quantity above 0 102,257 -> price above 0 101,933 -> product codes only 101,459 -> remove invoice 541431 101,458. Final shape (101458, 10).

**The giant order (detective moment):** the top row is invoice 541431, £77,183.60. She looks at the raw rows, finds C541433 cancelling the same 74,215 jars 16 minutes later, and removes 541431 with one commented line.

**Small notes for the notebook:** missing values are Description 304 and Customer ID 36,210. Customer IDs print as `17850.0` because a number column with empty cells is stored as decimals. Talk: do we drop rows with no customer ID? For products no, for customers yes.

**Save at the end:** `sales_clean.csv` and `cancellations.csv` to `work/`.

**Exercises:** keep only Germany (1,514 rows); keep only lines with revenue above a value she picks.

**Deck (10):** cover, question, pandas, open and look, rename, filter, new column, sort, Now in Colab, recap. The giant order lives in the notebook and speaker notes. **Handout:** the `&` filter pattern, cleaning checklist, `describe`, errors (file not found, KeyError after rename, `and` vs `&`).

**Teacher card:** likely mistakes: wrong Drive path, forgetting to save the filter result (`sales_clean = ...`). Hint ladder for the Germany filter.

**Exit ticket:** (1) what `shape` tells you ((105335, 8) at load, (101458, 10) at the end). (2) the Germany filter (1,514 rows).

**Recall:** Fri 27 to Sun 29 Nov, one pandas question a day and one month question. **Homework:** re-run the notebook, write the cleaning log in her own words, try `describe`, bring one question about the giant order.

### S5, Mon 30 Nov: Who are the star products?

**Question:** Which products bring most of the money?

**Recall:** three S4 questions (one about months). **Warm-up:** the PivotTable steps for revenue by product.

**Timing.** Block 1: recall 5, warm-up 5, groupby and sort 10, running total and share 7, ABC function 6, counting and country copy-alongs 2. Block 2 is the cold test and is never cut: test 20 (notes allowed, Bryan silent), look at one solution 5, exit ticket 7, close 3.

| Concept | Daily life | Excel | Say the limit |
|---|---|---|---|
| `groupby` + `sum` | sorting receipts into piles, then adding each pile | PivotTable | the result has a row label column; `reset_index()` makes it a normal table again |
| `cumsum` | a running total on a receipt roll | `=SUM($B$2:B2)` dragged down | sort first, or the total means nothing |
| ABC analysis | a few items take most of the space and money | sort, running %, IF | 80/95 is a habit, not a law |
| `.apply(function)` | using your S3 rule on every row | dragging your formula down | use a named function |

**Code she types:**

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

**Finding:** 671 of 3,066 products (21.9%) bring 79.98% of revenue. On the slide: "About 1 in 5 products bring 80% of the money." B 794, C 1,601. Top product REGENCY CAKESTAND 3 TIER, 51,504.85.

**Cold test:** revenue by month for the top country, using her month column. Answers: United Kingdom; Dec 2010 705,166.72; Jan 2011 468,651.61; Feb 2011 417,876.17. Score out of 4: it runs, the numbers are right (within 0.01), names are clear, one sentence says what it means.

**Save:** `product_value.csv` to `work/` for Power BI in S7.

**Deck (9):** cover, question, groupby = PivotTable, running total, ABC, the finding (one big number and one chart), Now in Colab and cold test, recap, homework. **Handout errors:** forgetting `reset_index`, cumsum before sorting, using a lambda.

**Exit ticket:** (1) which class is a product at 0.90? (B). (2) the 80/20 finding in one plain sentence.

**Recall:** Tue 1 and Wed 2 Dec. **Homework:** finish any copy-alongs, write her own ABC sentence.

### S6, Thu 3 Dec: Make the numbers talk

**Question:** How do we show the finding so a manager gets it in five seconds?

**Recall:** three S5 questions. **Warm-up:** sketch on paper the chart you would show a manager, with labelled axes.

**Timing.** Block 1: recall 5, warm-up 5, merge and the row-count lesson 12, top 10 bar chart 10, the title rule 3. Block 2: daily line chart 10, cumulative curve as copy-along 8 (homework if late), fix-a-chart exercise 4, exit ticket 8, close and case hunt 5. Seaborn is homework.

| Concept | Daily life | Excel | Say the limit |
|---|---|---|---|
| `merge` | matching a packing list to the catalogue | VLOOKUP / XLOOKUP | count rows before and after; a repeated key makes the table grow |
| matplotlib | drawing a chart step by step | Insert Chart, then edit | every chart needs a title and axis labels |
| seaborn | a chart template on top of matplotlib | chart styles | the same titles and labels still work |

**The merge lesson:** names built with `drop_duplicates()` on both columns give 3,107 rows, so the merge grows 3,066 -> 3,107. She finds the 41 extra rows (40 codes with two names), dedupes on `stock_code`, merges again: 3,066.

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

**Chart rule:** the title says the finding, not the chart type. Examples: "Revenue peaked in the first week of December" (best day 2010-12-07, 81,454.99), "About 1 in 5 products bring 80% of revenue", "Outside the UK, the Netherlands and Ireland lead". Daily revenue uses `.dt.date` as a 3-minute copy-along.

**Case hunt:** explained in the last 5 minutes, due S8. She finds the case herself; the teacher card has two backup cases.

**Deck (9):** cover, question, merge, one chart step by step, the title rule, seaborn, Now in Colab, case hunt, recap. **Handout:** the chart recipe (`figure`, `barh`/`plot`, `title`, `xlabel`, `ylabel`, `tight_layout`, `xticks(rotation=45)` for long labels, `show`), three chart mistakes, the seaborn pattern with its expected picture, and the case hunt template.

**Exit ticket:** (1) your merge went from 3,066 to 3,107 rows. What happened and how do you fix it? (2) a finding-title for the daily chart.

**Recall:** Fri 4 to Sun 6 Dec. **Homework:** finish the top 10 chart, seaborn pattern, start the case hunt, **install Power BI Desktop**.

### S7, Mon 7 Dec: New tools, your own question

**Question:** What question will you answer in your project?

**Timing.** Block 1: recall 5, warm-up 5 (one question a manager might ask), SQL taste 15, Power BI demo 7 (she watches, builds it at home), exit ticket 3. Block 2: what makes a good question 6, pick from the menu 6, fill `project_plan.md` 12, presentation guide 8, close 3. If the cut order is on, SQL and Power BI become self-study and all 70 minutes go to the project.

**SQL, next to the pandas she knows:**

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

Answers: UK 1,591,694.50, Netherlands 58,182.55, EIRE 43,426.19, Germany 37,365.63, France 32,392.39. Second query: Germany only (37,365.63). Third query (top 10 rows) is homework in `sql_playground.md`. MySQL is another SQL database that runs on a server; we do not install it. Practice: sql-practice.com.

**Power BI:** Bryan shows it on screen: open, load `product_value.csv`, one bar chart, one card, save. She repeats it at home and sends a screenshot.

**A good question is** specific, answerable with this data, and useful to a manager. If a question needs a skill we did not teach, change the question, not the skill.

**Project menu:**
1. Is class A revenue steady month to month? (filter A, group by month, one line chart)
2. Which country outside the UK buys most, and what are its top 5 products? (one filter, one groupby, one bar chart)
3. How big are cancellations, and which products get cancelled most? (`cancellations.csv`, 1,904 rows)
4. A reorder point for the top 5 products, using lead time and safety stock she chooses. The slice has 68 trading days. Label every assumption as an assumption.

Olist (Kaggle) appears in `project_plan.md` as a January idea only, with a reminder to check its licence.

**Exit ticket:** (1) read a short SQL query and say what it returns. (2) your project question in one sentence, plus one column it needs.

**Recall:** Tue 8 and Wed 9 Dec, with one SQL reading question. **Homework:** Power BI at home, finish the project plan, start the analysis.

### S8, Thu 10 Dec: Detective work

**Question:** Her own.

**Timing.** Block 1: case hunt talk 10 (she presents for 2 minutes and links it to our data), project work 25. Block 2: project work 22, exit ticket 8, "what I found so far" in 3 sentences 5. Bryan uses the hint ladder only.

**AI from today:** allowed, but she explains and tests every line and logs the tool and prompt.

**Exit ticket:** (1) your question in one sentence. (2) one number you checked by hand, and how.

**Recall:** Fri 11 to Sun 13 Dec (can drop to 2 a day if the project is behind). **Homework:** keep going; **create a GitHub account and an empty public repository** with `github_guide.md`; finish the case hunt.

### S9, Mon 14 Dec: Polish and publish

**Question:** Can you say your finding in three sentences?

**Timing.** Block 1: final charts and the 3-sentence conclusion (answer, evidence, recommendation) 25, write the finding and recommendation (this is the exit ticket) 8, hand out the reflection 2. Block 2: GitHub 12 (Colab File > Save a copy in GitHub, then the README in the browser), start the 3 slides from `presentation_template.pptx` 21, close 2.

The README has her question, the data credit, her finding, and how to run it. Minimum if behind: the upload, one chart and one finding sentence.

**Recall:** Tue 15 and Wed 16 Dec. **Homework:** finish slides, rehearse once out loud, write the reflection.

### S10, Thu 17 Dec: Showtime

**Question:** Can she explain it like an analyst?

**Timing.** Block 1: settle in 5, her presentation 5, interview-style Q&A 15, feedback 10 (two strengths, one thing to improve). Block 2: reflection review 15, retro (keep, stop, start) 10, January ideas 3, exit ticket 7.

**Presentation:** cover, question, finding, recommendation, thank-you. In 5 minutes: 1 question and context, 2 finding and evidence, 1 recommendation, 1 spare. Slides in English. She presents in English; she may answer questions in Bahasa Indonesia if nervous. Delivery is scored on structure and pace, not accent.

**Q&A:** "Walk me through your project in 2 minutes." "Why did you remove those rows?" "What would you do with more time?" "How did you check your numbers?" "If you used AI, how did you check it?"

**Exit ticket:** (1) what can you do now that you could not do in November? (2) one thing you would do differently.

**Recall:** none after S10; an optional January practice sheet with 3 questions.

## 6. Course-wide files

| File | What it holds |
|---|---|
| `course_outline.docx` + `.pdf` | max 4 pages, black and white, the 7 sections of brief section 11 |
| `course_home.docx` | the one page she opens: schedule, links, recall, case hunt, AI rules |
| `teacher_guide.md` | Bahasa Indonesia: hint ladder, feedback rules, the 10-second wait, overload signal, cut order, cold test |
| `ai_rules.md` | the three AI phases and the prompt template |
| `case_hunt_template.md` | 5 points, one page |
| `reflection_template.md` | 6 questions, one page |
| `project_plan.md` | question, columns, steps, chart, decision; the menu; 68 trading days, clean revenue, reorder formula as assumptions; Olist note |
| `presentation_guide.md` | answer first, the 5-minute shape, numbers in plain words, the 2-minute Q&A version |
| `presentation_scoring.md` | clarity, evidence, recommendation, delivery, 1 to 4 with one-line anchors; project 10/10/10; cold test out of 4; reflection complete, partial or missing |
| `intro_sql.md`, `sql_playground.md`, `intro_powerbi.md` | one page each, the self-study versions |
| `presentation_template.pptx` | cover, question, finding, recommendation, thank-you, same theme |
| `glossary.md` | about 25 English words with a one-line Bahasa Indonesia meaning |
| `github_guide.md` | one page: account, empty public repo, save from Colab, README |
| `optional_jan_module.md` | outline only: Power BI, SQL, VS Code, git |
| `data/online_retail_ii_lesson.csv`, `data/README.md`, `data/ANSWER_KEY.md` | the slice, its source and rule, every expected answer |
| `PUSH_LIST.md` | what to upload, and by when |

**Course outline header:** Course: Python for Supply Chain. Dates 16/11/2026 to 17/12/2026. Online, 10 sessions, 15:00 SGT (14:00 WIB), 90-minute slot (S4 may use 5 minutes of the buffer). Instructor: Bryan Kusno. Email: `[BRYAN: email]`.

**Objectives:** 1) read and fix common Python errors (S1, S3, every session); 2) load, check and clean a real CSV with pandas (S4); 3) summarise with groupby and sort products with ABC (S5); 4) make clear charts with matplotlib and seaborn (S6); 5) present a finding in 5 minutes, answer first (S7 to S10).

**Assessment:** participation and daily recall 20%, cold test 15%, project 30%, presentation 20%, reflection 15%. One line: "This course is not graded. The weights show what matters most."

**Schedule table:** one row per session with date, summary, resources (only what we really give: notebook, handout, deck, the S1 video, the dataset credit, sql-practice.com, templates) and deadlines (cold test S5; case hunt S6 to S8; project plan S7; project and GitHub S9; reflection before S10; presentation S10).

## 7. Google Drive

```
Python for Supply Chain/
  00_course_home/   course home, outline, guides, templates
  data/             the lesson CSV only
  work/             her own files from S4: sales_clean.csv, cancellations.csv, product_value.csv
  week_1/           S1, S2
  week_2/           S3, S4
  week_3/           S5, S6
  week_4/           S7 to S10
teacher_only/       solutions, teacher cards, answer keys, deck PPTX, exit ticket answers
```

Upload the day before each session: S1 by 15 Nov, S2 by 17 Nov, S3 by 22 Nov, S4 by 25 Nov, S5 by 29 Nov, S6 by 2 Dec, S7 by 6 Dec, S8 by 9 Dec, S9 by 13 Dec, S10 by 16 Dec. Course home, outline and the data by 14 Nov. Never upload the raw xlsx, `_tools/`, `_verify/` or `data/work/`.

## 8. Build order and checks

**Phase 2, the S1 pilot:** build the slice with `_tools/build_slice.py` and check it; write `data/README.md`; write `ANSWER_KEY.md` for S1 to S3; build and run both S1 notebooks; theme preview with 3 S1 slides in 5 variants (L, L:soft, D, M:center, E:hard) so Bryan picks once; build the S1 deck, handout, teacher card, exit ticket, recall; build the course outline. **STOP:** Bryan reviews S1. His answers to these become the style for every later session: Is the pace right? Is the code style right? Are the analogies right? Is the teacher card tone right? Anything to change?

**Phase 3:** S2 to S10 one at a time. STOP after S4 to review S2 to S4 together. **Phase 4:** course-wide files. **Phase 5:** final check and a short summary for Bryan.

**Check every session before calling it done:**
1. Both notebooks run top to bottom in a fresh runtime.
2. Every expected answer matches `ANSWER_KEY.md`.
3. Exercises use only what was taught, and she has something to do after every two concept cells.
4. Caps: 30 cells, 2-page handout, 1-page teacher card, 6 to 10 slides (one idea each, 10 minutes max).
5. Run ppt-maker's `render.py` and `audit.py`, and look at every slide.
6. Read the learner files as a non-programmer with English as a second language. Rewrite anything that needs a second read.
7. No em-dashes, emojis, exclamation marks, or the words "delve", "leverage", "seamless", "journey".
8. No NUS branding.

**Deck environment (tested 2 Nov 2026):** PATH must include `/opt/homebrew/bin`. Our `render.py` copy has two patches (profile path from `PPT_MAKER_PROFILE`, and `as_uri()` because the repo path has spaces); keep them. Make PDFs with `render.py`, not the build script. Set `MPLCONFIGDIR` only when a deck draws a chart. Full commands: `_tools/deck_check/RUNBOOK.txt`.

## 9. Who builds what

| Role | Owns |
|---|---|
| Lead | the slice, answer key, S1 style sample, course outline, final check, `PLAN.md`, `PUSH_LIST.md` |
| Notebook builder | S2 to S10 notebooks, after S1 is approved |
| Deck builder | theme preview, all decks, `presentation_template.pptx` |
| Materials writer | handouts, teacher cards, exit tickets, recall, guides and templates |
| Verifier | read only: runs every notebook, checks caps and numbers, runs `fact_check.py` |

Numbers and code come from the Lead. Style comes from the approved S1. No images are downloaded without Bryan's yes.

## 10. Questions for Bryan

| # | Question | Our suggestion |
|---|---|---|
| 1 | The opening video is "I Wish Someone Explained Programming to Me Like This" (Cloud X Berry). How long is it, and where do we stop? | Show up to 8 minutes; the rest is homework. We write 3 discussion questions once you confirm |
| 2 | S2 on Wed 18 Nov instead of Thu 19 Nov? | Confirm. All weekdays are checked |
| 3 | Is 14:00 WIB fine for her? | Ask her |
| 4 | Email for the course outline? | Your choice |
| 5 | May we download openly licensed photos for the decks? | Yes, with credit, only where a photo helps (warehouse, shelves, receipts) |
| 6 | Use the Dec 2010 to Feb 2011 slice? | Yes. It keeps the S1 rows and the December peak. (Alternative Feb to Apr 2011: 94,371 rows, no giant order, but no peak and new example rows) |
| 7 | Remove the giant cancelled order 541431 in S4? | Yes, as a detective moment. All numbers here assume it is removed |
| 8 | Country chart without the UK? | Yes, and the title says "outside the UK" |
| 9 | Her name in the files, or "you"? | "You" in files; her name only on GitHub if she wants |
| 10 | The exact menu path to turn off Colab AI? | Send a screenshot from your Colab |
| 11 | Product rule: keep codes that start with a digit? | Yes. A fixed list would leave 19 non-product rows |
| 12 | S4 takes 80 minutes instead of 75? | Yes for S4 only. For a strict 75, the giant order moves to S5 |

If an answer is missing when we build, we leave a visible placeholder like `[BRYAN: email]`. We never guess.

## 11. Risks

| Risk | What we do |
|---|---|
| The giant order distorts the ranking | Question 7; the answer key keeps both versions |
| The UK swamps country charts | Question 8 |
| Colab's pandas differs from ours (2.3.3) | Only stable pandas 2.x calls; S4 checked live |
| No Proxima Nova on her Windows laptop | Show decks as PDF |
| S4 is too heavy | 80 minutes, hard stop at 90, giant order can move to S5 |
| She falls behind after S4 | Cut in this order: S7 intros become self-study, seaborn becomes homework, the project drops to 2 sessions |
| She misses a session | Send the notebook and solution walkthrough the same day; the next recall and warm-up become catch-up. If S4 is missed, build the clean table with her on screen |
| Colab restarts mid-session | Every notebook from S5 starts with load and shape check; nothing is lost |
| Login or screen share fails in S1 | Tech check by 13 Nov: she runs `print("hello")` in a shared Colab link, sends a screenshot, opens the Drive folder, tests screen share |
| Drive's permission pop-up in S4 | Mount once as S3 homework. Fallback: upload through the Files pane |
| The repo is public | `teacher_only/` is gitignored; solutions, answer keys and her scores are never committed |
| Numbers drift between files | One source: `ANSWER_KEY.md`, checked by the verifier |
| No photo permission | Decks work with colour and type alone |
