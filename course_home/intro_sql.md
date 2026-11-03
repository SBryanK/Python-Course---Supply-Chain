# Intro to SQL (self-study, one page)

SQL is the language for asking a database a question. Many companies keep their data in databases. You already know the ideas from pandas.

| SQL | pandas idea |
|---|---|
| `SELECT ... FROM` | choose columns |
| `WHERE` | filter rows |
| `GROUP BY` | `groupby` |
| `ORDER BY ... DESC` | sort, biggest first |
| `LIMIT 5` | keep the first 5 rows |

```sql
SELECT country, SUM(revenue) AS total_revenue
FROM sales
GROUP BY country
ORDER BY total_revenue DESC
LIMIT 5
```

This gives the five countries with the most revenue. The result is the same as `sales_clean.groupby("country")["revenue"].sum()` sorted and cut to five rows.

**Run it in Python:** the notebook for Session 7 puts the table into SQLite, which lives inside Python, so you install nothing. Use `pd.read_sql_query(query, connection)`.

**MySQL** is another SQL database. It runs on a server. Basic queries look almost the same. We do not install it.

**Practise** (free, in the browser): sql-practice.com.
