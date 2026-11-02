"""Build the same three preview slides (opening, questions or agenda, one result slide)
in several themes, export a PDF, and make one contact sheet with one row per theme.

Usage:
    python preview_themes.py spec.json --themes A,B:hard,C:soft,E:center,I [--format video] --out /path/preview.pptx

Each entry is THEME[:soft|regular|hard][:left|center], so one preview can compare tones and alignment too.

spec.json:
{
  "logo": "nus" or "/path/logo.png" (optional; "nus" is the bundled crest),
  "cover":  {"title": "...", "course": ["line 1", "line 2"], "group": "Group 10",
             "members": [["Bryan", "A0..."], ...], "image": "/path/photo.jpg" (optional), "notes": "..."},
  "agenda": {"title": "...", "questions": [["Question 1", "..."], ...],
             "steps_title": "Approach", "steps": [["Look", "..."], ...], "notes": "..."},
  "result": {"title": "...", "sub": null,
             "chart": {"type": "line" or "bar", "categories": [...], "series": {"name": [...]},
                       "dashed": ["name"], "number_format": "0.0", "label_every": 6, "horizontal": false},
             "stats": [["17.02 m", "label"], ...], "source": "...", "notes": "..."}
}
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from pptkit import Deck, SLIDE_W, M  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("--themes", default="A,B,C,D,E")
    ap.add_argument("--format", default="video", choices=["video", "live", "read"])
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    spec = json.loads(Path(a.spec).read_text())
    themes = json.loads((HERE.parent / "assets" / "themes.json").read_text())
    logo = spec.get("logo")
    if logo == "nus":
        logo = str(HERE.parent / "assets" / "logos" / "nus_crest.png")
    entries = [e.strip() for e in a.themes.split(",") if e.strip()]
    first = None
    for entry in entries:
        parts = entry.split(":")
        tid = parts[0].upper()
        tone = next((p for p in parts[1:] if p in ("soft", "regular", "hard")), "regular")
        align = next((p for p in parts[1:] if p in ("left", "center")), None)
        d = Deck(themes[tid], a.format, align=align, tone=tone, logo=logo)
        if first is None:
            first = d
        else:
            d.prs, d.page = first.prs, first.page
        t = themes[tid]
        tag = f"Theme {tid} · {t['name']} · {tone} · {d.align}"
        c, g, r = spec["cover"], spec["agenda"], spec["result"]
        s1 = d.cover(c["title"], course=c.get("course"), group=c.get("group"),
                     members=[m if isinstance(m, str) else tuple(m) for m in c.get("members", [])], image=c.get("image"), notes=c.get("notes"))
        s2 = d.questions(g["title"], [tuple(q) for q in g["questions"]],
                         steps=[tuple(x) for x in g.get("steps", [])] or None,
                         steps_title=g.get("steps_title"), notes=g.get("notes"))
        ch = r["chart"]

        def draw(deck, slide, x, y, w, h, ch=ch):
            if ch.get("type", "line") == "bar":
                deck.bar_chart(slide, x, y, w, h, ch["categories"], ch["series"],
                               horizontal=ch.get("horizontal", False), number_format=ch.get("number_format", "0.0"))
            else:
                deck.line_chart(slide, x, y, w, h, ch["categories"], ch["series"], dashed=ch.get("dashed", ()),
                                number_format=ch.get("number_format"), label_every=ch.get("label_every", 1))

        s3 = d.chart_stats(r["title"], draw, stats=[tuple(x) for x in r.get("stats", [])], sub=r.get("sub"),
                           source=r.get("source"), notes=r.get("notes"))
        for sl in (s1, s2, s3):
            d.text(sl, SLIDE_W - M - 4.6, 0.08, 4.6, 0.25, tag, size=9, color=d.t["muted"] if sl is not s1 else d.t["cover_ink"],
                   align="right", name="preview_label")
        first.page = d.page
    first.save(a.out)
    print("PPTX:", a.out)
    subprocess.run([sys.executable, str(HERE / "render.py"), a.out, "--per-sheet", str(3 * len(entries)), "--cols", "3",
                    "--dpi", "50"], check=True)


if __name__ == "__main__":
    main()
