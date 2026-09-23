# Leverage Points

Konsep dari Donella Meadows: titik-titik dalam sebuah sistem tempat perubahan kecil bisa menghasilkan pergeseran besar pada perilaku sistem. Bagian dari [[systems-thinking]]. Hierarki dari leverage terkecil ke terbesar.

## Hierarki (kecil → besar)
1. **Parameter individual** — angka/konstanta (contoh di agentic AI: temperature, jumlah retry, threshold confidence). Paling sering di-tweak, tapi dampaknya kecil kalau struktur di atasnya belum benar.
2. **Feedback loop delays & gains** — seberapa cepat kesalahan terdeteksi dan dikoreksi. Delay lama = penyimpangan makin jauh sebelum dikoreksi.
3. **Struktur informasi** — siapa tahu apa, apa yang mengalir ke mana. Sering jadi leverage paling *actionable*.
4. **Struktur aturan (rules)** — siapa boleh melakukan apa, kapan boleh otonom. Membatasi ruang kemungkinan perilaku tanpa mengontrol tiap keputusan individual.
5. **Tujuan sistem (goal)** — bukan yang tertulis, tapi yang benar-benar dioptimasi/direward.
6. **Paradigma / mental model** (leverage tertinggi) — cara sistem "memahami" tujuannya sendiri. Paling sulit diubah karena tersebar di banyak tempat, tapi mengubahnya menggeser seluruh perilaku sistem. Lihat [[paradigma-mental-model]].

## Penerapan di sistem agentic yang sudah emergent
Lihat [[agentic-ai]]. Saat perilaku sistem sudah muncul dari interaksi banyak agent (tidak bisa ditelusuri linear ke satu keputusan), leverage terbesar biasanya bukan di "agent mana yang salah", tapi di:
- **Goal definition** — apa yang benar-benar dianggap "sukses" oleh sistem
- **Struktur informasi antar agent** — banyak emergent behavior aneh (halusinasi menumpuk, agent saling kontradiksi) sebenarnya soal informasi tidak sinkron, bukan agent kurang pintar

Memperbaiki dua hal ini punya efek menjalar ke seluruh sistem, dibanding menambal satu agent atau satu parameter.

## Terkait
- [[systems-thinking]]
- [[agentic-ai]]
- [[feedback-loops]]
