"""Build the S2 deck: Shelves, cards and choices.

Theory slides that the teacher talks over: a title, one visual anchor, and at most one short line.
The speaker notes carry the explanation; the notebook is the playground.
"""
from pathlib import Path

import deckkit as k
from deckkit import (M, CW, NAVY, ORANGE, ORANGE_TEXT, SAND, SKY, PEACH, CREAM, MUTED, CODE_INK, WHITE, cols,
                     centred, muted)

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "sessions" / "s02_shelves_cards_choices" / "deck.pptx"

QUANTITIES = [6, 6, 8, 6, 6, 2, 6]


def cover(d):
    k.cover_for(d, "lists, dictionaries, comparisons, if rules",
                "Halo, selamat datang di sesi dua. Satu titik sudah kita lewati. Hari ini pertanyaannya: baris pesanan "
                "mana yang besar? Untuk menjawabnya kita perlu menyimpan banyak nilai sekaligus, dan membuat aturan. "
                "Siap?")


def goals(d):
    s, y = k.slide(d, "Today",
                   "Ini empat bagian hari ini. Satu, list: banyak nilai di satu rak. Dua, menghitung isi list. Tiga, "
                   "dictionary: kartu produk. Empat, perbandingan dan aturan if. Setiap bagian punya latihan di "
                   "notebook.", seconds=35)
    items = [("Lists", "[6, 6, 8]"), ("Count and total", "len  sum  min  max"), ("Dictionaries", '{"quantity": 6}'),
             ("Choices", "==  if  elif  else")]
    xs, w = cols(4)
    for i, (head, sub) in enumerate(items):
        d.rect(s, xs[i], 2.0, w, 2.6, SAND, name=f"g{i}")
        k.stop(d, s, xs[i] + w / 2 - 0.35, 2.3, 0.7, str(i + 1), ORANGE if i == 0 else NAVY, WHITE, size=22)
        k.label(d, s, xs[i], 3.2, w, 0.5, head, size=22, bold=True, name=f"gh{i}")
        k.label(d, s, xs[i] + 0.1, 3.75, w - 0.2, 0.4, sub, size=15, color=MUTED, mono=True, name=f"gs{i}")


def shelf(d):
    s, y = k.slide(d, "A list is a row of bins",
                   "List adalah satu rak dengan banyak tempat, berurutan. Di Excel, ini seperti satu kolom berisi nilai. "
                   "Ditulis dengan kurung siku, dipisah koma. Ini tujuh quantity pertama dari data kita. Urutannya tetap, "
                   "jadi kita bisa memanggil isinya berdasarkan posisi.", seconds=55)
    w, gap = 1.3, 0.15
    x0 = centred(7 * w + 6 * gap)
    d.rect(s, x0 - 0.2, 3.05, 7 * w + 6 * gap + 0.4, 0.18, MUTED, rounded=False, name="shelf")
    for i, q in enumerate(QUANTITIES):
        d.rect(s, x0 + i * (w + gap), 1.85, w, 1.15, SAND, name=f"bin{i}")
        k.label(d, s, x0 + i * (w + gap), 1.85, w, 1.15, str(q), size=30, bold=True, mono=True, name=f"q{i}")
    k.code_card(d, s, centred(8.4), 4.0, 8.4, ["quantities = [6, 6, 8, 6, 6, 2, 6]"], size=19)
    muted(d, s, 5.3, "Like one column in Excel")


def index(d):
    s, y = k.slide(d, "Python counts from 0",
                   "Setiap tempat punya nomor posisi, namanya index. Python mulai dari nol, bukan satu. Jadi isi pertama "
                   "adalah quantities nol. Minus satu artinya yang terakhir, dihitung dari belakang. Kalau meminta nomor "
                   "yang tidak ada, misalnya tujuh, muncul IndexError. Menurutmu, berapa quantities dua?", seconds=65)
    w, gap = 1.3, 0.15
    x0 = centred(7 * w + 6 * gap)
    for i, q in enumerate(QUANTITIES):
        x = x0 + i * (w + gap)
        hot = i in (0, 6)
        k.chip(d, s, x, 1.95, w, 1.0, str(q), ORANGE if hot else SAND, WHITE if hot else NAVY, size=28, bold=True,
               mono=True, name=f"b{i}")
        k.label(d, s, x, 3.05, w, 0.4, str(i), size=20, bold=True, mono=True, color=ORANGE_TEXT if hot else NAVY,
                name=f"i{i}")
        k.label(d, s, x, 3.45, w, 0.35, str(i - 7), size=15, mono=True, color=MUTED, name=f"n{i}")
    k.label(d, s, x0 - 1.4, 3.05, 1.3, 0.4, "index", size=15, color=MUTED, align="right", name="li")
    k.label(d, s, x0 - 1.4, 3.45, 1.3, 0.35, "from end", size=15, color=MUTED, align="right", name="ln")
    xs, w2 = cols(2, gap=0.4, w=8.0, x=centred(8.0))
    k.code_card(d, s, xs[0], 4.3, w2, ["quantities[0]"], output=["6"], size=18, name="c0")
    k.code_card(d, s, xs[1], 4.3, w2, ["quantities[-1]"], output=["6"], size=18, name="c1")


