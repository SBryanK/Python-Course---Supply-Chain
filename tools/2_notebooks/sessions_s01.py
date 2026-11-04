from nbkit import md, code, exercise, zoo

cells = [
    md("""# Session 1: Hello, Python

**Question for today:** what is one order line worth?

An *order line* is one product on one receipt. We will use real lines from an online gift shop.

**How this notebook works.** Click a cell and press **Shift + Enter** to run it. Run the cells from the top, in order.
If you see a `NameError`, run the cells above it again."""),

    md("""## Print

`print()` shows something on the screen. Python shows nothing unless you ask."""),
    code('''print("Hello, supply chain")
print("My first line of Python")'''),

    md("""## Variables

A **variable** is a label on a storage bin. You put a value in the bin and use the label to find it again.
If you change the value, other cells do not update by themselves. Run them again."""),
    code('''product_name = "WHITE HANGING HEART T-LIGHT HOLDER"
quantity = 6
unit_price = 2.55

print(product_name)
print(quantity)
print(unit_price)'''),

    *exercise("Change `quantity` to 7 and print it. Guess the result first. Then put it back to 6.",
              "`7`, and then `quantity` is 6 again.",
              "# TODO: set quantity to 7 and print it\n\n# TODO: set quantity back to 6\n",
              "quantity = 7\nprint(quantity)\n\nquantity = 6"),

    md("""## Multiply

The value of a line is `quantity * unit_price`, like `=B2*C2` in Excel."""),
    code('''sales_value = quantity * unit_price
print(sales_value)'''),

    md("""The long decimal is normal. A computer stores some decimals a little inexactly.
So when you show money, **round it**: `round(value, 2)` keeps 2 decimals."""),
    code("print(round(sales_value, 2))"),

    *exercise("Change `unit_price` to 3.39. Guess the new value, then check it. Put the price back to 2.55 after.",
              "`20.34`",
              "# TODO: set unit_price to 3.39, then print the rounded sales value\n\n# TODO: put unit_price back to 2.55\n",
              "unit_price = 3.39\nprint(round(quantity * unit_price, 2))\n\nunit_price = 2.55"),

    md("""## Types

Python keeps numbers and text apart.
- `int`: a whole number, like boxes counted
- `float`: a number with decimals, like a price
- `str`: text, like a product name

`"5"` in quotes is text. Python will not add text to a number."""),
    code('''print(type(quantity))
print(type(unit_price))
print(type(product_name))

print(5 + 5)
print("5" + "5")'''),

    md("""## f-strings

An **f-string** is a fill-in-the-blank label. Put an `f` before the quote and write the variable names inside `{ }`.
It is easy to forget the `f`."""),
    code('''print(f"We sold {quantity} units of {product_name} for {round(sales_value, 2)} pounds.")'''),

    *exercise("Compute the value of two more real lines: WHITE METAL LANTERN (6 units at 3.39) and CREAM CUPID HEARTS COAT HANGER (8 units at 2.75).",
              "`20.34` and `22.0`",
              "# TODO: print the value of 6 units at 3.39\n\n# TODO: print the value of 8 units at 2.75\n",
              "print(round(6 * 3.39, 2))\nprint(round(8 * 2.75, 2))"),

    *exercise("Write one sentence about the first line with an f-string. Use the variables, not typed numbers.",
              "Something like: `WHITE HANGING HEART T-LIGHT HOLDER: 6 units at 2.55 pounds each = 15.3 pounds`",
              "# TODO: print one f-string sentence about the first order line\n",
              'print(f"{product_name}: {quantity} units at {unit_price} pounds each = {round(sales_value, 2)} pounds")'),

    md("""## Errors

Errors are normal. Even analysts see them every day. **Read the last line first.** It names the error.

| Error | What it means |
|---|---|
| `NameError` | Python does not know this name (often a typo) |
| `SyntaxError` | A bracket or quote is missing |
| `TypeError` | You mixed things that do not mix, like text and a number |

Predict the error type, run each cell, and read the last line."""),
    zoo('print(quantiy)', 'print(quantity)   # fixed: the name is quantity'),
    zoo('print("hello"', 'print("hello")   # fixed: the bracket is closed'),
    zoo('print("5" + 5)', 'print(int("5") + 5)   # fixed: turn the text into a number first'),

    md("""**Your turn.** Fix the three cells above so each one runs without an error. Change the code in place, then run it again.

*Expected:* the three cells print `6`, `hello` and `10`."""),

    md("""## Why does this happen? (optional)

A computer keeps numbers in binary. Some decimals, like 2.55, cannot be stored exactly, just as 1/3 cannot be written exactly in decimals.
The error is tiny, but it shows up when you print. **For an analyst:** calculate with the full value and round only when you show the result."""),

    md("""## Recap

You can now:
1. Print a value and keep it in a variable.
2. Tell numbers from text, and multiply and round.
3. Write a sentence with an f-string and read an error.

**Homework.** Finish the Your turn cells. Make the three errors on purpose at home. Write one f-string about rows 8 to 10 on the handout.
**Before the lesson:** use a Google account, Chrome or Edge, a charger and a headset. Check you can open the Drive folder."""),
]

SESSION = {
    "folder": "s01_hello_python",
    "cells": cells,
    "expect": ["15.299999999999999", "15.3", "20.34", "22.0", "<class 'int'>", "<class 'float'>", "<class 'str'>", "55", "10"],
}
