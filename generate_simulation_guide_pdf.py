"""
scripts/generate_simulation_guide_pdf.py - Generates comprehensive, defense-grade
PDF guide and storyboard script for recording the SENTINEL-AD demonstration video.
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """Custom canvas that computes total pages and prints military footer on every page."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#DC2626"))
        
        # Header banner (military classification)
        self.drawCentredString(A4[0] / 2.0, A4[1] - 25, "KARTIKA CYBER HACKATHON 2026 // KATEGORI 04: SIBER SOSIAL (COGNITIVE DOMAIN)")
        
        # Top rule
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(36, A4[1] - 30, A4[0] - 36, A4[1] - 30)
        
        # Bottom rule
        self.line(36, 40, A4[0] - 36, 40)
        
        # Footer text
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(36, 26, "SENTINEL-AD | TNI AD Cognitive Defense & Threat Intelligence System")
        page_text = f"Halaman {self._pageNumber} dari {page_count}"
        self.drawRightString(A4[0] - 36, 26, page_text)
        self.restoreState()

def build_simulation_guide_pdf(output_path="PANDUAN_SIMULASI_VIDEO_SENTINEL_AD.pdf"):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=45,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()

    # Custom typography styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=18,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#0F172A')
    )

    subtitle_style = ParagraphStyle(
        'DocSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#475569')
    )

    badge_style = ParagraphStyle(
        'Badge',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#DC2626')
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=15,
        textColor=colors.HexColor('#0F172A'),
        spaceBefore=10,
        spaceAfter=4
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor('#1E3A8A'),
        spaceBefore=6,
        spaceAfter=2
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        alignment=TA_JUSTIFY,
        textColor=colors.HexColor('#1E293B')
    )

    body_bold = ParagraphStyle(
        'Body_Bold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#0F172A')
    )

    script_spoken = ParagraphStyle(
        'SpokenScript',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor('#0F172A')
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor('#0369A1')
    )

    elements = []

    # -------------------------------------------------------------
    # HEADER & TITLE BLOCK
    # -------------------------------------------------------------
    elements.append(Paragraph("KARTIKA CYBER HACKATHON 2026 // PUSSIBERAD × DISPENAD TNI AD", badge_style))
    elements.append(Spacer(1, 3))
    elements.append(Paragraph("PANDUAN OPERASIONAL & SKRIP REKAM LAYAR DEMO SIMULASI", title_style))
    elements.append(Spacer(1, 3))
    elements.append(Paragraph("Sistem Intelijen Siber & Pertahanan Kognitif Ruang Siber Sosial (SENTINEL-AD)<br/>Kategori 04: Siber Sosial (Cognitive Domain)", subtitle_style))
    elements.append(Spacer(1, 6))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#DC2626'), spaceBefore=2, spaceAfter=8))

    # -------------------------------------------------------------
    # METADATA & PREPARATION TABLE
    # -------------------------------------------------------------
    meta_data = [
        [
            Paragraph("<b>Nama Purwarupa:</b>", body_bold),
            Paragraph("SENTINEL-AD v2.5.0", body_style),
            Paragraph("<b>Target Lomba:</b>", body_bold),
            Paragraph("Kartika Cyber Hackathon 2026", body_style)
        ],
        [
            Paragraph("<b>Kategori Lomba:</b>", body_bold),
            Paragraph("Track 04: Siber Sosial", body_style),
            Paragraph("<b>Estimasi Durasi:</b>", body_bold),
            Paragraph("2 Menit s.d. 2 Menit 30 Detik", body_style)
        ],
        [
            Paragraph("<b>Tautan Aplikasi:</b>", body_bold),
            Paragraph("<code>http://localhost:8501</code> (Lokal)<br/><code>sentinel-ad.streamlit.app</code> (Online)", code_style),
            Paragraph("<b>Audio Pendukung:</b>", body_bold),
            Paragraph("<code>voiceover_demo.wav</code> (4.5 MB)", code_style)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[110, 160, 110, 143])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    elements.append(meta_table)
    elements.append(Spacer(1, 10))

    # -------------------------------------------------------------
    # SECTION 1: PERSIAPAN REKAM LAYAR (CHECKLIST)
    # -------------------------------------------------------------
    elements.append(Paragraph("I. CHECKLIST PERSIAPAN SEBELUM MEREKAM LAYAR", h1_style))
    prep_text = """
    Sebelum menekan tombol rekam layar, pastikan kondisi sistem memenuhi parameter berikut:<br/>
    1. <b>Pastikan Aplikasi Berjalan:</b> Buka peramban Chrome/Edge di alamat <code>http://localhost:8501</code> (atau <code>https://sentinel-ad.streamlit.app</code>). Tekan <b>F11</b> untuk mode layar penuh (*Fullscreen*) agar rekaman terlihat bersih dan profesional.<br/>
    2. <b>Resolusi & Aspek Rasio:</b> Gunakan resolusi 1920×1080 (1080p) pada rasio 16:9 agar nyaman ditonton dewan juri.<br/>
    3. <b>Alat Perekam Praktis (Pilih Salah Satu):</b><br/>
       • <b>Windows Game Bar:</b> Tekan tombol <code>Win + Alt + R</code> untuk langsung merekam layar.<br/>
       • <b>Snipping Tool Windows 11:</b> Tekan <code>Win + Shift + S</code>, pilih ikon video kamera, seleksi area layar, dan klik <i>Start</i>.<br/>
       • <b>OBS Studio / Canva:</b> Buka Canva di tab yang sudah terbuka, pilih fitur <i>Record Screen</i>, lalu gabungkan dengan berkas audio <code>voiceover_demo.wav</code>.<br/>
    4. <b>Sinkronisasi Suara:</b> Anda dapat membaca langsung teks narasi di bawah ini saat merekam, atau memutar berkas audio <code>voiceover_demo.wav</code> yang telah kami sediakan di repositori.
    """
    elements.append(Paragraph(prep_text, body_style))
    elements.append(Spacer(1, 10))

    # -------------------------------------------------------------
    # SECTION 2: RINGKASAN TIMELINE STORYBOARD
    # -------------------------------------------------------------
    elements.append(Paragraph("II. TABEL STORYBOARD & MATRIKS PENILAIAN JURI", h1_style))
    
    story_data = [
        [
            Paragraph("<b>Adegan / Waktu</b>", body_bold),
            Paragraph("<b>Modul Aplikasi</b>", body_bold),
            Paragraph("<b>Fokus Tindakan Layar</b>", body_bold),
            Paragraph("<b>Kriteria Penilaian Juri</b>", body_bold)
        ],
        [
            Paragraph("<b>Adegan 1</b><br/>00:00 - 00:20", body_style),
            Paragraph("Pusat Komando (C2 Overview)", body_style),
            Paragraph("Sorot radar DEFCON, Peta Sentimen 27 KODAM, dan tabel triage insiden.", body_style),
            Paragraph("<b>Sentiment Analysis</b><br/>Relevansi Manfaat (25%)", body_style)
        ],
        [
            Paragraph("<b>Adegan 2</b><br/>00:20 - 00:45", body_style),
            Paragraph("Ingesti & Loncatan Narasi", body_style),
            Paragraph("Tunjukkan perambatan isu dari kanal tertutup Telegram ke X & TikTok.", body_style),
            Paragraph("<b>Early Warning Isu</b><br/>Inovasi Teknis (25%)", body_style)
        ],
        [
            Paragraph("<b>Adegan 3</b><br/>00:45 - 01:25", body_style),
            Paragraph("CIB & Forensik Multimodal", body_style),
            Paragraph("Tab 1 (CIB <60s) ➔ Tab 2 (Audio Deepfake FFT) ➔ Tab 3 (Sprin Palsu ELA).", body_style),
            Paragraph("<b>Buzzer/Bot & Hoax</b><br/>Inovasi & Fungsional (50%)", body_style)
        ],
        [
            Paragraph("<b>Adegan 4</b><br/>01:25 - 01:50", body_style),
            Paragraph("Wargaming Sandbox", body_style),
            Paragraph("Simulasi naskah klarifikasi Dispenad pada 10 persona & Backfire Risk.", body_style),
            Paragraph("<b>Sentiment & Counter</b><br/>Relevansi Militer (25%)", body_style)
        ],
        [
            Paragraph("<b>Adegan 5</b><br/>01:50 - 02:10", body_style),
            Paragraph("Graf Jaringan (SNA)", body_style),
            Paragraph("Eksplorasi graf interaktif PyVis, simpul Seed, Bridge, & ekspor Excel.", body_style),
            Paragraph("<b>Social Network Analysis</b><br/>Fungsionalitas Purwarupa", body_style)
        ],
        [
            Paragraph("<b>Adegan 6</b><br/>02:10 - 02:35", body_style),
            Paragraph("Tactical SOAR & Rantai Komando", body_style),
            Paragraph("Otorisasi tanda tangan komandan, unduh SITREP PDF & Dossier BSSN.", body_style),
            Paragraph("<b>Kelayakan Operasional</b><br/>Kesiapan Doktrin (15%)", body_style)
        ]
    ]

    story_table = Table(story_data, colWidths=[80, 115, 185, 143])
    story_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F172A')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#FFFFFF'), colors.HexColor('#F8FAFC')])
    ]))
    elements.append(story_table)
    elements.append(Spacer(1, 10))

    # -------------------------------------------------------------
    # SECTION 3: SKRIP DETAIL ADEGAN DEMI ADEGAN
    # -------------------------------------------------------------
    elements.append(Paragraph("III. SKRIP LENGKAP DETAIL ADEGAN & TEKS BICARA", h1_style))

    scenes = [
        {
            "num": "1",
            "time": "00:00 - 00:20 (20 Detik)",
            "title": "PEMBUKA & PUSAT KOMANDO (C2 OVERVIEW)",
            "action": "Arahkan kursor ke Header atas (DEFCON 3 dan Badge Hackathon Kategori 04). Scroll pelan ke bawah menampilkan Peta Interaktif 27 KODAM se-Indonesia dan Radar Insiden Prioritas.",
            "spoken": '"Selamat pagi dan salam tangguh. Izin Komandan dan Dewan Juri Kartika Cyber Hackathon 2026. Berikut adalah demonstrasi operasional SENTINEL-AD, Sistem Intelijen Siber dan Pertahanan Kognitif Generasi Baru untuk TNI Angkatan Darat. Di halaman awal Pusat Komando C2, pimpinan dapat memantau kesiapsiagaan DEFCON dan sentimen teritorial di dua puluh tujuh Kodam se-Indonesia secara real-time."',
            "highlight": "Menunjukkan kesiapan platform command-and-control terintegrasi sesuai doktrin teritorial TNI AD."
        },
        {
            "num": "2",
            "time": "00:20 - 00:45 (25 Detik)",
            "title": "MODUL INGESTI & LONCATAN NARASI (NARRATIVE JUMP TRACKER)",
            "action": "Di menu navigasi kiri, klik '📡 Ingesti & Loncatan Narasi'. Scroll ke bawah menyoroti grafik Narrative Jump, metrik Jump Velocity (14 menit), dan tabel stream umpan berita multi-platform.",
            "spoken": '"Modul kedua adalah Ingesti dan Loncatan Narasi. Sistem ini mendeteksi propagasi disinformasi lintas ekosistem. Terlihat narasi hoaks bermula dari kanal tertutup Telegram, lalu meloncat ke linimasa publik X dan TikTok hanya dalam waktu 14 menit dengan amplifikasi volume 154 kali lipat sebelum viral di media daring."',
            "highlight": "Memenuhi syarat rubrik 'Early Warning Isu Viral' dengan algoritma deteksi loncatan narasi."
        },
        {
            "num": "3A",
            "time": "00:45 - 01:00 (15 Detik)",
            "title": "CIB SCREENER: SINKRONISASI WAKTU BOTNET (<60 DETIK)",
            "action": "Klik '🔍 CIB & Deepfake Screener'. Buka 'TAB 1: SINKRONISASI WAKTU CIB'. Scroll ke bawah memperlihatkan klaster botnet yang mengunggah narasi secara serempak.",
            "spoken": '"Modul ketiga adalah CIB Screener dan Forensik Multimodal. Pada Tab 1, sistem mengaudit operasi Coordinated Inauthentic Behavior. Algoritma kami mendeteksi ratusan akun botnet yang memviralkan isu secara serentak dalam jendela waktu kurang dari 60 detik."',
            "highlight": "Memenuhi syarat rubrik 'Buzzer/Bot Detection' dengan analisis temporal sinkronisitas."
        },
        {
            "num": "3B",
            "time": "01:00 - 01:15 (15 Detik)",
            "title": "CIB SCREENER: AUDIT SPEKTROGRAM AUDIO DEEPFAKE",
            "action": "Klik '🎙️ TAB 2: AUDIT SPEKTROGRAM AUDIO DEEPFAKE'. Scroll ke waveform gelombang suara dan analisis spektral cutoff 16 kHz.",
            "spoken": '"Pada Tab 2, rekaman audio kloning suara pejabat militer diuji menggunakan Fast Fourier Transform akustik. Terdeteksi pemotongan frekuensi buatan vocoder di atas 16 kilohertz serta ketiadaan jeda pernapasan biologis, membuktikan rekaman 88% sintetis buatan kecerdasan artifisial."',
            "highlight": "Memenuhi syarat rubrik 'Hoax Classifier' tingkat tinggi (Forensik Audio Sintetis)."
        },
        {
            "num": "3C",
            "time": "01:15 - 01:30 (15 Detik)",
            "title": "CIB SCREENER: INTEGRITAS DOKUMEN MILITER & OCR HIGHLIGHT",
            "action": "Klik '📄 TAB 3: INTEGRITAS DOKUMEN & HIGHLIGHT OCR'. Tunjukkan kotak merah font Courier New, stempel rotasi 14.2°, lalu klik 'Lapisan 2: Heatmap Forensik ELA' dan tunjukkan status register Minu Mabesad.",
            "spoken": '"Pada Tab 3, surat perintah mutasi palsu diuji dengan OCR tipografi dan Error Level Analysis (ELA). Sistem mendeteksi anomali font Courier New, stempel digital dengan rotasi 14.2 derajat, serta ketiadaan nomor register di Buku Agenda Minu Mabesad."',
            "highlight": "Pembeda inovasi utama: Perlindungan integritas naskah dinas militer TNI AD (Jukminu No. 12/IV/2021)."
        },
        {
            "num": "4",
            "time": "01:30 - 01:50 (20 Detik)",
            "title": "COGNITIVE WARGAMING SANDBOX (SIMULASI RESPON PUBLIK)",
            "action": "Klik '🧠 Wargaming Sandbox Persona'. Scroll ke bawah menyoroti simulasi respon dari 10 persona masyarakat (Nasionalis, Santri, Gen-Z, Buzzer) dan persentase Backfire Risk.",
            "spoken": '"Modul keempat adalah Cognitive Wargaming Sandbox. Sebelum Dispenad merilis naskah klarifikasi, narasi diuji secara multi-agen terhadap sepuluh persona masyarakat guna memprediksi pergeseran sentimen dan menekan risiko bumerang publik ke tingkat aman."',
            "highlight": "Inovasi perang kognitif pertahanan: Menghindari blunder komunikasi publik militer."
        },
        {
            "num": "5",
            "time": "01:50 - 02:10 (20 Detik)",
            "title": "GRAF JARINGAN ANCAMAN (SNA THREAT TOPOLOGY)",
            "action": "Klik '🕸️ Graf Jaringan Ancaman (SNA)'. Arahkan mouse ke simpul Seed merah, Amplifier oranye, dan Bridge kuning. Tunjukkan tombol unduh Excel & CSV.",
            "spoken": '"Modul kelima adalah Graf Jaringan Ancaman atau Social Network Analysis. Memetakan topologi jaringan aktor disinformasi, memisahkan akun inisiator Seed, klaster botnet amplifikasi, serta kanal jembatan. Data intelijen dapat langsung diekspor ke format Excel dan CSV."',
            "highlight": "Memenuhi syarat rubrik 'Social Network Analysis (SNA)' lengkap dengan metrik sentralitas."
        },
        {
            "num": "6",
            "time": "02:10 - 02:35 (25 Detik)",
            "title": "TACTICAL SOAR, SITREP PDF & DOSSIER TAKEDOWN BSSN",
            "action": "Klik '⚡ Tactical SOAR & Otorisasi'. Tunjukkan antrean persetujuan Komandan, tanda tangan digital, lalu klik tombol 'Unduh SITREP PDF' dan 'Unduh Dossier BSSN JSON'.",
            "spoken": '"Dan modul keenam adalah Tactical SOAR. Mengotomatisasi penindakan berjenjang rantai komando. Komandan mengesahkan penindakan dengan tanda tangan digital, menerbitkan dokumen Laporan Situasi Militer (SITREP) PDF resmi berstempel rahasia, serta dossier JSON berstempel SHA-256 untuk takedown cepat ke BSSN dan Kominfo."',
            "highlight": "Membuktikan kesiapan operasional nyata (Relevansi dan Manfaat 25%)."
        },
        {
            "num": "7",
            "time": "02:35 - 02:45 (10 Detik)",
            "title": "PENUTUP & DOKTRIN PERTAHANAN KOGNITIF",
            "action": "Kembali ke Pusat Komando atau sorot logo SENTINEL-AD TNI AD.",
            "spoken": '"SENTINEL-AD siap digelar di intranet tertutup MILNET Mabesad secara berdaulat tanpa bergantung pada klaster GPU mahal. Siap menjaga keutuhan NKRI di ranah siber sosial. Terima kasih. Cakra!"',
            "highlight": "Closing statement yang percaya diri, patriotik, dan meyakinkan dewan juri."
        }
    ]

    for sc in scenes:
        box_data = [
            [
                Paragraph(f"<b>ADEGAN {sc['num']} [{sc['time']}]: {sc['title']}</b>", body_bold),
            ],
            [
                Paragraph(f"<b>Tindakan Kursor & Layar:</b> {sc['action']}", body_style),
            ],
            [
                Paragraph(f"<b>Teks Lisan / Narasi Suara:</b><br/>{sc['spoken']}", script_spoken),
            ],
            [
                Paragraph(f"<b>Fokus Kriteria Juri:</b> <font color='#1E3A8A'>{sc['highlight']}</font>", body_style),
            ]
        ]
        sc_table = Table(box_data, colWidths=[523])
        sc_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E2E8F0')),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#FFFFFF'), colors.HexColor('#F8FAFC'), colors.HexColor('#FFFFFF')])
        ]))
        elements.append(KeepTogether([sc_table, Spacer(1, 6)]))

    # -------------------------------------------------------------
    # SECTION 4: CARA CEPAT MENGGABUNGKAN VIDEO & AUDIO
    # -------------------------------------------------------------
    elements.append(Spacer(1, 6))
    elements.append(Paragraph("IV. PANDUAN PENGGABUNGAN CEPAT VIDEO & AUDIO (CANVA / CAPCUT / CLIPCHAMP)", h1_style))
    merge_text = """
    Setelah selesai merekam layar selama 2 s.d. 2,5 menit, gabungkan video dengan audio narasi dengan langkah berikut:<br/>
    1. <b>Buka Canva Video / CapCut / Clipchamp (Bawaan Windows 11):</b><br/>
       • Buat proyek video baru format 16:9 (1920×1080).<br/>
       • Tarik berkas rekaman layar Anda ke dalam linimasa video.<br/>
       • Tarik berkas <code>voiceover_demo.wav</code> dari folder proyek ke linimasa audio.<br/>
    2. <b>Sesuaikan Kecepatan (Speed / Trimming):</b> Potong bagian jeda awal/akhir rekaman agar pas dengan ketukan narasi suara <code>voiceover_demo.wav</code>.<br/>
    3. <b>Ekspor:</b> Klik tombol <i>Export / Unduh</i> sebagai <b>MP4 1080p</b>. Video demonstrasi resmi Anda siap diunggah ke formulir registrasi <b>Kartika Cyber Hackathon 2026</b>!
    """
    elements.append(Paragraph(merge_text, body_style))
    elements.append(Spacer(1, 8))

    # Build PDF with custom NumberedCanvas
    doc.build(elements, canvasmaker=NumberedCanvas)
    print(f"PDF Guide successfully generated at: {output_path}")

if __name__ == "__main__":
    build_simulation_guide_pdf("PANDUAN_SIMULASI_VIDEO_SENTINEL_AD.pdf")
