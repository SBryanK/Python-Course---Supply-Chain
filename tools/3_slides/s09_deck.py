"""Build the S9 deck: Polish and publish.

Theory slides that the teacher talks over: a title, one visual anchor, and at most one short line.
Most of this session is project work; the slides frame it and the speaker notes carry the explanation.
"""
from pathlib import Path

import deckkit as k
from deckkit import (M, CW, NAVY, ORANGE, ORANGE_TEXT, SAND, SKY, PEACH, CREAM, MUTED, CODE_INK, WHITE, cols,
                     centred, muted)

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "sessions" / "s09_polish_publish" / "deck.pptx"


def cover(d):
    k.cover_for(d, "final charts, three sentences, GitHub, your slides",
                "Halo, selamat datang di sesi sembilan. Delapan titik sudah lewat, tinggal dua. Hari ini kita "
                "merapikan: grafik akhir, temuan dalam tiga kalimat, proyek di GitHub, dan tiga slide untuk "
                "presentasi. Siap?")


def goals(d):
    s, y = k.slide(d, "Today",
                   "Ini empat bagian hari ini. Satu, grafik akhir yang rapi. Dua, temuan dalam tiga kalimat. Tiga, "
                   "mengunggah notebook ke GitHub dengan README. Empat, mulai tiga slide presentasi.", seconds=30)
    items = [("Final chart", "checklist"), ("Three sentences", "answer first"), ("GitHub", "notebook + README"),
             ("Your slides", "3 content slides")]
    xs, w = cols(4)
    for i, (head, sub) in enumerate(items):
        d.rect(s, xs[i], 2.0, w, 2.6, SAND, name=f"g{i}")
        k.stop(d, s, xs[i] + w / 2 - 0.35, 2.3, 0.7, str(i + 1), ORANGE if i == 0 else NAVY, WHITE, size=22)
        k.label(d, s, xs[i], 3.2, w, 0.5, head, size=22, bold=True, name=f"gh{i}")
        k.label(d, s, xs[i] + 0.1, 3.75, w - 0.2, 0.4, sub, size=16, color=MUTED, name=f"gs{i}")


def checklist(d):
    s, y = k.slide(d, "Final chart checklist",
                   "Sebelum grafik masuk ke slide, cek lima hal. Judul menyatakan temuan. Kedua sumbu punya label dan "
                   "satuan. Satu pesan per grafik. Label panjang terbaca. Dan kamu bisa mengucapkan angka utamanya "
                   "dengan sederhana. Grafikmu sudah lolos berapa?", seconds=50)
    items = ["The title says the finding", "Both axes: label and unit", "One message per chart",
             "Long labels are readable", "The main number, said simply"]
    x0 = centred(9.0)
    for i, t in enumerate(items):
        ry = 1.8 + i * 0.82
        k.stop(d, s, x0, ry, 0.6, str(i + 1), ORANGE if i == 0 else NAVY, WHITE, size=18)
        k.chip(d, s, x0 + 0.85, ry, 8.15, 0.6, t, SAND, NAVY, size=19, name=f"t{i}")
    muted(d, s, 6.0, "Five checks before a chart goes on a slide.")


def before_after(d):
    s, y = k.slide(d, "Before and after",
                   "Ini perbedaan grafik draf dan grafik akhir. Kiri: judul kosong, sumbu tanpa label, angka panjang. "
                   "Kanan: judul menyatakan temuan, sumbu berlabel dengan pounds, dan satu angka yang mudah diucapkan. "
                   "Grafik yang sama, tapi manajer langsung paham.", seconds=50)
    xs, w = cols(2, gap=0.5, w=11.0, x=centred(11.0))
    left = ["title: (none)", "x axis: (none)", "1876534.04"]
    right = ["About 1 in 5 products bring 80% of revenue", "Revenue (pounds)", "about 1.9 million pounds"]
    k.label(d, s, xs[0], 1.75, w, 0.4, "draft", size=20, bold=True, color=MUTED)
    k.label(d, s, xs[1], 1.75, w, 0.4, "final", size=20, bold=True, color=ORANGE_TEXT)
    for i, (a, b) in enumerate(zip(left, right)):
        ry = 2.3 + i * 1.0
        k.chip(d, s, xs[0], ry, w, 0.8, a, SAND, MUTED, size=17, mono=i == 2, name=f"l{i}")
        k.chip(d, s, xs[1], ry, w, 0.8, b, WHITE, NAVY, size=17, bold=i == 0, line=ORANGE, name=f"r{i}")


