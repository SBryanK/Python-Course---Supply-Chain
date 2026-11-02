"""Re-check every number the Phase 1 docs claim against the real data.

Run after _tools/convert_sheets.py and any change to the docs or the slice.
Writes _tools/fact_check_results.json and prints PASS/FAIL.
"""
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "_tools" / "fact_check_results.json"

dtypes = {"Invoice": str, "StockCode": str, "Description": str, "Customer ID": float}
s1 = pd.read_csv(ROOT / "data/work/sheet_2009_2010.csv", dtype=dtypes, parse_dates=["InvoiceDate"])
s2 = pd.read_csv(ROOT / "data/work/sheet_2010_2011.csv", dtype=dtypes, parse_dates=["InvoiceDate"])
cols = ["Invoice", "StockCode", "Description", "Quantity", "InvoiceDate", "Price", "Customer ID", "Country"]
raw = pd.concat([s1[cols], s2[cols]], ignore_index=True)

inv = raw["Invoice"]
is_c = inv.str.upper().str.startswith("C")
q = raw["Quantity"]
p = raw["Price"]
rev = q * p
code = raw["StockCode"]
first = code.str[0]
is_product = first.str.isdigit()

checks = []


def check(name, got, want, tol=0.005):
    if isinstance(want, float):
        ok = abs(float(got) - want) <= tol
    else:
        ok = got == want
    checks.append({"check": name, "got": got, "want": want, "pass": bool(ok)})
    if not ok:
        print(f"FAIL {name}: got {got!r}, want {want!r}", flush=True)


# --- whole file ---
check("rows sheet1", len(s1), 525461)
check("rows sheet2", len(s2), 541910)
check("rows total", len(raw), 1067371)
check("date min", str(raw["InvoiceDate"].min()), "2009-12-01 07:45:00")
check("date max", str(raw["InvoiceDate"].max()), "2011-12-09 12:50:00")
check("unique invoices", int(inv.nunique()), 53628)
check("unique customers", int(raw["Customer ID"].nunique()), 5942)
check("unique countries", int(raw["Country"].nunique()), 43)
check("unique stock codes", int(code.nunique()), 5305)
check("unique descriptions", int(raw["Description"].nunique()), 5698)
for c, want in [("Description", 4382), ("Customer ID", 243007)]:
    check(f"missing {c}", int(raw[c].isna().sum()), want)
check("missing desc sheet1", int(s1["Description"].isna().sum()), 2928)
check("missing desc sheet2", int(s2["Description"].isna().sum()), 1454)
check("missing cust sheet1", int(s1["Customer ID"].isna().sum()), 107927)
check("missing cust sheet2", int(s2["Customer ID"].isna().sum()), 135080)
check("missing customer pct", round(100 * raw["Customer ID"].isna().mean(), 2), 22.77)
check("missing desc all zero price", int(raw[raw["Description"].isna()]["Price"].ne(0).sum()), 0)

# --- cancellations and odd values ---
check("C rows", int(is_c.sum()), 19494)
check("C row pct", round(100 * is_c.mean(), 2), 1.83)
check("distinct C invoices", int(inv[is_c].nunique()), 8292)
check("C qty >= 0 rows", int((is_c & (q >= 0)).sum()), 1)
check("non-C negative qty", int((~is_c & (q < 0)).sum()), 3457)
check("negative price rows", int((p < 0).sum()), 5)
check("zero price rows", int((p == 0).sum()), 6202)
check("price under 0.01", int((p < 0.01).sum()), 6225)
check("price over 100", int((p > 100).sum()), 1946)
check("price over 1000", int((p > 1000).sum()), 245)
check("zero price positive qty", int(((p == 0) & (q > 0)).sum()), 2745)
check("qty negative rows", int((q < 0).sum()), 22950)
check("qty zero rows", int((q == 0).sum()), 0)
check("qty over 1000", int((q > 1000).sum()), 352)
check("qty over 10000", int((q > 10000).sum()), 9)
check("qty abs over 10000", int((q.abs() > 10000).sum()), 11)
check("price min", float(p.min()), -53594.36)
check("price max", float(p.max()), 38970.0)
check("qty min", int(q.min()), -80995)
check("qty max", int(q.max()), 80995)
check("revenue total", round(float(rev.sum()), 2), 19287250.57)
check("revenue positive", round(float(rev[rev > 0].sum()), 2), 20972968.14)
check("revenue negative", round(float(rev[rev < 0].sum()), 2), -1685717.57)
check("negative revenue rows", int((rev < 0).sum()), 19498)

