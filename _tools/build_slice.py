"""Build the teaching slice for Python for Supply Chain.

Reads the untouched raw workbook, keeps every row of the `Year 2010-2011`
sheet from 2010-12-01 00:00 up to but not including 2011-03-01 00:00,
and writes the uncleaned CSV the course uses.

Run:  _tools/venv/bin/python _tools/build_slice.py
"""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw" / "online_retail_II.xlsx"
OUT = ROOT / "data" / "online_retail_ii_lesson.csv"
SHEET = "Year 2010-2011"
START = pd.Timestamp("2010-12-01 00:00:00")
END = pd.Timestamp("2011-03-01 00:00:00")

print("reading", RAW, flush=True)
raw = pd.read_excel(RAW, sheet_name=SHEET)
print("sheet rows:", len(raw), flush=True)

mask = (raw["InvoiceDate"] >= START) & (raw["InvoiceDate"] < END)
slice_df = raw.loc[mask].copy()
print("slice rows:", len(slice_df), flush=True)

slice_df.to_csv(OUT, index=False, date_format="%Y-%m-%d %H:%M:%S", na_rep="")
print("wrote", OUT, flush=True)

# checks against the build spec (PLAN.md section 3)
checks = {
    "rows": (len(slice_df), 105335),
    "columns": (slice_df.shape[1], 8),
    "first timestamp": (str(slice_df["InvoiceDate"].min()), "2010-12-01 08:26:00"),
    "last timestamp": (str(slice_df["InvoiceDate"].max()), "2011-02-28 17:04:00"),
    "missing customer": (int(slice_df["Customer ID"].isna().sum()), 36210),
    "missing description": (int(slice_df["Description"].isna().sum()), 304),
    "cancellations": (int(slice_df["Invoice"].astype(str).str.upper().str.startswith("C").sum()), 1904),
    "duplicates": (int(slice_df.drop_duplicates().shape[0] - len(slice_df)), -975),
    "zero price": (int((slice_df["Price"] == 0).sum()), 540),
    "negative price": (int((slice_df["Price"] < 0).sum()), 0),
    "non-product rows": (int((~slice_df["StockCode"].astype(str).str[0].str.isdigit()).sum()), 588),
    "size MB": (round(OUT.stat().st_size / 1024 / 1024, 2), 9.3),
}
for name, (got, want) in checks.items():
    if name == "size MB":
        ok = abs(got - want) < 0.2
    else:
        ok = got == want
    print(f"{'OK ' if ok else 'BAD'} {name}: {got} (expected {want})", flush=True)
print("done", flush=True)
