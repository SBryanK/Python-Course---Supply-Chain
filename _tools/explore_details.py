"""Second-pass exploration: odd values, the two yearly sheets, and the proposed lesson slice.

Writes _tools/exploration_details.json and prints a short summary.
Run after _tools/convert_sheets.py.
"""
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT / "data" / "work"
OUT = ROOT / "_tools" / "exploration_details.json"

DATA_COLS = ["Invoice", "StockCode", "Description", "Quantity", "InvoiceDate", "Price", "Customer ID", "Country"]
raw = pd.read_csv(WORK / "online_retail_ii_with_sheet.csv", parse_dates=["InvoiceDate"])
print("loaded", raw.shape, flush=True)

out = {}

# ---------- the two yearly sheets overlap ----------
dup_mask = raw.duplicated(subset=DATA_COLS, keep=False)
dup_rows = raw[dup_mask]
out["overlap"] = {
    "duplicate_rows_total": int(raw.duplicated(subset=DATA_COLS).sum()),
    "rows_in_duplicate_groups": int(dup_mask.sum()),
    "duplicate_dates_min": str(dup_rows["InvoiceDate"].min()),
    "duplicate_dates_max": str(dup_rows["InvoiceDate"].max()),
    "duplicate_rows_by_sheet": {str(k): int(v) for k, v in dup_rows.groupby("source_sheet").size().items()},
    "duplicate_rows_all_in_dec_2010": bool(
        (dup_rows["InvoiceDate"] >= "2010-12-01").all() and (dup_rows["InvoiceDate"] <= "2010-12-10").all()
    ),
}
# rows that appear once in each sheet (exact pair across sheets)
in_s1 = raw[raw["source_sheet"] == "Year 2009-2010"]
in_s2 = raw[raw["source_sheet"] == "Year 2010-2011"]
merged = in_s1.merge(in_s2, on=DATA_COLS, how="inner")
out["overlap"]["rows_in_both_sheets"] = int(len(merged))
out["overlap"]["sheet1_dec_1_9_rows"] = int(
    ((in_s1["InvoiceDate"] >= "2010-12-01") & (in_s1["InvoiceDate"] < "2010-12-10")).sum()
)
out["overlap"]["sheet2_dec_1_9_rows"] = int(
    ((in_s2["InvoiceDate"] >= "2010-12-01") & (in_s2["InvoiceDate"] < "2010-12-10")).sum()
)
out["overlap"]["duplicates_within_sheet1"] = int(in_s1.duplicated(subset=DATA_COLS).sum())
out["overlap"]["duplicates_within_sheet2"] = int(in_s2.duplicated(subset=DATA_COLS).sum())

# ---------- the 6 'A' invoices ----------
inv = raw["Invoice"].astype(str)
a_rows = raw[inv.str.upper().str.startswith("A")]
out["a_invoices"] = {
    "rows": int(len(a_rows)),
    "detail": a_rows[DATA_COLS].astype(str).to_dict("records"),
}

# ---------- C invoice with positive quantity ----------
is_c = inv.str.upper().str.startswith("C")
odd_c = raw[is_c & (raw["Quantity"] > 0)]
out["c_positive_qty"] = {
    "rows": int(len(odd_c)),
    "detail": odd_c[DATA_COLS].astype(str).to_dict("records"),
}

# ---------- negative quantity rows without a C invoice ----------
neg_not_c = raw[~is_c & (raw["Quantity"] < 0)]
out["negative_qty_not_c"] = {
    "rows": int(len(neg_not_c)),
    "by_stock_code": {
        str(k): int(v) for k, v in neg_not_c["StockCode"].value_counts().head(20).items()
    },
    "by_description": {
        str(k): int(v) for k, v in neg_not_c["Description"].value_counts(dropna=False).head(15).items()
    },
}

# ---------- negative prices ----------
neg_price = raw[raw["Price"] < 0]
out["negative_prices"] = {
    "rows": int(len(neg_price)),
    "detail": neg_price[DATA_COLS].astype(str).to_dict("records"),
}

# ---------- zero prices ----------
zero_price = raw[raw["Price"] == 0]
out["zero_prices"] = {
    "rows": int(len(zero_price)),
    "by_stock_code": {str(k): int(v) for k, v in zero_price["StockCode"].value_counts().head(20).items()},
    "by_description": {str(k): int(v) for k, v in zero_price["Description"].value_counts(dropna=False).head(15).items()},
    "rows_with_missing_description": int(zero_price["Description"].isna().sum()),
    "rows_positive_qty": int((zero_price["Quantity"] > 0).sum()),
}

