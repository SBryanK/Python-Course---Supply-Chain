from nbkit import md, code, task

cells = [
    md("""# Session 10: Showtime

Can you explain it like an analyst?"""),

    md("""## Before you start

- [ ] My slides open and I know the order.
- [ ] My answer comes first, in the first 30 seconds.
- [ ] I say numbers simply.
- [ ] I do not read the slides.

5 minutes: 1 for the question, 2 for the finding and evidence, 1 for the recommendation, 1 spare."""),

    md("## The course in five cells\n\nOne cell from each part of the course. Guess each one first."),
]

cells += task("predict", "Session 1. What prints?",
              '''# My guess:
print(round(6 * 2.55, 2))''')

cells += task("predict", "Session 2. What prints?",
              '''# My guess:
quantities = [6, 6, 8, 6, 6, 2, 6]
print(quantities[2], len(quantities))''')

cells += task("predict", "Session 3. What prints?",
              '''# My guess:
def order_size(quantity):
    if quantity >= 100:
        return "big"
    elif quantity >= 12:
        return "medium"
    else:
        return "small"

for quantity in [6, 24, 3114]:
    print(order_size(quantity))''')

cells += task("predict", "Sessions 4 and 5. How many rows are left, and what is the total? Guess first.",
              '''# My guess:
import pandas as pd

orders = pd.DataFrame({"invoice": ["536365", "C536379", "536366"], "revenue": [15.3, -27.5, 11.1]})
kept = orders[~orders["invoice"].str.startswith("C")]
print(len(kept), round(kept["revenue"].sum(), 2))''')

cells += task("predict", "Session 7. What does this query return?",
              '''# My guess:
import sqlite3

connection = sqlite3.connect(":memory:")
orders.to_sql("orders", connection, index=False)
pd.read_sql_query("SELECT COUNT(*) AS lines FROM orders WHERE revenue > 0", connection)''')

cells += task("write", "One line of your own: an f-string sentence about your project's main number, said simply.",
              '''# My sentence
''',
              '''print("About 1 in 5 products bring 80% of revenue.")''')

cells += [
    md("""## Questions to expect

- Walk me through your project in 2 minutes.
- Why did you remove those rows?
- What would you do with more time?
- How did you check your numbers?

*Notes for my answers:*"""),

    md("""## Feedback I received

*Two things I did well:*

*One thing to improve:*"""),

    md("""## Keep, stop, start

- **Keep:**
- **Stop:**
- **Start:**"""),

    md("""## What next

Optional ideas for January: deeper Power BI, more SQL, VS Code, git on the command line.

*My plan for the next 30 days:*"""),
]

SESSION = {
    "folder": "s10_showtime",
    "cells": cells,
    "expect": ["15.3", "8 7", "small\nmedium\nbig", "2 26.4", "About 1 in 5 products bring 80% of revenue."],
}
