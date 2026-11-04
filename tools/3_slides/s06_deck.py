"""Build the S6 deck: Make the numbers talk.

Theory slides that the teacher talks over: a title, one visual anchor, and at most one short line.
The speaker notes carry the explanation; the notebook is the playground.
"""
from pathlib import Path

import deckkit as k
from deckkit import (M, CW, NAVY, ORANGE, ORANGE_TEXT, SAND, SKY, PEACH, CREAM, MUTED, CODE_INK, WHITE, cols,
                     centred, muted)

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "sessions" / "s06_numbers_talk" / "deck.pptx"

# From the S6 notebook run on the clean table
TOP10 = [("REGENCY CAKESTAND 3 TIER", 51504.85), ("WHITE HANGING HEART T-LIGHT HOLDER", 30780.98),
         ("CHILLI LIGHTS", 17013.92), ("JUMBO BAG RED RETROSPOT", 14684.04),
         ("VINTAGE UNION JACK MEMOBOARD", 14050.55), ("WOOD BLACK BOARD ANT WHITE FINISH", 11013.87),
         ("HEART OF WICKER LARGE", 10999.97), ("HEART OF WICKER SMALL", 10815.52),
         ("SET OF 3 CAKE TINS PANTRY DESIGN", 10050.01), ("RED WOOLLY HOTTIE WHITE HEART.", 9652.62)]
DAYS = ['1 Dec', '2 Dec', '3 Dec', '5 Dec', '6 Dec', '7 Dec', '8 Dec', '9 Dec', '10 Dec', '12 Dec', '13 Dec',
        '14 Dec', '15 Dec', '16 Dec', '17 Dec', '19 Dec', '20 Dec', '21 Dec', '22 Dec', '23 Dec', '4 Jan', '5 Jan',
        '6 Jan', '7 Jan', '9 Jan', '10 Jan', '11 Jan', '12 Jan', '13 Jan', '14 Jan', '16 Jan', '17 Jan', '18 Jan',
        '19 Jan', '20 Jan', '21 Jan', '23 Jan', '24 Jan', '25 Jan', '26 Jan', '27 Jan', '28 Jan', '30 Jan', '31 Jan',
        '1 Feb', '2 Feb', '3 Feb', '4 Feb', '6 Feb', '7 Feb', '8 Feb', '9 Feb', '10 Feb', '11 Feb', '13 Feb',
        '14 Feb', '15 Feb', '16 Feb', '17 Feb', '18 Feb', '20 Feb', '21 Feb', '22 Feb', '23 Feb', '24 Feb', '25 Feb',
        '27 Feb', '28 Feb']
DAILY = [57442, 47596, 44789, 30909, 51667, 81455, 44154, 49976, 56686, 17126, 36575, 44327, 30368, 48868, 41188,
         7288, 25449, 43631, 4857, 11222, 15325, 31919, 39968, 27662, 15401, 23305, 67857, 23419, 19582, 46155, 6974,
         27747, 17181, 25090, 20387, 31544, 10198, 24297, 28107, 19141, 23280, 19619, 6543, 22479, 28509, 20156,
         22929, 23836, 3440, 25508, 19900, 15521, 14590, 22392, 5645, 26202, 39534, 24588, 24718, 15827, 9434,
         35264, 32131, 25775, 22571, 20129, 9365, 19817]


def cover(d):
    k.cover_for(d, "merge, bar charts, line charts, finding titles",
                "Halo, selamat datang di sesi enam. Lima titik sudah lewat, lebih dari separuh jalan. Kemarin kita "
                "menemukan produk bintang. Hari ini pertanyaannya: bagaimana menunjukkannya supaya manajer paham dalam "
                "lima detik? Siap?")


def goals(d):
    s, y = k.slide(d, "Today",
                   "Ini empat bagian hari ini. Satu, merge: VLOOKUP dalam kode, dan pelajaran menghitung baris. Dua, "
                   "bar chart. Tiga, line chart. Empat, judul yang menyatakan temuan. Di akhir, tugas case hunt.",
                   seconds=35)
    items = [("Merge", "count rows before, after"), ("Bar chart", "plt.barh"), ("Line chart", "plt.plot"),
             ("Finding titles", "say what to see")]
    xs, w = cols(4)
    for i, (head, sub) in enumerate(items):
        d.rect(s, xs[i], 2.0, w, 2.6, SAND, name=f"g{i}")
        k.stop(d, s, xs[i] + w / 2 - 0.35, 2.3, 0.7, str(i + 1), ORANGE if i == 0 else NAVY, WHITE, size=22)
        k.label(d, s, xs[i], 3.2, w, 0.5, head, size=22, bold=True, name=f"gh{i}")
        k.label(d, s, xs[i] + 0.1, 3.75, w - 0.2, 0.4, sub, size=15, color=MUTED, mono=True, name=f"gs{i}")


