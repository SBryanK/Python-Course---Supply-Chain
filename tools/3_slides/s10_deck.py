"""Build the S10 deck: Showtime.

Theory slides that the teacher talks over: a title, one visual anchor, and at most one short line.
This session is her presentation and a look back; the slides only frame it.
"""
from pathlib import Path

import deckkit as k
from deckkit import (M, CW, NAVY, ORANGE, ORANGE_TEXT, SAND, SKY, PEACH, CREAM, MUTED, CODE_INK, WHITE, cols,
                     centred, muted)

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "sessions" / "s10_showtime" / "deck.pptx"


def cover(d):
    k.cover_for(d, "your talk, questions, feedback, what next",
                "Halo, selamat datang di sesi terakhir. Sembilan titik sudah lewat, dan hari ini titik sepuluh. "
                "Pertanyaannya: bisakah kamu menjelaskan proyekmu seperti seorang analis? Tarik napas, kamu sudah "
                "siap.")


def agenda(d):
    s, y = k.slide(d, "Today",
                   "Ini agenda hari ini. Blok pertama: presentasimu lima menit, tanya jawab seperti wawancara, lalu "
                   "umpan balik. Blok kedua: membaca refleksimu bersama, keep stop start untuk kursus ini, dan ide untuk "
                   "Januari.", seconds=35)
    items = [("Your talk", "5 minutes"), ("Q&A", "like an interview"), ("Feedback", "2 strengths, 1 to improve"),
             ("Look back", "reflection, keep stop start"), ("What next", "January ideas")]
    xs, w = cols(5, gap=0.2)
    for i, (head, sub) in enumerate(items):
        d.rect(s, xs[i], 2.0, w, 2.6, SAND, name=f"g{i}")
        k.stop(d, s, xs[i] + w / 2 - 0.35, 2.3, 0.7, str(i + 1), ORANGE if i == 0 else NAVY, WHITE, size=22)
        k.label(d, s, xs[i], 3.2, w, 0.5, head, size=21, bold=True, name=f"gh{i}")
        k.label(d, s, xs[i] + 0.15, 3.75, w - 0.3, 0.7, sub, size=15, color=MUTED, anchor="top", name=f"gs{i}")


def talk(d):
    s, y = k.slide(d, "Five minutes, answer first",
                   "Lima menit: satu menit pertanyaan dan konteks, dua menit temuan dan bukti, satu menit rekomendasi, "
                   "satu menit cadangan. Jawaban di tiga puluh detik pertama. Presentasi dalam bahasa Inggris; "
                   "pertanyaan boleh dijawab dalam bahasa Indonesia. Yang dinilai struktur dan tempo, bukan aksen.",
                   seconds=50)
    parts = [("Question", 1, SAND, NAVY), ("Finding + evidence", 2, ORANGE, WHITE), ("Recommendation", 1, NAVY, WHITE),
             ("Spare", 1, CREAM, MUTED)]
    unit = 2.2
    x = centred(5 * unit)
    for i, (t, mins, f, c) in enumerate(parts):
        w = mins * unit
        shp = d.rect(s, x, 2.0, w - 0.08, 1.4, f, line=SKY if f == CREAM else None, rounded=False, name=f"p{i}")
        k.label(d, s, x, 2.0, w - 0.08, 1.4, t, size=19, bold=True, color=c, name=f"t{i}")
        k.label(d, s, x, 3.5, w - 0.08, 0.4, f"{mins} min", size=17, color=MUTED, name=f"m{i}")
        x += w
    k.box(d, s, centred(7.6), 4.5, 7.6, "Structure and pace, not accent.", size=19)


