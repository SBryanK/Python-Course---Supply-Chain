from nbkit import md, code, exercise, zoo

cells = [
    md("""# Session 3: Let the loop do the walking

**Question for today:** can one rule label every order line?"""),

    md("""## Warm-up (on paper)

Write down what these print:

```python
quantities = [6, 6, 8, 6, 6, 2, 6]
print(quantities[2])
if quantities[0] >= 12:
    print("medium")
else:
    print("small")
```"""),

    md("""## For loops

A **for loop** walks down the shelf and checks each bin. In Excel, it is like dragging a formula down a column.
The lines inside the loop must be indented."""),
    code('''quantities = [6, 6, 8, 6, 6, 2, 6]

for quantity in quantities:
    print(quantity)'''),

    *exercise("Loop over the list and print each quantity times 2.",
              "`12`, `12`, `16`, `12`, `12`, `4`, `12`, one per line",
              "# TODO: loop over quantities and print quantity * 2\n",
              "for quantity in quantities:\n    print(quantity * 2)"),

    md("""## Functions

A **function** is your own reusable rule, like your own named formula in Excel.
Writing it does nothing yet. It runs only when you **call** it."""),
    code('''def order_size(quantity):
    if quantity >= 100:
        return "big"
    elif quantity >= 12:
        return "medium"
    else:
        return "small"

print(order_size(6))
print(order_size(250))'''),

    md("""## `return` and `print` are different

`return` hands the answer back, so you can use it again. `print` only shows it.
Look at what the second function gives back."""),
    code('''def size_with_print(quantity):
    print("small")

answer = size_with_print(6)
print(answer)'''),

    md("""Now use the function on every quantity with a loop."""),
    code('''for quantity in quantities:
    label = order_size(quantity)
    print(f"{quantity} units -> {label}")'''),

    md("""## Real order lines

The first five lines of the data. Each line is a dictionary (a product card), and the list holds the five cards."""),
    code('''order_lines = [
    {"description": "WHITE HANGING HEART T-LIGHT HOLDER", "quantity": 6, "price": 2.55},
    {"description": "WHITE METAL LANTERN", "quantity": 6, "price": 3.39},
    {"description": "CREAM CUPID HEARTS COAT HANGER", "quantity": 8, "price": 2.75},
    {"description": "KNITTED UNION FLAG HOT WATER BOTTLE", "quantity": 6, "price": 3.39},
    {"description": "RED WOOLLY HOTTIE WHITE HEART.", "quantity": 6, "price": 3.39},
]

for line in order_lines:
    print(f"{line['description']}: {order_size(line['quantity'])}")'''),

    *exercise("Write a function `line_value(quantity, price)` that **returns** `quantity * price` rounded to 2 decimals. Call it for 6 units at 2.55.",
              "`15.3`",
              "# TODO: write line_value(quantity, price) with return\n\n# TODO: call it with 6 and 2.55 and print the answer\n",
              "def line_value(quantity, price):\n    return round(quantity * price, 2)\n\nprint(line_value(6, 2.55))"),

    *exercise("Loop over the five real lines and print the value of each, using `line_value`.",
              "`15.3`, `20.34`, `22.0`, `20.34`, `20.34`",
              "# TODO: loop over order_lines and print line_value for each line\n",
              'for line in order_lines:\n    print(line_value(line["quantity"], line["price"]))'),

    *exercise("Label these quantities with `order_size`: 6, 12, 99, 100, 1930. Then change the medium rule from 12 to 50 in the function and guess what changes.",
              "`small`, `medium`, `medium`, `big`, `big`. With 50, the 12 becomes `small`.",
              "# TODO: loop over [6, 12, 99, 100, 1930] and print order_size for each\n\n# TODO: edit order_size so medium starts at 50, run the loop again\n",
              "for quantity in [6, 12, 99, 100, 1930]:\n    print(order_size(quantity))\n\ndef order_size(quantity):\n    if quantity >= 100:\n        return \"big\"\n    elif quantity >= 50:\n        return \"medium\"\n    else:\n        return \"small\"\n\nfor quantity in [6, 12, 99, 100, 1930]:\n    print(order_size(quantity))"),

    md("""## Reading a traceback

A **traceback** is a stack of plates. The last plate is on top, and Python prints it at the bottom.
**Read the bottom line first,** then go up to see which line caused it.

This cell has a text quantity (`"12"`) in the list. Run it and find the line that broke."""),
    zoo('''def order_size(quantity):
    if quantity >= 100:
        return "big"
    elif quantity >= 12:
        return "medium"
    else:
        return "small"

mixed_quantities = [6, "12", 8]

for quantity in mixed_quantities:
    print(order_size(quantity))''',
        '''def order_size(quantity):
    if quantity >= 100:
        return "big"
    elif quantity >= 12:
        return "medium"
    else:
        return "small"

mixed_quantities = [6, 12, 8]   # fixed: 12 is a number now

for quantity in mixed_quantities:
    print(order_size(quantity))'''),

    md("""**Your turn.** Which line broke? Write the line, then fix the list so the loop runs.

*Expected:* the line is `if quantity >= 100:` inside the function, because text cannot be compared with a number."""),

    md("""## Why does this happen? (optional)

Python runs a function only when you call it. Until then, the `def` is just a saved rule. That is why you can write a function today and use it a hundred times tomorrow.
**For an analyst:** a function is how you write a rule once, so every report uses the same rule."""),

    md("""## Recap

You can now:
1. Use a for loop to visit every item.
2. Write a function with `def` and `return`.
3. Read a traceback from the bottom.

**Homework.** Use `line_value` on the five real lines on your handout. Write one function of your own with a `return`.
Open a blank Colab notebook, run the two lines below once, and accept the Google permission screen. This keeps the pop-up away from Session 4.

```python
from google.colab import drive
drive.mount("/content/drive")
```"""),
]

SESSION = {
    "folder": "s03_let_loop_walk",
    "cells": cells,
    "expect": ["12\n12\n16\n12\n12\n4\n12", "big", "medium", "small", "None", "15.3", "20.34", "22.0"],
}
