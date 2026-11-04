"""Build the S1 deck: Hello, Python.

Theory slides that the teacher talks over: a title, one visual anchor, and at most one short line.
The speaker notes carry the explanation; the notebook is the playground.
"""
from pathlib import Path

import deckkit as k
from deckkit import (M, CW, NAVY, ORANGE, ORANGE_TEXT, SAND, SKY, PEACH, CREAM, MUTED, CODE_INK, WHITE, cols,
                     centred, muted)

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "sessions" / "s01_hello_python" / "deck.pptx"


def cover(d):
    k.cover_for(d, "print, variables, types, f-strings, errors",
                "Halo, selamat datang di sesi pertama dari sepuluh. Lihat jalannya: sepuluh titik, dan hari ini kita "
                "di titik satu. Pertanyaan hari ini sederhana: berapa nilai satu baris pesanan? Kita bergantian: teori "
                "sebentar di slide, lalu kamu yang mengetik di notebook. Siap?")


def goals(d):
    s, y = k.slide(d, "Today",
                   "Ini enam bagian hari ini. Satu, Colab dan cara menjalankan sel. Dua, print. Tiga, variabel. Empat, "
                   "tipe data. Lima, menghitung dan membulatkan. Enam, f-string dan membaca error. Setiap bagian punya "
                   "latihan di notebook.", seconds=35)
    items = [("Colab", "Shift + Enter"), ("print", "show a value"), ("Variables", "a label on a bin"),
             ("Types", "int  float  str"), ("Maths", "*  round()"), ("f-strings, errors", 'f"...{x}"')]
    xs, w = cols(3)
    for i, (head, sub) in enumerate(items):
        x, ty = xs[i % 3], 1.75 + (i // 3) * 2.45
        d.rect(s, x, ty, w, 2.15, SAND, name=f"g{i}")
        k.stop(d, s, x + 0.35, ty + 0.35, 0.6, str(i + 1), ORANGE if i == 0 else NAVY, WHITE, size=20)
        k.label(d, s, x + 0.35, ty + 1.08, w - 0.7, 0.45, head, size=22, bold=True, align="left", name=f"gh{i}")
        k.label(d, s, x + 0.35, ty + 1.55, w - 0.7, 0.4, sub, size=15, color=MUTED, mono=True, align="left",
                name=f"gs{i}")


def why(d):
    s, y = k.slide(d, "Why Python for supply chain",
                   "Kenapa Python? Tiga alasan. File Excel yang sangat besar mulai lambat. Pekerjaan yang sama setiap "
                   "minggu bisa dijalankan lagi dengan satu klik. Dan setiap langkah tertulis, jadi atasan bisa melihat "
                   "persis apa yang kamu lakukan. Excel tetap dipakai; Python mengambil bagian yang berat. Di "
                   "pekerjaanmu, bagian mana yang paling sering diulang?", seconds=50)
    items = [("Big files", "100,000 rows and more"), ("Repeat work", "run the weekly steps again"),
             ("Show your work", "every step is written down")]
    xs, w = cols(3)
    for i, (head, sub) in enumerate(items):
        k.tile(d, s, xs[i], 2.0, w, 2.4, head, sub, head_size=26, name=f"w{i}",
               fill=NAVY if i == 0 else SAND, head_color=WHITE if i == 0 else NAVY,
               sub_color="C9D3DE" if i == 0 else MUTED)
    muted(d, s, 5.2, "Excel stays. Python takes the heavy part.")


def colab(d):
    s, y = k.slide(d, "Colab: text cells and code cells",
                   "Ini Colab, notebook di browser. Ada dua jenis kotak. Kotak teks berisi penjelasan. Kotak kode berisi "
                   "Python. Klik kotak kode, tekan Shift dan Enter, dan hasilnya muncul tepat di bawahnya. Tidak perlu "
                   "install apa pun, cukup akun Google. Menurutmu, di mana hasilnya muncul?", seconds=60)
    x0 = centred(11.45)
    d.rect(s, x0, 1.8, 9.0, 0.8, WHITE, line=SAND, name="text_cell")
    k.label(d, s, x0 + 0.3, 1.8, 8.4, 0.8, "## Variables   (a text cell)", size=18, color=MUTED, align="left",
            name="tc")
    k.code_card(d, s, x0, 2.85, 9.0, ['quantity = 6', 'print(quantity)'], output=["6"], size=18)
    k.chip(d, s, x0 + 9.25, 3.0, 2.2, 0.62, "Shift + Enter", ORANGE, WHITE, size=17, bold=True, name="key")
    k.label(d, s, x0 + 9.25, 3.7, 2.2, 0.35, "runs the cell", size=15, color=MUTED)
    muted(d, s, 5.6, "The result shows right under the cell.")


def order(d):
    s, y = k.slide(d, "Run cells from the top",
                   "Notebook menjalankan sel sesuai urutan kamu klik, bukan urutan di layar. Kalau sel tiga dijalankan "
                   "sebelum sel satu, Python belum kenal namanya dan memberi NameError. Jadi kalau muncul NameError, "
                   "jalankan dulu sel-sel di atasnya. Notebook tidak ingat apa yang kamu ubah di kepalamu.", seconds=55)
    cells = [("1", "quantity = 6"), ("2", "unit_price = 2.55"), ("3", "print(quantity * unit_price)")]
    x0 = centred(9.4)
    for i, (n, code) in enumerate(cells):
        ry = 1.8 + i * 0.95
        k.stop(d, s, x0, ry, 0.7, n, ORANGE if i == 2 else NAVY, WHITE, size=20)
        k.chip(d, s, x0 + 1.0, ry, 8.4, 0.7, code, NAVY, CODE_INK, size=18, mono=True, name=f"c{i}")
    k.box(d, s, centred(7.6), 5.0, 7.6, "NameError? Run the cells above first.", size=18)


def printing(d):
    s, y = k.slide(d, "print shows a value",
                   "print itu seperti membaca label keras-keras. Python tidak menampilkan apa pun kalau tidak diminta. "
                   "Teks ditulis di dalam tanda kutip, angka tanpa kutip. Satu print, satu baris hasil. Di Excel, kamu "
                   "mengetik di sel dan langsung terlihat; di Python, kamu meminta dengan print.", seconds=50)
    k.code_card(d, s, centred(8.0), 1.9, 8.0, ['print("Hello, supply chain")', "print(6)"],
                output=["Hello, supply chain", "6"], size=20)
    xs, w = cols(2, gap=0.4, w=8.0, x=centred(8.0))
    k.tile(d, s, xs[0], 4.65, w, 1.1, '"text"', "in quotes", mono=True, head_size=22, name="q")
    k.tile(d, s, xs[1], 4.65, w, 1.1, "6", "no quotes", mono=True, head_size=22, name="n")


def variable(d):
    s, y = k.slide(d, "A variable is a label on a bin",
                   "Variabel adalah label di tempat penyimpanan. Kamu simpan nilai di dalamnya, lalu panggil lagi dengan "
                   "namanya. Tanda sama dengan artinya simpan, bukan sama dengan seperti di matematika. Di Excel, ini "
                   "seperti sel yang diberi nama. Nama yang baik bilang isinya: quantity, unit_price.", seconds=60)
    bins = [("product_name", '"WHITE HANGING HEART..."'), ("quantity", "6"), ("unit_price", "2.55")]
    widths = [4.6, 2.6, 2.6]
    x = centred(sum(widths) + 0.5 * 2)
    for i, ((name, val), w) in enumerate(zip(bins, widths)):
        k.chip(d, s, x, 1.85, w, 0.55, name, ORANGE, WHITE, size=17, mono=True, bold=True, name=f"l{i}")
        d.rect(s, x, 2.45, w, 1.4, SAND, name=f"b{i}")
        k.label(d, s, x, 2.45, w, 1.4, val, size=20 if i else 15, mono=True, name=f"v{i}")
        x += w + 0.5
    k.code_card(d, s, centred(8.0), 4.35, 8.0, ['quantity = 6', 'print(quantity)'], output=["6"], size=17)


def update(d):
    s, y = k.slide(d, "Change it, then run again",
                   "Kalau quantity diubah dari 6 menjadi 7, isinya berganti. Tapi sel lain tidak ikut berubah sendiri, "
                   "berbeda dengan Excel yang otomatis menghitung ulang. Di notebook, kamu harus menjalankan selnya lagi. "
                   "Menurutmu, apa yang dicetak sel lama kalau tidak dijalankan ulang?", seconds=55)
    x0 = centred(2.6 * 2 + 1.6)
    k.tile(d, s, x0, 2.0, 2.6, 1.6, "6", "quantity before", mono=True, head_size=40, name="a")
    k.arrow(d, s, x0 + 2.8, 2.6, 1.2, 0.42, fill=ORANGE)
    k.label(d, s, x0 + 2.6, 3.1, 1.6, 0.35, "quantity = 7", size=14, mono=True, color=ORANGE_TEXT, bold=True)
    k.tile(d, s, x0 + 4.2, 2.0, 2.6, 1.6, "7", "quantity after", mono=True, head_size=40, fill=NAVY,
           head_color=WHITE, sub_color="C9D3DE", name="b")
    k.box(d, s, centred(8.4), 4.5, 8.4, "Excel updates by itself. A notebook does not. Run the cell again.", size=18)


def types(d):
    s, y = k.slide(d, "Three types of value",
                   "Python membedakan tiga tipe di sesi ini. int untuk bilangan bulat, seperti jumlah kotak. float untuk "
                   "angka desimal, seperti harga. str untuk teks, seperti nama produk. Di Excel ada format angka dan "
                   "format teks; di Python namanya tipe. type memberitahu tipe sebuah nilai.", seconds=60)
    cards = [("int", "6", "counting boxes"), ("float", "2.55", "a price, a weight"),
             ("str", '"LANTERN"', "a product name")]
    xs, w = cols(3)
    for i, (t, ex, use) in enumerate(cards):
        d.rect(s, xs[i], 1.8, w, 2.7, SAND, name=f"d{i}")
        k.label(d, s, xs[i], 2.0, w, 0.6, t, size=30, mono=True, bold=True, color=ORANGE_TEXT)
        k.label(d, s, xs[i], 2.8, w, 0.6, ex, size=22, mono=True)
        k.label(d, s, xs[i], 3.6, w, 0.5, use, size=17, color=MUTED)
    k.code_card(d, s, centred(6.0), 4.95, 6.0, ["type(2.55)"], output=["<class 'float'>"], size=17)


def text_numbers(d):
    s, y = k.slide(d, '"5" is text, not a number',
                   "Ini jebakan yang sering muncul. Lima tanpa kutip adalah angka, lima dengan kutip adalah teks. Angka "
                   "ditambah angka menjadi sepuluh. Teks ditambah teks ditempel menjadi lima lima. Teks ditambah angka? "
                   "Python menolak dan memberi TypeError. Di data asli, angka kadang terbaca sebagai teks. Bagaimana "
                   "kamu tahu?", seconds=60)
    rows = [("5 + 5", "10", WHITE), ('"5" + "5"', '"55"', WHITE), ('"5" + 5', "TypeError", PEACH)]
    x0 = centred(3.4 + 1.2 + 3.4)
    for i, (expr, res, f) in enumerate(rows):
        ry = 1.9 + i * 1.0
        k.chip(d, s, x0, ry, 3.4, 0.72, expr, NAVY, CODE_INK, size=20, mono=True, name=f"e{i}")
        k.arrow(d, s, x0 + 3.6, ry + 0.2, 0.8, 0.32)
        k.chip(d, s, x0 + 4.6, ry, 3.4, 0.72, res, f, ORANGE_TEXT if i == 2 else NAVY, size=20, mono=True,
               bold=i == 2, line=SAND, name=f"r{i}")
    muted(d, s, 5.3, "Quotes make text.")


def maths(d):
    s, y = k.slide(d, "Python as a calculator",
                   "Tanda hitung di Python sama dengan Excel: tambah, kurang, kali dengan bintang, bagi dengan garis "
                   "miring. Nilai satu baris pesanan adalah quantity kali unit_price, seperti B2 kali C2 di Excel. "
                   "Hasilnya bisa disimpan di variabel baru, sales_value. Jadi ini rumus pertama yang kamu tulis sendiri di notebook, dan kita pakai lagi nanti.", seconds=50)
    syms = [("+", "add"), ("-", "subtract"), ("*", "multiply"), ("/", "divide")]
    xs, w = cols(4)
    for i, (sym, mean) in enumerate(syms):
        d.rect(s, xs[i], 1.8, w, 2.0, PEACH if i == 2 else SAND, line=ORANGE if i == 2 else None, name=f"y{i}")
        k.label(d, s, xs[i], 1.95, w, 1.0, sym, size=54, bold=True, color=ORANGE_TEXT, mono=True)
        k.label(d, s, xs[i], 3.05, w, 0.45, mean, size=18, bold=True)
    k.code_card(d, s, centred(8.6), 4.3, 8.6, ["sales_value = quantity * unit_price"], size=19)
    muted(d, s, 5.55, "Like =B2*C2 in Excel")


def float_surprise(d):
    s, y = k.slide(d, "6 × 2.55 is not exactly 15.3",
                   "Ini momen kejutan. Enam kali 2,55 dicetak 15.299999999999999. Bukan salah ketik. Komputer menyimpan "
                   "desimal dalam biner, dan 2,55 tidak bisa disimpan persis, seperti sepertiga tidak bisa ditulis persis "
                   "dalam desimal. Selisihnya sangat kecil. Solusinya: bulatkan uang saat ditampilkan.", seconds=60)
    x0 = centred(1.5 + 0.8 + 1.8 + 0.8 + 6.0)
    k.chip(d, s, x0, 2.1, 1.5, 0.9, "6", SAND, NAVY, size=28, bold=True, name="a")
    k.label(d, s, x0 + 1.5, 2.1, 0.8, 0.9, "×", size=34, bold=True, color=MUTED)
    k.chip(d, s, x0 + 2.3, 2.1, 1.8, 0.9, "2.55", SAND, NAVY, size=28, bold=True, name="b")
    k.label(d, s, x0 + 4.1, 2.1, 0.8, 0.9, "=", size=34, bold=True, color=MUTED)
    k.chip(d, s, x0 + 4.9, 2.1, 6.0, 0.9, "15.299999999999999", ORANGE, WHITE, size=28, bold=True, mono=True,
           name="r")
    k.box(d, s, centred(6.6), 4.1, 6.6, "Round money when you show it.", size=20)


def rounding(d):
    s, y = k.slide(d, "round keeps two decimals",
                   "round menerima dua hal: angkanya dan berapa desimal. Untuk uang, dua desimal. Hitung dengan nilai "
                   "lengkap, bulatkan hanya di akhir saat menampilkan. Kalau dibulatkan di tengah, selisih kecil bisa "
                   "menumpuk. Sama seperti fungsi ROUND di Excel.", seconds=50)
    x0 = centred(5.4 + 2.6 + 2.2)
    k.chip(d, s, x0, 2.0, 5.4, 0.8, "15.299999999999999", SAND, NAVY, size=22, mono=True, name="a")
    k.arrow(d, s, x0 + 5.6, 2.22, 2.2, 0.36, fill=ORANGE)
    k.label(d, s, x0 + 5.4, 2.7, 2.6, 0.35, "round(x, 2)", size=16, bold=True, mono=True, color=ORANGE_TEXT)
    k.chip(d, s, x0 + 8.0, 2.0, 2.2, 0.8, "15.3", ORANGE, WHITE, size=26, bold=True, mono=True, name="b")
    k.code_card(d, s, centred(7.0), 3.75, 7.0, ["print(round(sales_value, 2))"], output=["15.3"], size=19)
    muted(d, s, 5.5, "Like ROUND(B2*C2, 2) in Excel")


def fstring(d):
    s, y = k.slide(d, "An f-string fills in the blanks",
                   "f-string adalah label isian. Huruf f di depan tanda kutip, lalu nama variabel di dalam kurung "
                   "kurawal. Python mengganti setiap kurung kurawal dengan nilainya. Yang paling sering lupa: huruf f. "
                   "Tanpa f, kurung kurawal tercetak apa adanya. Kalimat seperti ini yang kamu kirim ke manajer.",
                   seconds=60)
    k.code_card(d, s, centred(11.0), 1.85, 11.0, ['print(f"We sold {quantity} units for {round(sales_value, 2)} pounds")'],
                output=["We sold 6 units for 15.3 pounds"], size=17)
    marks = [("f", "before the quote"), ("{quantity}", "the value goes here")]
    xs, w = cols(2, gap=0.4, w=8.0, x=centred(8.0))
    for x, (head, sub) in zip(xs, marks):
        k.tile(d, s, x, 4.1, w, 1.3, head, sub, mono=True, head_size=24, name="m")
    muted(d, s, 5.8, "No f: the braces print as they are.")


def tracebacks(d):
    s, y = k.slide(d, "Read an error from the bottom",
                   "Error itu normal, analis melihatnya setiap hari. Pesan error panjang, tapi jawabannya ada di baris "
                   "terakhir: nama error dan artinya. Baca dari bawah dulu, lalu naik untuk melihat baris mana yang "
                   "salah. Panah kecil menunjuk baris kodenya.", seconds=55)
    lines = ["NameError        Traceback (most recent call last)", "<ipython-input-3> in <cell line: 1>()",
             "----> 1 print(quantiy)", ""]
    k.code_card(d, s, centred(10.0), 1.8, 10.0, lines[:3], size=16)
    k.chip(d, s, centred(10.0), 3.75, 10.0, 0.7, "NameError: name 'quantiy' is not defined", ORANGE, WHITE, size=18,
           mono=True, bold=True, name="last")
    k.label(d, s, centred(10.0), 4.55, 10.0, 0.4, "read this line first", size=16, bold=True, color=ORANGE_TEXT)


def errors(d):
    s, y = k.slide(d, "Three errors you will meet",
                   "Tiga error yang paling sering hari ini. NameError: Python tidak kenal namanya, biasanya salah ketik "
                   "atau sel di atas belum dijalankan. SyntaxError: kurung atau kutip kurang. TypeError: mencampur teks "
                   "dan angka. Di notebook, kamu akan memperbaiki ketiganya. Mana yang paling mungkin kamu buat?",
                   seconds=60)
    items = [("NameError", "unknown name", "print(quantiy)"), ("SyntaxError", "a bracket or quote is missing",
                                                                 'print("hello"'),
             ("TypeError", "text and a number mixed", '"5" + 5')]
    xs, w = cols(3)
    for i, (name, mean, ex) in enumerate(items):
        d.rect(s, xs[i], 1.8, w, 3.2, SAND, name=f"e{i}")
        k.label(d, s, xs[i], 2.05, w, 0.6, name, size=24, bold=True, mono=True, color=ORANGE_TEXT)
        k.label(d, s, xs[i] + 0.25, 2.85, w - 0.5, 0.8, mean, size=18, anchor="top")
        k.chip(d, s, xs[i] + 0.3, 4.05, w - 0.6, 0.6, ex, NAVY, CODE_INK, size=16, mono=True, name=f"x{i}")


def toolkit(d):
    s, y = k.slide(d, "Your first toolkit",
                   "Ini ringkasan alat hari ini, seperti contekan. Kamu akan memakai semuanya lagi di setiap sesi. Mana "
                   "yang paling sulit diingat?", seconds=35)
    rows = [["Code", "Does"], ["print(x)", "show a value"], ["quantity = 6", "store a value in a name"],
            ["type(x)", "int, float or str"], ["*  /  +  -", "multiply, divide, add, subtract"],
            ["round(x, 2)", "keep 2 decimals"], ['f"...{x}..."', "a sentence with values"]]
    k.ltable(d, s, centred(9.0), 1.75, 9.0, rows, [3.6, 5.4], code_cols=(0,), size=16, row_h=0.55)


def now_colab(d):
    s, y = k.slide(d, "Now in Colab",
                   "Sekarang kita pindah ke notebook s1_hello_python. Latihannya naik seperti tangga: dua tebakan, satu "
                   "isian, tiga bug yang harus diperbaiki, tiga kode yang kamu tulis sendiri, dan satu kasus invoice. "
                   "Kamu yang mengetik semuanya. Siap?", seconds=35)
    k.ladder(d, s, M, 1.85, 8.0, 3.6, [("Predict", 2), ("Fill in", 1), ("Fix it", 3), ("Write it", 3), ("Case", 1)])
    d.text(s, 9.3, 1.9, 3.43, 4.2,
           [{"text": "Notebook", "bold": True, "color": ORANGE_TEXT, "size": 16},
            {"text": "s1_hello_python", "after": 14},
            {"text": "Homework", "bold": True, "color": ORANGE_TEXT, "size": 16},
            {"text": "2 extras", "after": 14},
            {"text": "Recall", "bold": True, "color": ORANGE_TEXT, "size": 16},
            {"text": "Tue 17 Nov"}],
           size=20, color=NAVY, name="side")


def thanks(d):
    k.thanks_next(d, "Terima kasih untuk hari ini. Kamu sudah menulis Python pertamamu dan menghitung nilai satu baris "
                     "pesanan. Titik satu selesai. Berikutnya titik dua: daftar, kartu produk dan aturan if, untuk "
                     "mencari baris pesanan yang besar. Jangan lupa recall hari Selasa.")


def build():
    d = k.lecture_deck(1)
    for make in (cover, goals, why, colab, order, printing, variable, update, types, text_numbers, maths,
                 float_surprise, rounding, fstring, tracebacks, errors, toolkit, now_colab, thanks):
        make(d)
    k.save(d, OUT)


if __name__ == "__main__":
    build()
