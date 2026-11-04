from nbkit import md, code, task, DRIVE_WORK

cells = [
    md("""# Session 6: Make the numbers talk

How do we show the finding so a manager gets it in five seconds?"""),

    md("## Load your tables\n\nThe shapes must be `(101458, 10)` and `(3066, 4)`."),
    code(f'''import pandas as pd
import matplotlib.pyplot as plt
from google.colab import drive

drive.mount("/content/drive")
sales_clean = pd.read_csv("{DRIVE_WORK}sales_clean.csv")
sales_clean["invoice_date"] = pd.to_datetime(sales_clean["invoice_date"])   # a CSV forgets dates
product_value = pd.read_csv("{DRIVE_WORK}product_value.csv")

print(sales_clean.shape)
print(product_value.shape)'''),

    md("## Merge: your VLOOKUP\n\nFirst try: a names table with every pair of code and description."),
    code('''names_both = sales_clean[["stock_code", "description"]].drop_duplicates()
print(len(product_value))'''),
]

cells += task("predict", "After this merge, will the table have more, fewer or the same 3,066 rows? Guess first.",
              '''# My guess:
merged_first = product_value.merge(names_both, on="stock_code", how="left")
print(len(merged_first))''')

cells += [
    code('''extra_rows = merged_first[merged_first["stock_code"].duplicated()]
print(len(extra_rows))
extra_rows.head()'''),

    md("The fix: keep one name for each code, then count again."),
    code('''product_names = sales_clean[["stock_code", "description"]].drop_duplicates(subset="stock_code")

product_value = product_value.merge(product_names, on="stock_code", how="left")
print(len(product_value))   # must be 3066 again'''),
]

cells += task("fill", "Show the top 3 products with their names. Expected: REGENCY CAKESTAND 3 TIER on top",
              'product_value[["description", ____]].____(3)',
              'product_value[["description", "revenue"]].head(3)')

cells += [
    md("## A bar chart\n\nThe title says the finding, not the chart type."),
    code('''top10 = product_value.head(10).sort_values("revenue")

plt.figure(figsize=(10, 5))
plt.barh(top10["description"], top10["revenue"])
plt.title("The top 10 products are only 9.6% of revenue")
plt.xlabel("Revenue (pounds)")
plt.tight_layout()
plt.show()'''),
]

cells += task("fix", "This chart has no title and no labels. Add a title that says the finding, and both axis labels.",
              '''top5 = product_value.head(5).sort_values("revenue")

plt.figure(figsize=(10, 4))
plt.barh(top5["description"], top5["revenue"])
plt.tight_layout()
plt.show()''',
              '''top5 = product_value.head(5).sort_values("revenue")

plt.figure(figsize=(10, 4))
plt.barh(top5["description"], top5["revenue"])
plt.title("Five products bring about 7% of revenue")
plt.xlabel("Revenue (pounds)")
plt.ylabel("Product")
plt.tight_layout()
plt.show()''')

cells += task("fix", "One column name is wrong. Fix it so the chart draws.",
              '''plt.figure(figsize=(10, 4))
plt.barh(top5["Description"], top5["revenue"])
plt.title("REGENCY CAKESTAND 3 TIER leads by far")
plt.xlabel("Revenue (pounds)")
plt.tight_layout()
plt.show()''',
              '''plt.figure(figsize=(10, 4))
plt.barh(top5["description"], top5["revenue"])
plt.title("REGENCY CAKESTAND 3 TIER leads by far")
plt.xlabel("Revenue (pounds)")
plt.tight_layout()
plt.show()''')

cells += [
    md("## A line chart\n\n`.dt.date` takes the day from a date, like `.dt.to_period` took the month."),
    code('''sales_clean["invoice_day"] = sales_clean["invoice_date"].dt.date
daily_revenue = sales_clean.groupby("invoice_day")["revenue"].sum()
print(len(daily_revenue))'''),
]

cells += task("fill", "Draw the daily line chart with a finding title and two axis labels.",
              '''plt.figure(figsize=(10, 4))
plt.____(daily_revenue.index, daily_revenue.values)
plt.title(____)
plt.xlabel("Day")
plt.ylabel("Revenue (pounds)")
plt.tight_layout()
plt.show()''',
              '''plt.figure(figsize=(10, 4))
plt.plot(daily_revenue.index, daily_revenue.values)
plt.title("Revenue peaked in the first week of December")
plt.xlabel("Day")
plt.ylabel("Revenue (pounds)")
plt.tight_layout()
plt.show()''')

