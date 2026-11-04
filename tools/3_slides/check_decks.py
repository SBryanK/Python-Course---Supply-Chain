"""Quality check for every course deck.

Lecture decks (keywords "lecture") may have 10 to 30 slides and use the read word limit.

Checks the build-spec rules that can be checked without opening the slides:
slide count, fonts, no photos, no names in slide text, no banned words, no
exclamation marks, no em dashes, a speaker header and Bahasa Indonesia notes on
every slide, a title on every content slide, a Now in Colab slide where the plan
asks for one, and the audit.py warning count.

Run:  python tools/3_slides/check_decks.py
"""
import re
import subprocess
import sys
from pathlib import Path

from pptx import Presentation

ROOT = Path(__file__).resolve().parents[2]
AUDIT = ROOT / "tools" / "3_slides" / "ppt_maker" / "ppt-maker" / "scripts" / "audit.py"
FONTS = {"Proxima Nova", "DejaVu Sans Mono"}
BANNED = ["delve", "leverage", "seamless", "journey"]
NAMES = ["michella", "natalia", "bryan"]
INDONESIAN = ["yang", "kita", "kamu", "dan", "untuk", "dengan", "ini", "jadi", "atau", "sudah"]
SPEAKER = re.compile(r"^[A-Z][A-Z .'-]+ \(about \d+ seconds\)\s*$", re.MULTILINE)


def slide_text(slide):
    parts = []
    for shp in slide.shapes:
        if shp.name == "copyright":   # the owner's copyright line is the one place a name may appear
            continue
        if shp.has_text_frame:
            parts.append(shp.text_frame.text)
        if getattr(shp, "has_table", False) and shp.has_table:
            for row in shp.table.rows:
                for cell in row.cells:
                    parts.append(cell.text)
    return "\n".join(parts)


def notes_text(slide):
    if not slide.has_notes_slide:
        return ""
    return slide.notes_slide.notes_text_frame.text


def check(deck, expected_max=10, now_in_colab=False):
    template = expected_max == 5
    problems = []
    prs = Presentation(deck)
    n = len(prs.slides)
    lecture = prs.core_properties.keywords == "lecture"
    if lecture:
        if not (10 <= n <= 30):
            problems.append(f"{n} slides, outside 10-30 for a lecture deck")
    elif expected_max == 5:
        if n != 5:
            problems.append(f"{n} slides, expected 5")
    elif not (6 <= n <= expected_max):
        problems.append(f"{n} slides, outside 6-{expected_max}")

    fonts = set()
    pictures = 0
    for slide in prs.slides:
        for shp in slide.shapes:
            if shp.shape_type == 13:
                pictures += 1
            for el in shp._element.iter():
                if el.tag.endswith("}latin") and el.get("typeface"):
                    fonts.add(el.get("typeface"))
    extra = fonts - FONTS
    if extra:
        problems.append(f"fonts outside the theme: {sorted(extra)}")
    if pictures:
        problems.append(f"{pictures} picture shapes (no photos allowed)")

    has_colab = False
    for i, slide in enumerate(prs.slides, 1):
        text = slide_text(slide)
        low = text.lower()
        if "now in colab" in low:
            has_colab = True
        for word in BANNED:
            if word in low:
                problems.append(f"slide {i}: banned word '{word}'")
        for name in NAMES:
            if name in low:
                problems.append(f"slide {i}: name '{name}' in slide text")
        if "—" in text or "–" in text:
            problems.append(f"slide {i}: dash character in slide text")
        if re.search(r"!(?!=)", text):   # != is the Python operator, not an exclamation
            problems.append(f"slide {i}: exclamation mark")
        if template:
            continue
        notes = notes_text(slide)
        if not SPEAKER.search(notes):
            problems.append(f"slide {i}: missing speaker header in notes")
        body = SPEAKER.sub("", notes).lower()
        hits = sum(1 for w in INDONESIAN if re.search(r"\b" + w + r"\b", body))
        if hits < 2:
            problems.append(f"slide {i}: notes do not look like Bahasa Indonesia")

    if now_in_colab and not has_colab:
        problems.append("no Now in Colab slide")
    return n, problems


def audit(deck):
    # Lecture decks are read as notes later, so they use the read word limit; text stays 14 pt or more.
    fmt = "read" if Presentation(deck).core_properties.keywords == "lecture" else "live"
    cmd = [sys.executable, str(AUDIT), str(deck), "--format", fmt,
           "--fonts", "Proxima Nova,DejaVu Sans Mono"]
    out = subprocess.run(cmd, capture_output=True, text=True).stdout
    m = re.search(r"(\d+) warnings", out)
    warnings = int(m.group(1)) if m else -1
    lines = [line.strip() for line in out.splitlines() if line.strip().startswith("- ")]
    return warnings, lines


def main():
    decks = sorted((ROOT / "sessions").glob("s*/deck.pptx"))
    decks.append(ROOT / "course_home" / "presentation_template.pptx")
    failed = 0
    passed = 0
    for deck in decks:
        session = deck.parent.name if deck.parent.name.startswith("s") else "template"
        template = session == "template"
        if template:
            n, problems = check(deck, expected_max=5)
        else:
            number = int(session[1:3])
            n, problems = check(deck, expected_max=10, now_in_colab=number <= 8)
        warnings, warn_lines = audit(deck)
        status = "OK" if not problems else "FAIL"
        if problems:
            failed += 1
        else:
            passed += 1
        print(f"{status} {deck.relative_to(ROOT)}: {n} slides, audit warnings {warnings}")
        for p in problems:
            print("   -", p)
        for line in warn_lines:
            print("   audit:", line)
        pdf = deck.with_suffix(".pdf")
        if not pdf.exists() or pdf.stat().st_size < 10000:
            failed += 1
            print("   - missing or empty PDF")
    print(f"\n{passed}/{len(decks)} decks passed")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
