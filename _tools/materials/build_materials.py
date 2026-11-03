"""Build handout.pdf, recall.md, exit_ticket.md and teacher_card.md for every session.

Run:  _tools/venv/bin/python _tools/materials/build_materials.py
Needs soffice (LibreOffice) on PATH for the handout PDFs.
"""
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import pandas as pd
from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
from content_a import ALL_A  # noqa: E402
from content_b import ALL_B  # noqa: E402
from scoring import SCORING  # noqa: E402

FONT = "Arial"
MONO = "Courier New"
ALL = ALL_A + ALL_B


def set_cell_borders(cell):
    tcPr = cell._tc.get_or_add_tcPr()
    borders = OxmlElement("w:tcBorders")
    for edge in ("top", "left", "bottom", "right"):
        el = OxmlElement(f"w:{edge}")
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), "4")
        el.set(qn("w:color"), "000000")
        borders.append(el)
    tcPr.append(borders)


def run_font(run, size=9, bold=False, mono=False, italic=False):
    run.font.name = MONO if mono else FONT
    run._element.rPr.rFonts.set(qn("w:eastAsia"), MONO if mono else FONT)
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic


def para(doc, text="", size=9, bold=False, italic=False, mono=False, after=2, before=0):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(after)
    p.paragraph_format.space_before = Pt(before)
    p.paragraph_format.line_spacing = 1.0
    if text:
        run_font(p.add_run(text), size, bold, mono, italic)
    return p


def heading(doc, text):
    para(doc, text, size=10.5, bold=True, after=2, before=6)


def table(doc, rows, widths, header=True, size=8.5):
    t = doc.add_table(rows=len(rows), cols=len(rows[0]))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    tblPr = t._tbl.tblPr
    layout = OxmlElement("w:tblLayout")
    layout.set(qn("w:type"), "fixed")
    tblPr.append(layout)
    for j, w in enumerate(widths):
        t.columns[j].width = Cm(w)
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            c = t.cell(i, j)
            c.width = Cm(widths[j])
            set_cell_borders(c)
            p = c.paragraphs[0]
            p.paragraph_format.space_after = Pt(1)
            p.paragraph_format.space_before = Pt(1)
            run_font(p.add_run(str(val)), size, bold=(header and i == 0))
    return t


def first12():
    d = pd.read_csv(ROOT / "data" / "online_retail_ii_lesson.csv").head(12)
    rows = [["Row", "Invoice", "Description", "Qty", "Price"]]
    for i, r in d.iterrows():
        rows.append([i + 1, r["Invoice"], r["Description"], int(r["Quantity"]), f"{r['Price']:.2f}"])
    return rows


def make_handout(S, out_pdf):
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Cm(21.0), Cm(29.7)
    sec.left_margin = sec.right_margin = Cm(1.6)
    sec.top_margin = Cm(1.3)
    sec.bottom_margin = Cm(1.4)
    st = doc.styles["Normal"]
    st.font.name = FONT
    st.font.size = Pt(9)

    para(doc, f"Session {S['no']}: {S['title']}", size=15, bold=True, after=0)
    para(doc, f"Question: {S['question']}", size=9.5, italic=True, after=4)

    if S.get("concepts"):
        heading(doc, "Concepts")
        rows = [["Concept", "In daily life", "In Excel", "The limit"]] + [list(c) for c in S["concepts"]]
        table(doc, rows, [2.9, 4.2, 3.8, 6.9])
    if S.get("patterns"):
        heading(doc, "Code patterns")
        for pat in S["patterns"]:
            for line in pat.split("\n"):
                para(doc, line, size=8, mono=True, after=0)
            para(doc, "", size=3, after=2)
    if S.get("errors"):
        heading(doc, "Three common errors")
        table(doc, [["Error", "What to do"]] + [list(e) for e in S["errors"]], [4.3, 13.5])
    if S.get("exercises"):
        heading(doc, "Exercises and expected answers")
        table(doc, [["Exercise", "Expected"]] + [list(e) for e in S["exercises"]], [8.8, 9.0])
    extra = S.get("extra_table")
    if extra:
        heading(doc, S["extra_title"])
        rows = first12() if extra == "FIRST12" else extra
        widths = {5: [1.2, 2.0, 10.8, 1.6, 2.0], 2: [4.5, 13.3]}.get(len(rows[0]), [17.8 / len(rows[0])] * len(rows[0]))
        table(doc, rows, widths)
    if S.get("scoring"):
        heading(doc, "Presentation scoring (each criterion 1 to 4)")
        rows = [["Criterion", "1", "2", "3", "4"]] + [[k] + v for k, v in SCORING.items()]
        table(doc, rows, [2.4, 3.8, 3.8, 3.8, 4.0], size=7.5)
        heading(doc, "Questions to expect")
        for q in ["Walk me through your project in 2 minutes.", "Why did you remove those rows?",
                  "What would you do with more time?", "How did you check your numbers?"]:
            para(doc, "- " + q, size=9, after=1)
        heading(doc, "Your 5 minutes")
        para(doc, "1 minute question and context. 2 minutes finding and evidence. 1 minute recommendation. 1 minute spare. "
                  "Answer first. Say numbers simply.", size=9)

    footer = sec.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_font(footer.add_run(f"Python for Supply Chain  |  Session {S['no']}"), 7.5)

    with tempfile.TemporaryDirectory() as tmp:
        docx = Path(tmp) / "handout.docx"
        doc.save(docx)
        subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", tmp, str(docx)],
                       check=True, capture_output=True,
                       env={"PATH": "/opt/homebrew/bin:/usr/bin:/bin", "HOME": tmp})
        shutil.copy(Path(tmp) / "handout.pdf", out_pdf)
    out = subprocess.run(["pdfinfo", str(out_pdf)], capture_output=True, text=True,
                         env={"PATH": "/opt/homebrew/bin:/usr/bin:/bin"}).stdout
    return int(re.search(r"Pages:\s+(\d+)", out).group(1))


