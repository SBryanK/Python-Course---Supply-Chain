"""Write a self-contained build script for a new deck: pptkit pasted in, the chosen theme
embedded, and a skeleton build() to fill with the real slides.

Usage:
    python new_deck.py --theme A --format video --out /path/build_deck.py --deck-name Group10_deck
                       [--tone soft|regular|hard] [--align left|center] [--logo nus|/path/logo.png]

A logo is copied into an "assets" folder next to the build script, so the script keeps working
without the skill. Put photos for the deck in the same folder (fetch_image.py get --out that folder).

The output script needs only python-pptx, lxml and pillow, so it can be rerun
later without the skill (for example when a number changes).
"""

import argparse
import json
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent

SKELETON = '''

THEME = {theme}
FORMAT = "{fmt}"
TONE = "{tone}"
ALIGN = "{align}"
HERE = Path(__file__).resolve().parent
ASSETS = HERE / "assets"
LOGO = {logo}
OUT = HERE / "{deck}.pptx"


def build():
    d = Deck(THEME, FORMAT, align=ALIGN, tone=TONE, logo=LOGO)

    d.cover("Project title", course=["Course code and name", "University"], group="Group N",
            members=[("Name", "Student ID")],
            notes="Opening lines, as you would say them.", speaker="Name", seconds=15)

    d.questions("Research questions and approach",
                [("Question 1", "..."), ("Question 2", "...")],
                steps=[("Look", "..."), ("Model", "..."), ("Test", "..."), ("Forecast", "...")],
                steps_title="Approach", speaker="Name",
                notes="...", seconds=20)

    def draw_main(deck, slide, x, y, w, h):
        deck.line_chart(slide, x, y, w, h, ["2024", "2025", "2026"], {{"Actual": [1, 2, 3]}})

    d.chart_stats("A title that states the finding", draw_main,
                  stats=[("1.0 m", "what the number means, in a few words")],
                  source="Data: source name, year", speaker="Name", notes="...", seconds=30)

    d.thanks("Thank you", subtitle="Project title", members_line="Group N  ·  names")
    return d


def export_pdf(path):
    soffice = shutil.which("soffice") or "/Applications/LibreOffice.app/Contents/MacOS/soffice"
    if not Path(soffice).exists():
        print("LibreOffice not found: export the PDF from PowerPoint (File, Export, PDF).")
        return
    subprocess.run([soffice, "--headless", "--convert-to", "pdf", "--outdir", str(path.parent), str(path)],
                   check=True, capture_output=True, timeout=300)
    print("PDF:", path.with_suffix(".pdf"))


if __name__ == "__main__":
    deck = build()
    deck.save(OUT)
    print("PPTX:", OUT)
    if "--pdf" in sys.argv:
        export_pdf(OUT)
'''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--theme", required=True)
    ap.add_argument("--format", default="video", choices=["video", "live", "read"])
    ap.add_argument("--out", required=True)
    ap.add_argument("--deck-name", default="deck")
    ap.add_argument("--title", default="the deck")
    ap.add_argument("--tone", default="regular", choices=["soft", "regular", "hard"])
    ap.add_argument("--align", default=None, choices=["left", "center"])
    ap.add_argument("--logo", default=None)
    ap.add_argument("--head-font")
    ap.add_argument("--body-font")
    a = ap.parse_args()
    themes = json.loads((HERE.parent / "assets" / "themes.json").read_text())
    theme = dict(themes[a.theme.upper()])
    if a.head_font:
        theme["head"] = a.head_font
    if a.body_font:
        theme["body"] = a.body_font
    out_dir = Path(a.out).resolve().parent
    logo_expr = "None"
    if a.logo:
        src = HERE.parent / "assets" / "logos" / "nus_crest.png" if a.logo == "nus" else Path(a.logo)
        (out_dir / "assets").mkdir(parents=True, exist_ok=True)
        shutil.copy(src, out_dir / "assets" / src.name)
        logo_expr = f'str(ASSETS / "{src.name}")'
    kit = (HERE / "pptkit.py").read_text()
    kit = kit.split('"""', 2)[2].lstrip("\n")
    header = (f'"""Build {a.title}.\n\nRun:  python {Path(a.out).name}        (add --pdf to export a PDF with LibreOffice)\n'
              'Needs: pip install python-pptx lxml pillow\n\n'
              'The slides are written in build() at the bottom. The drawing code above it\n'
              'keeps every text box, chart and table editable in PowerPoint.\n"""\n\n'
              'import shutil\nimport subprocess\nimport sys\nfrom pathlib import Path\n')
    align = a.align or theme.get("align", "left")
    body = SKELETON.format(theme=json.dumps(theme, indent=4), fmt=a.format, deck=a.deck_name, tone=a.tone,
                           align=align, logo=logo_expr)
    Path(a.out).write_text(header + kit + body)
    print(f"wrote {a.out} (theme {a.theme.upper()} {theme['name']}, {a.tone}, {align}, format {a.format})")


if __name__ == "__main__":
    main()
