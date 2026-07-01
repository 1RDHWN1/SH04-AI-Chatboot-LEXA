# User Guide — Lexa Customer Service Chatbot

**Project:** SH04-AI-Chatbot-LEXA  
**Version:** 1.0.0  
**Last Updated:** 2025-07-01

---

## Welcome to Lexa 💬

Lexa adalah asisten customer service berbasis AI yang dirancang untuk menjawab pertanyaan pelanggan dengan ramah, sopan, dan profesional. Lexa menggunakan teknologi Groq Cloud API untuk memberikan respons cepat dan alami.

Lexa tersedia dalam dua mode:
- **Mode Browser (Streamlit)** — Antarmuka chat modern di browser Anda
- **Mode Terminal (CLI)** — Percakapan langsung dari terminal/command prompt

---

## Getting Started

### Prerequisites

Sebelum menggunakan Lexa, pastikan Anda telah:

- [ ] Menginstal Python 3.9 atau lebih baru
- [ ] Memiliki Groq API Key (gratis di [console.groq.com](https://console.groq.com))
- [ ] Menginstal semua dependensi (`pip install -r requirements.txt`)
- [ ] Mengatur file `.env` dengan API Key Anda

Jika Anda belum melakukan langkah-langkah di atas, lihat **Installation Guide** terlebih dahulu.

---

## Mode 1: Browser Interface (Streamlit)

### Memulai Lexa di Browser

```bash
streamlit run app.py
```

Browser akan otomatis terbuka di `http://localhost:8501`.

### Tampilan Antarmuka

```
┌──────────────────────────────────────────────────────┐
│  Lexa CS Control Panel    │  💬 Lexa Customer Service  │
│  ─────────────────────    │  ─────────────────────     │
│  🤖                       │                            │
│                           │  [User] Halo Lexa          │
│  Gunakan tombol di bawah  │  [Lexa] Halo! Ada yang...  │
│  untuk menyetel ulang     │                            │
│  percakapan.              │  [User] Berapa harga...    │
│                           │  [Lexa] Untuk informasi..  │
│  [Reset Percakapan]       │                            │
│                           │  ┌─ Ada yang bisa saya ─┐  │
│                           │  │    bantu hari ini?    │  │
│                           │  └──────────────────────┘  │
└──────────────────────────────────────────────────────┘
```

### Cara Menggunakan

1. **Ketik pesan** di kotak input di bagian bawah halaman.
2. **Tekan Enter** atau klik tombol kirim untuk mengirim pesan.
3. **Tunggu respons** — Lexa akan menjawab secara streaming (teks muncul bertahap).
4. **Lanjutkan percakapan** — Lexa mengingat konteks percakapan selama sesi berlangsung.

### Sidebar: Lexa CS Control Panel

| Elemen | Fungsi |
|--------|--------|
| 🤖 Icon | Identitas visual Lexa |
| Deskripsi | Panduan singkat penggunaan |
| Tombol "Reset Percakapan" | Menghapus semua riwayat chat dan memulai sesi baru |

> ⚠️ **Peringatan:** Klik tombol Reset akan menghapus **seluruh riwayat percakapan** dan tidak dapat dibatalkan.

### Tips Penggunaan Browser

- Riwayat percakapan **disimpan selama sesi berlangsung** (tab browser terbuka).
- Menutup tab atau me-refresh halaman akan **menghapus riwayat percakapan**.
- Anda dapat membuka **beberapa tab** — setiap tab memiliki sesi percakapan sendiri.

---

## Mode 2: Terminal Interface (CLI)

### Memulai Lexa di Terminal

```bash
python main.py
```

### Tampilan Terminal

```
=== Memulai Chatbot Customer Service Lexa ===
Lexa aktif! Ketik 'keluar' atau 'exit' untuk menyudahi obrolan.

Pelanggan: Halo, saya butuh bantuan
Lexa: Halo! Selamat datang. Saya Lexa, siap membantu Anda. Ada yang bisa saya bantu?

Pelanggan: Bagaimana cara mengembalikan produk?
Lexa: Tentu! Untuk mengembalikan produk, Anda perlu...

Pelanggan: keluar
Lexa: Terima kasih telah menghubungi kami. Semoga hari Anda menyenangkan!
```

### Perintah CLI

| Perintah | Fungsi |
|----------|--------|
| Ketik pesan → Enter | Kirim pesan ke Lexa |
| `keluar` | Mengakhiri percakapan dengan pesan perpisahan |
| `exit` | Sama dengan `keluar` |
| `Ctrl+C` | Menghentikan program secara paksa |

### Tips Penggunaan CLI

- Tekan Enter pada input kosong akan **dilewati** — tidak ada pesan yang dikirim.
- Riwayat percakapan **hilang** saat program ditutup.
- Respons ditampilkan secara **streaming** (muncul bertahap, terasa lebih natural).

---

## Pertanyaan yang Bisa Ditanyakan ke Lexa

Lexa dirancang sebagai asisten customer service. Berikut contoh pertanyaan yang dapat ditangani:

**✅ Cocok untuk Lexa:**
- "Bagaimana cara mengembalikan produk yang rusak?"
- "Jam berapa customer service bisa dihubungi?"
- "Saya ingin tahu status pesanan saya"
- "Apa kebijakan refund kalian?"
- "Produk saya tidak sampai, apa yang harus saya lakukan?"

**⚠️ Tidak Optimal untuk Lexa:**
- Pertanyaan spesifik tentang produk (harga, stok) — Lexa tidak memiliki akses database
- Permintaan di luar konteks layanan pelanggan
- Instruksi pemrograman atau teknis non-CS

---

## Frequently Asked Questions (FAQ)

**Q: Apakah Lexa menyimpan percakapan saya?**  
A: Tidak. Riwayat percakapan hanya disimpan di memori selama sesi berlangsung dan tidak ditulis ke disk atau database. Saat sesi berakhir, semua data percakapan hilang.

**Q: Apakah percakapan saya aman?**  
A: Pesan Anda dikirimkan ke server Groq Cloud untuk diproses. Harap jangan membagikan informasi sensitif seperti nomor kartu kredit, kata sandi, atau data pribadi yang sangat sensitif.

**Q: Kenapa Lexa terkadang lambat merespons?**  
A: Kecepatan respons bergantung pada koneksi internet dan beban server Groq. Lexa menggunakan streaming sehingga teks muncul bertahap — ini bukan hang atau error.

**Q: Apa yang terjadi jika saya tekan Reset?**  
A: Seluruh riwayat percakapan dihapus dan Lexa kembali ke kondisi awal. Ini tidak bisa dibatalkan.

**Q: Bisakah saya mengganti model AI yang digunakan?**  
A: Ya, jika Anda developer. Ubah parameter `model` saat inisialisasi `LexaChatbot()`:
```python
bot = LexaChatbot(model="llama-3.1-8b-instant")
```
Model yang tersedia dapat dilihat di [Groq Console](https://console.groq.com).

**Q: Apa yang dilakukan Lexa jika tidak mengerti pertanyaan saya?**  
A: Lexa akan meminta klarifikasi dengan sopan. Coba ubah kalimat pertanyaan Anda atau tambahkan detail lebih lanjut.

---

## Troubleshooting

| Masalah | Kemungkinan Penyebab | Solusi |
|---------|----------------------|--------|
| "API Key Groq tidak ditemukan!" | `.env` tidak ada atau key salah | Buat/periksa file `.env` |
| Respons sangat lambat | Koneksi internet lemah | Periksa koneksi; coba lagi |
| "Gagal memproses request" | API error sementara | Tunggu beberapa detik; coba lagi |
| Halaman Streamlit tidak terbuka | Port 8501 diblokir | Jalankan `streamlit run app.py --server.port 8502` |
| Error saat `pip install` | Python versi lama | Update ke Python 3.9+ |

Untuk panduan instalasi lengkap, lihat [Installation Guide](InstallationGuide.md).
