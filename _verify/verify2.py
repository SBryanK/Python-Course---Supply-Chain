"""Second pass: cross-check every quantitative claim in data/EXPLORATION.md
against the independent raw-xlsx computation, and explain discrepancies.

Reads only _verify/raw_sheets.pkl (raw xlsx cache) for the source of truth;
Lead's CSVs/JSON are read ONLY for discrepancy attribution, never trusted.
"""
import json
import os

os.environ.setdefault("MPLCONFIGDIR", os.path.abspath("_tools/mplconfig"))

import numpy as np
import pandas as pd

pd.set_option("display.width", 250)
pd.set_option("display.max_rows", 300)

data = pd.read_pickle("_verify/raw_sheets.pkl")
S1, S2 = "Year 2009-2010", "Year 2010-2011"
df1, df2 = data[S1].copy(), data[S2].copy()
COLS = ["Invoice", "StockCode", "Description", "Quantity", "InvoiceDate", "Price", "Customer ID", "Country"]
combo = pd.concat([df1, df2], ignore_index=True)
OUT = {}
L = []


def p(*a):
    s = " ".join(str(x) for x in a)
    L.append(s)
    print(s)


def claim(name, mine, lead):
    ok = mine == lead
    OUT[name] = {"mine": mine, "lead": lead, "match": bool(ok)}
    p(("MATCH " if ok else "DIFF  ") + f"{name}: mine={mine!r} lead={lead!r}")


# ---------------- A. slice non-product detail
p("\n=== A. slice non-product classification ===")
sl = df2[(df2["InvoiceDate"] >= pd.Timestamp("2010-12-01")) & (df2["InvoiceDate"] < pd.Timestamp("2011-03-01"))].copy()
PRODUCT_RE = __import__("re").compile(r"^\d{5}[A-Za-z]{0,2}$", __import__("re").ASCII)
sl_sc = sl["StockCode"].astype(str)
sl_np_mask = ~sl_sc.apply(lambda s: bool(PRODUCT_RE.fullmatch(s)))
np_counts = sl.loc[sl_np_mask, "StockCode"].astype(str).value_counts()
p("slice non-product rows (regex):", int(sl_np_mask.sum()))
p("slice non-product breakdown:")
p(np_counts.to_string())
LEAD13 = ["POST", "DOT", "M", "BANK CHARGES", "C2", "D", "S", "AMAZONFEE", "ADJUST", "CRUK", "PADS", "B", "GIFT"]
p("slice rows in Lead's 13-code list:", int(sl["StockCode"].astype(str).isin(LEAD13).sum()))
p("slice rows in the 8 lesson codes:", int(sl["StockCode"].astype(str).isin(LEAD13[:8]).sum()))
extra = np_counts[~np_counts.index.isin(LEAD13)]
p("slice non-product rows NOT in Lead 13-code list:", int(extra.sum()))
p(extra.to_string())
OUT["slice_nonprod_breakdown"] = {str(k): int(v) for k, v in np_counts.items()}
OUT["slice_nonprod_total"] = int(sl_np_mask.sum())

