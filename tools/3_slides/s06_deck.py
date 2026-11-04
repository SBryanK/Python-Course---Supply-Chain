"""Build the S6 deck: Make the numbers talk."""
import json
from pathlib import Path

import deckkit as k

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "sessions" / "s06_numbers_talk" / "deck.pptx"
DATA = json.loads((ROOT / "tools" / "3_slides" / "deck_data.json").read_text())
MONTHS = {"01": "Jan", "02": "Feb", "03": "Mar", "04": "Apr", "05": "May", "06": "Jun",
          "07": "Jul", "08": "Aug", "09": "Sep", "10": "Oct", "11": "Nov", "12": "Dec"}


def draw_daily(deck, slide, x, y, w, h):
    rows = DATA["daily"]
    cats = []
    for i, row in enumerate(rows):
        d = row["date"]
        # The line has one point per trading day; only every tenth day gets a label,
        # so the axis stays readable on a projected slide.
        cats.append(f"{int(d[8:10])} {MONTHS[d[5:7]]}" if i % 10 == 0 else "")
    vals = [row["revenue"] for row in rows]
    deck.line_chart(slide, x, y, w, h, cats, {"Revenue": vals}, number_format="#,##0",
                    label_every=10, legend=False, widths={"Revenue": 2.5})


def build():
    d = k.new_deck()

    k.cover(d, "Make the numbers talk", 6, "Thu 3 Dec 2026",
            "Hari ini kita ubah angka jadi gambar. Satu grafik yang jelas lebih berguna daripada sepuluh tabel. Kita "
            "akan belajar tiga hal: menggabungkan tabel, membuat grafik, dan memberi judul yang langsung mengatakan "
            "temuannya.",
            seconds=20)

    k.question(d, "How do we show the finding so a manager gets it in five seconds?",
               "Manajer tidak akan membaca tabel kita. Dia melihat satu gambar sebentar, lalu mengambil keputusan. "
               "Jadi pertanyaannya: gambar apa yang langsung menjawab temuannya?",
               seconds=35)

    k.concept(d, "A merge adds columns from another table",
              "Matching a packing list to the product catalogue.",
              "VLOOKUP or XLOOKUP.",
              "Count rows before and after.",
              ['names = sales_clean[["stock_code", "description"]]',
               'names = names.drop_duplicates(subset="stock_code")',
               'product_value = product_value.merge(',
               '    names, on="stock_code", how="left")',
               'print(len(product_value))'],
              "merge itu seperti mencocokkan daftar kirim dengan katalog produk. Di Excel kamu pakai VLOOKUP. "
              "Batasnya: hitung jumlah baris sebelum dan sesudah. Kalau kuncinya berulang, tabel bisa membengkak. "
              "Menurutmu, apa yang terjadi kalau satu kode punya dua nama?",
              seconds=80, code_size=14)

    k.table_slide(d, "A repeated name grows the table",
                  [["Step", "Rows"],
                   ["Product table", "3,066"],
                   ["Naive merge", "3,107"],
                   ["After dedupe", "3,066"]],
                  "Di data kita ada 40 kode dengan dua nama. Merge pertama menambah 41 baris. Kita temukan, lalu "
                  "rapikan tabel nama sebelum merge lagi. Ini pelajaran penting: selalu cek jumlah baris.",
                  seconds=60,
                  below="40 product codes have two names. That adds 41 rows.",
                  col_widths=[5.0, 2.4],
                  highlight=[(2, 1)])

    k.concept(d, "A chart is a few lines of code",
              "Drawing a chart by hand.",
              "Insert Chart, then edit each part.",
              "Every chart needs a title and axis labels.",
              ['plt.barh(top10["description"],',
               '         top10["revenue"])',
               'plt.title("Top 10: 9.6% of revenue")',
               'plt.xlabel("Revenue (pounds)")',
               'plt.show()'],
              "Grafik di matplotlib itu seperti menggambar dengan tangan: satu perintah untuk kanvas, satu untuk "
              "batang, satu untuk judul, satu untuk label. Batasnya: grafik tanpa judul dan label tidak bisa dibaca "
              "orang lain. Coba tebak, mana yang lebih dulu menarik perhatian: angka atau judul?",
              seconds=80, code_size=14)

    k.finding_chart(d, "Revenue peaked in the first week of December",
                    draw_daily,
                    [("81,454.99", "best day, 7 December"),
                     ("68", "trading days")],
                    "Judul grafik ini langsung mengatakan temuannya: puncak penjualan di minggu pertama Desember. "
                    "Garisnya menunjukkan naik turun tiap hari; angka besar menunjukkan hari terbaik. Batasnya: judul "
                    "grafik harus temuannya, bukan jenis grafiknya. Menurutmu, apa judul yang salah untuk grafik ini?",
                    source="Clean slice, Dec 2010 to Feb 2011", seconds=55)

    k.concept(d, "Seaborn styles the same chart",
              "A chart template on top of matplotlib.",
              "Chart styles.",
              "The same titles and labels still work.",
              ['import seaborn as sns',
               'top = country_revenue.head(5).reset_index()',
               'sns.barplot(data=top, x="revenue", y="country")',
               'plt.title("Outside the UK, the Netherlands lead")',
               'plt.show()'],
              "Seaborn itu template di atas matplotlib. Warnanya sudah rapi, tetapi judul dan label tetap tanggung "
              "jawab kita. Batasnya: seaborn hanya mengubah tampilan, bukan pesan. PR: coba pola ini di rumah.",
              seconds=60, code_size=14)

    k.now_in_colab(d, "s6_numbers_talk.ipynb",
                   "Sekarang buka notebook s6_numbers_talk. Kita kerjakan merge, dua grafik, lalu latihan memperbaiki "
                   "grafik. Di akhir, saya jelaskan case hunt untuk PR.",
                   seconds=20,
                   items=[("Notebook", "s6_numbers_talk.ipynb"),
                          ("In class", "Merge, then two charts"),
                          ("At the end", "Case hunt explained")])

    k.recap(d, [("Join tables", "merge and check rows"),
                ("Draw a chart", "title, labels, show"),
                ("Make it readable", "title says the finding")],
            "Tiga hal yang sekarang bisa kamu lakukan: menggabungkan tabel dengan cek baris, membuat grafik dengan "
            "judul dan label, dan menulis judul yang mengatakan temuan. PR: bereskan grafik dan mulai case hunt.",
            seconds=30)

    k.homework(d, ["Finish the top 10 chart", "Try the seaborn pattern", "Start the case hunt", "Install Power BI Desktop"],
               ["Three questions Friday", "Three questions Saturday", "Three questions Sunday"],
               "PR: selesaikan grafik top 10, coba pola seaborn, mulai case hunt, dan install Power BI Desktop untuk "
               "Sesi 7. Recall Jumat sampai Minggu, tiga pertanyaan tiap hari. Apa satu hal yang masih belum jelas?",
               seconds=35)

    k.save(d, OUT)


if __name__ == "__main__":
    build()
