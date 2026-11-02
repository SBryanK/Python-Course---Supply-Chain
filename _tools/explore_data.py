"""Explore UCI Online Retail II and record every fact the course needs.

Writes data/work/online_retail_ii.csv (faithful conversion of both sheets)
and _tools/exploration_stats.json (all numbers used in EXPLORATION.md).
"""
import json
import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw" / "online_retail_II.xlsx"
WORK = ROOT / "data" / "work"
WORK.mkdir(parents=True, exist_ok=True)
OUT = ROOT / "_tools" / "exploration_stats.json"

SHEETS = ["Year 2009-2010", "Year 2010-2011"]
stats = {}

print("reading xlsx ...", flush=True)
parts = []
for sheet in SHEETS:
    df = pd.read_excel(RAW, sheet_name=sheet)
    df["source_sheet"] = sheet
    parts.append(df)
    s = {
        "rows": int(len(df)),
        "date_min": str(df["InvoiceDate"].min()),
        "date_max": str(df["InvoiceDate"].max()),
        "dtypes": {c: str(t) for c, t in df.dtypes.items()},
        "missing": {c: int(df[c].isna().sum()) for c in df.columns},
    }
    stats[sheet] = s
    print(sheet, df.shape, flush=True)

raw = pd.concat(parts, ignore_index=True)
print("combined", raw.shape, flush=True)

# Faithful CSV conversion, both years, without helper columns.
raw.drop(columns=["source_sheet"]).to_csv(WORK / "online_retail_ii.csv", index=False)
print("csv written", flush=True)

# ---------- overview ----------
stats["combined"] = {
    "rows": int(len(raw)),
    "columns": list(raw.columns),
    "date_min": str(raw["InvoiceDate"].min()),
    "date_max": str(raw["InvoiceDate"].max()),
    "memory_mb": round(raw.memory_usage(deep=True).sum() / 1024**2, 1),
    "missing": {c: int(raw[c].isna().sum()) for c in raw.columns if c != "source_sheet"},
    "missing_pct": {c: round(100 * raw[c].isna().mean(), 2) for c in raw.columns if c != "source_sheet"},
}
inv_str = raw["Invoice"].astype(str)
stats["combined"]["invoice_dtype"] = str(raw["Invoice"].dtype)
stats["combined"]["unique_invoices"] = int(inv_str.nunique())
stats["combined"]["unique_customers"] = int(raw["Customer ID"].nunique())
stats["combined"]["unique_countries"] = int(raw["Country"].nunique())
stats["combined"]["unique_products"] = int(raw["StockCode"].nunique())
stats["combined"]["unique_descriptions"] = int(raw["Description"].nunique())

# ---------- cancellations ----------
is_c = inv_str.str.upper().str.startswith("C")
stats["cancellations"] = {
    "rows_c_invoice": int(is_c.sum()),
    "pct_rows": round(100 * is_c.mean(), 2),
    "unique_c_invoices": int(inv_str[is_c].nunique()),
    "rows_c_positive_qty": int((is_c & (raw["Quantity"] > 0)).sum()),
    "rows_c_nonnegative_qty": int((is_c & (raw["Quantity"] >= 0)).sum()),
    "rows_not_c_negative_qty": int((~is_c & (raw["Quantity"] < 0)).sum()),
    "rows_not_c_zero_qty": int((~is_c & (raw["Quantity"] == 0)).sum()),
    "c_invoice_examples": inv_str[is_c].unique()[:10].tolist(),
}
other_prefix = inv_str.str.upper().str[0]
prefix_rows = other_prefix.value_counts().head(15)
stats["cancellations"]["invoice_first_char_rows"] = {str(k): int(v) for k, v in prefix_rows.items()}

# ---------- quantities ----------
q = raw["Quantity"]
stats["quantity"] = {
    "min": int(q.min()),
    "max": int(q.max()),
    "mean": round(float(q.mean()), 2),
    "median": float(q.median()),
    "negative_rows": int((q < 0).sum()),
    "zero_rows": int((q == 0).sum()),
    "positive_rows": int((q > 0).sum()),
    "rows_over_1000": int((q > 1000).sum()),
    "rows_over_10000": int((q > 10000).sum()),
    "largest_values": q.nlargest(10).tolist(),
    "most_negative_values": q.nsmallest(10).tolist(),
}

