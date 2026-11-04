"""Shared deck kit for the Python for Supply Chain course decks.

Session decks use the lecture look: cream, navy and one orange, a title and one visual
anchor per slide, the wavy route on the cover and Thank you slides. Code is set in
DejaVu Sans Mono (shipped in tools/3_slides/fonts). new_deck() is the plain theme L deck
used by the presentation template.
"""
import json
import sys
from pathlib import Path

from pptx.util import Inches, Pt

ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / "tools" / "3_slides" / "ppt_maker" / "ppt-maker"
sys.path.insert(0, str(SKILL / "scripts"))

from pptkit import Deck, M, CW, FOOT_Y, rgb  # noqa: E402

THEMES = json.loads((SKILL / "assets" / "themes.json").read_text())
MONO = "DejaVu Sans Mono"


def new_deck():
    return Deck(THEMES["L"], "live", align="left", tone="soft", logo=None)


def _mono(d, slide, x, y, w, h, lines, size=15, color=None, after=4):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.line_spacing = 1.0
        p.space_after = Pt(after)
        run = p.add_run()
        run.text = line
        run.font.name = MONO
        run.font.size = Pt(size)
        run.font.bold = False
        run.font.color.rgb = rgb(color or d.t["ink"])
    return box


def strip_speaker_tags(d):
    """Remove the footer speaker name: learner PDFs must not carry a person's name."""
    for slide in d.prs.slides:
        for shape in list(slide.shapes):
            if shape.name == "speaker_tag":
                shape._element.getparent().remove(shape._element)


# ---------- Lecture look: cream, navy, one orange; theory on slides, practice in Colab ----------

from pptx.enum.shapes import MSO_SHAPE  # noqa: E402
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN  # noqa: E402
from pptkit import SLIDE_W, _plain  # noqa: E402

CREAM, SAND, NAVY, MUTED = "FBF8F3", "F2ECE1", "14213D", "6F6A60"
ORANGE, ORANGE_TEXT, PEACH = "C2501C", "B4471A", "F7DCCB"
SKY, GOLD, CODE_INK, CODE_OUT = "9DB4C8", "E3A53B", "F4EFE6", "F2B279"

ROUTE = dict(THEMES["L"], name="Route", bg=CREAM, card=SAND, card2="FFFFFF", ink=NAVY, muted=MUTED,
             accent=ORANGE_TEXT, fill=NAVY, on_fill="FFFFFF", rule=ORANGE, highlight=PEACH,
             cover_bg=CREAM, cover_ink=NAVY, series=[NAVY, ORANGE, SKY, GOLD])


def shape_text(shp, text, size, color, bold=False, mono=False, align="center", font=None):
    """Put centred text inside a shape (a chip, a stop, a step)."""
    tf = shp.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.08 if align == "left" else 0.02)
    tf.margin_top = tf.margin_bottom = Inches(0.02)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.alignment = {"left": PP_ALIGN.LEFT, "center": PP_ALIGN.CENTER}[align]
    r = p.add_run()
    r.text = text
    r.font.name = MONO if mono else (font or ROUTE["body"])
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.color.rgb = rgb(color)
    return shp


def chip(d, s, x, y, w, h, text, fill, color, size=16, bold=False, mono=False, line=None, name=None):
    shp = d.rect(s, x, y, w, h, fill, line=line, name=name)
    return shape_text(shp, text, size, color, bold=bold, mono=mono)


def stop(d, s, x, y, dia, text, fill, color, size=14, line=None):
    shp = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x), Inches(y), Inches(dia), Inches(dia))
    shp.fill.solid()
    shp.fill.fore_color.rgb = rgb(fill)
    if line:
        shp.line.color.rgb = rgb(line)
        shp.line.width = Pt(1.5)
    else:
        shp.line.fill.background()
    _plain(shp)
    return shape_text(shp, text, size, color, bold=True)


def arrow(d, s, x, y, w, h, fill=MUTED):
    shp = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(x), Inches(y), Inches(w), Inches(h))
    shp.fill.solid()
    shp.fill.fore_color.rgb = rgb(fill)
    shp.line.fill.background()
    _plain(shp)
    return shp