# ---------- extreme quantities ----------
big_qty = raw[raw["Quantity"].abs() > 10000]
out["extreme_quantities"] = {
    "rows_over_10000_abs": int(len(big_qty)),
    "detail": big_qty[DATA_COLS].astype(str).to_dict("records"),
}

# ---------- high prices ----------
high_price = raw[raw["Price"] > 1000]
out["high_prices"] = {
    "rows": int(len(high_price)),
    "by_stock_code": {str(k): int(v) for k, v in high_price["StockCode"].value_counts().head(15).items()},
    "detail_top": high_price.nlargest(10, "Price")[DATA_COLS].astype(str).to_dict("records"),
}

# ---------- non-product stock codes, classified by hand-visible rule ----------
code = raw["StockCode"].astype(str)
# Real products are 5 digits, optionally followed by 1-2 letters, any case.
is_product_code = code.str.match(r"^\d{5}[A-Za-z]{0,2}$")
non_product_codes = (
    raw.loc[~is_product_code]
    .groupby("StockCode", dropna=False)
    .agg(
        rows=("Quantity", "size"),
        quantity=("Quantity", "sum"),
        revenue=("Price", lambda s: 0),  # placeholder replaced below
    )
    .reset_index()
)
rev = raw.loc[~is_product_code].assign(_r=raw["Quantity"] * raw["Price"]).groupby("StockCode")["_r"].sum()
non_product_codes["revenue"] = non_product_codes["StockCode"].map(rev)
desc = raw.loc[~is_product_code].groupby("StockCode")["Description"].first()
non_product_codes["description"] = non_product_codes["StockCode"].map(desc)
non_product_codes = non_product_codes.sort_values("rows", ascending=False)
out["non_product_codes"] = {
    "rows": int((~is_product_code).sum()),
    "pct": round(100 * (~is_product_code).mean(), 2),
    "codes": [
        {
            "stock_code": str(r.StockCode),
            "description": "" if pd.isna(r.description) else str(r.description),
            "rows": int(r.rows),
            "quantity": int(r.quantity),
            "revenue": round(float(r.revenue), 2),
        }
        for r in non_product_codes.itertuples()
    ],
}

# ---------- description problems ----------
out["descriptions"] = {
    "missing_rows": int(raw["Description"].isna().sum()),
    "rows_with_trailing_space": int(raw["Description"].astype(str).str.strip().ne(raw["Description"].astype(str)).sum()),
    "unique_after_strip_lower": int(raw["Description"].astype(str).str.strip().str.upper().nunique()),
}

# ---------- stock code case variants ----------
lower_codes = code[code.str.contains(r"[a-z]")]
out["stock_code_case"] = {
    "rows_with_lowercase_code": int(len(lower_codes)),
    "example_pairs": sorted(lower_codes.unique())[:10],
}


# ---------- slice analysis ----------
def clean_steps(df):
    """The S4 cleaning, step by step, with the row count after each step."""
    steps = [("raw", len(df))]
    d = df.drop_duplicates()
    steps.append(("drop_duplicates", len(d)))
    d = d[~d["Invoice"].astype(str).str.upper().str.startswith("C")]
    steps.append(("drop_cancellations", len(d)))
    d = d[d["Quantity"] > 0]
    steps.append(("quantity_positive", len(d)))
    d = d[d["Price"] > 0]
    steps.append(("price_positive", len(d)))
    non_product = ["POST", "DOT", "M", "BANK CHARGES", "C2", "D", "S", "AMAZONFEE", "ADJUST", "CRUK", "PADS", "B", "GIFT"]
    d = d[~d["StockCode"].isin(non_product)]
    steps.append(("drop_non_products", len(d)))
    return d, steps


