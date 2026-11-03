"""Build the S8 deck: Detective work."""
from pathlib import Path

import deckkit as k

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "sessions" / "s08_detective_work" / "deck.pptx"


def build():
    d = k.new_deck()

    k.cover(d, "Detective work", 8, "Thu 10 Dec 2026",
            "Hari ini hampir semuanya kerja proyek. Saya hanya memberi petunjuk, dan kamu yang mengetik.",
            seconds=15)

    k.question(d, "Your own question",
               "Pertanyaan hari ini adalah pertanyaanmu sendiri. Mulai dengan case hunt dua menit, lalu proyek.",
               seconds=20, kicker="Today's question")

    k.cards(d, "Case hunt: two minutes",
            [("The case", None, "What is the problem?"),
             ("The data", None, "What would show it?"),
             ("The link", None, "How does it connect to our data?")],
            notes="Presentasikan kasusmu dalam dua menit: masalahnya, data apa yang akan menunjukkannya, dan satu "
                  "kaitan dengan data kita. Tidak ada jawaban benar atau salah; ini latihan melihat masalah nyata "
                  "lewat data.",
            seconds=40, cols=3)

    k.cards(d, "Project checklist",
            [("Plan", None, "One sentence question, columns, steps."),
             ("Check", None, "Print the row count after each filter."),
             ("Chart", None, "Title says the finding.")],
            notes="Pegang tiga hal ini sepanjang sesi. Rencana: pertanyaan satu kalimat, kolom yang diperlukan, "
                  "langkah-langkahnya. Cek: tampilkan jumlah baris setelah tiap filter. Grafik: judul menyatakan "
                  "temuan. Saya hanya memberi petunjuk bertahap.",
            seconds=35, cols=3)

    k.cards(d, "Check one number a second way",
            [("Filter and sum", None, "Repeat it with a filter."),
             ("Excel", None, "Try a small piece in Excel."),
             ("Write it down", None, "Say how you checked.")],
            notes="Sebelum membuat grafik, periksa satu angka dengan cara kedua. Bisa dengan filter dan sum, atau "
                  "dengan Excel pada sebagian kecil data. Tuliskan caranya. Kebiasaan ini membuat temuanmu bisa "
                  "dipercaya.",
            seconds=35, cols=3)

    k.now_in_colab(d, "s8_detective_work.ipynb",
                   "Sekarang buka notebook s8_detective_work ini dan mulai bekerja. Kamu yang mengetik, saya hanya memberi petunjuk.",
                   seconds=15,
                   items=[("Notebook", "s8_detective_work.ipynb"),
                          ("In class", "Project work, hints only"),
                          ("Last 5 minutes", "What I found so far")])

    k.cards(d, "What I found so far",
            [("Answer", None, "One sentence."),
             ("Evidence", None, "One number."),
             ("Next", None, "One step.")],
            notes="Lima menit terakhir: tiga kalimat tentang apa yang sudah kamu temukan. Jawaban, bukti, dan langkah "
                  "berikutnya. PR: lanjutkan analisis, buat akun GitHub dan repository publik yang kosong dengan "
                  "github_guide.md, lalu selesaikan case hunt kalau belum. Recall Jumat sampai Minggu.",
            seconds=40, cols=3)

    k.save(d, OUT)


if __name__ == "__main__":
    build()
