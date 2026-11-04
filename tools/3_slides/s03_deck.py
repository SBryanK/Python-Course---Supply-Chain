"""Build the S3 deck: Let the loop do the walking.

Theory slides that the teacher talks over: a title, one visual anchor, and at most one short line.
The speaker notes carry the explanation; the notebook is the playground.
"""
from pathlib import Path

import deckkit as k
from deckkit import (M, CW, NAVY, ORANGE, ORANGE_TEXT, SAND, SKY, PEACH, CREAM, MUTED, CODE_INK, WHITE, cols,
                     centred, muted)

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "sessions" / "s03_let_loop_walk" / "deck.pptx"

QUANTITIES = [6, 6, 8, 6, 6, 2, 6]


def cover(d):
    k.cover_for(d, "for loops, functions, return, tracebacks",
                "Halo, selamat datang di sesi tiga. Dua titik sudah lewat. Pertanyaan hari ini: bisakah satu aturan "
                "memberi label ke setiap baris pesanan? Kita belajar loop dan function, dua alat yang membuat Python "
                "bekerja untuk kita. Siap?")


def goals(d):
    s, y = k.slide(d, "Today",
                   "Ini empat bagian hari ini. Satu, for loop: berjalan di sepanjang rak. Dua, function: aturan buatanmu "
                   "sendiri. Tiga, return: jawaban yang diserahkan kembali. Empat, membaca traceback. Setiap bagian punya "
                   "latihan di notebook.", seconds=35)
    items = [("for loops", "for q in quantities:"), ("Functions", "def order_size(q):"), ("return", "hand it back"),
             ("Tracebacks", "read from the bottom")]
    xs, w = cols(4)
    for i, (head, sub) in enumerate(items):
        d.rect(s, xs[i], 2.0, w, 2.6, SAND, name=f"g{i}")
        k.stop(d, s, xs[i] + w / 2 - 0.35, 2.3, 0.7, str(i + 1), ORANGE if i == 0 else NAVY, WHITE, size=22)
        k.label(d, s, xs[i], 3.2, w, 0.5, head, size=22, bold=True, name=f"gh{i}")
        k.label(d, s, xs[i] + 0.1, 3.75, w - 0.2, 0.4, sub, size=15, color=MUTED, mono=True, name=f"gs{i}")


def walk(d):
    s, y = k.slide(d, "A loop walks down the shelf",
                   "Loop berjalan di sepanjang rak dan mengecek setiap tempat, satu per satu. Di Excel, ini seperti "
                   "menarik rumus ke bawah. Setiap putaran, nama quantity berisi satu nilai berikutnya. Tujuh nilai, "
                   "tujuh putaran. Kita cukup menulis aturannya sekali.", seconds=55)
    w, gap = 1.3, 0.15
    x0 = centred(7 * w + 6 * gap)
    for i, q in enumerate(QUANTITIES):
        hot = i == 2
        k.chip(d, s, x0 + i * (w + gap), 1.95, w, 1.0, str(q), ORANGE if hot else SAND, WHITE if hot else NAVY,
               size=28, bold=True, mono=True, name=f"b{i}")
    k.arrow(d, s, x0, 3.15, 7 * w + 6 * gap, 0.32, fill=SKY)
    k.label(d, s, x0, 3.55, 7 * w + 6 * gap, 0.35, "one bin per turn", size=16, color=MUTED)
    k.code_card(d, s, centred(7.0), 4.25, 7.0, ["for quantity in quantities:", "    print(quantity)"], size=19)


def body(d):
    s, y = k.slide(d, "The indent is the loop body",
                   "Baris yang menjorok empat spasi adalah isi loop, dan dijalankan setiap putaran. Baris yang tidak "
                   "menjorok berjalan sekali saja, setelah loop selesai. Sama seperti aturan if di sesi dua: titik dua, "
                   "lalu indent. Menurutmu, berapa kali kata done dicetak?", seconds=60)
    lines = ["for quantity in quantities:", "    double = quantity * 2", "    print(double)", 'print("done")']
    k.code_card(d, s, centred(10.65), 1.85, 8.0, lines, size=20)
    x = centred(10.65) + 8.25
    k.chip(d, s, x, 2.35, 2.4, 0.6, "7 times", ORANGE, WHITE, size=17, bold=True, name="seven")
    k.chip(d, s, x, 3.15, 2.4, 0.6, "once", SAND, NAVY, size=17, bold=True, name="once")
    muted(d, s, 5.0, "Indented: every turn.  Not indented: after the loop.")


