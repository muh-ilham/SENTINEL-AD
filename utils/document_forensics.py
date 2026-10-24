"""
utils/document_forensics.py - Military Document Forensics & OCR Integrity Engine
Provides multi-layer document forensics, Error Level Analysis (ELA),
typography mismatch detection, Mabesad Minu registry verification,
and BSSN-compliant forensic dossier generation.
"""

import io
import json
import hashlib
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageEnhance
import numpy as np

def compute_sha256(data_bytes: bytes) -> str:
    """Computes SHA-256 hexadecimal string from byte data."""
    return hashlib.sha256(data_bytes).hexdigest()

def compute_md5(data_bytes: bytes) -> str:
    """Computes MD5 hexadecimal string from byte data."""
    return hashlib.md5(data_bytes).hexdigest()

def generate_document_canvas_image(doc_key: str) -> tuple[Image.Image, Image.Image]:
    """
    Generates deterministic, defense-grade document raster images and their corresponding
    Error Level Analysis (ELA) heatmap images for military document forensic simulation.
    
    Returns:
        tuple[Image.Image, Image.Image]: (original_document_img, ela_heatmap_img)
    """
    width, height = 750, 1000
    
    # 1. Base Paper Canvas (Clean Military Cream/White Paper)
    img = Image.new("RGB", (width, height), color=(253, 253, 252))
    draw = ImageDraw.Draw(img)
    
    # Subtle paper border / shadow frame
    draw.rectangle([0, 0, width - 1, height - 1], outline=(203, 213, 225), width=2)
    draw.rectangle([15, 15, width - 16, height - 16], outline=(226, 232, 240), width=1)
    
    # ELA Canvas base (Dark noise floor)
    ela = Image.new("RGB", (width, height), color=(15, 23, 42))
    draw_ela = ImageDraw.Draw(ela)
    
    # Draw faint background ELA uniform compression noise
    np_noise = np.random.normal(12, 4, (height, width, 3)).clip(5, 30).astype(np.uint8)
    noise_img = Image.fromarray(np_noise)
    ela = ImageChops.add(ela, noise_img)
    draw_ela = ImageDraw.Draw(ela)

    if doc_key == "doc_a":
        # -------------------------------------------------------------
        # DOKUMEN A: Sprin Mutasi Palsu Dispenad (Sprin/482/IX/2026)
        # -------------------------------------------------------------
        # Header (Kop Surat)
        draw.line([(50, 95), (width - 50, 95)], fill=(15, 23, 42), width=2)
        draw.text((width // 2, 45), "TENTARA NASIONAL INDONESIA ANGKATAN DARAT", fill=(15, 23, 42), anchor="mm")
        draw.text((width // 2, 65), "MARKAS BESAR", fill=(15, 23, 42), anchor="mm")
        draw.text((width // 2, 80), "Jalan Veteran No. 5 Jakarta Pusat - 10110", fill=(100, 116, 139), anchor="mm")
        
        # Classification Stamp
        draw.rectangle([width - 150, 30, width - 60, 52], outline=(220, 38, 38), width=2)
        draw.text((width - 105, 41), "RAHASIA", fill=(220, 38, 38), anchor="mm")
        
        # Document Title
        draw.text((width // 2, 130), "SURAT PERINTAH", fill=(15, 23, 42), anchor="mm")
        draw.line([(width // 2 - 90, 142), (width // 2 + 90, 142)], fill=(15, 23, 42), width=1)
        
        # Anomaly Box 1: Font Mismatch in Sprin Number (Courier New Typewriter)
        draw.rectangle([width // 2 - 190, 152, width // 2 + 190, 178], fill=(254, 226, 226), outline=(239, 68, 68), width=2)
        draw.text((width // 2, 165), "Nomor: Sprin / 482 / IX / 2026-DISPENAD [ANOMALI FONT]", fill=(185, 28, 28), anchor="mm")
        
        # ELA High Brightness on Anomaly 1 (Digital splicing of font)
        draw_ela.rectangle([width // 2 - 190, 152, width // 2 + 190, 178], fill=(230, 40, 80), outline=(255, 200, 200), width=1)
        
        # Body Text
        draw.text((70, 215), "Pertimbangan :", fill=(15, 23, 42))
        draw.text((180, 215), "Bahwa dalam rangka pembinaan karir dan penyegaran satuan", fill=(51, 65, 85))
        draw.text((180, 235), "intelijen serta penerangan di lingkungan Angkatan Darat...", fill=(51, 65, 85))
        
        draw.text((70, 275), "Dasar              :", fill=(15, 23, 42))
        draw.text((180, 275), "1. Keputusan Panglima TNI Nomor Kep/812/VIII/2026;", fill=(51, 65, 85))
        draw.text((180, 295), "2. Pertimbangan pimpinan Staf Umum Angkatan Darat.", fill=(51, 65, 85))
        
        draw.text((width // 2, 345), "D I P E R I N T A H K A N", fill=(15, 23, 42), anchor="mm")
        
        draw.text((70, 380), "Kepada          :", fill=(15, 23, 42))
        draw.text((180, 380), "Kolonel Inf. Ahmad Fauzi, S.I.P. (NRP 11980023410775)", fill=(15, 23, 42))
        draw.text((180, 400), "Jabatan Lama: Kasubdis Media Online Dispenad", fill=(71, 85, 105))
        draw.text((180, 420), "Jabatan Baru: Staf Khusus Kasad (Non-Job / Mutasi)", fill=(220, 38, 38))
        
        draw.text((70, 460), "Untuk              :", fill=(15, 23, 42))
        draw.text((180, 460), "1. Segera melaksanakan serah terima jabatan terhitung 24 Okt 2026;", fill=(51, 65, 85))
        draw.text((180, 480), "2. Melaporkan pelaksanaan mutasi kepada Kepala Staf Angkatan Darat;", fill=(51, 65, 85))
        draw.text((180, 500), "3. Melaksanakan perintah ini dengan penuh rasa tanggung jawab.", fill=(51, 65, 85))
        
        # Sign-off Area
        sign_x = width - 260
        draw.text((sign_x + 90, 600), "Dikeluarkan di : Jakarta", fill=(51, 65, 85), anchor="mm")
        draw.text((sign_x + 90, 620), "pada tanggal    : 22 September 2026", fill=(51, 65, 85), anchor="mm")
        draw.text((sign_x + 90, 650), "a.n. KEPALA STAF ANGKATAN DARAT", fill=(15, 23, 42), anchor="mm")
        draw.text((sign_x + 90, 668), "WAKIL KEPALA STAF,", fill=(15, 23, 42), anchor="mm")
        
        # Anomaly Box 2: Forged Stamp (Overlayed Digital PNG with 14.2 deg rotation)
        stamp_cx, stamp_cy = sign_x + 40, 740
        draw.ellipse([stamp_cx - 48, stamp_cy - 48, stamp_cx + 48, stamp_cy + 48], outline=(220, 38, 38), width=3)
        draw.ellipse([stamp_cx - 36, stamp_cy - 36, stamp_cx + 36, stamp_cy + 36], outline=(220, 38, 38), width=1)
        draw.text((stamp_cx, stamp_cy - 12), "MARKAS BESAR", fill=(220, 38, 38), anchor="mm")
        draw.text((stamp_cx, stamp_cy + 2), "★ TNI AD ★", fill=(220, 38, 38), anchor="mm")
        draw.text((stamp_cx, stamp_cy + 16), "ROTASI 14.2°", fill=(239, 68, 68), anchor="mm")
        
        # Bounding box on stamp anomaly
        draw.rectangle([stamp_cx - 56, stamp_cy - 56, stamp_cx + 56, stamp_cy + 56], outline=(239, 68, 68), width=2)
        
        # ELA High Brightness on Anomaly 2 (Stamp PNG splicing artifact)
        draw_ela.ellipse([stamp_cx - 50, stamp_cy - 50, stamp_cx + 50, stamp_cy + 50], fill=(245, 158, 11), outline=(255, 255, 100), width=3)
        draw_ela.rectangle([stamp_cx - 56, stamp_cy - 56, stamp_cx + 56, stamp_cy + 56], outline=(255, 100, 100), width=1)

        # Signature
        draw.text((sign_x + 110, 735), "M. Syahrir", fill=(30, 58, 138), anchor="mm")
        draw.text((sign_x + 90, 790), "M. SYAHRIR, M.Sc.", fill=(15, 23, 42), anchor="mm")
        draw.line([(sign_x + 20, 800), (sign_x + 160, 800)], fill=(15, 23, 42), width=1)
        draw.text((sign_x + 90, 815), "LETNAN JENDERAL TNI", fill=(71, 85, 105), anchor="mm")

    elif doc_key == "doc_b":
        # -------------------------------------------------------------
        # DOKUMEN B: Pengesahan Anggaran Pengadaan Fiktif Alutsista
        # -------------------------------------------------------------
        draw.line([(50, 95), (width - 50, 95)], fill=(15, 23, 42), width=2)
        draw.text((width // 2, 45), "KEMENTERIAN PERTAHANAN REPUBLIK INDONESIA", fill=(15, 23, 42), anchor="mm")
        draw.text((width // 2, 65), "DIREKTORAT JENDERAL PERENCANAAN PERTAHANAN", fill=(15, 23, 42), anchor="mm")
        draw.text((width // 2, 80), "Gedung D.I. Pandjaitan Lt. 5, Jl. Medan Merdeka Barat No. 13-14", fill=(100, 116, 139), anchor="mm")
        
        draw.rectangle([width - 150, 30, width - 60, 52], outline=(234, 88, 12), width=2)
        draw.text((width - 105, 41), "TERBATAS", fill=(234, 88, 12), anchor="mm")
        
        draw.text((width // 2, 130), "LEMBAR PENGESAHAN ALOKASI ANGGARAN KHUSUS", fill=(15, 23, 42), anchor="mm")
        draw.line([(width // 2 - 160, 142), (width // 2 + 160, 142)], fill=(15, 23, 42), width=1)
        
        draw.text((width // 2, 160), "Nomor Registrasi: DIPA / 088 / BM / ALUTSISTA / X / 2026", fill=(51, 65, 85), anchor="mm")
        
        draw.text((70, 210), "Program          :", fill=(15, 23, 42))
        draw.text((180, 210), "Modernisasi Radar Pertahanan Udara & Sensor Taktis Wilayah Barat", fill=(51, 65, 85))
        
        draw.text((70, 240), "Satuan Kerja  :", fill=(15, 23, 42))
        draw.text((180, 240), "Pusat Kesenjataan Artileri Pertahanan Udara (Pussenarhanud)", fill=(51, 65, 85))
        
        # Anomaly Box: Doctored Budget Amount (JPEG Splicing Peak)
        draw.rectangle([70, 280, width - 70, 350], fill=(254, 242, 242), outline=(239, 68, 68), width=2)
        draw.text((width // 2, 302), "JUMLAH ALOKASI PENCAIRAN TERMIN I (FIKTIF):", fill=(185, 28, 28), anchor="mm")
        draw.text((width // 2, 328), "Rp 847.500.000.000,- [ANOMALI SPLICING NOMINAL]", fill=(220, 38, 38), anchor="mm")
        
        draw_ela.rectangle([70, 280, width - 70, 350], fill=(239, 68, 68), outline=(255, 255, 255), width=2)
        
        draw.text((70, 380), "Keterangan Validasi Minu:", fill=(15, 23, 42))
        draw.text((70, 405), "Dokumen ini diklaim memuat komitmen pencairan langsung rekening luar negeri.", fill=(71, 85, 105))
        draw.text((70, 425), "Setelah diverifikasi terhadap Sistem Perbendaharaan Kemenkeu & Ranmin Kemhan,", fill=(71, 85, 105))
        draw.text((70, 445), "kode rekening 088-BM tidak terdaftar dalam pagu APBN 2026.", fill=(220, 38, 38))
        
        # Forged Signatures
        sign_x = width - 260
        draw.text((sign_x + 90, 640), "Jakarta, 14 Oktober 2026", fill=(51, 65, 85), anchor="mm")
        draw.text((sign_x + 90, 665), "Pejabat Pembuat Komitmen,", fill=(15, 23, 42), anchor="mm")
        
        stamp_cx, stamp_cy = sign_x + 40, 740
        draw.ellipse([stamp_cx - 45, stamp_cy - 45, stamp_cx + 45, stamp_cy + 45], outline=(220, 38, 38), width=2)
        draw.text((stamp_cx, stamp_cy), "DITJEN RENHAN", fill=(220, 38, 38), anchor="mm")
        draw_ela.ellipse([stamp_cx - 45, stamp_cy - 45, stamp_cx + 45, stamp_cy + 45], fill=(234, 88, 12), outline=(255, 200, 100), width=2)
        
        draw.text((sign_x + 90, 800), "Drs. HENDRA WIJAYA, M.Si.", fill=(15, 23, 42), anchor="mm")
        draw.line([(sign_x + 20, 810), (sign_x + 160, 810)], fill=(15, 23, 42), width=1)
        draw.text((sign_x + 90, 825), "Pembina Utama Madya IV/d", fill=(71, 85, 105), anchor="mm")

    else:
        # -------------------------------------------------------------
        # DOKUMEN C: Dokumen Asli Terverifikasi Mabesad (Golden Standard)
        # -------------------------------------------------------------
        draw.line([(50, 95), (width - 50, 95)], fill=(15, 23, 42), width=2)
        draw.text((width // 2, 45), "TENTARA NASIONAL INDONESIA ANGKATAN DARAT", fill=(15, 23, 42), anchor="mm")
        draw.text((width // 2, 65), "DINAS PENERANGAN", fill=(15, 23, 42), anchor="mm")
        draw.text((width // 2, 80), "Jalan Veteran No. 5 Jakarta Pusat - 10110", fill=(100, 116, 139), anchor="mm")
        
        draw.rectangle([width - 150, 30, width - 60, 52], outline=(16, 185, 129), width=2)
        draw.text((width - 105, 41), "TERBUKA", fill=(16, 185, 129), anchor="mm")
        
        draw.text((width // 2, 130), "SURAT PERINTAH", fill=(15, 23, 42), anchor="mm")
        draw.line([(width // 2 - 90, 142), (width // 2 + 90, 142)], fill=(15, 23, 42), width=1)
        
        # Valid Green Box
        draw.rectangle([width // 2 - 180, 152, width // 2 + 180, 178], fill=(236, 253, 245), outline=(16, 185, 129), width=2)
        draw.text((width // 2, 165), "Nomor: Sprin / 104 / III / 2026-DISPENAD [TERVERIFIKASI]", fill=(4, 120, 87), anchor="mm")
        
        draw.text((70, 215), "Pertimbangan :", fill=(15, 23, 42))
        draw.text((180, 215), "Bahwa dalam rangka pelaksanaan program publikasi transparansi TNI AD...", fill=(51, 65, 85))
        
        draw.text((width // 2, 340), "D I P E R I N T A H K A N", fill=(15, 23, 42), anchor="mm")
        
        draw.text((70, 380), "Kepada          :", fill=(15, 23, 42))
        draw.text((180, 380), "Tim Satgas Media Siber Dispenad", fill=(15, 23, 42))
        draw.text((180, 400), "Tugas: Pelaksanaan Pemantauan Opini Publik & Klarifikasi Berita Hoaks", fill=(51, 65, 85))
        
        # Official Seal with Authentic Ink Bleed and QR Code BSrE
        sign_x = width - 260
        draw.text((sign_x + 90, 600), "Dikeluarkan di : Jakarta", fill=(51, 65, 85), anchor="mm")
        draw.text((sign_x + 90, 620), "pada tanggal    : 10 Maret 2026", fill=(51, 65, 85), anchor="mm")
        draw.text((sign_x + 90, 650), "KEPALA DINAS PENERANGAN TNI AD,", fill=(15, 23, 42), anchor="mm")
        
        stamp_cx, stamp_cy = sign_x + 40, 740
        # Authentic wet stamp (Deep Navy / Purple official ink)
        draw.ellipse([stamp_cx - 48, stamp_cy - 48, stamp_cx + 48, stamp_cy + 48], outline=(30, 58, 138), width=2)
        draw.ellipse([stamp_cx - 38, stamp_cy - 38, stamp_cx + 38, stamp_cy + 38], outline=(30, 58, 138), width=1)
        draw.text((stamp_cx, stamp_cy - 10), "DINAS PENERANGAN", fill=(30, 58, 138), anchor="mm")
        draw.text((stamp_cx, stamp_cy + 8), "★ MABESAD ★", fill=(30, 58, 138), anchor="mm")
        
        # Verified BSrE QR Code simulation box
        draw.rectangle([70, 680, 150, 760], fill=(241, 245, 249), outline=(16, 185, 129), width=2)
        draw.text((110, 715), "QR BSrE", fill=(4, 120, 87), anchor="mm")
        draw.text((110, 735), "TERDAFTAR", fill=(4, 120, 87), anchor="mm")
        
        draw.text((sign_x + 90, 800), "KRISNO WIDODO", fill=(15, 23, 42), anchor="mm")
        draw.line([(sign_x + 20, 810), (sign_x + 160, 810)], fill=(15, 23, 42), width=1)
        draw.text((sign_x + 90, 825), "BRIGADIR JENDERAL TNI", fill=(71, 85, 105), anchor="mm")
        
        # For genuine document, ELA has uniform low noise (no bright splicing blocks)

    return img, ela

def perform_real_ela(image_bytes: bytes, quality: int = 90) -> tuple[Image.Image, float, dict]:
    """
    Performs authentic Error Level Analysis (ELA) on arbitrary image bytes.
    Resaves image at specified JPEG quality, computes pixel difference, scales extrema,
    and returns (ela_enhanced_image, tamper_score_pct, metrics_dict).
    """
    try:
        orig = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        resaved_buf = io.BytesIO()
        orig.save(resaved_buf, "JPEG", quality=quality)
        resaved = Image.open(resaved_buf)
        
        # Image difference
        diff = ImageChops.difference(orig, resaved)
        extrema = diff.getextrema()
        max_diff = max([ex[1] for ex in extrema])
        scale = 255.0 / max_diff if max_diff > 0 else 1.0
        
        # Enhance brightness to reveal compression artifacts
        ela_img = ImageEnhance.Brightness(diff).enhance(scale * 0.9)
        
        # Compute tamper score from high-variance outlier regions
        diff_np = np.array(diff)
        mean_val = float(np.mean(diff_np))
        std_val = float(np.std(diff_np))
        high_diff_ratio = float(np.sum(diff_np > (mean_val + 2.5 * std_val))) / (diff_np.size + 1e-6)
        
        tamper_score = min(99.0, max(5.0, high_diff_ratio * 400.0 + mean_val * 1.5))
        tamper_score = round(tamper_score, 1)
        
        metrics = {
            "max_difference": int(max_diff),
            "mean_error_level": round(mean_val, 2),
            "error_std_dev": round(std_val, 2),
            "compression_quality": quality,
            "width": orig.width,
            "height": orig.height
        }
        return ela_img, tamper_score, metrics
    except Exception as e:
        # Fallback dummy ELA in case of unsupported format
        fallback = Image.new("RGB", (600, 800), color=(15, 23, 42))
        return fallback, 50.0, {"error": str(e)}

def get_document_catalog():
    """Returns rich tactical metadata for all available military document specimens."""
    return {
        "doc_a": {
            "id": "DOC-FORGERY-482IX",
            "code": "Sprin/482/IX/2026",
            "name": "Surat Edaran Palsu Mutasi Staf Dispenad (Sprin/482/IX/2026)",
            "category": "Pemalsuan Surat Perintah (Sprin) Personel Mabesad",
            "threat_level": "Kritis",
            "verdict": "DOKUMEN PALSU TERKONFIRMASI (FABRICATED FORGERY)",
            "verdict_color": "#EF4444",
            "tamper_prob": 94.6,
            "sha256": "8f4e2b91c60d84a7e3115599b1a030491e8892ccbd64789fae15099238f40192",
            "md5": "b34e5684a0d9237ff1104e12e88a09bc",
            "minu_register_check": {
                "status": "INVALID / TIDAK TERDAFTAR",
                "status_color": "#EF4444",
                "db_status": "Gagal Verifikasi",
                "officer_auth": "Nihil (Nama Pejabat Penandatangan Mismatch)",
                "bsre_signature": "Tidak Memiliki Sertifikat Elektronik Balai Sertifikasi BSSN",
                "official_agenda_book": "Buku Agenda Minu Dispenad Tahun 2026 (Nomor 482 Kosong/Non-Eksis)"
            },
            "exif_metadata": {
                "Software": "Canva Web Editor v2.4 (Raster Overlay Output)",
                "CreationDate": "2026-09-22 14:12:05 UTC",
                "ModifiedDate": "2026-09-22 15:45:18 UTC (Spliced 3 Times)",
                "ColorSpace": "sRGB IEC61966-2.1 (Bukan Standar Percetakan Milnet CMYK)",
                "DPI": "72 DPI (Artefak Scraping Resolusi Rendah)",
                "PageFormat": "Custom Web Canvas (210 x 280 mm Mismatch A4 Jukminu)"
            },
            "findings": [
                {
                    "item": "Kop Surat & Lambang Mabesad",
                    "status": "NON-STANDARD CROPPED DRAFT",
                    "color": "#EF4444",
                    "detail": "Lambang garuda dan kop surat memiliki artefak piksel 72 DPI (hasil crop dari situs internet terbuka). Standar Jukminu Mabesad mewajibkan aset vektor monokrom/emas resolusi 300 DPI."
                },
                {
                    "item": "Penomoran Sprin & Tipografi",
                    "status": "FONT KERNING MISMATCH (COURIER NEW)",
                    "color": "#EF4444",
                    "detail": "Karakter nomor surat menggunakan font 'Courier New' monospaced. Standar naskah dinas Mabesad mewajibkan font Arial atau Bookman Old Style ukuran 12 pt dengan spasi baris 1.5."
                },
                {
                    "item": "Stempel Basah Komando",
                    "status": "FORGED DIGITAL OVERLAY (ROTASI 14.2°)",
                    "color": "#EF4444",
                    "detail": "Stempel komando terdeteksi berupa layer PNG transparan dengan sudut rotasi artifisial 14.2°. Tidak ditemukan pola penyerapan tinta fisik (ink bleed) pada serat kertas mikro."
                },
                {
                    "item": "Tanda Tangan Komando",
                    "status": "UNAUTHENTICATED BRUSH SCRIPT",
                    "color": "#EF4444",
                    "detail": "Tanda tangan digital meniru paraf Wakasad menggunakan font tulisan tangan Brush Script komersial tanpa kode hash tanda tangan elektronik resmi (BSrE)."
                },
                {
                    "item": "Struktur Redaksi Militer",
                    "status": "SYNTAX & TERMINOLOGY VIOLATION",
                    "color": "#F59E0B",
                    "detail": "Penggunaan frasa 'penyegaran satuan' tidak lazim dalam konsiderans Surat Perintah mutasi resmi Angkatan Darat (lazimnya menggunakan formula 'kebutuhan organisasi dan pembinaan karier')."
                }
            ]
        },
        "doc_b": {
            "id": "DOC-FORGERY-088BM",
            "code": "DIPA/088/BM/2026",
            "name": "Lembar Pengesahan Anggaran Pengadaan Fiktif Alutsista (DIPA/088/BM/2026)",
            "category": "Dokumen Pengadaan Alutsista Bodong (Hoaks Finansial)",
            "threat_level": "Tinggi",
            "verdict": "DOKUMEN MANIPULATIF HOAKS KEUANGAN",
            "verdict_color": "#F59E0B",
            "tamper_prob": 88.2,
            "sha256": "4c91a0b38827d141e9882201f99c8391200192837465abc88291029384756102",
            "md5": "e0192847561029384756102938475610",
            "minu_register_check": {
                "status": "INVALID / KODE DIPA TIDAK DITEMUKAN",
                "status_color": "#EF4444",
                "db_status": "Gagal Verifikasi",
                "officer_auth": "NIP/NRP Pejabat Tidak Terdaftar di Ranmin Kemhan",
                "bsre_signature": "Tidak Terverifikasi di Portal SPSE / LPSE Kemenkeu",
                "official_agenda_book": "Buku DIPA Kemhan TA 2026 (Kode Sub-Alokasi 088-BM Fiktif)"
            },
            "exif_metadata": {
                "Software": "Adobe Photoshop 24.1 (Windows)",
                "CreationDate": "2026-10-14 09:18:22 UTC",
                "ModifiedDate": "2026-10-14 11:02:44 UTC",
                "ColorSpace": "RGB Standard Display",
                "DPI": "96 DPI",
                "PageFormat": "Letter Mismatch A4 Militer"
            },
            "findings": [
                {
                    "item": "Blok Anggaran Nominal",
                    "status": "JPEG SPLICING PEAK DETECTED",
                    "color": "#EF4444",
                    "detail": "Area teks nominal 'Rp 847.500.000.000,-' menunjukkan lonjakan tingkat kesalahan kompresi ELA drastis, menandakan angka nominal telah disunting dan ditempelkan di atas dokumen lain."
                },
                {
                    "item": "Hierarki Kop Surat",
                    "status": "HIERARCHY MISMATCH",
                    "color": "#EF4444",
                    "detail": "Kombinasi nama instansi Kementerian Pertahanan dengan format tata naskah Mabes TNI tanpa konsistensi kode jabatan eselon I."
                },
                {
                    "item": "Stempel Renhan",
                    "status": "MISSING SERIAL CODE",
                    "color": "#F59E0B",
                    "detail": "Cap dinas Ditjen Renhan tidak memiliki kode stensil pengaman dan nomor seri register cap pengadaan."
                }
            ]
        },
        "doc_c": {
            "id": "DOC-AUTH-104III",
            "code": "Sprin/104/III/2026",
            "name": "Surat Perintah Asli Terverifikasi Dispenad (Sprin/104/III/2026 - Golden Standard)",
            "category": "Dokumen Militer Resmi Terverifikasi (Golden Standard Kontrol)",
            "threat_level": "Aman",
            "verdict": "DOKUMEN OTENTIK TERVERIFIKASI RESMI",
            "verdict_color": "#10B981",
            "tamper_prob": 2.1,
            "sha256": "1a084bc912384756102938475610293847561029384756102938475610293847",
            "md5": "78912345678912345678912345678912",
            "minu_register_check": {
                "status": "TERVERIFIKASI RESMI MABESAD",
                "status_color": "#10B981",
                "db_status": "Valid & Terdaftar",
                "officer_auth": "Kadispenad (Brigjen TNI Krisno Widodo) - Sah",
                "bsre_signature": "Sertifikat Elektronik BSSN / BSrE Valid (Serial 09-BSRE-2026-X)",
                "official_agenda_book": "Buku Agenda Sprin Dispenad TA 2026 Halaman 42 Baris 14"
            },
            "exif_metadata": {
                "Software": "Mabesad Minu Auto-Doc Generator v4.1 (Milnet Engine)",
                "CreationDate": "2026-03-10 08:00:00 WIB",
                "ModifiedDate": "Nihil (Arsip Kriptografis Terkunci)",
                "ColorSpace": "CMYK Press Profile Standar Jukminu",
                "DPI": "300 DPI (High Resolution Print Quality)",
                "PageFormat": "Standar A4 Presisi (210 x 297 mm)"
            },
            "findings": [
                {
                    "item": "Kop Surat & Lambang Garuda",
                    "status": "AUTHENTIC VECTOR GRAPHIC (300 DPI)",
                    "color": "#10B981",
                    "detail": "Kop surat menggunakan lambang resmi dengan resolusi presisi 300 DPI dan ketebalan garis standar Minu Mabesad."
                },
                {
                    "item": "Tipografi & Penomoran",
                    "status": "STANDAR JUKMINU TNI AD COMPLIANT",
                    "color": "#10B981",
                    "detail": "Jenis font Arial / Bookman Old Style 12 pt dengan kerning konsisten dan format kode naskah dinas baku."
                },
                {
                    "item": "Stempel Basah Komando",
                    "status": "NATURAL INK ABSORPTION & MICRO-SEAL",
                    "color": "#10B981",
                    "detail": "Tinta cap berwarna ungu kebiruan dengan mikrogram pengaman dan sebaran resapan serat kertas alami."
                },
                {
                    "item": "Sertifikat Digital BSrE",
                    "status": "VALID CRYPTOGRAPHIC SIGNATURE",
                    "color": "#10B981",
                    "detail": "QR Code terhubung langsung ke gerbang verifikasi Balai Sertifikasi Elektronik BSSN dan berstatus aktif."
                }
            ]
        }
    }

def generate_document_dossier_json(doc_info: dict, examiner_role: str = "Analis Siber (Pussiberad)") -> bytes:
    """Generates standardized BSSN & Pussiberad JSON forensic dossier for military document forgery."""
    dossier = {
        "dossier_type": "MILITARY_DOCUMENT_FORENSIC_AUDIT_DOSSIER",
        "standard": "BSSN-SINTEL-2026-DOC-FORENSIC-V2",
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S WIB"),
        "examiner_agency": "Pusat Siber TNI AD (Pussiberad) & Dispenad",
        "examiner_role": examiner_role,
        "classification": "RAHASIA / DEFENSE ONLY",
        "target_document": {
            "incident_id": doc_info.get("id"),
            "document_code": doc_info.get("code"),
            "document_name": doc_info.get("name"),
            "category": doc_info.get("category"),
            "tamper_probability_percentage": doc_info.get("tamper_prob"),
            "forensic_verdict": doc_info.get("verdict"),
            "sha256_checksum": doc_info.get("sha256"),
            "md5_checksum": doc_info.get("md5")
        },
        "minu_registry_audit": doc_info.get("minu_register_check", {}),
        "exif_metadata_inspection": doc_info.get("exif_metadata", {}),
        "ocr_findings_matrix": doc_info.get("findings", []),
        "chain_of_custody": {
            "evidence_intake_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S WIB"),
            "intake_source": "SENTINEL-AD Military Document Forensics Engine",
            "integrity_sealed": True,
            "next_chain": "Tactical SOAR & Komando Siber Mabes TNI / BSSN Takedown Queue"
        }
    }
    return json.dumps(dossier, indent=2, ensure_ascii=False).encode("utf-8")

def get_clean_document_html(doc_key: str, show_anomalies: bool = True) -> str:
    """
    Returns clean, non-indented HTML for military document rendering.
    Avoids Markdown 4-space indentation block parser bug.
    """
    if doc_key == "doc_a":
        border_color = "#EF4444" if show_anomalies else "#94A3B8"
        font_box_style = (
            "background: rgba(239, 68, 68, 0.16); border: 1.5px dashed #EF4444; padding: 3px 8px; border-radius: 3px; color: #991B1B;"
            if show_anomalies else "padding: 3px 8px; color: #0F172A;"
        )
        font_badge = '<span style="color: #DC2626; font-size: 8.5px; font-family: monospace; font-weight: bold;">[ANOMALI: FONT COURIER NEW]</span>' if show_anomalies else ''
        kop_badge = '<div style="font-size: 8.5px; color: #DC2626; font-family: monospace; margin-top: 2px;">[ANOMALI RESOLUSI KOP: 72 DPI BITMAP CROP]</div>' if show_anomalies else ''
        stamp_border = "border: 2px dashed #EF4444; background: rgba(239,68,68,0.15);" if show_anomalies else "border: 2px solid #1E3A8A; background: transparent;"
        stamp_badge = '<div style="font-size: 8px; color: #EF4444; margin-top: 3px; font-family: monospace; font-weight: bold;">[STEMPEL PNG OVERLAY ROTASI 14.2°]</div>' if show_anomalies else ''
        
        return f"""<div style="background: #FFFFFF; color: #0F172A; padding: 26px 30px; border-radius: 6px; box-shadow: 0 4px 20px rgba(0,0,0,0.45); font-family: 'Times New Roman', serif; position: relative; border: 2px solid {border_color};">
<div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
<div style="font-size: 9px; font-weight: bold; border: 1.5px solid #DC2626; color: #DC2626; padding: 1px 6px; border-radius: 2px; font-family: 'JetBrains Mono', monospace;">RAHASIA</div>
<div style="font-size: 9px; color: #DC2626; font-weight: bold; font-family: 'JetBrains Mono', monospace; background: rgba(239,68,68,0.12); padding: 2px 6px; border-radius: 3px;">TAMPER CONFIDENCE: 94.6%</div>
</div>
<div style="text-align: center; border-bottom: 2px solid #0F172A; padding-bottom: 6px; margin-bottom: 12px;">
<div style="font-size: 11.5px; font-weight: bold; letter-spacing: 0.05em;">TENTARA NASIONAL INDONESIA ANGKATAN DARAT</div>
<div style="font-size: 10.5px; font-weight: bold;">MARKAS BESAR</div>
<div style="font-size: 9px; color: #475569;">Jalan Veteran No. 5 Jakarta Pusat - 10110</div>
{kop_badge}
</div>
<div style="text-align: center; margin-bottom: 14px;">
<div style="font-size: 12px; font-weight: bold; text-decoration: underline;">SURAT PERINTAH</div>
<div style="margin-top: 4px;">
<span style="font-size: 10.5px; font-family: 'Courier New', monospace; {font_box_style} display: inline-block;">
Nomor: Sprin / 482 / IX / 2026-DISPENAD {font_badge}
</span>
</div>
</div>
<div style="font-size: 10px; line-height: 1.5; margin-bottom: 14px;">
<div style="margin-bottom: 6px;"><b>Pertimbangan:</b> Bahwa dalam rangka pembinaan karir dan penyegaran satuan intelijen serta penerangan di lingkungan Angkatan Darat...</div>
<div><b>Dasar:</b> 1. Keputusan Panglima TNI Nomor Kep/812/VIII/2026; 2. Pertimbangan Staf Umum Angkatan Darat.</div>
</div>
<div style="text-align: center; font-size: 10.5px; font-weight: bold; letter-spacing: 0.15em; margin: 10px 0;">D I P E R I N T A H K A N</div>
<div style="font-size: 10px; line-height: 1.5; margin-bottom: 16px;">
<div><b>Kepada:</b> Kolonel Inf. Ahmad Fauzi, S.I.P. (NRP 11980023410775)</div>
<div style="color: #64748B; font-size: 9.5px; margin-left: 50px;">Jabatan Lama: Kasubdis Media Online Dispenad</div>
<div style="color: #DC2626; font-size: 9.5px; font-weight: bold; margin-left: 50px;">Jabatan Baru: Staf Khusus Kasad (Non-Job / Mutasi Hoaks)</div>
<div style="margin-top: 6px;"><b>Untuk:</b> 1. Segera melaksanakan serah terima jabatan; 2. Melaporkan pelaksanaan tugas kepada Kasad.</div>
</div>
<div style="display: flex; justify-content: flex-end; margin-top: 18px;">
<div style="text-align: center; width: 210px; position: relative;">
<div style="font-size: 9.5px;">Ditetapkan di: Jakarta</div>
<div style="font-size: 9.5px;">pada tanggal: 22 September 2026</div>
<div style="font-size: 9.5px; font-weight: bold; margin-top: 4px;">a.n. KEPALA STAF ANGKATAN DARAT</div>
<div style="font-size: 9.5px; font-weight: bold;">WAKIL KEPALA STAF,</div>
<div style="height: 55px; position: relative; display: flex; align-items: center; justify-content: center; margin: 3px 0;">
<div style="position: absolute; left: 8px; {stamp_border} width: 68px; height: 68px; border-radius: 50%; display: flex; flex-direction: column; align-items: center; justify-content: center; font-size: 7.5px; color: #DC2626; font-weight: bold; transform: rotate(14.2deg);">
<span>MARKAS BESAR</span>
<span style="font-size: 9px;">★ TNI AD ★</span>
<span style="font-size: 6.5px; color: #B91C1C;">ROTASI 14.2°</span>
</div>
<span style="font-family: 'Brush Script MT', cursive, sans-serif; font-size: 20px; color: #1E3A8A; z-index: 2; margin-left: 15px;">M. Syahrir</span>
</div>
<div style="font-size: 10px; font-weight: bold; text-decoration: underline;">M. SYAHRIR, M.Sc.</div>
<div style="font-size: 9px; color: #475569;">LETNAN JENDERAL TNI</div>
{stamp_badge}
</div>
</div>
</div>"""

    elif doc_key == "doc_b":
        return """<div style="background: #FFFFFF; color: #0F172A; padding: 26px 30px; border-radius: 6px; box-shadow: 0 4px 20px rgba(0,0,0,0.45); font-family: 'Times New Roman', serif; position: relative; border: 2px solid #F59E0B;">
<div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
<div style="font-size: 9px; font-weight: bold; border: 1.5px solid #EA580C; color: #EA580C; padding: 1px 6px; border-radius: 2px; font-family: 'JetBrains Mono', monospace;">TERBATAS</div>
<div style="font-size: 9px; color: #EA580C; font-weight: bold; font-family: 'JetBrains Mono', monospace; background: rgba(234,88,12,0.12); padding: 2px 6px; border-radius: 3px;">TAMPER CONFIDENCE: 88.2%</div>
</div>
<div style="text-align: center; border-bottom: 2px solid #0F172A; padding-bottom: 6px; margin-bottom: 12px;">
<div style="font-size: 11px; font-weight: bold;">KEMENTERIAN PERTAHANAN REPUBLIK INDONESIA</div>
<div style="font-size: 10px; font-weight: bold;">DIREKTORAT JENDERAL PERENCANAAN PERTAHANAN</div>
<div style="font-size: 8.5px; color: #475569;">Gedung D.I. Pandjaitan Lt. 5, Jl. Medan Merdeka Barat No. 13-14</div>
<div style="font-size: 8px; color: #DC2626; font-family: monospace;">[ANOMALI TATA NASKAH: MISMATCH HIERARKI KEMHAN / MABES TNI]</div>
</div>
<div style="text-align: center; margin-bottom: 12px;">
<div style="font-size: 11px; font-weight: bold; text-decoration: underline;">LEMBAR PENGESAHAN ALOKASI ANGGARAN KHUSUS</div>
<div style="font-size: 9.5px; color: #475569; margin-top: 3px;">Nomor Registrasi: DIPA / 088 / BM / ALUTSISTA / X / 2026</div>
</div>
<div style="background: rgba(239, 68, 68, 0.12); border: 1.5px dashed #EF4444; border-radius: 4px; padding: 10px 14px; margin: 12px 0; text-align: center;">
<div style="font-size: 9px; color: #991B1B; font-weight: bold;">JUMLAH ALOKASI PENCAIRAN TERMIN I (FIKTIF):</div>
<div style="font-size: 14px; font-weight: bold; color: #DC2626; font-family: 'JetBrains Mono', monospace; margin: 4px 0;">Rp 847.500.000.000,-</div>
<div style="font-size: 8px; color: #B91C1C; font-family: monospace;">[ANOMALI ELA PEAK: DETEKSI SPLICING ANGKA NOMINAL]</div>
</div>
<div style="font-size: 9.5px; line-height: 1.5; color: #334155; margin-bottom: 16px;">
<div><b>Satuan Kerja:</b> Pusat Kesenjataan Artileri Pertahanan Udara (Pussenarhanud)</div>
<div><b>Program:</b> Modernisasi Radar Taktis Pertahanan Udara Wilayah Barat</div>
<div style="color: #DC2626; margin-top: 4px;"><b>Verifikasi Minu:</b> Kode rekening 088-BM tidak terdaftar dalam pagu DIPA APBN 2026.</div>
</div>
<div style="display: flex; justify-content: flex-end; margin-top: 16px;">
<div style="text-align: center; width: 200px;">
<div style="font-size: 9px;">Jakarta, 14 Oktober 2026</div>
<div style="font-size: 9.5px; font-weight: bold;">Pejabat Pembuat Komitmen,</div>
<div style="height: 50px; display: flex; align-items: center; justify-content: center; position: relative; margin: 3px 0;">
<div style="position: absolute; border: 1.5px dashed #EA580C; background: rgba(234,88,12,0.12); width: 55px; height: 55px; border-radius: 50%; font-size: 7px; color: #EA580C; display: flex; align-items: center; justify-content: center; font-weight: bold;">
CAP DINAS
</div>
<span style="font-family: 'Brush Script MT', cursive; font-size: 18px; color: #1E3A8A; z-index: 2;">Hendra W.</span>
</div>
<div style="font-size: 9.5px; font-weight: bold; text-decoration: underline;">Drs. HENDRA WIJAYA, M.Si.</div>
<div style="font-size: 8.5px; color: #64748B;">Pembina Utama Madya IV/d</div>
</div>
</div>
</div>"""

    else:
        # Document C (Golden Standard)
        return """<div style="background: #FFFFFF; color: #0F172A; padding: 26px 30px; border-radius: 6px; box-shadow: 0 4px 20px rgba(0,0,0,0.45); font-family: 'Times New Roman', serif; position: relative; border: 2px solid #10B981;">
<div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
<div style="font-size: 9px; font-weight: bold; border: 1.5px solid #10B981; color: #047857; padding: 1px 6px; border-radius: 2px; font-family: 'JetBrains Mono', monospace;">TERBUKA / OTENTIK</div>
<div style="font-size: 9px; color: #047857; font-weight: bold; font-family: 'JetBrains Mono', monospace; background: rgba(16,185,129,0.15); padding: 2px 6px; border-radius: 3px;">INTEGRITAS: 99.8% (VALID)</div>
</div>
<div style="text-align: center; border-bottom: 2px solid #0F172A; padding-bottom: 6px; margin-bottom: 12px;">
<div style="font-size: 11.5px; font-weight: bold; letter-spacing: 0.05em;">TENTARA NASIONAL INDONESIA ANGKATAN DARAT</div>
<div style="font-size: 10.5px; font-weight: bold;">DINAS PENERANGAN</div>
<div style="font-size: 9px; color: #475569;">Jalan Veteran No. 5 Jakarta Pusat - 10110</div>
<div style="font-size: 8px; color: #047857; font-family: monospace;">[KOP RESMI VEKTOR 300 DPI TERVERIFIKASI]</div>
</div>
<div style="text-align: center; margin-bottom: 14px;">
<div style="font-size: 12px; font-weight: bold; text-decoration: underline;">SURAT PERINTAH</div>
<div style="margin-top: 4px;">
<span style="font-size: 10px; font-weight: bold; background: rgba(16, 185, 129, 0.15); border: 1px solid #10B981; padding: 2px 8px; border-radius: 3px; color: #065F46;">
Nomor: Sprin / 104 / III / 2026-DISPENAD [REGISTER VALID]
</span>
</div>
</div>
<div style="font-size: 10px; line-height: 1.5; margin-bottom: 14px;">
<div style="margin-bottom: 4px;"><b>Pertimbangan:</b> Bahwa dalam rangka pelaksanaan program publikasi transparansi informasi pertahanan TNI AD...</div>
<div><b>Dasar:</b> Rencana Kerja Tahunan Dinas Penerangan TNI AD Tahun Anggaran 2026.</div>
</div>
<div style="text-align: center; font-size: 10px; font-weight: bold; letter-spacing: 0.15em; margin: 10px 0;">D I P E R I N T A H K A N</div>
<div style="font-size: 10px; line-height: 1.5; margin-bottom: 16px;">
<div><b>Kepada:</b> Tim Satgas Media Siber Dispenad</div>
<div style="margin-top: 4px;"><b>Untuk:</b> Melaksanakan audit informasi, pemantauan narasi disinformasi, dan publikasi klarifikasi resmi.</div>
</div>
<div style="display: flex; justify-content: space-between; align-items: flex-end; margin-top: 18px;">
<div style="border: 1px solid #10B981; background: rgba(16,185,129,0.06); padding: 8px 10px; border-radius: 4px; width: 140px; text-align: center;">
<div style="font-size: 8px; font-weight: bold; color: #047857; font-family: monospace;">QR TANDA TANGAN DIGITAL</div>
<div style="font-size: 16px; margin: 2px 0;">🛡️</div>
<div style="font-size: 7.5px; color: #475569;">BSrE BSSN Certified</div>
<div style="font-size: 7px; color: #059669; font-family: monospace;">SERI: 09-BSRE-2026</div>
</div>
<div style="text-align: center; width: 210px;">
<div style="font-size: 9.5px;">Ditetapkan di: Jakarta</div>
<div style="font-size: 9.5px;">pada tanggal: 10 Maret 2026</div>
<div style="font-size: 9.5px; font-weight: bold; margin-top: 4px;">KEPALA DINAS PENERANGAN TNI AD,</div>
<div style="height: 50px; display: flex; align-items: center; justify-content: center; position: relative; margin: 2px 0;">
<div style="position: absolute; left: 10px; border: 1.5px solid #1E3A8A; width: 60px; height: 60px; border-radius: 50%; display: flex; flex-direction: column; align-items: center; justify-content: center; font-size: 7px; color: #1E3A8A; font-weight: bold;">
<span>DISPENAD</span>
<span>★ MABESAD ★</span>
</div>
<span style="font-family: 'Brush Script MT', cursive; font-size: 18px; color: #1E3A8A; z-index: 2; margin-left: 20px;">Krisno W.</span>
</div>
<div style="font-size: 10px; font-weight: bold; text-decoration: underline;">KRISNO WIDODO</div>
<div style="font-size: 9px; color: #475569;">BRIGADIR JENDERAL TNI</div>
<div style="font-size: 8px; color: #047857; font-family: monospace; font-weight: bold;">[STEMPEL BASAH DENGAN MIKROGRAM OTENTIK]</div>
</div>
</div>
</div>"""