def counting(d):
    s, y = k.slide(d, "Count, total, smallest, largest",
                   "Empat alat ini sama dengan COUNT, SUM, MIN dan MAX di Excel. Hanya ejaannya yang baru. len menghitung "
                   "berapa isi, sum menjumlahkan, min yang terkecil, max yang terbesar. Ini cara cepat melihat satu "
                   "kolom angka.", seconds=55)
    tools = [("len", "7", "COUNT"), ("sum", "40", "SUM"), ("min", "2", "MIN"), ("max", "8", "MAX")]
    xs, w = cols(4)
    for i, (fn, val, xl) in enumerate(tools):
        d.rect(s, xs[i], 1.85, w, 2.9, NAVY if i == 1 else SAND, name=f"t{i}")
        c = WHITE if i == 1 else NAVY
        k.label(d, s, xs[i], 2.05, w, 0.5, f"{fn}(quantities)", size=17, mono=True, color=CODE_INK if i == 1 else NAVY)
        k.label(d, s, xs[i], 2.65, w, 1.0, val, size=54, bold=True, color=ORANGE if i == 1 else ORANGE_TEXT)
        k.label(d, s, xs[i], 3.85, w, 0.45, f"Excel: {xl}", size=16, color="C9D3DE" if i == 1 else MUTED)
    muted(d, s, 5.35, "Same idea, new spelling.")


def card(d):
    s, y = k.slide(d, "A dictionary is a product card",
                   "Dictionary adalah kartu produk: setiap nilai punya nama. Nama di kiri disebut key, nilainya di kanan. "
                   "Di Excel, ini seperti satu baris dengan judul kolom. Ditulis dengan kurung kurawal, key dan nilai "
                   "dipisah titik dua. Bedanya dengan list: list memakai posisi, dictionary memakai nama.", seconds=60)
    fields = [("stock_code", '"85123A"'), ("quantity", "6"), ("price", "2.55"), ("country", '"United Kingdom"')]
    x0, w = centred(8.0), 8.0
    d.rect(s, x0, 1.8, w, 3.4, WHITE, line=SAND, name="card")
    d.rect(s, x0, 1.8, w, 0.12, ORANGE, rounded=False, name="card_top")
    for i, (key, val) in enumerate(fields):
        ry = 2.15 + i * 0.72
        k.chip(d, s, x0 + 0.4, ry, 2.8, 0.55, key, SAND, NAVY, size=17, mono=True, bold=True, name=f"k{i}")
        k.label(d, s, x0 + 3.5, ry, 4.2, 0.55, val, size=19, mono=True, align="left", name=f"v{i}")
    k.label(d, s, x0 + 0.4, 5.3, 2.8, 0.35, "key", size=16, bold=True, color=ORANGE_TEXT)
    k.label(d, s, x0 + 3.5, 5.3, 2.0, 0.35, "value", size=16, bold=True, color=ORANGE_TEXT, align="left")


def lookup(d):
    s, y = k.slide(d, "Look up by name, not by position",
                   "Untuk mengambil nilai, tulis nama kartu lalu key di kurung siku. Tidak perlu ingat posisinya. Kalau "
                   "key salah ketik, atau huruf besar kecilnya beda, Python memberi KeyError. Nama key harus persis "
                   "sama. Di sesi empat, nama kolom di pandas bekerja dengan cara yang sama.", seconds=55)
    k.code_card(d, s, centred(8.4), 1.85, 8.4, ['order_line["quantity"]'], output=["6"], size=20, name="ok")
    k.code_card(d, s, centred(8.4), 3.55, 8.4, ['order_line["Quantity"]'], output=["KeyError: 'Quantity'"], size=20,
                name="bad")
    muted(d, s, 5.35, "The key must match exactly.")