def function(d):
    s, y = k.slide(d, "A function is your own rule",
                   "Function adalah aturan buatanmu sendiri, seperti rumus Excel yang kamu beri nama. def artinya "
                   "define, membuat. Lalu nama, lalu input di dalam kurung, lalu titik dua. Batasnya: menulis def tidak "
                   "menjalankan apa pun. Function baru bekerja saat dipanggil.", seconds=60)
    parts = [("def", "make a rule"), ("order_size", "its name"), ("(quantity)", "its input"), (":", "body below")]
    ws = [1.3, 2.9, 2.6, 0.8]
    x = centred(sum(ws) + 0.5 * 3)
    for i, ((p, lab), w) in enumerate(zip(parts, ws)):
        k.chip(d, s, x, 1.95, w, 0.75, p, ORANGE if i == 1 else NAVY, WHITE if i == 1 else CODE_INK, size=20,
               mono=True, name=f"p{i}")
        k.label(d, s, x - 0.2, 2.8, w + 0.4, 0.35, lab, size=15, color=MUTED, name=f"pl{i}")
        x += w + 0.5
    k.box(d, s, centred(7.2), 4.1, 7.2, "Writing def runs nothing. Call it to use it.", size=18)


def calling(d):
    s, y = k.slide(d, "Write once, call many times",
                   "Ini function order_size dari aturan if sesi dua. Sekarang aturannya punya nama, jadi bisa dipanggil "
                   "berkali-kali dengan angka yang berbeda. Panggil dengan 6, hasilnya small. Panggil dengan 250, "
                   "hasilnya big. Satu aturan, dipakai di mana saja.", seconds=60)
    k.code_card(d, s, M + 0.3, 1.8, 6.4, ["def order_size(quantity):", "    if quantity >= 100:", '        return "big"',
                                          "    elif quantity >= 12:", '        return "medium"', "    else:",
                                          '        return "small"'], size=16)
    calls = [("order_size(6)", '"small"'), ("order_size(24)", '"medium"'), ("order_size(250)", '"big"')]
    for i, (c, r) in enumerate(calls):
        ry = 2.0 + i * 1.0
        k.chip(d, s, 7.6, ry, 3.0, 0.65, c, NAVY, CODE_INK, size=17, mono=True, name=f"c{i}")
        k.arrow(d, s, 10.75, ry + 0.18, 0.5, 0.28)
        k.chip(d, s, 11.35, ry, 1.38, 0.65, r, PEACH, NAVY, size=16, mono=True, name=f"r{i}")


def returning(d):
    s, y = k.slide(d, "return hands the answer back",
                   "return menyerahkan jawaban kembali ke yang memanggil, jadi bisa disimpan dan dipakai lagi. print hanya "
                   "menampilkan di layar, lalu hilang. Kalau function tidak punya return, hasilnya None, artinya kosong. "
                   "Ini kesalahan paling sering hari ini. Apa yang tersimpan di answer?", seconds=65)
    xs, w = cols(2, gap=0.5, w=11.0, x=centred(11.0))
    k.label(d, s, xs[0], 1.75, w, 0.4, "return", size=20, bold=True, color=ORANGE_TEXT, mono=True)
    k.code_card(d, s, xs[0], 2.25, w, ["def size_a(quantity):", '    return "small"', "", "answer = size_a(6)",
                                       "print(answer)"], output=["small"], size=16, name="a")
    k.label(d, s, xs[1], 1.75, w, 0.4, "print only", size=20, bold=True, color=MUTED, mono=True)
    k.code_card(d, s, xs[1], 2.25, w, ["def size_b(quantity):", '    print("small")', "", "answer = size_b(6)",
                                       "print(answer)"], output=["small", "None"], size=16, name="b")
    muted(d, s, 5.75, "No return: the answer is None.")


