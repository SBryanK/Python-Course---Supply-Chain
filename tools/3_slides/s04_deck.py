"""Build the S4 deck: Cleaning day.

Theory slides that the teacher talks over: a title, one visual anchor, and at most one short line.
The slide text is a reference, not a script; the speaker notes carry the explanation. The notebook is
the playground, so the slides never show the answer to a notebook exercise.
"""
from pathlib import Path

import deckkit as k
from deckkit import (M, CW, NAVY, ORANGE, ORANGE_TEXT, SAND, SKY, PEACH, CREAM, MUTED, CODE_INK, WHITE, cols,
                     centred, muted)

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "sessions" / "s04_cleaning_day" / "deck.pptx"

# Rows removed at each cleaning step (checked by the S4 notebook run)
LOG = [("Duplicates", 975), ("Cancelled (C...)", 1889), ("Quantity 0 or less", 214),
       ("Price 0 or less", 324), ("Not a product", 474), ("Giant order", 1)]


def cover(d):
    k.cover_for(d, "pandas, missing values, filters, new columns",
                "Halo, selamat datang di sesi empat dari sepuluh. Lihat jalannya: tiga titik sudah kita lewati, dan "
                "jalannya terus naik. Hari ini kita belajar pandas dan membersihkan data penjualan yang asli. Kita "
                "bergantian: teori sebentar di slide, lalu kamu mencoba di notebook. Siap?")