def qa(d):
    s, y = k.slide(d, "Questions like an interview",
                   "Setelah presentasi, saya bertanya seperti pewawancara kerja. Empat pertanyaan ini. Tidak ada jebakan; "
                   "semuanya tentang pekerjaanmu sendiri. Jawab singkat, dengan satu angka kalau bisa. Kalau tidak tahu, "
                   "bilang bagaimana kamu akan mencari tahu.", seconds=50)
    items = ["Walk me through your project in 2 minutes.", "Why did you remove those rows?",
             "What would you do with more time?", "How did you check your numbers?"]
    xs, w = cols(2, gap=0.3)
    for i, t in enumerate(items):
        x, ty = xs[i % 2], 1.8 + (i // 2) * 1.85
        d.rect(s, x, ty, w, 1.6, SAND, name=f"q{i}")
        k.label(d, s, x + 0.2, ty + 0.1, 0.9, 0.9, "?", size=44, bold=True, color=ORANGE_TEXT, name=f"m{i}")
        k.label(d, s, x + 1.1, ty, w - 1.3, 1.6, t, size=20, bold=True, align="left", name=f"t{i}")
    muted(d, s, 5.6, "Short answers. One number if you can.")


def feedback(d):
    s, y = k.slide(d, "Feedback: two and one",
                   "Umpan balik saya selalu dua kekuatan dan satu hal yang bisa diperbaiki. Penilaian memakai empat "
                   "kriteria dari presentation_scoring: kejelasan, bukti, rekomendasi, dan cara menyampaikan, masing-"
                   "masing satu sampai empat. Catat di notebook supaya tidak hilang.", seconds=45)
    xs, w = cols(3)
    for i, (head, sub) in enumerate([("Strength", "what worked"), ("Strength", "what worked"),
                                     ("To improve", "one thing")]):
        k.tile(d, s, xs[i], 1.9, w, 1.8, head, sub, head_size=26, name=f"f{i}",
               fill=WHITE if i == 2 else SAND, line=ORANGE if i == 2 else None)
    crit = ["Clarity", "Evidence", "Recommendation", "Delivery"]
    xs, w = cols(4, gap=0.2, w=10.0, x=centred(10.0))
    for x, c in zip(xs, crit):
        k.chip(d, s, x, 4.3, w, 0.65, f"{c}  1-4", NAVY, WHITE, size=17, name="c")


def keep_stop_start(d):
    s, y = k.slide(d, "Keep, stop, start",
                   "Sekarang giliranmu menilai kursus ini. Keep: apa yang berjalan baik dan harus dipertahankan. Stop: "
                   "apa yang tidak membantu. Start: apa yang ingin kamu tambah. Jawaban jujur membantu kursus berikutnya.",
                   seconds=45)
    items = [("Keep", "what worked"), ("Stop", "what did not help"), ("Start", "what you want more of")]
    xs, w = cols(3)
    for i, (head, sub) in enumerate(items):
        k.tile(d, s, xs[i], 2.0, w, 2.4, head, sub, head_size=36, name=f"k{i}", fill=[SAND, PEACH, NAVY][i],
               head_color=WHITE if i == 2 else NAVY, sub_color="C9D3DE" if i == 2 else MUTED)
    muted(d, s, 5.0, "Honest answers help the next course.")


def look_back(d):
    s, y = k.slide(d, "What you can do now",
                   "Lihat jalannya dari November. Dari print satu baris, sampai membersihkan seratus ribu baris, mencari "
                   "produk bintang, menggambar grafik, menulis SQL, dan menjelaskan temuan seperti analis. Mana yang "
                   "paling kamu banggakan?", seconds=50)
    items = [("1-3", "Python basics", "variables, lists, loops, functions"),
             ("4-5", "pandas", "clean 105,335 rows, groupby, ABC"),
             ("6", "Charts", "titles that say the finding"),
             ("7", "SQL, Power BI", "the same idea, new tools"),
             ("8-10", "A real project", "question, evidence, GitHub, a talk")]
    xs, w = cols(5, gap=0.2)
    for i, (n, head, sub) in enumerate(items):
        d.rect(s, xs[i], 1.9, w, 3.0, NAVY if i == 4 else SAND, name=f"l{i}")
        k.label(d, s, xs[i], 2.05, w, 0.6, n, size=26, bold=True, color=ORANGE if i == 4 else ORANGE_TEXT)
        k.label(d, s, xs[i] + 0.1, 2.8, w - 0.2, 0.5, head, size=19, bold=True, color=WHITE if i == 4 else NAVY)
        k.label(d, s, xs[i] + 0.15, 3.4, w - 0.3, 1.2, sub, size=15, color="C9D3DE" if i == 4 else MUTED,
                anchor="top")


def now_colab(d):
    s, y = k.slide(d, "Now in Colab",
                   "Sekarang buka notebook s10_showtime. Ada lima tebakan singkat, satu dari setiap bagian kursus, dan "
                   "satu kode kecil untuk ditulis. Lalu catat umpan balik dan jawabanmu untuk keep stop start. Tanpa "
                   "tekanan; ini untuk melihat seberapa jauh kamu sudah berjalan.", seconds=30)
    k.ladder(d, s, M, 1.85, 8.0, 3.6, [("Predict", 5), ("Write it", 1), ("Notes", 3)])
    d.text(s, 9.3, 1.9, 3.43, 4.2,
           [{"text": "Notebook", "bold": True, "color": ORANGE_TEXT, "size": 16},
            {"text": "s10_showtime", "after": 14},
            {"text": "Recall", "bold": True, "color": ORANGE_TEXT, "size": 16},
            {"text": "optional January sheet", "after": 14}],
           size=20, color=NAVY, name="side")


def next_ideas(d):
    s, y = k.slide(d, "What next: January ideas",
                   "Beberapa ide untuk Januari, semuanya pilihan. Power BI yang lebih dalam. SQL lebih banyak, misalnya "
                   "di sql-practice.com. VS Code untuk menulis Python di laptop. Dan git dari command line. Yang paling "
                   "penting: rencana tiga puluh harimu sendiri. Satu hal kecil setiap minggu sudah cukup.", seconds=45)
    items = [("Power BI", "deeper dashboards"), ("SQL", "sql-practice.com"), ("VS Code", "Python on your laptop"),
             ("git", "the command line")]
    xs, w = cols(4)
    for i, (head, sub) in enumerate(items):
        k.tile(d, s, xs[i], 2.0, w, 2.0, head, sub, head_size=24, name=f"n{i}")
    k.box(d, s, centred(7.6), 4.6, 7.6, "One small thing every week is enough.", size=19)


def thanks(d):
    k.thanks_slide(d, ["Ten sessions done", "Keep asking good questions", "Python for Supply Chain"],
                   "Terima kasih banyak untuk sepuluh sesi ini. Kamu mulai dari satu baris print, dan sekarang kamu bisa "
                   "membersihkan data asli, menemukan produk bintang, dan menjelaskan temuanmu seperti analis. Jalannya "
                   "sudah lengkap. Terus bertanya, dan terus berlatih.")


def build():
    d = k.lecture_deck(10)
    for make in (cover, agenda, talk, qa, feedback, look_back, now_colab, keep_stop_start, next_ideas, thanks):
        make(d)
    k.save(d, OUT)


if __name__ == "__main__":
    build()