def three_sentences(d):
    s, y = k.slide(d, "Your finding in three sentences",
                   "Temuan proyekmu dalam tiga kalimat. Pertama jawaban: apa yang kamu temukan. Kedua bukti: angka mana "
                   "yang menunjukkannya. Ketiga rekomendasi: apa yang harus dilakukan manajer. Jawaban selalu di depan; "
                   "cerita prosesnya tidak perlu. Ini juga exit ticket hari ini.", seconds=60)
    items = [("Answer", "what you found", "Class A sales stayed steady."),
             ("Evidence", "the numbers", "Each month, class A was close to 80%."),
             ("Recommendation", "what to do", "Keep class A stock safe every month.")]
    x0 = centred(11.0)
    for i, (head, sub, ex) in enumerate(items):
        ry = 1.8 + i * 1.3
        k.stop(d, s, x0, ry + 0.1, 0.8, str(i + 1), ORANGE if i == 0 else NAVY, WHITE, size=24)
        k.label(d, s, x0 + 1.1, ry, 3.0, 0.5, head, size=22, bold=True, align="left", name=f"h{i}")
        k.label(d, s, x0 + 1.1, ry + 0.5, 3.0, 0.4, sub, size=16, color=MUTED, align="left", name=f"s{i}")
        k.chip(d, s, x0 + 4.3, ry, 6.7, 1.0, ex, SAND, NAVY, size=17, name=f"e{i}")
    muted(d, s, 5.85, "Examples only. Write your own.")


def simply(d):
    s, y = k.slide(d, "Say numbers simply",
                   "Saat presentasi, angka yang panjang sulit diingat. 21,9 persen menjadi sekitar satu dari lima. "
                   "1.876.534,04 pounds menjadi sekitar 1,9 juta pounds. Angka lengkapnya tetap di notebook; di slide dan "
                   "di mulut, ucapkan yang sederhana. Coba ubah angka utamamu.", seconds=50)
    rows = [("21.9% of products", "about 1 in 5 products"), ("1,876,534.04 pounds", "about 1.9 million pounds"),
            ("84.82% of revenue", "about 85% of revenue")]
    x0 = centred(4.6 + 1.4 + 4.6)
    for i, (a, b) in enumerate(rows):
        ry = 1.9 + i * 1.0
        k.chip(d, s, x0, ry, 4.6, 0.75, a, SAND, NAVY, size=19, mono=True, name=f"a{i}")
        k.arrow(d, s, x0 + 4.8, ry + 0.22, 1.0, 0.32, fill=ORANGE)
        k.chip(d, s, x0 + 6.0, ry, 4.6, 0.75, b, ORANGE if i == 0 else NAVY, WHITE, size=19, bold=True,
               name=f"b{i}")
    muted(d, s, 5.2, "Exact in the notebook. Simple on the slide.")


def github(d):
    s, y = k.slide(d, "GitHub: four clicks",
                   "GitHub adalah tempat analis menunjukkan pekerjaannya. Kamu sudah punya akun dan repository kosong. "
                   "Empat langkah, dan kamu klik semuanya sendiri: simpan salinan dari Colab ke GitHub, buat file "
                   "README, tulis isinya dan commit, lalu buka link di jendela private untuk mengecek.", seconds=60)
    steps = [("Colab", "File > Save a copy in GitHub"), ("Add a file", "README.md"), ("Commit", "save the change"),
             ("Check", "open the link in a private window")]
    xs, w = cols(4)
    for i, (head, sub) in enumerate(steps):
        d.rect(s, xs[i], 1.9, w, 2.6, NAVY if i == 0 else SAND, name=f"s{i}")
        k.stop(d, s, xs[i] + w / 2 - 0.35, 2.15, 0.7, str(i + 1), ORANGE, WHITE, size=22)
        k.label(d, s, xs[i], 3.05, w, 0.5, head, size=22, bold=True, color=WHITE if i == 0 else NAVY)
        k.label(d, s, xs[i] + 0.2, 3.6, w - 0.4, 0.7, sub, size=16, color="C9D3DE" if i == 0 else MUTED,
                anchor="top")
    muted(d, s, 5.0, "You click every button yourself.")


def readme(d):
    s, y = k.slide(d, "The README is the front page",
                   "README adalah halaman depan proyekmu: orang membacanya sebelum membuka notebook. Empat bagian: "
                   "pertanyaan, sumber data dengan kredit yang benar, temuanmu, dan cara menjalankannya. Kalau waktunya "
                   "kurang, minimal: unggahan, satu grafik, dan satu kalimat temuan.", seconds=55)
    k.code_card(d, s, centred(10.6), 1.8, 10.6,
                ["# My project title", "", "**Question:** ...", "",
                 "**Data:** Chen (2012), Online Retail II, UCI. CC BY 4.0", "",
                 "**Finding:** ...", "", "**How to run:** open in Colab, run from the top."], size=16)


