"""Build the S2 deck: Shelves, cards and choices."""
from pathlib import Path

import deckkit as k

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "sessions" / "s02_shelves_cards_choices" / "deck.pptx"


def build():
    d = k.new_deck()

    k.cover(d, "Shelves, cards and choices", 2, "Wed 18 Nov 2026",
            "Halo, selamat datang di sesi kedua. Hari ini kita simpan banyak angka di satu tempat, lalu menulis satu "
            "aturan kecil untuk menilai setiap baris pesanan. Kamu yang mengetik semua kodenya, saya menemani. Anggap "
            "sesi ini seperti menata rak: satu rak berisi banyak kotak, dan kita ingin tahu kotak mana yang besar. "
            "Batasnya, Python tidak mengingat apa yang kamu ubah di kepala; setiap perubahan harus ditulis di sel. "
            "Sudah siap mulai dari satu baris pesanan?",
            seconds=20)

    k.question(d, "Which order lines are big?",
               "Pertanyaan hari ini: baris pesanan mana yang besar? Datanya mencatat baris, bukan satu invoice utuh, "
               "jadi besar artinya satu baris yang besar. Anggap seperti menimbang satu kotak di rak, bukan seluruh "
               "truk. Batasnya, satu baris besar belum tentu satu invoice besar, karena satu invoice bisa berisi banyak "
               "baris kecil. Menurutmu, baris dengan 8 unit itu besar atau kecil?",
               seconds=40)

    k.concept(d, "A list holds a row of values",
              "A row of bins on one shelf.",
              "One column.",
              "The first bin is number zero.",
              ['quantities = [6, 6, 8, 6, 6, 2, 6]',
               'print(quantities[0])',
               'print(quantities[2])',
               'print(quantities[-1])'],
              "List itu satu baris rak berisi banyak kotak, dan setiap kotak punya nomor. Kita pakai tujuh angka "
              "quantity dari file asli: 6, 6, 8, 6, 6, 2, 6. Nomor pertama adalah 0, jadi kotak terakhir ada di nomor "
              "6. Batasnya, list menyimpan urutan, bukan nama, jadi kita harus hafal nomornya. Kalau nomornya keluar "
              "dari isi rak, Python memberi IndexError. Coba tebak, quantities[2] berisi angka berapa?",
              seconds=75, code_size=14)

    k.concept(d, "len, sum, min and max measure the list",
              "Count the boxes, add them, find the smallest and largest.",
              "COUNT, SUM, MIN, MAX.",
              "Same idea, new spelling.",
              ['print(len(quantities))',
               'print(sum(quantities))',
               'print(min(quantities))',
               'print(max(quantities))'],
              "Empat alat hitung cepat: len menghitung isi, sum menjumlahkan, min mengambil yang terkecil, dan max "
              "yang terbesar. Hasilnya len 7, sum 40, min 2, dan max 8. Anggap seperti menghitung kotak, menjumlah "
              "isinya, lalu mencari kotak paling ringan dan paling berat. Batasnya, nama fungsinya sama dengan COUNT, "
              "SUM, MIN, MAX di Excel, tetapi Python memakai huruf kecil semua. Kalau satu baris baru kita tambahkan, "
              "angka mana yang berubah?",
              seconds=70, code_size=14)

    k.concept(d, "A dict is a product card with labels",
              "A product card: field name to value.",
              "One row with headers.",
              "Look up by name, not by position.",
              ['order_line = {',
               '    "quantity": 6,',
               '    "country": "United Kingdom",',
               '}',
               'print(order_line["quantity"])'],
              "Dict itu seperti kartu produk: setiap label punya nilai. Di kartu ini ada stock_code, quantity, price, "
              "dan country. Kita mencari nilai lewat namanya, bukan lewat urutan seperti list. Anggap seperti satu baris "
              "Excel dengan nama kolom di atasnya. Batasnya, kalau nama label salah ketik, muncul KeyError, bukan angka "
              "nol. Coba sebutkan satu label yang ada di kartu ini.",
              seconds=75, code_size=14)

    k.concept(d, "A comparison asks a yes or no question",
              "Is this more than that?",
              "=A2>10",
              "= stores a value. == asks a question.",
              ['quantity = order_line["quantity"]',
               'is_big = quantity >= 100',
               'print(is_big)',
               'print(quantity == 6)'],
              "Perbandingan itu pertanyaan yang jawabannya True atau False. quantity >= 100 bertanya apakah jumlahnya "
              "seratus atau lebih, lalu jawabannya kita simpan di is_big. Anggap seperti bertanya ke kotak: isi kamu "
              "lebih dari seratus? Batasnya, satu tanda sama dengan menyimpan nilai, dua tanda sama dengan bertanya; "
              "kalau tertukar, hasilnya membingungkan. Coba tebak, quantity == 6 hasilnya True atau False?",
              seconds=70, code_size=14)

    k.concept(d, "A packing rule becomes if, elif, else",
              "A packing rule.",
              "=IF(...)",
              "The indent is part of the rule.",
              ['if quantity >= 100:',
               '    print("Big")',
               'elif quantity >= 12:',
               '    print("Medium")',
               'else:',
               '    print("Small")'],
              "Sekarang aturannya: kalau quantity 100 atau lebih, cetak Big order line. Kalau 12 atau lebih, Medium. "
              "Selain itu, Small. Hanya satu cabang yang jalan, dari atas ke bawah, dan cabang pertama yang cocok yang "
              "dipakai. Anggap seperti aturan packing: kotak besar untuk pesanan besar, kotak kecil untuk sisanya. "
              "Batasnya, indentasi adalah bagian dari aturan; kalau menjoroknya salah, Python tidak tahu mana yang di "
              "dalam if. Angka 100 dan 12 hanya contoh untuk belajar, bukan aturan bisnis. Kalau quantity 12, aturan "
              "mana yang jalan?",
              seconds=80, code_size=14)

    k.now_in_colab(d, "s2_shelves_cards.ipynb",
                   "Sekarang kita pindah ke Colab, ke notebook s2_shelves_cards. Buka dari Drive, lalu ketik setiap "
                   "sel sendiri. Kita mulai dari list, lalu len, dict, perbandingan, dan if. Anggap notebook seperti "
                   "meja kerja: semua alat tadi ada di situ. Batasnya, urutan sel penting, jadi jalankan dari atas ke "
                   "bawah. Siap membuka notebooknya?",
                   seconds=30,
                   items=[("Notebook", "s2_shelves_cards.ipynb"),
                          ("In class", "List, len, dict, comparison, if"),
                          ("Before you type", "Predict the output first")])

    k.recap(d, [("Store a row", "a list of quantities"),
                ("Measure it", "len, sum, min and max"),
                ("Make a choice", "if, elif, else")],
            "Tiga hal yang sekarang bisa kamu lakukan: menyimpan baris di list, mengukurnya dengan len, sum, min, dan "
            "max, lalu memilih dengan if. Anggap ketiganya sebagai alat di meja kerja yang akan kita pakai sampai sesi "
            "sepuluh. Batasnya, semuanya hanya bekerja pada data yang sudah kita tulis; tidak ada yang otomatis seperti "
            "di Excel. Dari tiga tadi, mana yang paling ingin kamu ulang sekali lagi?",
            seconds=35)

    k.homework(d, ["Add rows 8 to 10 from the handout",
                   "Redo len, sum, min and max",
                   "Write one if rule about prices"],
               ["Three questions a day",
                "Thursday to Sunday"],
               "PR: tambahkan baris 8 sampai 10 dari handout sesi satu ke list, lalu ulangi len, sum, min, dan max. "
               "Tulis juga satu aturan if tentang harga. Recall mulai Kamis sampai Minggu, tiga pertanyaan tiap hari. "
               "Anggap PR ini sebagai mengulang gerakan yang sama supaya hafal, bukan ujian. Batasnya, kalau macet, "
               "buka lagi slide list dan if; tidak perlu menebak. Kapan kamu punya waktu tenang untuk mengerjakannya?",
               seconds=40)

    k.save(d, OUT)


if __name__ == "__main__":
    build()