cells += task("predict", "Which day had the most revenue? Guess from the chart first.",
              '''# My guess:
print(daily_revenue.idxmax())''')

cells += task("write", "The revenue on the best day, rounded to 2 decimals. Expected: `81454.99`",
              '''best_day_revenue = ____
best_day_revenue''',
              '''best_day_revenue = round(daily_revenue.max(), 2)
best_day_revenue''')

cells += task("write", "A bar chart of revenue per month, with a finding title and axis labels. "
              "Expected: three bars, December the tallest",
              '''monthly_revenue = sales_clean.groupby("month")["revenue"].sum()

# Your chart here''',
              '''monthly_revenue = sales_clean.groupby("month")["revenue"].sum()

plt.figure(figsize=(8, 4))
plt.bar(monthly_revenue.index, monthly_revenue.values)
plt.title("December brought the most revenue")
plt.xlabel("Month")
plt.ylabel("Revenue (pounds)")
plt.tight_layout()
plt.show()''')

cells += task("case", "A sales manager wants to visit one country outside the UK. Show the top 5 countries outside "
              "the UK in a bar chart with a finding title, and print the top one. Expected: `Netherlands 58182.55`",
              '''revenue_by_country = sales_clean.groupby("country")["revenue"].sum()
outside_uk = ____
top_countries = ____

# Your chart here

# My sentence for the manager:''',
              '''revenue_by_country = sales_clean.groupby("country")["revenue"].sum()
outside_uk = revenue_by_country[revenue_by_country.index != "United Kingdom"]
top_countries = outside_uk.sort_values(ascending=False).head(5)
print(top_countries.index[0], round(top_countries.iloc[0], 2))

top_sorted = top_countries.sort_values()
plt.figure(figsize=(8, 4))
plt.barh(top_sorted.index, top_sorted.values)
plt.title("Outside the UK, the Netherlands and Ireland lead")
plt.xlabel("Revenue (pounds)")
plt.ylabel("Country")
plt.tight_layout()
plt.show()

# My sentence for the manager: visit the Netherlands first; it buys the most outside the UK.''')

cells += [
    md("""## Case hunt (due Session 8)

Find one real supply chain case. Answer five points on one page with the template in your course home:
the problem, who is affected, what data would show it, one question for data, and which tool fits."""),

    md("## Extra (homework)"),
]

cells += task("extra", "The same top 5 countries with seaborn. Use `sns.barplot` with `x` and `y`.",
              '''import seaborn as sns

top_table = top_countries.reset_index()

# Your seaborn chart here''',
              '''import seaborn as sns

top_table = top_countries.reset_index()
sns.barplot(data=top_table, x="revenue", y="country")
plt.title("Outside the UK, the Netherlands and Ireland lead")
plt.xlabel("Revenue (pounds)")
plt.ylabel("Country")
plt.tight_layout()
plt.show()''')

cells += task("extra", "The 80% curve: plot `cumulative_share` against the product rank, with a dashed line at 0.80 "
              "(`plt.axhline(0.80, linestyle=\"--\")`).",
              '''product_value["product_rank"] = range(1, len(product_value) + 1)

# Your chart here''',
              '''product_value["product_rank"] = range(1, len(product_value) + 1)

plt.figure(figsize=(8, 4))
plt.plot(product_value["product_rank"], product_value["cumulative_share"])
plt.axhline(0.80, linestyle="--")
plt.title("About 1 in 5 products bring 80% of revenue")
plt.xlabel("Products, ranked from biggest to smallest")
plt.ylabel("Share of total revenue")
plt.tight_layout()
plt.show()''')

SESSION = {
    "folder": "s06_numbers_talk",
    "cells": cells,
    "expect": ["(101458, 10)", "(3066, 4)", "3107", "41", "3066", "REGENCY CAKESTAND 3 TIER", "68", "2010-12-07",
               "81454.99", "Netherlands 58182.55"],
}
