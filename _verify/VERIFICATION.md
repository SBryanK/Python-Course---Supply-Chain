# PySC-101 Phase 1: independent data verification

Verifier: data-verifier. Date: 2 Nov 2026.
Method: every number below was computed independently from the raw file
`data/raw/online_retail_II.xlsx` (both sheets, `pd.read_excel` with `Invoice`,
`StockCode` and `Customer ID` read as text, `InvoiceDate` parsed as datetime).
Pre-existing JSON/CSV files were not used as a source; the Lead's CSVs and JSON
were opened only afterwards, to attribute the differences listed in section 13.

- Raw file size: 45,622,278 bytes. sha256: `bcbe73b35f5b7babf197fb0cb983a11f5d9ff929078d4aa53d171b1f2df2e980` (matches the Lead's report).
- Zip sha256: `572e36277c2390fbfde10664750731e0a86f55e33470d91919085f0408e67bfb` (matches).
- Environment: Python 3.12.13, pandas 2.3.3, openpyxl 3.1.5, `MPLCONFIGDIR=$PWD/_tools/mplconfig`.
- Scripts and raw output: `_verify/load_raw.py`, `_verify/analyze.py` (items 1 to 11),
  `_verify/verify2.py` (cross-check of every claim in `data/EXPLORATION.md`).
  Results: `_verify/results.json`, `_verify/results.txt`, `_verify/lead_claims_check.json`.
- Cross-check of sheet sizes with openpyxl dimensions: 525,462 and 541,911 rows
  including the header row, consistent with 525,461 and 541,910 data rows.

Verdict: items 1 to 11 all reproduced. The Lead's whole-file, slice, clean-table,
ABC, product, country, monthly and float numbers match. Four report defects found
(section 13); they are in text and table arithmetic, not in the cleaned-data
pipeline.

## 1. Rows and date ranges

| Sheet | Rows | Min InvoiceDate | Max InvoiceDate |
|---|---|---|---|
| Year 2009-2010 | 525,461 | 2009-12-01 07:45 | 2010-12-09 20:01 |
| Year 2010-2011 | 541,910 | 2010-12-01 08:26 | 2011-12-09 12:50 |
| Combined | 1,067,371 | 2009-12-01 07:45 | 2011-12-09 12:50 |

No missing InvoiceDate values.

## 2. Missing values and dtypes (combined)

| Column | Missing | Share | dtype (text read) |
|---|---|---|---|
| Invoice | 0 | 0% | object |
| StockCode | 0 | 0% | object |
| Description | 4,382 | 0.4105% | object |
| Quantity | 0 | 0% | int64 |
| InvoiceDate | 0 | 0% | datetime64[ns] |
| Price | 0 | 0% | float64 |
| Customer ID | 243,007 | 22.7669% | object |
| Country | 0 | 0% | object |

Per sheet: Description missing 2,928 (2009-2010) and 1,454 (2010-2011);
Customer ID missing 107,927 and 135,080. Every missing Description row has
Price = 0 (4,382 of 4,382). A default pandas read gives Customer ID float64;
it is object here only because it was read as text.

## 3. Cancellations and adjustments

| Check | Result |
|---|---|
| Rows with Invoice starting with C (case-insensitive) | 19,494 (2009-2010: 10,206; 2010-2011: 9,288) |
| Distinct C invoices | 8,292 |
| C rows with Quantity >= 0 | 1 |
| C rows with negative Quantity | 19,493 |
| Non-C rows with Quantity < 0 | 3,457 |

The single C row with Quantity >= 0 is `C496350`, stock code `M` (Manual),
Quantity 1, Price 373.57, 2010-02-01 08:24, no Customer ID, United Kingdom.
Of the 3,457 non-C negative rows, 2,689 have a missing Description; the most
common descriptions are `check` 123, `damages` 84, `?` 83, `damaged` 78,
`missing` 27, `sold as set on dotcom` 20. These are stock adjustments, not sales.

## 4. Prices and extreme quantities

| Check | Result |
|---|---|
| Negative Price rows | 5 (all `Adjust bad debt`, StockCode `B`, A-prefix invoice) |
| Zero Price rows | 6,202 |
| Price > 1000 rows | 245 |
| abs(Quantity) > 10000 rows | 11 |
| Quantity == 0 rows | 0 |

The 5 negative prices are: A506401 -53,594.36; A516228 -44,031.79;
A528059 -38,925.87; A563186 -11,062.06; A563187 -11,062.06 (all Quantity 1).
Price min -53,594.36, max 38,970.00 (invoice C556445, StockCode M), mean 4.6494,
median 2.10. Prices under 0.01: 6,225 rows; over 100: 1,946 rows; zero price
with positive quantity: 2,745 rows.
Quantity min -80,995, max 80,995, mean 9.94, median 3; negative rows 22,950;
over 1,000 units 352 rows; over 10,000 units 9 rows.
The 11 rows with abs(Quantity) > 10,000 are the 2 giant buy-cancel pairs
(74,215 jars on 541431 / C541433; 80,995 paper craft on 581483 / C581484),
the 5 x 12,480 to 12,960 Denmark paper lines on 501534, 19,152 mugs on 497946,
10,200 flags on 507637 and 12,540 stickers on 578841.

## 5. Exact duplicates and the December 2010 overlap

Stacking both sheets on the 8 data columns gives 34,335 duplicate rows
(6,865 within 2009-2010, 5,268 within 2010-2011; the rest are cross-sheet pairs).

Dec 2010 overlap window `2010-12-01 00:00 <= InvoiceDate < 2010-12-10 00:00`:

| Check | Result |
|---|---|
| Rows in window, 2009-2010 sheet | 22,523 |
| Rows in window, 2010-2011 sheet | 22,523 |
| Distinct rows shared by both sheets | 22,202 |
| Inner-join row pairs (same 8 columns) | 23,221 |
| Multisets of the two windows | identical |

So the whole tail of the 2009-2010 sheet (1 to 9 Dec 2010) is repeated at the
start of the 2010-2011 sheet, including its repeated lines. The lesson slice
comes from the 2010-2011 sheet only, so the overlap cannot double count it.

## 6. Non-product stock codes (rule `^\d{5}[A-Za-z]{0,2}$`)

Real product rows: 1,061,277. Non-product rows: 6,094 (0.57%), in 63 distinct
codes:

```
POST 2122 | DOT 1446 | M 1421 | C2 282 | D 177 | S 104 | BANK CHARGES 102
ADJUST 67 | AMAZONFEE 43 | DCGS0058 31 | gift_0001_20 29 | gift_0001_30 29
DCGSSGIRL 25 | DCGSSBOY 23 | PADS 19 | gift_0001_10 16 | CRUK 16
TEST001 15 | DCGS0076 15 | DCGS0003 14 | gift_0001_50 8 | gift_0001_40 7
DCGS0069 6 | B 6 | DCGS0004 5 | m 5 | gift_0001_80 4 | DCGS0066N 4
DCGS0072 4 | SP1002 3 | gift_0001_70 3 | DCGS0070 3 | DCGS0068 3 | ADJUST2 3
gift_0001_90 2 | gift_0001_60 2 | DCGS0062 2 | DCGS0037 2 | TEST002 2
then 1 each: DCGS0067, DCGS0044, C3, DCGS0006, DCGS0016, DCGS0027, DCGS0036,
DCGS0039, DCGS0041, DCGS0053, DCGS0071, DCGS0055, DCGS0056, GIFT, DCGS0057,
DCGS0059, DCGS0060, DCGSLGIRL, DCGSLBOY, DCGS0075, DCGS0074, DCGS0073,
DCGS0066P, and '47503J ' (note the trailing space)
```

Grouped: POST 2,122; DOT 1,446; M 1,421; C2 282; D 177; S 104; BANK CHARGES 102;
ADJUST 67; AMAZONFEE 43; DCGS-prefix 158 across 34 codes; gift_0001_* vouchers
100 across 9 codes; PADS 19; CRUK 16; TEST001/TEST002 17; B 6; m 5; C3 1;
GIFT 1; ADJUST2 3; SP1002 3; `'47503J '` 1.
Total 6,094. If StockCode is stripped first: 62 codes, 6,093 rows, 1,061,278
product rows, because `'47503J '` becomes the valid product code `47503J`.
There are no 4-digit or 6-digit codes and no 3-letter suffixes, with or without
stripping.

## 7. A-prefix invoices

6 rows, 6 distinct invoices, all StockCode `B`, Description `Adjust bad debt`,
Quantity 1, missing Customer ID, United Kingdom:

| Invoice | InvoiceDate | Price |
|---|---|---|
| A506401 | 2010-04-29 13:36 | -53,594.36 |
| A516228 | 2010-07-19 11:24 | -44,031.79 |
| A528059 | 2010-10-20 12:04 | -38,925.87 |
| A563185 | 2011-08-12 14:50 | +11,062.06 |
| A563186 | 2011-08-12 14:51 | -11,062.06 |
| A563187 | 2011-08-12 14:52 | -11,062.06 |

Invoice first-character counts for the whole file: `5` 939,382; `4` 108,489;
`C` 19,494; `A` 6.

## 8. Lesson slice (2010-2011 sheet, [2010-12-01, 2011-03-01))

Raw slice: 105,335 rows, 8 columns, 2010-12-01 08:26 to 2011-02-28 17:04.
Missing Customer ID 36,210; missing Description 304; cancellation rows 1,904
(805 distinct C invoices); duplicate rows 975; non-product rows 588 under the
section 6 rule (565 of them carry the 8 lesson codes); negative Quantity rows
2,118; zero Price rows 540; negative Price rows 0; raw revenue 1,807,019.93.

Cleaning steps, exact sequence:

| Step | Rows left | Removed |
|---|---|---|
| start | 105,335 | - |
| drop_duplicates | 104,360 | 975 |
| remove Invoice starting with C | 102,471 | 1,889 |
| keep Quantity > 0 | 102,257 | 214 |
| keep Price > 0 | 101,933 | 324 |
| remove StockCode in POST, DOT, M, S, C2, D, BANK CHARGES, AMAZONFEE | 101,478 | 455 |
| remove Invoice 541431 | 101,477 | 1 |

Clean table: 101,477 rows, 3,723 invoices, 3,077 distinct StockCode,
1,679 customers with an ID, 35,383 missing Customer ID (34.9%), 0 missing
Description. Clean total revenue = sum(Quantity * Price) = **1,876,839.90**.
Rows removed by the 8-code filter: POST 217, DOT 175, M 90, S 30, C2 20, D 13,
AMAZONFEE 11, BANK CHARGES 9.
The removed invoice 541431 is 74215 x 1.04 = 77,183.60 (customer 12346,
23166, 2011-01-18 10:01); its cancellation C541433 is 16 minutes later.

## 9. Final clean table metrics

- Distinct StockCode: 3,077. Total revenue: 1,876,839.90.
- Top 10 products by revenue:

| Rank | StockCode | Description | Revenue | Share |
|---|---|---|---|---|
| 1 | 22423 | REGENCY CAKESTAND 3 TIER | 51,504.85 | 2.7442% |
| 2 | 85123A | WHITE HANGING HEART T-LIGHT HOLDER | 30,780.98 | 1.6400% |
| 3 | 79321 | CHILLI LIGHTS | 17,013.92 | 0.9065% |
| 4 | 85099B | JUMBO BAG RED RETROSPOT | 14,684.04 | 0.7824% |
| 5 | 21623 | VINTAGE UNION JACK MEMOBOARD | 14,050.55 | 0.7486% |
| 6 | 82484 | WOOD BLACK BOARD ANT WHITE FINISH | 11,013.87 | 0.5868% |
| 7 | 22470 | HEART OF WICKER LARGE | 10,999.97 | 0.5861% |
| 8 | 22469 | HEART OF WICKER SMALL | 10,815.52 | 0.5763% |
| 9 | 22720 | SET OF 3 CAKE TINS PANTRY DESIGN | 10,050.01 | 0.5355% |
| 10 | 84029E | RED WOOLLY HOTTIE WHITE HEART. | 9,652.62 | 0.5143% |

Top 10 cumulative share: 9.62%. Top 3 are 22423, 85123A, 79321.

- ABC split (products ranked by revenue descending, cumulative share <= 0.80 A,
  <= 0.95 B, else C):

| Class | Products | % of products | Revenue | % of revenue |
|---|---|---|---|---|
| A | 671 | 21.81% | 1,500,839.03 | 79.97% |
| B | 796 | 25.87% | 282,144.50 | 15.03% |
| C | 1,610 | 52.32% | 93,856.37 | 5.00% |

- Country revenue top 5: United Kingdom 1,592,000.36 (84.82%);
  Netherlands 58,182.55 (3.10%); EIRE 43,426.19 (2.31%);
  Germany 37,365.63 (1.99%); France 32,392.39 (1.73%). 31 countries in the slice.
- Monthly revenue: 2010-12 775,717.50 (40,829 rows); 2011-01 593,255.86
  (33,904 rows); 2011-02 507,866.54 (26,744 rows). Sum equals total revenue.
- Extra confirmed: 68 trading days; best day 2010-12-07 81,454.99; worst day
  3,439.67; 40 stock codes with more than one description; 541 rows with a
  lower-case letter in the StockCode.

## 10. First 7 data rows of the 2010-2011 sheet (raw)

| Invoice | StockCode | Description | Quantity | Price |
|---|---|---|---|---|
| 536365 | 85123A | WHITE HANGING HEART T-LIGHT HOLDER | 6 | 2.55 |
| 536365 | 71053 | WHITE METAL LANTERN | 6 | 3.39 |
| 536365 | 84406B | CREAM CUPID HEARTS COAT HANGER | 8 | 2.75 |
| 536365 | 84029G | KNITTED UNION FLAG HOT WATER BOTTLE | 6 | 3.39 |
| 536365 | 84029E | RED WOOLLY HOTTIE WHITE HEART. | 6 | 3.39 |
| 536365 | 22752 | SET 7 BABUSHKA NESTING BOXES | 2 | 7.65 |
| 536365 | 21730 | GLASS STAR FROSTED T-LIGHT HOLDER | 6 | 4.25 |

All seven are InvoiceDate 2010-12-01 08:26, Customer ID 17850, United Kingdom.
Quantities [6, 6, 8, 6, 6, 2, 6]: len 7, sum 40, min 2, max 8.

## 11. Float check

- `repr(6 * 2.55)` = `'15.299999999999999'`
- `repr(round(6 * 2.55, 2))` = `'15.3'`
- `15.3 == 6 * 2.55` is `False`.

## 12. Other whole-file claims checked (all matched)

Distinct invoices 53,628; distinct customers 5,942; countries 43; stock codes
5,305; descriptions 5,698. Sheet date ranges, all 25 monthly row counts (sum
1,067,371), country row counts (UK 981,330 = 91.94%; through Cyprus 1,176),
gross revenue 19,287,250.57, positive-row revenue 20,972,968.14, negative-row
revenue -1,685,717.57, rows with negative revenue 19,498, Description rows with
outer spaces 213,035, lowercase-code rows 3,471, high-price breakdown (M 166,
AMAZONFEE 39, DOT 29, BANK CHARGES 2, D 2, POST 2, CRUK 2, ADJUST 1, 84016 1,
B 1), and every clean-table and alternative-window claim in the Lead's report.
Kept-giant what-if: 101,478 rows, revenue 1,954,023.50, top product 23166
77,183.60 (3.95%), ABC A 649 / B 798 / C 1,631.

## 13. Discrepancies found in data/EXPLORATION.md

1. Section 8, non-product code table arithmetic. The table rows sum to 6,040,
   not the stated 6,094. The DCGS group is 158 rows across 34 codes, not 113;
   `gift_0001_10` to `gift_0001_90` is 100 rows across 9 codes, not 98.
   Three entries are omitted: ADJUST2 (3 rows), SP1002 (3 rows) and
   `'47503J '` (1 row, StockCode has a trailing space). Corrected groups give
   exactly 6,094. Consequence: if StockCode is stripped first, product coverage
   becomes 1,061,278 rows / 62 non-product codes, so the rule only covers
   1,061,277 rows when applied to the unstripped codes.
2. Sections 8 and 12, lesson-slice non-product count. By the report's own
   product-code rule the raw slice has 588 non-product rows, not 565. The 565
   figure counts only the 8 codes that the S4 cleaning step removes. The other
   23 rows are gift vouchers (`gift_0001_20` 3, `gift_0001_30` 3,
   `gift_0001_50` 1, `gift_0001_40` 1), DCGS voucher codes (12 rows) and
   lowercase `m` (1 row). So the section 8 sentence "only 8 of these codes
   appear" is wrong: 23 distinct non-product codes appear in the slice.
   Nineteen of those rows (11 codes: DCGS0003, DCGS0076, DCGS0069, DCGS0070,
   DCGSSBOY, DCGSSGIRL, gift_0001_20, gift_0001_30, gift_0001_40,
   gift_0001_50, m) survive the exact cleaning sequence, worth 305.86 revenue.
   Therefore "products 3,077" includes 11 non-product codes; excluding them
   gives 3,066 products and revenue 1,876,534.04, with ABC A 671, B 794,
   C 1,601. Low impact, but the report should say the filter is partial.
3. Section 9, distinct descriptions. After stripping and upper-casing there are
   5,631 distinct non-missing descriptions, not 5,632. The Lead's script
   (`_tools/explore_details.py`, line 146) calls `.astype(str)` before
   `nunique()`, which turns the 4,382 missing values into the single string
   `nan` and adds one to the count.
4. Section 12, alternative window cleaning definition. "Clean rows 90,792" for
   the 2011-02-01 to 2011-04-30 window uses a 13-code non-product filter
   (POST, DOT, M, BANK CHARGES, C2, D, S, AMAZONFEE, ADJUST, CRUK, PADS, B,
   GIFT), while the canonical S4 step lists only 8 codes. With the canonical
   8-code filter the window has 90,793 clean rows. The one-row difference is a
   PADS line with price 0.001, which is why revenue is identical to the cent
   (1,713,178.04). The alt-window matched-cancelled-sale numbers reproduce
   exactly (506 rows, 13,311.65, 0.78%).

Minor wording point, not a number error: section 8 says "in the slice, 40 stock
codes have more than one description". The raw slice has 69; 40 is the clean
table figure. Also the report's "Memory, combined, pandas 313.2 MB" depends on
the read dtypes (Customer ID float64 there, object here); it is not a data fact.

Everything else checked out, including the two audit-relevant traps: the
9-day cross-sheet overlap is real and fully duplicated (identical multisets),
and `6 * 2.55` is `15.299999999999999`.
