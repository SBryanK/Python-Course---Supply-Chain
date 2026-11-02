"""Independent verification of Phase 1 facts, computed from the raw UCI xlsx.

Source: _verify/raw_sheets.pkl produced by _verify/load_raw.py from
data/raw/online_retail_II.xlsx (two sheets, Invoice/StockCode read as text).
No pre-existing JSON/CSV files are used.
"""
import json
import os
import re

os.environ.setdefault("MPLCONFIGDIR", os.path.abspath("_tools/mplconfig"))

import numpy as np
import pandas as pd

pd.set_option("display.max_columns", 50)
pd.set_option("display.width", 250)
pd.set_option("display.max_rows", 200)

RAW = "data/raw/online_retail_II.xlsx"
data = pd.read_pickle("_verify/raw_sheets.pkl")
S1_NAME, S2_NAME = "Year 2009-2010", "Year 2010-2011"
df1, df2 = data[S1_NAME].copy(), data[S2_NAME].copy()

COLS = [
    "Invoice",
    "StockCode",
    "Description",
    "Quantity",
    "InvoiceDate",
    "Price",
    "Customer ID",
    "Country",
]
for d in (df1, df2):
    d.columns = [str(c).strip() for c in d.columns]
assert list(df1.columns) == COLS, df1.columns.tolist()
assert list(df2.columns) == COLS, df2.columns.tolist()

R = {}  # results dict
lines = []


def sec(title):
    lines.append("")
    lines.append("=" * 78)
    lines.append(title)
    lines.append("=" * 78)


def rec(key, value):
    R[key] = value
    lines.append(f"{key}: {value}")


def show(label, obj):
    lines.append(f"--- {label} ---")
    lines.append(obj.to_string() if isinstance(obj, (pd.Series, pd.DataFrame)) else str(obj))


combo = pd.concat([df1, df2], ignore_index=True)


def topy(x):
    if isinstance(x, (np.integer,)):
        return int(x)
    if isinstance(x, (np.floating,)):
        return float(x)
    if isinstance(x, (pd.Timestamp,)):
        return x.isoformat()
    if isinstance(x, np.bool_):
        return bool(x)
    return x


# ------------------------------------------------------------------ item 1
sec("ITEM 1: rows per sheet, total, date ranges")
n1, n2 = len(df1), len(df2)
rec("sheet1_rows", n1)
rec("sheet2_rows", n2)
rec("total_rows", len(combo))
for name, d in [(S1_NAME, df1), (S2_NAME, df2)]:
    rec(f"{name} min_date", d["InvoiceDate"].min())
    rec(f"{name} max_date", d["InvoiceDate"].max())
    rec(f"{name} n_null_invoicedate", int(d["InvoiceDate"].isna().sum()))
rec("combined_min_date", combo["InvoiceDate"].min())
rec("combined_max_date", combo["InvoiceDate"].max())

# cross-check sheet row counts via openpyxl dimensions only
import openpyxl

wb = openpyxl.load_workbook(RAW, read_only=True)
rec(
    "openpyxl_max_row_by_sheet",
    {s: wb[s].max_row for s in wb.sheetnames},
)
rec("openpyxl_sheetnames", wb.sheetnames)
wb.close()

# ------------------------------------------------------------------ item 2
sec("ITEM 2: missing counts and dtypes (combined)")
miss = combo.isna().sum()
show("missing per column", miss)
R["missing_counts"] = {c: int(miss[c]) for c in COLS}
R["missing_pct"] = {c: round(float(miss[c]) / len(combo) * 100, 4) for c in COLS}
show("dtypes combined", combo.dtypes.astype(str))
R["dtypes"] = {c: str(combo[c].dtype) for c in COLS}
# per sheet for Invoice/StockCode type detail
R["dtypes_sheet1"] = {c: str(df1[c].dtype) for c in COLS}
R["dtypes_sheet2"] = {c: str(df2[c].dtype) for c in COLS}
lines.append(f"Invoice dtype sheet1={df1['Invoice'].dtype} sheet2={df2['Invoice'].dtype}")
lines.append(f"StockCode dtype sheet1={df1['StockCode'].dtype} sheet2={df2['StockCode'].dtype}")
R["invoice_dtype"] = {"sheet1": str(df1["Invoice"].dtype), "sheet2": str(df2["Invoice"].dtype)}
R["stockcode_dtype"] = {"sheet1": str(df1["StockCode"].dtype), "sheet2": str(df2["StockCode"].dtype)}