# --- duplicates and overlap ---
check("exact duplicate rows stacked", int(raw.duplicated(subset=cols).sum()), 34335)
check("duplicates within sheet1", int(s1.duplicated(subset=cols).sum()), 6865)
check("duplicates within sheet2", int(s2.duplicated(subset=cols).sum()), 5268)
d1 = s1[(s1["InvoiceDate"] >= "2010-12-01") & (s1["InvoiceDate"] < "2010-12-10")]
d2 = s2[(s2["InvoiceDate"] >= "2010-12-01") & (s2["InvoiceDate"] < "2010-12-10")]
check("overlap rows sheet1", len(d1), 22523)
check("overlap rows sheet2", len(d2), 22523)
common = d1[cols].drop_duplicates().merge(d2[cols].drop_duplicates(), on=cols, how="inner")
check("distinct rows in both sheets", len(common), 22202)
pairs = d1[cols].merge(d2[cols], on=cols, how="inner")
check("join pairs", len(pairs), 23221)

# --- non-product classification ---
check("rows matching product pattern", int(is_product.sum()), 1061278)
check("non-product rows", int((~is_product).sum()), 6093)
check("non-product pct", round(100 * (~is_product).mean(), 2), 0.57)
check("non-product distinct codes", int(code[~is_product].nunique()), 62)
check("rows failing unstripped product pattern", int((~code.str.match(r"^\d{5}[A-Za-z]{0,2}$")).sum()), 6094)
trailing = (raw["Description"].astype(str) != raw["Description"].astype(str).str.strip()).sum()
check("description trailing/leading space rows", int(trailing), 213035)
check("descriptions distinct strip upper", int(raw["Description"].astype(str).str.strip().str.upper().nunique()), 5632)
check("lowercase code rows whole file", int(code.str.contains(r"[a-z]").sum()), 3471)

# --- countries ---
c_counts = raw["Country"].value_counts()
check("UK rows", int(c_counts["United Kingdom"]), 981330)
check("UK row share pct", round(100 * c_counts["United Kingdom"] / len(raw), 2), 91.94)
check("EIRE rows", int(c_counts["EIRE"]), 17866)
check("Germany rows", int(c_counts["Germany"]), 17624)

# --- monthly rows ---
monthly = raw.groupby(raw["InvoiceDate"].dt.to_period("M").astype(str)).size()
want_months = {"2009-12": 45228, "2010-01": 31555, "2010-02": 29388, "2010-03": 41511,
               "2010-04": 34057, "2010-05": 35323, "2010-06": 39983, "2010-07": 33383,
               "2010-08": 33306, "2010-09": 42091, "2010-10": 59098, "2010-11": 78015,
               "2010-12": 65004, "2011-01": 35147, "2011-02": 27707, "2011-03": 36748,
               "2011-04": 29916, "2011-05": 37030, "2011-06": 36874, "2011-07": 39518,
               "2011-08": 35284, "2011-09": 50226, "2011-10": 60742, "2011-11": 84711,
               "2011-12": 25526}
for k, v in want_months.items():
    check(f"month rows {k}", int(monthly[k]), v)

