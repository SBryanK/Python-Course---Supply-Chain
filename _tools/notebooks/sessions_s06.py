from nbkit import md, code, exercise, DRIVE_WORK

cells = [
    md("""# Session 6: Make the numbers talk

**Question for today:** how do we show the finding so a manager understands it in five seconds?"""),

    md("""## Warm-up (on paper)

Sketch the chart you would show a manager to answer "which products matter?". Label the two axes."""),

    md("""## Load your tables

Two files from your work folder: the clean table (Session 4) and the product table (Session 5). Check both shapes.
The first must be `(101458, 10)`. The second must be `(3066, 4)`."""),
    code(f'''import pandas as pd
from google.colab import drive

drive.mount("/content/drive")
sales_clean = pd.read_csv("{DRIVE_WORK}sales_clean.csv")
sales_clean["invoice_date"] = pd.to_datetime(sales_clean["invoice_date"])   # a CSV forgets dates
product_value = pd.read_csv("{DRIVE_WORK}product_value.csv")

print(sales_clean.shape)
print(product_value.shape)'''),

    md("""## Merge: your VLOOKUP

`merge` matches two tables on a key, like VLOOKUP or XLOOKUP. We want to add the product name to the product table.
**Always count the rows before and after.** If a key repeats, one row matches several rows and the table grows.

First try: a names table with every pair of code and description."""),
    code('''names_both = sales_clean[["stock_code", "description"]].drop_duplicates()

print(len(product_value))
merged_first = product_value.merge(names_both, on="stock_code", how="left")
print(len(merged_first))'''),

    md("""The table grew. Some codes have more than one description. `duplicated` marks a row `True` when its code already appeared above it.
Let us find the extra rows."""),
    code('''extra_rows = merged_first[merged_first["stock_code"].duplicated()]
print(len(extra_rows))
extra_rows.head()'''),

    md("""The fix: keep **one** name for each code. `drop_duplicates(subset="stock_code")` keeps the first row for each code. Then merge again and check the count."""),
    code('''product_names = sales_clean[["stock_code", "description"]].drop_duplicates(subset="stock_code")

print(len(product_value))
product_value = product_value.merge(product_names, on="stock_code", how="left")
print(len(product_value))   # must be the same number as the line above'''),

    *exercise("Show the top 3 rows of `product_value`, now with the product names.",
              "REGENCY CAKESTAND 3 TIER, WHITE HANGING HEART T-LIGHT HOLDER, CHILLI LIGHTS",
              "# TODO: show the top 3 rows of product_value\n",
              "product_value.head(3)"),

    md("""## Chart 1: a bar chart

matplotlib draws a chart step by step, like Insert Chart and then editing each part. **Every chart needs a title and axis labels.**
`barh` draws horizontal bars. We sort so the biggest bar is on top."""),
    code('''import matplotlib.pyplot as plt

top10 = product_value.head(10)
top10 = top10.sort_values("revenue")

plt.figure(figsize=(10, 5))
plt.barh(top10["description"], top10["revenue"])
plt.title("The top 10 products are only 9.6% of revenue")
plt.xlabel("Revenue (pounds)")
plt.tight_layout()
plt.show()'''),

    md("""**The title says the finding, not the chart type.** "Bar chart of revenue" tells nothing. "The top 10 products are only 9.6% of revenue" tells the manager what to see."""),

    *exercise("This chart has no title and no labels. Add a title that says the finding, and both axis labels.",
              "A bar chart with a title like `The top 5 products bring about 3% of revenue`, a label on each axis",
              '''top5 = product_value.head(5)
top5 = top5.sort_values("revenue")

plt.figure(figsize=(10, 4))
plt.barh(top5["description"], top5["revenue"])
plt.tight_layout()
plt.show()
# TODO: add plt.title, plt.xlabel and plt.ylabel before plt.show()
''',
              '''top5 = product_value.head(5)
top5 = top5.sort_values("revenue")

plt.figure(figsize=(10, 4))
plt.barh(top5["description"], top5["revenue"])
plt.title("The top 5 products bring about 3% of revenue")
plt.xlabel("Revenue (pounds)")
plt.ylabel("Product")
plt.tight_layout()
plt.show()'''),

    md("""## Chart 2: a line chart

Revenue for each day. `.dt.date` takes the day from a date (like `.dt.to_period` took the month). The line chart shows change over time."""),
    code('''sales_clean["invoice_day"] = sales_clean["invoice_date"].dt.date
daily_revenue = sales_clean.groupby("invoice_day")["revenue"].sum()

plt.figure(figsize=(10, 4))
plt.plot(daily_revenue.index, daily_revenue.values)
plt.title("Revenue peaked in the first week of December")
plt.xlabel("Day")
plt.ylabel("Revenue (pounds)")
plt.tight_layout()
plt.show()'''),

    md("""## Chart 3: the 80% curve

The cumulative share from Session 5, drawn against the rank of each product. The dashed line marks 80%. This is a copy-along: type it, run it, and read the picture."""),
    code('''product_value["product_rank"] = range(1, len(product_value) + 1)

plt.figure(figsize=(8, 4))
plt.plot(product_value["product_rank"], product_value["cumulative_share"])
plt.axhline(0.80, linestyle="--")
plt.title("About 1 in 5 products bring 80% of revenue")
plt.xlabel("Products, ranked from biggest to smallest")
plt.ylabel("Share of total revenue")
plt.tight_layout()
plt.show()'''),

    md("""## Seaborn (homework)

seaborn is a chart template on top of matplotlib. The titles and labels work the same way.
The UK is about 85% of revenue, so we leave it out. The title says so."""),
    code('''import seaborn as sns

revenue_by_country = sales_clean.groupby("country")["revenue"].sum()
revenue_by_country = revenue_by_country.reset_index()

outside_uk = revenue_by_country[revenue_by_country["country"] != "United Kingdom"]
top_countries = outside_uk.sort_values("revenue", ascending=False).head(5)

sns.barplot(data=top_countries, x="revenue", y="country")
plt.title("Outside the UK, the Netherlands and Ireland lead")
plt.xlabel("Revenue (pounds)")
plt.ylabel("Country")
plt.tight_layout()
plt.show()'''),

    md("""## Case hunt

Find one real supply chain case: from the news, a company report or a course case. Answer five points on one page:
1. The problem
2. Who is affected
3. What data would show it
4. One question you could answer with data
5. Which tool fits: Python, SQL or a dashboard

Use the template in your course home folder. Bring it to Session 8."""),

    md("""## Why does this happen? (optional)

A merge can make a table longer when the key repeats on the right side. Each left row is matched with every right row that has the same key. That is why we count rows before and after.
**For an analyst:** a changed row count after a merge is a warning. It can double your revenue without any error message."""),

    md("""## Recap

You can now:
1. Merge two tables and check the row count.
2. Draw a bar chart and a line chart with a title and labels.
3. Write a title that states the finding.

**Homework.** Finish the top 10 chart. Do the seaborn chart. Start your case hunt. Install **Power BI Desktop** on your Windows laptop before Session 7."""),
]

SESSION = {
    "folder": "s06_numbers_talk",
    "cells": cells,
    "expect": ["(101458, 10)", "(3066, 4)", "3107", "41", "REGENCY CAKESTAND 3 TIER"],
}