# ------------------------------------------------------------------ item 3
sec("ITEM 3: cancellation rows")
inv = combo["Invoice"].astype(str)
is_c = inv.str.upper().str.startswith("C")
rec("c_rows", int(is_c.sum()))
rec("c_unique_invoices", int(inv[is_c].nunique()))
rec("c_rows_qty_ge_0", int((is_c & (combo["Quantity"] >= 0)).sum()))
rec("nonc_rows_qty_lt_0", int((~is_c & (combo["Quantity"] < 0)).sum()))
# per sheet
for name, d in [(S1_NAME, df1), (S2_NAME, df2)]:
    i = d["Invoice"].astype(str).str.upper().str.startswith("C")
    rec(f"{name}: c_rows", int(i.sum()))
    rec(f"{name}: c_unique_invoices", int(d["Invoice"].astype(str)[i].nunique()))
show("C rows with Quantity >= 0", combo[is_c & (combo["Quantity"] >= 0)][COLS])
nonc_neg = combo[~is_c & (combo["Quantity"] < 0)]
show("non-C rows with Quantity < 0 (count=" + str(len(nonc_neg)) + ")", nonc_neg[COLS])
R["nonc_neg_qty_rows"] = len(nonc_neg)

# ------------------------------------------------------------------ item 4
sec("ITEM 4: price / quantity extremes")
negp = combo[combo["Price"] < 0]
show(f"negative price rows (count={len(negp)})", negp[COLS])
R["negative_price_rows"] = len(negp)
R["negative_price_detail"] = [
    {c: topy(r[c]) for c in COLS} for _, r in negp.iterrows()
]
zero_p = combo[combo["Price"] == 0]
rec("zero_price_rows", len(zero_p))
rec("price_gt_1000_rows", int((combo["Price"] > 1000).sum()))
show("price > 1000 rows", combo[combo["Price"] > 1000][COLS])
bigq = combo[combo["Quantity"].abs() > 10000]
show(f"abs(Quantity) > 10000 rows (count={len(bigq)})", bigq[COLS])
R["abs_qty_gt_10000_rows"] = len(bigq)
R["abs_qty_gt_10000_detail"] = [
    {c: topy(r[c]) for c in COLS} for _, r in bigq.iterrows()
]
# extra sanity: exact zero-quantity rows
rec("qty_eq_0_rows", int((combo["Quantity"] == 0).sum()))

# ------------------------------------------------------------------ item 5
sec("ITEM 5: exact duplicates when stacked; Dec 2010 overlap")
dup_mask = combo.duplicated(subset=COLS, keep="first")
rec("stacked_duplicate_rows", int(dup_mask.sum()))
rec("stacked_unique_rows", int(len(combo) - dup_mask.sum()))
show("sample duplicated rows", combo[dup_mask].head(10)[COLS])
rec("dup_within_sheet1", int(df1.duplicated(subset=COLS, keep="first").sum()))
rec("dup_within_sheet2", int(df2.duplicated(subset=COLS, keep="first").sum()))

start = pd.Timestamp("2010-12-01")
end_excl = pd.Timestamp("2010-12-10")  # "to 2010-12-09" inclusive
o1 = df1[(df1["InvoiceDate"] >= start) & (df1["InvoiceDate"] < end_excl)]
o2 = df2[(df2["InvoiceDate"] >= start) & (df2["InvoiceDate"] < end_excl)]
rec("overlap_sheet1_rows", len(o1))
rec("overlap_sheet1_min", o1["InvoiceDate"].min())
rec("overlap_sheet1_max", o1["InvoiceDate"].max())
rec("overlap_sheet2_rows", len(o2))
rec("overlap_sheet2_min", o2["InvoiceDate"].min())
rec("overlap_sheet2_max", o2["InvoiceDate"].max())


def distinct_row_set(d):
    d = d[COLS].copy()
    for c in COLS:
        if d[c].dtype == object:
            d[c] = d[c].apply(lambda v: "<NA>" if pd.isna(v) else str(v))
    return set(map(tuple, d.itertuples(index=False, name=None)))


set1, set2 = distinct_row_set(o1), distinct_row_set(o2)
rec("overlap_sheet1_distinct_rows", len(set1))
rec("overlap_sheet2_distinct_rows", len(set2))
rec("overlap_rows_shared_distinct", len(set1 & set2))
rec("overlap_sheet1_distinct_only", len(set1 - set2))
rec("overlap_sheet2_distinct_only", len(set2 - set1))
# within-sheet dup in the overlap window
rec("overlap_sheet1_dup_rows", int(o1.duplicated(subset=COLS, keep="first").sum()))
rec("overlap_sheet2_dup_rows", int(o2.duplicated(subset=COLS, keep="first").sum()))
# date coverage checks
rec("sheet1_last_invoice_date", df1["InvoiceDate"].max())
rec("sheet2_first_invoice_date", df2["InvoiceDate"].min())

