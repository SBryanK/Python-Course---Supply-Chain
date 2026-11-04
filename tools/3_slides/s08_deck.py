"""Build the S8 deck: Detective work.

Theory slides that the teacher talks over: a title, one visual anchor, and at most one short line.
Most of this session is project work; the slides frame it and the speaker notes carry the explanation.
"""
from pathlib import Path

import deckkit as k
from deckkit import (M, CW, NAVY, ORANGE, ORANGE_TEXT, SAND, SKY, PEACH, CREAM, MUTED, CODE_INK, WHITE, cols,
                     centred, muted)

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "sessions" / "s08_detective_work" / "deck.pptx"


def cover(d):
    k.cover_for(d, "your question, your analysis, checked numbers",
                "Halo, selamat datang di sesi delapan. Tujuh titik sudah lewat. Hari ini hampir semuanya kerja "
                "proyek. Pertanyaannya adalah pertanyaanmu sendiri. Saya hanya memberi petunjuk, dan kamu yang "
                "mengetik semuanya. Siap?")


def goals(d):
    s, y = k.slide(d, "Today",
                   "Ini tiga bagian hari ini. Satu, case hunt dua menit. Dua, kerja proyek, dengan latihan detektif "
                   "singkat di awal notebook. Tiga, lima menit terakhir: apa yang sudah kamu temukan, dalam tiga "
                   "kalimat.", seconds=30)
    items = [("Case hunt", "2 minutes"), ("Project work", "hints only"), ("What I found", "3 sentences")]
    xs, w = cols(3)
    for i, (head, sub) in enumerate(items):
        d.rect(s, xs[i], 2.0, w, 2.6, SAND, name=f"g{i}")
        k.stop(d, s, xs[i] + w / 2 - 0.35, 2.3, 0.7, str(i + 1), ORANGE if i == 0 else NAVY, WHITE, size=22)
        k.label(d, s, xs[i], 3.2, w, 0.5, head, size=24, bold=True, name=f"gh{i}")
        k.label(d, s, xs[i] + 0.1, 3.75, w - 0.2, 0.4, sub, size=16, color=MUTED, name=f"gs{i}")


def case_hunt(d):
    s, y = k.slide(d, "Case hunt: two minutes",
                   "Presentasikan kasusmu dalam dua menit: masalahnya, data apa yang akan menunjukkannya, dan satu "
                   "kaitan dengan data kita. Tidak ada jawaban benar atau salah. Ini latihan melihat masalah nyata lewat "
                   "data, persis yang dilakukan analis setiap hari.", seconds=40)
    items = [("The case", "what is the problem?"), ("The data", "what would show it?"),
             ("The link", "how does it connect to our data?")]
    x0 = centred(3.4 * 3 + 0.9 * 2)
    for i, (head, sub) in enumerate(items):
        x = x0 + i * 4.3
        k.tile(d, s, x, 2.0, 3.4, 2.0, head, sub, head_size=24, name=f"c{i}", fill=NAVY if i == 2 else SAND,
               head_color=WHITE if i == 2 else NAVY, sub_color="C9D3DE" if i == 2 else MUTED)
        if i < 2:
            k.arrow(d, s, x + 3.5, 2.85, 0.7, 0.32, fill=ORANGE)
    muted(d, s, 4.6, "No right or wrong answer.")


def loop(d):
    s, y = k.slide(d, "The analyst's loop",
                   "Setiap analisis berjalan dalam putaran yang sama. Mulai dari pertanyaan satu kalimat. Tentukan kolom "
                   "yang dibutuhkan. Jalankan satu langkah, lalu cek hasilnya sebelum lanjut. Baru buat grafik. Kalau "
                   "hasil cek aneh, kembali satu langkah. Di langkah mana kamu sekarang?", seconds=60)
    steps = ["Question", "Columns", "One step", "Check", "Chart"]
    n = len(steps)
    import math
    cx, cy, r = 6.665, 3.6, 1.75
    for i, t in enumerate(steps):
        a = -math.pi / 2 + 2 * math.pi * i / n
        x, y2 = cx + r * 1.6 * math.cos(a), cy + r * math.sin(a)
        hot = t == "Check"
        k.chip(d, s, x - 1.1, y2 - 0.35, 2.2, 0.7, t, ORANGE if hot else NAVY, WHITE, size=19, bold=True,
               name=f"s{i}")
    k.label(d, s, cx - 1.5, cy - 0.3, 3.0, 0.6, "repeat", size=20, bold=True, color=MUTED, name="mid")