# ---------------- B. whole file claims
p("\n=== B. whole-file claims ===")
claim("combined rows", len(combo), 1067371)
claim("distinct invoices", int(combo["Invoice"].astype(str).nunique()), 53628)
claim("distinct customers", int(combo["Customer ID"].nunique()), 5942)
claim("distinct countries", int(combo["Country"].nunique()), 43)
claim("distinct stock codes", int(combo["StockCode"].astype(str).nunique()), 5305)
claim("distinct descriptions", int(combo["Description"].nunique()), 5698)
mem = combo.memory_usage(deep=True).sum() / 1e6
p(f"memory use deep combined: {mem:.1f} MB (report 313.2 MB)")
OUT["memory_mb"] = round(float(mem), 1)
claim("missing desc sheet1", int(df1["Description"].isna().sum()), 2928)
claim("missing desc sheet2", int(df2["Description"].isna().sum()), 1454)
claim("missing cust sheet1", int(df1["Customer ID"].isna().sum()), 107927)
claim("missing cust sheet2", int(df2["Customer ID"].isna().sum()), 135080)
claim("desc missing rows with price 0", int((combo["Description"].isna() & (combo["Price"] == 0)).sum()), 4382)
claim("desc missing rows total", int(combo["Description"].isna().sum()), 4382)
inv = combo["Invoice"].astype(str)
pref = inv.str[0].value_counts()
p("invoice first-char counts:", pref.to_dict())
claim("invoice first char 5 rows", int(pref.get("5", 0)), 939382)
claim("invoice first char 4 rows", int(pref.get("4", 0)), 108489)
claim("invoice first char C rows", int(pref.get("C", 0)), 19494)
claim("invoice first char A rows", int(pref.get("A", 0)), 6)
cpos = combo[inv.str.upper().str.startswith("C") & (combo["Quantity"] >= 0)]
p("C row(s) with qty>=0:\n" + cpos[COLS].to_string())
claim("neg qty not C rows", int((~inv.str.upper().str.startswith("C") & (combo["Quantity"] < 0)).sum()), 3457)
nn = combo[~inv.str.upper().str.startswith("C") & (combo["Quantity"] < 0)]
p("neg qty not C: missing desc rows:", int(nn["Description"].isna().sum()), "(report 2,689)")
p("neg qty not C: desc value counts (top 20):")
p(nn["Description"].fillna("<NaN>").astype(str).value_counts().head(20).to_string())
OUT["negqty_nonc_nan"] = int(nn["Description"].isna().sum())
OUT["negqty_nonc_desc_top"] = {str(k): int(v) for k, v in nn["Description"].fillna("<NaN>").astype(str).value_counts().head(20).items()}

# prices
p("\n-- prices --")
claim("price min", round(float(combo["Price"].min()), 2), -53594.36)
claim("price max", round(float(combo["Price"].max()), 2), 38970.0)
claim("price mean 4dp", round(float(combo["Price"].mean()), 4), 4.6494)
claim("price median", round(float(combo["Price"].median()), 2), 2.10)
claim("negative price rows", int((combo["Price"] < 0).sum()), 5)
claim("zero price rows", int((combo["Price"] == 0).sum()), 6202)
claim("price under 0.01 rows", int((combo["Price"] < 0.01).sum()), 6225)
claim("price over 100 rows", int((combo["Price"] > 100).sum()), 1946)
claim("price over 1000 rows", int((combo["Price"] > 1000).sum()), 245)
claim("zero price positive qty rows", int(((combo["Price"] == 0) & (combo["Quantity"] > 0)).sum()), 2745)
hp = combo[combo["Price"] > 1000]
p("price>1000 by stock code:", hp["StockCode"].astype(str).value_counts().head(15).to_dict())
OUT["price_gt1000_codes"] = {str(k): int(v) for k, v in hp["StockCode"].astype(str).value_counts().items()}
hp_other = hp[~hp["StockCode"].astype(str).isin(["M", "AMAZONFEE", "DOT", "BANK CHARGES", "D", "POST", "CRUK", "ADJUST", "B"])]
p("price>1000 rows that are not known non-product codes:\n" + hp_other[COLS].to_string())

# quantities
p("\n-- quantities --")
claim("qty min", int(combo["Quantity"].min()), -80995)
claim("qty max", int(combo["Quantity"].max()), 80995)
claim("qty mean 2dp", round(float(combo["Quantity"].mean()), 2), 9.94)
claim("qty median", float(combo["Quantity"].median()), 3.0)
claim("negative qty rows", int((combo["Quantity"] < 0).sum()), 22950)
claim("qty over 1000 rows", int((combo["Quantity"] > 1000).sum()), 352)
claim("qty over 10000 rows", int((combo["Quantity"] > 10000).sum()), 9)

# revenue
p("\n-- revenue --")
combo_rev = combo["Quantity"] * combo["Price"]
claim("gross revenue", round(float(combo_rev.sum()), 2), 19287250.57)
claim("positive revenue sum", round(float(combo_rev[combo_rev > 0].sum()), 2), 20972968.14)
claim("negative revenue sum", round(float(combo_rev[combo_rev < 0].sum()), 2), -1685717.57)
claim("negative revenue rows", int((combo_rev < 0).sum()), 19498)