# ---------- prices ----------
p = raw["Price"]
stats["price"] = {
    "min": float(p.min()),
    "max": float(p.max()),
    "mean": round(float(p.mean()), 4),
    "median": float(p.median()),
    "negative_rows": int((p < 0).sum()),
    "zero_rows": int((p == 0).sum()),
    "rows_under_0_01": int((p < 0.01).sum()),
    "rows_over_100": int((p > 100).sum()),
    "rows_over_1000": int((p > 1000).sum()),
    "largest_values": p.nlargest(10).tolist(),
    "negative_rows_by_sheet": raw.loc[p < 0].groupby("source_sheet").size().to_dict(),
}
stats["price"]["negative_rows_by_sheet"] = {str(k): int(v) for k, v in stats["price"]["negative_rows_by_sheet"].items()}

# ---------- duplicates ----------
stats["duplicates"] = {
    "exact_duplicate_rows": int(raw.drop(columns=["source_sheet"]).duplicated().sum()),
    "exact_duplicate_groups": int(raw.drop(columns=["source_sheet"]).duplicated(keep=False).sum()),
    "business_key_duplicates": int(
        raw.duplicated(subset=["Invoice", "StockCode", "Quantity", "Price", "InvoiceDate"]).sum()
    ),
}

# ---------- revenue ----------
raw["_revenue"] = raw["Quantity"] * raw["Price"]
stats["revenue"] = {
    "total": round(float(raw["_revenue"].sum()), 2),
    "positive_only": round(float(raw.loc[raw["_revenue"] > 0, "_revenue"].sum()), 2),
    "negative_rows": int((raw["_revenue"] < 0).sum()),
    "negative_sum": round(float(raw.loc[raw["_revenue"] < 0, "_revenue"].sum()), 2),
}

# ---------- countries ----------
country_counts = raw["Country"].value_counts()
stats["countries"] = {
    "top15_rows": {str(k): int(v) for k, v in country_counts.head(15).items()},
    "uk_share_pct": round(100 * (raw["Country"] == "United Kingdom").mean(), 2),
    "n_countries": int(raw["Country"].nunique()),
}

# ---------- stock codes that are not products ----------
code = raw["StockCode"].astype(str)
product_pattern = re.compile(r"^\d{5}[A-Z]?$")
is_product_code = code.str.match(product_pattern)
non_product = (
    raw.loc[~is_product_code]
    .groupby(["StockCode", "Description"], dropna=False)
    .agg(rows=("Quantity", "size"), quantity=("Quantity", "sum"), revenue=("_revenue", "sum"))
    .reset_index()
    .sort_values("rows", ascending=False)
)
stats["stock_codes"] = {
    "rows_matching_5digit_pattern": int(is_product_code.sum()),
    "rows_not_matching_pattern": int((~is_product_code).sum()),
    "pct_not_matching": round(100 * (~is_product_code).mean(), 2),
    "non_product_breakdown": [
        {
            "stock_code": str(r.StockCode),
            "description": "" if pd.isna(r.Description) else str(r.Description),
            "rows": int(r.rows),
            "quantity": int(r.quantity),
            "revenue": round(float(r.revenue), 2),
        }
        for r in non_product.head(40).itertuples()
    ],
    "codes_with_letters": {str(k): int(v) for k, v in code[~is_product_code].value_counts().head(40).items()},
}

# ---------- missing descriptions ----------
desc_missing = raw["Description"].isna()
stats["missing_description"] = {
    "rows": int(desc_missing.sum()),
    "by_sheet": {str(k): int(v) for k, v in raw.loc[desc_missing].groupby("source_sheet").size().items()},
    "stock_codes": {str(k): int(v) for k, v in raw.loc[desc_missing, "StockCode"].value_counts().head(15).items()},
    "c_invoice_rows": int((desc_missing & is_c).sum()),
}