# --- the lesson slice ---
w = s2[(s2["InvoiceDate"] >= "2010-12-01") & (s2["InvoiceDate"] < "2011-03-01")].copy()
check("slice rows", len(w), 105335)
check("slice cols", w.shape[1], 8)
check("slice first date", str(w["InvoiceDate"].min()), "2010-12-01 08:26:00")
check("slice last date", str(w["InvoiceDate"].max()), "2011-02-28 17:04:00")
w_inv = w["Invoice"]
w_c = w_inv.str.upper().str.startswith("C")
check("slice invoices", int(w_inv.nunique()), 4894)
check("slice products", int(w["StockCode"].nunique()), 3159)
check("slice countries", int(w["Country"].nunique()), 31)
check("slice missing customer", int(w["Customer ID"].isna().sum()), 36210)
check("slice missing customer pct", round(100 * w["Customer ID"].isna().mean(), 1), 34.4)
check("slice missing description", int(w["Description"].isna().sum()), 304)
check("slice cancellation rows", int(w_c.sum()), 1904)
check("slice distinct C invoices", int(w_inv[w_c].nunique()), 805)
check("slice duplicate rows", int(w.duplicated(subset=cols).sum()), 975)
check("slice negative qty rows", int((w["Quantity"] < 0).sum()), 2118)
check("slice zero price rows", int((w["Price"] == 0).sum()), 540)
check("slice negative price rows", int((w["Price"] < 0).sum()), 0)
check("slice non-product rows", int((~w["StockCode"].str[0].str.isdigit()).sum()), 588)
check("slice Germany rows", int((w["Country"] == "Germany").sum()), 1741)
check("slice raw revenue", round(float((w["Quantity"] * w["Price"]).sum()), 2), 1807019.93)
check("slice first 7 qty", [int(x) for x in w["Quantity"].head(7)], [6, 6, 8, 6, 6, 2, 6])
check("slice lowercase code rows", int(w["StockCode"].str.contains(r"[a-z]").sum()), 541)
check("6 * 2.55", repr(6 * 2.55), "15.299999999999999")

# --- cleaning steps ---
d = w.drop_duplicates()
s_dedup = len(d)
d = d[~d["Invoice"].str.upper().str.startswith("C")]
s_c = len(d)
d = d[d["Quantity"] > 0]
s_q = len(d)
d = d[d["Price"] > 0]
s_p = len(d)
first_char = d["StockCode"].str[0]
d = d[first_char.str.isdigit()]
s_np = len(d)
d = d.copy()
d["revenue"] = d["Quantity"] * d["Price"]
d["month"] = d["InvoiceDate"].dt.to_period("M")
d = d[d["Invoice"] != "541431"]
s_clean = len(d)
check("step dedup", s_dedup, 104360)
check("step C", s_c, 102471)
check("step qty", s_q, 102257)
check("step price", s_p, 101933)
check("step nonproduct", s_np, 101459)
check("clean rows", s_clean, 101458)
check("clean shape", list(d.shape), [101458, 10])
check("clean months", int(d["month"].nunique()), 3)
check("clean revenue", round(float(d["revenue"].sum()), 2), 1876534.04)
check("clean invoices", int(d["Invoice"].nunique()), 3723)
check("clean products", int(d["StockCode"].nunique()), 3066)
check("clean customers", int(d["Customer ID"].nunique()), 1679)
check("clean missing customer", int(d["Customer ID"].isna().sum()), 35364)
check("clean missing descriptions", int(d["Description"].isna().sum()), 0)
check("clean Germany rows", int((d["Country"] == "Germany").sum()), 1514)
check("clean lowercase code rows", int(d["StockCode"].str.contains(r"[a-z]").sum()), 532)
check("clean multi-description codes", int((d.groupby("StockCode")["Description"].nunique() > 1).sum()), 40)

