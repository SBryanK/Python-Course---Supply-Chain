from nbkit import md, code, task

cells = [
    md("""# Session 2: Shelves, cards and choices

Which order lines are big? Our data records one line at a time, so "big" means one big line."""),

    md("## Lists"),
    code('''quantities = [6, 6, 8, 6, 6, 2, 6]

print(quantities[0])
print(quantities[-1])'''),
]

cells += task("predict", "What is `quantities[2]`? And `quantities[5]`? Guess first.",
              '''# My guess:
print(quantities[2])
print(quantities[5])''')

cells += [
    md("## Count, total, smallest, largest"),
    code('''print(len(quantities))
print(sum(quantities))
print(min(quantities), max(quantities))'''),
]

cells += task("fill", "The average quantity is the total divided by the count. Expected: `5.71`",
              '''average_quantity = round(____(quantities) / ____(quantities), 2)
print(average_quantity)''',
              '''average_quantity = round(sum(quantities) / len(quantities), 2)
print(average_quantity)''')

cells += [
    md("## Dictionaries"),
    code('''order_line = {
    "stock_code": "85123A",
    "description": "WHITE HANGING HEART T-LIGHT HOLDER",
    "quantity": 6,
    "price": 2.55,
    "country": "United Kingdom",
}

print(order_line["quantity"])'''),
]

cells += task("fill", "The value of this line, from the card. Expected: `15.3`",
              '''line_value = round(order_line[____] * order_line[____], 2)
print(line_value)''',
              '''line_value = round(order_line["quantity"] * order_line["price"], 2)
print(line_value)''')

cells += task("fix", "This asks for a position that does not exist. Fix it so it prints the last quantity, `6`.",
              "print(quantities[7])",
              "print(quantities[-1])")

cells += task("fix", "This key is spelled wrong. Fix it so it prints `2.55`.",
              'print(order_line["Price"])',
              'print(order_line["price"])')

cells += [
    md("## Comparisons and if rules\n\nThe numbers 100 and 12 are teaching numbers, not business rules."),
    code('''quantity = order_line["quantity"]

if quantity >= 100:
    print("Big order line")
elif quantity >= 12:
    print("Medium order line")
else:
    print("Small order line")'''),
]

cells += task("predict", "Set `quantity` to 12. Which line prints? Guess first.",
              '''# My guess:
quantity = 12

if quantity >= 100:
    print("Big order line")
elif quantity >= 12:
    print("Medium order line")
else:
    print("Small order line")''')

cells += task("write", "Print `UK` if the card's country is United Kingdom, else `Outside UK`. Expected: `UK`",
              "# Your rule here\n",
              '''if order_line["country"] == "United Kingdom":
    print("UK")
else:
    print("Outside UK")''')

cells += task("write", "Add rows 8 to 10 to the list: 6, 6 and 6. Use `quantities + [...]`. Then print the new "
              "length and total. Expected: `10` and `58`",
              '''quantities = ____
print(len(quantities))
print(sum(quantities))''',
              '''quantities = quantities + [6, 6, 6]
print(len(quantities))
print(sum(quantities))''')

cells += task("write", "A price rule: print `Cheap` if the price is below 3, else `Not cheap`. Use the card. "
              "Expected: `Cheap`",
              "# Your price rule here\n",
              '''if order_line["price"] < 3:
    print("Cheap")
else:
    print("Not cheap")''')

cells += task("case", "The warehouse packs a line in a big box when the quantity is 24 or more, else a small box. "
              "Make a card for the line with code `22752` (SET 7 BABUSHKA NESTING BOXES, 2 units at 7.65), "
              "and print which box it needs. Expected: `22752: small box`",
              '''babushka = {
    "stock_code": ____,
    "quantity": ____,
    "price": ____,
}

# Your box rule here

# My sentence for the warehouse:''',
              '''babushka = {
    "stock_code": "22752",
    "quantity": 2,
    "price": 7.65,
}

if babushka["quantity"] >= 24:
    print(f'{babushka["stock_code"]}: big box')
else:
    print(f'{babushka["stock_code"]}: small box')

# My sentence for the warehouse: the babushka line has only 2 units, so a small box is enough.''')

cells += [md("## Extra (homework)")]

cells += task("extra", "Change the card's country to Germany, then run your UK rule again. Expected: `Outside UK`",
              '''order_line["country"] = ____

# Your UK rule again''',
              '''order_line["country"] = "Germany"

if order_line["country"] == "United Kingdom":
    print("UK")
else:
    print("Outside UK")''')

cells += task("extra", "How many different values are in the list? Use `set()`, which keeps each value once, "
              "and `len`. Expected: `3`",
              '''different = ____
print(different)''',
              '''different = len(set(quantities))
print(different)''')

SESSION = {
    "folder": "s02_shelves_cards_choices",
    "cells": cells,
    "expect": ["8\n2", "7\n40\n2 8", "5.71", "15.3", "2.55", "Small order line", "Medium order line", "UK", "10\n58",
               "Cheap", "22752: small box", "Outside UK"],
}
