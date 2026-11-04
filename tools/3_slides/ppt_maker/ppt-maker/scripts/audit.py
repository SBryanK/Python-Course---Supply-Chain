"""Check a deck for the problems that show up again and again.

Usage:
    python audit.py deck.pptx [--format video|live|read] [--fonts "Proxima Nova,Montserrat"] [--wpm 130]

Reports, per slide: text under the size floor, text that probably overflows its
box, text boxes that overlap, shapes outside the slide, fonts outside the theme,
too many visible words, and filler words. Then the speaker notes: words and
estimated time per speaker, and slides with no notes. It only warns; read the
render to decide.
"""

import argparse
import math
import re
from collections import defaultdict

from pptx import Presentation
from pptx.util import Emu

FLOOR = {"video": 12, "live": 14, "read": 10}
MAX_WORDS = {"video": 70, "live": 45, "read": 170}
SKIP_NAMES = {"source", "page_no", "speaker_tag", "preview_label", "copyright"}
FILLER = ["delve", "leverage", "seamless", "unlock", "game-changer", "cutting-edge", "tapestry", "journey",
          "in conclusion", "it is important to note", "let's dive", "dive into", "robust and", "empower",
          "holistic", "synergy", "in today's", "ever-evolving", "embark", "revolutionize"]
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿]")


def inches(v):
    return Emu(v or 0).inches


def walk(shapes):
    for sh in shapes:
        yield sh
        if sh.shape_type == 6:
            yield from walk(sh.shapes)


def needed_height(tf, width_in):
    """Rough height a text frame needs: average glyph width about 0.5 em."""
    total = 0.0
    for p in tf.paragraphs:
        sizes = [r.font.size.pt for r in p.runs if r.font.size] or [14]
        size = max(sizes)
        text = "".join(r.text for r in p.runs)
        cpl = max(1, int(width_in * 72 / (size * 0.5)))
        lines = max(1, math.ceil(len(text) / cpl)) if text else 1
        spacing = p.line_spacing if isinstance(p.line_spacing, float) else 1.1
        after = p.space_after.pt if p.space_after is not None else 0
        total += lines * size * 1.2 * spacing / 72 + after / 72
    return total


def overlap(a, b):
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    w = min(ax + aw, bx + bw) - max(ax, bx)
    h = min(ay + ah, by + bh) - max(ay, by)
    return w * h if w > 0 and h > 0 else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pptx")
    ap.add_argument("--format", default="video", choices=FLOOR)
    ap.add_argument("--fonts", default=None, help="comma list of allowed font families")
    ap.add_argument("--wpm", type=int, default=130)
    a = ap.parse_args()
    prs = Presentation(a.pptx)
    sw, sh_ = inches(prs.slide_width), inches(prs.slide_height)
    allowed = {f.strip() for f in a.fonts.split(",")} if a.fonts else None
    floor = FLOOR[a.format]
    issues = 0
    speakers = defaultdict(lambda: [0, 0, []])
    fonts_seen = defaultdict(int)
    print(f"{a.pptx}: {len(prs.slides)} slides, {sw:.2f} x {sh_:.2f} in, format {a.format}, size floor {floor} pt\n")
    for n, slide in enumerate(prs.slides, 1):
        msgs = []
        boxes = []
        words = 0
        text_all = []
        for shp in walk(slide.shapes):
            x, y, w, h = inches(shp.left), inches(shp.top), inches(shp.width), inches(shp.height)
            if shp.shape_type != 9 and (x < -0.01 or y < -0.01 or x + w > sw + 0.01 or y + h > sh_ + 0.01):
                msgs.append(f"'{shp.name}' sits outside the slide ({x:.2f}, {y:.2f}, {w:.2f} x {h:.2f})")
            frames = []
            if shp.has_text_frame:
                frames.append(shp.text_frame)
            if getattr(shp, "has_table", False) and shp.has_table:
                frames += [c.text_frame for row in shp.table.rows for c in row.cells]
            for tf in frames:
                for p in tf.paragraphs:
                    for r in p.runs:
                        if r.font.name:
                            fonts_seen[r.font.name] += 1
                        if (r.font.size and r.font.size.pt < floor and shp.name not in SKIP_NAMES
                                and r.text.strip()):
                            msgs.append(f"{r.font.size.pt:g} pt under the floor in '{shp.name}': \"{r.text.strip()[:50]}\"")
                            break
            if shp.has_text_frame and shp.text_frame.text.strip():
                t = shp.text_frame.text.strip()
                text_all.append(t)
                if shp.name not in SKIP_NAMES:
                    words += len(t.split())
                    boxes.append((shp.name, (x, y, w, h)))
                    need = needed_height(shp.text_frame, w)
                    if need > h + 0.12 and need > h * 1.25:
                        msgs.append(f"text may overflow '{shp.name}': needs about {need:.2f} in, box is {h:.2f} in: \"{t[:50]}\"")
            if getattr(shp, "has_table", False) and shp.has_table:
                words += sum(len(c.text.split()) for row in shp.table.rows for c in row.cells)
        for i in range(len(boxes)):
            for j in range(i + 1, len(boxes)):
                if overlap(boxes[i][1], boxes[j][1]) > 0.04:
                    msgs.append(f"text boxes overlap: '{boxes[i][0]}' and '{boxes[j][0]}'")
        if words > MAX_WORDS[a.format]:
            msgs.append(f"{words} visible words (aim for at most {MAX_WORDS[a.format]} in {a.format} format)")
        low = " ".join(text_all).lower()
        for wd in FILLER:
            if wd in low:
                msgs.append(f"filler phrase on the slide: '{wd}'")
        if EMOJI.search(" ".join(text_all)):
            msgs.append("emoji on the slide")
        notes = slide.notes_slide.notes_text_frame.text.strip() if slide.has_notes_slide else ""
        m = re.match(r"^([A-Z][A-Z .'-]+?)\s*\(about (\d+) seconds\)", notes)
        body = notes.split("\n", 1)[1] if m and "\n" in notes else ("" if m else notes)
        nwords = len(re.sub(r"\[point:[^\]]*\]", "", body).split())
        if m:
            sp = speakers[m.group(1).title()]
            sp[0] += nwords
            sp[1] += int(m.group(2))
            sp[2].append(n)
        elif notes:
            speakers["(no speaker line)"][0] += nwords
            speakers["(no speaker line)"][2].append(n)
        elif a.format != "read":
            msgs.append("no speaker notes")
        if msgs:
            issues += len(msgs)
            print(f"slide {n}:")
            for msg in msgs:
                print(f"  - {msg}")
    print("\nfonts used:", ", ".join(f"{k} ({v})" for k, v in sorted(fonts_seen.items(), key=lambda kv: -kv[1])))
    if allowed:
        extra = [f for f in fonts_seen if f not in allowed]
        if extra:
            issues += 1
            print("  fonts outside the theme:", ", ".join(extra))
    if speakers:
        print(f"\nspeaker notes (at {a.wpm} words a minute):")
        tw = 0
        for name, (wds, secs, slides) in speakers.items():
            tw += wds
            print(f"  {name}: slides {','.join(map(str, slides))}, {wds} words, about {wds / a.wpm:.1f} min"
                  + (f" (header says {secs / 60:.1f} min)" if secs else ""))
        print(f"  total: {tw} words, about {tw / a.wpm:.1f} min")
    print(f"\n{issues} warnings")


if __name__ == "__main__":
    main()