BODY = 18          # body text on lecture slides
TOP = 1.45         # first content row under the title
WHITE = "FFFFFF"
MID = M + CW / 2   # horizontal centre of the content area

NAMES = ["Hello, Python", "Shelves, cards, choices", "Let the loop walk", "Cleaning day", "Star products",
         "Numbers talk", "New tools", "Detective work", "Polish and publish", "Showtime"]
DATES = ["Mon 16 Nov", "Wed 18 Nov", "Mon 23 Nov", "Thu 26 Nov", "Mon 30 Nov", "Thu 3 Dec", "Mon 7 Dec",
         "Thu 10 Dec", "Mon 14 Dec", "Thu 17 Dec"]
QUESTIONS = ["What is one order line worth?", "Which order lines are big?", "Can one rule label every line?",
             "What does clean data look like?", "Who are the star products?", "How do the numbers talk?",
             "What will your project ask?", "Detective work on your question", "Can you say it in three sentences?",
             "Explain it like an analyst"]


def cols(n, gap=0.3, w=CW, x=M):
    """x positions and width for n equal columns."""
    cw = (w - gap * (n - 1)) / n
    return [x + i * (cw + gap) for i in range(n)], cw


def centred(total_w):
    """x that centres something total_w wide in the content area."""
    return MID - total_w / 2


def muted(d, s, y, text, size=18):
    """One short grey line across the content area, centred."""
    label(d, s, M, y, CW, 0.4, text, size=size, color=MUTED, name="line")


def lecture_deck(session_no):
    """Theory slides: one concept per slide, read like lecture notes. The notebook is the playground."""
    d = Deck(ROUTE, "live", align="left", tone="regular", logo=None)
    d.session = session_no
    d.prs.core_properties.keywords = "lecture"
    return d


COPYRIGHT = "© 2026 Santasila Bryan Kusno. All rights reserved."


def copyright_line(d, s, right=SLIDE_W - M - 0.65):
    """The copyright line, bottom right, just left of the page number."""
    d.text(s, right - 6.0, 6.98, 6.0, 0.3, COPYRIGHT, size=11, color=MUTED, align="right", name="copyright")


def slide(d, title, notes, seconds=60):
    """Title, page number and copyright. Returns (slide, y where content starts)."""
    s = d.new_slide()
    d.text(s, M, 0.55, CW, 0.6, title, size=32, bold=True, head=True, spacing=1.0, name="title")
    d.footer(s)
    copyright_line(d, s)
    d.notes(s, notes, "Bryan", seconds)
    return s, TOP


def text_h(d, items, size, w, gap=8):
    return sum(d._text_h(t, size, w) + gap / 72 for t in items)


def para(d, s, x, y, w, text, size=BODY, color=NAVY, name="para"):
    """One plain paragraph; **stars** mark bold. Returns the y below it."""
    h = d._text_h(text, size, w) + 0.05
    d.text(s, x, y, w, h, text, size=size, color=color, name=name)
    return y + h + 0.12


def bullets(d, s, x, y, w, items, size=BODY, gap=8, name="bullets"):
    """Bullet list, one line or two per item. Returns the y below it."""
    lines = ["•  " + t for t in items]
    h = text_h(d, lines, size, w, gap) + 0.05
    d.text(s, x, y, w, h, [{"text": t, "after": gap} for t in lines], size=size, color=NAVY, name=name)
    return y + h + 0.1


def box(d, s, x, y, w, text, size=17):
    """A plain box with a full border, for the one thing on a slide that must not be missed."""
    lines = max(1, round(d._text_h(text, size, w - 0.6) / (size * 1.25 / 72)))
    h = lines * size * 1.2 / 72 + 0.4
    shp = d.rect(s, x, y, w, h, "FFFFFF", line=ORANGE, name="box")
    shp.line.width = Pt(1.5)
    d.text(s, x + 0.3, y, w - 0.6, h, text, size=size, color=NAVY, anchor="middle", align="center",
           spacing=1.0, after=0, name="box_text")
    return y + h + 0.2


