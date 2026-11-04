from nbkit import md, code, exercise, DRIVE_DATA, DRIVE_WORK

cells = [
    md("""# Session 4: Cleaning day

**Question for today:** what does the data look like when it is clean, and how much did we sell?

**Data credit.** Chen, D. (2012). Online Retail II [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5CG6D. Licence: CC BY 4.0.
It is real sales data from a UK online gift shop. This lesson file holds three months: December 2010 to February 2011. Prices are in pounds."""),

    md("""## Warm-up (on paper)

1. We load a table with 105,335 rows and 8 columns. What will `sales.shape` print?
2. How would you keep only the rows from Germany in Excel?"""),

    md("""## Load the file

**pandas** is a tool for tables. A table in pandas is called a **DataFrame**. It is like a sheet in Excel.
`read_csv` opens the file, like File > Open. The path must be exact.

The first time, Google asks for permission to open your Drive. Accept it."""),
    code(f'''import pandas as pd
from google.colab import drive

drive.mount("/content/drive")
sales = pd.read_csv("{DRIVE_DATA}")
sales.head()'''),

    md("""## Look first

Looking first is part of the job. `shape` gives (rows, columns). `info` shows the type of each column.
Each column holds one type of data."""),
    code('''print(sales.shape)
sales.info()'''),

    md("""## Missing values

**NaN** means an empty box on a form. `isna()` marks the empty cells and `sum()` counts them.
The customer IDs look like `17850.0`. A number column with empty cells is stored with decimals, so pandas adds `.0`."""),
    code("sales.isna().sum()"),

    md("""## Short names

Short lowercase names are easier to type. A dictionary (from Session 2) maps the old name to the new name."""),
    code('''new_names = {
    "Invoice": "invoice",
    "StockCode": "stock_code",
    "Description": "description",
    "Quantity": "quantity",
    "InvoiceDate": "invoice_date",
    "Price": "price",
    "Customer ID": "customer_id",
    "Country": "country",
}
sales = sales.rename(columns=new_names)
sales.head(3)'''),

    md("""## The cleaning log

Write the number of rows you have after each step. Double-click this cell to edit it.

| Step | Rows left |
|---|---|
| Start | 105,335 |
| Drop duplicates | |
| Remove cancelled invoices | |
| Quantity above 0 | |
| Price above 0 | |
| Real products only | |
| Remove the giant order | |"""),

    md("""## Clean step by step

A **filter** keeps only the good boxes. In Excel, it is a helper column and then Filter.
The original table does not change unless you **save the result** in a variable.

- A cancelled invoice starts with the letter `C`. We save those rows first, for the project later.
- `~` means **not**. `.str.startswith("C")` checks the first letter of the text.
- With two conditions, use `&` (not `and`) and put each condition in brackets."""),
    code('''is_cancelled = sales["invoice"].str.startswith("C")
cancellations = sales[is_cancelled]          # kept for the project later

sales_clean = sales.drop_duplicates()
print(len(sales_clean))

sales_clean = sales_clean[~sales_clean["invoice"].str.startswith("C")]   # ~ means NOT
print(len(sales_clean))'''),
]

cells += exercise(
    "Add three more steps. After each step, print `len(sales_clean)` and write it in your log. 1) Keep only rows where `quantity` is above 0. 2) Keep only rows where `price` is above 0. 3) Keep only real products: take the first character of `stock_code` with `.str[0]`, then keep the rows where `.str.isdigit()` is true.",
    "`102257`, then `101933`, then `101459`",
    "# TODO 1: keep only rows where quantity is above 0, then print len(sales_clean)\n\n# TODO 2: keep only rows where price is above 0, then print len(sales_clean)\n\n# TODO 3: keep only real products (first character of stock_code is a digit), then print len(sales_clean)\n",
    '''sales_clean = sales_clean[sales_clean["quantity"] > 0]
print(len(sales_clean))

sales_clean = sales_clean[sales_clean["price"] > 0]
print(len(sales_clean))

first_character = sales_clean["stock_code"].str[0]
sales_clean = sales_clean[first_character.str.isdigit()]   # real products start with a digit
print(len(sales_clean))''')

cells += [
    md("""## A safe copy

`.copy()` is like Save As with a new name. Changing the copy cannot hurt the original. We copy once, before we add new columns."""),
    code('''sales_clean = sales_clean.copy()
print(sales_clean.shape)'''),

    md("""## New columns and sorting

A new column is like a formula column in Excel, but it does not update by itself. Run the cell again if the data changes.

- `revenue` is quantity times price.
- `pd.to_datetime` turns the text into a real date. A column must be a real date before you can take a month from it.
- `to_period("M")` makes a month from a date. The `M` means month, and it keeps the year.

Then sort the biggest revenue first, like Sort Z to A."""),
    code('''sales_clean["revenue"] = sales_clean["quantity"] * sales_clean["price"]
sales_clean["invoice_date"] = pd.to_datetime(sales_clean["invoice_date"])
sales_clean["month"] = sales_clean["invoice_date"].dt.to_period("M")   # M = month, keeps the year
sales_clean.head()'''),
    code('sales_clean.sort_values("revenue", ascending=False).head(10)'),

    md("""## The detective moment

The biggest row is invoice 541431: 74,215 jars, worth 77,183.60 pounds. That looks strange.
Let us look at the raw table for this invoice and for the one that starts with `C`."""),
    code('''giant_rows = sales[(sales["invoice"] == "541431") | (sales["invoice"] == "C541433")]
giant_rows'''),
]

cells += exercise(
    "The `C` invoice cancels the same 74,215 jars 16 minutes later. So the sale never happened. Remove invoice 541431 from `sales_clean` and print the shape.",
    "`(101458, 10)`",
    "# TODO: remove invoice 541431 from sales_clean, write a comment about why, then print the shape\n",
    '''sales_clean = sales_clean[sales_clean["invoice"] != "541431"]   # it was cancelled 16 minutes later
print(sales_clean.shape)''')

cells += [
    code(f'''sales_clean.to_csv("{DRIVE_WORK}sales_clean.csv", index=False)
cancellations.to_csv("{DRIVE_WORK}cancellations.csv", index=False)
print("Saved two files in your work folder")'''),
]

cells += exercise(
    "Keep only the rows from Germany in `sales_clean`. Save them in `germany_sales` and print the shape.",
    "`(1514, 10)`",
    '# TODO: keep only rows where country is "Germany", save in germany_sales, then print its shape\n',
    'germany_sales = sales_clean[sales_clean["country"] == "Germany"]\nprint(germany_sales.shape)')

cells += [
    md("""## Why does this happen? (optional)

A filter gives you a **new table**. The old one stays the same, like a photocopy of the sheet with some rows covered. If you do not save the result in a variable, it is lost.
**For an analyst:** this protects your raw data. You can always go back, and you can show exactly what you removed."""),

    md("""## Recap

You can now:
1. Load a file and look at it first.
2. Clean it step by step and keep a log.
3. Add columns and sort.

**Decision to think about.** Rows with no customer ID are kept here. For product questions that is fine. For customer questions you must drop them. Why?

**Homework.** Run the notebook again from the top. Write the cleaning log in your own words. Try `sales_clean.describe()` and look at the numbers. Bring one question about the giant order."""),
]

SESSION = {
    "folder": "s04_cleaning_day",
    "cells": cells,
    "expect": ["(105335, 8)", "104360", "102471", "102257", "101933", "101459", "(101459, 8)", "(101458, 10)", "(1514, 10)", "77183.6", "Saved two files"],
}