def slides(d):
    s, y = k.slide(d, "Your deck: five slides, five minutes",
                   "Presentasimu punya lima slide dari template: cover, pertanyaan, temuan, rekomendasi, terima kasih. "
                   "Lima menit: satu menit pertanyaan, dua menit temuan dan bukti, satu menit rekomendasi, satu menit "
                   "cadangan. Satu grafik per slide, dan jawaban di tiga puluh detik pertama. Ini yang kita latih hari ini, jadi kamu siap di sesi sepuluh.", seconds=60)
    parts = [("Cover", 0), ("Question", 1), ("Finding", 2), ("Recommendation", 1), ("Thank you", 0)]
    w, gap = 2.2, 0.2
    x0 = centred(5 * w + 4 * gap)
    for i, (t, mins) in enumerate(parts):
        x = x0 + i * (w + gap)
        hot = t == "Finding"
        d.rect(s, x, 1.9, w, 1.4, ORANGE if hot else SAND, name=f"p{i}")
        k.label(d, s, x, 1.9, w, 1.4, t, size=19, bold=True, color=WHITE if hot else NAVY, name=f"t{i}")
        if mins:
            k.label(d, s, x, 3.4, w, 0.4, f"{mins} min", size=18, bold=True, color=ORANGE_TEXT, name=f"m{i}")
    k.box(d, s, centred(7.6), 4.4, 7.6, "The answer comes in the first 30 seconds.", size=19)
    muted(d, s, 5.5, "Plus 1 spare minute. presentation_template.pptx")


def reflection(d):
    s, y = k.slide(d, "Reflection: due before Session 10",
                   "Refleksi satu halaman, enam pertanyaan, dikumpulkan sebelum sesi sepuluh. Apa yang sekarang bisa kamu "
                   "lakukan, kesalahan terbesar dan cara memperbaikinya, di mana masih butuh bantuan, apa yang akan kamu "
                   "ubah, rencana tiga puluh hari, dan satu hal yang kamu banggakan. Kita baca bersama di sesi terakhir.",
                   seconds=55)
    items = ["What I can do now", "My biggest mistake", "Where I need help", "What I would change",
             "My next 30 days", "One thing I am proud of"]
    xs, w = cols(3)
    for i, t in enumerate(items):
        x, ty = xs[i % 3], 1.8 + (i // 3) * 1.75
        d.rect(s, x, ty, w, 1.5, SAND, name=f"r{i}")
        k.stop(d, s, x + 0.3, ty + 0.45, 0.6, str(i + 1), ORANGE if i == 5 else NAVY, WHITE, size=18)
        k.label(d, s, x + 1.1, ty, w - 1.3, 1.5, t, size=19, bold=True, align="left", name=f"t{i}")
    muted(d, s, 5.5, "One page. reflection_template.md")


def now_colab(d):
    s, y = k.slide(d, "Now in Colab",
                   "Sekarang buka notebook s9_polish_publish. Mulai dengan latihan singkat merapikan grafik dan angka: "
                   "satu tebakan, satu isian, satu bug, dua kode. Lalu grafik akhirmu, tiga kalimat, dan GitHub. PR: "
                   "selesaikan slide, latihan bicara sekali, tulis refleksi.", seconds=30)
    k.ladder(d, s, M, 1.85, 8.0, 3.6, [("Predict", 1), ("Fill in", 1), ("Fix it", 1), ("Write it", 2),
                                       ("Project", 1)])
    d.text(s, 9.3, 1.9, 3.43, 4.2,
           [{"text": "Notebook", "bold": True, "color": ORANGE_TEXT, "size": 16},
            {"text": "s9_polish_publish", "after": 14},
            {"text": "Homework", "bold": True, "color": ORANGE_TEXT, "size": 16},
            {"text": "slides, rehearse, reflection", "after": 14},
            {"text": "Recall", "bold": True, "color": ORANGE_TEXT, "size": 16},
            {"text": "Tue 15, Wed 16 Dec"}],
           size=20, color=NAVY, name="side")


def thanks(d):
    k.thanks_next(d, "Terima kasih untuk hari ini. Proyekmu sekarang ada di GitHub, dan temuanmu bisa diucapkan dalam "
                     "tiga kalimat. Titik sembilan selesai. Berikutnya titik terakhir: presentasi, tanya jawab, dan "
                     "melihat kembali seluruh kursus. Latihan bicara sekali dengan suara keras.")


def build():
    d = k.lecture_deck(9)
    for make in (cover, goals, checklist, before_after, three_sentences, simply, github, readme, slides, reflection,
                 now_colab, thanks):
        make(d)
    k.save(d, OUT)


if __name__ == "__main__":
    build()
