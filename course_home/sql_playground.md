# SQL practice

Use the `sales` table from the Session 7 notebook. Run each query with `pd.read_sql_query(query, connection)`.

1. The total revenue of Germany. *Answer: 37365.63*
```sql
SELECT SUM(revenue) AS germany_revenue FROM sales WHERE country = 'Germany'
```
2. The 10 rows with the biggest revenue. *The first row has revenue 6539.4*
```sql
SELECT invoice, description, revenue FROM sales ORDER BY revenue DESC LIMIT 10
```
3. Try it yourself: how many rows are there for France? Hint: `COUNT(*)`.
4. Try it yourself: the 5 products with the most units sold. Hint: `SUM(quantity)` and `GROUP BY description`.

More free practice: sql-practice.com.
