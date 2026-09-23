# Systems Thinking di Desain Software/Arsitektur

Penerapan [[systems-thinking]] pada desain sistem perangkat lunak: melihat arsitektur sebagai jaringan komponen yang saling memengaruhi, bukan sekadar kumpulan modul terpisah.

## Kenapa relevan
- Perubahan di satu service/modul bisa berdampak tak terduga ke service lain lewat dependency, shared state, atau API contract — mirip efek domino di [[systems-thinking]] secara umum.
- Bug yang sulit dilacak sering muncul dari **interaksi** antar komponen (race condition, urutan pemanggilan, cache yang stale), bukan dari satu baris kode yang salah — lihat [[emergent-behavior]] untuk versi khusus AI agent.
- Coupling yang tersembunyi (dua service yang diam-diam bergantung pada urutan deploy tertentu) adalah bentuk struktur informasi yang tidak terlihat sampai sistem gagal — terkait [[leverage-points]] level struktur informasi.

## Feedback loop dalam arsitektur
- **Balancing**: circuit breaker, health check, auto-scaling — mendeteksi penyimpangan (load tinggi, service down) dan menariknya kembali ke kondisi stabil.
- **Reinforcing yang berbahaya**: retry storm (service down → semua klien retry bersamaan → makin down), atau technical debt yang menumpuk karena tidak pernah dibayar (lihat [[feedback-loops]]).

## Leverage point di arsitektur
Root-cause fix di level arsitektur biasanya berarti memperbaiki **kontrak/interface** (leverage tinggi: struktur informasi dan rules) dibanding menambal satu implementasi (leverage rendah: parameter) — lihat [[leverage-points]].

## Terkait
- [[systems-thinking]]
- [[emergent-behavior]]
- [[leverage-points]]
- [[feedback-loops]]
