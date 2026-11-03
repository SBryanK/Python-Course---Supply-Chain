"""Shared deck kit for the Python for Supply Chain course decks.

One theme for every deck: L (Maritime blue), soft tone, left aligned, live format,
no logo, no photos. Code is set in DejaVu Sans Mono (shipped in _tools/fonts).

Slide helpers keep every deck on the same grid:
  cover, question, concept, code_slide, code_compare, errors_slide,
  finding_chart, table_slide, section, now_in_colab, recap, homework.
"""
import json
import sys
from pathlib import Path

from pptx.util import Inches, Pt

ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / "_tools" / "ppt_maker" / "ppt-maker"
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


def _label(d, slide, x, y, text):
    d.text(slide, x, y, 4.5, 0.28, text.upper(), size=d.s["label"], bold=True,
           color=d.t["accent"], head=True, name="label")


def cover(d, title, session_no, date, notes, seconds=20):
    d.cover(title, course=["Python for Supply Chain", f"Session {session_no}  ·  {date}"],
            group=None, members=(), notes=notes, speaker="Bryan", seconds=seconds)


def question(d, text, notes, seconds=40, kicker="Today's question"):
    s = d.new_slide()
    y = d.title(s, kicker)
    d.text(s, M, y + 0.55, CW, 2.0, text, size=44, bold=True, head=True, color=d.t["accent"])
    d.footer(s)
    d.notes(s, notes, "Bryan", seconds)
    return s


def concept(d, title, daily, excel, limit, code, notes, seconds=75, code_size=15):
    """One concept: title, daily life, Excel bridge, 3 to 6 code lines, the limit."""
    s = d.new_slide()
    y = d.title(s, title)
    top = y + 0.12
    left_w = 4.5
    _label(d, s, M, top, "In daily life")
    d.text(s, M, top + 0.34, left_w, 0.9, daily, size=d.s["body"], name="daily")
    _label(d, s, M, top + 1.55, "In Excel")
    d.text(s, M, top + 1.89, left_w, 0.9, excel, size=d.s["body"], name="excel")
    _label(d, s, M, top + 2.95, "The limit")
    d.text(s, M, top + 3.29, left_w, 1.2, limit, size=d.s["body"], color=d.t["accent"], name="limit")
    px, py, pw, ph = M + 4.75, top - 0.02, CW - 4.75, 4.72
    d.rect(s, px, py, pw, ph, d.t["card2"], name="code_panel")
    d.rect(s, px, py, 0.06, ph, d.t["fill"], rounded=False, name="code_bar")
    _mono(d, s, px + 0.3, py + 0.24, pw - 0.55, ph - 0.4, code, size=code_size)
    d.footer(s)
    d.notes(s, notes, "Bryan", seconds)
    return s


def code_slide(d, title, intro, code, notes, seconds=60, code_size=15):
    """A slide whose point is a short block of code."""
    s = d.new_slide()
    y = d.title(s, title)
    if intro:
        d.text(s, M, y, 4.5, 1.9, intro, size=d.s["body"], name="intro")
    px = M + 4.75 if intro else M
    pw = CW - 4.75 if intro else CW
    d.rect(s, px, y - 0.02, pw, 4.5, d.t["card2"], name="code_panel")
    d.rect(s, px, y - 0.02, 0.06, 4.5, d.t["fill"], rounded=False, name="code_bar")
    _mono(d, s, px + 0.3, y + 0.22, pw - 0.55, 4.1, code, size=code_size)
    d.footer(s)
    d.notes(s, notes, "Bryan", seconds)
    return s


def code_compare(d, title, left_label, left_code, right_label, right_code, notes, seconds=70):
    """Two code panels side by side, for showing SQL next to pandas."""
    s = d.new_slide()
    y = d.title(s, title)
    gap = 0.3
    w = (CW - gap) / 2
    for i, (label, code) in enumerate(((left_label, left_code), (right_label, right_code))):
        x = M + i * (w + gap)
        d.text(s, x, y, w, 0.34, label, size=d.s["h"], bold=True, color=d.t["accent"], head=True)
        d.rect(s, x, y + 0.42, w, 4.35, d.t["card2"], name=f"panel{i}")
        d.rect(s, x, y + 0.42, 0.06, 4.35, d.t["fill"], rounded=False, name=f"bar{i}")
        _mono(d, s, x + 0.28, y + 0.62, w - 0.5, 4.0, code, size=14)
    d.footer(s)
    d.notes(s, notes, "Bryan", seconds)
    return s


def errors_slide(d, title, rows, bottom, notes, seconds=60):
    """A native table of errors and what each one means."""
    return d.table_slide(title, rows, below=bottom, notes=notes, speaker="Bryan", seconds=seconds)


def finding_chart(d, title, draw, stats, notes, source=None, seconds=55, chart_w=7.7):
    """Chart on the left, two or three big numbers on the right."""
    return d.chart_stats(title, draw, stats=stats, source=source, notes=notes,
                         speaker="Bryan", seconds=seconds, chart_w=chart_w)


def table_slide(d, title, rows, notes, seconds=50, below=None, col_widths=None, highlight=()):
    return d.table_slide(title, rows, col_widths=col_widths, highlight=highlight, below=below,
                         notes=notes, speaker="Bryan", seconds=seconds)


def section(d, title, items, notes, seconds=30):
    return d.section(title, items=items, notes=notes, speaker="Bryan", seconds=seconds)


def now_in_colab(d, notebook, notes, seconds=30, items=None):
    if items is None:
        items = [("Notebook", notebook),
                 ("Open from", "Drive > Python for Supply Chain"),
                 ("In class", "Type every cell yourself")]
    return d.section("Now in Colab", items=items, notes=notes, speaker="Bryan", seconds=seconds)


def cards(d, title, cards, notes, seconds=35, cols=None, sub=None, source=None):
    return d.cards(title, cards, cols=cols, sub=sub, source=source, notes=notes,
                   speaker="Bryan", seconds=seconds)


def recap(d, items, notes, seconds=30):
    """Three things she can do now. items: three (heading, short text)."""
    return d.cards("Three things you can do now", [(h, None, t) for h, t in items],
                   cols=3, notes=notes, speaker="Bryan", seconds=seconds)


def homework(d, points, recall, notes, seconds=30):
    return d.two_lists("Homework and daily recall", ("Homework", points), ("Daily recall", recall),
                       notes=notes, speaker="Bryan", seconds=seconds)


def thanks(d, line, subtitle, notes, seconds=15):
    return d.thanks(line, subtitle=subtitle, members_line=None, course="Python for Supply Chain",
                    notes=notes, speaker="Bryan", seconds=seconds)


def strip_speaker_tags(d):
    """Remove the footer speaker name: learner PDFs must not carry a person's name."""
    for slide in d.prs.slides:
        for shape in list(slide.shapes):
            if shape.name == "speaker_tag":
                shape._element.getparent().remove(shape._element)


def save(d, path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    strip_speaker_tags(d)
    d.save(str(path))
    print("PPTX:", path)
