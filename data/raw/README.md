# Raw data (not committed)

The raw dataset file is not in this repository because it is 43.5 MiB and does not change. Restore it with the steps below.

## File

- Name: `online_retail_II.xlsx`
- Size: 45,622,278 bytes (43.5 MiB)
- sha256: `bcbe73b35f5b7babf197fb0cb983a11f5d9ff929078d4aa53d171b1f2df2e980`
- Downloaded: 2 November 2026
- Source: https://archive.ics.uci.edu/static/public/502/online+retail+ii.zip (the zip holds the xlsx)
- Zip sha256: `572e36277c2390fbfde10664750731e0a86f55e33470d91919085f0408e67bfb`

## How to restore

```bash
mkdir -p data/raw
curl -L -o data/raw/online_retail_ii.zip "https://archive.ics.uci.edu/static/public/502/online+retail+ii.zip"
cd data/raw && unzip -o online_retail_ii.zip
shasum -a 256 online_retail_II.xlsx
```

The last command must print the sha256 above. If it does not, stop and check the download.

## Licence and citation

Chen, D. (2012). Online Retail II [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5CG6D. Licence CC BY 4.0.

Credit this source in the data README, in the first notebook that uses the data (S4), in the course outline, in the course home, and on the learner's GitHub README.

## Derived files

`data/work/` holds the full CSV conversions and the slice working copy. It is generated locally and ignored by git. The only data file that will be committed is the small teaching slice, `data/online_retail_ii_lesson.csv`, built in Phase 2.
