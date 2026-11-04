"""Build the S5 deck: Who are the star products?"""
import json
from pathlib import Path

import deckkit as k

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "sessions" / "s05_star_products" / "deck.pptx"
DATA = json.loads((ROOT / "tools" / "3_slides" / "deck_data.json").read_text())


def draw_abc(deck, slide, x, y, w, h):
    labels = ["Class A", "Class B", "Class C"]
    shares = [DATA["abc"][c]["pct_revenue"] / 100 for c in "ABC"]
    chart = deck.bar_chart(slide, x, y, w, h, labels, {"Share of revenue": shares},
                           number_format="0.0%", legend=False)
    chart.value_axis.maximum_scale = 1.0
    chart.value_axis.minimum_scale = 0.0
    chart.value_axis.tick_labels.number_format = "0%"
    chart.value_axis.tick_labels.number_format_is_linked = False


def build():
    d = k.new_deck()

    k.cover(d, "Who are the star products?", 5, "Mon 30 Nov 2026",
            "Hari ini kita cari produk yang paling banyak memberi uang. Setelah itu ada cold test: dua puluh menit, "
            "catatan boleh dibuka, saya diam. Ini bukan ujian besar; ini cara kita lihat apa yang sudah menempel.",
            seconds=20)

    k.question(d, "Which products bring most of the money?", 
               "Pertanyaannya sederhana: dari 3.066 produk, mana yang paling banyak menyumbang penjualan? Jawabannya "
               "akan kita pakai untuk memilih produk mana yang harus dijaga stoknya.",
               seconds=35)

    k.concept(d, "groupby sorts the receipts into piles",
              "Receipts sorted into piles, then each pile added up.",
              "A PivotTable.",
              "The result has a row label; reset_index flattens it.",
              ['by_product = sales_clean.groupby("stock_code")["revenue"]',
               'by_product = by_product.sum()',
               'by_product = by_product.sort_values(ascending=False)',
               'by_product.head()'],
              "groupby itu seperti memilah struk ke dalam tumpukan, satu tumpukan per produk, lalu menjumlahkan tiap "
              "tumpukan. Excel menyebutnya PivotTable. Batasnya: hasilnya membawa kolom label tambahan; reset_index "
              "membuatnya kembali jadi tabel biasa. Jadi, tumpukan mana yang paling besar?",
              seconds=80, code_size=14)

    k.concept(d, "A running total needs a sorted list first",
              "A running total on a receipt roll.",
              "=SUM($B$2:B2) dragged down.",
              "Sort first, or the running total means nothing.",
              ['total = by_product["revenue"].sum()',
               'by_product["cumulative"] = by_product["revenue"].cumsum()',
               'by_product["share"] = by_product["cumulative"] / total'],
              "Sekarang kita tambahkan berjalan: produk pertama, lalu dua produk pertama, lalu tiga, dan seterusnya. "
              "Di Excel ini =SUM($B$2:B2) yang di-drag ke bawah. Batasnya: kalau tidak diurutkan dulu, total berjalan "
              "tidak ada artinya. Berapa persen produk yang perlu kita jaga?",
              seconds=70, code_size=14)

    k.concept(d, "ABC puts products into groups",
              "A few items hold most money.",
              "Sort, running %, IF.",
              "A habit, not a law.",
              ['def abc_class(cumulative_share):',
               '    if cumulative_share <= 0.80:',
               '        return "A"',
               '    elif cumulative_share <= 0.95:',
               '        return "B"',
               '    return "C"'],
              "ABC itu kebiasaan lama di gudang: kelompok A yang paling penting, B sedang, C banyak tetapi kecil. "
              "Kita pakai aturan 80 persen dan 95 persen. Batasnya: 80/95 itu kebiasaan, bukan hukum alam. Menurutmu, "
              "produk kelas C perlu tempat sebesar kelas A?",
              seconds=75, code_size=14)

    k.finding_chart(d, "About 1 in 5 products bring 80% of the money",
                    draw_abc,
                    [("80%", "of revenue from class A"),
                     ("21.9%", "of products are class A")],
                    "Angka besar di kiri ini temuannya: sekitar satu dari lima produk membawa 80 persen uang. Kelas A "
                    "hanya 671 dari 3.066 produk. Jadi jangan perlakukan semua produk sama rata. Angka mana yang paling "
                    "mengejutkan untukmu?",
                    source="Clean slice, Dec 2010 to Feb 2011", seconds=50)

    k.now_in_colab(d, "s5_star_products.ipynb",
                   "Sekarang buka notebook s5_star_products. Kamu kerjakan latihan singkat, lalu cold test dua puluh "
                   "menit. Catatan boleh dibuka, saya diam. Setelah itu kita lihat satu solusi bersama.",
                   seconds=25,
                   items=[("Notebook", "s5_star_products.ipynb"),
                          ("Cold test", "20 minutes, notes allowed"),
                          ("After", "One solution together")])

    k.recap(d, [("Rank products", "groupby and sort"),
                ("See the concentration", "a running share"),
                ("Classify", "A, B, C with a function")],
            "Tiga hal yang sekarang bisa kamu lakukan: mengurutkan produk dengan groupby, melihat konsentrasi dengan "
            "running share, dan mengelompokkan produk dengan satu function. Sesi berikutnya kita gambar.",
            seconds=30)

    k.homework(d, ["Finish the copy-alongs", "Write your own ABC sentence"],
               ["Three questions Tuesday", "Three questions Wednesday"],
               "PR singkat: selesaikan copy-along dan tulis satu kalimat ABC dengan bahasamu sendiri. Recall Selasa "
               "dan Rabu, tiga pertanyaan tiap hari. Satu pertanyaan yang masih mengganjal?",
               seconds=30)

    k.save(d, OUT)


if __name__ == "__main__":
    build()
