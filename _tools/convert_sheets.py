"""Convert each xlsx sheet to its own CSV, plus a combined CSV with a source column.

Work files only: data/work/ is never delivered to the learner.
"""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw" / "online_retail_II.xlsx"
WORK = ROOT / "data" / "work"
WORK.mkdir(parents=True, exist_ok=True)

SHEETS = {
    "Year 2009-2010": "sheet_2009_2010.csv",
    "Year 2010-2011": "sheet_2010_2011.csv",
}
parts = []
for sheet, name in SHEETS.items():
    df = pd.read_excel(RAW, sheet_name=sheet)
    df.to_csv(WORK / name, index=False)
    d = df.copy()
    d["source_sheet"] = sheet
    parts.append(d)
    print(sheet, df.shape, "->", name, flush=True)

combined = pd.concat(parts, ignore_index=True)
combined.to_csv(WORK / "online_retail_ii_with_sheet.csv", index=False)
print("combined", combined.shape, flush=True)