def label(d, s, x, y, w, h, text, size=18, color=NAVY, bold=False, mono=False, align="center",
          anchor="middle", name="label"):
    """Short text, centred by default; mono for code."""
    box = d.text(s, x, y, w, h, text, size=size, color=color, bold=bold, align=align, anchor=anchor,
                 spacing=1.0, after=0, name=name)
    if mono:
        for p in box.text_frame.paragraphs:
            for r in p.runs:
                r.font.name = MONO
    return box


def tile(d, s, x, y, w, h, head, sub=None, fill=SAND, head_color=NAVY, head_size=22, mono=False, sub_size=16,
         sub_color=MUTED, line=None, sub_mono=False, name="tile"):
    """A card with a big head line and a short line under it, both centred in the card."""
    shp = d.rect(s, x, y, w, h, fill, line=line, name=name)
    if line:
        shp.line.width = Pt(1.5)
    hh = head_size / 72 * 1.25
    sh = (sub_size / 72 * 1.25 * max(1, round(d._text_h(sub, sub_size, w - 0.4) / (sub_size * 1.25 / 72))))
    sh = sh if sub else 0
    top = y + (h - hh - (sh + 0.1 if sub else 0)) / 2
    label(d, s, x + 0.15, top, w - 0.3, hh, head, size=head_size, color=head_color, bold=not mono, mono=mono,
          name=f"{name}_h")
    if sub:
        label(d, s, x + 0.2, top + hh + 0.1, w - 0.4, sh, sub, size=sub_size, color=sub_color, mono=sub_mono,
              anchor="top", name=f"{name}_s")
    return shp


def ltable(d, s, x, y, w, rows, col_widths, code_cols=(), size=16, row_h=None):
    """Native table; code columns are set in the mono font. Returns the y below it."""
    row_h = row_h or 0.44
    tbl = d.table(s, x, y, w, rows, col_widths=col_widths, row_h=row_h, size=size)
    for i in range(1, len(rows)):
        for j in range(len(rows[0])):
            tbl.cell(i, j).text_frame.paragraphs[0].alignment = PP_ALIGN.LEFT
        for j in code_cols:
            for r in tbl.cell(i, j).text_frame.paragraphs[0].runs:
                r.font.name = MONO
                r.font.size = Pt(size - 1)
            tbl.cell(i, j).text_frame.paragraphs[0].alignment = PP_ALIGN.LEFT
    return y + row_h * len(rows) + 0.2


def code_card(d, s, x, y, w, lines, output=None, size=15, name="code"):
    """Dark code card sized to its code, with the output under a thin line."""
    lh = size * 1.32 / 72
    h = 0.5 + len(lines) * lh + ((0.25 + len(output) * lh) if output else 0)
    d.rect(s, x, y, w, h, NAVY, name=f"{name}_card")
    _mono(d, s, x + 0.28, y + 0.25, w - 0.5, len(lines) * lh, lines, size=size, color=CODE_INK, after=2)
    if output:
        oy = y + 0.25 + len(lines) * lh + 0.08
        d.line(s, x + 0.28, oy, x + w - 0.28, oy, color="3A4A66", width=0.75)
        _mono(d, s, x + 0.28, oy + 0.12, w - 0.5, len(output) * lh, ["→ " + o for o in output],
              size=size, color=CODE_OUT, after=2)
    return y + h


def big_number(d, s, x, y, w, value, label, color=ORANGE_TEXT, size=60):
    vh = size / 72 * 1.15
    d.text(s, x, y, w, vh, value, size=size, bold=True, head=True, color=color, spacing=1.0, name="big")
    d.text(s, x, y + vh + 0.02, w, 0.4, label, size=18, color=MUTED, name="big_label")
    return y + vh + 0.45


def route_cover(d, title, subtitle, date, names, notes, seconds=20):
    """Cover: the course as a route of ten stops; today is the big orange stop."""
    s = d.new_slide()
    d.text(s, M, 0.55, 9, 0.35, "PYTHON FOR SUPPLY CHAIN", size=16, bold=True, color=ORANGE_TEXT, head=True,
           name="course")
    d.text(s, M, 0.92, 9, 0.35, f"Session {d.session}  ·  {date}", size=18, color=MUTED, name="date")
    d.text(s, M, 1.75, CW, 1.1, title, size=64, bold=True, head=True, spacing=1.0, name="cover_title")
    d.text(s, M, 2.95, 9.5, 0.5, subtitle, size=24, color=MUTED, name="cover_sub")
    route_map(d, s, names[d.session - 1])
    copyright_line(d, s, right=SLIDE_W - M)
    d.notes(s, notes, "Bryan", seconds)
    return s