def lookup(d):
    s, y = k.slide(d, "merge is your VLOOKUP",
                   "Tabel produk kita hanya punya kode, tanpa nama. Nama ada di tabel penjualan. merge mencocokkan dua "
                   "tabel lewat kolom yang sama, namanya key, di sini stock_code. Seperti mencocokkan daftar barang dengan "
                   "katalog, atau VLOOKUP di Excel. how left artinya semua baris tabel kiri tetap ada.", seconds=60)
    x0 = centred(3.6 * 3 + 1.2 * 2)
    k.label(d, s, x0, 1.7, 3.6, 0.35, "product_value", size=16, bold=True, mono=True)
    k.label(d, s, x0 + 4.8, 1.7, 3.6, 0.35, "product_names", size=16, bold=True, mono=True)
    k.label(d, s, x0 + 9.6, 1.7, 3.6, 0.35, "after merge", size=16, bold=True, color=ORANGE_TEXT)
    rows = [("22423", "51504.85", "REGENCY CAKESTAND..."), ("85123A", "30780.98", "WHITE HANGING HEART...")]
    for i, (c, r, n) in enumerate(rows):
        ry = 2.15 + i * 0.62
        k.chip(d, s, x0, ry, 1.6, 0.52, c, ORANGE, WHITE, size=15, mono=True, name=f"a{i}")
        k.chip(d, s, x0 + 1.65, ry, 1.95, 0.52, r, WHITE, NAVY, size=15, mono=True, line=SAND, name=f"b{i}")
        k.chip(d, s, x0 + 4.8, ry, 1.6, 0.52, c, ORANGE, WHITE, size=15, mono=True, name=f"c{i}")
        k.chip(d, s, x0 + 6.45, ry, 1.95, 0.52, n.split()[0], WHITE, NAVY, size=15, mono=True, line=SAND,
               name=f"d{i}")
        k.chip(d, s, x0 + 9.6, ry, 3.6, 0.52, n, PEACH, NAVY, size=14, mono=True, name=f"e{i}")
    k.arrow(d, s, x0 + 3.75, 2.5, 0.9, 0.32)
    k.arrow(d, s, x0 + 8.55, 2.5, 0.9, 0.32, fill=ORANGE)
    k.code_card(d, s, centred(11.0), 3.9, 11.0,
                ['product_value = product_value.merge(product_names, on="stock_code", how="left")'], size=15)
    muted(d, s, 5.2, "on = the key both tables share")


def count_rows(d):
    s, y = k.slide(d, "Count rows before and after",
                   "Aturan emas merge: hitung baris sebelum dan sesudah. Tabel produk punya 3.066 baris. Setelah merge "
                   "pertama, jadi 3.107. Tidak ada error, tapi 41 baris muncul entah dari mana. Kalau kita jumlahkan "
                   "revenue sekarang, angkanya terlalu besar. Dari mana baris tambahan itu?", seconds=60)
    x0 = centred(3.8 * 2 + 2.0)
    k.big_number(d, s, x0, 2.0, 3.8, "3,066", "rows before", color=NAVY, size=60)
    k.arrow(d, s, x0 + 4.0, 2.45, 1.6, 0.5, fill=ORANGE)
    k.label(d, s, x0 + 3.8, 3.05, 2.0, 0.35, "merge", size=16, bold=True, color=ORANGE_TEXT, mono=True)
    k.big_number(d, s, x0 + 5.8, 2.0, 3.8, "3,107", "rows after", size=60)
    k.box(d, s, centred(7.4), 4.6, 7.4, "41 extra rows and no error message.", size=19)


