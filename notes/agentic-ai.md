# Systems Thinking di Agentic AI

Penerapan [[systems-thinking]] pada desain dan debugging sistem agentic (AI agent yang beraksi, pakai tools, dan berinteraksi dengan lingkungan).

## Agent sebagai bagian dari sistem
Satu agent LLM jarang berdiri sendiri — berinteraksi dengan tools, memory, agent lain, dan lingkungan (API, filesystem, user). Loop-nya: input → reasoning → action → observasi hasil → balik ke reasoning. Optimasi satu bagian saja (misal prompt doang) tanpa lihat feedback loop-nya membuat sistem rapuh.

## Feedback loops
- **Reinforcing loop**: keputusan salah → error masuk lagi ke context → agent makin "yakin" dengan asumsi salah → error menumpuk (contoh: hallucination yang menumpuk di multi-turn tool use).
- **Balancing loop**: ada mekanisme koreksi — validasi output, human-in-the-loop, atau reviewer agent — yang menstabilkan sistem, bukan membiarkannya liar. Lihat [[feedback-loops]].

## Emergent behavior dari multi-agent — lihat [[emergent-behavior]]
Saat beberapa agent kerja bareng (orchestrator + subagent), perilaku sistem sering muncul dari *interaksi antar agent*, bukan dari satu agent yang dirancang pintar sendirian. Bisa saling redundant, saling menunggu, atau saling melengkapi kalau pembagian tanggung jawab jelas.

## Leverage points (ala Donella Meadows) — lihat [[leverage-points]]
Titik pengungkit terkuat di sistem agentic biasanya bukan "tambah lebih banyak tool", tapi:
- **Struktur informasi** — apa yang masuk ke context agent (memory yang salah desain = downstream errors berulang)
- **Aturan sistem** — permission boundaries, kapan agent boleh bertindak otonom vs harus tanya
- **Tujuan yang didefinisikan** — goal yang didefinisikan sempit (optimasi metrik tertentu) sering punya efek samping tak terduga ke bagian sistem lain (mirip reward hacking)

## Debugging jadi soal sistem, bukan baris kode
Kalau agent salah, root cause sering bukan di satu function, tapi di interaksi: prompt + tool schema + memory + urutan pemanggilan. Perbaiki di titik struktural yang dilewati semua path, bukan tambal di satu jalur saja.

## Terkait
- [[systems-thinking]]
- [[feedback-loops]]
