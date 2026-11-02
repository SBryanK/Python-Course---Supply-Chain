"""Load the raw UCI Online Retail II xlsx directly and cache as pickle.

Independent verification: no pre-existing JSON/CSV in the repo is used.
Invoice and StockCode are read as text, InvoiceDate parsed as datetime.
"""
import os
import time

os.environ.setdefault("MPLCONFIGDIR", os.path.abspath("_tools/mplconfig"))

import pandas as pd

RAW = "data/raw/online_retail_II.xlsx"
OUT = "_verify/raw_sheets.pkl"

SHEETS = ["Year 2009-2010", "Year 2010-2011"]

t0 = time.time()
xl = pd.ExcelFile(RAW, engine="openpyxl")
print("sheet names:", xl.sheet_names, flush=True)
print("headers:", {s: xl.parse(s, nrows=0).columns.tolist() for s in xl.sheet_names}, flush=True)

data = {}
for s in SHEETS:
    t = time.time()
    df = pd.read_excel(
        RAW,
        sheet_name=s,
        engine="openpyxl",
        dtype={"Invoice": str, "StockCode": str, "Customer ID": str},
        parse_dates=["InvoiceDate"],
    )
    # Normalise column names defensively (keep raw header text version too)
    df.columns = [str(c).strip() for c in df.columns]
    data[s] = df
    print(
        f"{s}: rows={len(df)} cols={df.columns.tolist()} load={time.time()-t:.1f}s",
        flush=True,
    )
    print(df.head(7).to_string(), flush=True)
    print("dtypes:\n", df.dtypes, flush=True)

pd.to_pickle(data, OUT)
print(f"saved {OUT}; total elapsed {time.time()-t0:.1f}s", flush=True)
