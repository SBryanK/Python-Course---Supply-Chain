from nbkit import md, code, exercise

cells = [
    md("""# Session 2: Shelves, cards and choices

**Question for today:** which order lines are big?

Our data records one line at a time, so "a big order" here means one big line."""),

    md("""## Warm-up (on paper)

Before you run anything, write down what this prints:

```python
quantity = 12
print(quantity)
```"""),

    md("""## Lists

A **list** is a row of bins on one shelf. In Excel, it is one column of values.
Python counts the bins from **0**, not 1. The first bin is number 0."""),
    code('''quantities = [6, 6, 8, 6, 6, 2, 6]

print(quantities[0])
print(quantities[1])
print(quantities[-1])'''),

    *exercise("Guess `quantities[2]` and `quantities[-1]` on paper. Then print both.",
              "`8` and `6`",
              "# TODO: print quantities[2] and quantities[-1]\n",
              "print(quantities[2])\nprint(quantities[-1])"),

    md("""## Count, total, smallest, largest

Same ideas as `COUNT`, `SUM`, `MIN` and `MAX` in Excel. Only the spelling is new."""),
    code('''print(len(quantities))
print(sum(quantities))
print(min(quantities), max(quantities))'''),

    md("""## Dictionaries

A **dictionary** is a product card: a field name and its value. In Excel, it is one row with headers.
You look up a value by its **name**, not by its position."""),
    code('''order_line = {
    "stock_code": "85123A",
    "description": "WHITE HANGING HEART T-LIGHT HOLDER",
    "quantity": 6,
    "price": 2.55,
    "country": "United Kingdom",
}

print(order_line["quantity"])'''),

    *exercise("Print the price and the country from the card.",
              "`2.55` and `United Kingdom`",
              "# TODO: print the price and the country of order_line\n",
              'print(order_line["price"])\nprint(order_line["country"])'),

    md("""## Comparisons

A comparison asks a question and answers `True` or `False`. In Excel: `=A2>10`.
One `=` **stores** a value. Two `==` **ask** if two things are equal."""),
    code('''print(6 > 10)
print(6 == 6)
print(order_line["country"] == "United Kingdom")'''),

    md("""## Decisions: if, elif, else

An `if` rule is like a packing rule: check the first condition, then the next, else do the last thing.
The indent (4 spaces) is part of the rule.

The numbers 100 and 12 are **teaching numbers**, not business rules."""),
    code('''quantity = order_line["quantity"]

if quantity >= 100:
    print("Big order line")
elif quantity >= 12:
    print("Medium order line")
else:
    print("Small order line")'''),

    *exercise("Set `quantity` to 12, then to 100. Guess each answer before you run it.",
              "`Medium order line`, then `Big order line`",
              "# TODO: copy the if rule, set quantity = 12, run it\n\n# TODO: now set quantity = 100 and run it again\n",
              'quantity = 12\nif quantity >= 100:\n    print("Big order line")\nelif quantity >= 12:\n    print("Medium order line")\nelse:\n    print("Small order line")\n\nquantity = 100\nif quantity >= 100:\n    print("Big order line")\nelif quantity >= 12:\n    print("Medium order line")\nelse:\n    print("Small order line")'),

    *exercise("Write a rule that prints `UK` if the country on the card is United Kingdom, and `Outside UK` if not. Then change the country to Germany and run it again.",
              "`UK`, then `Outside UK`",
              '# TODO: write the UK or Outside UK rule\n',
              'if order_line["country"] == "United Kingdom":\n    print("UK")\nelse:\n    print("Outside UK")\n\norder_line["country"] = "Germany"\nif order_line["country"] == "United Kingdom":\n    print("UK")\nelse:\n    print("Outside UK")'),

    md("""## Why does this happen? (optional)

Python counts how many steps you are **from the start**. The first bin is 0 steps away, so it is number 0. The last bin is `-1` steps from the end.
**For an analyst:** when someone says "the 3rd row", check if they count from 0 or from 1. This causes many off-by-one mistakes."""),

    md("""## Recap

You can now:
1. Use a list and read items by position.
2. Use a dictionary to look up a value by name.
3. Write an if / elif / else rule.

**Homework.** Add the quantities of rows 8 to 10 (from the Session 1 handout) to your list, and redo `len`, `sum`, `min`, `max`. Write one if rule about prices."""),
]

SESSION = {
    "folder": "s02_shelves_cards_choices",
    "cells": cells,
    "expect": ["7\n40\n2 8", "Small order line", "Medium order line", "Big order line", "UK", "Outside UK", "2.55", "United Kingdom"],
}
