"""Build the S5 deck: Who are the star products?

Theory slides that the teacher talks over: a title, one visual anchor, and at most one short line.
The speaker notes carry the explanation; the notebook is the playground.
"""
from pathlib import Path

import deckkit as k
from deckkit import (M, CW, NAVY, ORANGE, ORANGE_TEXT, SAND, SKY, PEACH, CREAM, MUTED, CODE_INK, WHITE, cols,
                     centred, muted)

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "sessions" / "s05_star_products" / "deck.pptx"

# From the S5 notebook run on the clean table: products and revenue share per class
ABC = [("A", 671, 21.9, 80.0), ("B", 794, 25.9, 15.0), ("C", 1601, 52.2, 5.0)]


def cover(d):
    k.cover_for(d, "groupby, running totals, ABC classes, a cold test",
                "Halo, selamat datang di sesi lima. Empat titik sudah lewat, dan tabel bersihmu sudah tersimpan di "
                "Drive. Pertanyaan hari ini: produk mana yang membawa sebagian besar uang? Di blok kedua ada cold test "
                "dua puluh menit. Siap?")


def goals(d):
    s, y = k.slide(d, "Today",
                   "Ini empat bagian hari ini. Satu, memuat tabel bersih dan mengecek bentuknya. Dua, groupby, "
                   "PivotTable dalam kode. Tiga, running total dan kelas ABC. Empat, cold test di blok kedua. Setiap "
                   "bagian punya latihan di notebook.", seconds=35)
    items = [("Load and check", "(101458, 10)"), ("Group and sum", "groupby  sum"), ("ABC classes", "cumsum  apply"),
             ("Cold test", "20 minutes, notes allowed")]
    xs, w = cols(4)
    for i, (head, sub) in enumerate(items):
        d.rect(s, xs[i], 2.0, w, 2.6, SAND, name=f"g{i}")
        k.stop(d, s, xs[i] + w / 2 - 0.35, 2.3, 0.7, str(i + 1), ORANGE if i == 0 else NAVY, WHITE, size=22)
        k.label(d, s, xs[i], 3.2, w, 0.5, head, size=22, bold=True, name=f"gh{i}")
        k.label(d, s, xs[i] + 0.1, 3.75, w - 0.2, 0.4, sub, size=15, color=MUTED, mono=True, name=f"gs{i}")


def load(d):
    s, y = k.slide(d, "Start from your clean table",
                   "Kita mulai dari file yang kamu simpan di sesi empat, bukan data mentah. CSV menyimpan teks, jadi "
                   "tanggal lupa bahwa dia tanggal; kita ubah lagi dengan to_datetime. Lalu cek shape. Harus 101458 "
                   "baris dan 10 kolom. Kalau beda, berhenti dan perbaiki dulu. Kenapa cek ini penting?", seconds=60)
    x0 = centred(4.0 * 2 + 2.0)
    k.tile(d, s, x0, 1.85, 4.0, 1.5, "Session 4", "sales_clean.csv", head_size=24, sub_mono=True, name="a")
    k.arrow(d, s, x0 + 4.25, 2.4, 1.5, 0.42, fill=ORANGE)
    k.tile(d, s, x0 + 6.0, 1.85, 4.0, 1.5, "Session 5", "starts here", head_size=24, fill=NAVY, head_color=WHITE,
           sub_color="C9D3DE", name="b")
    k.code_card(d, s, centred(11.0), 3.75, 11.0, ['sales_clean["invoice_date"] = pd.to_datetime(sales_clean["invoice_date"])',
                                                 "sales_clean.shape"], output=["(101458, 10)"], size=15)
    k.box(d, s, centred(6.4), 5.75, 6.4, "A wrong shape: stop and fix it first.", size=17)


