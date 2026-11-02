"""Check large lines and cancellation artefacts in candidate lesson windows.

For each window: the biggest single lines, and how much revenue in the cleaned
window belongs to positive lines that have a matching cancellation later
(same customer, product, quantity, price). This tells us whether a window
contains the known 'buy then cancel' outlier.
"""
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
raw = pd.read_csv(ROOT / "data" / "work" / "sheet_2010_2011.csv", parse_dates=["InvoiceDate"])
raw["Invoice"] = raw["Invoice"].astype(str)
raw["StockCode"] = raw["StockCode"].astype(str)

WINDOWS = {
    "A_dec2010_feb2011": ("2010-12-01", "2011-03-01"),
    "F_feb2011_apr2011": ("2011-02-01", "2011-05-01"),
    "G_mar2011_may2011": ("2011-03-01", "2011-06-01"),
}

NON_PRODUCT = ["POST", "DOT", "M", "BANK CHARGES", "C2", "D", "S", "AMAZONFEE", "ADJUST", "CRUK", "PADS", "B", "GIFT"]


def clean(df):
    d = df.drop_duplicates()
    d = d[~d["Invoice"].str.upper().str.startswith("C")]
    d = d[d["Quantity"] > 0]
    d = d[d["Price"] > 0]
    d = d[~d["StockCode"].isin(NON_PRODUCT)]
    return d.copy()


out = {}
for name, (start, end) in WINDOWS.items():
    w = raw[(raw["InvoiceDate"] >= start) & (raw["InvoiceDate"] < end)].copy()
    c = clean(w)
    c["revenue"] = c["Quantity"] * c["Price"]

    # Big single lines.
    big = c.nlargest(12, "revenue")[
        ["Invoice", "StockCode", "Description", "Quantity", "Price", "InvoiceDate", "revenue"]
    ]

    # Cancellation matching: C rows give (customer, code, abs qty, price), then
    # positive rows that match and come earlier in the same window.
    canc = w[w["Invoice"].str.upper().str.startswith("C")].copy()
    canc = canc[canc["Quantity"] < 0]
    canc["qty_abs"] = -canc["Quantity"]
    canc = canc[["Customer ID", "StockCode", "qty_abs", "Price", "InvoiceDate"]].rename(
        columns={"InvoiceDate": "cancel_date"}
    )
    pos = c[["Customer ID", "StockCode", "Quantity", "Price", "InvoiceDate", "revenue"]].copy()
    pos["Quantity"] = pos["Quantity"].astype(int)
    pos = pos.rename(columns={"InvoiceDate": "sale_date"})
    matched = pos.merge(
        canc,
        left_on=["Customer ID", "StockCode", "Quantity", "Price"],
        right_on=["Customer ID", "StockCode", "qty_abs", "Price"],
        how="inner",
    )
    matched = matched[matched["cancel_date"] > matched["sale_date"]]
    matched = matched.drop_duplicates(subset=["sale_date", "Customer ID", "StockCode", "Quantity", "Price"])
    out[name] = {
        "window": f"{start} to {end}",
        "raw_rows": int(len(w)),
        "clean_rows": int(len(c)),
        "clean_revenue": round(float(c["revenue"].sum()), 2),
        "biggest_lines": [
            {
                "invoice": str(r["Invoice"]),
                "stock_code": str(r["StockCode"]),
                "description": "" if pd.isna(r["Description"]) else str(r["Description"]),
                "quantity": int(r["Quantity"]),
                "price": float(r["Price"]),
                "date": str(r["InvoiceDate"]),
                "revenue": round(float(r["revenue"]), 2),
            }
            for _, r in big.iterrows()
        ],
        "matched_cancelled_sales_rows": int(len(matched)),
        "matched_cancelled_sales_revenue": round(float(matched["revenue"].sum()), 2),
        "matched_pct_of_clean_revenue": round(100 * float(matched["revenue"].sum()) / float(c["revenue"].sum()), 2),
        "top_products_clean": [
            {
                "stock_code": str(k),
                "description": str(g),
                "revenue": round(float(v), 2),
            }
            for (k, g), v in c.groupby(["StockCode", "Description"])["revenue"].sum().sort_values(ascending=False).head(10).items()
        ],
        "first_rows": [
            {
                "invoice": str(r["Invoice"]),
                "stock_code": str(r["StockCode"]),
                "description": "" if pd.isna(r["Description"]) else str(r["Description"]),
                "quantity": int(r["Quantity"]),
                "price": float(r["Price"]),
                "date": str(r["InvoiceDate"]),
                "customer": None if pd.isna(r["Customer ID"]) else int(r["Customer ID"]),
                "country": str(r["Country"]),
            }
            for _, r in c.head(8).iterrows()
        ],
    }
    print(name, out[name]["raw_rows"], out[name]["clean_revenue"], flush=True)

(ROOT / "_tools" / "window_check.json").write_text(json.dumps(out, indent=1, default=str))
print("written")