def compare(d):
    s, y = k.slide(d, "A comparison answers True or False",
                   "Perbandingan mengajukan pertanyaan, dan jawabannya True atau False. Di Excel, sama seperti A2 lebih "
                   "besar dari 10. Yang penting: satu tanda sama dengan menyimpan nilai, dua tanda sama dengan bertanya. "
                   "Ini kesalahan paling sering di awal. Apa jawaban 6 lebih besar dari 10?", seconds=60)
    rows = [("6 > 10", "False"), ("6 == 6", "True"), ('"UK" == "Germany"', "False")]
    x0 = centred(5.0 + 1.2 + 2.2)
    for i, (expr, res) in enumerate(rows):
        ry = 1.85 + i * 0.85
        k.chip(d, s, x0, ry, 5.0, 0.62, expr, NAVY, CODE_INK, size=18, mono=True, name=f"e{i}")
        k.arrow(d, s, x0 + 5.2, ry + 0.17, 0.8, 0.28)
        t = res == "True"
        k.chip(d, s, x0 + 6.2, ry, 2.2, 0.62, res, ORANGE if t else SAND, WHITE if t else NAVY, size=18, mono=True,
               name=f"r{i}")
    xs, w = cols(2, gap=0.4, w=8.0, x=centred(8.0))
    k.tile(d, s, xs[0], 4.55, w, 1.2, "=", "stores", mono=True, head_size=30, name="one")
    k.tile(d, s, xs[1], 4.55, w, 1.2, "==", "asks", mono=True, head_size=30, fill=PEACH, line=ORANGE, name="two")


def rule(d):
    s, y = k.slide(d, "if, elif, else: a packing rule",
                   "Aturan if seperti aturan di gudang. Cek syarat pertama; kalau benar, lakukan itu dan berhenti. Kalau "
                   "tidak, cek syarat berikutnya, elif. Kalau semua salah, lakukan else. Hanya satu cabang yang jalan. "
                   "Angka 100 dan 12 ini angka latihan, bukan aturan bisnis. Untuk quantity 6, cabang mana yang jalan?",
                   seconds=70)
    steps = [("quantity >= 100", "Big"), ("quantity >= 12", "Medium"), ("else", "Small")]
    x0 = centred(4.0 + 1.0 + 2.6)
    for i, (cond, out) in enumerate(steps):
        ry = 1.85 + i * 1.15
        last = i == 2
        k.chip(d, s, x0, ry, 4.0, 0.8, cond, NAVY, CODE_INK, size=19, mono=True, name=f"c{i}")
        k.arrow(d, s, x0 + 4.15, ry + 0.24, 0.7, 0.32, fill=ORANGE if last else MUTED)
        k.chip(d, s, x0 + 5.0, ry, 2.6, 0.8, out, ORANGE if last else SAND, WHITE if last else NAVY, size=20,
               bold=True, name=f"o{i}")
        if i < 2:
            k.label(d, s, x0, ry + 0.8, 4.0, 0.35, "no", size=14, color=MUTED, name=f"no{i}")
    muted(d, s, 5.5, "quantity = 6: only one branch runs.")


def indent(d):
    s, y = k.slide(d, "The colon and the indent",
                   "Dua hal kecil yang wajib: titik dua di akhir baris if, dan empat spasi di baris di bawahnya. Indent "
                   "itu bagian dari aturan, bukan hiasan. Itu cara Python tahu baris mana yang termasuk cabang itu. Tanpa "
                   "titik dua atau tanpa indent, muncul SyntaxError atau IndentationError.", seconds=60)
    k.code_card(d, s, centred(8.0), 1.85, 8.0,
                ["if quantity >= 100:", '    print("Big order line")', "elif quantity >= 12:",
                 '    print("Medium order line")', "else:", '    print("Small order line")'], size=19)
    k.chip(d, s, centred(8.0) + 8.25, 2.05, 1.9, 0.55, ":  ends it", ORANGE, WHITE, size=16, bold=True, name="colon")
    k.chip(d, s, centred(8.0) + 8.25, 2.75, 1.9, 0.55, "4 spaces", PEACH, NAVY, size=16, bold=True, name="sp")
    k.box(d, s, centred(7.6), 5.25, 7.6, "No colon or no indent: the rule breaks.", size=18)


