# 🛡️ SENTINEL-AD: TNI AD Cognitive Defense & Threat Intelligence System

**Sistem Intelijen Siber & Pertahanan Kognitif Generasi Baru untuk TNI Angkatan Darat**  
Dikembangkan untuk mendeteksi, menganalisis, dan memitigasi operasi disinformasi, *Coordinated Inauthentic Behavior* (CIB), kampanye narasi separatisme/SARA, serta serangan rekayasa kognitif terhadap jajaran komando teritorial Kodam se-Indonesia.

---

## ⚡ Fitur Utama

1. **Pusat Komando (C2 Overview & Peta Geospasial):**
   - Pemantauan real-time satelit GEOINT terhadap 15 Kodam di seluruh Indonesia.
   - Deteksi konsentrasi narasi separatisme, SARA, dan isu viral.
   - Radar Insiden Prioritas & Pusat Triage Lengkap dengan filter multi-kriteria dan paginasi.

2. **Deteksi CIB & Forensik Deepfake Multimodal:**
   - Deteksi algoritma amplifikasi terkoordinasi (CIB burst window <60s).
   - Analisis spektrogram & bentuk gelombang audio tiruan (*voice cloning*).
   - Analisis OCR komparatif dokumen dinas resmi vs surat edaran palsu.

3. **Cognitive Wargaming Sandbox:**
   - Simulasi multi-persona (10 agen netizen: Nasionalis, Gen-Z, Skeptis, Buzzer, dll).
   - Prediksi pergeseran sentimen publik dan mitigasi *Backfire Risk*.

4. **SNA & Dynamic Threat Graph:**
   - Visualisasi graf interaktif simpul botnet, akun proksi, dan jembatan amplifikasi (menggunakan NetworkX & Pyvis).

5. **SOAR 1-Click Defense Automation:**
   - Pembuatan Dokumen Laporan Situasi Militer (SITREP PDF) berstandar Dispenad/Pussiberad.
   - Berkas Takedown JSON terenkripsi standar regulasi BSSN & Kominfo.
   - Jejak audit kriptografis SHA-256 untuk rantai komando.

6. **Dukungan Dual-Mode Telemetri:**
   - **Mode Live Online OSINT:** Menyerap berita dan isu viral langsung dari internet secara real-time.
   - **Mode Simulasi Taktis Cadangan:** Operasional mandiri offline untuk kondisi darurat perang informasi.

---

## 🚀 Panduan Menjalankan Aplikasi Secara Lokal

### 1. Prasyarat
- Python 3.10 atau 3.11
- Git

### 2. Instalasi Dependensi
```bash
git clone https://github.com/<username>/<nama-repo>.git
cd <nama-repo>
pip install -r requirements.txt
```

### 3. Menjalankan Dashboard
```bash
streamlit run app.py
```
Aplikasi akan otomatis terbuka pada peramban web di alamat: `http://localhost:8501`.

---

## 🌐 Deployment Gratis via Streamlit Community Cloud (CI/CD Otomatis)

1. *Push* kode ini ke akun GitHub Anda.
2. Kunjungi [Streamlit Community Cloud](https://share.streamlit.io/) dan login dengan akun GitHub Anda.
3. Klik **"Create app"** lalu pilih repositori ini.
4. Tentukan *Main file path*: `app.py`.
5. Klik **"Deploy!"**.
6. Setiap ada perubahan kode yang di-*push* ke GitHub (`git push`), aplikasi di cloud akan otomatis memperbarui dirinya secara live tanpa biaya (100% Free).

---

## 🎖️ Tim Pengembang
*Hak Cipta © 2026 - SENTINEL-AD Cognitive Operations System (Inovasi Hackathon TNI AD)*
