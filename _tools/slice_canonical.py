"""Canonical lesson-slice numbers for PLAN.md.

Slice: rows of the 'Year 2010-2011' sheet from 2010-12-01 to 2011-02-28.
Cleaning follows the S4 plan, plus the one cancelled giant order (invoice
541431) removed after investigation. Saves _tools/slice_canonical.json.
"""
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
raw = pd.read_csv(ROOT / "data" / "work" / "sheet_2010_2011.csv", parse_dates=["InvoiceDate"])
raw["Invoice"] = raw["Invoice"].astype(str)
raw["StockCode"] = raw["StockCode"].astype(str)

WINDOW = ("2010-12-01", "2011-03-01")
NON_PRODUCT = ["POST", "DOT", "M", "BANK CHARGES", "C2", "D", "S", "AMAZONFEE", "ADJUST", "CRUK", "PADS", "B", "GIFT"]
GIANT = "541431"

w = raw[(raw["InvoiceDate"] >= WINDOW[0]) & (raw["InvoiceDate"] < WINDOW[1])].copy()
w.to_csv(ROOT / "data" / "work" / "slice_dec2010_feb2011_raw.csv", index=False)

steps = {"raw": len(w)}
d = w.drop_duplicates()
steps["drop_duplicates"] = len(d)
d = d[~d["Invoice"].str.upper().str.startswith("C")]
steps["drop_cancellations"] = len(d)
cancelled = d[d["Invoice"].str.upper().str.startswith("C")]
d = d[d["Quantity"] > 0]
steps["quantity_positive"] = len(d)
zero_price_before = int((d["Price"] == 0).sum())
d = d[d["Price"] > 0]
steps["price_positive"] = len(d)
d = d[~d["StockCode"].isin(NON_PRODUCT)]
steps["drop_non_products"] = len(d)
d = d.copy()
d["revenue"] = d["Quantity"] * d["Price"]
giant = d[d["Invoice"] == GIANT]
steps["drop_cancelled_giant"] = len(d) - len(giant)
c = d[d["Invoice"] != GIANT].copy()
steps["clean"] = len(c)

out = {
    "slice_rule": "sheet 'Year 2010-2011', InvoiceDate in [2010-12-01, 2011-03-01)",
    "steps": steps,
    "raw_rows": int(len(w)),
    "raw_cols": int(w.shape[1]),
    "shape": [int(x) for x in w.shape],
    "clean_rows": int(len(c)),
    "clean_invoices": int(c["Invoice"].nunique()),
    "clean_products": int(c["StockCode"].nunique()),
    "clean_customers": int(c["Customer ID"].nunique()),
    "missing_customer_rows_raw": int(w["Customer ID"].isna().sum()),
    "missing_customer_rows_clean": int(c["Customer ID"].isna().sum()),
    "missing_description_rows_raw": int(w["Description"].isna().sum()),
    "description_rows_with_trailing_space_raw": int(
        (w["Description"].astype(str) != w["Description"].astype(str).str.strip()).sum()
    ),
    "cancellation_rows_raw": int(w["Invoice"].str.upper().str.startswith("C").sum()),
    "unique_cancellation_invoices_raw": int(w.loc[w["Invoice"].str.upper().str.startswith("C"), "Invoice"].nunique()),
    "duplicate_rows_raw": int(w.duplicated().sum()),
    "negative_qty_rows_raw": int((w["Quantity"] < 0).sum()),
    "negative_price_rows_raw": int((w["Price"] < 0).sum()),
    "zero_price_rows_raw": int((w["Price"] == 0).sum()),
    "zero_price_rows_after_qty_filter": zero_price_before,
    "non_product_rows_raw": int(w["StockCode"].isin(NON_PRODUCT).sum()),
    "non_product_breakdown_raw": {
        str(k): int(v) for k, v in w.loc[w["StockCode"].isin(NON_PRODUCT), "StockCode"].value_counts().items()
    },
    "germany_rows_raw": int((w["Country"] == "Germany").sum()),
    "germany_rows_clean": int((c["Country"] == "Germany").sum()),
    "countries_raw": int(w["Country"].nunique()),
    "date_first": str(w["InvoiceDate"].min()),
    "date_last": str(w["InvoiceDate"].max()),
    "revenue": round(float(c["revenue"].sum()), 2),
    "revenue_with_giant": round(float(d["revenue"].sum()), 2),
    "giant_invoice_detail": giant[["Invoice", "StockCode", "Description", "Quantity", "Price", "InvoiceDate", "Customer ID", "revenue"]].astype(str).to_dict("records")
    if len(giant) else [],
}