def make_recall(S, path):
    L = [f"# Session {S['no']}: daily recall", "",
         "Three short questions a day. Answer from memory first, then check the answers at the end.", ""]
    for d_i, (label, qs) in enumerate(S["recall"], 1):
        L += [f"## {label}", ""]
        for i, (q, _) in enumerate(qs, 1):
            L.append(f"{i}. {q}")
        L.append("")
    L += ["## Answers", ""]
    for label, qs in S["recall"]:
        L.append(f"**{label}**")
        for i, (_, a) in enumerate(qs, 1):
            L.append(f"{i}. {a}")
        L.append("")
    path.write_text("\n".join(L).rstrip() + "\n")


def make_exit(S, path):
    L = [f"# Session {S['no']}: exit ticket", "", "Two questions. No help. About 8 minutes.", ""]
    for i, (q, _) in enumerate(S["exit"], 1):
        L += [f"{i}. {q}", ""]
    L += ["---", "", "## Answers (teacher only)", ""]
    for i, (_, a) in enumerate(S["exit"], 1):
        L.append(f"{i}. {a}")
    path.write_text("\n".join(L).rstrip() + "\n")


def make_card(S, path):
    c = S["card"]
    L = [f"# Teacher card, Sesi {S['no']}: {S['title']} ({S['date']})", "",
         f"**Pertanyaan:** {S['question']}", "", "**Urutan ide**"]
    for i, x in enumerate(c["ide"], 1):
        L.append(f"{i}. {x}")
    L += ["", "**Analogi dan batasnya** (ucapkan batasnya keras-keras)"]
    for name, analogy, limit in c["analogi"]:
        L.append(f"- {name}: {analogy}. Batas: {limit}.")
    L += ["", "**Dua kesalahan yang mungkin muncul**"]
    for x in c["salah"]:
        L.append(f"- {x}")
    L += ["", f"**Tangga petunjuk untuk {c['tangga_untuk']}** (diam 10 detik sebelum tiap langkah)"]
    for i, x in enumerate(c["tangga"], 1):
        L.append(f"{i}. {x}")
    L += ["", f"**Waktu:** {c['waktu']}"]
    path.write_text("\n".join(L) + "\n")


if __name__ == "__main__":
    for S in ALL:
        sdir = ROOT / "sessions" / S["folder"]
        tdir = ROOT / "teacher_only" / "sessions" / S["folder"]
        sdir.mkdir(parents=True, exist_ok=True)
        tdir.mkdir(parents=True, exist_ok=True)
        pages = make_handout(S, sdir / "handout.pdf")
        make_recall(S, sdir / "recall.md")
        make_exit(S, tdir / "exit_ticket.md")
        make_card(S, tdir / "teacher_card.md")
        flag = "" if pages <= 2 else "  FAIL more than 2 pages"
        print(f"s{S['no']:02d}: handout {pages} page(s){flag}")