def piles(d):
    s, y = k.slide(d, "groupby sorts receipts into piles",
                   "groupby seperti memilah struk ke beberapa tumpukan, satu tumpukan per produk, lalu menjumlahkan "
                   "setiap tumpukan. Di Excel, ini PivotTable. Baris dengan kode yang sama masuk ke tumpukan yang sama. "
                   "Hasilnya satu baris per produk.", seconds=60)
    rows = [("85123A", "15.30"), ("71053", "20.34"), ("85123A", "15.30"), ("71053", "20.34")]   # first clean rows
    for i, (code, rev) in enumerate(rows):
        hot = code == "85123A"
        k.chip(d, s, 1.0, 1.85 + i * 0.62, 2.0, 0.5, code, PEACH if hot else WHITE, NAVY, size=16, mono=True,
               line=SAND, name=f"c{i}")
        k.chip(d, s, 3.1, 1.85 + i * 0.62, 1.6, 0.5, rev, WHITE, NAVY, size=16, mono=True, line=SAND, name=f"r{i}")
    k.arrow(d, s, 5.1, 3.0, 1.2, 0.45, fill=ORANGE)
    k.label(d, s, 4.9, 3.5, 1.6, 0.35, "groupby", size=15, bold=True, color=ORANGE_TEXT, mono=True)
    for i, (code, total, n) in enumerate([("85123A", "30.60", "2 rows"), ("71053", "40.68", "2 rows")]):
        ry = 2.2 + i * 1.3
        k.chip(d, s, 6.8, ry, 2.2, 0.9, code, PEACH if i == 0 else SAND, NAVY, size=20, mono=True, bold=True,
               name=f"p{i}")
        k.chip(d, s, 9.1, ry, 1.8, 0.9, total, NAVY, WHITE, size=20, mono=True, bold=True, name=f"t{i}")
        k.label(d, s, 11.0, ry, 1.7, 0.9, n, size=16, color=MUTED, align="left", name=f"n{i}")
    muted(d, s, 5.55, "Like a PivotTable: rows = stock_code, values = sum of revenue")


def anatomy(d):
    s, y = k.slide(d, "Read a groupby from left to right",
                   "Baca groupby dari kiri ke kanan. Tabelnya, lalu kelompokkan per stock_code, lalu ambil kolom revenue, "
                   "lalu jumlahkan. Empat bagian, satu baris. Kalau ganti sum dengan mean atau count, kamu dapat "
                   "rata-rata atau jumlah baris per produk.", seconds=55)
    parts = [("sales_clean", "the table"), ('.groupby("stock_code")', "the piles"), ('["revenue"]', "the column"),
             (".sum()", "add each pile")]
    ws = [2.5, 4.3, 2.3, 1.4]
    x = centred(sum(ws) + 0.1 * 3)
    for i, ((p, lab), w) in enumerate(zip(parts, ws)):
        k.chip(d, s, x, 2.0, w, 0.75, p, ORANGE if i == 1 else NAVY, WHITE if i == 1 else CODE_INK, size=17,
               mono=True, name=f"p{i}")
        k.label(d, s, x, 2.85, w, 0.35, lab, size=15, color=MUTED, name=f"pl{i}")
        x += w + 0.1
    xs, w = cols(3, gap=0.3, w=9.0, x=centred(9.0))
    for x, (code, mean) in zip(xs, [(".sum()", "total"), (".mean()", "average"), (".count()", "how many rows")]):
        k.tile(d, s, x, 3.9, w, 1.2, code, mean, mono=True, head_size=20, name="agg")


