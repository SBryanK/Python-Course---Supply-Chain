"""Build the S10 deck: Showtime."""
from pathlib import Path

import deckkit as k

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "sessions" / "s10_showtime" / "deck.pptx"


def build():
    d = k.new_deck()

    k.cover(d, "Showtime", 10, "Thu 17 Dec 2026",
            "Hari ini sesi terakhir. Kamu presentasi, kita tanya jawab, lalu kita lihat perjalanan belajarmu.",
            seconds=15)

    k.table_slide(d, "Today's agenda",
                  [["Time", "What"],
                   ["5 min", "Your presentation"],
                   ["15 min", "Interview-style questions"],
                  ["10 min", "Feedback"],
                   ["After the break", "Reflection and what next"]],
                  "Urutan hari ini: presentasimu lima menit, tanya jawab seperti wawancara, lalu masukan. Setelah "
                  "istirahat, kita baca refleksimu dan bicara langkah berikutnya.",
                  seconds=30,
                  col_widths=[3.2, 5.2])

    k.cards(d, "Questions to expect",
            [("Walk me through", None, "Your project, in 2 minutes."),
             ("Why", None, "Did you remove those rows?"),
             ("How", None, "Did you check your numbers?")],
            notes="Pertanyaan ini seperti wawancara kerja. Jawab singkat, mulai dari jawabannya. Kalau tidak tahu, "
                  "katakan apa yang akan kamu cek. Kamu boleh menjawab dalam Bahasa Indonesia kalau gugup.",
            seconds=40, cols=3)

    k.cards(d, "Keep, stop, start",
            [("Keep", None, "What worked well."),
             ("Stop", None, "What did not help."),
             ("Start", None, "What you want more of.")],
            notes="Retro untuk kursus ini. Apa yang harus dipertahankan, dihentikan, dan dimulai. Jawaban jujurmu "
                  "akan membantu kursus berikutnya.",
            seconds=40, cols=3)

    k.cards(d, "What next",
            [("Practise", None, "Redo one project step each week."),
             ("Explore", None, "Power BI, more SQL, VS Code."),
             ("Share", None, "Keep your GitHub project up to date.")],
            notes="Langkah berikutnya, kalau kamu mau: latihan kecil tiap minggu, lalu Power BI yang lebih dalam, SQL, "
                  "dan VS Code. Jaga proyek GitHub-mu tetap rapi karena itu bisa kamu tunjukkan saat melamar kerja.",
            seconds=35, cols=3)

    k.thanks(d, "Thank you", "You did the work. Keep going.",
             "Terima kasih. Kamu sudah bekerja keras. Teruslah berlatih.",
             seconds=15)

    k.save(d, OUT)


if __name__ == "__main__":
    build()
