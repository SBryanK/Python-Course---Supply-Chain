"""Build course_outline.docx/.pdf, course_home.docx, ANSWER_KEY.md, teacher_guide.md, data/README.md.

Run:  python tools/4_handouts_and_docs/build_course_docs.py
"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from docx import Document
from docx.shared import Cm, Pt

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
from build_materials import FONT, para, heading, table, run_font  # noqa: E402
from content_a import ALL_A  # noqa: E402
from content_b import ALL_B  # noqa: E402

ALL = ALL_A + ALL_B
CITE = ("Chen, D. (2012). Online Retail II [Dataset]. UCI Machine Learning Repository. "
        "https://doi.org/10.24432/C5CG6D. Licence: CC BY 4.0.")


def new_doc(margin=2.0):
    doc = Document()
    s = doc.sections[0]
    s.page_width, s.page_height = Cm(21.0), Cm(29.7)
    s.left_margin = s.right_margin = Cm(margin)
    s.top_margin = s.bottom_margin = Cm(1.8)
    doc.styles["Normal"].font.name = FONT
    doc.styles["Normal"].font.size = Pt(10)
    return doc


def to_pdf(doc, out_docx, out_pdf=None):
    doc.save(out_docx)
    if out_pdf:
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", tmp, str(out_docx)],
                           check=True, capture_output=True, env={"PATH": "/opt/homebrew/bin:/usr/bin:/bin", "HOME": tmp})
            shutil.copy(Path(tmp) / (Path(out_docx).stem + ".pdf"), out_pdf)


SCHEDULE = [
    ("1", "Mon 16 Nov", "Hello, Python. Print, variables, types, round, f-strings, reading errors.", "Notebook, handout, slides", ""),
    ("2", "Wed 18 Nov", "Shelves, cards and choices. Lists, dictionaries, comparisons, if / elif / else.", "Notebook, handout, slides", ""),
    ("3", "Mon 23 Nov", "Let the loop do the walking. For loops, functions, reading a traceback.", "Notebook, handout, slides", "Mount Google Drive once"),
    ("4", "Thu 26 Nov", "Cleaning day. Load a real CSV, check it, clean it, add columns. (May use 5 spare minutes.)", "Notebook, handout, slides, dataset credit", ""),
    ("5", "Mon 30 Nov", "Who are the star products? Groupby, running total, ABC analysis.", "Notebook, handout, slides", "Cold test (in class)"),
    ("6", "Thu 3 Dec", "Make the numbers talk. Merge and charts with matplotlib and seaborn.", "Notebook, handout, slides, case hunt template", "Case hunt handed out"),
    ("7", "Mon 7 Dec", "New tools, your own question. A taste of SQL and Power BI, then your project plan.", "Notebook, handout, slides, sql-practice.com, templates", "Project plan"),
    ("8", "Thu 10 Dec", "Detective work. Case hunt talk, then project work.", "Notebook, handout, slides", "Case hunt due"),
    ("9", "Mon 14 Dec", "Polish and publish. Final charts, three sentences, GitHub, slides.", "Notebook, handout, slides, templates", "Project and GitHub; reflection handed out"),
    ("10", "Thu 17 Dec", "Showtime. Your 5-minute presentation, questions, feedback, look back.", "Slides, scoring sheet", "Reflection (before the session); presentation"),
]


def outline():
    doc = new_doc()
    para(doc, "Python for Supply Chain", size=18, bold=True, after=2)
    para(doc, "Course outline", size=11, italic=True, after=6)
    table(doc, [["Course title", "Python for Supply Chain"],
                ["Class dates", "From 16/11/2026 to 17/12/2026"],
                ["Format", "Online, 10 sessions, 15:00 SGT (14:00 WIB), 90-minute slot"]],
          [4.0, 13.0], header=False, size=9.5)
    heading(doc, "1. Overview")
    para(doc, "Excel is great, until a file is too big, the steps repeat every week, or you need to show exactly what you did. "
              "Python helps with all three. In this course you start from zero and work with real sales data from a UK online "
              "gift shop. You clean the data, find which products matter, show it in clear charts, and present one finding in 5 minutes.",
         size=10, after=4)
    heading(doc, "2. Course objectives")
    for i, o in enumerate(["Read and fix common Python errors.", "Load, check and clean a real CSV file with pandas.",
                           "Summarise data with groupby and sort products with ABC analysis.",
                           "Make clear charts with matplotlib and seaborn.",
                           "Present a finding in 5 minutes, answer first."], 1):
        para(doc, f"{i}. {o}", size=10, after=1)
    heading(doc, "3. Assessment")
    table(doc, [["Component", "Weight"], ["Class participation and daily recall", "20%"], ["Cold test", "15%"],
                ["Project", "30%"], ["Final presentation", "20%"], ["Self-reflection", "15%"], ["Total", "100%"]],
          [12.0, 5.0], size=9.5)
    para(doc, "This course is not graded. The weights show what matters most.", size=9.5, italic=True, before=3, after=4)
    heading(doc, "4. Schedule and outline")
    rows = [["Lesson", "Date", "Session", "Resources", "Deadlines"]] + [list(r) for r in SCHEDULE]
    table(doc, rows, [1.6, 2.2, 6.2, 3.9, 3.1], size=8.5)
    heading(doc, "5. General guide and resources")
    para(doc, "Dataset: " + CITE, size=9.5, after=3)
    para(doc, "Course home: one page with the schedule and your folders in Google Drive. Open it first.", size=9.5, after=3)
    para(doc, "Notebooks: open each notebook from Google Drive in Google Colab. Run the cells from the top, in order.", size=9.5, after=3)
    para(doc, "Daily recall: three short questions a day between sessions. Answer from memory first, then check.", size=9.5, after=3)
    para(doc, "Help: write down what is unclear at the end of each session and bring it to the next one.", size=9.5, after=3)
    heading(doc, "6. Academic honesty")
    para(doc, "Your work must show your own understanding. Credit every source and the dataset.", size=9.5)
    return doc


def course_home():
    doc = new_doc(1.8)
    para(doc, "Python for Supply Chain: course home", size=16, bold=True, after=2)
    para(doc, "Open this page first. Everything you need is in the Google Drive folder Python for Supply Chain.", size=10, after=4)
    heading(doc, "Schedule (15:00 SGT, 14:00 WIB)")
    rows = [["#", "Date", "Topic", "Folder"]]
    wk = {1: "week_1", 2: "week_1", 3: "week_2", 4: "week_2", 5: "week_3", 6: "week_3", 7: "week_4", 8: "week_4", 9: "week_4", 10: "week_4"}
    short = {"1": "Hello, Python", "2": "Shelves, cards and choices", "3": "Let the loop do the walking", "4": "Cleaning day",
             "5": "Who are the star products?", "6": "Make the numbers talk", "7": "New tools, your own question",
             "8": "Detective work", "9": "Polish and publish", "10": "Showtime"}
    for n, d, *_ in SCHEDULE:
        rows.append([n, d, short[n], wk[int(n)]])
    table(doc, rows, [1.0, 2.8, 8.0, 5.0], size=9)
    heading(doc, "How a session works")
    para(doc, "Each session is 35 minutes, a 5-minute break, then 35 minutes. You type the code yourself. Open the notebook from the week folder.", size=9.5)
    heading(doc, "Daily recall")
    para(doc, "Between sessions, answer three short questions a day from the recall file. Answer from memory, then check the answers at the end.", size=9.5)
    heading(doc, "Case hunt")
    para(doc, "Handed out in Session 6, due in Session 8. Find one real supply chain case and answer five points on one page. Use case_hunt_template.", size=9.5)
    heading(doc, "Your project")
    para(doc, "Plan it in Session 7, work on it in Session 8, publish it on GitHub in Session 9, present it in Session 10. Files: project_plan, github_guide, presentation_guide, presentation_template.", size=9.5)
    heading(doc, "Your own files")
    para(doc, "From Session 4 you save your files in the work folder: sales_clean.csv, cancellations.csv and product_value.csv.", size=9.5)
    heading(doc, "Data credit")
    para(doc, CITE, size=9)
    return doc


def md_files():
    # Answer key
    L = ["# Answer key (teacher only)", "", "Every number comes from running the notebooks on `data/online_retail_ii_lesson.csv`. All money is in pounds.", "",
         "## Key numbers", "",
         "| What | Value |", "|---|---|",
         "| Raw rows / clean rows | 105,335 / 101,458 |",
         "| Cleaning log | 105,335 -> 104,360 -> 102,471 -> 102,257 -> 101,933 -> 101,459 -> 101,458 |",
         "| Clean shape | (101458, 10) |", "| Clean revenue | 1,876,534.04 |",
         "| Products / class A / B / C | 3,066 / 671 / 794 / 1,601 |",
         "| Class A in words | 21.9% of products bring 80.0% of revenue (79.98%) |",
         "| Top product | 22423 REGENCY CAKESTAND 3 TIER, 51,504.85 |",
         "| UK revenue by month (cold test) | Dec 705,166.72, Jan 468,651.61, Feb 417,876.17 |",
         "| Top 5 outside the UK | Netherlands 58,182.55, EIRE 43,426.19, Germany 37,365.63, France 32,392.39, Australia 24,678.48 |",
         "| Germany rows (clean) | (1514, 10) |", "| Merge check | 3,066 -> 3,107 -> 3,066 (41 extra rows, 40 codes with two names) |",
         "| Best day | 2010-12-07, 81,454.99 |", "| Trading days | 68 |", "", "## Exercises by session", ""]
    for S in ALL:
        L.append(f"### Session {S['no']}: {S['title']}")
        for task, ans in S["exercises"]:
            L.append(f"- {task}: {ans}")
        L.append("")
    (ROOT / "teacher_only" / "ANSWER_KEY.md").write_text("\n".join(L))

    # Teacher guide
    G = """# Panduan guru (Bahasa Indonesia)

