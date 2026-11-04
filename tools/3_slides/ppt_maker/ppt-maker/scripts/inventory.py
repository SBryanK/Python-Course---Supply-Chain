"""Read an existing deck before refactoring it: every slide's shapes with position, fill,
font sizes and text, the speaker notes, and a summary of fonts, sizes and colours.

Usage:
    python inventory.py deck.pptx [--slides 1-5] > inventory.txt
"""

import argparse
from collections import Counter

from pptx import Presentation


def walk(shapes):
    for sh in shapes:
        yield sh
        if sh.shape_type == 6:
            yield from walk(sh.shapes)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pptx")
    ap.add_argument("--slides", default=None, help="range such as 3-9")
    a = ap.parse_args()
    prs = Presentation(a.pptx)
    lo, hi = 1, len(prs.slides)
    if a.slides:
        lo, hi = (int(v) for v in a.slides.split("-"))
    fonts, sizes, colors, fills = Counter(), Counter(), Counter(), Counter()
    print(f"slide size {prs.slide_width / 914400:.3f} x {prs.slide_height / 914400:.3f} in, {len(prs.slides)} slides")
    for i, s in enumerate(prs.slides, 1):
        show = lo <= i <= hi
        if show:
            print(f"\n=== slide {i} (layout {s.slide_layout.name})")
        for sh in walk(s.shapes):
            fill = ""
            try:
                if sh.fill.type == 1:
                    fill = str(sh.fill.fore_color.rgb)
                    fills[fill] += 1
            except Exception:
                pass
            parts = []
            if sh.has_text_frame:
                for p in sh.text_frame.paragraphs:
                    for r in p.runs:
                        if r.font.name:
                            fonts[r.font.name] += 1
                        if r.font.size:
                            sizes[r.font.size.pt] += 1
                        try:
                            if r.font.color and r.font.color.type is not None:
                                colors[str(r.font.color.rgb)] += 1
                        except Exception:
                            pass
                    sz = sorted({r.font.size.pt for r in p.runs if r.font.size})
                    bold = any(r.font.bold for r in p.runs)
                    if p.text.strip():
                        parts.append(f"[{'/'.join(f'{v:g}' for v in sz)}{'B' if bold else ''}] {p.text.strip()[:140]}")
            kind = str(sh.shape_type).split(".")[-1].split(" ")[0]
            if show:
                x = (sh.left or 0) / 914400
                y = (sh.top or 0) / 914400
                w = (sh.width or 0) / 914400
                h = (sh.height or 0) / 914400
                extra = " | ".join(parts)
                if kind.startswith("PICTURE"):
                    extra = "(picture)"
                print(f"  {kind:10} {sh.name[:20]:20} x{x:5.2f} y{y:5.2f} w{w:5.2f} h{h:5.2f} {fill:6} {extra[:500]}")
        if show and s.has_notes_slide:
            n = s.notes_slide.notes_text_frame.text.strip()
            if n:
                print(f"  NOTES ({len(n.split())} words): {n[:600]}")
    print("\nfonts:", fonts.most_common(10))
    print("sizes:", sorted(sizes.items()))
    print("text colours:", colors.most_common(10))
    print("fills:", fills.most_common(12))


if __name__ == "__main__":
    main()