def reset(d):
    s, y = k.slide(d, "reset_index makes a normal table",
                   "Hasil groupby punya label baris, yaitu stock_code, bukan kolom biasa. Itu Series. reset_index "
                   "mengubahnya kembali menjadi tabel biasa dengan dua kolom. Setelah itu kamu bisa menambah kolom baru. "
                   "Kalau lupa, product_value revenue memberi KeyError.", seconds=55)
    k.label(d, s, 1.4, 1.75, 4.0, 0.4, "Series", size=18, bold=True, color=MUTED)
    for i, (c, r) in enumerate([("22423", "51504.85"), ("85123A", "30780.98"), ("79321", "17013.92")]):
        ry = 2.25 + i * 0.6
        k.chip(d, s, 1.4, ry, 1.7, 0.5, c, SKY, NAVY, size=16, mono=True, bold=True, name=f"si{i}")
        k.chip(d, s, 3.2, ry, 2.2, 0.5, r, WHITE, NAVY, size=16, mono=True, line=SAND, name=f"sv{i}")
    k.arrow(d, s, 5.8, 2.75, 1.4, 0.45, fill=ORANGE)
    k.label(d, s, 5.6, 3.25, 1.8, 0.35, "reset_index()", size=14, bold=True, color=ORANGE_TEXT, mono=True)
    k.label(d, s, 7.6, 1.75, 4.6, 0.4, "a normal table", size=18, bold=True, color=ORANGE_TEXT)
    k.chip(d, s, 7.6, 2.25, 2.2, 0.5, "stock_code", NAVY, WHITE, size=15, mono=True, name="h0")
    k.chip(d, s, 9.9, 2.25, 2.2, 0.5, "revenue", NAVY, WHITE, size=15, mono=True, name="h1")
    for i, (c, r) in enumerate([("22423", "51504.85"), ("85123A", "30780.98"), ("79321", "17013.92")]):
        ry = 2.85 + i * 0.6
        k.chip(d, s, 7.6, ry, 2.2, 0.5, c, WHITE, NAVY, size=16, mono=True, line=SAND, name=f"ti{i}")
        k.chip(d, s, 9.9, ry, 2.2, 0.5, r, WHITE, NAVY, size=16, mono=True, line=SAND, name=f"tv{i}")
    k.code_card(d, s, centred(8.0), 4.95, 8.0, ["product_value = revenue_by_product.reset_index()"], size=17)


def running(d):
    s, y = k.slide(d, "cumsum is a running total",
                   "cumsum adalah total berjalan, seperti gulungan struk kasir yang terus menambah. Di Excel, SUM dengan "
                   "dolar di awal, ditarik ke bawah. Setiap baris berisi jumlah semua baris sampai di situ. Syaratnya: "
                   "urutkan dulu dari terbesar. Kalau tidak diurutkan, total berjalannya tidak berarti apa-apa.",
                   seconds=60)
    vals = [("51504.85", "51504.85"), ("30780.98", "82285.83"), ("17013.92", "99299.75")]
    x0 = centred(3.0 + 1.5 + 3.4)
    k.label(d, s, x0, 1.75, 3.0, 0.4, "revenue", size=17, bold=True, mono=True)
    k.label(d, s, x0 + 4.5, 1.75, 3.4, 0.4, "running total", size=17, bold=True, mono=True, color=ORANGE_TEXT)
    for i, (v, c) in enumerate(vals):
        ry = 2.25 + i * 0.7
        k.chip(d, s, x0, ry, 3.0, 0.56, v, WHITE, NAVY, size=18, mono=True, line=SAND, name=f"v{i}")
        k.arrow(d, s, x0 + 3.3, ry + 0.15, 0.9, 0.26)
        k.chip(d, s, x0 + 4.5, ry, 3.4, 0.56, c, PEACH if i == 2 else SAND, NAVY, size=18, mono=True, name=f"c{i}")
    k.box(d, s, centred(6.4), 4.6, 6.4, "Sort first, then cumsum.", size=19)
    muted(d, s, 5.55, "Like =SUM($B$2:B2) dragged down")


