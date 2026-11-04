from nbkit import md, code, task

cells = [
    md("""# Session 3: Let the loop do the walking

Can one rule label every order line?"""),

    md("## For loops"),
    code('''quantities = [6, 6, 8, 6, 6, 2, 6]

for quantity in quantities:
    print(quantity)'''),
]

cells += task("predict", "How many times does `done` print? Guess first.",
              '''# My guess:
for quantity in quantities:
    print(quantity * 2)
print("done")''')

cells += [
    md("## Functions"),
    code('''def order_size(quantity):
    if quantity >= 100:
        return "big"
    elif quantity >= 12:
        return "medium"
    else:
        return "small"

print(order_size(6))
print(order_size(250))'''),
]

cells += task("predict", "This function prints but does not return. What is saved in `answer`? Guess first.",
              '''# My guess:
def size_with_print(quantity):
    print("small")

answer = size_with_print(6)
print(answer)''')

cells += task("fill", "Label every quantity in the list. Expected: `6 units -> small` and so on, 7 lines",
              '''for quantity in ____:
    label = ____(quantity)
    print(f"{quantity} units -> {label}")''',
              '''for quantity in quantities:
    label = order_size(quantity)
    print(f"{quantity} units -> {label}")''')

cells += task("fill", "A function that returns the value of a line, rounded to 2 decimals. Expected: `15.3`",
              '''def line_value(quantity, price):
    ____ round(quantity * price, 2)

print(line_value(6, 2.55))''',
              '''def line_value(quantity, price):
    return round(quantity * price, 2)

print(line_value(6, 2.55))''')

cells += task("fix", "The loop body is not indented. Fix it so it prints the 7 quantities.",
              '''for quantity in quantities:
print(quantity)''',
              '''for quantity in quantities:
    print(quantity)''')

cells += task("fix", "This is a real traceback: one quantity is text. Read it from the bottom, then fix the list. "
              "Expected: `small`, `medium`, `small`",
              '''mixed_quantities = [6, "12", 8]

for quantity in mixed_quantities:
    print(order_size(quantity))''',
              '''mixed_quantities = [6, 12, 8]   # 12 is a number now

for quantity in mixed_quantities:
    print(order_size(quantity))''')

cells += [
    md("## Real order lines\n\nEach line is a dictionary, and the list holds the cards."),
    code('''order_lines = [
    {"description": "WHITE HANGING HEART T-LIGHT HOLDER", "quantity": 6, "price": 2.55},
    {"description": "WHITE METAL LANTERN", "quantity": 6, "price": 3.39},
    {"description": "CREAM CUPID HEARTS COAT HANGER", "quantity": 8, "price": 2.75},
    {"description": "KNITTED UNION FLAG HOT WATER BOTTLE", "quantity": 6, "price": 3.39},
    {"description": "RED WOOLLY HOTTIE WHITE HEART.", "quantity": 6, "price": 3.39},
]

for line in order_lines:
    print(line["description"])'''),
]

cells += task("write", "Loop over the five lines and print the value of each with `line_value`. "
              "Expected: `15.3`, `20.34`, `22.0`, `20.34`, `20.34`",
              "# Your loop here\n",
              '''for line in order_lines:
    print(line_value(line["quantity"], line["price"]))''')

cells += task("write", "Change `order_size` so medium starts at 50, then label 6, 12, 99, 100 and 1930. "
              "Expected: `small`, `small`, `medium`, `big`, `big`",
              '''def order_size(quantity):
    ____

for quantity in [6, 12, 99, 100, 1930]:
    print(order_size(quantity))''',
              '''def order_size(quantity):
    if quantity >= 100:
        return "big"
    elif quantity >= 50:
        return "medium"
    else:
        return "small"

for quantity in [6, 12, 99, 100, 1930]:
    print(order_size(quantity))''')

cells += task("write", "Write `is_uk(country)` that returns `True` for United Kingdom and `False` for any other "
              "country. Expected: `True`, `False`",
              '''def is_uk(country):
    ____

print(is_uk("United Kingdom"))
print(is_uk("Germany"))''',
              '''def is_uk(country):
    if country == "United Kingdom":
        return True
    else:
        return False

print(is_uk("United Kingdom"))
print(is_uk("Germany"))''')

cells += task("case", "Invoice 540815 is a real big order with three lines: 1930 units at 2.55, 2000 at 1.85 and "
              "3114 at 2.10. For each line, print its size and its value. "
              "Expected: `1930 units: big, 4921.5 pounds`, then `3700.0` and `6539.4`",
              '''big_order = [
    {"quantity": 1930, "price": 2.55},
    {"quantity": 2000, "price": 1.85},
    {"quantity": 3114, "price": 2.10},
]

for line in big_order:
    ____

# My sentence for the manager:''',
              '''big_order = [
    {"quantity": 1930, "price": 2.55},
    {"quantity": 2000, "price": 1.85},
    {"quantity": 3114, "price": 2.10},
]

for line in big_order:
    size = order_size(line["quantity"])
    value = line_value(line["quantity"], line["price"])
    print(f"{line['quantity']} units: {size}, {value} pounds")

# My sentence for the manager: all three lines are big, and the biggest line is worth about 6,540 pounds.''')

cells += [md("## Extra (homework)")]

cells += task("extra", "Write your own function with a `return`: `with_tax(price)` gives the price plus 20%, "
              "rounded to 2 decimals. Expected: `3.06`",
              '''def with_tax(price):
    ____

print(with_tax(2.55))''',
              '''def with_tax(price):
    return round(price * 1.2, 2)

print(with_tax(2.55))''')

cells += task("extra", "Before Session 4: open a blank Colab notebook, run these two lines once and accept the "
              "Google permission screen.",
              '''# from google.colab import drive
# drive.mount("/content/drive")''')

SESSION = {
    "folder": "s03_let_loop_walk",
    "cells": cells,
    "expect": ["12\n12\n16\n12\n12\n4\n12\ndone", "small\nbig", "None", "6 units -> small", "15.3",
               "small\nmedium\nsmall", "15.3\n20.34\n22.0\n20.34\n20.34", "small\nsmall\nmedium\nbig\nbig",
               "True\nFalse", "1930 units: big, 4921.5 pounds", "3700.0", "6539.4", "3.06"],
}