# descriptions dirtiness
p("\n-- descriptions --")
dstr = combo["Description"].astype(str)
dirty = dstr != dstr.str.strip()
claim("description rows with outer spaces", int(dirty.sum()), 213035)
claim("distinct descriptions strip+upper", int(combo["Description"].dropna().astype(str).str.strip().str.upper().nunique()), 5632)
claim("distinct descriptions strip+lower", int(combo["Description"].dropna().astype(str).str.strip().str.lower().nunique()), 5632)
lc = combo["StockCode"].astype(str).str.contains(r"[a-z]")
claim("rows with lowercase stock code letter", int(lc.sum()), 3471)

# countries
p("\n-- countries --")
cc = combo.groupby("Country").size().sort_values(ascending=False)
p("country row counts top 15:\n" + cc.head(15).to_string())
report_country_rows = {
    "United Kingdom": 981330, "EIRE": 17866, "Germany": 17624, "France": 14330,
    "Netherlands": 5140, "Spain": 3811, "Switzerland": 3189, "Belgium": 3123,
    "Portugal": 2620, "Australia": 1913, "Channel Islands": 1664, "Italy": 1534,
    "Norway": 1455, "Sweden": 1364, "Cyprus": 1176,
}
for k, v in report_country_rows.items():
    claim(f"country rows {k}", int(cc.get(k, 0)), v)
claim("UK row share pct", round(float(cc.get("United Kingdom", 0)) / len(combo) * 100, 2), 91.94)
OUT["country_row_counts"] = {str(k): int(v) for k, v in cc.items()}

# monthly rows whole file
p("\n-- monthly rows whole file --")
m = combo.groupby(combo["InvoiceDate"].dt.to_period("M").astype(str)).size()
report_monthly = {
    "2009-12": 45228, "2010-01": 31555, "2010-02": 29388, "2010-03": 41511,
    "2010-04": 34057, "2010-05": 35323, "2010-06": 39983, "2010-07": 33383,
    "2010-08": 33306, "2010-09": 42091, "2010-10": 59098, "2010-11": 78015,
    "2010-12": 65004, "2011-01": 35147, "2011-02": 27707, "2011-03": 36748,
    "2011-04": 29916, "2011-05": 37030, "2011-06": 36874, "2011-07": 39518,
    "2011-08": 35284, "2011-09": 50226, "2011-10": 60742, "2011-11": 84711,
    "2011-12": 25526,
}
for k, v in report_monthly.items():
    claim(f"monthly rows {k}", int(m.get(k, 0)), v)
p("monthly rows sum:", int(m.sum()))
OUT["monthly_rows_whole"] = {str(k): int(v) for k, v in m.items()}

# duplicates decomposition
p("\n-- duplicates --")
dup_mask = combo.duplicated(subset=COLS, keep="first")
claim("stacked duplicate rows", int(dup_mask.sum()), 34335)
claim("dup within sheet1", int(df1.duplicated(subset=COLS, keep="first").sum()), 6865)
claim("dup within sheet2", int(df2.duplicated(subset=COLS, keep="first").sum()), 5268)
o1 = df1[(df1["InvoiceDate"] >= "2010-12-01") & (df1["InvoiceDate"] < "2010-12-10")]
o2 = df2[(df2["InvoiceDate"] >= "2010-12-01") & (df2["InvoiceDate"] < "2010-12-10")]
claim("overlap sheet1 rows", len(o1), 22523)
claim("overlap sheet2 rows", len(o2), 22523)
# join pair count
joined = o1[COLS].merge(o2[COLS], on=COLS, how="inner")
claim("overlap inner-join pairs", len(joined), 23221)
p("overlap inner-join pairs detail:", len(joined))
# distinct shared via hashable multiset check
def rowset(d):
    d = d[COLS].copy()
    for c in COLS:
        if d[c].dtype == object:
            d[c] = d[c].apply(lambda v: "<NA>" if pd.isna(v) else str(v))
    return set(map(tuple, d.itertuples(index=False, name=None)))