## Prinsip
- **Dia yang mengetik. Selalu.** Kamu tidak mengetik untuk dia.
- **Tunggu 10 detik** dalam diam sebelum memberi petunjuk. Diam itu bagian dari belajar.
- **Puji prosesnya, spesifik.** Contoh: "Kamu baca baris error terakhir dulu, bagus." Bukan "pintar".
- Mulai dari kehidupan sehari-hari, lalu Excel, lalu kode. Ucapkan batas setiap analogi.
- Slide maksimal 10 menit per sesi. Sisanya coding langsung di Colab.

## Tangga petunjuk
1. "Apa yang kamu harapkan dari baris ini?"
2. Tunjuk barisnya tanpa bicara.
3. Beri petunjuk konsep ("Ingat cara filter di Excel?").
4. Tunjukkan polanya, bukan jawabannya.
5. Kerjakan bersama, lalu dia mengerjakan yang serupa sendiri.

## Alur satu sesi (75 menit)
Blok 1: recall 5, warm-up kertas 5, 3 sampai 4 siklus (konsep lalu latihan) 25. Istirahat 5 (kamera dan layar mati). Blok 2: worksheet 22 (dia yang jalan, kamu hanya petunjuk), exit ticket 8 (tanpa bantuan), penutup 5 (PR, rencana recall, "satu hal yang masih belum jelas"). Slot 90 menit, sisanya cadangan. S4 direncanakan 80 menit. Selalu berhenti di 90.

