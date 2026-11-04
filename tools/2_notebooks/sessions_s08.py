from nbkit import md, code, task, blank, DRIVE_WORK

cells = [
    md("""# Session 8: Detective work

Your own question today. A short warm-up first, then your project. You type everything."""),

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

    md("## Detective warm-up"),
]

cells += task("predict", "Fewer or more than 5,000 rows for the Netherlands? Guess first.",
              '''# My guess:
netherlands_sales = sales_clean[sales_clean["country"] == "Netherlands"]
print(netherlands_sales.shape)''')

cells += task("fill", "The Netherlands' revenue with a filter and a sum. Expected: `58182.55`",
              '''round(netherlands_sales[____].____(), 2)''',
              '''round(netherlands_sales["revenue"].sum(), 2)''')

cells += task("fix", "Keep the class A products. One sign is wrong. Expected: `(671, 4)`",
              '''class_a = product_value[product_value["abc_class"] = "A"]
class_a.shape''',
              '''class_a = product_value[product_value["abc_class"] == "A"]
class_a.shape''')

cells += task("write", "Check the same Netherlands number a second way, with `groupby`. Expected: `58182.55` again",
              '''revenue_by_country = ____
round(revenue_by_country["Netherlands"], 2)''',
              '''revenue_by_country = sales_clean.groupby("country")["revenue"].sum()
round(revenue_by_country["Netherlands"], 2)''')

cells += task("write", "Class A revenue for each month. Join the class onto the sales rows with `merge`, and count "
              "the rows before and after. Expected: the row count stays `101458`",
              '''classes = product_value[["stock_code", "abc_class"]]
print(len(sales_clean))
sales_with_class = ____
print(len(sales_with_class))''',
              '''classes = product_value[["stock_code", "abc_class"]]
print(len(sales_clean))
sales_with_class = sales_clean.merge(classes, on="stock_code", how="left")
print(len(sales_with_class))

class_a_sales = sales_with_class[sales_with_class["abc_class"] == "A"]
print(class_a_sales.groupby("month")["revenue"].sum())''')

cells += [
    md("""## Project checklist

- [ ] My question is one sentence.
- [ ] I know which columns I need.
- [ ] I print the shape after each filter.
- [ ] I check one number a second way.
- [ ] My chart title says the finding, and both axes have labels."""),

    md("""## My question

*My question:*

*The columns I need:*"""),

    md("## First analysis step"),
    blank("# Your first step\n",
          '''netherlands_products = netherlands_sales.groupby("description")["revenue"].sum()
netherlands_products = netherlands_products.sort_values(ascending=False)
netherlands_products.head(5)'''),

    md("## Check one number a second way\n\n*How I checked it:*"),
    blank("# Your check\n",
          '''lunch_box = netherlands_sales[netherlands_sales["description"] == "SPACEBOY LUNCH BOX"]
round(lunch_box["revenue"].sum(), 2)'''),

    md("## Next step"),
    blank("# Your next step\n",
          '''print(netherlands_sales["invoice"].nunique())'''),

    md("## Chart draft"),
    blank("# Your first chart\n",
          '''top5 = netherlands_products.head(5).sort_values()

plt.figure(figsize=(10, 4))
plt.barh(top5.index, top5.values)
plt.title("The Netherlands buys lunch boxes and snack boxes most")
plt.xlabel("Revenue (pounds)")
plt.ylabel("Product")
plt.tight_layout()
plt.show()'''),

    md("""## What I found so far

1. **Answer:**
2. **Evidence:**
3. **Next:**"""),

    md("""## Homework

- Keep going with your analysis.
- Make a **GitHub account** and an **empty public repository** with `github_guide.md`.
- Finish the case hunt if it is not done."""),
]

SESSION = {
    "folder": "s08_detective_work",
    "cells": cells,
    "expect": ["(101458, 10)", "(3066, 4)", "58182.55", "(671, 4)", "101458\n101458", "ROUND SNACK BOXES SET OF4 WOODLAND",
               "1689.6"],
}
