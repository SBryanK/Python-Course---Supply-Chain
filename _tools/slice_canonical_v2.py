"""Final canonical slice numbers with the corrected non-product rule.

Rule: a row is a product row when the first character of its stock code is a
digit. This removes postage, fees, samples, discounts, manual lines, gift
vouchers and old DCGS catalogue codes in one line, and is what the S4 notebook
will teach.

Writes _tools/slice_canonical_v2.json (and the alt window check).
"""
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sheet2 = pd.read_csv(ROOT / "data" / "work" / "sheet_2010_2011.csv", parse_dates=["InvoiceDate"])
sheet2["Invoice"] = sheet2["Invoice"].astype(str)
sheet2["StockCode"] = sheet2["StockCode"].astype(str)


def analyse(start, end, giant="541431", giant_decision="remove"):
    w = sheet2[(sheet2["InvoiceDate"] >= start) & (sheet2["InvoiceDate"] < end)].copy()
    steps = {"raw": len(w)}
    d = w.drop_duplicates()
    steps["drop_duplicates"] = len(d)
    d = d[~d["Invoice"].str.upper().str.startswith("C")]
    steps["drop_cancellations"] = len(d)
    canc = d[d["Invoice"].str.upper().str.startswith("C")]
    d = d[d["Quantity"] > 0]
    steps["quantity_positive"] = len(d)
    zero_price = int((d["Price"] == 0).sum())
    d = d[d["Price"] > 0]
    steps["price_positive"] = len(d)
    first_char = d["StockCode"].str[0]
    is_product = first_char.str.isdigit()
    non_product_rows_here = int((~is_product).sum())
    d = d[is_product]
    steps["drop_non_products"] = len(d)
    d = d.copy()
    d["revenue"] = d["Quantity"] * d["Price"]
    giant_row = d[d["Invoice"] == giant]
    steps["drop_cancelled_giant"] = len(d) - len(giant_row)
    c = d[d["Invoice"] != giant].copy()
    steps["clean"] = len(c)
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
    country = c.groupby("Country")["revenue"].sum().sort_values(ascending=False)
    monthly = c.groupby(c["InvoiceDate"].dt.to_period("M").astype(str))["revenue"].sum()
    daily = c.groupby(c["InvoiceDate"].dt.date)["revenue"].sum()
    return {
        "window": f"{start} to {end}",
        "steps": {k: int(v) for k, v in steps.items()},
        "raw_rows": int(len(w)),
        "date_first": str(w["InvoiceDate"].min()),
        "date_last": str(w["InvoiceDate"].max()),
        "missing_customer_raw": int(w["Customer ID"].isna().sum()),
        "missing_description_raw": int(w["Description"].isna().sum()),
        "cancellation_rows_raw": int(w["Invoice"].str.upper().str.startswith("C").sum()),
        "unique_cancellation_invoices_raw": int(canc["Invoice"].nunique()),
        "duplicates_raw": int(w.duplicated().sum()),
        "negative_qty_raw": int((w["Quantity"] < 0).sum()),
        "zero_price_raw": int((w["Price"] == 0).sum()),
        "zero_price_before_price_filter": zero_price,
        "non_product_rows_raw": int((~w["StockCode"].str[0].str.isdigit()).sum()),
        "non_product_rows_at_filter": non_product_rows_here,
        "countries_raw": int(w["Country"].nunique()),
        "invoices_raw": int(w["Invoice"].nunique()),
        "products_raw": int(w["StockCode"].nunique()),
        "germany_raw": int((w["Country"] == "Germany").sum()),
        "clean_rows": int(len(c)),
        "clean_invoices": int(c["Invoice"].nunique()),
        "clean_products": int(c["StockCode"].nunique()),
        "clean_customers": int(c["Customer ID"].nunique()),
        "clean_missing_customer": int(c["Customer ID"].isna().sum()),
        "revenue": round(total, 2),
        "germany_clean": int((c["Country"] == "Germany").sum()),
        "abc": {
            str(k): {
                "products": int(r.products),
                "pct_products": round(100 * r.products / len(pv), 1),
                "revenue": round(float(r.revenue), 2),
                "pct_revenue": round(100 * r.revenue / total, 2),
            }
            for k, r in cls.iterrows()
        },
        "top10_products": [
            {
                "rank": i + 1,
                "stock_code": str(r.StockCode),
                "description": "" if pd.isna(r.description) else str(r.description),
                "revenue": round(float(r.revenue), 2),
                "pct_revenue": round(100 * r.revenue / total, 2),
                "cum_share": round(float(r.cum_share), 4),
            }
            for i, r in enumerate(pv.head(10).itertuples())
        ],
        "top10_cum_share": round(float(pv["cum_share"].head(10).iloc[-1]), 4),
        "top5_countries": {str(k): round(float(v), 2) for k, v in country.head(5).items()},
        "uk_share_pct": round(100 * float(country.get("United Kingdom", 0)) / total, 2),
        "monthly": {str(k): round(float(v), 2) for k, v in monthly.items()},
        "daily": {
            "days": int(len(daily)),
            "min": round(float(daily.min()), 2),
            "max": round(float(daily.max()), 2),
            "max_day": str(daily.idxmax()),
            "top5": {str(k): round(float(v), 2) for k, v in daily.sort_values(ascending=False).head(5).items()},
        },
        "codes_with_multiple_names": int((c.groupby("StockCode")["Description"].nunique() > 1).sum()),
        "lowercase_code_rows": int(c["StockCode"].str.contains(r"[a-z]").sum()),
        "product_names_rows": int(c[["StockCode", "Description"]].drop_duplicates(subset="StockCode").shape[0]),
        "first7_qty": [int(x) for x in w.head(7)["Quantity"].tolist()],
        "first7_desc": [str(x) for x in w.head(7)["Description"].tolist()],
        "first12": [
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
            for r in w.head(12).to_dict("records")
        ],
        "giant_rows": giant_row[["Invoice", "StockCode", "Description", "Quantity", "Price", "InvoiceDate", "Customer ID"]].astype(str).to_dict("records"),
    }


out = {
    "main": analyse("2010-12-01", "2011-03-01"),
    "alt_feb_apr": analyse("2011-02-01", "2011-05-01"),
}
(ROOT / "_tools" / "slice_canonical_v2.json").write_text(json.dumps(out, indent=1, default=str))
m = out["main"]
print(json.dumps({k: m[k] for k in ["steps", "raw_rows", "clean_rows", "clean_invoices", "clean_products", "clean_customers", "revenue", "abc", "top10_products", "top10_cum_share", "top5_countries", "uk_share_pct", "monthly", "daily", "germany_raw", "germany_clean", "non_product_rows_raw", "non_product_rows_at_filter", "codes_with_multiple_names", "lowercase_code_rows", "product_names_rows", "missing_customer_raw", "missing_description_raw", "cancellation_rows_raw", "duplicates_raw"]}, indent=1, default=str))
print("ALT:", json.dumps({k: out["alt_feb_apr"][k] for k in ["steps", "clean_rows", "revenue", "non_product_rows_raw", "non_product_rows_at_filter"]}, indent=1))