## Tanda kelebihan beban
Dua exit ticket berturut-turut di bawah 50%: pelankan dan buang bagian bonus.

## Urutan pemotongan (kalau dia tertinggal setelah S4)
1. Pengenalan SQL dan Power BI di S7 jadi halaman belajar mandiri.
2. Seaborn di S6 jadi PR, kurva 80% juga.
3. Proyek dari 3 sesi menjadi 2 sesi.

## Cold test (S5)
Dua puluh menit, catatan boleh, kamu diam. Pertanyaan: pendapatan per bulan untuk negara teratas. Nilai setelah kelas, 0 sampai 4: jalan, angka benar (selisih 0,01), nama jelas, satu kalimat arti. Jawaban ada di ANSWER_KEY.

## Kalau dia absen
Kirim notebook dan penjelasan solusi di hari yang sama. Recall dan warm-up sesi berikutnya (10 menit) jadi pengejaran. Kalau S4 terlewat, bangun tabel bersih bersama di layar.

## Sebelum S1
Cek 10 menit sebelum 16 Nov: dia membuka link Colab, menjalankan `print("hello")`, kirim screenshot, membuka folder Drive, dan tes share screen.
"""
    (ROOT / "teacher_only" / "teacher_guide.md").write_text(G)


    # Data README
    D = f"""# Lesson data

`online_retail_ii_lesson.csv` is the teaching file. It is not cleaned: cleaning is the learner's work in Session 4.

**Source.** {CITE} The file is an adaptation of the dataset and stays under CC BY 4.0.

**What it is.** Transactions from a UK online gift shop. Prices are in pounds.

**Slice rule.** Every row of the `Year 2010-2011` sheet with `InvoiceDate` from 2010-12-01 00:00 up to but not including 2011-03-01 00:00. Built by `tools/1_data/build_slice.py`.

| Property | Value |
|---|---|
| Rows / columns | 105,335 / 8 |
| Dates | 2010-12-01 08:26 to 2011-02-28 17:04 |
| Size | about 9.3 MB |

| Column | Meaning |
|---|---|
| `Invoice` | Invoice number. Starts with C for a cancellation |
| `StockCode` | Product code |
| `Description` | Product name |
| `Quantity` | Units on the line. Negative for cancellations |
| `InvoiceDate` | Date and time |
| `Price` | Unit price in pounds |
| `Customer ID` | Customer number. Empty for many rows |
| `Country` | Country of the customer |
"""
    (ROOT / "data" / "README.md").write_text(D)


if __name__ == "__main__":
    ch = ROOT / "course_home"
    to_pdf(outline(), ch / "course_outline.docx", ch / "course_outline.pdf")
    to_pdf(course_home(), ch / "course_home.docx")
    md_files()
    print(subprocess.run(["pdfinfo", str(ch / "course_outline.pdf")], capture_output=True, text=True,
                         env={"PATH": "/opt/homebrew/bin:/usr/bin:/bin"}).stdout.split("Pages:")[1].split("\n")[0].strip(), "page(s) in outline")
