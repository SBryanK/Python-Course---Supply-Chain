# Lesson data

`online_retail_ii_lesson.csv` is the teaching file. It is not cleaned: cleaning is the learner's work in Session 4.

**Source.** Chen, D. (2012). Online Retail II [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5CG6D. Licence: CC BY 4.0. The file is an adaptation of the dataset and stays under CC BY 4.0.

**What it is.** Transactions from a UK online gift shop. Prices are in pounds.

**Slice rule.** Every row of the `Year 2010-2011` sheet with `InvoiceDate` from 2010-12-01 00:00 up to but not including 2011-03-01 00:00. Built by `_tools/build_slice.py`.

| Property | Value |
|---|---|
| Rows / columns | 105,335 / 8 |
| Dates | 2010-12-01 08:26 to 2011-02-28 17:04 |
| Size | about 9.3 MB |

| Column | Meaning |
|---|---|
| `Invoice` | Invoice number. Starts with C for a cancellation |
| `StockCode` | Product code |
| `Description` | Product name |
| `Quantity` | Units on the line. Negative for cancellations |
| `InvoiceDate` | Date and time |
| `Price` | Unit price in pounds |
| `Customer ID` | Customer number. Empty for many rows |
| `Country` | Country of the customer |