def shape_check(d):
    s, y = k.slide(d, "Print the shape after every filter",
                   "Kebiasaan detektif nomor satu: setelah setiap filter, tampilkan shape atau jumlah baris. Kalau "
                   "angkanya tiba-tiba nol, atau tidak berubah, ada yang salah. Lebih baik ketahuan sekarang daripada "
                   "saat presentasi. Berapa baris yang kamu harapkan setelah filter Netherlands?", seconds=55)
    k.code_card(d, s, centred(11.4), 1.85, 11.4,
                ['netherlands_sales = sales_clean[sales_clean["country"] == "Netherlands"]',
                 "print(netherlands_sales.shape)"], size=15)
    items = [("0 rows", "the filter is wrong"), ("No change", "the filter did nothing"),
             ("A sensible number", "keep going")]
    xs, w = cols(3, gap=0.3, w=10.0, x=centred(10.0))
    for i, (head, sub) in enumerate(items):
        k.tile(d, s, xs[i], 3.5, w, 1.5, head, sub, head_size=22, name=f"t{i}",
               fill=WHITE if i == 2 else SAND, line=ORANGE if i == 2 else None)


def second_way(d):
    s, y = k.slide(d, "Check one number a second way",
                   "Sebelum membuat grafik, periksa satu angka dengan cara kedua. Misalnya revenue Belanda: sekali dengan "
                   "groupby, sekali dengan filter lalu sum, atau dengan SQL. Kalau dua cara memberi angka yang sama, "
                   "angkamu bisa dipercaya. Tuliskan caranya di notebook.", seconds=55)
    x0 = centred(3.6 * 3 + 0.4 * 2)
    ways = [("groupby", '...groupby("country")'), ("filter + sum", 'df[mask]["revenue"].sum()'),
            ("SQL", "WHERE country = ...")]
    for i, (head, code) in enumerate(ways):
        x = x0 + i * 4.0
        d.rect(s, x, 1.9, 3.6, 1.7, SAND, name=f"w{i}")
        k.label(d, s, x, 2.05, 3.6, 0.5, head, size=22, bold=True)
        k.label(d, s, x + 0.15, 2.7, 3.3, 0.5, code, size=14, mono=True, color=MUTED)
    k.chip(d, s, centred(4.4), 4.1, 4.4, 0.9, "58,182.55 = 58,182.55", ORANGE, WHITE, size=22, bold=True,
           name="same")
    muted(d, s, 5.35, "Same number two ways: you can trust it.")


