"""Build the S3 deck: Let the loop do the walking."""
from pathlib import Path

import deckkit as k

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "sessions" / "s03_let_loop_walk" / "deck.pptx"


def build():
    d = k.new_deck()

    k.cover(d, "Let the loop do the walking", 3, "Mon 23 Nov 2026",
            "Halo, selamat datang di sesi ketiga. Hari ini kita minta Python menilai semua baris pesanan dengan satu "
            "aturan yang sama. Minggu lalu kita menilai satu baris; sekarang kita ulangi untuk semua baris tanpa "
            "mengetik ulang. Kamu yang mengetik semua kodenya. Anggap seperti berjalan menyusuri rak dan memeriksa "
            "setiap kotak. Batasnya, loop hanya mengulang; aturan penilainya tetap harus kita tulis. Siap mencoba?",
            seconds=20)

    k.question(d, "Can one rule label every order line?",
               "Pertanyaannya: bisakah satu aturan memberi label pada setiap baris pesanan? Kalau ada seratus baris, "
               "mengetik seratus if bukan pilihan yang baik. Anggap seperti satu resep yang dipakai untuk semua "
               "pesanan, bukan resep baru untuk tiap kotak. Batasnya, aturan yang sama harus masuk akal untuk semua "
               "baris; kalau ada pengecualian, kita harus menuliskannya. Menurutmu, apa yang terjadi kalau aturannya "
               "salah untuk satu baris saja?",
               seconds=40)

    k.concept(d, "A for loop walks down the list",
              "Walking down the shelf, checking each bin.",
              "Dragging a formula down.",
              "The body must be indented.",
              ['quantities = [6, 6, 8, 6, 6, 2, 6]',
               'for quantity in quantities:',
               '    print(quantity)',
               'print("Done")'],
              "for loop mengambil satu nilai dari list, menjalankan isi blok, lalu lanjut ke nilai berikutnya sampai "
              "list habis. Kita pakai tujuh quantity dari sesi dua. Anggap seperti berjalan menyusuri rak dan memeriksa "
              "satu kotak di satu waktu. Batasnya, isi loop harus di-indent; kalau indent salah, Python tidak tahu "
              "bagian mana yang diulang. Contoh nyata ada di invoice 540815: barisnya 1.930, 2.000, dan 3.114 unit, dan "
              "loop bisa memeriksa semuanya. Kalau list berisi tujuh angka, berapa kali print di dalam loop jalan?",
              seconds=75, code_size=14)

    k.concept(d, "A function is your own reusable rule",
              "Your own reusable rule.",
              "A named formula.",
              "It does nothing until you call it.",
              ['def order_size(quantity):',
               '    if quantity >= 100:',
               '        return "big"',
               '    elif quantity >= 12:',
               '        return "medium"',
               '    return "small"'],
              "Function itu aturan milikmu sendiri yang diberi nama. Kita tulis def order_size, isinya if dari sesi "
              "dua, dan setiap cabang memakai return. Setelah ditulis, aturan itu tidak melakukan apa-apa sampai kita "
              "panggil. Anggap seperti resep yang disimpan di laci: baru berguna saat dimasak. Batasnya, definisi saja "
              "tidak menjalankan apa pun; function baru bekerja saat dipanggil dengan kurung. Coba tebak, "
              "order_size(2000) mengembalikan apa?",
              seconds=80, code_size=14)

    k.concept(d, "print shows, return hands the answer back",
              "Showing the answer, or handing it over.",
              "The value a formula shows.",
              "print only shows. return hands it back.",
              ['def order_size_printed(quantity):',
               '    print("big")',
               '',
               'print(order_size_printed(1930))',
               'print(order_size(1930))'],
              "Ini beda yang penting, jadi kita bahas pelan. print menunjukkan jawaban di layar, sedangkan return menyerahkan jawaban itu ke baris berikutnya. Kalau "
              "fungsi hanya print, maka print dari panggilannya menghasilkan None. Di slide, versi print mencetak big "
              "lalu None, versi return mencetak big. Anggap seperti membaca jawaban keras-keras dibanding menyerahkan "
              "kertas jawaban. Batasnya, print hanya menunjukkan, return memberi nilai yang bisa dipakai lagi. "
              "Menurutmu, kenapa ada None setelah kata big?",
              seconds=75, code_size=14)

    k.table_slide(d, "Read a traceback from the bottom",
                  [["Read", "What you get"],
                   ["Last line", "The error type and message"],
                   ["Line above", "The line that broke"],
                   ["Higher up", "Who called that line"]],
                  "Error yang kita buat dengan sengaja ini tiga lapis: loop memanggil function, lalu function "
                  "membandingkan teks dengan angka, dan Python berhenti dengan TypeError. Bacanya dari bawah: baris "
                  "terakhir bilang error apa, satu baris di atasnya bilang kode mana yang salah. Anggap seperti "
                  "tumpukan piring: pesan terpenting ada di piring paling bawah. Batasnya, pesan error panjang, tetapi "
                  "jawabannya ada di akhir. Kalau baris terakhir tertulis TypeError, apa artinya sederhananya?",
                  seconds=70,
                  below="Start at the last line. Then walk up.",
                  col_widths=[3.0, 8.4],
                  highlight=[(1, 0), (1, 1)])

    k.now_in_colab(d, "s3_let_loop_walk.ipynb",
                   "Sekarang buka notebook s3_let_loop_walk. Kita tulis loop, lalu function, lalu sengaja membuat satu "
                   "error tiga lapis dan membaca traceback-nya. Anggap notebook sebagai jalur jalan yang kita susuri "
                   "pelan-pelan. Batasnya, jalankan dari atas ke bawah; kalau ada sel yang dilewati, error yang muncul "
                   "bisa menyesatkan. Siap mengetik loop pertamamu?",
                   seconds=30,
                   items=[("Notebook", "s3_let_loop_walk.ipynb"),
                          ("In class", "Loop, function, return, traceback"),
                          ("Real order", "Invoice 540815: 1,930, 2,000, 3,114 units")])

    k.recap(d, [("Walk a list", "for quantity in quantities"),
                ("Wrap a rule", "def order_size(quantity)"),
                ("Hand back an answer", "return, not print")],
            "Tiga hal yang sekarang bisa kamu lakukan: berjalan di list dengan for, membungkus aturan dengan def, dan "
            "menyerahkan jawaban dengan return. Anggap ini tiga gerakan yang akan kita pakai lagi di sesi lima. "
            "Batasnya, loop tidak menghitung total; untuk itu nanti kita pakai alat lain. Dari tiga tadi, mana yang "
            "paling sering kamu lupa indentasinya?",
            seconds=35)

    k.homework(d, ["Write line_value(quantity, price)",
                   "Loop over the 5 handout lines",
                   "Write one function of your own",
                   "Mount Drive once at home"],
               ["Three questions Tuesday 24",
                "Three questions Wednesday 25"],
               "PR: tulis line_value(quantity, price) dengan return, lalu pakai untuk lima baris di handout. Tulis juga "
               "satu function buatanmu sendiri, lalu buka notebook kosong di Colab dan mount Drive sekali, supaya layar "
               "izinnya tidak muncul tiba-tiba di sesi empat. Anggap seperti memanaskan mesin sebelum perjalanan. "
               "Batasnya, kalau mount gagal, ulangi sekali dan terima izinnya; tidak perlu panik. Function buatanmu "
               "tadi tentang apa?",
               seconds=40)

    k.save(d, OUT)


if __name__ == "__main__":
    build()