# --- ABC, products, countries, months, days ---
pv = d.groupby("StockCode")["revenue"].sum().sort_values(ascending=False).reset_index()
pv["cum"] = pv["revenue"].cumsum()
pv["share"] = pv["cum"] / pv["revenue"].sum()
pv["abc"] = pv["share"].apply(lambda s: "A" if s <= 0.80 else ("B" if s <= 0.95 else "C"))
cls = pv.groupby("abc").agg(n=("StockCode", "size"), rev=("revenue", "sum"))
total = float(pv["revenue"].sum())
check("ABC A products", int(cls.loc["A", "n"]), 671)
check("ABC A revenue", round(float(cls.loc["A", "rev"]), 2), 1500839.03)
check("ABC A rev pct", round(100 * float(cls.loc["A", "rev"]) / total, 2), 79.98)
check("ABC A product pct", round(100 * int(cls.loc["A", "n"]) / len(pv), 1), 21.9)
check("ABC B products", int(cls.loc["B", "n"]), 794)
check("ABC B revenue", round(float(cls.loc["B", "rev"]), 2), 281777.11)
check("ABC C products", int(cls.loc["C", "n"]), 1601)
check("ABC C revenue", round(float(cls.loc["C", "rev"]), 2), 93917.90)
check("top product revenue", round(float(pv.iloc[0]["revenue"]), 2), 51504.85)
check("top product code", str(pv.iloc[0]["StockCode"]), "22423")
check("top 10 cumulative share", round(float(pv["share"].head(10).iloc[-1]), 4), 0.0962)
check("product table rows (merge check)", int(d[["StockCode", "Description"]].drop_duplicates(subset="StockCode").shape[0]), 3066)
pairs = d[["StockCode", "Description"]].drop_duplicates()
check("name pairs before dedupe", int(len(pairs)), 3107)
check("extra name-pair rows", int(len(pairs) - d["StockCode"].nunique()), 41)

country = d.groupby("Country")["revenue"].sum().sort_values(ascending=False)
check("UK revenue", round(float(country["United Kingdom"]), 2), 1591694.50)
check("UK revenue share", round(100 * float(country["United Kingdom"]) / total, 2), 84.82)
non_uk = country.drop("United Kingdom")
check("non-UK top5", {str(k): round(float(v), 2) for k, v in non_uk.head(5).items()},
      {"Netherlands": 58182.55, "EIRE": 43426.19, "Germany": 37365.63, "France": 32392.39, "Australia": 24678.48})

monthly_rev = d.groupby(d["InvoiceDate"].dt.to_period("M").astype(str))["revenue"].sum()
check("slice month 2010-12 rev", round(float(monthly_rev["2010-12"]), 2), 775572.23)
check("slice month 2011-01 rev", round(float(monthly_rev["2011-01"]), 2), 593178.39)
check("slice month 2011-02 rev", round(float(monthly_rev["2011-02"]), 2), 507783.42)
daily = d.groupby(d["InvoiceDate"].dt.date)["revenue"].sum()
check("trading days", int(len(daily)), 68)
check("best day revenue", round(float(daily.max()), 2), 81454.99)
check("best day date", str(daily.idxmax()), "2010-12-07")
check("worst day revenue", round(float(daily.min()), 2), 3439.67)
uk_month = d[d["Country"] == "United Kingdom"].groupby(
    d["InvoiceDate"].dt.to_period("M").astype(str))["revenue"].sum()
check("UK month 2010-12", round(float(uk_month["2010-12"]), 2), 705166.72)
check("UK month 2011-01", round(float(uk_month["2011-01"]), 2), 468651.61)
check("UK month 2011-02", round(float(uk_month["2011-02"]), 2), 417876.17)

# --- alternative window ---
a = s2[(s2["InvoiceDate"] >= "2011-02-01") & (s2["InvoiceDate"] < "2011-05-01")].copy()
ad = a.drop_duplicates()
ad = ad[~ad["Invoice"].str.upper().str.startswith("C")]
ad = ad[ad["Quantity"] > 0]
ad = ad[ad["Price"] > 0]
ad = ad[ad["StockCode"].str[0].str.isdigit()].copy()
ad["revenue"] = ad["Quantity"] * ad["Price"]
check("alt raw rows", len(a), 94371)
check("alt clean rows", len(ad), 90771)
check("alt clean revenue", round(float(ad["revenue"].sum()), 2), 1712846.69)

# --- report ---
passed = sum(1 for c in checks if c["pass"])
failed = [c for c in checks if not c["pass"]]
OUT.write_text(json.dumps({"passed": passed, "failed": len(failed), "checks": checks}, indent=1))
print(f"\n{passed}/{len(checks)} checks passed, {len(failed)} failed")