# ---------- missing customer ----------
cust_missing = raw["Customer ID"].isna()
stats["missing_customer"] = {
    "rows": int(cust_missing.sum()),
    "pct": round(100 * cust_missing.mean(), 2),
    "negative_qty_rows": int((cust_missing & (raw["Quantity"] < 0)).sum()),
    "revenue": round(float(raw.loc[cust_missing, "_revenue"].sum()), 2),
}

# ---------- monthly rows and revenue ----------
month = raw["InvoiceDate"].dt.to_period("M").astype(str)
monthly = raw.groupby(month).agg(rows=("Invoice", "size"), revenue=("_revenue", "sum"))
stats["monthly"] = {
    str(k): {"rows": int(v["rows"]), "revenue": round(float(v["revenue"]), 2)} for k, v in monthly.iterrows()
}

# ---------- candidate lesson windows ----------
windows = {
    "2010_full_year": ("2010-01-01", "2010-12-31"),
    "2010_dec_2011_feb": ("2010-12-01", "2011-02-28"),
    "2011_jan_mar": ("2011-01-01", "2011-03-31"),
    "2011_jan_jun": ("2011-01-01", "2011-06-30"),
    "2011_dec_only": ("2011-12-01", "2011-12-09"),
}
stats["candidate_windows"] = {}
for name, (start, end) in windows.items():
    mask = (raw["InvoiceDate"] >= start) & (raw["InvoiceDate"] < pd.Timestamp(end) + pd.Timedelta(days=1))
    w = raw.loc[mask]
    stats["candidate_windows"][name] = {
        "rows": int(len(w)),
        "products": int(w["StockCode"].nunique()),
        "invoices": int(w["Invoice"].astype(str).nunique()),
        "countries": int(w["Country"].nunique()),
        "cancellation_rows": int(w["Invoice"].astype(str).str.upper().str.startswith("C").sum()),
        "missing_customer_rows": int(w["Customer ID"].isna().sum()),
        "revenue_all": round(float((w["Quantity"] * w["Price"]).sum()), 2),
        "csv_mb_estimate": round(len(w) * 0.115 / 1024, 2),
    }

# ---------- product examples for lessons ----------
# First rows of the 2010-2011 sheet: the story the brief opens with.
head_rows = raw[raw["source_sheet"] == "Year 2010-2011"].head(12)
stats["lesson_examples"] = {
    "first_rows_2010_2011": [
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
        for r in head_rows.to_dict("records")
    ],
    "top10_products_by_revenue_2011": [],
}

# Top products in the chosen example window (2011 Jan-Mar), uncleaned, by revenue.
mask = (raw["InvoiceDate"] >= "2011-01-01") & (raw["InvoiceDate"] < "2011-04-01")
w = raw.loc[mask]
top = (
    w.groupby(["StockCode", "Description"], dropna=False)
    .agg(rows=("Quantity", "size"), quantity=("Quantity", "sum"), revenue=("_revenue", "sum"))
    .reset_index()
    .sort_values("revenue", ascending=False)
    .head(15)
)
stats["lesson_examples"]["top15_products_2011_q1_uncleaned"] = [
    {
        "stock_code": str(r.StockCode),
        "description": "" if pd.isna(r.Description) else str(r.Description),
        "rows": int(r.rows),
        "quantity": int(r.quantity),
        "revenue": round(float(r.revenue), 2),
    }
    for r in top.itertuples()
]

# Number of rows after a plain S4-style clean on the example window, to size exercises.
def clean(df):
    d = df.copy()
    d = d.drop_duplicates()
    d = d[~d["Invoice"].astype(str).str.upper().str.startswith("C")]
    d = d[d["Quantity"] > 0]
    d = d[d["Price"] > 0]
    return d

w_clean = clean(w)
stats["lesson_examples"]["clean_rows_2011_q1"] = {
    "raw_rows": int(len(w)),
    "clean_rows": int(len(w_clean)),
    "removed_rows": int(len(w) - len(w_clean)),
    "products_clean": int(w_clean["StockCode"].nunique()),
    "revenue_clean": round(float((w_clean["Quantity"] * w_clean["Price"]).sum()), 2),
}

OUT.write_text(json.dumps(stats, indent=2, default=str))
print("stats written to", OUT, flush=True)
