# Project plan

Fill this in during Session 7. Keep it short. One question, one chart, one decision.

| Part | Your answer |
|---|---|
| My question | |
| Columns I need | |
| Steps | |
| The chart I expect | |
| The decision it helps | |

## Project menu

Choose one, or write your own. A good question is specific, answerable with this data, and useful to a manager.
If a question needs a skill we did not teach, change the question, not the skill.

1. Is class A revenue steady month to month? (Filter class A, group by month, one line chart.)
2. Which country outside the UK buys the most, and what are its top 5 products?
3. How big are cancellations, and which products get cancelled most? (Use `cancellations.csv`, 1,904 rows.)
4. A reorder point for the top 5 products. Use a lead time and a safety stock that **you choose**. Label every assumption as an assumption.

## Facts you can use

- The data has **68 trading days** (1 December 2010 to 28 February 2011).
- Clean revenue is **1,876,534.04 pounds**.
- The clean table has 101,458 rows and 3,066 products.

## Worked example for the reorder point (question 4)

Reorder point = daily demand x lead time, plus safety stock.

| Item | Value | Data or assumption? |
|---|---|---|
| Product | 85123A WHITE HANGING HEART T-LIGHT HOLDER | data |
| Units sold in 68 days | 11,156 | data |
| Daily demand (units / 68) | 164.1 | data |
| Lead time | 7 days | **assumption** |
| Demand during lead time | 164.1 x 7 = 1,148.7 | calculated |
| Safety stock | 20% of that = 229.7 | **assumption** |
| Reorder point | 1,378 units | calculated |

Choose your own lead time and safety stock, and say why.

## A January idea (not for this course)

Olist, a Brazilian e-commerce dataset on Kaggle, is a good next dataset. Check its licence before you publish anything.