def analyse_slice(name, df, start, end):
    mask = (df["InvoiceDate"] >= start) & (df["InvoiceDate"] < end)
    w = df.loc[mask].copy()
    clean, steps = clean_steps(w)
    clean = clean.assign(revenue=clean["Quantity"] * clean["Price"])
    product_value = (
        clean.groupby("StockCode")["revenue"].sum().sort_values(ascending=False).reset_index()
    )
    total_revenue = product_value["revenue"].sum()
    product_value["cumulative_revenue"] = product_value["revenue"].cumsum()
    product_value["cumulative_share"] = product_value["cumulative_revenue"] / total_revenue
    product_value["abc"] = pd.cut(
        product_value["cumulative_share"], bins=[-1, 0.80, 0.95, 2], labels=["A", "B", "C"]
    )
    # pd.cut: A if <= 0.80 etc. Count and revenue share per class.
    abc = product_value.groupby("abc", observed=True).agg(
        products=("StockCode", "size"), revenue=("revenue", "sum")
    )
    abc_share = {
        str(k): {
            "products": int(r.products),
            "pct_products": round(100 * r.products / len(product_value), 1),
            "revenue": round(float(r.revenue), 2),
            "pct_revenue": round(100 * r.revenue / total_revenue, 1),
        }
        for k, r in abc.iterrows()
    }
    names_per_code = clean.groupby("StockCode")["Description"].nunique()
    top = product_value.merge(
        clean.groupby("StockCode")["Description"].first().reset_index(), on="StockCode", how="left"
    ).head(10)
    country = clean.groupby("Country")["revenue"].sum().sort_values(ascending=False)
    monthly = clean.groupby(clean["InvoiceDate"].dt.to_period("M").astype(str))["revenue"].sum()
    daily = clean.groupby(clean["InvoiceDate"].dt.date)["revenue"].sum()
    res = {
        "window": f"{start} to {end} (exclusive)",
        "source": "Year 2010-2011 sheet only",
        "raw_rows": int(len(w)),
        "date_first": str(w["InvoiceDate"].min()),
        "date_last": str(w["InvoiceDate"].max()),
        "invoices": int(w["Invoice"].astype(str).nunique()),
        "products_raw": int(w["StockCode"].nunique()),
        "countries": int(w["Country"].nunique()),
        "missing_customer_rows": int(w["Customer ID"].isna().sum()),
        "cancellation_rows": int(w["Invoice"].astype(str).str.upper().str.startswith("C").sum()),
        "steps": {k: int(v) for k, v in steps},
        "clean_rows": int(len(clean)),
        "clean_invoices": int(clean["Invoice"].astype(str).nunique()),
        "clean_products": int(clean["StockCode"].nunique()),
        "clean_customers": int(clean["Customer ID"].nunique()),
        "clean_revenue": round(float(total_revenue), 2),
        "clean_missing_customer_rows": int(clean["Customer ID"].isna().sum()),
        "top10_products": [
            {
                "stock_code": str(r.StockCode),
                "description": "" if pd.isna(r.Description) else str(r.Description),
                "revenue": round(float(r.revenue), 2),
                "pct_revenue": round(100 * r.revenue / total_revenue, 2),
            }
            for r in top.itertuples()
        ],
        "abc": abc_share,
        "top5_countries": {str(k): round(float(v), 2) for k, v in country.head(5).items()},
        "uk_share_pct": round(100 * country.get("United Kingdom", 0) / total_revenue, 2),
        "monthly_revenue": {str(k): round(float(v), 2) for k, v in monthly.items()},
        "daily_revenue": {
            "days": int(len(daily)),
            "min": round(float(daily.min()), 2),
            "max": round(float(daily.max()), 2),
            "top5": {str(k): round(float(v), 2) for k, v in daily.sort_values(ascending=False).head(5).items()},
        },
        "codes_with_multiple_names": int((names_per_code > 1).sum()),
        "lowercase_code_rows": int(w["StockCode"].astype(str).str.contains(r"[a-z]").sum()),
        "zero_price_rows": int((w["Price"] == 0).sum()),
        "negative_price_rows": int((w["Price"] < 0).sum()),
        "negative_qty_rows": int((w["Quantity"] < 0).sum()),
        "description_missing_rows": int(w["Description"].isna().sum()),
        "first_12_rows": [
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
        ],
    }
    return res


# Candidate A: Dec 2010 to Feb 2011, 2010-2011 sheet only (no cross-sheet overlap).
# Candidate B: Jan to Mar 2011, same sheet.
sheet2 = raw[raw["source_sheet"] == "Year 2010-2011"]
out["slices"] = {
    "A_dec2010_feb2011": analyse_slice("A", sheet2, "2010-12-01", "2011-03-01"),
    "B_jan2011_mar2011": analyse_slice("B", sheet2, "2011-01-01", "2011-04-01"),
}

# sanity: the first 7 quantities of sheet2 (the S2 example)
out["first_7_quantities_sheet2"] = [int(x) for x in sheet2["Quantity"].head(7).tolist()]
out["first_7_descriptions_sheet2"] = [str(x) for x in sheet2["Description"].head(7).tolist()]

OUT.write_text(json.dumps(out, indent=1, default=str))
print("written", OUT)
print(json.dumps({k: out[k] for k in ["overlap"]}, indent=1)[:2000])