# ------------------------------------------------------------------ item 6
sec("ITEM 6: non-product stock codes")
PRODUCT_RE = re.compile(r"^\d{5}[A-Za-z]{0,2}$", re.ASCII)
sc = combo["StockCode"].astype(str)
is_prod = sc.apply(lambda s: bool(PRODUCT_RE.fullmatch(s)))
rec("real_product_rows", int(is_prod.sum()))
rec("non_product_rows", int((~is_prod).sum()))
nonprod = (
    combo.loc[~is_prod]
    .groupby(combo.loc[~is_prod, "StockCode"].astype(str), dropna=False)
    .size()
    .sort_values(ascending=False)
)
show(f"non-product codes with row counts (n_codes={len(nonprod)})", nonprod)
R["non_product_code_counts"] = {str(k): int(v) for k, v in nonprod.items()}
rec("non_product_code_count", len(nonprod))
# rows whose StockCode is missing
rec("stockcode_missing_rows", int(combo["StockCode"].isna().sum()))
# raw StockCode form check (spaces etc.)
suspicious = [s for s in sc.dropna().unique() if s != s.strip()]
rec("stockcodes_with_outer_spaces", suspicious[:20])

# ------------------------------------------------------------------ item 7
sec("ITEM 7: A-prefix invoices")
inv_str = combo["Invoice"].astype(str)
a_mask = inv_str.str.upper().str.startswith("A")
rec("a_invoice_rows", int(a_mask.sum()))
rec("a_unique_invoices", int(inv_str[a_mask].nunique()))
show("A-prefix invoice rows", combo[a_mask][COLS])
show("A-prefix invoice numbers", inv_str[a_mask].value_counts())
R["a_invoice_numbers"] = {str(k): int(v) for k, v in inv_str[a_mask].value_counts().items()}
# other non-numeric invoice prefixes for context
pref = inv_str.str.extract(r"^([A-Za-z]+)")[0].dropna().value_counts()
show("non-numeric invoice prefixes (context)", pref)

# ------------------------------------------------------------------ item 8
sec("ITEM 8: lesson slice (sheet2, 2010-12-01 <= InvoiceDate < 2011-03-01)")
s_start = pd.Timestamp("2010-12-01")
s_end = pd.Timestamp("2011-03-01")
slice_df = df2[(df2["InvoiceDate"] >= s_start) & (df2["InvoiceDate"] < s_end)].copy()
rec("slice_rows_raw", len(slice_df))
rec("slice_columns", list(slice_df.columns))
rec("slice_min_date", slice_df["InvoiceDate"].min())
rec("slice_max_date", slice_df["InvoiceDate"].max())
rec("slice_missing_customer_id", int(slice_df["Customer ID"].isna().sum()))
rec("slice_missing_description", int(slice_df["Description"].isna().sum()))
sl_inv = slice_df["Invoice"].astype(str)
sl_c = sl_inv.str.upper().str.startswith("C")
rec("slice_cancellation_rows", int(sl_c.sum()))
rec("slice_duplicate_rows", int(slice_df.duplicated(subset=COLS, keep="first").sum()))
sl_sc = slice_df["StockCode"].astype(str)
sl_prod = sl_sc.apply(lambda s: bool(PRODUCT_RE.fullmatch(s)))
rec("slice_non_product_rows", int((~sl_prod).sum()))
sl_nonprod = (
    slice_df.loc[~sl_prod]
    .groupby(sl_sc[~sl_prod])
    .size()
    .sort_values(ascending=False)
)
show("slice non-product codes with counts", sl_nonprod)

cur = slice_df.copy()
steps = []
steps.append(("start", len(cur)))
cur = cur.drop_duplicates(subset=COLS, keep="first")
steps.append(("drop_duplicates", len(cur)))
cur = cur[~cur["Invoice"].astype(str).str.upper().str.startswith("C")]
steps.append(("remove C invoices", len(cur)))
cur = cur[cur["Quantity"] > 0]
steps.append(("Quantity > 0", len(cur)))
cur = cur[cur["Price"] > 0]
steps.append(("Price > 0", len(cur)))
NONPROD_CODES = ["POST", "DOT", "M", "S", "C2", "D", "BANK CHARGES", "AMAZONFEE"]
cur_sc = cur["StockCode"].astype(str)
removed = cur[cur_sc.isin(NONPROD_CODES)]
show("rows removed by non-product code filter (with codes)", removed[COLS])
cur = cur[~cur_sc.isin(NONPROD_CODES)]
steps.append(("remove listed non-product codes", len(cur)))
before_541431 = len(cur)
cur = cur[cur["Invoice"].astype(str) != "541431"]
steps.append(("remove invoice 541431", len(cur)))
R["lesson_steps"] = [(s, int(n)) for s, n in steps]
rec("rows_removed_by_541431", before_541431 - len(cur))
for s, n in steps:
    lines.append(f"step {s}: {n}")
