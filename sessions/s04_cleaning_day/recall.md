# Session 4: daily recall

Three short questions a day. Answer from memory first, then check the answers at the end.

## Fri 27 Nov

1. What does `sales.shape` tell you?
2. Why do we look at the data before we clean it?
3. How do you keep only the rows where `price` is above 0?

## Sat 28 Nov

1. What is the difference between a list and a dictionary?
2. Why must you save a filter in a variable?
3. What does `.copy()` do?

## Sun 29 Nov

1. Which column holds the month, and how did we make it?
2. What does `&` do in a filter?
3. Why did we remove invoice 541431?

## Answers

**Fri 27 Nov**
1. The number of rows and columns.
2. To know what is inside, so we choose the right steps.
3. `sales_clean = sales_clean[sales_clean["price"] > 0]`.

**Sat 28 Nov**
1. A list is found by position. A dictionary is found by name.
2. A filter gives a new table. If you do not save it, it is lost.
3. It makes a separate table, like Save As.

**Sun 29 Nov**
1. `month`, from `invoice_date` with `.dt.to_period("M")`.
2. It combines two conditions. Both must be true.
3. It was cancelled 16 minutes later, so the sale never happened.