def two_inputs(d):
    s, y = k.slide(d, "A function can take two inputs",
                   "Function bisa menerima lebih dari satu input, dipisah koma. line_value menerima quantity dan price, "
                   "lalu mengembalikan nilainya yang sudah dibulatkan. Urutan input penting: yang pertama masuk ke "
                   "quantity, yang kedua ke price. Ini yang akan kamu tulis sendiri di notebook.", seconds=55)
    x0 = centred(2.0 + 0.5 + 2.0 + 1.0 + 3.6 + 1.0 + 2.0)
    k.chip(d, s, x0, 2.0, 2.0, 0.8, "6", SAND, NAVY, size=26, bold=True, mono=True, name="q")
    k.chip(d, s, x0 + 2.5, 2.0, 2.0, 0.8, "2.55", SAND, NAVY, size=26, bold=True, mono=True, name="p")
    k.arrow(d, s, x0 + 4.7, 2.22, 0.6, 0.36)
    k.chip(d, s, x0 + 5.5, 1.9, 3.6, 1.0, "line_value", NAVY, CODE_INK, size=22, mono=True, bold=True, name="f")
    k.arrow(d, s, x0 + 9.3, 2.22, 0.6, 0.36, fill=ORANGE)
    k.chip(d, s, x0 + 10.1, 2.0, 2.0, 0.8, "15.3", ORANGE, WHITE, size=26, bold=True, mono=True, name="r")
    k.label(d, s, x0, 2.9, 2.0, 0.35, "quantity", size=15, color=MUTED, mono=True)
    k.label(d, s, x0 + 2.5, 2.9, 2.0, 0.35, "price", size=15, color=MUTED, mono=True)
    k.code_card(d, s, centred(7.4), 3.8, 7.4, ["line_value(6, 2.55)"], output=["15.3"], size=19)


def loop_and_rule(d):
    s, y = k.slide(d, "Loop + function: label every line",
                   "Sekarang gabungkan keduanya. Loop berjalan di setiap quantity, dan setiap putaran memanggil "
                   "order_size. Hasilnya: setiap baris dapat label, dengan satu aturan yang sama. Ini jawaban pertanyaan "
                   "hari ini. Di sesi lima, pandas melakukan hal yang sama dengan apply.", seconds=60)
    k.code_card(d, s, M + 0.3, 1.85, 6.6, ["for quantity in [6, 24, 250]:", "    label = order_size(quantity)",
                                           '    print(f"{quantity} units -> {label}")'],
                output=["6 units -> small", "24 units -> medium", "250 units -> big"], size=16)
    for i, (q, lab) in enumerate([("6", "small"), ("24", "medium"), ("250", "big")]):
        ry = 2.0 + i * 0.95
        k.chip(d, s, 8.0, ry, 1.6, 0.7, q, SAND, NAVY, size=20, mono=True, bold=True, name=f"q{i}")
        k.arrow(d, s, 9.75, ry + 0.2, 0.7, 0.3, fill=ORANGE)
        k.chip(d, s, 10.6, ry, 2.13, 0.7, lab, ORANGE if i == 2 else NAVY, WHITE, size=19, bold=True, name=f"l{i}")


def records(d):
    s, y = k.slide(d, "A list of product cards",
                   "Data asli punya banyak kolom per baris. Kita gabungkan dua alat sesi dua: setiap baris adalah "
                   "dictionary, kartu produk, dan list menyimpan semua kartunya. Loop mengambil satu kartu per putaran, "
                   "lalu kita membaca isinya dengan nama key. Ini sudah sangat mirip tabel di sesi empat.", seconds=60)
    cards = [("WHITE HANGING HEART...", "6", "2.55"), ("WHITE METAL LANTERN", "6", "3.39"),
             ("CREAM CUPID HEARTS...", "8", "2.75")]
    xs, w = cols(3)
    for i, (desc, q, p) in enumerate(cards):
        d.rect(s, xs[i], 1.85, w, 2.3, WHITE, line=SAND, name=f"c{i}")
        d.rect(s, xs[i], 1.85, w, 0.1, ORANGE if i == 0 else SKY, rounded=False, name=f"ct{i}")
        k.label(d, s, xs[i] + 0.2, 2.1, w - 0.4, 0.45, desc, size=16, bold=True, name=f"d{i}")
        k.label(d, s, xs[i] + 0.2, 2.7, w - 0.4, 0.45, f"quantity  {q}", size=17, mono=True, name=f"q{i}")
        k.label(d, s, xs[i] + 0.2, 3.25, w - 0.4, 0.45, f"price  {p}", size=17, mono=True, name=f"p{i}")
    k.code_card(d, s, centred(9.0), 4.5, 9.0, ["for line in order_lines:", '    print(line["quantity"])'], size=18)