def goals(d):
    s, y = k.slide(d, "Today",
                   "Ini enam bagian hari ini. Satu, membaca file dan melihatnya dulu. Dua, sel kosong. Tiga, filter. "
                   "Empat, aturan pembersihan. Lima, kolom baru. Enam, mengurutkan, menghitung dan menyimpan. Setiap "
                   "bagian punya latihan di notebook.", seconds=40)
    items = [("Read and look", "read_csv  head  info"), ("Missing values", "isna  sum"),
             ("Filters", "df[mask]  &  |  ~"), ("Cleaning rules", "6 rules, 1 log"),
             ("New columns", "revenue  month"), ("Sort, count, save", "value_counts  to_csv")]
    xs, w = cols(3)
    for i, (head, sub) in enumerate(items):
        x, ty = xs[i % 3], 1.75 + (i // 3) * 2.45
        d.rect(s, x, ty, w, 2.15, SAND, name=f"g{i}")
        k.stop(d, s, x + 0.35, ty + 0.35, 0.6, str(i + 1), ORANGE if i == 0 else NAVY, WHITE, size=20)
        k.label(d, s, x + 0.35, ty + 1.08, w - 0.7, 0.45, head, size=22, bold=True, align="left", name=f"gh{i}")
        k.label(d, s, x + 0.35, ty + 1.55, w - 0.7, 0.4, sub, size=15, color=MUTED, mono=True, align="left",
                name=f"gs{i}")


def dataframe(d):
    s, y = k.slide(d, "pandas and the DataFrame",
                   "pandas adalah library Python untuk tabel. Satu tabel disebut DataFrame, satu kolomnya disebut Series. "
                   "Nama kolom ada di atas, index di kiri sebagai label baris. Bedanya dengan Excel: index mulai dari 0, "
                   "sama seperti list di sesi dua. Kolom oranye adalah satu Series. Menurutmu, kenapa satu kolom hanya "
                   "punya satu tipe data?", seconds=70)
    heads = ["invoice", "quantity", "price", "country"]
    vals = [["536365", "6", "2.55", "United Kingdom"], ["536365", "6", "3.39", "United Kingdom"],
            ["536370", "24", "3.75", "France"], ["536389", "6", "2.10", "Australia"]]
    cw, iw, gap = 2.25, 0.7, 0.06
    total = iw + 0.12 + 4 * cw + 3 * gap
    x0 = centred(total)
    tx = x0 + iw + 0.12
    k.label(d, s, tx, 1.65, 4 * cw + 3 * gap, 0.35, "column names", size=16, bold=True, color=ORANGE_TEXT)
    for j, h in enumerate(heads):
        k.chip(d, s, tx + j * (cw + gap), 2.05, cw, 0.5, h, NAVY, WHITE, size=16, mono=True, name=f"h{j}")
    for i, row in enumerate(vals):
        ry = 2.62 + i * 0.52
        k.chip(d, s, x0, ry, iw, 0.46, str(i), SKY, NAVY, size=16, mono=True, name=f"i{i}")
        for j, v in enumerate(row):
            k.chip(d, s, tx + j * (cw + gap), ry, cw, 0.46, v, PEACH if j == 1 else WHITE, NAVY, size=15,
                   mono=True, line=SAND, name=f"c{i}{j}")
    k.label(d, s, x0 - 0.3, 4.75, iw + 0.6, 0.35, "index", size=16, bold=True, color=ORANGE_TEXT)
    k.label(d, s, tx + cw + gap, 4.75, cw, 0.35, "one Series", size=16, bold=True, color=ORANGE_TEXT)
    xs, w = cols(3, gap=0.25, w=10.5, x=centred(10.5))
    for x, t in zip(xs, ["DataFrame  ≈  a sheet", "Series  ≈  a column", "index  ≈  row number, from 0"]):
        k.chip(d, s, x, 5.6, w, 0.6, t, SAND, NAVY, size=17, name="eq")


def read_file(d):
    s, y = k.slide(d, "read_csv opens a file",
                   "read_csv membuka file CSV dan mengembalikan DataFrame, seperti File > Open di Excel. Path adalah "
                   "alamat file: Drive kamu, folder kursus, folder data, lalu nama file. Colab baru bisa melihat Drive "
                   "setelah drive.mount dijalankan. Satu huruf salah saja dan muncul FileNotFoundError, jadi salin path "
                   "dari panel Files. Bagian mana yang paling mudah salah ketik?", seconds=70)
    parts = [("/content/drive/MyDrive/", "your Drive"), ("Python for Supply Chain/", "course folder"),
             ("data/", "folder"), ("online_retail_ii_lesson.csv", "file")]
    ws = [len(p) * 16 * 0.6 / 72 + 0.3 for p, _ in parts]
    x = centred(sum(ws) + 0.08 * 3)
    for i, ((p, lab), w) in enumerate(zip(parts, ws)):
        k.chip(d, s, x, 1.85, w, 0.62, p, ORANGE if i == 3 else NAVY, WHITE if i == 3 else CODE_INK, size=16,
               mono=True, name=f"p{i}")
        k.label(d, s, x, 2.55, w, 0.35, lab, size=16, color=MUTED, name=f"pl{i}")
        x += w + 0.08
    k.code_card(d, s, centred(9.6), 3.35, 9.6,
                ['folder = "/content/drive/MyDrive/Python for Supply Chain"',
                 'sales = pd.read_csv(folder + "/data/online_retail_ii_lesson.csv")'], size=16)
    k.box(d, s, centred(7.0), 5.3, 7.0, "One wrong letter: FileNotFoundError", size=18)


def look_first(d):
    s, y = k.slide(d, "Look first",
                   "Sebelum membersihkan, kita lihat dulu. head menampilkan baris pertama, shape memberi jumlah baris dan "
                   "kolom, info memberi tipe dan jumlah sel terisi, describe memberi ringkasan angka. Perhatikan: shape "
                   "tanpa kurung karena itu fakta tentang tabel; head pakai kurung karena itu melakukan sesuatu. Kita "
                   "tidak bisa membersihkan yang belum kita lihat.", seconds=65)
    tools = [(".head()", "first rows"), (".shape", "rows, columns"), (".info()", "types, filled cells"),
             (".describe()", "count, mean, min, max")]
    xs, w = cols(4)
    for i, (code, sub) in enumerate(tools):
        k.tile(d, s, xs[i], 1.8, w, 1.9, code, sub, mono=True, head_size=24, name=f"t{i}",
               fill=NAVY if i == 1 else SAND, head_color=WHITE if i == 1 else NAVY,
               sub_color="C9D3DE" if i == 1 else MUTED)
    k.code_card(d, s, centred(6.0), 4.25, 6.0, ["sales.shape"], output=["(105335, 8)"], size=18)
    muted(d, s, 6.15, "no brackets: a fact      brackets: an action")


def dtypes(d):
    s, y = k.slide(d, "One column, one type",
                   "Setiap kolom punya satu tipe data. int64 bilangan bulat, float64 desimal, object teks, datetime64 "
                   "tanggal. Customer ID tampil 17850.0 karena ada sel kosong, dan sel kosong hanya muat di kolom "
                   "desimal. Setelah read_csv, tanggal masih teks, jadi harus diubah dulu sebelum kita ambil bulannya. "
                   "Menurutmu, kenapa tipe data penting?", seconds=70)
    cards = [("int64", "6   24   3906", "Quantity"), ("float64", "2.55   17850.0", "Price, Customer ID"),
             ("object", '"LANTERN"', "Invoice, Description, Country"),
             ("datetime64", "2010-12-07 10:15", "after pd.to_datetime")]
    xs, w = cols(4)
    for i, (t, ex, colnames) in enumerate(cards):
        last = i == 3
        d.rect(s, xs[i], 1.8, w, 2.7, PEACH if last else SAND, line=ORANGE if last else None, name=f"d{i}")
        k.label(d, s, xs[i], 2.0, w, 0.5, t, size=24, mono=True, color=ORANGE_TEXT if last else NAVY)
        k.label(d, s, xs[i] + 0.15, 2.8, w - 0.3, 0.5, ex, size=17, mono=True)
        k.label(d, s, xs[i] + 0.15, 3.55, w - 0.3, 0.7, colnames, size=15, color=MUTED, anchor="top")
    k.box(d, s, centred(7.6), 5.15, 7.6, "After read_csv, dates are text. Convert them first.", size=18)


def rename(d):
    s, y = k.slide(d, "rename gives columns new labels",
                   "Nama kolom masih panjang, ada spasi dan huruf besar. Kita pakai dictionary dari sesi dua: nama lama "
                   "ke nama baru. Nama yang tidak ada di dictionary tetap sama. rename memberi DataFrame baru, jadi "
                   "simpan lagi ke sales. Setelah itu nama lama hilang, dan sales dengan Country huruf besar memberi "
                   "KeyError.", seconds=65)
    pairs = [("Invoice", "invoice"), ("StockCode", "stock_code"), ("Customer ID", "customer_id"),
             ("InvoiceDate", "invoice_date")]
    for i, (old, new) in enumerate(pairs):
        ty = 1.85 + i * 0.82
        k.chip(d, s, M, ty, 2.9, 0.6, old, CREAM, NAVY, size=17, mono=True, line=SKY, name=f"o{i}")
        k.arrow(d, s, M + 3.05, ty + 0.16, 0.7, 0.28)
        k.chip(d, s, M + 3.9, ty, 2.9, 0.6, new, ORANGE, WHITE, size=17, mono=True, name=f"n{i}")
    k.code_card(d, s, 8.0, 2.05, 4.73, ["names = {", '    "Invoice": "invoice",', '    "Customer ID": "customer_id",',
                                        "}", "sales = sales.rename(columns=names)"], size=14)
    k.box(d, s, centred(7.6), 5.55, 7.6, 'After rename, sales["Country"] gives KeyError', size=18)


def missing(d):
    s, y = k.slide(d, "NaN: an empty cell",
                   "Sel kosong tampil sebagai NaN, artinya tidak ada nilai yang dicatat. isna mengubah setiap sel menjadi "
                   "True kalau kosong, False kalau terisi. sum menghitung True, karena True bernilai 1 dan False 0. Empat "
                   "sel, dua kosong, hasilnya 2. Di data asli, Customer ID kosong di 36.210 baris. Kenapa banyak pembeli "
                   "tidak punya ID?", seconds=70)
    vals = ["17850.0", "NaN", "13047.0", "NaN"]
    x0, by = 0.9, 2.0
    k.label(d, s, x0, by - 0.45, 2.2, 0.35, "Customer ID", size=16, bold=True)
    for i, v in enumerate(vals):
        nan = v == "NaN"
        k.chip(d, s, x0, by + i * 0.62, 2.2, 0.52, v, PEACH if nan else WHITE, NAVY, size=17, mono=True, line=SAND,
               name=f"v{i}")
        k.chip(d, s, x0 + 3.5, by + i * 0.62, 1.8, 0.52, str(nan), ORANGE if nan else SAND,
               WHITE if nan else NAVY, size=17, mono=True, name=f"b{i}")
    k.label(d, s, x0 + 2.25, by + 0.55, 1.2, 0.35, ".isna()", size=16, bold=True, color=ORANGE_TEXT, mono=True)
    k.arrow(d, s, x0 + 2.45, by + 0.98, 0.8, 0.32)
    k.label(d, s, x0 + 5.35, by + 0.55, 1.2, 0.35, ".sum()", size=16, bold=True, color=ORANGE_TEXT, mono=True)
    k.arrow(d, s, x0 + 5.55, by + 0.98, 0.8, 0.32)
    k.stop(d, s, x0 + 6.55, by + 0.62, 1.0, "2", NAVY, WHITE, size=32)
    k.code_card(d, s, 9.0, by, 3.73, ["sales.isna().sum()"],
                output=["...", "Description    304", "Customer ID  36210", "..."], size=15)
    muted(d, s, 5.6, "True = 1, False = 0")


def missing_choice(d):
    s, y = k.slide(d, "Keep, drop or fill?",
                   "Ada tiga pilihan untuk sel kosong: biarkan, buang barisnya, atau isi. Pertanyaannya yang menentukan. "
                   "Hari ini kita bertanya tentang produk dan uang, jadi baris tanpa Customer ID kita biarkan; kira-kira "
                   "sepertiga data. Kalau pertanyaannya tentang pembeli, baris itu dibuang. Hati-hati mengisi dengan nol: "
                   "harga kosong yang diisi nol terlihat seperti barang gratis.", seconds=65)
    opts = [("Keep", "(nothing)", "the question does not need it"),
            ("Drop", "dropna(subset=[...])", "the question needs it"),
            ("Fill", "fillna(0)", "a safe default exists")]
    xs, w = cols(3)
    for i, (head, code, when) in enumerate(opts):
        today = i == 0
        d.rect(s, xs[i], 2.05, w, 3.0, WHITE if today else SAND, line=ORANGE if today else None, name=f"o{i}")
        k.label(d, s, xs[i], 2.3, w, 0.55, head, size=28, bold=True, color=ORANGE_TEXT if today else NAVY)
        k.label(d, s, xs[i] + 0.2, 3.15, w - 0.4, 0.45, code, size=16, mono=True)
        k.label(d, s, xs[i] + 0.2, 3.95, w - 0.4, 0.7, when, size=16, color=MUTED, anchor="top")
    k.chip(d, s, xs[0] + w / 2 - 0.6, 1.8, 1.2, 0.42, "today", ORANGE, WHITE, size=15, bold=True, name="today")
    muted(d, s, 5.6, "The question decides.")


def mask(d):
    s, y = k.slide(d, "A condition asks every row",
                   "Kalau kita membandingkan satu kolom, pandas mengecek setiap baris sekaligus. Hasilnya kolom True dan "
                   "False, namanya boolean mask. Setiap negara ditanya: apakah sama dengan Germany? Di kanan, tanda-tanda "
                   "perbandingan. Ingat sesi dua: satu sama dengan menyimpan, dua sama dengan bertanya. Di data mentah ada "
                   "1.741 baris Jerman.", seconds=70)
    rows = ["United Kingdom", "Germany", "France", "Germany", "EIRE"]
    for i, c in enumerate(rows):
        de = c == "Germany"
        k.chip(d, s, M, 1.85 + i * 0.6, 2.6, 0.5, c, WHITE, NAVY, size=16, line=SAND, name=f"r{i}")
        k.chip(d, s, M + 4.25, 1.85 + i * 0.6, 1.7, 0.5, str(de), ORANGE if de else SAND, WHITE if de else NAVY,
               size=16, mono=True, name=f"m{i}")
    k.label(d, s, M + 2.6, 2.75, 1.65, 0.35, '== "Germany"', size=14, bold=True, color=ORANGE_TEXT, mono=True)
    k.arrow(d, s, M + 2.95, 3.2, 0.9, 0.32)
    signs = [("==", "equal"), ("!=", "not equal"), (">", "bigger"), (">=", "bigger or equal"), ("<", "smaller"),
             ("<=", "smaller or equal")]
    xs, w = cols(2, gap=0.2, w=5.5, x=7.23)
    for i, (sg, mean) in enumerate(signs):
        k.tile(d, s, xs[i % 2], 1.85 + (i // 2) * 1.0, w, 0.85, sg, mean, mono=True, head_size=20, sub_size=14,
               name=f"s{i}")
    k.code_card(d, s, centred(7.2), 5.15, 7.2, ['is_germany = sales["country"] == "Germany"'], size=16)


def filtering(d):
    s, y = k.slide(d, "df[mask] keeps the True rows",
                   "Masukkan mask ke dalam kurung siku, dan pandas hanya menyimpan baris yang True. Hasilnya tabel baru, "
                   "dan tabel sales yang asli tidak berubah. Di Excel, filter menyembunyikan baris di sheet yang sama; "
                   "di pandas kita dapat tabel baru dan tabel lama tetap aman. Kenapa itu bagus untuk analis?",
                   seconds=60)
    rows = [("United Kingdom", False), ("Germany", True), ("France", False), ("Germany", True), ("EIRE", False)]
    for i, (c, keep) in enumerate(rows):
        ry = 1.85 + i * 0.6
        k.chip(d, s, 1.2, ry, 2.6, 0.5, c, WHITE if keep else SAND, NAVY if keep else MUTED, size=16,
               line=SAND, name=f"r{i}")
        k.chip(d, s, 3.9, ry, 1.4, 0.5, str(keep), ORANGE if keep else SAND, WHITE if keep else MUTED, size=16,
               mono=True, name=f"k{i}")
    k.arrow(d, s, 5.85, 3.0, 1.2, 0.5, fill=ORANGE)
    k.label(d, s, 7.6, 1.5, 3.0, 0.35, "germany", size=16, bold=True, mono=True, color=ORANGE_TEXT, align="left")
    for i in range(2):
        k.chip(d, s, 7.6, 2.75 + i * 0.6, 2.6, 0.5, "Germany", WHITE, NAVY, size=16, line=ORANGE, name=f"g{i}")
    k.label(d, s, 7.6, 4.0, 4.5, 0.35, "sales stays the same", size=16, color=MUTED, align="left")
    k.code_card(d, s, centred(6.4), 5.05, 6.4, ["germany = sales[is_germany]", "germany.shape"],
                output=["(1741, 8)"], size=16)


def combine(d):
    s, y = k.slide(d, "Two conditions: &  |  ~",
                   "Untuk dua syarat, pakai simbol, bukan kata. Tanda dan berarti keduanya benar, garis tegak berarti "
                   "salah satu benar, tilde membalik True dan False. Setiap syarat masuk ke dalam kurung. Kalau memakai "
                   "kata and, Python memberi ValueError: the truth value of a Series is ambiguous. Artinya: pakai tanda "
                   "dan, dengan kurung.", seconds=70)
    syms = [("&", "both true", "(a > 0) & (b > 0)"), ("|", "at least one", "(a > 0) | (b > 0)"),
            ("~", "flip True/False", "~is_germany")]
    xs, w = cols(3)
    for i, (sym, mean, ex) in enumerate(syms):
        d.rect(s, xs[i], 1.8, w, 2.9, SAND, name=f"y{i}")
        k.label(d, s, xs[i], 1.95, w, 1.1, sym, size=66, bold=True, color=ORANGE_TEXT, mono=True)
        k.label(d, s, xs[i], 3.15, w, 0.45, mean, size=20, bold=True)
        k.label(d, s, xs[i] + 0.2, 3.75, w - 0.4, 0.45, ex, size=16, mono=True, color=MUTED)
    k.box(d, s, centred(8.2), 5.25, 8.2, "Words and / or  →  ValueError. Use symbols and brackets.", size=18)


def text_tools(d):
    s, y = k.slide(d, ".str asks questions about text",
                   "Untuk kolom teks, ada pintu bernama str. Setelah titik str kita bisa bertanya: apakah dimulai dengan "
                   "C, apa huruf pertamanya, apakah semuanya angka, apakah mengandung HEART. Hasilnya True atau False, "
                   "jadi bisa dipakai sebagai filter. Alat ini bisa disambung. str hanya bekerja di kolom teks; di kolom "
                   "angka muncul AttributeError.", seconds=70)
    rows = [("C541433", '.str.startswith("C")', "True"), ("85123A", ".str[0]", '"8"'),
            ("POST", ".str.isdigit()", "False"), ("HEART T-LIGHT", '.str.contains("HEART")', "True")]
    wv, wt, wr, a = 3.0, 4.2, 1.6, 0.6
    total = wv + wt + wr + 2 * (a + 0.3)
    x0 = centred(total)
    for i, (v, tool, res) in enumerate(rows):
        ry = 1.9 + i * 0.95
        k.chip(d, s, x0, ry, wv, 0.6, v, WHITE, NAVY, size=17, mono=True, line=SAND, name=f"v{i}")
        k.arrow(d, s, x0 + wv + 0.15, ry + 0.17, a, 0.26)
        k.chip(d, s, x0 + wv + a + 0.3, ry, wt, 0.6, tool, NAVY, CODE_INK, size=16, mono=True, name=f"t{i}")
        k.arrow(d, s, x0 + wv + wt + a + 0.45, ry + 0.17, a, 0.26)
        k.chip(d, s, x0 + wv + wt + 2 * a + 0.6, ry, wr, 0.6, res, PEACH, NAVY, size=17, mono=True, name=f"r{i}")
    muted(d, s, 5.9, "Text columns only. Tools can be chained.")


def rules(d):
    s, y = k.slide(d, "Six cleaning rules",
                   "Ini enam aturan pembersihan kita. Duplikat menghitung uang dua kali. Invoice berawalan C berarti "
                   "dibatalkan. Quantity nol atau negatif adalah retur atau koreksi stok. Harga nol adalah barang gratis "
                   "atau penyesuaian. Kode seperti POST dan DOT adalah ongkos kirim dan biaya, bukan produk. Dan satu "
                   "pesanan raksasa yang dibatalkan. Setiap baris yang dibuang harus punya alasan.", seconds=90)
    items = [("Duplicates", "same row twice"), ("Cancelled", "invoice starts with C"),
             ("Quantity 0 or less", "returns, stock fixes"), ("Price 0 or less", "free items, adjustments"),
             ("Not a product", "POST, DOT, M"), ("Giant order", "cancelled 16 minutes later")]
    xs, w = cols(3)
    for i, (head, sub) in enumerate(items):
        x, ty = xs[i % 3], 1.8 + (i // 3) * 2.2
        d.rect(s, x, ty, w, 1.95, SAND, name=f"u{i}")
        k.stop(d, s, x + 0.3, ty + 0.3, 0.52, str(i + 1), NAVY, WHITE, size=17)
        k.label(d, s, x + 0.3, ty + 0.98, w - 0.5, 0.42, head, size=20, bold=True, align="left", name=f"uh{i}")
        k.label(d, s, x + 0.3, ty + 1.42, w - 0.5, 0.36, sub, size=16, color=MUTED, align="left", name=f"us{i}")


def cleaning_log(d):
    s, y = k.slide(d, "The cleaning log",
                   "Log pembersihan mencatat berapa baris yang tersisa setelah setiap langkah. Kalau satu angka terlihat "
                   "aneh, kita tahu langkah mana yang dicek. Batang oranye menunjukkan berapa baris yang dibuang: paling "
                   "banyak invoice yang dibatalkan, paling sedikit hanya satu baris. Total 3.877 baris keluar. Di notebook "
                   "kamu mengisi log ini sendiri.", seconds=70)
    top = 2.0
    k.big_number(d, s, M, top + 1.2, 2.7, "105,335", "raw rows", color=NAVY, size=44)
    biggest = max(n for _, n in LOG)
    for i, (lab, n) in enumerate(LOG):
        ry = top + i * 0.66
        k.label(d, s, 3.45, ry, 2.5, 0.42, lab, size=18, align="left", name=f"st{i}")
        w = max(0.06, 2.4 * n / biggest)
        d.rect(s, 6.05, ry + 0.05, w, 0.32, ORANGE, rounded=False, name=f"bar{i}")
        k.label(d, s, 6.15 + w, ry, 1.3, 0.42, f"−{n:,}", size=18, bold=True, color=ORANGE_TEXT, align="left",
                name=f"nm{i}")
    k.big_number(d, s, 10.05, top + 1.2, 2.7, "101,458", "clean rows", size=44)


def new_table(d):
    s, y = k.slide(d, "A filter makes a new table",
                   "Setiap filter membuat tabel baru. Simpan hasilnya ke nama, misalnya sales_clean, supaya tidak hilang. "
                   "Jalankan sel dari atas ke bawah; kalau sel filter dijalankan dua kali, filternya berjalan dua kali. "
                   "Sebelum menambah kolom ke tabel hasil filter, buat salinan dengan copy, seperti Save As. Tanpa copy, "
                   "pandas bisa memberi SettingWithCopyWarning. Menurutmu, apa yang terjadi kalau hasilnya tidak "
                   "disimpan?", seconds=70)
    tw, gw = 2.9, 1.55
    x0 = centred(3 * tw + 2 * gw)
    xb, xc = x0 + tw + gw, x0 + 2 * (tw + gw)
    k.tile(d, s, x0, 1.9, tw, 1.4, "sales", "105,335 rows", mono=True, head_size=22, name="a")
    k.arrow(d, s, x0 + tw + 0.2, 2.4, gw - 0.4, 0.42, fill=ORANGE)
    k.label(d, s, x0 + tw, 2.9, gw, 0.35, "filter", size=15, bold=True, color=ORANGE_TEXT)
    k.tile(d, s, xb, 1.9, tw, 1.4, "sales_clean", "fewer rows", mono=True, head_size=22, fill=NAVY,
           head_color=WHITE, sub_color="C9D3DE", name="b")
    k.arrow(d, s, xb + tw + 0.2, 2.4, gw - 0.4, 0.42, fill=ORANGE)
    k.label(d, s, xb + tw, 2.9, gw, 0.35, ".copy()", size=15, bold=True, color=ORANGE_TEXT, mono=True)
    k.tile(d, s, xc, 1.9, tw, 1.4, "Save As", "safe to change", head_size=22, fill=WHITE, line=ORANGE, name="c")
    k.code_card(d, s, centred(7.0), 3.9, 7.0, ["sales_clean = sales_clean[mask]", "sales_clean = sales_clean.copy()"],
                size=17)
    muted(d, s, 5.65, "Run cells from top to bottom.")


def new_columns(d):
    s, y = k.slide(d, "A new column, every row at once",
                   "Kolom baru dibuat dengan satu baris kode: nama kolom di kurung siku, sama dengan, lalu rumusnya. "
                   "pandas menghitung semua baris sekaligus, tanpa drag ke bawah seperti di Excel. Tapi kolom ini tidak "
                   "otomatis diperbarui; kalau data berubah, jalankan sel lagi. Ingat sesi satu: 6 kali 2,55 menjadi "
                   "15.299999999999999, jadi uang dibulatkan di akhir.", seconds=70)
    k.code_card(d, s, centred(7.6), 1.8, 7.6, ['df["revenue"] = df["quantity"] * df["price"]'], size=17)
    heads = ["quantity", "price", "revenue"]
    rows = [("6", "2.55", "15.30"), ("6", "3.39", "20.34"), ("24", "3.75", "90.00")]
    cw, sym = 2.4, 0.7
    x0 = centred(3 * cw + 2 * sym)
    for j, h in enumerate(heads):
        x = x0 + j * (cw + sym)
        k.chip(d, s, x, 3.05, cw, 0.55, h, ORANGE if j == 2 else NAVY, WHITE, size=17, mono=True, name=f"h{j}")
        for i, row in enumerate(rows):
            k.chip(d, s, x, 3.7 + i * 0.6, cw, 0.5, row[j], PEACH if j == 2 else WHITE, NAVY, size=17, mono=True,
                   line=SAND, name=f"c{i}{j}")
    for j, sy in enumerate(["×", "="]):
        k.label(d, s, x0 + cw + j * (cw + sym), 4.2, sym, 0.6, sy, size=32, bold=True, color=MUTED)
    muted(d, s, 5.85, "No drag-down. No auto-update.")


def dates(d):
    s, y = k.slide(d, "Text becomes a real date",
                   "Setelah read_csv, tanggal masih teks. pd.to_datetime mengubahnya menjadi tanggal sungguhan. Lalu titik "
                   "dt membuka alat tanggal, sama seperti titik str membuka alat teks. Dari satu tanggal kita bisa ambil "
                   "tahun, bulan, nama hari, atau periode bulan. to_period M menyimpan tahun dan bulan bersama. Kenapa "
                   "bulan tanpa tahun bisa menyesatkan?", seconds=70)
    k.code_card(d, s, centred(9.0), 1.75, 9.0, ['sales["invoice_date"] = pd.to_datetime(sales["invoice_date"])'],
                size=16)
    k.chip(d, s, M + 0.3, 3.85, 3.4, 0.75, "2010-12-07 10:15", ORANGE, WHITE, size=18, mono=True, bold=True,
           name="date")
    branch = [(".dt.year", "2010"), (".dt.month", "12"), (".dt.day_name()", "Tuesday"),
              ('.dt.to_period("M")', "2010-12")]
    for i, (tool, res) in enumerate(branch):
        ry = 3.0 + i * 0.72
        d.line(s, M + 3.7, 4.22, 5.1, ry + 0.27, color=SKY, width=1.5)
        k.chip(d, s, 5.1, ry, 4.1, 0.55, tool, NAVY, CODE_INK, size=16, mono=True, name=f"t{i}")
        k.chip(d, s, 9.4, ry, 2.4, 0.55, res, WHITE, NAVY, size=17, mono=True, line=SAND, name=f"r{i}")


def sort_count(d):
    s, y = k.slide(d, "Count rows per value",
                   "value_counts menghitung berapa baris untuk setiap nilai, langsung terurut dari yang terbesar. Lihat "
                   "grafiknya: Inggris jauh di atas negara lain. sort_values mengurutkan seluruh tabel, ascending False "
                   "berarti dari yang terbesar, seperti Sort Z to A. nunique menghitung berapa nilai yang berbeda. Satu "
                   "invoice punya satu baris per produk, jadi baris bukan pesanan.", seconds=70)
    k.code_card(d, s, M, 1.85, 5.6, ['sales["country"].value_counts()'], size=16)
    tools = [(".value_counts()", "rows per value"), (".sort_values()", "biggest first"),
             (".nunique()", "how many different")]
    for i, (code, mean) in enumerate(tools):
        ry = 3.1 + i * 0.85
        k.chip(d, s, M, ry, 2.9, 0.6, code, SAND, NAVY, size=16, mono=True, name=f"k{i}")
        k.label(d, s, M + 3.05, ry, 2.6, 0.6, mean, size=17, color=MUTED, align="left", name=f"km{i}")
    chart = d.bar_chart(s, 6.6, 1.65, 6.13, 4.6, ["United Kingdom", "Germany", "France", "EIRE", "Spain"],
                        {"Rows": [97393, 1741, 1540, 1032, 560]}, colors=[NAVY], horizontal=True, legend=False,
                        number_format="#,##0", point_colors={0: ORANGE}, gap=45)
    chart.value_axis.visible = False
    chart.value_axis.has_major_gridlines = False


def summary_numbers(d):
    s, y = k.slide(d, "Mean or median?",
                   "sum memberi total, mean rata-rata, median nilai tengah. Lihat quantity per baris di data bersih: "
                   "mediannya 3, tapi rata-ratanya 9,39. Kenapa? Ada beberapa pesanan sangat besar, sampai 3.906 buah, "
                   "yang menarik rata-rata ke atas. Median tidak ikut tertarik. Untuk data yang miring seperti ini, "
                   "laporkan median juga. Mana yang lebih jujur untuk pesanan biasa?", seconds=75)
    k.label(d, s, M, 1.75, CW, 0.4, "Quantity per row, clean data", size=18, bold=True)
    ly = 3.75
    d.line(s, 1.0, ly, 12.3, ly, color=MUTED, width=2)
    marks = [("3", "median", 1.4, NAVY, NAVY), ("9.39", "mean", 3.4, ORANGE, ORANGE_TEXT),
             ("3,906", "biggest", 12.3, MUTED, MUTED)]
    for val, lab, x, c, tc in marks:
        d.oval(s, x - 0.17, ly - 0.17, 0.34, c)
        k.label(d, s, x - 1.0, ly - 1.25, 2.0, 0.65, val, size=36, bold=True, color=tc, name=f"v_{lab}")
        k.label(d, s, x - 1.0, ly + 0.3, 2.0, 0.4, lab, size=17, color=tc, name=f"l_{lab}")
    xs, w = cols(4, gap=0.25, w=10.0, x=centred(10.0))
    for x, (code, mean) in zip(xs, [(".sum()", "total"), (".mean()", "average"), (".median()", "middle"),
                                    ("round(x, 2)", "2 decimals")]):
        k.tile(d, s, x, 4.95, w, 1.15, code, mean, mono=True, head_size=18, sub_size=15, name="sn")


def saving(d):
    s, y = k.slide(d, "Save to Drive, or lose it",
                   "to_csv menyimpan tabel ke file. index False berarti label baris tidak ditulis sebagai kolom tambahan. "
                   "Colab lupa semuanya kalau runtime berhenti; hanya file di Drive yang tetap ada. Jadi simpan tabel "
                   "bersih di folder work, supaya sesi lima bisa mulai dari situ.", seconds=55)
    x0 = centred(4.2 * 2 + 2.2)
    k.tile(d, s, x0, 1.95, 4.2, 1.6, "Colab runtime", "forgets when it stops", head_size=24, name="a")
    k.arrow(d, s, x0 + 4.45, 2.55, 1.7, 0.45, fill=ORANGE)
    k.label(d, s, x0 + 4.2, 3.05, 2.2, 0.35, "to_csv", size=16, bold=True, color=ORANGE_TEXT, mono=True)
    k.tile(d, s, x0 + 6.4, 1.95, 4.2, 1.6, "Drive / work", "stays", head_size=24, fill=NAVY, head_color=WHITE,
           sub_color="C9D3DE", name="b")
    k.code_card(d, s, centred(9.4), 4.2, 9.4,
                ['sales_clean.to_csv(folder + "/work/sales_clean.csv", index=False)'], size=16)
    muted(d, s, 5.55, "index=False: no extra column of row labels")


def case_study(d):
    s, y = k.slide(d, "The giant order",
                   "Ini contoh kerja detektif. Setelah membuat revenue dan mengurutkan, baris teratas adalah invoice "
                   "541431: 74.215 toples kali 1,04 pound, jadi 77.183,60 pounds. Kita cari invoice C dengan nomor yang "
                   "hampir sama. Pelanggan sama, produk sama, jumlah sama, 16 menit kemudian. Jadi penjualan ini tidak "
                   "pernah terjadi. Apa pelajaran untuk analis?", seconds=80)
    x0 = centred(3.0 + 0.6 + 2.6 + 0.6 + 3.5)
    k.chip(d, s, x0, 1.9, 3.0, 0.95, "74,215 jars", SAND, NAVY, size=24, bold=True, name="q")
    k.label(d, s, x0 + 3.0, 1.9, 0.6, 0.95, "×", size=34, bold=True, color=MUTED)
    k.chip(d, s, x0 + 3.6, 1.9, 2.6, 0.95, "£1.04 each", SAND, NAVY, size=24, bold=True, name="p")
    k.label(d, s, x0 + 6.2, 1.9, 0.6, 0.95, "=", size=34, bold=True, color=MUTED)
    k.chip(d, s, x0 + 6.8, 1.9, 3.5, 0.95, "£77,183.60", ORANGE, WHITE, size=28, bold=True, name="r")
    rec = [("541431 ", "+74,215 jars", "10:01", WHITE, NAVY), ("C541433", "−74,215 jars", "10:17", PEACH, ORANGE_TEXT)]
    for i, (inv, qty, tm, f, c) in enumerate(rec):
        ry = 3.45 + i * 0.85
        k.chip(d, s, x0, ry, 10.3, 0.7, f"{inv}     {qty}     18 Jan 2011, {tm}", f, c, size=18, mono=True,
               line=SAND, name=f"rc{i}")
    muted(d, s, 5.4, "Same customer, same product, 16 minutes later. The sale never happened.")


def toolkit(d):
    s, y = k.slide(d, "Your cleaning toolkit",
                   "Ini ringkasan alat hari ini, seperti contekan. Kiri untuk membuka, melihat dan memilih baris. Kanan "
                   "untuk membersihkan, menambah kolom dan menyimpan. Kamu akan memakainya lagi di sesi lima sampai "
                   "sepuluh. Mana yang paling sulit diingat?", seconds=45)
    left = [["Code", "Does"], ["pd.read_csv(path)", "open a CSV file"], [".head() .shape .info()", "look first"],
            [".isna().sum()", "count empty cells"], [".rename(columns={...})", "new column names"],
            ["df[mask]", "keep the True rows"], ["&  |  ~", "and, or, not"], [".str...", "text tools"]]
    right = [["Code", "Does"], [".drop_duplicates()", "drop repeats"], [".copy()", "Save As"],
             ['df["new"] = ...', "add a column"], ["pd.to_datetime() .dt", "real dates"],
             [".sort_values() .value_counts()", "sort and count"], [".sum() .mean() .median()", "summary numbers"],
             [".to_csv(path, index=False)", "save to Drive"]]
    xs, w = cols(2, gap=0.3)
    k.ltable(d, s, xs[0], 1.7, w, left, [3.4, w - 3.4], code_cols=(0,), size=15, row_h=0.52)
    k.ltable(d, s, xs[1], 1.7, w, right, [3.95, w - 3.95], code_cols=(0,), size=15, row_h=0.52)


def colab(d):
    s, y = k.slide(d, "Now in Colab",
                   "Sekarang kita pindah ke notebook s4_cleaning_day. Latihannya naik seperti tangga: dua tebakan, dua "
                   "isian, satu bug yang harus diperbaiki, lima kode yang kamu tulis sendiri, dan satu kasus gudang. Di "
                   "akhir, simpan sales_clean.csv. Dua latihan ekstra untuk PR. Siap mulai?", seconds=40)
    k.ladder(d, s, M, 1.85, 8.0, 3.6, [("Predict", 2), ("Fill in", 2), ("Fix it", 1), ("Write it", 5),
                                       ("Case", 1)])
    d.text(s, 9.3, 1.9, 3.43, 4.2,
           [{"text": "Notebook", "bold": True, "color": ORANGE_TEXT, "size": 16},
            {"text": "s4_cleaning_day", "after": 14},
            {"text": "Save", "bold": True, "color": ORANGE_TEXT, "size": 16},
            {"text": "sales_clean.csv", "after": 14},
            {"text": "Homework", "bold": True, "color": ORANGE_TEXT, "size": 16},
            {"text": "2 extras", "after": 14},
            {"text": "Recall", "bold": True, "color": ORANGE_TEXT, "size": 16},
            {"text": "Fri 27 to Sun 29"}],
           size=20, color=NAVY, name="side")


def thanks(d):
    k.thanks_next(d, "Terima kasih untuk hari ini. Kamu sudah membersihkan data asli dan menghitung penjualan yang "
                     "sebenarnya. Titik empat sudah selesai, dan berikutnya titik lima: mencari produk bintang dari tabel "
                     "bersih yang kamu simpan hari ini. Jangan lupa recall Jumat sampai Minggu dan dua latihan ekstra.")


def build():
    d = k.lecture_deck(4)
    for make in (cover, goals, dataframe, read_file, look_first, dtypes, rename, missing, missing_choice, mask,
                 filtering, combine, text_tools, rules, cleaning_log, new_table, new_columns, dates, sort_count,
                 summary_numbers, saving, case_study, toolkit, colab, thanks):
        make(d)
    k.save(d, OUT)


if __name__ == "__main__":
    build()