def traps(d):
    s, y = k.slide(d, "Four traps to watch",
                   "Empat jebakan yang sering muncul di proyek. Hasil filter tidak disimpan ke nama. Merge yang membuat "
                   "tabel tumbuh. Tanggal yang masih teks setelah membaca CSV. Dan lupa bahwa Inggris 85 persen revenue. "
                   "Semuanya sudah kita temui; sekarang kamu tahu cara mengeceknya.", seconds=60)
    items = [("Filter not saved", "assign it to a name"), ("Merge grows", "count rows before and after"),
             ("Dates as text", "pd.to_datetime again"), ("UK is 85%", "say so in the title")]
    xs, w = cols(2, gap=0.3, w=10.0, x=centred(10.0))
    for i, (head, sub) in enumerate(items):
        x, ty = xs[i % 2], 1.8 + (i // 2) * 1.85
        d.rect(s, x, ty, w, 1.6, SAND, name=f"t{i}")
        k.stop(d, s, x + 0.3, ty + 0.45, 0.7, str(i + 1), ORANGE, WHITE, size=20)
        k.label(d, s, x + 1.25, ty + 0.3, w - 1.4, 0.5, head, size=22, bold=True, align="left", name=f"h{i}")
        k.label(d, s, x + 1.25, ty + 0.85, w - 1.4, 0.45, sub, size=17, color=MUTED, align="left", name=f"s{i}")


def hints(d):
    s, y = k.slide(d, "How I will help today",
                   "Hari ini saya membantu dengan tangga petunjuk, selalu dengan sepuluh detik diam dulu. Pertama saya "
                   "bertanya apa yang kamu harapkan dari baris itu. Lalu saya menunjuk barisnya. Lalu petunjuk konsep. "
                   "Lalu pola, bukan jawaban. Terakhir kita kerjakan bersama, lalu kamu coba yang mirip sendiri.",
                   seconds=55)
    steps = [("What do you expect?", 1), ("Point at the line", 2), ("A concept hint", 3), ("The pattern", 4),
             ("Together, then alone", 5)]
    n = len(steps)
    w, gap = 2.2, 0.15
    x0 = centred(n * w + (n - 1) * gap)
    for i, (t, _) in enumerate(steps):
        h = 1.2 + 0.45 * i
        x = x0 + i * (w + gap)
        d.rect(s, x, 5.2 - h, w, h, ORANGE if i == 0 else NAVY, name=f"h{i}")
        k.label(d, s, x + 0.1, 5.2 - h + 0.15, w - 0.2, 0.9, t, size=16, bold=True, color=WHITE, anchor="top",
                name=f"t{i}")
    muted(d, s, 5.55, "Ten seconds of silence before each step.")


def status(d):
    s, y = k.slide(d, "What I found so far",
                   "Lima menit terakhir: tiga kalimat tentang apa yang sudah kamu temukan. Jawaban, bukti, dan langkah "
                   "berikutnya. Kalimat pertama adalah jawabannya, bukan cerita prosesnya. Ini latihan untuk presentasi "
                   "di sesi sepuluh.", seconds=40)
    items = [("Answer", "one sentence"), ("Evidence", "one number"), ("Next", "one step")]
    xs, w = cols(3)
    for i, (head, sub) in enumerate(items):
        k.tile(d, s, xs[i], 2.0, w, 2.2, head, sub, head_size=28, name=f"s{i}", fill=NAVY if i == 0 else SAND,
               head_color=WHITE if i == 0 else NAVY, sub_color="C9D3DE" if i == 0 else MUTED)
        k.stop(d, s, xs[i] + w / 2 - 0.3, 1.7, 0.6, str(i + 1), ORANGE, WHITE, size=18)
    muted(d, s, 4.8, "Answer first, not the story of the work.")


def now_colab(d):
    s, y = k.slide(d, "Now in Colab",
                   "Sekarang buka notebook s8_detective_work. Mulai dengan latihan detektif singkat: satu tebakan, satu "
                   "isian, satu bug, dua kode. Lalu proyekmu sendiri. Saya hanya memberi petunjuk. PR: buat akun GitHub "
                   "dan repository publik yang kosong.", seconds=30)
    k.ladder(d, s, M, 1.85, 8.0, 3.6, [("Predict", 1), ("Fill in", 1), ("Fix it", 1), ("Write it", 2),
                                       ("Project", 1)])
    d.text(s, 9.3, 1.9, 3.43, 4.2,
           [{"text": "Notebook", "bold": True, "color": ORANGE_TEXT, "size": 16},
            {"text": "s8_detective_work", "after": 14},
            {"text": "Homework", "bold": True, "color": ORANGE_TEXT, "size": 16},
            {"text": "GitHub account, empty repository", "after": 14},
            {"text": "Recall", "bold": True, "color": ORANGE_TEXT, "size": 16},
            {"text": "Fri 11 to Sun 13"}],
           size=20, color=NAVY, name="side")


def thanks(d):
    k.thanks_next(d, "Terima kasih untuk hari ini. Kamu sudah bekerja seperti detektif dan memeriksa angkamu sendiri. "
                     "Titik delapan selesai. Berikutnya titik sembilan: merapikan grafik, menulis temuan dalam tiga "
                     "kalimat, dan mengunggah proyekmu ke GitHub.")


def build():
    d = k.lecture_deck(8)
    for make in (cover, goals, case_hunt, loop, shape_check, second_way, traps, hints, status, now_colab, thanks):
        make(d)
    k.save(d, OUT)


if __name__ == "__main__":
    build()
