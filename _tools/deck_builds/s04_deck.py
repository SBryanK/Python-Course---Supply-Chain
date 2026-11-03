"""Build the S4 deck: Cleaning day."""
from pathlib import Path

import deckkit as k

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "sessions" / "s04_cleaning_day" / "deck.pptx"


def build():
    d = k.new_deck()

    k.cover(d, "Cleaning day", 4, "Thu 26 Nov 2026",
            "Halo, selamat datang di cleaning day. Hari ini sesi paling berat: kita bersihkan 105.335 baris dan "
            "menjawab berapa penjualan bersih kita, yaitu 1.876.534,04 pounds. Waktunya kita bagi dengan tenang, ada "
            "istirahat di tengah. Kamu yang mengetik semua kodenya, saya menemani. Anggap file mentah ini seperti gudang "
            "yang belum ditata; tugas kita menata raknya. Batasnya, kita tidak membuang data tanpa alasan; setiap baris "
            "yang dibuang harus punya sebab. Siap masuk ke gudangnya?",
            seconds=20)

    k.question(d, "What does the data look like when it is clean, and how much did we sell?",
               "Pertanyaannya dua: seperti apa data yang bersih, dan berapa yang kita jual? Anggap file mentah seperti "
               "catatan gudang yang masih kotor, dan kita ingin satu tabel bersih yang bisa dipercaya. Batasnya, tabel "
               "bersih bukan berarti semua baris dibuang; hanya baris yang memang tidak masuk hitungan. Menurutmu, "
               "baris seperti apa yang sebaiknya dibuang?",
               seconds=40)

    k.concept(d, "read_csv opens the file",
              "Opening the workbook.",
              "File > Open.",
              "The path must be exact.",
              ['import pandas as pd',
               'folder = "/content/drive/MyDrive/Python for Supply Chain"',
               'csv_file = "online_retail_ii_lesson.csv"',
               'sales = pd.read_csv(f"{folder}/data/{csv_file}")',
               'sales.head()'],
              "Kita mulai dari membuka file. read_csv membaca CSV dan menyimpannya sebagai tabel bernama sales, lalu "
              "head menampilkan lima baris pertama. Anggap seperti membuka buku besar dan membaca halaman pertama. "
              "Batasnya, path harus tepat; satu huruf saja salah, muncul FileNotFoundError. Di notebook, sel pertama "
              "mount Drive dulu, dan path lengkapnya ada di sana. Di slide ini folder dan nama file dipisah supaya "
              "muat. Menurutmu, kenapa kita perlu melihat data dulu sebelum membersihkannya?",
              seconds=75, code_size=14)

    k.concept(d, "Look first: 105,335 rows and 8 columns",
              "First page, page count, cover.",
              "Scrolling and COUNTA.",
              "Looking first is part of the job.",
              ['sales.shape',
               'sales.info()',
               'sales.isna().sum()'],
              "Sebelum membersihkan, kita lihat dulu. shape memberi jumlah baris dan kolom, yaitu 105.335 baris dan 8 "
              "kolom. info menunjukkan tipe kolom dan sel kosong, dan isna menghitung sel kosong. Anggap seperti "
              "menghitung jumlah kotak di gudang sebelum menata. Batasnya, melihat dulu itu bagian dari pekerjaan; "
              "kalau langsung dibersihkan, kita tidak tahu apa yang hilang. Coba tebak, kolom apa yang paling banyak "
              "kosong?",
              seconds=70, code_size=14)

    k.concept(d, "A dict gives columns shorter names",
              "Relabelling the bins.",
              "Editing the headers.",
              "Uses the dict from session 2.",
              ['new_names = {',
               '    "Invoice": "invoice", "Price": "price",',
               '    "Quantity": "quantity", "Country": "country",',
               '}',
               'sales = sales.rename(columns=new_names)'],
              "Delapan nama kolom masih panjang dan berhuruf besar. Kita buat dict dari nama lama ke nama baru, lalu "
              "memakai rename. Ini dict yang sama dari sesi dua. Anggap seperti menempel label baru di rak; isi kotaknya "
              "tidak berubah, hanya namanya. Batasnya, kalau satu nama salah ketik, kolom itu tidak berganti dan nanti "
              "muncul KeyError. Di slide ini empat contohnya, notebook mengganti delapan kolom. Menurutmu, kenapa nama "
              "pendek lebih enak dipakai?",
              seconds=70, code_size=14)

    k.concept(d, "A filter keeps only the rows you want",
              "Keeping only the good boxes.",
              "Filter, then copy the result.",
              "The original does not change. Use & and brackets.",
              ['is_germany = sales_clean["country"] == "Germany"',
               'germany = sales_clean[is_germany]',
               'germany.shape'],
              "Filter menyimpan hanya baris yang lolos uji. Kita uji country sama dengan Germany dan quantity lebih "
              "dari 100, lalu menggabungkan dua uji itu dengan tanda & dan tanda kurung. Anggap seperti menyisihkan "
              "kotak yang layak saja. Batasnya, tabel asli tidak berubah; hasil filter disimpan di nama baru. Kalau "
              "memakai kata and, Python memberi error yang membingungkan. Filter Germany saja menghasilkan 1.514 baris. "
              "Menurutmu, dua syarat tadi memilih baris seperti apa?",
              seconds=70, code_size=14)

    k.concept(d, "Add a revenue column, then sort",
              "Writing a value on each box.",
              "A formula column, then Sort Z to A.",
              "No auto-update. Top row: 541431.",
              ['revenue = sales_clean["quantity"] * sales_clean["price"]',
               'sales_clean["revenue"] = revenue',
               'top = sales_clean.sort_values("revenue", ascending=False)',
               'top.head(10)'],
              "Kita tambah kolom revenue, yaitu quantity kali price untuk setiap baris. Lalu kita urutkan dari yang "
              "terbesar dengan sort_values. Anggap seperti menulis harga di setiap kotak, lalu menaruh kotak termahal "
              "di depan. Batasnya, kolom baru tidak otomatis diperbarui kalau data berubah, jadi jalankan sel lagi. Dan "
              "di baris teratas ada kejutan: invoice 541431 dengan 77.183,60 pounds. Menurutmu, pesanan sebesar itu "
              "wajar atau mencurigakan?",
              seconds=75, code_size=14)

    k.concept(d, "A real date comes first, then the month",
              "A calendar column.",
              "A date cell.",
              "A real date first, then group by month.",
              ['dates = pd.to_datetime(sales_clean["invoice_date"])',
               'sales_clean["invoice_date"] = dates',
               'sales_clean["month"] = dates.dt.to_period("M")'],
              "Kolom tanggal masih teks. pd.to_datetime mengubahnya jadi tanggal sungguhan, lalu dt.to_period "
              "mengubahnya jadi bulan. Anggap seperti kalender: tanggal harus benar dulu sebelum bisa dikelompokkan per "
              "bulan. Batasnya, kalau tanggal masih teks, pengelompokan per bulan tidak bisa dipercaya. Setelah ini, "
              "total revenue bersih kita 1.876.534,04 pounds. Menurutmu, bulan apa yang paling besar?",
              seconds=70, code_size=14)

    k.now_in_colab(d, "s4_cleaning_day.ipynb",
                   "Sekarang kita pindah ke notebook s4_cleaning_day. Kita bersihkan setahap demi setahap, mencatat "
                   "jumlah baris setelah setiap langkah, lalu menyimpan tabel bersih untuk sesi lima. Anggap seperti "
                   "menata gudang sambil menulis catatan di buku. Batasnya, setiap langkah harus dicek jumlah barisnya; "
                   "kalau tidak, kita tidak tahu apa yang hilang. Siap mengecek baris pertama?",
                   seconds=30,
                   items=[("Notebook", "s4_cleaning_day.ipynb"),
                          ("In class", "Clean, count rows, write the log"),
                          ("At the end", "Save sales_clean.csv to work")])

    d.two_lists("Clean data and 1,876,534.04 pounds",
                ("Recap in numbers",
                 ["105,335 raw rows, 8 columns",
                  "101,458 clean rows, 10 columns",
                  "1,876,534.04 pounds"]),
                ("Homework and recall",
                 ["Re-run the notebook",
                  "Write the cleaning log",
                  "Try describe",
                  "Recall Fri 27 to Sun 29"]),
                notes="Recap: file mentah 105.335 baris dan 8 kolom menjadi tabel bersih 101.458 baris dan 10 kolom, "
                      "dengan revenue 1.876.534,04 pounds. Perjalanan barisnya dari 105.335 ke 104.360 setelah duplikat, "
                      "102.471 setelah invoice berawalan C, 102.257 setelah quantity, 101.933 setelah price, 101.459 "
                      "setelah kode produk, dan 101.458 setelah pesanan raksasa dihapus. Anggap log ini seperti catatan "
                      "perjalanan: setiap langkah meninggalkan jejak. PR: jalankan ulang notebook, tulis log ini dengan "
                      "bahasamu sendiri, dan coba describe. Recall Jumat sampai Minggu. Bagian mana dari pembersihan "
                      "yang paling sulit kamu ikuti?",
                speaker="Bryan", seconds=50)

    k.save(d, OUT)


if __name__ == "__main__":
    build()
