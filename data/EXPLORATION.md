# Online Retail II: data exploration

Phase 1 report for Python for Supply Chain. Written 2 Nov 2026 from the real UCI file. Every number below was computed by running pandas on the raw file, not typed from memory. STOP: Bryan must review this file before Phase 2 starts.

Verification: an independent audit recomputed the whole-file and slice numbers from the raw xlsx, and `_tools/fact_check.py` checks 155 values against the data as a regression test. It does not read this prose; a typo in a sentence still needs a human read. Two review rounds found and fixed five stale figures (non-product row totals, slice non-product rows, missing descriptions count, a clean-table customer count and one alternative-window row count). The numbers in this file are the corrected ones.

## 1. Source and files

| Item | Value |
|---|---|
| Dataset | Online Retail II |
| Creator | Daqing Chen |
| Citation | Chen, D. (2012). Online Retail II [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5CG6D |
| Licence | CC BY 4.0 |
| Downloaded from | https://archive.ics.uci.edu/static/public/502/online+retail+ii.zip on 2 Nov 2026 |
| Raw file kept | `data/raw/online_retail_II.xlsx` (untouched, 45,622,278 bytes = 43.5 MiB) |
| Raw checksum | sha256 `bcbe73b35f5b7babf197fb0cb983a11f5d9ff929078d4aa53d171b1f2df2e980` |
| Derived slice licence | CC BY 4.0, same as the source, with the citation above wherever it is used (data README, S4 notebook, course outline, course home, GitHub README template) |
| Zip checksum | sha256 `572e36277c2390fbfde10664750731e0a86f55e33470d91919085f0408e67bfb` |

Working copies for our own analysis live in `data/work/` and are never delivered: `sheet_2009_2010.csv`, `sheet_2010_2011.csv`, `online_retail_ii_with_sheet.csv`, plus the proposed lesson slice `slice_dec2010_feb2011_raw.csv`. They are a direct conversion of the two sheets, no cleaning.

What the company is: a UK-based, registered, non-store online retailer that mainly sells unique all-occasion giftware. Many customers are wholesalers. Transactions run from 1 Dec 2009 to 9 Dec 2011.

## 2. Shape of the file

| Check | Result |
|---|---|
| Sheets | 2: `Year 2009-2010` and `Year 2010-2011` |
| Rows, sheet 2009-2010 | 525,461 |
| Rows, sheet 2010-2011 | 541,910 |
| Rows, combined | 1,067,371 (matches the UCI page) |
| Columns | 8 |
| Date range, sheet 2009-2010 | 2009-12-01 07:45 to 2010-12-09 20:01 |
| Date range, sheet 2010-2011 | 2010-12-01 08:26 to 2011-12-09 12:50 |
| Date range, combined | 2009-12-01 07:45 to 2011-12-09 12:50 |
| Memory, combined, with Customer ID read as text | 313.2 MB |
| Distinct invoices | 53,628 |
| Distinct customers | 5,942 |
| Distinct countries | 43 |
| Distinct stock codes | 5,305 |
| Distinct descriptions | 5,698 |

### Columns (exact names in the xlsx)

| Column | Meaning | Type after pandas read | Course name from S4 |
|---|---|---|---|
| `Invoice` | Invoice number. Starts with C for a cancellation | object (text) | `invoice` |
| `StockCode` | Product code | object (text) | `stock_code` |
| `Description` | Product name | object (text) | `description` |
| `Quantity` | Units on the line. Negative on cancellations and adjustments | int64 | `quantity` |
| `InvoiceDate` | Date and time of the transaction | datetime64[ns] | `invoice_date` |
| `Price` | Unit price in pounds sterling (GBP) | float64 | `price` |
| `Customer ID` | Customer number. Missing for many rows | float64 (because of NaN) | `customer_id` |
| `Country` | Country of the customer | object (text) | `country` |

The [VERIFY] items in the brief are confirmed: the real column names are `Invoice`, `StockCode`, `Description`, `Quantity`, `InvoiceDate`, `Price`, `Customer ID`, `Country`, with a space in `Customer ID`. The price column really is called `Price`, not `UnitPrice`. All prices are in GBP.

## 3. Missing values

| Column | Missing rows | Share |
|---|---|---|
| Description | 4,382 | 0.41% |
| Customer ID | 243,007 | 22.77% |
| All other columns | 0 | 0% |

By sheet: Description is missing 2,928 times in 2009-2010 and 1,454 times in 2010-2011. Customer ID is missing 107,927 times in 2009-2010 and 135,080 times in 2010-2011.

Every row with a missing Description also has `Price = 0` (the count is the same, 4,382, and a check of the rows confirms it). These are stock adjustments, damages and manual entries, not product sales.

## 4. Cancellations and returns

| Check | Result |
|---|---|
| Rows whose Invoice starts with C | 19,494 (1.83% of rows) |
| Distinct C invoices | 8,292 |
| C rows with Quantity at or above 0 | 1 |
| C rows with negative Quantity | 19,493 |
| Rows with negative Quantity but no C invoice | 3,457 |
| Invoice first character | 5: 939,382 rows, 4: 108,489 rows, C: 19,494 rows, A: 6 rows |

The single C row with a positive quantity is invoice `C496350`, stock code `M` (Manual), quantity 1, price 373.57, 1 Feb 2010. It is an odd row, not a normal sale.

The 3,457 negative quantity rows without a C invoice are stock adjustments. Their descriptions are mostly missing (2,689 rows), or words such as `check` (123), `damages` (84), `?` (83), `damaged` (78), `missing` (27), `sold as set on dotcom` (20), `Unsaleable, destroyed.` (9), `smashed` (9), `thrown away` (9).

The 6 `A` invoices are bad debt adjustments, all with stock code `B`, description `Adjust bad debt`, customer missing, and quantity 1. Details:

| Invoice | Date | Quantity | Price | Country |
|---|---|---|---|---|
| A506401 | 2010-04-29 13:36 | 1 | -53,594.36 | United Kingdom |
| A516228 | 2010-07-19 11:24 | 1 | -44,031.79 | United Kingdom |
| A528059 | 2010-10-20 12:04 | 1 | -38,925.87 | United Kingdom |
| A563185 | 2011-08-12 14:50 | 1 | 11,062.06 | United Kingdom |
| A563186 | 2011-08-12 14:51 | 1 | -11,062.06 | United Kingdom |
| A563187 | 2011-08-12 14:52 | 1 | -11,062.06 | United Kingdom |

Rule for the course: a cancellation is a negative line with an invoice number that starts with C. The A invoices are not in the lesson slice.

## 5. Prices

| Check | Result |
|---|---|
| Minimum price | -53,594.36 |
| Maximum price | 38,970.00 |
| Mean price | 4.6494 |
| Median price | 2.10 |
| Negative prices | 5 rows (all the A bad debt rows above) |
| Zero prices | 6,202 rows |
| Prices under 0.01 | 6,225 rows |
| Prices over 100 | 1,946 rows |
| Prices over 1,000 | 245 rows |
| Zero price rows with positive quantity | 2,745 |

The 245 high prices are almost all non-product charges: stock code `M` (Manual) 166 rows, `AMAZONFEE` 39, `DOT` 29, `BANK CHARGES` 2, `D` 2, `POST` 2, `CRUK` 2, `ADJUST` 1, `B` 1, and one product code. The highest is a Manual line at 38,970.00 on invoice C556445.

## 6. Quantities

| Check | Result |
|---|---|
| Minimum | -80,995 |
| Maximum | 80,995 |
| Mean | 9.94 |
| Median | 3 |
| Negative rows | 22,950 |
| Zero quantity rows | 0 |
| Over 1,000 units | 352 rows |
| Over 10,000 units | 9 rows |

The 11 rows with absolute quantity over 10,000:

| Invoice | Code | Description | Quantity | Price | Date |
|---|---|---|---|---|---|
| 497946 | 37410 | BLACK AND WHITE PAISLEY FLOWER MUG | 19,152 | 0.10 | 2010-02-15 |
| 501534 | 21099 | SET/6 STRAWBERRY PAPER CUPS | 12,960 | 0.10 | 2010-03-17 |
| 501534 | 21092 | SET/6 STRAWBERRY PAPER PLATES | 12,480 | 0.10 | 2010-03-17 |
| 501534 | 21091 | SET/6 WOODLAND PAPER PLATES | 12,960 | 0.10 | 2010-03-17 |
| 501534 | 21085 | SET/6 WOODLAND PAPER CUPS | 12,744 | 0.10 | 2010-03-17 |
| 507637 | 84016 | FLAG OF ST GEORGE CAR FLAG | 10,200 | 0.00 | 2010-05-10 |
| 541431 | 23166 | MEDIUM CERAMIC TOP STORAGE JAR | 74,215 | 1.04 | 2011-01-18 |
| C541433 | 23166 | MEDIUM CERAMIC TOP STORAGE JAR | -74,215 | 1.04 | 2011-01-18 |
| 578841 | 84826 | ASSTD DESIGN 3D PAPER STICKERS | 12,540 | 0.00 | 2011-11-25 |
| 581483 | 23843 | PAPER CRAFT, LITTLE BIRDIE | 80,995 | 2.08 | 2011-12-09 |
| C581484 | 23843 | PAPER CRAFT, LITTLE BIRDIE | -80,995 | 2.08 | 2011-12-09 |

Two of these are famous buy-then-cancel cases: 74,215 jars bought at 10:01 and cancelled at 10:17 the same morning, and 80,995 paper craft sets bought and cancelled 12 minutes apart. The second one is outside the lesson slice. The first one is inside it and matters for the plan (section 12).

## 7. Duplicates and the 9-day overlap between the two sheets

The two sheets are not two clean separate years. Sheet 2009-2010 ends on 2010-12-09 and sheet 2010-2011 starts on 2010-12-01, so 1 to 9 Dec 2010 appears in both sheets:

| Check | Result |
|---|---|
| Rows in 1 to 9 Dec 2010, sheet 2009-2010 | 22,523 |
| Rows in 1 to 9 Dec 2010, sheet 2010-2011 | 22,523 |
| Distinct rows that appear in both sheets | 22,202 |
| Matching row pairs when joining the sheets | 23,221 |
| Exact duplicate rows, both sheets stacked | 34,335 |
| Duplicate rows within sheet 2009-2010 | 6,865 |
| Duplicate rows within sheet 2010-2011 | 5,268 |

So duplicates come from two places: the 9-day overlap between the yearly sheets, and genuine repeated lines inside a sheet. The first is a file artefact. The second is normal for this kind of system export (for example, the same product appearing on two lines of one invoice with different quantities).

Consequence for the course: the lesson slice is taken from the 2010-2011 sheet only, so no row is counted twice because of the overlap. `drop_duplicates()` in S4 still removes real repeated lines.

## 8. Stock codes that are not products

A real product code is 5 digits, optionally followed by 1 or 2 letters, any case: `^\d{5}[A-Za-z]{0,2}$`. That rule covers 1,061,277 rows without touching the text. One more row has a real product code with a trailing space (`47503J `), so after stripping spaces 1,061,278 rows are product rows. There are no 4-digit or 6-digit codes and no 3-letter suffixes.

The remaining 6,094 rows (0.57%) do not match that pattern. 6,093 of them carry 62 non-product codes:

| Code or group | Rows | Description |
|---|---|---|
| POST | 2,122 | POSTAGE |
| DOT | 1,446 | DOTCOM POSTAGE |
| M | 1,421 | Manual |
| C2 | 282 | CARRIAGE |
| D | 177 | Discount |
| S | 104 | SAMPLES |
| BANK CHARGES | 102 | Bank Charges |
| ADJUST | 67 | Adjustment by john |
| AMAZONFEE | 43 | AMAZON FEE |
| DCGS catalogue codes (34 codes) | 158 | old Dotcomgiftshop catalogue and voucher codes |
| gift_0001 vouchers (9 codes) | 100 | Gift vouchers |
| PADS | 19 | PADDING |
| CRUK | 16 | CRUK Commission |
| TEST001, TEST002 | 17 | Test products |
| B | 6 | Adjust bad debt |
| m | 5 | Manual, lower case |
| ADJUST2 | 3 | Adjustment by Peter |
| SP1002 | 3 | KID'S CHALKBOARD/EASEL |
| C3 | 1 | carriage |
| GIFT | 1 | gift |

The last row that fails the pattern is `47503J` with a trailing space. It is a real product code with a typo, and after stripping the text it becomes a product like the others.

Course rule for S4: instead of a hard-coded list, the notebook keeps the rows whose stock code starts with a digit. Every real product code starts with a digit. Every charge, voucher, manual line and old code starts with a letter. In the slice this one rule removes postage, fees, samples, discounts, manual lines, gift vouchers and the old DCGS codes in one step, and it cannot go out of date when a new fee code appears.

The slice has 588 non-product rows in total. 565 of them are the eight main codes: POST 217 (216 plus one with a missing description), DOT 175, M 90, S 30, C2 20, D 13, AMAZONFEE 11, BANK CHARGES 9. The other 23 rows are gift vouchers, old DCGS codes and lower-case Manual entries. The hard-coded 8-code list would leave 19 of those rows in the clean table and 11 non-product codes would show up as products. The first-character rule removes the 474 rows still present at that step; no non-product row survives to the clean table. The other 114 non-product rows were already removed by the dedupe, cancellation, quantity and price steps.

Product code case is messy: 3,471 rows in the whole file and 541 rows in the raw slice have a lower-case letter in the code, for example `15056bl`, `85123a`, `84997c`. These are real products, but the same product can appear under two spellings (`85123A` and `85123a`), so a groupby on stock code splits it. The course does not clean this in S4 (it would add a new concept and risk the merging lesson in S6); the teacher card notes it as a data quirk. In the clean slice, 40 stock codes have more than one description.

## 9. Descriptions

| Check | Result |
|---|---|
| Missing descriptions | 4,382 rows, all with price 0 |
| Rows whose description has leading or trailing spaces | 213,035 (20.0%) |
| Distinct descriptions after stripping and upper-casing | 5,631 |

So the description text is dirty in small ways (spaces) and has 4,382 missing values. (5,631 distinct descriptions after stripping and upper-casing; 5,632 if the missing value is counted as the text "nan".) The S4 cleaning plan does not drop missing descriptions; product analysis uses the stock code, and all product rows in the clean slice keep a description (0 missing after the filters). The `description` column is only used for labels in S6.

## 10. Countries and revenue

| Country | Rows |
|---|---|
| United Kingdom | 981,330 (91.94%) |
| EIRE | 17,866 |
| Germany | 17,624 |
| France | 14,330 |
| Netherlands | 5,140 |
| Spain | 3,811 |
| Switzerland | 3,189 |
| Belgium | 3,123 |
| Portugal | 2,620 |
| Australia | 1,913 |
| Channel Islands | 1,664 |
| Italy | 1,534 |
| Norway | 1,455 |
| Sweden | 1,364 |
| Cyprus | 1,176 |

43 countries in total. Revenue totals on the whole raw file, using `quantity * price`:

| Measure | Value |
|---|---|
| Gross revenue, all rows | 19,287,250.57 |
| Sum of positive rows | 20,972,968.14 |
| Sum of negative rows | -1,685,717.57 |
| Rows with negative revenue | 19,498 |

## 11. Rows per month, whole file

| Month | Rows | Month | Rows |
|---|---|---|---|
| 2009-12 | 45,228 | 2010-12 | 65,004 |
| 2010-01 | 31,555 | 2011-01 | 35,147 |
| 2010-02 | 29,388 | 2011-02 | 27,707 |
| 2010-03 | 41,511 | 2011-03 | 36,748 |
| 2010-04 | 34,057 | 2011-04 | 29,916 |
| 2010-05 | 35,323 | 2011-05 | 37,030 |
| 2010-06 | 39,983 | 2011-06 | 36,874 |
| 2010-07 | 33,383 | 2011-07 | 39,518 |
| 2010-08 | 33,306 | 2011-08 | 35,284 |
| 2010-09 | 42,091 | 2011-09 | 50,226 |
| 2010-10 | 59,098 | 2011-10 | 60,742 |
| 2010-11 | 78,015 | 2011-11 | 84,711 |
|  |  | 2011-12 | 25,526 |

Note: 2010-12 counts the overlap rows twice. November and December are the peak months, as expected for giftware.

## 12. Proposed lesson slice for S4 to S9

**Rule:** take every row of the `Year 2010-2011` sheet whose InvoiceDate falls from 2010-12-01 00:00 up to but not including 2011-03-01 00:00. Write it to `data/online_retail_ii_lesson.csv`, uncleaned. This is one time window of three months, from the same sheet, so the 9-day overlap does not duplicate any row.

| Check | Value |
|---|---|
| Rows | 105,335 |
| Columns | 8 |
| First timestamp | 2010-12-01 08:26 |
| Last timestamp | 2011-02-28 17:04 |
| File size as CSV | 9,279,397 bytes (9.28 MB) |
| Invoices | 4,894 |
| Products (distinct stock codes) | 3,159 |
| Countries | 31 |
| Missing Customer ID | 36,210 (34.4%) |
| Missing Description | 304 |
| Cancellation rows | 1,904 (805 distinct C invoices) |
| Exact duplicate rows | 975 |
| Negative quantity rows | 2,118 (1,904 cancellation rows plus 214 adjustments) |
| Zero price rows | 540 |
| Negative price rows | 0 |
| Non-product code rows | 588 (565 main codes plus 23 vouchers and old codes) |
| Germany rows | 1,741 |
| Revenue, raw rows | 1,807,019.93 |

What the slice deliberately excludes: the 2009-2010 year, the November 2011 peak, the bad debt A invoices (three in 2010 and three in August 2011), the 80,995 unit buy-and-cancel pair (December 2011) and all rows outside the three months. Those rows stay in the untouched raw file, and no learner material claims anything about them.

The CSV will keep the original column names, the original column order and the original row order. `Customer ID` is blank when missing, `Invoice` and `StockCode` are written as text, `InvoiceDate` is written as `YYYY-MM-DD HH:MM:SS`. In Colab, `read_csv` gives `quantity` as int, `price` as float, `customer_id` as float with NaN, and the three text columns as object.

The first rows are the first rows of the 2010-2011 sheet, which makes the story continuous from S1 to S4:

| Invoice | Code | Description | Quantity | Price |
|---|---|---|---|---|
| 536365 | 85123A | WHITE HANGING HEART T-LIGHT HOLDER | 6 | 2.55 |
| 536365 | 71053 | WHITE METAL LANTERN | 6 | 3.39 |
| 536365 | 84406B | CREAM CUPID HEARTS COAT HANGER | 8 | 2.75 |
| 536365 | 84029G | KNITTED UNION FLAG HOT WATER BOTTLE | 6 | 3.39 |
| 536365 | 84029E | RED WOOLLY HOTTIE WHITE HEART. | 6 | 3.39 |
| 536365 | 22752 | SET 7 BABUSHKA NESTING BOXES | 2 | 7.65 |
| 536365 | 21730 | GLASS STAR FROSTED T-LIGHT HOLDER | 6 | 4.25 |

The brief's sample numbers are real: the first 7 quantities are [6, 6, 8, 6, 6, 2, 6], `len` is 7, `sum` is 40, `min` is 2, `max` is 8, index 0 is 6, index 2 is 8, and index -1 is 6. `6 * 2.55` prints `15.299999999999999`, so the float teaching moment is real.

### The S4 cleaning steps on this slice

| Step | Rows left | Rows removed |
|---|---|---|
| Start | 105,335 |  |
| `drop_duplicates()` | 104,360 | 975 |
| Remove invoices starting with C | 102,471 | 1,889 |
| Keep `quantity > 0` | 102,257 | 214 |
| Keep `price > 0` | 101,933 | 324 |
| Keep only product codes (first character is a digit) | 101,459 | 474 |
| Remove invoice 541431 (see below) | 101,458 | 1 |

Clean table after all steps:

| Check | Value |
|---|---|
| Rows | 101,458 |
| Invoices | 3,723 |
| Products | 3,066 |
| Customers with an ID | 1,679 |
| Rows with missing Customer ID | 35,364 (34.9%) |
| Revenue, sum of quantity times price | 1,876,534.04 |
| Missing descriptions | 0 |
| Columns in the saved clean file | 10: the 8 original columns plus `revenue` and `month` |

### The cancelled giant order inside the slice

Invoice `541431`, 18 Jan 2011 10:01, customer 12346, stock code `23166`, MEDIUM CERAMIC TOP STORAGE JAR, 74,215 units at 1.04, revenue 77,183.60. Sixteen minutes later invoice `C541433` cancels the same quantity at the same price. The simple S4 cleaning drops the C row, so the positive 77,183.60 line stays, becomes the number one product, and counts as 3.95% of revenue if it is kept. That is wrong for a revenue analysis: the sale was cancelled.

Proposal: let the learner find this line in the S4 "biggest revenue rows" step, investigate it, and remove that one invoice with a commented line. The cleaning log then records one extra decision. Full reasons and options are in `PLAN.md`, open question 7. If Bryan prefers not to touch it, the slice numbers become: revenue 1,953,717.64, products 3,067, top product 23166 at 77,183.60, and the ABC split changes from A 671 products to A 649 products.

### On the clean table (with invoice 541431 removed)

| Check | Value |
|---|---|
| Class A products | 671 (21.9% of products), 1,500,839.03 revenue (79.98%) |
| Class B products | 794 (25.9%), 281,777.11 (15.02%) |
| Class C products | 1,601 (52.2%), 93,917.90 (5.00%) |
| Top product | 22423 REGENCY CAKESTAND 3 TIER, 51,504.85 (2.74%) |
| Second product | 85123A WHITE HANGING HEART T-LIGHT HOLDER, 30,780.98 (1.64%) |
| Third product | 79321 CHILLI LIGHTS, 17,013.92 (0.91%) |
| Top 10 products, cumulative share | 9.62% |
| United Kingdom share | 84.82% |
| Top country by revenue | United Kingdom, 1,591,694.50 |
| Next countries | Netherlands 58,182.55, EIRE 43,426.19, Germany 37,365.63, France 32,392.39, Australia 24,678.48 |
| Revenue by month | 2010-12: 775,572.23; 2011-01: 593,178.39; 2011-02: 507,783.42 |
| Trading days | 68 |
| Best day | 2010-12-07, 81,454.99 |
| Worst day | 3,439.67 |
| Distinct stock codes with more than one description | 40 |
| Rows with a lower-case letter in the stock code (raw slice) | 541 |
| Product rows and name pairs for the S6 merge | 3,066 product rows and 3,107 code-description pairs; the merge check goes 3,066 to 3,107 to 3,066 after deduping names |

S5 key finding: 21.9% of products (671 of 3,066) bring 79.98% of revenue. The slide title can say "22% of the products bring 80% of the revenue". These numbers come from the run above.

### Alternative window, if Bryan prefers no special case in S4

Window 2011-02-01 to 2011-04-30, also from the 2010-2011 sheet only:

| Check | Value |
|---|---|
| Raw rows | 94,371 |
| Clean rows | 90,771 |
| Clean revenue | 1,712,846.69 |
| Top product | 22423 REGENCY CAKESTAND 3 TIER, 44,181.69 |
| Second product | 47566 PARTY BUNTING, 24,249.39 |
| Revenue by month | 2011-02: 507,783.42; 2011-03: 689,708.49; 2011-04: 515,354.78 |

This window has no single order that distorts the product ranking, but it does not contain the first rows of the sheet, so the S1 to S3 examples would have to come from different rows, and the month chart loses the December peak.

## 13. Key facts that the course materials may use

These are verified and safe to reuse. All money is GBP.

| Fact | Value |
|---|---|
| File period | 1 Dec 2009 to 9 Dec 2011 |
| Rows | 1,067,371 |
| UK share of rows | 91.94% |
| Rows with missing customer | 243,007 (22.77%) |
| Cancellation rows | 19,494 |
| Lesson slice rows | 105,335 |
| Lesson slice clean rows | 101,458 |
| Lesson slice clean revenue | 1,876,534.04 |
| Lesson slice products | 3,066 |
| Class A products and revenue share | 671 (21.9%), 79.98% |
| Top product | REGENCY CAKESTAND 3 TIER, 51,504.85 |
| December 2010 slice revenue | 775,572.23 |
| January 2011 slice revenue | 593,178.39 |
| February 2011 slice revenue | 507,783.42 |
| Slice best day | 2010-12-07, 81,454.99 |
| Slice Germany rows before and after cleaning | 1,741 and 1,514 |
| Slice first 7 quantities | 6, 6, 8, 6, 6, 2, 6 |
| `6 * 2.55` | 15.299999999999999 |
| `round(6 * 2.55, 2)` | 15.3 |

### Quirks the course materials must treat honestly

- Cancellations are removed in S4, but the original positive sale stays in the clean table unless it is the one giant order. About 1% of clean revenue inside the slice is later cancelled. Some slice sales are cancelled after the window, for example invoice 540815 in April 2011, so the teacher note says "about 1% inside the slice".
- 35,364 clean rows (34.9%) have no customer ID. Product analysis keeps them; customer analysis cannot.
- 541 rows in the raw slice carry a lowercase letter in the stock code, so a few products split across two spellings. The course does not normalise them.
- 40 stock codes in the clean slice have more than one description. The S6 merge keeps the first one and checks the row count before and after.
- The slice is one UK giftware retailer in three months. Any country chart needs to say "outside the UK" because the UK is 84.82% of revenue.
- Prices are GBP. Rounding for slides is allowed, but the exact value goes in the notes and the answer key.

## 14. How to reproduce

The raw file is untouched. The analysis used Python 3.12.13 with pandas 2.3.3, matplotlib 3.11.2, seaborn 0.13.2, openpyxl 3.1.5. Internal scripts (not delivered):

- `_tools/convert_sheets.py` converts the two xlsx sheets to CSV in `data/work/`.
- `_tools/fact_check.py` checks 155 values against the data. Run it after any data or doc change. It reads the CSV conversions in `data/work/`, so run `convert_sheets.py` first if they are missing.

## 15. What Bryan must decide before Phase 2

1. Confirm the lesson slice rule in section 12 (2010-12-01 to 2011-02-28, 2010-2011 sheet only), or ask for the alternative in section 12.
2. Confirm how to treat the cancelled giant order in S4: remove invoice 541431 with a commented line (recommended), or leave it in.
3. Confirm the non-product rule for S4: keep stock codes whose first character is a digit (recommended; it removes the 474 non-product rows still present at that step and none reaches the clean table), instead of a hard-coded list.
4. Answer the five open items in section 15 of the build brief (video topic and length, S2 date, WIB time, email, photo permission).
5. Confirm the additional plan choices listed in `PLAN.md` section 9, in particular excluding the UK from the seaborn country chart in S6 and addressing the learner by name or not.

All other [VERIFY] items in the brief are now checked and correct: column names, cancellation prefix C, number of duplicates, missing values, negative and zero prices, non-product codes and the 6 * 2.55 float behaviour.
