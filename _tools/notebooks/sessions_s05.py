from nbkit import md, code, exercise, blank, DRIVE_WORK

cells = [
    md("""# Session 5: Who are the star products?

**Question for today:** which products bring most of the money?"""),

    md("""## Warm-up (on paper)

Write the steps you would click in an Excel PivotTable to get the total revenue for each product."""),

    md("""## Load your clean table

This is the file you saved in Session 4. A CSV file forgets that a column was a date, so we convert `invoice_date` again.
Then we check the shape. It must be `(101458, 10)`. If not, stop and fix it first."""),
    code(f'''import pandas as pd
from google.colab import drive

drive.mount("/content/drive")
sales_clean = pd.read_csv("{DRIVE_WORK}sales_clean.csv")
sales_clean["invoice_date"] = pd.to_datetime(sales_clean["invoice_date"])   # a CSV forgets dates
print(sales_clean.shape)'''),

    md("""## Group and sum

`groupby` sorts the receipts into piles, then adds each pile. It is a PivotTable in code.
The result has a row label column (the *index*). `reset_index()` turns it back into a normal table."""),
    code('''revenue_by_product = sales_clean.groupby("stock_code")["revenue"].sum()
revenue_by_product = revenue_by_product.sort_values(ascending=False)

product_value = revenue_by_product.reset_index()
product_value.head()'''),

    *exercise("Show the top 3 products with `head`. You can use the code above.",
              "stock codes `22423`, `85123A` and `79321`, with revenue `51504.85`, `30780.98` and `17013.92`",
              "# TODO: show the top 3 rows of product_value\n",
              "product_value.head(3)"),

    md("""## Running total

`cumsum` is a running total, like `=SUM($B$2:B2)` dragged down. **Sort first,** or the running total means nothing.
Dividing by the total gives the **cumulative share**: how much of all revenue we have reached so far."""),
    code('''total_revenue = product_value["revenue"].sum()

product_value["cumulative_share"] = product_value["revenue"].cumsum() / total_revenue
product_value.head()'''),

    md("""## ABC classes

Few items bring most of the money. **ABC analysis** sorts products into three classes:
- **A:** the first 80% of revenue
- **B:** the next 15%
- **C:** the rest

80 and 95 are a habit from inventory work, not a law. We write the rule as a function (Session 3) and use `.apply` to run it on every row, like dragging your formula down."""),
    code('''def abc_class(cumulative_share):
    if cumulative_share <= 0.80:
        return "A"
    elif cumulative_share <= 0.95:
        return "B"
    else:
        return "C"

product_value["abc_class"] = product_value["cumulative_share"].apply(abc_class)

print((product_value["abc_class"] == "A").sum())'''),

    *exercise("Count the class B products and the class C products with the same idea as above.",
              "`794` and `1601`",
              "# TODO: print how many products are class B, then class C\n",
              'print((product_value["abc_class"] == "B").sum())\nprint((product_value["abc_class"] == "C").sum())'),

    md("""## The finding

How big is class A in products, and how much revenue does it bring?"""),
    code('''a_products = product_value[product_value["abc_class"] == "A"]

share_of_products = round(100 * len(a_products) / len(product_value), 1)
share_of_revenue = round(100 * a_products["revenue"].sum() / total_revenue, 1)

print(f"{share_of_products}% of products bring {share_of_revenue}% of revenue")'''),

    md("""## Revenue by country

The same `groupby` idea, with a different pile."""),
    code('''revenue_by_country = sales_clean.groupby("country")["revenue"].sum()
revenue_by_country = revenue_by_country.sort_values(ascending=False)
revenue_by_country.head(5)'''),

    md("""Save the product table. You will use it for Power BI in Session 7."""),
    code(f'''product_value.to_csv("{DRIVE_WORK}product_value.csv", index=False)
print("Saved product_value.csv")'''),

    md("""## Cold test

You may use your notes and this notebook. Your teacher stays silent for 20 minutes.

**Question:** find the top country by revenue. Then show its revenue for each month. Use the `month` column you made in Session 4.

When it works, write one sentence in the text cell below: what does the result tell a manager?"""),
    blank("# TODO: your cold test code\n",
          '''top_country = revenue_by_country.index[0]
print(top_country)

top_country_sales = sales_clean[sales_clean["country"] == top_country]
revenue_by_month = top_country_sales.groupby("month")["revenue"].sum()
print(revenue_by_month)'''),
    md("*My sentence:*"),

    md("""## Why does this happen? (optional)

Inventory people noticed long ago that a small share of items takes most of the sales. The 80/95 cut points are a habit, not a law. Your own data decides how steep the curve is.
**For an analyst:** the class A list tells you where to look first, where to keep stock safe, and which items to check most often."""),

    md("""## Recap

You can now:
1. Group and sum, like a PivotTable.
2. Make a running total and share.
3. Sort products into A, B and C with your own function.

**Homework.** Finish any parts we skipped. Write your own sentence for the finding, using your own words."""),
]

SESSION = {
    "folder": "s05_star_products",
    "cells": cells,
    "expect": ["(101458, 10)", "22423", "51504.85", "671", "794", "1601", "21.9% of products bring 80.0% of revenue",
               "United Kingdom", "705166.72", "468651.61", "417876.17", "Saved product_value.csv"],
}