show("removed invoice 541431 rows", slice_df[slice_df["Invoice"].astype(str) == "541431"][COLS])
# remaining non-product codes after the exact cleaning sequence
clean_sc = cur["StockCode"].astype(str)
rem_prod = clean_sc.apply(lambda s: bool(PRODUCT_RE.fullmatch(s)))
rec("clean_non_product_rows_remaining", int((~rem_prod).sum()))
show(
    "clean table remaining non-product codes",
    cur.loc[~rem_prod].groupby(clean_sc[~rem_prod]).size().sort_values(ascending=False),
)

# ------------------------------------------------------------------ item 9
sec("ITEM 9: final clean table metrics")
cur = cur.reset_index(drop=True)
cur["Revenue"] = cur["Quantity"] * cur["Price"]
total_rev = cur["Revenue"].sum()
rec("clean_rows", len(cur))
rec("clean_total_revenue", float(total_rev))
rec("clean_distinct_stockcodes", int(cur["StockCode"].nunique()))
rec("clean_distinct_invoices", int(cur["Invoice"].nunique()))
rec("clean_date_min", cur["InvoiceDate"].min())
rec("clean_date_max", cur["InvoiceDate"].max())

prod_rev = (
    cur.groupby("StockCode")
    .agg(Revenue=("Revenue", "sum"), Rows=("Revenue", "size"), Description=("Description", "first"))
    .sort_values("Revenue", ascending=False)
)
prod_rev["RevenueShare"] = prod_rev["Revenue"] / total_rev
prod_rev["CumShare"] = prod_rev["RevenueShare"].cumsum()
show("top 10 products by revenue", prod_rev.head(10))
R["top10_products"] = [
    {
        "StockCode": str(i),
        "Description": (None if pd.isna(r["Description"]) else str(r["Description"])),
        "Revenue": round(float(r["Revenue"]), 2),
        "Rows": int(r["Rows"]),
        "RevenueSharePct": round(float(r["RevenueShare"]) * 100, 4),
        "CumSharePct": round(float(r["CumShare"]) * 100, 4),
    }
    for i, r in prod_rev.head(10).iterrows()
]
show("top 20 products only codes", prod_rev.head(20)[["Revenue", "Rows", "CumShare"]])
R["top10_product_codes"] = [str(i) for i in prod_rev.head(10).index]

# ABC split: rank desc by revenue, cum share <=0.80 -> A, <=0.95 -> B, else C
def abc_class(cum):
    if cum <= 0.80:
        return "A"
    if cum <= 0.95:
        return "B"
    return "C"


prod_rev["ABC"] = prod_rev["CumShare"].apply(abc_class)
abc = prod_rev.groupby("ABC").agg(
    Products=("Revenue", "size"), Revenue=("Revenue", "sum")
)
abc["PctOfProducts"] = abc["Products"] / len(prod_rev) * 100
abc["RevenueSharePct"] = abc["Revenue"] / total_rev * 100
abc = abc.reindex(["A", "B", "C"])
show("ABC split", abc)
R["abc"] = {
    k: {
        "products": int(abc.loc[k, "Products"]),
        "pct_of_products": round(float(abc.loc[k, "PctOfProducts"]), 4),
        "revenue": round(float(abc.loc[k, "Revenue"]), 2),
        "revenue_share_pct": round(float(abc.loc[k, "RevenueSharePct"]), 4),
    }
    for k in ["A", "B", "C"]
}
R["total_products"] = int(len(prod_rev))
# boundary checks: products exactly at thresholds
for thr in (0.80, 0.95):
    near = prod_rev[(prod_rev["CumShare"] > thr - 0.01) & (prod_rev["CumShare"] <= thr + 0.01)]
    show(f"products with cum share near {thr}", near[["Revenue", "CumShare"]].head(10))

# country revenue top 5 (and full list)
country = (
    cur.groupby("Country")["Revenue"]
    .sum()
    .sort_values(ascending=False)
)
country_share = country / total_rev * 100
show("country revenue (all, top shown separately)", country.head(15))
R["country_top5"] = [
    {
        "Country": str(k),
        "Revenue": round(float(v), 2),
        "SharePct": round(float(country_share[k]), 4),
    }
    for k, v in country.head(5).items()
]
R["n_countries"] = int(len(country))
R["country_all"] = {str(k): round(float(v), 2) for k, v in country.items()}