def traceback(d):
    s, y = k.slide(d, "A traceback is a stack of plates",
                   "Traceback menunjukkan jalan error dari luar ke dalam. Loop memanggil function, dan di dalam function "
                   "ada perbandingan teks dengan angka. Python menumpuk langkah-langkahnya seperti piring, dan yang "
                   "paling bawah adalah error-nya. Baca dari bawah: TypeError di baris if. Lalu naik: dipanggil dari "
                   "loop.", seconds=70)
    plates = [("for quantity in mixed_quantities:", "the loop calls"), ("    print(order_size(quantity))", "the function"),
              ("if quantity >= 100:", "where it broke")]
    x0 = centred(10.0)
    for i, (code, lab) in enumerate(plates):
        ry = 1.8 + i * 0.85
        k.chip(d, s, x0 + i * 0.4, ry, 7.0, 0.65, code, NAVY, CODE_INK, size=16, mono=True, name=f"pl{i}")
        k.label(d, s, x0 + 8.0, ry, 2.0, 0.65, lab, size=16, color=MUTED, align="left", name=f"lb{i}")
    k.chip(d, s, x0, 4.45, 10.0, 0.75, "TypeError: '>=' not supported between 'str' and 'int'", ORANGE, WHITE,
           size=17, mono=True, bold=True, name="last")
    k.label(d, s, x0, 5.3, 10.0, 0.4, "read the bottom line first, then go up", size=16, bold=True, color=ORANGE_TEXT)


def errors(d):
    s, y = k.slide(d, "Three mistakes you will meet",
                   "Tiga kesalahan umum hari ini. Indent hilang: IndentationError. return lupa: tidak ada error, tapi "
                   "hasilnya None, jadi lebih licik. Memanggil function sebelum def dijalankan: NameError. Yang kedua "
                   "paling sulit dilihat, karena Python tidak protes. Bagaimana kamu tahu return-nya hilang?",
                   seconds=60)
    items = [("IndentationError", "the body is not indented", "for q in quantities:\nprint(q)"),
             ("None", "the function has no return", "answer = size_b(6)"),
             ("NameError", "called before def ran", "line_value(6, 2.55)")]
    xs, w = cols(3)
    for i, (name, mean, ex) in enumerate(items):
        d.rect(s, xs[i], 1.8, w, 3.2, SAND, name=f"e{i}")
        k.label(d, s, xs[i], 2.05, w, 0.6, name, size=22, bold=True, mono=True, color=ORANGE_TEXT)
        k.label(d, s, xs[i] + 0.25, 2.85, w - 0.5, 0.8, mean, size=18, anchor="top")
        k.chip(d, s, xs[i] + 0.3, 3.95, w - 0.6, 0.75, ex, NAVY, CODE_INK, size=14, mono=True, name=f"x{i}")


def toolkit(d):
    s, y = k.slide(d, "Your toolkit so far",
                   "Ini ringkasan alat hari ini. Function dan loop akan kembali di sesi empat dan lima, dalam bentuk "
                   "pandas. Mana yang paling sulit diingat?", seconds=35)
    rows = [["Code", "Does"], ["for x in a_list:", "repeat for every value"], ["    (4 spaces)", "the loop or rule body"],
            ["def name(input):", "make your own rule"], ["return value", "hand the answer back"],
            ["name(6)", "call the rule"], ["None", "no answer came back"], ["traceback", "read from the bottom"]]
    k.ltable(d, s, centred(9.0), 1.7, 9.0, rows, [3.8, 5.2], code_cols=(0,), size=16, row_h=0.52)


def now_colab(d):
    s, y = k.slide(d, "Now in Colab",
                   "Sekarang kita pindah ke notebook s3_let_loop_walk. Tangganya: dua tebakan, dua isian, dua bug, tiga "
                   "kode yang kamu tulis sendiri, dan satu kasus pesanan besar. Siap?", seconds=30)
    k.ladder(d, s, M, 1.85, 8.0, 3.6, [("Predict", 2), ("Fill in", 2), ("Fix it", 2), ("Write it", 3), ("Case", 1)])
    d.text(s, 9.3, 1.9, 3.43, 4.2,
           [{"text": "Notebook", "bold": True, "color": ORANGE_TEXT, "size": 16},
            {"text": "s3_let_loop_walk", "after": 14},
            {"text": "Homework", "bold": True, "color": ORANGE_TEXT, "size": 16},
            {"text": "2 extras, mount Drive", "after": 14},
            {"text": "Recall", "bold": True, "color": ORANGE_TEXT, "size": 16},
            {"text": "Tue 24, Wed 25"}],
           size=20, color=NAVY, name="side")


def thanks(d):
    k.thanks_next(d, "Terima kasih untuk hari ini. Satu aturan sekarang bisa memberi label ke setiap baris. Titik tiga "
                     "selesai. Berikutnya titik empat, hari pembersihan: kita membuka data asli dengan pandas. Jangan "
                     "lupa mount Drive sekali di rumah, dan recall Selasa dan Rabu.")


def build():
    d = k.lecture_deck(3)
    for make in (cover, goals, walk, body, function, calling, returning, two_inputs, loop_and_rule, records,
                 traceback, errors, toolkit, now_colab, thanks):
        make(d)
    k.save(d, OUT)


if __name__ == "__main__":
    build()
