# 🛡️ PANDUAN DEPLOYMENT MILNET & ARSITEKTUR ON-PREMISE AIR-GAPPED
## SENTINEL-AD: TNI AD Cognitive Defense & Threat Intelligence System
*Dokumen Kesiapan Implementasi & Kelayakan Operasional Satuan TNI AD*

---

### 1. Ringkasan Eksekutif Kesiapan Operasional
SENTINEL-AD dirancang tidak hanya sebagai purwarupa kompetisi, melainkan solusi operasional nyata yang **100% siap digelar (Production-Ready)** di lingkungan **Pusat Siber TNI AD (Pussiberad)**, **Dinas Penerangan TNI AD (Dispenad)**, maupun Markas Komando Daerah Militer (Makodam) se-Indonesia.

Sistem memiliki kapabilitas arsitektur **Dual-Mode**:
1. **Mode Live Hybrid OSINT:** Terhubung ke ekosistem media sosial publik (TikTok, Instagram, X, Facebook, YouTube, dan Media Daring) untuk pemantauan opini publik dan deteksi dini propaganda eksternal.
2. **Mode Air-Gapped MILNET (Jaringan Intranet Tertutup TNI AD):** Beroperasi mandiri di dalam perimeter *Military Network (MILNET)* Mabesad tanpa kebocoran data (*zero telemetry data leakage*), dengan penyimpanan lokal terenkripsi AES-256-GCM.

---

### 2. Spesifikasi Kebutuhan Perangkat Keras (COTS Hardware Ready)
Sistem dioptimalkan untuk efisiensi komputasi tingkat tinggi sehingga **tidak mewajibkan klaster GPU mahal**:

| Komponen | Spesifikasi Minimum (Tingkat Korem/Kodim) | Spesifikasi Rekomendasi (Pussiberad / Mabesad C2) |
| :--- | :--- | :--- |
| **Processor** | 4-Core Intel Xeon / AMD EPYC (2.4 GHz+) | 8-Core / 16-Thread Intel Xeon Scalable |
| **RAM** | 8 GB DDR4 ECC | 16 GB - 32 GB DDR4 ECC |
| **Storage** | 100 GB NVMe SSD (Arsip Enkripsi SOAR) | 500 GB NVMe Enterprise RAID-1 |
| **Network** | 1 Gbps Ethernet NIC (MILNET Dedicated) | Dual 10 Gbps SFP+ (Redundant Trunk) |
| **Sistem Operasi**| Ubuntu Server 22.04 LTS / RHEL 9 (Security Hardened) | RHEL 9 Defense Hardened STIG Compliant |

---

### 3. Topologi Integrasi Antar-Satuan (Rantai Komando Interoperabel)

```text
       [ RADAR MULTI-PLATFORM OSINT ] 
                      │ (Feed & Telemetri Real-Time)
                      ▼
 ┌─────────────────────────────────────────────────────────┐
 │               SENTINEL-AD CORE ENGINE                   │
 │  • CIB Burst Temporal Engine (<60s)                     │
 │  • Multimodal Deepfake Screener (FFT 16kHz & Doc ELA)   │
 │  • SNA Threat Graph (PyVis Topology & Bridge Nodes)     │
 │  • Cognitive Wargaming (10 Agen Persona Netizen)        │
 └────────────────────────────┬────────────────────────────┘
                              │
               [ TACTICAL SOAR DISPATCHER ]
                              │
      ┌───────────────────────┼───────────────────────┐
      ▼                       ▼                       ▼
┌──────────────┐      ┌──────────────┐      ┌────────────────┐
│ PUSSIBERAD   │      │  DISPENAD    │      │ KOMANDAN (C2)  │
│ Analis Siber │      │  Penerangan  │      │ Otorisasi RBAC │
│ - Takedown   │      │ - Counter    │      │ - Digital Seal │
│ - BSSN JSON  │      │   Narrative  │      │ - SITREP PDF   │
│ - Forensik   │      │ - Debunk     │      │ - Eskalasi Kasad│
└──────────────┘      └──────────────┘      └────────────────┘
```

---

### 4. Langkah-Langkah Deployment Cepat (Docker & Docker Compose)

#### A. Deployment Menggunakan Docker Compose (Rekomendasi Satuan)
1. Klon repositori ke server lokal:
   ```bash
   git clone https://github.com/muh-ilham/SENTINEL-AD.git
   cd SENTINEL-AD
   ```
2. Jalankan orkestrasi container:
   ```bash
   docker compose up -d --build
   ```
3. Verifikasi status container dan healthcheck:
   ```bash
   docker compose ps
   ```
4. Akses sistem melalui peramban intranet:
   `http://<IP-SERVER-MILNET>:8501`

#### B. Menjalankan di Lingkungan Air-Gapped (Tanpa Akses Internet)
1. Ekspor image docker dari workstation terhubung:
   ```bash
   docker save -o sentinel-ad-v2.5.tar sentinel-ad-military-core:latest
   ```
2. Salin arsip `.tar` menggunakan media USB terisolasi sesuai SOP Sintelad.
3. Impor pada server fisik MILNET:
   ```bash
   docker load -i sentinel-ad-v2.5.tar
   docker run -d -p 8501:8501 --name sentinel-ad-airgapped -v /milnet/data:/app/data sentinel-ad-military-core:latest
   ```

---

### 5. Kepatuhan Hukum & Doktrin Pertahanan Siber

* **UU No. 27 Tahun 2022 tentang Perlindungan Data Pribadi (UU PDP):** Seluruh data telemetri yang diekstraksi dari ruang publik dienkripsi lokal, tanpa transfer data ke server yurisdiksi asing.
* **UU No. 1 Tahun 2024 tentang ITE:** Seluruh berkas alat bukti (Dossier JSON) memiliki segel kriptografis SHA-256 yang memenuhi syarat keabsahan bukti hukum elektronik di pengadilan.
* **Peraturan BSSN No. 4 Tahun 2021:** Mengadopsi taksonomi insiden siber nasional untuk integrasi cepat ke CSIRT BSSN.
* **Jukminu TNI AD No. 12/IV/2021:** Audit dokumen dan tipografi surat dinas sepenuhnya mengacu pada pedoman tata naskah dinas resmi Angkatan Darat.