def why_grows(d):
    s, y = k.slide(d, "A repeated key makes the table grow",
                   "Ini sebabnya. 40 kode produk punya dua nama di data, misalnya ejaan yang sedikit berbeda. Kalau tabel "
                   "nama punya dua baris untuk satu kode, satu baris produk dicocokkan dengan dua nama, dan menjadi dua "
                   "baris. Revenue-nya ikut tercatat dua kali. Bagaimana cara memperbaikinya?", seconds=65)
    x0 = centred(2.8 + 1.0 + 4.0 + 1.0 + 2.8)
    k.chip(d, s, x0, 2.45, 2.8, 0.7, "1 product row", NAVY, WHITE, size=18, bold=True, name="one")
    k.arrow(d, s, x0 + 3.0, 2.65, 0.6, 0.32)
    k.chip(d, s, x0 + 3.8, 1.95, 4.0, 0.62, "same code, name 1", SAND, NAVY, size=17, name="n1")
    k.chip(d, s, x0 + 3.8, 2.95, 4.0, 0.62, "same code, name 2", PEACH, NAVY, size=17, name="n2")
    k.arrow(d, s, x0 + 8.0, 2.65, 0.6, 0.32, fill=ORANGE)
    k.chip(d, s, x0 + 8.8, 2.45, 2.8, 0.7, "2 rows", ORANGE, WHITE, size=18, bold=True, name="two")
    k.label(d, s, M, 4.0, CW, 0.4, "40 codes have two names  →  41 extra rows", size=18, bold=True,
            color=ORANGE_TEXT)


def fix(d):
    s, y = k.slide(d, "Keep one name per code",
                   "Perbaikannya: buat tabel nama dengan satu nama untuk setiap kode. drop_duplicates dengan subset "
                   "stock_code menyimpan baris pertama untuk setiap kode. Lalu merge lagi, dan hitung lagi. 3.066 sebelum, "
                   "3.066 sesudah. Sekarang aman.", seconds=55)
    k.code_card(d, s, centred(11.4), 1.85, 11.4,
                ['product_names = sales_clean[["stock_code", "description"]]',
                 'product_names = product_names.drop_duplicates(subset="stock_code")'], size=16)
    x0 = centred(3.4 * 2 + 1.6)
    k.tile(d, s, x0, 3.55, 3.4, 1.4, "3,066", "before", head_size=34, name="a")
    k.label(d, s, x0 + 3.4, 3.55, 1.6, 1.4, "=", size=40, bold=True, color=ORANGE_TEXT)
    k.tile(d, s, x0 + 5.0, 3.55, 3.4, 1.4, "3,066", "after", head_size=34, fill=NAVY, head_color=WHITE,
           sub_color="C9D3DE", name="b")
    muted(d, s, 5.4, "Same number: the merge is safe.")