out["first_12_rows"] = [
    {
        "invoice": str(r["Invoice"]),
        "stock_code": str(r["StockCode"]),
        "description": "" if pd.isna(r["Description"]) else str(r["Description"]),
        "quantity": int(r["Quantity"]),
        "price": float(r["Price"]),
        "invoice_date": str(r["InvoiceDate"]),
        "customer_id": None if pd.isna(r["Customer ID"]) else int(r["Customer ID"]),
        "country": str(r["Country"]),
    }
    for r in w.head(12).to_dict("records")
]
first7 = w.head(7)
out["first_7_quantities"] = [int(x) for x in first7["Quantity"].tolist()]
out["first_7_prices"] = [float(x) for x in first7["Price"].tolist()]
out["first_7_descriptions"] = [str(x) for x in first7["Description"].tolist()]
out["first_7_sum"] = int(first7["Quantity"].sum())
out["first_7_len"] = int(len(first7))
out["first_7_min"] = int(first7["Quantity"].min())
out["first_7_max"] = int(first7["Quantity"].max())

# Product value and ABC on the canonical clean table.
pv = c.groupby("StockCode")["revenue"].sum().sort_values(ascending=False).reset_index()
pv["cum"] = pv["revenue"].cumsum()
pv["cum_share"] = pv["cum"] / pv["revenue"].sum()


def abc(share):
    if share <= 0.80:
        return "A"
    if share <= 0.95:
        return "B"
    return "C"


pv["abc"] = pv["cum_share"].apply(abc)
names = c.groupby("StockCode")["Description"].first()
pv["description"] = pv["StockCode"].map(names)
total = float(pv["revenue"].sum())
cls = pv.groupby("abc").agg(products=("StockCode", "size"), revenue=("revenue", "sum"))
out["abc"] = {
    str(k): {
        "products": int(r.products),
        "pct_products": round(100 * r.products / len(pv), 1),
        "revenue": round(float(r.revenue), 2),
        "pct_revenue": round(100 * r.revenue / total, 2),
    }
    for k, r in cls.iterrows()
}
out["product_count"] = int(len(pv))
out["top15_products"] = [
    {
        "rank": i + 1,
        "stock_code": str(r.StockCode),
        "description": "" if pd.isna(r.description) else str(r.description),
        "revenue": round(float(r.revenue), 2),
        "pct_revenue": round(100 * r.revenue / total, 2),
        "cumulative_share": round(float(r.cum_share), 4),
        "abc": r.abc,
    }
    for i, r in enumerate(pv.head(15).itertuples())
]
out["cumulative_share_first_10"] = [round(float(x), 4) for x in pv["cum_share"].head(10).tolist()]
out["codes_with_multiple_names"] = int((c.groupby("StockCode")["Description"].nunique() > 1).sum())
out["lowercase_code_rows"] = int(c["StockCode"].str.contains(r"[a-z]").sum())
out["duplicate_invoice_stockcode_rows"] = int(c.duplicated(subset=["Invoice", "StockCode"]).sum())

# Country revenue.
country = c.groupby("Country")["revenue"].sum().sort_values(ascending=False)
out["top5_countries"] = {str(k): round(float(v), 2) for k, v in country.head(5).items()}
out["uk_share_pct"] = round(100 * float(country.get("United Kingdom", 0)) / total, 2)

# Monthly revenue.
monthly = c.groupby(c["InvoiceDate"].dt.to_period("M").astype(str))["revenue"].sum()
out["monthly_revenue"] = {str(k): round(float(v), 2) for k, v in monthly.items()}

# Daily revenue.
daily = c.groupby(c["InvoiceDate"].dt.date)["revenue"].sum()
out["daily_days"] = int(len(daily))
out["daily_min"] = round(float(daily.min()), 2)
out["daily_max"] = round(float(daily.max()), 2)
out["daily_max_day"] = str(daily.idxmax())
out["daily_top5"] = {str(k): round(float(v), 2) for k, v in daily.sort_values(ascending=False).head(5).items()}
out["daily_first_10"] = {str(k): round(float(v), 2) for k, v in daily.head(10).items()}

# What-if: cleaning without the giant-order removal (for the answer key discussion).
out["revenue_if_giant_kept"] = round(float(d["revenue"].sum()), 2)
pv2 = d.groupby("StockCode")["revenue"].sum().sort_values(ascending=False)
out["top5_products_if_giant_kept"] = [
    {"stock_code": str(k), "revenue": round(float(v), 2), "pct": round(100 * float(v) / float(d["revenue"].sum()), 2)}
    for k, v in pv2.head(5).items()
]

(ROOT / "_tools" / "slice_canonical.json").write_text(json.dumps(out, indent=1, default=str))
print(json.dumps(out, indent=1, default=str)[:9000])
