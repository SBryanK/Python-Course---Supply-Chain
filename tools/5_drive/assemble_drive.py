"""Assemble the learner-only Google Drive folder at drive_package/Python for Supply Chain/.

Copies only what Michella may see (see PROGRESS.md). Never copies teacher_only/, tools/ or raw data.
Run:  python tools/5_drive/assemble_drive.py
Then drag the folder into Google Drive, or upload the week folders by the dates in PROGRESS.md.
"""
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "drive_package" / "Python for Supply Chain"
WEEK = {1: "week_1", 2: "week_1", 3: "week_2", 4: "week_2", 5: "week_3", 6: "week_3",
        7: "week_4", 8: "week_4", 9: "week_4", 10: "week_4"}

if OUT.parent.exists():
    shutil.rmtree(OUT.parent)
(OUT / "work").mkdir(parents=True)
(OUT / "data").mkdir()
shutil.copy(ROOT / "data" / "online_retail_ii_lesson.csv", OUT / "data")
shutil.copy(ROOT / "data" / "README.md", OUT / "data")

home = OUT / "00_course_home"
home.mkdir()
for name in ["course_outline.pdf", "course_home.docx", "glossary.md", "case_hunt_template.md", "reflection_template.md",
             "project_plan.md", "presentation_guide.md", "presentation_scoring.md", "intro_sql.md", "sql_playground.md",
             "intro_powerbi.md", "github_guide.md", "presentation_template.pptx"]:
    shutil.copy(ROOT / "course_home" / name, home)

# Notebook names exactly as the slides say them.
NB = {1: "s1_hello_python", 2: "s2_shelves_cards", 3: "s3_let_loop_walk", 4: "s4_cleaning_day", 5: "s5_star_products",
      6: "s6_numbers_talk", 7: "s7_new_tools", 8: "s8_detective_work", 9: "s9_polish_publish", 10: "s10_showtime"}

for s in sorted((ROOT / "sessions").iterdir()):
    n = int(s.name[1:3])
    dst = OUT / WEEK[n] / s.name
    dst.mkdir(parents=True, exist_ok=True)
    shutil.copy(s / "student.ipynb", dst / f"{NB[n]}.ipynb")
    for f in ["deck.pdf", "handout.pdf", "recall.md"]:
        shutil.copy(s / f, dst)
print("Ready:", OUT)
