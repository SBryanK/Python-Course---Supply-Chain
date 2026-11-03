"""Build the S7 deck: New tools, your own question."""
from pathlib import Path

import deckkit as k

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "sessions" / "s07_new_tools" / "deck.pptx"


def build():
    d = k.new_deck()

    k.cover(d, "New tools, your own question", 7, "Mon 7 Dec 2026",
            "Hari ini ada tiga bagian pendek. Pertama, SQL. Kedua, Power BI. Ketiga dan paling penting, kamu memilih "
            "pertanyaan untuk proyekmu. Dua bagian pertama hanya pengenalan.",
            seconds=20)

    k.question(d, "What question will you answer in your project?",
               "Mulai hari ini kamu bekerja untuk dirimu sendiri. SQL dan Power BI hanya dua alat tambahan untuk "
               "menjawab pertanyaan. Yang paling penting adalah pertanyaan yang kamu pilih. Kalau waktu mepet, "
               "pengenalan alat kita potong dan kita pakai waktunya untuk proyek.",
               seconds=40)

    k.code_compare(d, "SQL and pandas answer the same question",
                   "SQL",
                   ['SELECT country,',
                    '  SUM(revenue) AS total',
                    'FROM sales',
                    'GROUP BY country',
                    'ORDER BY total DESC',
                    'LIMIT 5'],
                   "pandas",
                   ['totals = sales_clean.groupby(',
                    '    "country")["revenue"].sum()',
                    'totals = totals.sort_values(',
                    '    ascending=False)',
                    'totals.head(5)'],
                   "Dua bahasa, satu pertanyaan: lima negara dengan penjualan terbesar. GROUP BY sama dengan groupby. "
                   "ORDER BY DESC sama dengan sort_values dari yang terbesar. Kita memakai SQLite karena sudah ada di "
                   "Python. MySQL adalah database lain yang jalan di server, tetapi query dasarnya hampir sama. "
                   "Hasilnya sama: United Kingdom 1.591.694,50 di urutan pertama.",
                   seconds=80)

    k.table_slide(d, "Four SQL words cover most questions",
                  [["SQL", "pandas idea"],
                   ["SELECT ... FROM", "choose columns"],
                   ["WHERE", "filter rows"],
                   ["GROUP BY", "groupby"],
                   ["ORDER BY ... LIMIT", "sort, keep the top"]],
                  "Empat kata kunci SQL yang sering dipakai, masing-masing dengan padanannya di pandas. Kamu sudah tahu "
                  "idenya; hanya ejaannya yang baru. Latihan gratis ada di sql-practice.com.",
                  seconds=45,
                  below="Free practice: sql-practice.com",
                  col_widths=[4.2, 4.2])

    s = d.new_slide()
    y = d.title(s, "Power BI in three clicks")
    d.steps(s, y + 0.1, [("Get data", "Open product_value.csv"),
                         ("Bar chart", "Product and revenue"),
                         ("Card", "Total revenue")])
    d.footer(s)
    d.notes(s, "Saya tunjukkan Power BI di layar selama tujuh menit. Tiga langkah: ambil data dari file CSV, buat satu "
               "grafik batang, lalu satu kartu angka. Kamu yang mengulanginya di rumah dengan intro_powerbi.md, lalu "
               "kirim screenshot. Power BI cocok untuk dashboard; Python cocok untuk menyiapkan dan memeriksa datanya.",
            "Bryan", 40)

    k.cards(d, "A good question has three parts",
            [("Specific", None, "One thing, not 'what drives sales?'"),
             ("Answerable", None, "Products, countries, dates. No profit data."),
             ("Useful", None, "A manager can decide something.")],
            notes="Pertanyaan yang baik punya tiga ciri. Spesifik: satu hal saja. Bisa dijawab dengan data kita: ada "
                  "produk, negara, tanggal, jumlah, dan harga, tetapi tidak ada laba atau stok. Berguna: manajer bisa "
                  "mengambil keputusan dari jawabannya. Kalau pertanyaan butuh keterampilan yang belum diajarkan, kita "
                  "ubah pertanyaannya, bukan keterampilannya.",
            seconds=60, cols=3)

    k.table_slide(d, "Pick one project, or write your own",
                  [["#", "Question"],
                   ["1", "Is class A revenue steady by month?"],
                   ["2", "Which country outside the UK buys most?"],
                   ["3", "Which products get cancelled most?"],
                   ["4", "A reorder point, with your assumptions"]],
                  "Ini empat contoh pertanyaan. Kamu boleh menulis pertanyaanmu sendiri asal masuk tiga ciri tadi. Nomor "
                  "4 memakai asumsi yang kamu pilih, jadi tandai dengan jelas bahwa itu asumsi, bukan data. Sekarang "
                  "isi project_plan.md: pertanyaan, kolom, langkah, grafik, dan keputusan.",
                  seconds=60,
                  col_widths=[0.8, 7.6])

    k.now_in_colab(d, "s7_new_tools.ipynb",
                   "Sekarang buka notebook s7_new_tools. Kita lihat dua query SQL, lalu kamu mengisi rencana "
                   "proyekmu.",
                   seconds=20,
                   items=[("Notebook", "s7_new_tools.ipynb"),
                          ("In class", "SQL, then your project plan"),
                          ("At home", "Power BI chart")])

    k.homework(d, ["Build the Power BI chart at home", "Finish your project plan", "Start the first analysis"],
               ["Three questions Tuesday", "Three questions Wednesday"],
               "Ini PR untuk kamu: bangun grafik Power BI di rumah dan kirim screenshot, selesaikan rencana proyek, dan mulai analisis "
               "pertama. Recall Selasa dan Rabu, tiga pertanyaan tiap hari.",
               seconds=30)

    k.save(d, OUT)


if __name__ == "__main__":
    build()