def share(d):
    s, y = k.slide(d, "Cumulative share: how far we are",
                   "Total berjalan dibagi total semua revenue memberi cumulative share: berapa bagian dari seluruh uang "
                   "yang sudah tercapai sampai produk ini. Produk teratas saja sudah 2,7 persen. Sepuluh produk "
                   "teratas, 9,6 persen. Di produk ke-671, kita sampai 80 persen. Apa artinya untuk gudang?",
                   seconds=65)
    marks = [(1, "2.7%"), (10, "9.6%"), (100, "36.0%"), (671, "80.0%"), (3066, "100%")]
    lx0, lx1, ly = 1.2, 12.1, 3.4
    d.line(s, lx0, ly, lx1, ly, color=MUTED, width=2)
    for i, (rank, pct) in enumerate(marks):
        x = lx0 + (lx1 - lx0) * i / 4
        hot = rank == 671
        d.oval(s, x - 0.16, ly - 0.16, 0.32, ORANGE if hot else NAVY)
        k.label(d, s, x - 1.0, ly - 1.05, 2.0, 0.6, pct, size=28 if hot else 22, bold=True,
                color=ORANGE_TEXT if hot else NAVY, name=f"p{i}")
        k.label(d, s, x - 1.0, ly + 0.3, 2.0, 0.4, f"product {rank:,}", size=16, color=MUTED, name=f"r{i}")
    k.code_card(d, s, centred(11.4), 4.6, 11.4,
                ['product_value["cumulative_share"] = product_value["revenue"].cumsum() / total_revenue'], size=15)


def abc(d):
    s, y = k.slide(d, "ABC: three classes of product",
                   "Analisis ABC membagi produk menjadi tiga kelas. A: produk yang membawa 80 persen pertama revenue. B: "
                   "15 persen berikutnya, sampai 95. C: sisanya. Angka 80 dan 95 adalah kebiasaan di dunia inventory, "
                   "bukan hukum. Datamu sendiri yang menentukan seberapa curam kurvanya.", seconds=60)
    cards = [("A", "up to 80%", "watch closely"), ("B", "80% to 95%", "check often"), ("C", "the rest", "keep simple")]
    xs, w = cols(3)
    for i, (cls, rng, act) in enumerate(cards):
        d.rect(s, xs[i], 1.8, w, 3.0, NAVY if i == 0 else SAND, name=f"k{i}")
        k.label(d, s, xs[i], 1.95, w, 1.1, cls, size=66, bold=True, color=ORANGE if i == 0 else ORANGE_TEXT)
        k.label(d, s, xs[i], 3.15, w, 0.45, rng, size=20, bold=True, color=WHITE if i == 0 else NAVY)
        k.label(d, s, xs[i], 3.75, w, 0.45, act, size=17, color="C9D3DE" if i == 0 else MUTED)
    muted(d, s, 5.4, "80 and 95 are a habit, not a law.")


def apply_rule(d):
    s, y = k.slide(d, "apply runs your rule on every row",
                   "Aturan ABC kita tulis sebagai function, persis seperti order_size di sesi tiga. Lalu apply "
                   "menjalankan function itu di setiap baris kolom, seperti menarik rumus ke bawah di Excel. Tanpa loop. "
                   "Kita pakai function bernama, bukan lambda, supaya aturannya mudah dibaca. Jadi ini aturan yang sama dengan sesi tiga, dan kamu sudah bisa menulisnya.", seconds=60)
    k.code_card(d, s, M + 0.3, 1.8, 5.8, ["def abc_class(share):", "    if share <= 0.80:", '        return "A"',
                                          "    elif share <= 0.95:", '        return "B"', "    else:",
                                          '        return "C"'], size=16)
    rows = [("0.03", "A"), ("0.90", "B"), ("0.99", "C")]
    k.label(d, s, 7.3, 1.75, 5.4, 0.4, ".apply(abc_class)", size=18, bold=True, mono=True, color=ORANGE_TEXT)
    for i, (sh, cls) in enumerate(rows):
        ry = 2.35 + i * 0.85
        k.chip(d, s, 7.6, ry, 2.0, 0.65, sh, WHITE, NAVY, size=18, mono=True, line=SAND, name=f"s{i}")
        k.arrow(d, s, 9.8, ry + 0.18, 0.8, 0.3, fill=ORANGE)
        k.chip(d, s, 10.8, ry, 1.6, 0.65, cls, ORANGE if i == 0 else NAVY, WHITE, size=20, bold=True, name=f"c{i}")
    muted(d, s, 5.6, "Your Session 3 rule, on every row")


