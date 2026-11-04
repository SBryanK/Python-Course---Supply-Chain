"""Build the S7 deck: New tools, your own question.

Theory slides that the teacher talks over: a title, one visual anchor, and at most one short line.
The speaker notes carry the explanation; the notebook is the playground.
"""
from pathlib import Path

import deckkit as k
from deckkit import (M, CW, NAVY, ORANGE, ORANGE_TEXT, SAND, SKY, PEACH, CREAM, MUTED, CODE_INK, WHITE, cols,
                     centred, muted)

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "sessions" / "s07_new_tools" / "deck.pptx"


def cover(d):
    k.cover_for(d, "SQL, Power BI, and your project question",
                "Halo, selamat datang di sesi tujuh. Enam titik sudah lewat. Hari ini sedikit berbeda: kita mencicipi "
                "dua alat baru, SQL dan Power BI, lalu kamu memilih pertanyaan proyekmu sendiri. Mulai sesi delapan, "
                "kamu yang memimpin. Siap?")


def goals(d):
    s, y = k.slide(d, "Today",
                   "Ini tiga bagian hari ini. Satu, SQL: bahasa untuk bertanya ke database. Dua, Power BI: alat "
                   "dashboard, saya tunjukkan dan kamu coba di rumah. Tiga, pertanyaan proyekmu dan rencananya. Blok "
                   "kedua hampir seluruhnya untuk proyek.", seconds=35)
    items = [("SQL", "SELECT  WHERE  GROUP BY"), ("Power BI", "a look, then at home"),
             ("Your question", "project_plan.md")]
    xs, w = cols(3)
    for i, (head, sub) in enumerate(items):
        d.rect(s, xs[i], 2.0, w, 2.6, SAND, name=f"g{i}")
        k.stop(d, s, xs[i] + w / 2 - 0.35, 2.3, 0.7, str(i + 1), ORANGE if i == 0 else NAVY, WHITE, size=22)
        k.label(d, s, xs[i], 3.2, w, 0.5, head, size=24, bold=True, name=f"gh{i}")
        k.label(d, s, xs[i] + 0.1, 3.75, w - 0.2, 0.4, sub, size=15, color=MUTED, mono=True, name=f"gs{i}")


def what_sql(d):
    s, y = k.slide(d, "SQL asks a database a question",
                   "Banyak perusahaan menyimpan data di database, bukan di file CSV. SQL adalah bahasa untuk bertanya ke "
                   "database. Kita pakai SQLite, yang hidup di dalam Python, jadi tidak perlu install. MySQL juga SQL, "
                   "tapi berjalan di server; query dasarnya hampir sama. Di kantormu, data disimpan di mana?",
                   seconds=55)
    x0 = centred(3.4 * 3 + 1.0 * 2)
    k.tile(d, s, x0, 2.0, 3.4, 1.6, "Your question", "in SQL", head_size=22, name="q")
    k.arrow(d, s, x0 + 3.6, 2.6, 0.6, 0.4, fill=ORANGE)
    k.tile(d, s, x0 + 4.4, 2.0, 3.4, 1.6, "Database", "SQLite, MySQL", head_size=22, fill=NAVY, head_color=WHITE,
           sub_color="C9D3DE", name="db")
    k.arrow(d, s, x0 + 8.0, 2.6, 0.6, 0.4, fill=ORANGE)
    k.tile(d, s, x0 + 8.8, 2.0, 3.4, 1.6, "A table back", "the answer", head_size=22, fill=WHITE, line=ORANGE,
           name="t")
    k.code_card(d, s, centred(9.0), 4.2, 9.0, ['sql_table.to_sql("sales", connection, index=False)'], size=17)
    muted(d, s, 5.4, "SQLite lives inside Python. Nothing to install.")


def anatomy(d):
    s, y = k.slide(d, "Read a query line by line",
                   "Query SQL dibaca baris per baris. SELECT memilih kolom. FROM menyebut tabelnya. GROUP BY "
                   "mengelompokkan, sama dengan groupby. ORDER BY DESC mengurutkan dari terbesar. LIMIT membatasi "
                   "jumlah baris. AS memberi nama kolom hasil. Satu query, satu pertanyaan. Jadi ini pola yang kita pakai di semua latihan SQL, dan kamu yang menulisnya.", seconds=65)
    rows = [("SELECT country, SUM(revenue) AS total_revenue", "which columns"), ("FROM sales", "which table"),
            ("GROUP BY country", "the piles"), ("ORDER BY total_revenue DESC", "biggest first"),
            ("LIMIT 5", "five rows")]
    x0 = centred(8.2 + 0.3 + 3.0)
    for i, (code, mean) in enumerate(rows):
        ry = 1.8 + i * 0.78
        k.chip(d, s, x0, ry, 8.2, 0.62, code, NAVY, CODE_INK, size=17, mono=True, name=f"c{i}")
        k.label(d, s, x0 + 8.5, ry, 3.0, 0.62, mean, size=17, color=MUTED, align="left", name=f"m{i}")
    muted(d, s, 5.85, "One query, one question.")


