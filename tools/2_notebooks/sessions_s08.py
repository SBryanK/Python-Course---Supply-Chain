from nbkit import md, code, blank, DRIVE_WORK

cells = [
    md("""# Session 8: Detective work

**Question for today:** your own. Today you work on your project. Your teacher gives hints only, and you type everything."""),

    md("""## Load your table

Check the shape: `(101458, 10)`."""),
    code(f'''import pandas as pd
from google.colab import drive

drive.mount("/content/drive")
sales_clean = pd.read_csv("{DRIVE_WORK}sales_clean.csv")
sales_clean["invoice_date"] = pd.to_datetime(sales_clean["invoice_date"])   # a CSV forgets dates
print(sales_clean.shape)'''),

    md("""## Project checklist

- [ ] My question is one sentence.
- [ ] I know which columns I need.
- [ ] I run my steps in order, from the top.
- [ ] I print the shape or row count after each filter.
- [ ] I check one number by hand.
- [ ] My chart has a title that says the finding, and axis labels."""),

    md("""## My question, in my own words

*My question:*

*The columns I need:*"""),

    md("""## First analysis

Write your first step here. Run it, and look at the result before you go further."""),
    blank("# TODO: your first analysis step\n",
          '''revenue_by_country = sales_clean.groupby("country")["revenue"].sum()
revenue_by_country = revenue_by_country.sort_values(ascending=False)
print(revenue_by_country.head(3))'''),

    md("""## Check one number by hand

Pick one number from your result. Check it a second way: a filter and a `sum`, or Excel on a small piece of the data.
Write down what you did."""),
    blank("# TODO: check one number a second way\n",
          '''netherlands_sales = sales_clean[sales_clean["country"] == "Netherlands"]
print(round(netherlands_sales["revenue"].sum(), 2))
print(len(netherlands_sales))'''),

    md("""*How I checked it:*"""),

    md("""## Next step"""),
    blank("# TODO: your next step\n",
          '''netherlands_products = netherlands_sales.groupby("description")["revenue"].sum()
netherlands_products = netherlands_products.sort_values(ascending=False)
netherlands_products.head(5)'''),

    md("""## Chart draft

Use what you learned in Session 6: a title that says the finding, and axis labels."""),
    blank("# TODO: a first chart of your result\n",
          '''import matplotlib.pyplot as plt

top5 = netherlands_products.head(5).sort_values()

plt.figure(figsize=(10, 4))
plt.barh(top5.index, top5.values)
plt.title("The Netherlands buys mostly a few gift items")
plt.xlabel("Revenue (pounds)")
plt.ylabel("Product")
plt.tight_layout()
plt.show()'''),

    md("""## What I found so far (3 sentences)

1. **Answer:**
2. **Evidence:**
3. **What I will do next:**"""),

    md("""## Recap

**Homework.**
- Keep going with your analysis.
- Make a **GitHub account** and an **empty public repository**. Use `github_guide.md`. Do not upload the notebook yet.
- Finish your case hunt if it is not done."""),
]

SESSION = {
    "folder": "s08_detective_work",
    "cells": cells,
    "expect": ["United Kingdom", "Netherlands"],
}