def count_true(d):
    s, y = k.slide(d, "Count with True and sum",
                   "Untuk menghitung produk kelas A, tanyakan setiap baris: apakah kelasnya A? Hasilnya kolom True dan "
                   "False. Lalu sum, karena True bernilai satu. Ini trik yang sama dengan isna sum di sesi empat. "
                   "Jawabannya 671 produk.", seconds=55)
    vals = ["A", "A", "B", "C", "A"]
    x0 = 1.6
    for i, v in enumerate(vals):
        a = v == "A"
        k.chip(d, s, x0, 1.85 + i * 0.6, 1.4, 0.5, v, WHITE, NAVY, size=17, mono=True, line=SAND, name=f"v{i}")
        k.chip(d, s, x0 + 2.9, 1.85 + i * 0.6, 1.6, 0.5, str(a), ORANGE if a else SAND, WHITE if a else NAVY,
               size=16, mono=True, name=f"b{i}")
    k.label(d, s, x0 + 1.4, 2.55, 1.5, 0.35, '== "A"', size=15, bold=True, mono=True, color=ORANGE_TEXT)
    k.arrow(d, s, x0 + 1.6, 2.95, 1.1, 0.32)
    k.label(d, s, x0 + 4.55, 2.55, 1.2, 0.35, ".sum()", size=15, bold=True, mono=True, color=ORANGE_TEXT)
    k.arrow(d, s, x0 + 4.65, 2.95, 1.0, 0.32)
    k.stop(d, s, x0 + 5.85, 2.6, 1.0, "3", NAVY, WHITE, size=32)
    k.big_number(d, s, 9.0, 2.2, 3.7, "671", "class A products", size=60)


def finding(d):
    s, y = k.slide(d, "About 1 in 5 products bring 80% of the money",
                   "Ini temuannya. 671 dari 3.066 produk, sekitar satu dari lima, membawa 80 persen revenue. Lihat "
                   "grafiknya: kelas C punya lebih dari separuh produk, tapi hanya lima persen uang. Untuk manajer: "
                   "jaga stok kelas A, dan pertanyakan apakah semua produk C perlu disimpan. Bagaimana kamu "
                   "mengatakannya dalam satu kalimat?", seconds=80)
    k.big_number(d, s, M, 2.1, 4.2, "21.9%", "of products", size=54)
    k.big_number(d, s, M, 3.85, 4.2, "80.0%", "of revenue", color=NAVY, size=54)
    chart = d.bar_chart(s, 5.2, 1.6, 7.53, 4.7, ["Class A", "Class B", "Class C"],
                        {"Share of products (%)": [c[2] for c in ABC], "Share of revenue (%)": [c[3] for c in ABC]},
                        colors=[SKY, ORANGE], legend=True, number_format="0.0", gap=60)
    chart.value_axis.visible = False
    chart.value_axis.has_major_gridlines = False


def country(d):
    s, y = k.slide(d, "Same groupby, another pile",
                   "Ide groupby yang sama bisa dipakai untuk pertanyaan lain: cukup ganti kolom tumpukannya. Per negara, "
                   "Inggris jauh di atas, 84,8 persen revenue. Jadi hati-hati: grafik negara kita tidak menggambarkan "
                   "pasar global. Pertanyaan apa lagi yang bisa dijawab dengan groupby?", seconds=55)
    k.code_card(d, s, M, 1.85, 5.6, ['groups = sales_clean.groupby("country")', 'groups["revenue"].sum()'], size=14)
    k.label(d, s, M, 3.3, 5.6, 0.4, "UK is 84.8% of revenue", size=20, bold=True, color=ORANGE_TEXT, align="left")
    k.label(d, s, M, 3.8, 5.6, 0.4, "Country charts are not global.", size=17, color=MUTED, align="left")
    chart = d.bar_chart(s, 6.6, 1.65, 6.13, 4.6, ["United Kingdom", "Netherlands", "EIRE", "Germany", "France"],
                        {"Revenue": [1591694.50, 58182.55, 43426.19, 37365.63, 32392.39]}, colors=[NAVY],
                        horizontal=True, legend=False, number_format="#,##0", point_colors={0: ORANGE}, gap=45)
    chart.value_axis.visible = False
    chart.value_axis.has_major_gridlines = False