def side_by_side(d):
    s, y = k.slide(d, "SQL and pandas: the same idea",
                   "Ini pertanyaan yang sama dalam dua bahasa. Kiri SQL, kanan pandas yang sudah kamu kenal. GROUP BY "
                   "sama dengan groupby, WHERE sama dengan filter, ORDER BY sama dengan sort_values. Belajar idenya "
                   "sekali, dan kamu bisa membaca keduanya. Jawabannya sama: Inggris 1.591.694,50 pounds.", seconds=60)
    pairs = [("WHERE", "df[mask]"), ("GROUP BY", ".groupby()"), ("SUM()", ".sum()"), ("ORDER BY ... DESC",
                                                                                      ".sort_values(ascending=False)"),
             ("LIMIT 5", ".head(5)")]
    x0 = centred(4.0 + 1.2 + 5.6)
    k.label(d, s, x0, 1.7, 4.0, 0.4, "SQL", size=18, bold=True, color=ORANGE_TEXT)
    k.label(d, s, x0 + 5.2, 1.7, 5.6, 0.4, "pandas", size=18, bold=True, color=ORANGE_TEXT)
    for i, (a, b) in enumerate(pairs):
        ry = 2.2 + i * 0.72
        k.chip(d, s, x0, ry, 4.0, 0.58, a, NAVY, CODE_INK, size=17, mono=True, name=f"a{i}")
        k.label(d, s, x0 + 4.0, ry, 1.2, 0.58, "=", size=24, bold=True, color=MUTED, name=f"eq{i}")
        k.chip(d, s, x0 + 5.2, ry, 5.6, 0.58, b, SAND, NAVY, size=17, mono=True, name=f"b{i}")
    muted(d, s, 5.95, "Learn the idea once.")


def where(d):
    s, y = k.slide(d, "WHERE is the filter",
                   "WHERE adalah filter di SQL, seperti df mask di pandas. Teks ditulis dengan tanda kutip tunggal. Satu "
                   "tanda sama dengan, bukan dua, karena di SQL tidak ada penyimpanan nilai. Query ini menjumlahkan "
                   "revenue Jerman saja. Hasilnya harus sama dengan groupby di sesi lima.", seconds=55)
    k.code_card(d, s, centred(9.0), 1.85, 9.0, ["SELECT SUM(revenue) AS germany_revenue", "FROM sales",
                                               "WHERE country = 'Germany'"], output=["37365.63"], size=18)
    xs, w = cols(2, gap=0.4, w=9.0, x=centred(9.0))
    k.tile(d, s, xs[0], 4.45, w, 1.2, "'Germany'", "single quotes for text", mono=True, head_size=22, name="q")
    k.tile(d, s, xs[1], 4.45, w, 1.2, "=", "one sign asks in SQL", mono=True, head_size=26, fill=PEACH,
           line=ORANGE, name="e")


def results(d):
    s, y = k.slide(d, "The first query's answer",
                   "Ini hasil query pertama: lima negara dengan revenue terbesar. Angkanya sama persis dengan pandas. "
                   "Inggris jauh di atas, jadi grafik ini menunjukkan pasar Inggris, bukan pasar global. Kalau kamu "
                   "manajer, pertanyaan apa yang muncul berikutnya?", seconds=50)
    chart = d.bar_chart(s, M, 1.55, CW, 4.7, ["United Kingdom", "Netherlands", "EIRE", "Germany", "France"],
                        {"Revenue": [1591694.50, 58182.55, 43426.19, 37365.63, 32392.39]}, colors=[NAVY],
                        horizontal=True, legend=False, number_format="#,##0.00", point_colors={0: ORANGE}, gap=45)
    chart.category_axis.reverse_order = True
    chart.value_axis.visible = False
    chart.value_axis.has_major_gridlines = False


