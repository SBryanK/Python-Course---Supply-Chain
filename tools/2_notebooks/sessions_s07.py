from nbkit import md, code, exercise, DRIVE_WORK

cells = [
    md("""# Session 7: New tools, your own question

**Question for today:** what question will you answer in your project?

Today has three short parts: a taste of SQL, a look at Power BI, and then your project question."""),

    md("""## Warm-up (in writing)

Write one question that a manager might ask about this sales data.

*My question:*"""),

    md("""## Load your tables

The same two files as Session 6. Check the shapes: `(101458, 10)` and `(3066, 4)`."""),
    code(f'''import pandas as pd
from google.colab import drive

drive.mount("/content/drive")
sales_clean = pd.read_csv("{DRIVE_WORK}sales_clean.csv")
product_value = pd.read_csv("{DRIVE_WORK}product_value.csv")

print(sales_clean.shape)
print(product_value.shape)'''),

    md("""## SQL: the same question in another language

**SQL** is the language for asking a database a question. Many companies keep their data in a database, so analysts often meet SQL.
We use SQLite, which lives inside Python, so there is nothing to install. MySQL is another SQL database. It runs on a server, but basic queries look almost the same.

First we put a table into SQLite. We keep the columns we need."""),
    code('''import sqlite3

columns_for_sql = ["invoice", "stock_code", "description", "quantity", "price", "country", "revenue"]
sql_table = sales_clean[columns_for_sql]

connection = sqlite3.connect(":memory:")
sql_table.to_sql("sales", connection, index=False)'''),

    md("""## Query 1: revenue by country

`SELECT` chooses columns. `FROM` names the table. `GROUP BY` is `groupby`. `ORDER BY ... DESC` sorts the biggest first. `LIMIT 5` keeps five rows."""),
    code('''query = """
SELECT country, SUM(revenue) AS total_revenue
FROM sales
GROUP BY country
ORDER BY total_revenue DESC
LIMIT 5
"""
pd.read_sql_query(query, connection)'''),

    md("""The same answer in pandas, which you already know:"""),
    code('''revenue_by_country = sales_clean.groupby("country")["revenue"].sum()
revenue_by_country.sort_values(ascending=False).head(5)'''),

    *exercise("Write a query for the total revenue of Germany. In SQL, `WHERE` is the filter, and text goes in single quotes.",
              "`37365.63`",
              '''query = """
-- TODO: SELECT the sum of revenue FROM sales WHERE country is 'Germany'
"""
# TODO: run it with pd.read_sql_query(query, connection)
''',
              '''query = """
SELECT SUM(revenue) AS germany_revenue
FROM sales
WHERE country = 'Germany'
"""
pd.read_sql_query(query, connection)'''),

    *exercise("Homework. Write a query for the 10 rows with the biggest revenue: show `invoice`, `description` and `revenue`.",
              "The first row has revenue `6539.4`",
              '''query = """
-- TODO: SELECT invoice, description, revenue FROM sales, biggest revenue first, 10 rows
"""
# TODO: run it with pd.read_sql_query(query, connection)
''',
              '''query = """
SELECT invoice, description, revenue
FROM sales
ORDER BY revenue DESC
LIMIT 10
"""
pd.read_sql_query(query, connection)'''),

    md("""You can practise more, free and in the browser, at sql-practice.com."""),

    md("""## Power BI: a look

Power BI is a tool for dashboards. Your teacher shows it today. You build it at home.

1. Open Power BI Desktop. Choose **Get data**, then **Text/CSV**, and pick `product_value.csv` from your work folder.
2. Make one **bar chart**: product on the axis, revenue as the value.
3. Make one **card** with the total revenue.
4. Save the file and send a screenshot to your teacher.

The self-study page `intro_powerbi.md` has the same steps."""),

    md("""## What makes a good question?

A good analyst question is:
- **Specific:** one thing, not "what drives sales?"
- **Answerable with this data:** we have products, countries, dates, quantities and prices. We do not have profit, stock levels or lead times.
- **Useful to a manager:** someone can decide something from the answer.

If a question needs a skill we did not teach, change the question, not the skill."""),

    md("""## The project menu

Choose one, or write your own:
1. Is class A revenue steady month to month?
2. Which country outside the UK buys the most, and what are its top 5 products?
3. How big are cancellations, and which products get cancelled most? (Use `cancellations.csv`.)
4. A reorder point for the top 5 products, using a lead time and a safety stock that **you choose**. Label every assumption as an assumption."""),

    md("""What columns does the data have? Check before you choose."""),
    code("print(list(sales_clean.columns))"),

    md("""## My project plan

Fill this in, and copy it into `project_plan.md`.

- **My question:**
- **Columns I need:**
- **Steps:**
- **The chart I expect:**
- **The decision it helps:**"""),

    md("""## Why does this happen? (optional)

SQL and pandas are two languages for the same job: filter, group and sort a table. SQL runs where the data lives. pandas runs on your laptop or in Colab.
**For an analyst:** learn the idea once. `GROUP BY` and `groupby` are the same idea, and so are `WHERE` and a filter."""),

    md("""## Recap

You can now:
1. Read and write a basic SQL query and compare it with pandas.
2. Say what Power BI is for.
3. Write a good analyst question and a project plan.

**Homework.** Build the Power BI chart at home and send a screenshot. Finish your project plan. Start the first analysis."""),
]

SESSION = {
    "folder": "s07_new_tools",
    "cells": cells,
    "expect": ["(101458, 10)", "(3066, 4)", "United Kingdom", "58182.55", "37365.63", "6539.4"],
}