def route_map(d, s, text, highlight=None, done=None):
    """The ten sessions as a road going up; the highlighted stop is big and orange."""
    highlight = highlight or d.session
    done = d.session if done is None else done
    import math
    pts = [(1.0 + i * (SLIDE_W - 2.0) / 9, 5.45 + 0.42 * math.sin(i * 0.95)) for i in range(10)]
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        d.line(s, x1, y1, x2, y2, color=SKY, width=2.5, dash=True)
    for i, (x, y) in enumerate(pts, 1):
        if i == highlight:
            stop(d, s, x - 0.42, y - 0.42, 0.84, str(i), ORANGE, "FFFFFF", size=26)
        elif i <= done:
            stop(d, s, x - 0.28, y - 0.28, 0.56, str(i), NAVY, "FFFFFF", size=15)
        else:
            stop(d, s, x - 0.28, y - 0.28, 0.56, str(i), CREAM, NAVY, size=15, line=SKY)
    x, y = pts[highlight - 1]
    near = [py for i, (_, py) in enumerate(pts) if abs(i - (highlight - 1)) == 1]
    ly = max([y + 0.55] + [py + 0.34 for py in near])   # clear of the stop and its neighbours
    lx = min(max(x - 1.5, 0.3), SLIDE_W - 3.3)   # stays on the slide at the first and last stop
    label(d, s, lx, ly, 3.0, 0.4, text, size=16, bold=True, color=ORANGE_TEXT, name="today")


def thanks_slide(d, lines, notes, seconds=20):
    """Closing slide: thank you, the next session on its own lines, and the road with the next stop lit.

    After the last session the road is complete and stop 10 is lit as the finish.
    """
    s = d.new_slide()
    d.text(s, M, 0.9, CW, 1.1, "Thank you", size=64, bold=True, head=True, spacing=1.0, name="thanks")
    d.text(s, M, 2.1, 8, 1.4, [{"text": lines[0], "bold": True, "color": ORANGE_TEXT, "size": 18, "after": 6},
                               {"text": lines[1], "size": 26, "bold": True, "after": 4},
                               {"text": lines[2], "color": MUTED}],
           size=20, color=NAVY, name="next")
    if d.session < 10:
        route_map(d, s, "next", highlight=d.session + 1, done=d.session)
    else:
        route_map(d, s, "finish", highlight=10, done=10)
    copyright_line(d, s, right=SLIDE_W - M)
    d.notes(s, notes, "Bryan", seconds)
    return s


def cover_for(d, subtitle, notes):
    """The cover for this session, from the course names and dates."""
    return route_cover(d, NAMES[d.session - 1], subtitle, f"{DATES[d.session - 1]} 2026", NAMES, notes)


def thanks_next(d, notes):
    """The Thank you slide that points at the next session."""
    n = d.session + 1
    return thanks_slide(d, [f"Next: Session {n}", QUESTIONS[n - 1], DATES[n - 1]], notes)


def ladder(d, s, x, y, w, h, steps):
    """Exercise ladder: rising steps (label, count), the last one in orange."""
    n = len(steps)
    gap = 0.12
    sw = (w - gap * (n - 1)) / n
    for i, (label, count) in enumerate(steps):
        sh = h * (0.4 + 0.6 * (i + 1) / n)
        sx, sy = x + i * (sw + gap), y + h - sh
        last = i == n - 1
        d.rect(s, sx, sy, sw, sh, ORANGE if last else NAVY, name=f"step{i}")
        d.text(s, sx + 0.15, sy + 0.15, sw - 0.3, 0.8, str(count), size=40, bold=True, head=True,
               color="FFFFFF", name=f"step{i}_n")
        d.text(s, sx, y + h + 0.1, sw, 0.35, label, size=16, bold=True, color=NAVY, align="center",
               name=f"step{i}_l")


def save(d, path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    strip_speaker_tags(d)
    d.save(str(path))
    print("PPTX:", path)
