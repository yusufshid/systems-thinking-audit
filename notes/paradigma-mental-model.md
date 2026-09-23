# Paradigma / Mental Model Sistem

Level leverage tertinggi dalam [[leverage-points]] — cara sistem "memahami" tujuannya sendiri. Di sistem AI agent, ini bukan disimpan di satu file, tapi tersebar di beberapa lapisan.

## Di mana letaknya (dari paling dalam ke paling mudah diubah)

1. **Training/RLHF model dasar** — cara model "berpikir" tentang tugas yang baik, kapan jujur vs membantu, kapan menolak. Tertanam dari training, bukan konfigurasi. Bahkan developer aplikasi tidak bisa ubah langsung.
2. **System prompt / instruksi sistem** — paling mendekati "file md". Instruksi tingkat tinggi yang membentuk cara agent memandang perannya (contoh: mode "senior developer yang malas tapi efisien"). Ini cuma *ekspresi* paradigma, bukan paradigma itu sendiri — ganti filenya tidak otomatis mengubah perilaku total kalau model dasar tidak "percaya" instruksi itu.
3. **Konvensi/budaya organisasi** — CLAUDE.md, project conventions, style guide tim. Biasanya berwujud file, tapi kekuatannya dari *konsistensi penerapan* di semua sesi/agent yang memakainya, bukan dari file itu sendiri.
4. **Tool design & affordances** — tools apa yang tersedia dan bagaimana skemanya ditulis diam-diam membentuk cara pandang agent terhadap masalah. Bukan file tunggal, tapi desain arsitektur.
5. **Data feedback / reward signal berulang** — kalau ada fine-tuning berkelanjutan dari feedback user, paradigma bergeser pelan lewat data. Paling tidak "file-shaped" — wujudnya statistik dalam weight model.

## Titik yang bisa disentuh developer
Kalau ditanya "di mana paradigma itu *bisa disentuh*", jawabannya paling dekat ke **system prompt / instruction files** (level 2-3) — satu-satunya titik yang konkret, editable, dan berpengaruh besar tanpa retrain model. Paradigma "sejati" (level 1) tetap ada di training model, di luar jangkauan file apa pun.

## Terkait
- [[leverage-points]]
- [[agentic-ai]]
- [[systems-thinking]]