def power_bi(d):
    s, y = k.slide(d, "Power BI: a dashboard in four steps",
                   "Power BI adalah alat dashboard: grafik yang bisa diklik dan dibagikan, tanpa kode. Saya tunjukkan "
                   "sekarang dalam tujuh menit, dan kamu ulangi di rumah dengan intro_powerbi. Empat langkah: ambil data "
                   "dari product_value.csv, buat bar chart, buat card dengan total, simpan. Lalu kirim screenshot.",
                   seconds=55)
    steps = [("Get data", "Text/CSV: product_value.csv"), ("Bar chart", "product and revenue"),
             ("Card", "total revenue"), ("Save", "send a screenshot")]
    xs, w = cols(4)
    for i, (head, sub) in enumerate(steps):
        d.rect(s, xs[i], 1.9, w, 2.6, NAVY if i == 0 else SAND, name=f"s{i}")
        k.stop(d, s, xs[i] + w / 2 - 0.35, 2.15, 0.7, str(i + 1), ORANGE, WHITE, size=22)
        k.label(d, s, xs[i], 3.05, w, 0.5, head, size=22, bold=True, color=WHITE if i == 0 else NAVY)
        k.label(d, s, xs[i] + 0.2, 3.6, w - 0.4, 0.7, sub, size=16, color="C9D3DE" if i == 0 else MUTED,
                anchor="top")
    muted(d, s, 5.0, "Watch today. Build it at home.")


def good_question(d):
    s, y = k.slide(d, "A good question is...",
                   "Pertanyaan analis yang baik punya tiga sifat. Spesifik: satu hal, bukan apa yang mendorong penjualan. "
                   "Bisa dijawab dengan data ini. Berguna: seseorang bisa memutuskan sesuatu dari jawabannya. Kalau "
                   "pertanyaan butuh skill yang belum kita pelajari, ubah pertanyaannya, bukan skill-nya.", seconds=60)
    items = [("Specific", "one thing"), ("Answerable", "with this data"), ("Useful", "someone can decide")]
    xs, w = cols(3)
    for i, (head, sub) in enumerate(items):
        k.tile(d, s, xs[i], 1.9, w, 2.2, head, sub, head_size=28, name=f"t{i}",
               fill=NAVY if i == 2 else SAND, head_color=WHITE if i == 2 else NAVY,
               sub_color="C9D3DE" if i == 2 else MUTED)
    k.box(d, s, centred(8.4), 4.6, 8.4, "Change the question, not the skill.", size=19)


def data_we_have(d):
    s, y = k.slide(d, "What this data can and cannot answer",
                   "Sebelum memilih, cek kolomnya. Kita punya produk, negara, tanggal, quantity, harga dan revenue, tiga "
                   "bulan saja. Kita tidak punya profit, stok, atau lead time. Jadi pertanyaan tentang profit tidak bisa "
                   "dijawab dengan data ini. Pertanyaan tentang reorder point bisa, tapi lead time-nya asumsi.",
                   seconds=60)
    have = ["stock_code, description", "country", "invoice_date, month", "quantity, price, revenue"]
    lack = ["profit", "stock levels", "lead times", "more than 3 months"]
    xs, w = cols(2, gap=0.5, w=11.0, x=centred(11.0))
    k.label(d, s, xs[0], 1.75, w, 0.4, "We have", size=20, bold=True, color=ORANGE_TEXT)
    k.label(d, s, xs[1], 1.75, w, 0.4, "We do not have", size=20, bold=True, color=MUTED)
    for i, (a, b) in enumerate(zip(have, lack)):
        ry = 2.3 + i * 0.75
        k.chip(d, s, xs[0], ry, w, 0.6, a, NAVY, CODE_INK, size=17, mono=True, name=f"h{i}")
        k.chip(d, s, xs[1], ry, w, 0.6, b, SAND, MUTED, size=17, name=f"l{i}")


