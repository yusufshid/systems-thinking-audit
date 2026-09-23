# Mendesain Feedback Loop pada AI Agent

Penerapan praktis [[feedback-loops]] untuk sistem [[agentic-ai]]. Merancang feedback loop berarti menentukan: apa yang diukur, siapa/apa yang mengoreksi, dan seberapa cepat koreksi itu sampai kembali ke agent.

## 1. Tentukan jenis loop yang dibutuhkan
- **Balancing loop** (menstabilkan) — dominan untuk sistem produksi: mendeteksi penyimpangan lalu menariknya kembali ke target. Contoh: validator menolak output agent yang salah format, agent mencoba lagi.
- **Reinforcing loop** (memperkuat) — dipakai sengaja untuk eksplorasi/pembelajaran, tapi berbahaya kalau jadi efek samping desain yang lemah (error menumpuk tanpa koreksi).

## 2. Sumber sinyal koreksi
- **Self-check** — agent mengevaluasi outputnya sendiri. Murah, tapi lemah karena blind spot sama dengan saat generate.
- **Verifier/reviewer terpisah** — proses independen yang mengecek hasil. Lebih kuat karena tidak berbagi bias yang sama.
- **Environment ground truth** — hasil eksekusi nyata (test lulus/gagal, command error). Paling objektif, tidak bisa dihalusinasi.
- **Human-in-the-loop** — paling akurat untuk preferensi, tapi paling lambat dan mahal per-siklus.

## 3. Tempatkan loop sedekat mungkin ke sumber kesalahan
Prinsip root-cause: taruh pemeriksaan di titik kesalahan biasa muncul, bukan di ujung setelah beberapa langkah lagi. Semakin jauh jaraknya, semakin mahal melacak balik penyebabnya.

## 4. Atur delay dan gain
- **Delay** disesuaikan dengan biaya kesalahan: aksi berisiko tinggi (hapus data, kirim pesan) butuh loop cepat/sinkron; aksi murah dan reversibel bisa pakai loop lambat (audit setelah batch).
- **Gain jangan berlebihan** — koreksi yang terlalu agresif merespons tiap sinyal kecil membuat sistem *oscillate*. Beri ambang batas sebelum retry.

## 5. Hindari loop yang menipu diri sendiri
Verifier yang dijalankan oleh agent/model/prompt yang sama dengan pembuat output sering cuma mengonfirmasi asumsi yang sama, bukan menemukan kesalahan baru. Sinyal baik biasanya dari sumber independen: eksekusi nyata, agent lain dengan sudut pandang berbeda, atau manusia.

## 6. Loop bertingkat (multi-level)
Sistem matang punya beberapa loop berlapis dengan kecepatan berbeda:
- Loop cepat: validasi syntax/schema tiap langkah
- Loop menengah: reviewer agent per task selesai
- Loop lambat: evaluasi performa agregat lintas sesi → dipakai untuk revisi prompt/paradigma ([[paradigma-mental-model]])

Loop cepat memperbaiki eksekusi; loop lambat memperbaiki struktur dan tujuan sistem itu sendiri — lihat [[leverage-points]].

## Terkait
- [[feedback-loops]]
- [[agentic-ai]]
- [[leverage-points]]
- [[paradigma-mental-model]]
