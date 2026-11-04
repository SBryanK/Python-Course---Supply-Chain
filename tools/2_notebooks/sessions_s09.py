from nbkit import md, code, task, blank, DRIVE_WORK

cells = [
    md("""# Session 9: Polish and publish

Can you say your finding in three sentences?"""),

    md("## Load your tables"),
    code(f'''import pandas as pd
import matplotlib.pyplot as plt
from google.colab import drive

drive.mount("/content/drive")
sales_clean = pd.read_csv("{DRIVE_WORK}sales_clean.csv")
sales_clean["invoice_date"] = pd.to_datetime(sales_clean["invoice_date"])   # a CSV forgets dates
product_value = pd.read_csv("{DRIVE_WORK}product_value.csv")
print(sales_clean.shape)'''),

    md("## Polish warm-up"),
]

cells += task("predict", "671 of 3066 products are class A. About 1 in how many? Guess first.",
              '''# My guess:
round(3066 / 671)''')

cells += task("fill", "Say the total revenue simply, in millions with 1 decimal. Expected: `About 1.9 million pounds`",
              '''total_revenue = sales_clean["revenue"].sum()
millions = round(total_revenue / ____, ____)
print(f"About {millions} million pounds")''',
              '''total_revenue = sales_clean["revenue"].sum()
millions = round(total_revenue / 1_000_000, 1)
print(f"About {millions} million pounds")''')

cells += task("fix", "The month labels are dates as text and overlap. Make the chart readable: add `plt.xticks(rotation=45)` "
              "and a finding title.",
              '''monthly_revenue = sales_clean.groupby("month")["revenue"].sum()

plt.figure(figsize=(6, 4))
plt.bar(monthly_revenue.index, monthly_revenue.values)
plt.xlabel("Month")
plt.ylabel("Revenue (pounds)")
plt.show()''',
              '''monthly_revenue = sales_clean.groupby("month")["revenue"].sum()

plt.figure(figsize=(6, 4))
plt.bar(monthly_revenue.index, monthly_revenue.values)
plt.title("Revenue fell each month after December")
plt.xlabel("Month")
plt.ylabel("Revenue (pounds)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()''')

cells += task("write", "The UK share of revenue, said simply as a whole percent. Expected: `About 85% of revenue is from the UK`",
              '''uk_revenue = ____
uk_share = ____
print(f"About {uk_share}% of revenue is from the UK")''',
              '''uk_revenue = sales_clean[sales_clean["country"] == "United Kingdom"]["revenue"].sum()
uk_share = round(100 * uk_revenue / total_revenue)
print(f"About {uk_share}% of revenue is from the UK")''')

cells += task("write", "Three sentences for the ABC finding, printed with f-strings. Answer first. "
              "Expected: the first line is `About 1 in 5 products bring 80% of revenue.`",
              '''# Your three print lines here
''',
              '''print("About 1 in 5 products bring 80% of revenue.")
print(f"Class A is {(product_value['abc_class'] == 'A').sum()} of {len(product_value)} products.")
print("Keep class A in stock first, and review the class C products.")''')

cells += [
    md("""## Your final chart

- [ ] The title says the finding.
- [ ] Both axes have labels with units.
- [ ] One message per chart.
- [ ] Long labels are readable.
- [ ] The main number, said simply."""),
    blank("# Your final chart\n",
          '''netherlands_sales = sales_clean[sales_clean["country"] == "Netherlands"]
netherlands_products = netherlands_sales.groupby("description")["revenue"].sum()
top5 = netherlands_products.sort_values(ascending=False).head(5).sort_values()

plt.figure(figsize=(10, 4))
plt.barh(top5.index, top5.values)
plt.title("The Netherlands buys lunch boxes and snack boxes most")
plt.xlabel("Revenue (pounds)")
plt.ylabel("Product")
plt.tight_layout()
plt.show()'''),

    md("""## My three sentences

1. **Answer:**
2. **Evidence:**
3. **Recommendation:**"""),

    md("""## GitHub

1. In Colab: **File > Save a copy in GitHub**. Pick your repository.
2. On github.com: **Add a file > Create new file**, named `README.md`.
3. Write the README below, then **Commit changes**.
4. Open your link in a private window. Does it work?"""),

    md("""## README template

```
# My project title

**Question:** ...

**Data:** Chen, D. (2012). Online Retail II [Dataset]. UCI Machine Learning Repository.
https://doi.org/10.24432/C5CG6D. Licence CC BY 4.0.

**Finding:** ...

**How to run:** Open the notebook in Google Colab and run the cells from the top.
```"""),

    md("""## Your slides

`presentation_template.pptx`: cover, question, finding, recommendation, thank you.
One chart per slide. The answer in the first 30 seconds."""),

    md("""## Reflection (due before Session 10)

One page with `reflection_template.md`: what I can do now (show one cell), my biggest mistake and the fix,
where I need help, what I would change, my next 30 days, one thing I am proud of."""),
]

SESSION = {
    "folder": "s09_polish_publish",
    "cells": cells,
    "expect": ["(101458, 10)", "5", "About 1.9 million pounds", "About 85% of revenue is from the UK",
               "About 1 in 5 products bring 80% of revenue.", "Class A is 671 of 3066 products."],
}