# monthly revenue
monthly = (
    cur.assign(Month=cur["InvoiceDate"].dt.to_period("M").astype(str))
    .groupby("Month")
    .agg(Revenue=("Revenue", "sum"), Rows=("Revenue", "size"), Invoices=("Invoice", "nunique"))
)
show("monthly revenue", monthly)
R["monthly_revenue"] = {
    k: {
        "revenue": round(float(r["Revenue"]), 2),
        "rows": int(r["Rows"]),
        "invoices": int(r["Invoices"]),
    }
    for k, r in monthly.iterrows()
}
rec("monthly_total_check", float(monthly["Revenue"].sum()))

# ------------------------------------------------------------------ item 10
sec("ITEM 10: first 7 raw data rows of 2010-2011 sheet")
first7 = df2.head(7)
for i, r in first7.iterrows():
    lines.append(
        "row "
        + str(i)
        + ": Invoice="
        + repr(r["Invoice"])
        + " | StockCode="
        + repr(r["StockCode"])
        + " | Description="
        + repr(r["Description"])
        + " | Quantity="
        + repr(topy(r["Quantity"]))
        + " | Price="
        + repr(topy(r["Price"]))
        + " | InvoiceDate="
        + repr(topy(r["InvoiceDate"]))
        + " | Customer ID="
        + repr(r["Customer ID"])
        + " | Country="
        + repr(r["Country"])
    )
R["first7_sheet2"] = [
    {
        "Invoice": str(r["Invoice"]),
        "StockCode": str(r["StockCode"]),
        "Description": str(r["Description"]),
        "Quantity": topy(r["Quantity"]),
        "Price": topy(r["Price"]),
        "InvoiceDate": topy(r["InvoiceDate"]),
        "CustomerID": (None if pd.isna(r["Customer ID"]) else str(r["Customer ID"])),
        "Country": str(r["Country"]),
    }
    for _, r in first7.iterrows()
]
R["first7_sheet1"] = [
    {
        "Invoice": str(r["Invoice"]),
        "StockCode": str(r["StockCode"]),
        "Description": str(r["Description"]),
        "Quantity": topy(r["Quantity"]),
        "Price": topy(r["Price"]),
        "InvoiceDate": topy(r["InvoiceDate"]),
    }
    for _, r in df1.head(7).iterrows()
]

# ------------------------------------------------------------------ item 11
sec("ITEM 11: float check")
repr_val = repr(6 * 2.55)
lines.append("repr(6 * 2.55) = " + repr_val)
R["repr_6x2_55"] = repr_val
R["round_15_3"] = repr(round(6 * 2.55, 2))
R["float_15_3"] = repr(15.3)
R["float_15_3_equals_6x2_55"] = 15.3 == 6 * 2.55
lines.append("repr(round(6 * 2.55, 2)) = " + R["round_15_3"])
lines.append("repr(15.3) = " + R["float_15_3"])
lines.append("15.3 == 6 * 2.55 -> " + str(R["float_15_3_equals_6x2_55"]))

# ------------------------------------------------------------------ extra
sec("EXTRA checks: file / consistency")
import hashlib

h = hashlib.sha256()
with open(RAW, "rb") as f:
    for chunk in iter(lambda: f.read(1 << 20), b""):
        h.update(chunk)
rec("raw_sha256", h.hexdigest())
rec("raw_size_bytes", os.path.getsize(RAW))
rec("loaded_pickle_sheets", list(data.keys()))
rec("overlap_date_note", "overlap window defined as 2010-12-01 00:00 <= InvoiceDate < 2010-12-10 00:00")
# zero-quantity / weird values in sheet2 slice before cleaning for the record
rec("slice_qty_lt_0_rows", int((slice_df["Quantity"] < 0).sum()))
rec("slice_price_lt_0_rows", int((slice_df["Price"] < 0).sum()))
rec("slice_invoice_541431_rows", int((slice_df["Invoice"].astype(str) == "541431").sum()))
rec("slice_duplicate_rows_after_dedup_note", int(slice_df.duplicated().sum()))

with open("_verify/results.json", "w") as f:
    json.dump(R, f, indent=2, default=topy)
with open("_verify/results.txt", "w") as f:
    f.write("\n".join(lines) + "\n")
print("\n".join(lines))
print("\nWROTE _verify/results.json and _verify/results.txt")
