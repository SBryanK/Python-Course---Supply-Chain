from nbkit import md, code, task, DRIVE_DATA, DRIVE_WORK

cells = [
    md("""# Session 4: Cleaning day

What does clean data look like, and how much did we really sell?

*Data: Chen, D. (2012). Online Retail II. UCI Machine Learning Repository. https://doi.org/10.24432/C5CG6D. CC BY 4.0.*"""),

    md("## Load"),
    code(f'''import pandas as pd
from google.colab import drive

drive.mount("/content/drive")
sales = pd.read_csv("{DRIVE_DATA}")
sales.head()'''),

    md("## Look first"),
]

cells += task("predict", "What will `sales.shape` print? Guess first.", "# My guess:\nsales.shape")

cells += [
    code("sales.info()"),
    code("sales.isna().sum()"),
]

cells += task("write", "Percent of rows with no customer ID, rounded to 1 decimal. Expected: `34.4`",
              '''missing_pct = ____
missing_pct''',
              '''empty_ids = sales["Customer ID"].isna().sum()
missing_pct = round(100 * empty_ids / len(sales), 1)
missing_pct''')

cells += [
    md("## Short names"),
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
]

cells += task("fill", "Rows per country, biggest first.",
              'sales["country"].____().head(5)',
              'sales["country"].value_counts().head(5)')

cells += [
    md("""## The cleaning log

| Step | Rows left | Why |
|---|---|---|
| Start | 105,335 | |
| Drop duplicates | | |
| Remove cancelled invoices | | |
| Quantity above 0 | | |
| Price above 0 | | |
| Real products only | | |
| Remove the giant order | | |"""),

    md("## Clean step by step"),
    code('''is_cancelled = sales["invoice"].str.startswith("C")
cancellations = sales[is_cancelled]          # kept for the project later

sales_clean = sales.drop_duplicates()
print(len(sales_clean))

sales_clean = sales_clean[~sales_clean["invoice"].str.startswith("C")]
print(len(sales_clean))'''),
]

cells += task("predict", "How many rows have a quantity of 0 or less now? More or fewer than 1,000?",
              '''# My guess:
len(sales_clean[sales_clean["quantity"] <= 0])''')

cells += task("fill", "Quantity above 0, then price above 0. Expected: `102257`, `101933`",
              '''sales_clean = sales_clean[sales_clean["quantity"] ____ 0]
print(len(sales_clean))

sales_clean = sales_clean[sales_clean["price"] ____ 0]
print(len(sales_clean))''',
              '''sales_clean = sales_clean[sales_clean["quantity"] > 0]
print(len(sales_clean))

sales_clean = sales_clean[sales_clean["price"] > 0]
print(len(sales_clean))''')

cells += task("write", "Real products only: the stock code starts with a digit. Expected: `101459`",
              '''sales_clean = ____
print(len(sales_clean))''',
              '''first_character = sales_clean["stock_code"].str[0]
sales_clean = sales_clean[first_character.str.isdigit()]
print(len(sales_clean))''')

cells += task("fix", "German rows with quantity above 100. Expected: `6`",
              '''big_german = sales_clean[sales_clean["country"] == "Germany" and sales_clean["quantity"] > 100]
len(big_german)''',
              '''big_german = sales_clean[(sales_clean["country"] == "Germany") & (sales_clean["quantity"] > 100)]
len(big_german)''')

cells += [
    md("## New columns"),
    code('''sales_clean = sales_clean.copy()
sales_clean["revenue"] = sales_clean["quantity"] * sales_clean["price"]
sales_clean["invoice_date"] = pd.to_datetime(sales_clean["invoice_date"])
sales_clean["month"] = sales_clean["invoice_date"].dt.to_period("M")
sales_clean.head()'''),
    code('sales_clean.sort_values("revenue", ascending=False).head(10)'),

    md("## The giant order"),
    code('''giant_rows = sales[sales["invoice"].isin(["541431", "C541433"])]
giant_rows'''),
]

cells += task("write", "Remove invoice 541431, with a comment that says why. Expected: `(101458, 10)`",
              '''sales_clean = ____
sales_clean.shape''',
              '''sales_clean = sales_clean[sales_clean["invoice"] != "541431"]   # cancelled 16 minutes later
sales_clean.shape''')

cells += task("write", "Total revenue, rounded to 2 decimals. Expected: `1876534.04`",
              '''total_revenue = ____
total_revenue''',
              '''total_revenue = round(sales_clean["revenue"].sum(), 2)
total_revenue''')

cells += [
    md("## Save"),
    code(f'''sales_clean.to_csv("{DRIVE_WORK}sales_clean.csv", index=False)
cancellations.to_csv("{DRIVE_WORK}cancellations.csv", index=False)
print("Saved two files in your work folder")'''),
]

cells += task("write", "Only the rows from Germany, saved as `germany_sales`. Expected: `(1514, 10)`",
              '''germany_sales = ____
germany_sales.shape''',
              '''germany_sales = sales_clean[sales_clean["country"] == "Germany"]
germany_sales.shape''')

cells += task("case", "The German warehouse asks: how many orders, and the average revenue per order? "
              "Expected: `79` orders, `472.98` per order",
              '''german_orders = ____
revenue_per_order = ____
print(german_orders, revenue_per_order)

# My sentence for the warehouse:''',
              '''german_orders = germany_sales["invoice"].nunique()
revenue_per_order = round(germany_sales["revenue"].sum() / german_orders, 2)
print(german_orders, revenue_per_order)

# My sentence for the warehouse: Germany placed 79 orders, worth about 473 pounds each.''')

cells += [md("## Extra (homework)")]

cells += task("extra", "Median price, from `describe()`. Expected: `2.46`",
              '''print(sales_clean["price"].describe())

median_price = ____
median_price''',
              '''print(sales_clean["price"].describe())

median_price = sales_clean["price"].median()
median_price''')

cells += task("extra", "Rows with `HEART` in the description. Expected: `10816`",
              '''heart_rows = ____
heart_rows''',
              '''heart_rows = sales_clean["description"].str.contains("HEART").sum()
heart_rows''')

SESSION = {
    "folder": "s04_cleaning_day",
    "cells": cells,
    "expect": ["(105335, 8)", "34.4", "104360", "102471", "102257", "101933", "101459", "(101458, 10)",
               "1876534.04", "Saved two files", "(1514, 10)", "79 472.98", "2.46", "10816"],
}
