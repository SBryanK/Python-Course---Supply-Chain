from nbkit import md, code, blank, DRIVE_WORK

cells = [
    md("""# Session 9: Polish and publish

**Question for today:** can you say your finding in three sentences?"""),

    md("""## Load your table"""),
    code(f'''import pandas as pd
from google.colab import drive

drive.mount("/content/drive")
sales_clean = pd.read_csv("{DRIVE_WORK}sales_clean.csv")
sales_clean["invoice_date"] = pd.to_datetime(sales_clean["invoice_date"])   # a CSV forgets dates
print(sales_clean.shape)'''),

    md("""## Final chart checklist

- [ ] The title says the finding.
- [ ] Both axes have labels with units (pounds, units, days).
- [ ] One message per chart.
- [ ] Long labels are readable (`plt.tight_layout()`).
- [ ] I can say the main number in one simple sentence, for example "about 1 in 5"."""),
    blank("# TODO: your final chart\n",
          '''import matplotlib.pyplot as plt

netherlands_sales = sales_clean[sales_clean["country"] == "Netherlands"]
netherlands_products = netherlands_sales.groupby("description")["revenue"].sum()
top5 = netherlands_products.sort_values(ascending=False).head(5).sort_values()

plt.figure(figsize=(10, 4))
plt.barh(top5.index, top5.values)
plt.title("The Netherlands buys mostly a few gift items")
plt.xlabel("Revenue (pounds)")
plt.ylabel("Product")
plt.tight_layout()
plt.show()'''),

    md("""## The three sentences

Write them here. Answer first.

1. **Answer:** (what is the finding?)
2. **Evidence:** (which numbers show it?)
3. **Recommendation:** (what should a manager do?)"""),

    md("""## GitHub, step by step

You already have an account and an empty public repository. You click every button yourself.

1. In Colab, choose **File > Save a copy in GitHub**. Pick your repository and save.
2. Open your repository on github.com and click **Add a file > Create new file**. Name it `README.md`.
3. Write the README (template below) and click **Commit changes**.
4. Open your repository link in a private browser window. Does it work?"""),

    md("""## README template

```
# My project title

**Question:** ...

**Data:** Chen, D. (2012). Online Retail II [Dataset]. UCI Machine Learning Repository.
https://doi.org/10.24432/C5CG6D. Licence CC BY 4.0.

**Finding:** ...

**How to run:** Open the notebook in Google Colab and run the cells from the top.
```"""),

    md("""## Your three slides

Open `presentation_template.pptx`. It has a cover, three content slides and a thank-you slide.
- **Slide 1, the question:** one sentence.
- **Slide 2, the finding:** one chart and one big number.
- **Slide 3, the recommendation:** what a manager should do.

One chart per slide. Say numbers simply ("about 1 in 5 products")."""),

    md("""## Self-reflection (due before Session 10)

Write one page. Use `reflection_template.md`. Answer six questions:
1. What can I do now that I could not do before? (Show one cell.)
2. My biggest mistake and how I fixed it.
3. Where do I still need help?
4. What I would change in my project.
5. My plan for the next 30 days.
6. One thing I am proud of."""),

    md("""## Recap

**Homework.** Finish your slides. Say your 5-minute talk out loud once. Write your reflection."""),
]

SESSION = {
    "folder": "s09_polish_publish",
    "cells": cells,
    "expect": ["(101458, 10)"],
}
