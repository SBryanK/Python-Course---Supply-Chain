"""Build the S1 deck: Hello, Python."""
from pathlib import Path

import deckkit as k

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "sessions" / "s01_hello_python" / "deck.pptx"


def build():
    d = k.new_deck()

    k.cover(d, "Hello, Python", 1, "Mon 16 Nov 2026",
            "Halo, selamat datang di sesi pertama. Hari ini kita mulai dari satu baris pesanan: berapa nilainya. "
            "Kita akan membuka Colab, menulis beberapa baris Python, dan kamu yang mengetik semua kodenya.",
            seconds=20)

    k.cards(d, "Ten sessions, one picture",
            [("S1 16 Nov", None, "Hello"),
             ("S2 18 Nov", None, "Shelves"),
             ("S3 23 Nov", None, "Loops"),
             ("S4 26 Nov", None, "Cleaning"),
             ("S5 30 Nov", None, "Stars"),
             ("S6 3 Dec", None, "Charts"),
             ("S7 7 Dec", None, "Tools"),
             ("S8 10 Dec", None, "Detective"),
             ("S9 14 Dec", None, "Publish"),
             ("S10 17 Dec", None, "Showtime")],
            notes="Ini peta sepuluh sesi. Kita mulai dari satu baris, lalu daftar, loop, dan pandas. Sesi 4 hari "
                  "pembersihan data. Sesi 5 dan 6 analisis dan grafik. Sesi 7 sampai 10 kamu kerjakan proyek sendiri. "
                  "Tiap sesi 35 menit, istirahat 5 menit, lalu 35 menit lagi.",
            seconds=25, cols=5, source="Each session: 35 + 5 + 35 minutes.")

    k.cards(d, "Why Python for supply chain",
            [("Big files", None, "Excel slows down when the file gets large."),
             ("Repeat work", None, "One click runs the weekly steps again."),
             ("Show your work", None, "Every step stays visible for your manager.")],
            notes="Kenapa Python? Tiga alasan saja. File Excel yang besar mulai lambat; pekerjaan yang berulang tiap "
                  "minggu bisa dijalankan satu klik; dan setiap langkah terlihat, jadi bisa kamu tunjukkan ke atasan. "
                  "Excel tetap dipakai; Python mengambil bagian yang berat.",
            seconds=22, cols=3)

    s = d.new_slide()
    y = d.title(s, "A five-minute tour of Colab")
    d.steps(s, y + 0.1, [("Open", "The notebook in Drive"),
                         ("Text or code", "Click a cell to see"),
                         ("Run", "Shift and Enter"),
                         ("Order", "Run from the top")])
    d.footer(s)
    d.notes(s, "Ini Colab. Buka notebook dari Drive. Ada kotak teks dan kotak kode. Klik kotak kode, lalu tekan Shift "
               "dan Enter. Jalankan dari atas ke bawah, karena urutan itu penting. Kalau muncul NameError, jalankan "
               "ulang sel di atasnya.", "Bryan", 22)

    k.concept(d, "print shows a value, a variable keeps it",
              "A label on a storage bin.",
              "A named cell.",
              "Nothing shows unless you ask.",
              ['product_name = "WHITE HANGING HEART T-LIGHT HOLDER"',
               'quantity = 6',
               'print(product_name)',
               'print(quantity)'],
              "print itu seperti membaca label keras-keras. Variabel itu label di rak: kamu simpan nilai di situ dan "
              "panggil lagi dengan namanya. Batasnya: Python tidak menampilkan apa pun kalau tidak diminta. Coba ganti "
              "quantity menjadi 7, jalankan, dan lihat apa yang berubah.",
              seconds=75, code_size=14)

    k.concept(d, "Numbers and text are different types",
              "Counting boxes, weighing goods, a product name.",
              "Number format or text format.",
              '"5" is text. Python will not add it to a number.',
              ['quantity = 6',
               'unit_price = 2.55',
               'print(type(quantity))',
               'print(type(unit_price))',
               'print(type(product_name))'],
              "Ada tiga tipe di sesi ini: int untuk hitungan, float untuk berat atau uang, str untuk nama produk. "
              "Excel membedakan format angka dan teks; Python membedakan tipe. Batasnya: \"5\" itu teks, bukan angka. "
              "Kalau kamu jumlahkan dengan angka, Python akan protes.",
              seconds=70, code_size=14)

    k.concept(d, "Multiply, round, then write the sentence",
              "Adding up a receipt.",
              "=B2*C2 and ROUND.",
              "6 * 2.55 prints 15.299999999999999. Round money.",
              ['sales_value = quantity * unit_price',
               'print(sales_value)',
               'print(round(sales_value, 2))',
               'print(f"{quantity} units: {round(sales_value, 2)} pounds")'],
              "Sekarang kita hitung nilai satu baris: quantity kali unit_price. Hasilnya 15.299999999999999 karena "
              "komputer menyimpan desimal dalam biner. Batasnya: jangan tampilkan angka panjang ke manajer; bulatkan "
              "uang di akhir. Lalu tulis kalimat dengan f-string.",
              seconds=80, code_size=14)

    k.errors_slide(d, "Three errors you will meet",
                   [["Error", "What it means"],
                    ["NameError", "The name is not defined"],
                    ["SyntaxError", "A bracket or quote is missing"],
                    ["TypeError", "Text plus a number"]],
                   "Read the last line first. It names the error.",
                   "Tiga error yang paling sering: NameError, biasanya salah ketik nama; SyntaxError, biasanya kurung "
                   "atau kutip kurang; TypeError, teks ditambah angka. Batasnya: pesan error panjang, tetapi jawabannya "
                   "ada di baris terakhir. Baca dari bawah.",
                   seconds=55)

    k.now_in_colab(d, "s1_hello_python.ipynb",
                   "Sekarang kita pindah ke Colab: notebook s1_hello_python. Kamu mengetik sendiri setiap sel. PR: "
                   "selesaikan worksheet, buat tiga error dengan sengaja, lalu tulis satu f-string tentang baris 8 "
                   "sampai 10 di handout. Recall tiga pertanyaan untuk Selasa.",
                   seconds=25,
                   items=[("Notebook", "s1_hello_python.ipynb"),
                          ("Homework", "Worksheet, then make the three errors"),
                          ("Recall", "Three questions for Tuesday")])

    k.save(d, OUT)


if __name__ == "__main__":
    build()
