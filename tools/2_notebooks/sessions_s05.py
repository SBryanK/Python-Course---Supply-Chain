from nbkit import md, code, task, blank, DRIVE_WORK

cells = [
    md("""# Session 5: Who are the star products?

Which products bring most of the money?"""),

    md("## Load your clean table\n\nThe shape must be `(101458, 10)`. If not, stop and fix it first."),
    code(f'''import pandas as pd
from google.colab import drive

drive.mount("/content/drive")
sales_clean = pd.read_csv("{DRIVE_WORK}sales_clean.csv")
sales_clean["invoice_date"] = pd.to_datetime(sales_clean["invoice_date"])   # a CSV forgets dates
print(sales_clean.shape)'''),

    md("## Group and sum"),
    code('''revenue_by_product = sales_clean.groupby("stock_code")["revenue"].sum()
revenue_by_product = revenue_by_product.sort_values(ascending=False)
revenue_by_product.head()'''),
]

cells += task("predict", "How many products are there? One row per stock code. Guess first: more or fewer than 5,000?",
              '''# My guess:
len(revenue_by_product)''')

cells += task("fill", "Revenue per country, biggest first. Expected: `United Kingdom` on top with `1591694.5`",
              '''revenue_by_country = sales_clean.groupby(____)["revenue"].____()
revenue_by_country = revenue_by_country.sort_values(ascending=False)
revenue_by_country.head(5)''',
              '''revenue_by_country = sales_clean.groupby("country")["revenue"].sum()
revenue_by_country = revenue_by_country.sort_values(ascending=False)
revenue_by_country.head(5)''')

cells += task("fix", "Germany's revenue. One name is wrong since the rename in Session 4. Expected: `37365.63`",
              '''german_check = sales_clean.groupby("Country")["revenue"].sum()
round(german_check["Germany"], 2)''',
              '''german_check = sales_clean.groupby("country")["revenue"].sum()
round(german_check["Germany"], 2)''')

cells += [
    md("## A normal table again\n\n`reset_index()` turns the row labels back into a column."),
    code('''product_value = revenue_by_product.reset_index()
product_value.shape'''),

    md("## Running total and share"),
    code('''total_revenue = product_value["revenue"].sum()
print(round(total_revenue, 2))'''),
]

cells += task("fill", "A running total of revenue, in a new column. Expected: the second row is `82285.83`",
              '''product_value["running_total"] = product_value["revenue"].____()
product_value.head(3)''',
              '''product_value["running_total"] = product_value["revenue"].cumsum()
product_value.head(3)''')

cells += [
    md("The running total divided by the total is the **cumulative share**: how far we are."),
    code('''product_value["cumulative_share"] = product_value["revenue"].cumsum() / total_revenue
product_value = product_value.drop(columns="running_total", errors="ignore")
product_value.head(3)'''),

    md("## ABC classes\n\n80 and 95 are a habit from inventory work, not a law."),
    code('''def abc_class(cumulative_share):
    if cumulative_share <= 0.80:
        return "A"
    elif cumulative_share <= 0.95:
        return "B"
    else:
        return "C"

product_value["abc_class"] = product_value["cumulative_share"].apply(abc_class)
print((product_value["abc_class"] == "A").sum())'''),
]

cells += task("predict", "A product sits at a cumulative share of 0.90. Which class? Guess first.",
              '''# My guess:
abc_class(0.90)''')

cells += task("write", "Count the class B products and the class C products. Expected: `794` and `1601`",
              "# Your code here\n",
              '''print((product_value["abc_class"] == "B").sum())
print((product_value["abc_class"] == "C").sum())''')

cells += task("write", "The share of products in class A, in percent with 1 decimal. Expected: `21.9`",
              '''a_products = product_value[product_value["abc_class"] == "A"]
share_of_products = ____
share_of_products''',
              '''a_products = product_value[product_value["abc_class"] == "A"]
share_of_products = round(100 * len(a_products) / len(product_value), 1)
share_of_products''')

cells += task("write", "The share of revenue from class A, in percent with 1 decimal. Then one f-string sentence. "
              "Expected: `21.9% of products bring 80.0% of revenue`",
              '''share_of_revenue = ____
print(f"____")''',
              '''share_of_revenue = round(100 * a_products["revenue"].sum() / total_revenue, 1)
print(f"{share_of_products}% of products bring {share_of_revenue}% of revenue")''')

cells += [
    md("Save the product table. You use it for Power BI in Session 7."),
    code(f'''product_value.to_csv("{DRIVE_WORK}product_value.csv", index=False)
print("Saved product_value.csv")'''),

    md("""## Cold test (20 minutes)

Notes and this notebook are allowed. Your teacher stays silent.

Find the top country by revenue. Then show its revenue for each month, with the `month` column from Session 4.
Then write one sentence: what does it tell a manager?"""),
    blank("# Your cold test code\n",
          '''top_country = revenue_by_country.index[0]
print(top_country)

top_country_sales = sales_clean[sales_clean["country"] == top_country]
revenue_by_month = top_country_sales.groupby("month")["revenue"].sum()
print(revenue_by_month)'''),
    md("*My sentence:*"),

    md("## Extra (homework)"),
]

cells += task("extra", "Revenue for each month, for all countries. Expected: `775572.23`, `593178.39`, `507783.42`",
              '''monthly_revenue = ____
monthly_revenue''',
              '''monthly_revenue = sales_clean.groupby("month")["revenue"].sum()
monthly_revenue''')

cells += task("extra", "The top 10 products' share of revenue, in percent with 2 decimals. Expected: `9.62`",
              '''top10_share = ____
top10_share''',
              '''top10_share = round(100 * product_value["revenue"].head(10).sum() / total_revenue, 2)
top10_share''')

SESSION = {
    "folder": "s05_star_products",
    "cells": cells,
    "expect": ["(101458, 10)", "3066", "1591694.5", "37365.63", "(3066, 2)", "1876534.04", "82285.83", "671", "'B'", "794\n1601", "21.9",
               "21.9% of products bring 80.0% of revenue", "Saved product_value.csv", "United Kingdom", "705166.72",
               "468651.61", "417876.17", "775572.23", "9.62"],
}
