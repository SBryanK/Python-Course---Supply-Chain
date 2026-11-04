from nbkit import md, code, task

cells = [
    md("""# Session 1: Hello, Python

What is one order line worth? An *order line* is one product on one receipt.

Click a cell and press **Shift + Enter** to run it. Run the cells from the top."""),

    md("## Print"),
    code('''print("Hello, supply chain")
print(6)'''),

    md("## Variables"),
    code('''product_name = "WHITE HANGING HEART T-LIGHT HOLDER"
quantity = 6
unit_price = 2.55

print(product_name)
print(quantity)'''),
]

cells += task("predict", "What does this cell print? Guess first, then run it.",
              '''# My guess:
quantity = 7
print(quantity)
quantity = 6
print(quantity)''')

cells += [
    md("## Multiply and round"),
    code('''sales_value = quantity * unit_price
print(sales_value)
print(round(sales_value, 2))'''),
]

cells += task("fill", "The WHITE METAL LANTERN costs 3.39. Its line value, rounded to 2 decimals. Expected: `20.34`",
              '''lantern_price = 3.39
lantern_value = round(quantity * ____, ____)
print(lantern_value)''',
              '''lantern_price = 3.39
lantern_value = round(quantity * lantern_price, 2)
print(lantern_value)''')

cells += [
    md("## Types"),
    code('''print(type(quantity))
print(type(unit_price))
print(type(product_name))'''),
]

cells += task("predict", "Numbers add up. What does text do? Guess both lines first.",
              '''# My guess:
print(5 + 5)
print("5" + "5")''')

cells += [
    md("## f-strings"),
    code('''print(f"We sold {quantity} units for {round(sales_value, 2)} pounds")'''),

    md("## Errors\n\nRead the last line of an error first. It names the error."),
]

cells += task("fix", "A typo. Fix it so it prints `6`.",
              "print(quantiy)",
              "print(quantity)")

cells += task("fix", "Something is missing. Fix it so it prints `hello`.",
              'print("hello"',
              'print("hello")')

cells += task("fix", "Text plus a number. Fix it so it prints `10`.",
              'print("5" + 5)',
              'print(int("5") + 5)')

cells += task("write", "CREAM CUPID HEARTS COAT HANGER: 8 units at 2.75. Save the line value in `hanger_value`. "
              "Expected: `22.0`",
              '''hanger_value = ____
print(hanger_value)''',
              '''hanger_value = round(8 * 2.75, 2)
print(hanger_value)''')

cells += task("write", "One sentence about the first line, with an f-string. Use the variables, not typed numbers. "
              "Expected: `WHITE HANGING HEART T-LIGHT HOLDER: 6 units = 15.3 pounds`",
              '''# Your f-string here
''',
              '''print(f"{product_name}: {quantity} units = {round(sales_value, 2)} pounds")''')

cells += task("write", "The price goes up to 2.95. Change `unit_price`, then compute `sales_value` again. "
              "Expected: `17.7`",
              '''unit_price = ____
sales_value = ____
print(round(sales_value, 2))''',
              '''unit_price = 2.95
sales_value = quantity * unit_price
print(round(sales_value, 2))''')

cells += task("case", "Invoice 536365 starts with the three lines above: the T-light holder (6 at 2.55), the lantern "
              "(6 at 3.39) and the coat hanger (8 at 2.75). What are these three lines worth together? "
              "Print one sentence. Expected: `The first three lines are worth 57.64 pounds`",
              '''invoice_value = ____
print(f"The first three lines are worth {____} pounds")

# My sentence for the manager:''',
              '''invoice_value = 6 * 2.55 + 6 * 3.39 + 8 * 2.75
print(f"The first three lines are worth {round(invoice_value, 2)} pounds")

# My sentence for the manager: the first three lines of invoice 536365 bring about 58 pounds.''')

cells += [md("## Extra (homework)")]

cells += task("extra", "SET 7 BABUSHKA NESTING BOXES: 2 units at 7.65. Expected: `15.3`",
              '''boxes_value = ____
print(boxes_value)''',
              '''boxes_value = round(2 * 7.65, 2)
print(boxes_value)''')

cells += task("extra", "Make all three errors on purpose in this cell, one at a time, and read the last line each time.",
              "# Try a NameError, a SyntaxError and a TypeError here\n",
              "# A NameError: print(quantiy)\n# A SyntaxError: print(\"hello\"\n# A TypeError: print(\"5\" + 5)")

SESSION = {
    "folder": "s01_hello_python",
    "cells": cells,
    "expect": ["Hello, supply chain", "15.299999999999999", "15.3", "20.34", "<class 'float'>", "55", "hello", "22.0",
               "WHITE HANGING HEART T-LIGHT HOLDER: 6 units = 15.3 pounds", "17.7",
               "The first three lines are worth 57.64 pounds"],
}
