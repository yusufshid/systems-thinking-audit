# Feedback Loops

Mekanisme di mana output sebuah sistem memengaruhi kembali inputnya. Konsep inti dalam [[systems-thinking]].

## Dua jenis dasar
- **Reinforcing loop** (memperkuat) — perubahan di satu arah memicu perubahan lebih lanjut ke arah yang sama, sehingga efeknya membesar. Contoh: bunga majemuk, atau kesalahan yang menumpuk karena tidak ada koreksi.
- **Balancing loop** (menstabilkan) — sistem mendeteksi penyimpangan dari target lalu menariknya kembali. Contoh: thermostat, atau validator yang menolak output salah dan meminta agent mencoba lagi.

## Elemen penting sebuah loop
- **Sinyal** — apa yang diukur/dideteksi sebagai indikator penyimpangan
- **Delay** — jarak waktu antara aksi dan koreksi sampai kembali. Delay yang panjang membuat penyimpangan menjalar lebih jauh sebelum terkoreksi.
- **Gain** — seberapa besar respons koreksi terhadap sinyal. Gain berlebihan membuat sistem *oscillate* (overshoot berulang), gain terlalu kecil membuat koreksi lambat/tidak efektif.

## Kenapa penting di sistem kompleks
Kebanyakan perilaku sistem yang sulit dijelaskan (drift, eskalasi, osilasi) adalah hasil dari struktur feedback loop-nya, bukan dari satu bagian yang "salah". Mengubah loop (menambah balancing loop, mempercepat delay, menurunkan gain) sering lebih efektif daripada memperbaiki satu komponen.

## Terkait
- [[systems-thinking]]
- [[agentic-ai]]
- [[mendesain-feedback-loop]]
- [[leverage-points]]
