"""Build the S9 deck: Polish and publish."""
from pathlib import Path

import deckkit as k

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "sessions" / "s09_polish_publish" / "deck.pptx"


def build():
    d = k.new_deck()

    k.cover(d, "Polish and publish", 9, "Mon 14 Dec 2026",
            "Hari ini kita rapikan proyekmu, menyimpannya di GitHub, dan mulai menyusun tiga slide.",
            seconds=15)

    k.question(d, "Can you say your finding in three sentences?",
               "Ini yang kita latih hari ini. Kalau temuanmu tidak bisa dijelaskan dalam tiga kalimat, mungkin belum cukup jelas. Tiga kalimat itu: "
               "jawaban, bukti, dan rekomendasi. Jawaban dulu.",
               seconds=35)

    k.cards(d, "Final chart checklist",
            [("Title", None, "It says the finding."),
             ("Labels", None, "Both axes, with units."),
             ("One message", None, "One chart, one idea.")],
            notes="Sebelum chart masuk slide, cek tiga hal: judul menyatakan temuan, kedua sumbu berlabel dengan "
                  "satuan, dan satu grafik hanya membawa satu pesan.",
            seconds=35, cols=3)

    s = d.new_slide()
    y = d.title(s, "GitHub in the browser")
    d.steps(s, y + 0.1, [("Save", "File > Save a copy in GitHub"),
                         ("README", "Add a file, README.md"),
                         ("Commit", "Click Commit changes"),
                         ("Check", "Open it in a private window")])
    d.footer(s)
    d.notes(s, "Kamu sudah punya akun dan repository kosong dari PR. Sekarang kamu yang klik semuanya. Simpan notebook "
               "dari Colab ke GitHub, buat README.md, lalu klik Commit changes. Cek dengan membuka link repository di "
               "jendela private. Repository ini boleh publik karena datanya publik dan tidak ada data pribadi.",
            "Bryan", 50)

    k.code_slide(d, "The README has four parts",
                 "Question, data credit, finding, how to run.",
                 ['# My project title',
                  '**Question:** ...',
                  '**Data:** Chen, D. (2012).',
                  '  Online Retail II. UCI.',
                  '**Finding:** ...',
                  '**How to run:** ...'],
                 "README ini halaman depan repository untuk kamu. Empat bagian: pertanyaan, kredit data, temuan, dan cara "
                 "menjalankan. Kredit data wajib karena lisensinya CC BY 4.0. Kutipannya ada di template.",
                 seconds=45, code_size=14)

    k.cards(d, "Your three slides",
            [("Question", None, "One sentence."),
             ("Finding", None, "One chart, one big number."),
             ("Recommendation", None, "What a manager should do.")],
            notes="Tiga slide isi: pertanyaan, temuan, rekomendasi, ditambah sampul dan penutup dari template. Satu "
                  "grafik per slide. Sebut angka dengan sederhana, misalnya sekitar satu dari lima produk.",
            seconds=40, cols=3)

    k.cards(d, "Reflection, due before Session 10",
            [("Show a cell", None, "What you can do now."),
             ("Mistake", None, "The biggest one, and the fix."),
             ("Next 30 days", None, "Your plan.")],
            notes="Refleksi satu halaman dengan enam pertanyaan; template ada di course home. Jawab jujur, dan "
                  "tunjukkan satu sel kode sebagai bukti. PR: selesaikan slide, latihan presentasi sekali dengan "
                  "suara keras, dan tulis refleksi. Recall Selasa dan Rabu.",
            seconds=35, cols=3)

    k.save(d, OUT)


if __name__ == "__main__":
    build()