s1, s2 = rowset(o1), rowset(o2)
claim("overlap distinct shared rows", len(s1 & s2), 22202)
# decomposition of stacked dups
cross_rows = len(o2[COLS].merge(o1[COLS].drop_duplicates(), on=COLS, how="inner"))
p("sheet2 overlap-window rows that also occur in sheet1 (row count, join):", cross_rows)

# ---------------- C. raw slice claims
p("\n=== C. raw slice claims ===")
claim("slice rows", len(sl), 105335)
claim("slice columns", sl.shape[1], 8)
claim("slice invoices", int(sl["Invoice"].astype(str).nunique()), 4894)
claim("slice products raw", int(sl["StockCode"].astype(str).nunique()), 3159)
claim("slice countries", int(sl["Country"].nunique()), 31)
claim("slice missing customer", int(sl["Customer ID"].isna().sum()), 36210)
claim("slice missing description", int(sl["Description"].isna().sum()), 304)
claim("slice cancellation rows", int(sl["Invoice"].astype(str).str.upper().str.startswith("C").sum()), 1904)
c_sl = sl[sl["Invoice"].astype(str).str.upper().str.startswith("C")]
claim("slice unique C invoices", int(c_sl["Invoice"].astype(str).nunique()), 805)
claim("slice duplicate rows", int(sl.duplicated(subset=COLS).sum()), 975)
claim("slice negative qty rows", int((sl["Quantity"] < 0).sum()), 2118)
claim("slice zero price rows", int((sl["Price"] == 0).sum()), 540)
claim("slice negative price rows", int((sl["Price"] < 0).sum()), 0)
claim("slice Germany rows", int((sl["Country"] == "Germany").sum()), 1741)
claim("slice raw revenue", round(float((sl["Quantity"] * sl["Price"]).sum()), 2), 1807019.93)
claim("slice non-product rows (regex)", int(sl_np_mask.sum()), 565)

# ---------------- D. clean table claims
p("\n=== D. clean table claims ===")
w = sl.drop_duplicates(subset=COLS, keep="first")
w = w[~w["Invoice"].astype(str).str.upper().str.startswith("C")]
w = w[w["Quantity"] > 0]
w = w[w["Price"] > 0]
w = w[~w["StockCode"].astype(str).isin(LEAD13[:8])]
w = w[w["Invoice"].astype(str) != "541431"].copy()
w["Revenue"] = w["Quantity"] * w["Price"]
claim("clean rows", len(w), 101477)
claim("clean invoices", int(w["Invoice"].astype(str).nunique()), 3723)
claim("clean products", int(w["StockCode"].astype(str).nunique()), 3077)
claim("clean customers with ID", int(w["Customer ID"].nunique()), 1679)
claim("clean missing customer rows", int(w["Customer ID"].isna().sum()), 35383)
claim("clean missing description rows", int(w["Description"].isna().sum()), 0)
claim("clean revenue", round(float(w["Revenue"].sum()), 2), 1876839.90)
claim("clean Germany rows", int((w["Country"] == "Germany").sum()), 1514)
claim("clean trading days", int(w["InvoiceDate"].dt.date.nunique()), 68)
daily = w.groupby(w["InvoiceDate"].dt.date)["Revenue"].sum()
claim("clean best day revenue", round(float(daily.max()), 2), 81454.99)
claim("clean best day", str(daily.idxmax()), "2010-12-07")
claim("clean worst day revenue", round(float(daily.min()), 2), 3439.67)
claim("clean codes with >1 description", int((w.groupby("StockCode")["Description"].nunique() > 1).sum()), 40)
claim("clean lowercase code rows", int(w["StockCode"].astype(str).str.contains(r"[a-z]").sum()), 541)
claim("clean dup invoice+stockcode rows", int(w.duplicated(subset=["Invoice", "StockCode"]).sum()), 932)
pm = w.groupby("StockCode")["Revenue"].sum().sort_values(ascending=False)
claim("clean top1 revenue", round(float(pm.iloc[0]), 2), 51504.85)
claim("clean top2 revenue", round(float(pm.iloc[1]), 2), 30780.98)
claim("clean top3 revenue", round(float(pm.iloc[2]), 2), 17013.92)
claim("clean top10 cumulative pct", round(float(pm.head(10).sum() / pm.sum() * 100), 2), 9.62)
total_rev = float(w["Revenue"].sum())
cum = pm.cumsum() / total_rev
abc = pd.cut(cum, bins=[-np.inf, 0.80, 0.95, np.inf], labels=["A", "B", "C"], right=True)
cls = pd.DataFrame({"rev": pm, "abc": abc}).groupby("abc", observed=True).agg(n=("rev", "size"), r=("rev", "sum"))
for k in ["A", "B", "C"]:
    claim(f"clean ABC {k} products", int(cls.loc[k, "n"]),
          {"A": 671, "B": 796, "C": 1610}[k])
    claim(f"clean ABC {k} revenue", round(float(cls.loc[k, "r"]), 2),
          {"A": 1500839.03, "B": 282144.50, "C": 93856.37}[k])
