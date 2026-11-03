"""Build course_home/presentation_template.pptx: five slides she fills in S9.

Same theme as the session decks. Every slide carries a short hint in muted text.
"""
from pathlib import Path

import deckkit as k

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "course_home" / "presentation_template.pptx"


def hint(d, s, text, y=6.08):
    d.text(s, k.M, y, k.CW, 0.34, text, size=d.s["label"], color=d.t["muted"], name="hint")


def placeholder(d, s, text):
    d.text(s, k.M, 2.05, k.CW, 1.7, text, size=26, bold=True, color=d.t["accent"], name="placeholder")


def build():
    d = k.new_deck()

    s = d.cover("Your project title",
                course=["Python for Supply Chain", "Your name  ·  December 2026"],
                group=None, members=())
    hint(d, s, "Hint: replace the title, your name and the month.")
    d.notes(s, "Slide ini untuk judul proyekmu. Ganti judul, nama, dan bulan. Jangan tambah kalimat lain.",
            "Bryan", 10)

    s = d.new_slide()
    d.title(s, "Your question")
    placeholder(d, s, "Write the question your project answers.")
    hint(d, s, "Hint: one sentence. A manager should understand it.")
    d.footer(s)
    d.notes(s, "Tulis pertanyaan proyekmu dalam satu kalimat. Contoh: apakah pendapatan kelas A stabil tiap bulan?",
            "Bryan", 15)

    s = d.new_slide()
    d.title(s, "Your finding")
    placeholder(d, s, "Say the answer first. Then show one chart and one number.")
    d.rect(s, k.M, 3.55, 7.4, 2.3, d.t["card2"], name="chart_area")
    d.text(s, k.M + 2.3, 4.45, 3.0, 0.4, "Your chart here", size=d.s["h"], color=d.t["muted"])
    d.footer(s)
    d.notes(s, "Mulai dengan jawabannya, lalu tunjukkan satu grafik dan satu angka. Grafiknya nanti kamu tempel di sini.",
            "Bryan", 20)

    s = d.new_slide()
    d.title(s, "Your recommendation")
    placeholder(d, s, "What should the manager do with this finding?")
    hint(d, s, "Hint: one action, one sentence. No new numbers.")
    d.footer(s)
    d.notes(s, "Rekomendasi itu satu tindakan yang bisa dilakukan manajer. Satu kalimat saja, tanpa angka baru.",
            "Bryan", 15)

    s = d.thanks("Thank you", subtitle="Questions?",
                 course="Python for Supply Chain")
    hint(d, s, "Hint: pause here and invite questions.", y=6.5)
    d.notes(s, "Slide terakhir. Berhenti sebentar dan buka sesi tanya jawab.", "Bryan", 10)

    k.save(d, OUT)


if __name__ == "__main__":
    build()
