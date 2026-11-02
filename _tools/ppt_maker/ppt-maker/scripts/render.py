"""Export a .pptx to PDF with the deck's real fonts, then make page images and contact sheets.

LibreOffice only sees fonts in its own font folders, so a deck in Proxima Nova
or an Office font (Aptos, Gill Sans MT, ...) would be exported with a
substitute. This script finds the font files the deck uses, copies them into a
private LibreOffice profile, and exports from there.

Usage:
    python render.py deck.pptx [--outdir DIR] [--dpi 60] [--per-sheet 9] [--cols 3] [--no-pdf]

Prints the PDF path, the contact sheet paths, and any font that was still
substituted (from pdffonts).
"""

import argparse
import glob
import os
import shutil
import subprocess
import sys
from pathlib import Path

from pptx import Presentation

FONT_DIRS = [
    "~/Library/Fonts",
    "/Library/Fonts",
    "/System/Library/Fonts",
    "/System/Library/Fonts/Supplemental",
    "/Applications/Microsoft PowerPoint.app/Contents/Resources/DFonts",
    "/System/Library/AssetsV2/com_apple_MobileAsset_Font*/*/AssetData",
    "~/Downloads",
]
# The default ~/.cache profile is blocked in this workspace-write sandbox, so the
# profile lives inside the project unless PPT_MAKER_PROFILE says otherwise.
_DEFAULT_PROFILE = Path(__file__).resolve().parents[3] / "deck_check" / "lo_profile"
PROFILE = Path(os.environ.get("PPT_MAKER_PROFILE") or _DEFAULT_PROFILE).expanduser().resolve()


def fonts_in_deck(path):
    names = set()
    prs = Presentation(path)
    for slide in prs.slides:
        for el in slide._element.iter():
            if el.tag.endswith("}latin") and el.get("typeface") and not el.get("typeface").startswith("+"):
                names.add(el.get("typeface"))
    return names


def font_files(family):
    """Font files whose name starts with the family name (spaces and hyphens ignored)."""
    key = family.replace(" ", "").replace("-", "").lower()
    hits = []
    for pattern in FONT_DIRS:
        for d in glob.glob(os.path.expanduser(pattern)):
            for f in glob.glob(os.path.join(d, "*")):
                stem = Path(f).stem.replace(" ", "").replace("-", "").replace("_", "").lower()
                if f.lower().endswith((".ttf", ".otf", ".ttc")) and stem.startswith(key):
                    hits.append(f)
    return hits


def prepare_profile(families):
    fonts_dir = PROFILE / "user" / "fonts"
    fonts_dir.mkdir(parents=True, exist_ok=True)
    missing = []
    for fam in sorted(families):
        files = font_files(fam)
        if not files:
            missing.append(fam)
        for f in files:
            dst = fonts_dir / Path(f).name
            if not dst.exists():
                shutil.copy(f, dst)
    return missing


def export_pdf(pptx, outdir):
    soffice = shutil.which("soffice") or "/Applications/LibreOffice.app/Contents/MacOS/soffice"
    cmd = [soffice, f"-env:UserInstallation={PROFILE.as_uri()}", "--headless", "--convert-to", "pdf",
           "--outdir", str(outdir), str(pptx)]
    subprocess.run(cmd, check=True, capture_output=True, timeout=300)
    return Path(outdir) / (Path(pptx).stem + ".pdf")


def pdf_fonts(pdf):
    out = subprocess.run(["pdffonts", str(pdf)], capture_output=True, text=True).stdout.splitlines()[2:]
    return sorted({line.split()[0].split("+")[-1] for line in out if line.strip()})


def contact_sheets(pdf, outdir, dpi, per_sheet, cols):
    from PIL import Image, ImageDraw
    prefix = Path(outdir) / "page"
    subprocess.run(["pdftoppm", "-r", str(dpi), "-png", str(pdf), str(prefix)], check=True)
    pages = sorted(glob.glob(f"{prefix}-*.png"))
    sheets = []
    for start in range(0, len(pages), per_sheet):
        chunk = pages[start:start + per_sheet]
        w, h = Image.open(chunk[0]).size
        rows = (len(chunk) + cols - 1) // cols
        pad = 8
        sheet = Image.new("RGB", (cols * w + (cols + 1) * pad, rows * (h + 18) + (rows + 1) * pad), "#9a9a9a")
        draw = ImageDraw.Draw(sheet)
        for i, f in enumerate(chunk):
            x = pad + (i % cols) * (w + pad)
            y = pad + (i // cols) * (h + 18 + pad)
            draw.text((x, y), f"{start + i + 1}", fill="#000000")
            sheet.paste(Image.open(f), (x, y + 16))
        name = Path(outdir) / f"sheet_{start // per_sheet + 1:02d}.png"
        sheet.save(name)
        sheets.append(str(name))
    return pages, sheets


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pptx")
    ap.add_argument("--outdir", default=None)
    ap.add_argument("--dpi", type=int, default=60)
    ap.add_argument("--per-sheet", type=int, default=9)
    ap.add_argument("--cols", type=int, default=3)
    ap.add_argument("--no-pdf", action="store_true", help="reuse an existing PDF next to the deck")
    a = ap.parse_args()
    pptx = Path(a.pptx).resolve()
    outdir = Path(a.outdir or pptx.parent / f"{pptx.stem}_render").resolve()
    outdir.mkdir(parents=True, exist_ok=True)
    for old in glob.glob(str(outdir / "page-*.png")) + glob.glob(str(outdir / "sheet_*.png")):
        os.remove(old)
    used = fonts_in_deck(pptx)
    missing = prepare_profile(used)
    pdf = pptx.with_suffix(".pdf") if a.no_pdf else export_pdf(pptx, pptx.parent)
    pages, sheets = contact_sheets(pdf, outdir, a.dpi, a.per_sheet, a.cols)
    embedded = pdf_fonts(pdf)
    print(f"PDF: {pdf}")
    print(f"pages: {len(pages)} in {outdir}")
    for s in sheets:
        print(f"sheet: {s}")
    print(f"fonts in deck: {', '.join(sorted(used))}")
    print(f"fonts in PDF:  {', '.join(embedded)}")
    if missing:
        print(f"WARNING no font file found for: {', '.join(missing)} (the PDF uses a substitute)")
    flat = " ".join(embedded).replace("-", "").lower()
    for fam in used:
        if fam.replace(" ", "").lower() not in flat:
            print(f"WARNING '{fam}' is not embedded in the PDF; check the render for a substitute font")


if __name__ == "__main__":
    sys.exit(main())