def errors(d):
    s, y = k.slide(d, "Three errors you will meet",
                   "Tiga error baru hari ini. IndexError: meminta posisi yang tidak ada di list. KeyError: key tidak ada "
                   "di dictionary, sering karena huruf besar. SyntaxError: titik dua lupa. Seperti biasa, baca baris "
                   "terakhir dulu. Mana yang paling mungkin kamu buat?", seconds=55)
    items = [("IndexError", "no bin at that position", "quantities[7]"),
             ("KeyError", "no field with that name", 'order_line["Price"]'),
             ("SyntaxError", "the colon is missing", "if quantity > 12")]
    xs, w = cols(3)
    for i, (name, mean, ex) in enumerate(items):
        d.rect(s, xs[i], 1.8, w, 3.2, SAND, name=f"e{i}")
        k.label(d, s, xs[i], 2.05, w, 0.6, name, size=24, bold=True, mono=True, color=ORANGE_TEXT)
        k.label(d, s, xs[i] + 0.25, 2.85, w - 0.5, 0.8, mean, size=18, anchor="top")
        k.chip(d, s, xs[i] + 0.3, 4.05, w - 0.6, 0.6, ex, NAVY, CODE_INK, size=16, mono=True, name=f"x{i}")


def lines_not_orders(d):
    s, y = k.slide(d, "A big line, not a big order",
                   "Satu hal penting tentang data kita: setiap baris adalah satu produk di satu invoice. Satu invoice bisa "
                   "punya banyak baris. Jadi hari ini kita bertanya tentang baris yang besar, bukan pesanan yang besar. "
                   "Pesanan utuh baru kita hitung di sesi empat. Kenapa perbedaan ini penting untuk laporan?",
                   seconds=55)
    k.chip(d, s, centred(10.0), 1.85, 10.0, 0.7, "Invoice 536365", NAVY, WHITE, size=20, bold=True, name="inv")
    lines = ["WHITE HANGING HEART T-LIGHT HOLDER   6", "WHITE METAL LANTERN   6", "CREAM CUPID HEARTS COAT HANGER   8"]
    for i, t in enumerate(lines):
        k.chip(d, s, centred(10.0) + 0.6, 2.75 + i * 0.68, 9.4, 0.56, t, WHITE if i else PEACH, NAVY, size=17,
               mono=True, line=SAND, name=f"l{i}")
    k.label(d, s, centred(10.0), 4.85, 10.0, 0.4, "one row = one product on one invoice", size=18, bold=True,
            color=ORANGE_TEXT)


def toolkit(d):
    s, y = k.slide(d, "Your toolkit so far",
                   "Ini ringkasan alat hari ini. List dan dictionary akan muncul lagi di sesi tiga dan empat, dalam "
                   "bentuk tabel pandas. Mana yang paling sulit diingat?", seconds=35)
    rows = [["Code", "Does"], ["[6, 6, 8]", "a list: values in order"], ["quantities[0]", "the first value"],
            ["quantities[-1]", "the last value"], ["len  sum  min  max", "count, total, smallest, largest"],
            ['{"quantity": 6}', "a dictionary: values by name"], ['order_line["quantity"]', "look up by name"],
            ["==  !=  >  >=", "compare, gives True or False"], ["if / elif / else", "choose one branch"]]
    k.ltable(d, s, centred(9.6), 1.7, 9.6, rows, [4.2, 5.4], code_cols=(0,), size=16, row_h=0.5)


def now_colab(d):
    s, y = k.slide(d, "Now in Colab",
                   "Sekarang kita pindah ke notebook s2_shelves_cards_choices. Tangganya: dua tebakan, dua isian, dua "
                   "bug, tiga kode yang kamu tulis sendiri, dan satu kasus. Siap?", seconds=30)
    k.ladder(d, s, M, 1.85, 8.0, 3.6, [("Predict", 2), ("Fill in", 2), ("Fix it", 2), ("Write it", 3), ("Case", 1)])
    d.text(s, 9.3, 1.9, 3.43, 4.2,
           [{"text": "Notebook", "bold": True, "color": ORANGE_TEXT, "size": 16},
            {"text": "s2_shelves_cards", "after": 14},
            {"text": "Homework", "bold": True, "color": ORANGE_TEXT, "size": 16},
            {"text": "2 extras", "after": 14},
            {"text": "Recall", "bold": True, "color": ORANGE_TEXT, "size": 16},
            {"text": "Thu 19 to Sun 22"}],
           size=20, color=NAVY, name="side")


def thanks(d):
    k.thanks_next(d, "Terima kasih untuk hari ini. Kamu sudah memakai list, dictionary dan aturan if. Titik dua "
                     "selesai. Berikutnya titik tiga: loop dan function, supaya satu aturan bisa memberi label ke setiap "
                     "baris. Jangan lupa recall Kamis sampai Minggu.")


def build():
    d = k.lecture_deck(2)
    for make in (cover, goals, shelf, index, counting, card, lookup, compare, rule, indent, lines_not_orders, errors,
                 toolkit, now_colab, thanks):
        make(d)
    k.save(d, OUT)


if __name__ == "__main__":
    build()