def recipe(d):
    s, y = k.slide(d, "A chart, step by step",
                   "matplotlib menggambar grafik langkah demi langkah, seperti Insert Chart lalu mengedit setiap bagian. "
                   "Enam langkah: buat kanvas, gambar batangnya, beri judul, beri label sumbu, rapikan, lalu tampilkan. "
                   "Urutannya selalu sama, jadi mudah diingat. Ini resep yang kita pakai untuk setiap grafik, dan kamu yang mengetiknya.", seconds=55)
    steps = [("plt.figure()", "a canvas"), ("plt.barh()", "the bars"), ("plt.title()", "the finding"),
             ("plt.xlabel()", "the units"), ("plt.tight_layout()", "tidy"), ("plt.show()", "show it")]
    xs, w = cols(3)
    for i, (code, mean) in enumerate(steps):
        x, ty = xs[i % 3], 1.8 + (i // 3) * 1.85
        hot = i == 2
        d.rect(s, x, ty, w, 1.6, PEACH if hot else SAND, line=ORANGE if hot else None, name=f"r{i}")
        k.stop(d, s, x + 0.3, ty + 0.5, 0.6, str(i + 1), ORANGE if hot else NAVY, WHITE, size=18)
        k.label(d, s, x + 1.1, ty + 0.3, w - 1.3, 0.5, code, size=16, mono=True, bold=True, align="left",
                name=f"c{i}")
        k.label(d, s, x + 1.1, ty + 0.85, w - 1.3, 0.4, mean, size=16, color=MUTED, align="left", name=f"m{i}")
    muted(d, s, 5.65, "Every chart needs a title and axis labels.")


def titles(d):
    s, y = k.slide(d, "The title says the finding",
                   "Judul grafik bukan nama grafiknya. Bar chart of revenue tidak memberitahu apa-apa. Judul yang baik "
                   "menyatakan temuannya, jadi manajer tahu apa yang harus dilihat dalam lima detik. Coba: judul apa "
                   "untuk grafik penjualan harian?", seconds=60)
    xs, w = cols(2, gap=0.5, w=11.0, x=centred(11.0))
    k.chip(d, s, xs[0], 1.9, w, 2.2, "Bar chart of revenue", SAND, NAVY, size=22, bold=True, name="bad")
    k.chip(d, s, xs[1], 1.9, w, 2.2, "The top 10 products are only 9.6% of revenue", WHITE, NAVY, size=22,
           bold=True, line=ORANGE, name="good")
    k.label(d, s, xs[0], 4.25, w, 0.4, "no", size=20, bold=True, color=MUTED)
    k.label(d, s, xs[1], 4.25, w, 0.4, "yes", size=20, bold=True, color=ORANGE_TEXT)
    muted(d, s, 5.3, "A manager gets it in five seconds.")


def bar(d):
    s, y = k.slide(d, "The top 10 products are only 9.6% of revenue",
                   "Ini bar chart dari notebook. Batang horizontal, karena nama produk panjang. Diurutkan supaya yang "
                   "terbesar di atas. REGENCY CAKESTAND jauh di depan. Tapi lihat judulnya: sepuluh produk teratas hanya "
                   "9,6 persen revenue. Artinya uangnya tersebar di banyak produk. Apa kesimpulanmu untuk gudang?",
                   seconds=65)
    names = [n.title() for n, _ in TOP10]
    chart = d.bar_chart(s, M, 1.55, CW, 4.9, names, {"Revenue": [v for _, v in TOP10]}, colors=[NAVY],
                        horizontal=True, legend=False, number_format="#,##0", point_colors={0: ORANGE}, gap=40)
    chart.category_axis.reverse_order = True
    chart.value_axis.visible = False
    chart.value_axis.has_major_gridlines = False


def line(d):
    s, y = k.slide(d, "Revenue peaked in the first week of December",
                   "Ini line chart revenue per hari, 68 hari dagang. Line chart menunjukkan perubahan dari waktu ke waktu. "
                   "Puncaknya 7 Desember, 81.455 pounds, sebelum Natal. Setelah Natal turun, lalu lebih tenang di Januari "
                   "dan Februari. Hari di mana kamu melihat celah, dan kenapa?", seconds=65)
    chart = d.line_chart(s, M, 1.55, CW, 4.9, DAYS, {"Revenue": DAILY}, colors=[NAVY], legend=False,
                         number_format="#,##0", label_every=10)
    chart.value_axis.has_major_gridlines = False
    k.chip(d, s, 2.6, 1.6, 3.2, 0.5, "7 Dec: £81,455", ORANGE, WHITE, size=16, bold=True, name="peak")


def mistakes(d):
    s, y = k.slide(d, "Three chart mistakes",
                   "Tiga kesalahan grafik yang paling sering. Tidak ada judul atau label sumbu: pembaca menebak. Label "
                   "panjang bertumpuk: pakai barh atau putar labelnya. Terlalu banyak pesan dalam satu grafik: satu "
                   "grafik, satu pesan. Di notebook, kamu memperbaiki satu grafik yang rusak.", seconds=55)
    items = [("No title, no labels", "the reader guesses", "plt.title()  plt.xlabel()"),
             ("Labels on top of each other", "names too long", "plt.barh()  rotation=45"),
             ("Too many messages", "the eye gets lost", "one chart, one message")]
    xs, w = cols(3)
    for i, (head, mean, fixit) in enumerate(items):
        d.rect(s, xs[i], 1.8, w, 3.3, SAND, name=f"e{i}")
        k.label(d, s, xs[i] + 0.2, 2.0, w - 0.4, 0.9, head, size=21, bold=True, color=ORANGE_TEXT)
        k.label(d, s, xs[i] + 0.2, 2.95, w - 0.4, 0.5, mean, size=17)
        k.chip(d, s, xs[i] + 0.3, 4.05, w - 0.6, 0.6, fixit, NAVY, CODE_INK, size=14, mono=True, name=f"x{i}")


def seaborn(d):
    s, y = k.slide(d, "seaborn: a chart template",
                   "seaborn adalah template grafik di atas matplotlib. Satu baris memberi grafik yang rapi, dan judul "
                   "serta label tetap ditulis dengan plt seperti biasa. Karena Inggris 85 persen revenue, grafik negara "
                   "di PR kita tidak menyertakan Inggris, dan judulnya menyebutkan itu. Ini PR, bukan latihan kelas.",
                   seconds=55)
    k.code_card(d, s, centred(10.0), 1.85, 10.0,
                ["import seaborn as sns", "", 'sns.barplot(data=top_countries, x="revenue", y="country")',
                 'plt.title("Outside the UK, the Netherlands and Ireland lead")', 'plt.xlabel("Revenue (pounds)")',
                 "plt.show()"], size=16)
    muted(d, s, 5.0, "Same titles and labels, nicer defaults")


def case_hunt(d):
    s, y = k.slide(d, "Case hunt: due Session 8",
                   "Tugas case hunt. Cari satu kasus supply chain yang nyata: dari berita, laporan perusahaan, atau "
                   "kasus kuliah. Jawab lima poin dalam satu halaman, pakai template di course home. Kamu presentasikan "
                   "dua menit di sesi delapan. Tidak ada jawaban benar atau salah.", seconds=50)
    items = ["The problem", "Who is affected", "What data would show it", "One question for data",
             "Python, SQL or a dashboard?"]
    xs, w = cols(5, gap=0.2)
    for i, t in enumerate(items):
        d.rect(s, xs[i], 1.9, w, 2.4, SAND, name=f"c{i}")
        k.stop(d, s, xs[i] + w / 2 - 0.3, 2.15, 0.6, str(i + 1), ORANGE if i == 3 else NAVY, WHITE, size=18)
        k.label(d, s, xs[i] + 0.15, 3.0, w - 0.3, 1.0, t, size=17, bold=True, anchor="top", name=f"t{i}")
    muted(d, s, 4.9, "One page. Two minutes in Session 8.")


def toolkit(d):
    s, y = k.slide(d, "Your chart toolkit",
                   "Ini ringkasan alat hari ini. Grafik ini yang nanti masuk ke slide proyekmu. Mana yang paling sulit "
                   "diingat?", seconds=35)
    rows = [["Code", "Does"], ['a.merge(b, on="key", how="left")', "VLOOKUP: add columns"],
            ["len(a) before and after", "check the merge"], ['.drop_duplicates(subset="key")', "one row per key"],
            ["plt.barh(names, values)", "a bar chart"], ["plt.plot(days, values)", "a line chart"],
            ["plt.title()  plt.xlabel()", "the finding, the units"], [".dt.date", "the day from a date"]]
    k.ltable(d, s, centred(10.6), 1.7, 10.6, rows, [5.6, 5.0], code_cols=(0,), size=16, row_h=0.52)


def now_colab(d):
    s, y = k.slide(d, "Now in Colab",
                   "Sekarang kita pindah ke notebook s6_numbers_talk. Tangganya: dua tebakan, dua isian, dua grafik yang "
                   "harus diperbaiki, dua kode yang kamu tulis sendiri, dan satu kasus. Siap?", seconds=30)
    k.ladder(d, s, M, 1.85, 8.0, 3.6, [("Predict", 2), ("Fill in", 2), ("Fix it", 2), ("Write it", 2), ("Case", 1)])
    d.text(s, 9.3, 1.9, 3.43, 4.2,
           [{"text": "Notebook", "bold": True, "color": ORANGE_TEXT, "size": 16},
            {"text": "s6_numbers_talk", "after": 14},
            {"text": "Homework", "bold": True, "color": ORANGE_TEXT, "size": 16},
            {"text": "seaborn, case hunt, Power BI", "after": 14},
            {"text": "Recall", "bold": True, "color": ORANGE_TEXT, "size": 16},
            {"text": "Fri 4 to Sun 6"}],
           size=20, color=NAVY, name="side")


def thanks(d):
    k.thanks_next(d, "Terima kasih untuk hari ini. Angka-angkamu sekarang bisa berbicara lewat grafik dengan judul yang "
                     "jelas. Titik enam selesai. Berikutnya titik tujuh: SQL, Power BI, dan pertanyaan proyekmu sendiri. "
                     "Jangan lupa install Power BI Desktop dan mulai case hunt.")


def build():
    d = k.lecture_deck(6)
    for make in (cover, goals, lookup, count_rows, why_grows, fix, recipe, titles, bar, line, mistakes, seaborn,
                 case_hunt, toolkit, now_colab, thanks):
        make(d)
    k.save(d, OUT)


if __name__ == "__main__":
    build()