def menu(d):
    s, y = k.slide(d, "The project menu",
                   "Ini menu proyek. Pilih satu, atau tulis sendiri. Satu: apakah revenue kelas A stabil setiap bulan? "
                   "Dua: negara mana di luar Inggris yang paling banyak membeli, dan apa lima produk teratasnya? Tiga: "
                   "seberapa besar pembatalan? Empat: reorder point untuk lima produk teratas, dengan asumsi yang kamu "
                   "pilih. Mana yang paling menarik untukmu?", seconds=70)
    items = [("Steady stars?", "Is class A revenue steady month to month?"),
             ("Best export market", "Top country outside the UK, and its top 5 products"),
             ("Cancellations", "How big, and which products? cancellations.csv"),
             ("Reorder point", "Top 5 products, your own lead time. Label every assumption.")]
    xs, w = cols(2, gap=0.3)
    for i, (head, sub) in enumerate(items):
        x, ty = xs[i % 2], 1.75 + (i // 2) * 2.05
        d.rect(s, x, ty, w, 1.8, SAND, name=f"m{i}")
        k.stop(d, s, x + 0.3, ty + 0.55, 0.7, str(i + 1), NAVY, WHITE, size=22)
        k.label(d, s, x + 1.3, ty + 0.3, w - 1.5, 0.45, head, size=21, bold=True, align="left", name=f"mh{i}")
        k.label(d, s, x + 1.3, ty + 0.85, w - 1.5, 0.75, sub, size=16, color=MUTED, align="left", anchor="top",
                name=f"ms{i}")
    muted(d, s, 6.0, "Or write your own.")


def plan(d):
    s, y = k.slide(d, "Your project plan",
                   "Rencana proyekmu punya lima baris: pertanyaan, kolom yang dibutuhkan, langkah-langkah, grafik yang "
                   "kamu harapkan, dan keputusan yang dibantu. Tulis di project_plan.md. Rencana yang jelas hari ini "
                   "membuat sesi delapan jauh lebih mudah.", seconds=50)
    fields = ["My question", "Columns I need", "Steps", "The chart I expect", "The decision it helps"]
    x0 = centred(9.0)
    for i, f in enumerate(fields):
        ry = 1.8 + i * 0.8
        k.stop(d, s, x0, ry, 0.6, str(i + 1), ORANGE if i == 0 else NAVY, WHITE, size=18)
        k.chip(d, s, x0 + 0.85, ry, 3.5, 0.6, f, SAND, NAVY, size=18, bold=True, name=f"f{i}")
        d.line(s, x0 + 4.6, ry + 0.45, x0 + 9.0, ry + 0.45, color=SKY, width=1.5, dash=True)
    muted(d, s, 6.0, "project_plan.md")


def toolkit(d):
    s, y = k.slide(d, "Your SQL toolkit",
                   "Ini ringkasan SQL hari ini. Latihan tambahan gratis ada di sql-practice.com. Mana yang paling mirip "
                   "dengan pandas?", seconds=35)
    rows = [["SQL", "Does"], ["SELECT col1, col2", "choose columns"], ["FROM sales", "the table"],
            ["WHERE country = 'Germany'", "keep some rows"], ["GROUP BY country", "piles"],
            ["SUM(revenue) AS total", "add and name it"], ["ORDER BY total DESC", "biggest first"],
            ["LIMIT 10", "the first rows"], ["pd.read_sql_query(query, connection)", "run it from Python"]]
    k.ltable(d, s, centred(10.6), 1.7, 10.6, rows, [6.0, 4.6], code_cols=(0,), size=16, row_h=0.5)


def now_colab(d):
    s, y = k.slide(d, "Now in Colab",
                   "Sekarang kita pindah ke notebook s7_new_tools. Tangganya: satu tebakan, dua isian, satu bug, dua query "
                   "yang kamu tulis sendiri, dan satu kasus. Lalu rencana proyek. Siap?", seconds=30)
    k.ladder(d, s, M, 1.85, 8.0, 3.6, [("Predict", 1), ("Fill in", 2), ("Fix it", 1), ("Write it", 2), ("Case", 1)])
    d.text(s, 9.3, 1.9, 3.43, 4.2,
           [{"text": "Notebook", "bold": True, "color": ORANGE_TEXT, "size": 16},
            {"text": "s7_new_tools", "after": 14},
            {"text": "Homework", "bold": True, "color": ORANGE_TEXT, "size": 16},
            {"text": "Power BI, project plan", "after": 14},
            {"text": "Recall", "bold": True, "color": ORANGE_TEXT, "size": 16},
            {"text": "Tue 8, Wed 9 Dec"}],
           size=20, color=NAVY, name="side")


def thanks(d):
    k.thanks_next(d, "Terima kasih untuk hari ini. Kamu sudah mencoba SQL dan memilih pertanyaan proyekmu. Titik tujuh "
                     "selesai. Berikutnya titik delapan: kerja detektif untuk pertanyaanmu sendiri, dan presentasi case "
                     "hunt dua menit. Jangan lupa Power BI di rumah.")


def build():
    d = k.lecture_deck(7)
    for make in (cover, goals, what_sql, anatomy, side_by_side, where, results, power_bi, good_question,
                 data_we_have, menu, plan, toolkit, now_colab, thanks):
        make(d)
    k.save(d, OUT)


if __name__ == "__main__":
    build()
