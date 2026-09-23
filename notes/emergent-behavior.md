# Emergent Behavior pada AI Agent

Perilaku tingkat sistem yang tidak bisa ditelusuri langsung ke satu komponen — lahir dari **interaksi** antar bagian. Konsep dari [[systems-thinking]], relevan untuk [[agentic-ai]].

## Mekanisme kemunculannya

1. **Interaksi antar banyak langkah (single agent)** — akumulasi keputusan lokal yang tiap-tiapnya "wajar" bisa menghasilkan strategi global yang tidak pernah eksplisit diprogram, murni karena itu jalur termudah dari serangkaian keputusan lokal.

2. **Interaksi antar multi-agent** — perilaku sistem muncul dari cara agent saling merespons, bukan dari desain individual. Bisa saling menunggu, saling redundant, atau saling menguatkan bias yang sama karena berbagi model/prompt dasar.

3. **Feedback loop yang tidak disengaja** — lihat [[feedback-loops]]. Output satu langkah masuk lagi jadi context langkah berikutnya (memory, riwayat, hasil tool), membentuk loop bawaan yang bisa jadi reinforcing tanpa direncanakan: kesalahan kecil di awal terbawa dan diperkuat di tiap langkah berikutnya.

4. **Skala dan kombinatorik** — semakin banyak tools/agent/langkah, jumlah kombinasi interaksi tumbuh eksponensial. Pada skala besar, sebagian kombinasi menghasilkan perilaku yang tidak pernah dibayangkan perancangnya — kompleksitas perilaku melampaui kompleksitas aturan penyusunnya.

5. **Tekanan optimasi tidak langsung** — kalau agent dioptimasi terhadap proxy metric (misal "jumlah task selesai" bukan "task selesai benar"), dia bisa menemukan strategi yang secara teknis memenuhi metrik tapi menyimpang dari niat asli. Terkait [[leverage-points]] soal tujuan yang sesungguhnya dioptimasi vs yang tertulis.

6. **Kapasitas laten model dasar** — LLM sudah dilatih dengan kapasitas reasoning, planning, dan pattern-matching luas dari data training ([[paradigma-mental-model]] level training). Saat dipasangkan dengan tools dan loop otonom, kapasitas laten itu "diaktifkan" jadi perilaku baru yang tidak eksplisit didesain siapa pun yang membangun sistem agent-nya.

## Intinya
Emergence muncul dari kombinasi banyak bagian sederhana + interaksi berulang + feedback loop — bukan dari satu bagian yang "pintar" atau "dirancang untuk itu". Implikasinya: desain sistem agentic harus fokus ke struktur interaksi ([[leverage-points]]), bukan cuma memperbaiki satu agent secara terisolasi.

## Terkait
- [[systems-thinking]]
- [[agentic-ai]]
- [[feedback-loops]]
- [[leverage-points]]
- [[paradigma-mental-model]]