# remaining non-product codes in clean table
clean_np = w.loc[~w["StockCode"].astype(str).apply(lambda s: bool(PRODUCT_RE.fullmatch(s)))]
p("clean non-product rows remaining:", len(clean_np))
p(clean_np["StockCode"].astype(str).value_counts().to_string())
claim("clean non-product rows remaining", len(clean_np), "not in report")
OUT["clean_composition_check"] = {
    "clean_rows": len(w),
    "nonprod_rows_remaining": int(len(clean_np)),
    "nonprod_codes_remaining": {str(k): int(v) for k, v in clean_np["StockCode"].astype(str).value_counts().items()},
}

# ---------------- E. alternative window claims
p("\n=== E. alternative window 2011-02-01 to 2011-04-30 ===")
alt = df2[(df2["InvoiceDate"] >= "2011-02-01") & (df2["InvoiceDate"] < "2011-05-01")].copy()
claim("alt raw rows", len(alt), 94371)
a = alt.drop_duplicates(subset=COLS, keep="first")
a = a[~a["Invoice"].astype(str).str.upper().str.startswith("C")]
a = a[a["Quantity"] > 0]
a = a[a["Price"] > 0]
a = a[~a["StockCode"].astype(str).isin(LEAD13[:8])].copy()
a["Revenue"] = a["Quantity"] * a["Price"]
claim("alt clean rows", len(a), 90792)
claim("alt clean revenue", round(float(a["Revenue"].sum()), 2), 1713178.04)
ap = a.groupby("StockCode")["Revenue"].sum().sort_values(ascending=False)
claim("alt top1 code", str(ap.index[0]), "22423")
claim("alt top1 revenue", round(float(ap.iloc[0]), 2), 44181.69)
claim("alt top2 code", str(ap.index[1]), "47566")
claim("alt top2 revenue", round(float(ap.iloc[1]), 2), 24249.39)

# ---------------- F. overlap multiset detail for report
p("\n=== F. overlap multiset detail ===")
c1 = o1[COLS].apply(lambda col: col.astype(str) if col.dtype == object else col, axis=0)
p("o1 rows:", len(o1), "o1 distinct:", len(s1), "o2 rows:", len(o2), "o2 distinct:", len(s2), "shared:", len(s1 & s2))
# are multisets equal?
m1 = o1[COLS].apply(lambda c: c.fillna("__NA__").astype(str) if c.dtype == object else c)
m2 = o2[COLS].apply(lambda c: c.fillna("__NA__").astype(str) if c.dtype == object else c)
k1 = m1.value_counts().sort_index()
k2 = m2.value_counts().sort_index()
p("multiset identical:", k1.equals(k2))
if not k1.equals(k2):
    joined2 = pd.concat([k1.rename("s1"), k2.rename("s2")], axis=1).fillna(0)
    diff = joined2[joined2["s1"] != joined2["s2"]]
    p("multiset differences (row count 0 if identical):", len(diff))
    p(diff.head(10).to_string())

with open("_verify/lead_claims_check.json", "w") as f:
    json.dump(OUT, f, indent=2, default=str)
with open("_verify/lead_claims_check.txt", "w") as f:
    f.write("\n".join(L) + "\n")
p("\nWROTE _verify/lead_claims_check.json/.txt")
