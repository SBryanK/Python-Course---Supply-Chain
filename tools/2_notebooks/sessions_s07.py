from nbkit import md, code, task, DRIVE_WORK

cells = [
    md("""# Session 7: New tools, your own question

What question will you answer in your project? First a taste of SQL and Power BI."""),

    md("## Load your tables\n\nThe shapes must be `(101458, 10)` and `(3066, 4)`."),
    code(f'''import pandas as pd
from google.colab import drive

drive.mount("/content/drive")
sales_clean = pd.read_csv("{DRIVE_WORK}sales_clean.csv")
product_value = pd.read_csv("{DRIVE_WORK}product_value.csv")

print(sales_clean.shape)
print(product_value.shape)'''),

    md("## SQL\n\nSQLite lives inside Python, so there is nothing to install."),
    code('''import sqlite3

columns_for_sql = ["invoice", "stock_code", "description", "quantity", "price", "country", "revenue"]
sql_table = sales_clean[columns_for_sql]

connection = sqlite3.connect(":memory:")
sql_table.to_sql("sales", connection, index=False)'''),
]

cells += task("predict", "Read the query first. What will it return: how many rows, which columns? Then run it.",
              '''# My guess:
query = """
SELECT country, SUM(revenue) AS total_revenue
FROM sales
GROUP BY country
ORDER BY total_revenue DESC
LIMIT 5
"""
pd.read_sql_query(query, connection)''')

cells += [
    md("The same answer in pandas:"),
    code('''revenue_by_country = sales_clean.groupby("country")["revenue"].sum()
revenue_by_country.sort_values(ascending=False).head(5)'''),
]

cells += task("fill", "Total revenue of Germany. In SQL, `WHERE` is the filter and text goes in single quotes. "
              "Expected: `37365.63`",
              '''query = """
SELECT SUM(revenue) AS germany_revenue
FROM sales
____ country = ____
"""
pd.read_sql_query(query, connection)''',
              '''query = """
SELECT SUM(revenue) AS germany_revenue
FROM sales
WHERE country = 'Germany'
"""
pd.read_sql_query(query, connection)''')

cells += task("fill", "The 3 rows with the biggest revenue. Expected: the first row is invoice `540815` with `6539.4`",
              '''query = """
SELECT invoice, description, revenue
FROM sales
ORDER BY revenue ____
LIMIT ____
"""
pd.read_sql_query(query, connection)''',
              '''query = """
SELECT invoice, description, revenue
FROM sales
ORDER BY revenue DESC
LIMIT 3
"""
pd.read_sql_query(query, connection)''')

cells += task("fix", "This query forgot which table to ask. Fix it. Expected: `1876534.04`",
              '''query = """
SELECT ROUND(SUM(revenue), 2) AS total_revenue
"""
pd.read_sql_query(query, connection)''',
              '''query = """
SELECT ROUND(SUM(revenue), 2) AS total_revenue
FROM sales
"""
pd.read_sql_query(query, connection)''')

cells += task("write", "How many different orders did Germany place? Use `COUNT(DISTINCT invoice)`. "
              "Expected: `79`, the same as Session 4",
              '''query = """
____
"""
pd.read_sql_query(query, connection)''',
              '''query = """
SELECT COUNT(DISTINCT invoice) AS german_orders
FROM sales
WHERE country = 'Germany'
"""
pd.read_sql_query(query, connection)''')

cells += task("write", "How many countries are in the data? Use `COUNT(DISTINCT country)`. Then check it with pandas "
              "`nunique()`. Expected: `31` both times",
              '''query = """
____
"""
print(pd.read_sql_query(query, connection))
print(____)''',
              '''query = """
SELECT COUNT(DISTINCT country) AS countries
FROM sales
"""
print(pd.read_sql_query(query, connection))
print(sales_clean["country"].nunique())''')

cells += task("case", "Menu option 2 starts here. The top 5 products of the Netherlands by revenue, in SQL. "
              "Expected: `ROUND SNACK BOXES SET OF4 WOODLAND` on top with `1958.4`",
              '''query = """
SELECT description, SUM(revenue) AS total_revenue
FROM sales
____
"""
pd.read_sql_query(query, connection)

# What would a manager do with this?''',
              '''query = """
SELECT description, SUM(revenue) AS total_revenue
FROM sales
WHERE country = 'Netherlands'
GROUP BY description
ORDER BY total_revenue DESC
LIMIT 5
"""
pd.read_sql_query(query, connection)

# What would a manager do with this? Keep lunch boxes and snack boxes in stock for the Dutch customers.''')

cells += [
    md("""## Power BI (at home)

1. Open Power BI Desktop. **Get data > Text/CSV**, then `product_value.csv` from your work folder.
2. One **bar chart**: product on the axis, revenue as the value.
3. One **card** with the total revenue.
4. Save, and send a screenshot."""),

    md("""## Your project

A good question is **specific**, **answerable with this data**, and **useful** to a manager.

The menu:
1. Is class A revenue steady month to month?
2. Which country outside the UK buys the most, and what are its top 5 products?
3. How big are cancellations, and which products get cancelled most? (`cancellations.csv`)
4. A reorder point for the top 5 products, with a lead time and safety stock that you choose. Label every assumption."""),
    code("print(list(sales_clean.columns))"),

    md("""## My project plan

Copy it into `project_plan.md` too.

- **My question:**
- **Columns I need:**
- **Steps:**
- **The chart I expect:**
- **The decision it helps:**"""),

    md("## Extra (homework)"),
]

cells += task("extra", "Revenue per country for countries with more than 30000 pounds only. In SQL, a filter on a "
              "group uses `HAVING`. Expected: 5 countries",
              '''query = """
SELECT country, SUM(revenue) AS total_revenue
FROM sales
GROUP BY country
____
ORDER BY total_revenue DESC
"""
pd.read_sql_query(query, connection)''',
              '''query = """
SELECT country, SUM(revenue) AS total_revenue
FROM sales
GROUP BY country
HAVING total_revenue > 30000
ORDER BY total_revenue DESC
"""
pd.read_sql_query(query, connection)''')

SESSION = {
    "folder": "s07_new_tools",
    "cells": cells,
    "expect": ["(101458, 10)", "(3066, 4)", "United Kingdom", "58182.55", "37365.63", "540815", "6539.4",
               "1876534.04", "79", "31", "ROUND SNACK BOXES SET OF4 WOODLAND", "1958.4", "France"],
}