def cold_test(d):
    s, y = k.slide(d, "Cold test: 20 minutes",
                   "Blok kedua adalah cold test. Dua puluh menit, catatan dan notebook boleh dipakai, dan saya diam. "
                   "Ada empat poin: kodenya jalan, angkanya benar, namanya jelas, dan satu kalimat menjelaskan artinya. "
                   "Tidak ada yang perlu dihafal; yang dinilai cara kamu berpikir.", seconds=50)
    items = [("It runs", "top to bottom"), ("Right numbers", "within 0.01"), ("Clear names", "says what it holds"),
             ("One sentence", "what it means")]
    xs, w = cols(4)
    for i, (head, sub) in enumerate(items):
        k.tile(d, s, xs[i], 1.9, w, 2.0, head, sub, head_size=22, name=f"t{i}")
        k.stop(d, s, xs[i] + w / 2 - 0.3, 1.6, 0.6, "1", ORANGE, WHITE, size=18)
    k.box(d, s, centred(7.4), 4.6, 7.4, "Notes allowed. The teacher stays silent.", size=18)


def toolkit(d):
    s, y = k.slide(d, "Your analysis toolkit",
                   "Ini ringkasan alat hari ini. groupby dan apply akan kamu pakai lagi di proyek. Mana yang paling "
                   "sulit diingat?", seconds=35)
    rows = [["Code", "Does"], ['df.groupby("col")["revenue"].sum()', "total per group"],
            [".sort_values(ascending=False)", "biggest first"], [".reset_index()", "back to a normal table"],
            [".cumsum()", "running total"], [".apply(abc_class)", "your rule on every row"],
            ['(df["abc_class"] == "A").sum()', "count the True rows"], [".to_csv(path, index=False)", "save for later"]]
    k.ltable(d, s, centred(10.6), 1.7, 10.6, rows, [5.8, 4.8], code_cols=(0,), size=16, row_h=0.52)


def now_colab(d):
    s, y = k.slide(d, "Now in Colab",
                   "Sekarang kita pindah ke notebook s5_star_products. Tangganya: dua tebakan, dua isian, satu bug, tiga "
                   "kode yang kamu tulis sendiri, lalu cold test. Simpan product_value.csv untuk Power BI di sesi tujuh. "
                   "Siap?", seconds=30)
    k.ladder(d, s, M, 1.85, 8.0, 3.6, [("Predict", 2), ("Fill in", 2), ("Fix it", 1), ("Write it", 3),
                                       ("Cold test", 1)])
    d.text(s, 9.3, 1.9, 3.43, 4.2,
           [{"text": "Notebook", "bold": True, "color": ORANGE_TEXT, "size": 16},
            {"text": "s5_star_products", "after": 14},
            {"text": "Save", "bold": True, "color": ORANGE_TEXT, "size": 16},
            {"text": "product_value.csv", "after": 14},
            {"text": "Recall", "bold": True, "color": ORANGE_TEXT, "size": 16},
            {"text": "Tue 1, Wed 2 Dec"}],
           size=20, color=NAVY, name="side")


def thanks(d):
    k.thanks_next(d, "Terima kasih untuk hari ini. Kamu sudah menemukan produk bintang dan menyelesaikan cold test "
                     "pertamamu. Titik lima selesai. Berikutnya titik enam: membuat angka berbicara lewat grafik, supaya "
                     "manajer paham dalam lima detik. Jangan lupa recall Selasa dan Rabu.")


def build():
    d = k.lecture_deck(5)
    for make in (cover, goals, load, piles, anatomy, reset, running, share, abc, apply_rule, count_true, finding,
                 country, cold_test, toolkit, now_colab, thanks):
        make(d)
    k.save(d, OUT)


if __name__ == "__main__":
    build()
