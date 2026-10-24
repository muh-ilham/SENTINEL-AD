"""
modules/ingestion_tracker.py - Multi-Platform Ingestion & Narrative Jump Tracker
Monitors real-time threat feed with defense lexicon filters and visualizes cross-platform narrative propagation.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
from utils.data_generator import generate_threat_feed, PRIMARY_INCIDENTS, KODAM_REGIONS

DEFENSE_LEXICON = [
    "Panglima TNI", "KSAD", "Pussiberad", "Dispenad", "Kodam", "Kodam XIV/Hasanuddin", "Korem", "Kodim",
    "Babinsa", "Makassar", "Separatisme", "SARA", "Perbatasan RI-PNG", "Natuna", "Alutsista",
    "Latma (Latihan Bersama)", "Mutasi Pejabat", "Tunjangan Kinerja", "Operasi Militer"
]

def render_ingestion_tracker():
    """Renders the Ingestion Feed and Narrative Jump analysis module."""
    st.markdown("## 📡 INGESTI MULTI-PLATFORM & NARRATIVE JUMP TRACKER")
    st.markdown(
        "<p style='color: #94A3B8; font-size: 0.95rem; margin-top: -10px;'>"
        "Sistem deteksi dini perambatan disinformasi lintas ekosistem (Telegram, X, TikTok, YouTube, & Berita Online)."
        "</p>",
        unsafe_allow_html=True
    )
    
    # Tabs: Feed Monitoring vs Narrative Jump Analysis vs Kodam Territorial Focus
    tab_jump, tab_feed, tab_hasanuddin = st.tabs([
        "🚀 VISUALISASI NARRATIVE JUMP", 
        "📋 STREAM UMPAN ANCAMAN REAL-TIME", 
        "📍 RADAR MONITORING 27 KODAM (LIVE DATA)"
    ])
    
    feed_df = generate_threat_feed(70)
    
    # -------------------------------------------------------------
    # TAB 1: NARRATIVE JUMP VISUALIZER
    # -------------------------------------------------------------
    with tab_jump:
        st.markdown("### 🔀 ANALISIS PROPAGASI LINTAS PLATFORM (CROSS-PLATFORM SPREAD)")
        st.markdown(
            "Visualisasi alur perpindahan isu dari kanal tertutup (Closed Darknet / Telegram) "
            "menuju ranah terbuka beramplifikasi tinggi (X / TikTok) hingga dikutip oleh agregator berita online."
        )
        
        # Incident Selector
        incident_titles = [inc["title"] for inc in PRIMARY_INCIDENTS]
        selected_title = st.selectbox(
            "🎯 Pilih Kasus Insiden Operasi Kognitif untuk Dianalisis:",
            incident_titles,
            index=0
        )
        
        # Retrieve Incident Profile
        curr_inc = next(item for item in PRIMARY_INCIDENTS if item["title"] == selected_title)
        
        # Top Incident Metadata Card
        st.markdown(
            f"""
            <div class="tactical-card danger" style="padding: 16px 20px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <span style="font-family: 'JetBrains Mono'; font-weight: 800; color: #38BDF8;">
                        IDENTIFIER: {curr_inc['id']}
                    </span>
                    <span class="status-pill pill-critical">TINGKAT: {curr_inc['level'].upper()}</span>
                </div>
                <h4 style="margin: 0 0 6px 0; color: #F8FAFC;">{curr_inc['title']}</h4>
                <div style="font-size: 0.85rem; color: #CBD5E1; margin-bottom: 10px;">
                    {curr_inc['sample_text']}
                </div>
                <div style="display: flex; gap: 15px; font-family: 'JetBrains Mono'; font-size: 0.78rem;">
                    <span style="color: #94A3B8;">Kategori: <b style="color: #F8FAFC;">{curr_inc['category']}</b></span>
                    <span style="color: #94A3B8;">Titik Awal (Origin): <b style="color: #22D3EE;">{curr_inc['root_platform']}</b></span>
                    <span style="color: #94A3B8;">Target Wilayah: <b style="color: #F59E0B;">{curr_inc['target_kodam']}</b></span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # 4 Ringkasan Metrik Propagasi Lintas Platform
        m_col1, m_col2, m_col3, m_col4 = st.columns(4)
        with m_col1:
            st.metric("Kecepatan Loncatan (Jump Velocity)", "14 Menit", "Inisiasi ➔ X (Super Cepat)", help="Waktu yang dibutuhkan isu dari unggahan pertama di kanal tertutup hingga muncul di linimasa terbuka X (Twitter).")
        with m_col2:
            st.metric("Faktor Ledakan Volume", "1 : 154x", "Amplifikasi Botnet", help="Perbandingan volume penonton dari saluran tertutup (1.2K) melonjak menjadi ratusan ribu setelah masuk TikTok & WhatsApp.")
        with m_col3:
            st.metric("Titik Kritis Loncatan", "X ➔ TikTok", "Konversi Teks ke Video", help="Fase paling berbahaya di mana narasi teks diubah menjadi video pendek emosional yang memicu viralitas massal.")
        with m_col4:
            st.metric("Jendela Emas Intervensi", "< 60 Menit", "Golden Defense Hour", help="Batas waktu ideal bagi tim siber untuk melakukan klarifikasi/takedown sebelum isu menyebar ke WhatsApp grup warga.")

        st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
        
        col_sankey, col_stages = st.columns([7, 5])
        
        with col_sankey:
            st.markdown("#### 🌊 Diagram Sankey Transmisi Volume & Konversi Platform")
            st.caption("Visualisasi aliran volume konten hoaks berpindah dari kanal rahasia (kiri) menuju ruang publik warga (kanan):")
            
            # Dynamic Clean Sankey Diagram with Explicit Coordinates
            node_labels = [
                f"1️⃣ {curr_inc['root_platform']}<br>(Kanal Tertutup / Asal)",
                "2️⃣ X / Twitter<br>(Amplifikasi Bot)",
                "3️⃣ TikTok & Reels<br>(Klip Video Viral)",
                "4️⃣ Media Daring<br>(Agregator Berita)",
                "5️⃣ YouTube<br>(Ulasan Opini)",
                "6️⃣ Publik & WhatsApp<br>(Persepsi Luas)"
            ]
            
            # Explicit left-to-right positioning for clean, readable hierarchy
            x_coords = [0.01, 0.28, 0.55, 0.55, 0.78, 0.99]
            y_coords = [0.50, 0.35, 0.15, 0.85, 0.25, 0.55]
            node_colors = ["#EF4444", "#06B6D4", "#EC4899", "#8B5CF6", "#F59E0B", "#10B981"]
            
            # Flow links with realistic volume conversions
            source_indices = [0, 0, 1, 1, 2, 4, 3]
            target_indices = [1, 2, 2, 3, 4, 5, 5]
            flow_values =    [85, 35, 65, 40, 50, 75, 45]
            
            fig_sankey = go.Figure(data=[go.Sankey(
                arrangement="snap",
                node=dict(
                    pad=22,
                    thickness=22,
                    line=dict(color="#0F172A", width=1.5),
                    label=node_labels,
                    x=x_coords,
                    y=y_coords,
                    color=node_colors,
                    hovertemplate='<b>%{label}</b><br>Estimasi Volume: <b>%{value:,} Konten/Sebaran</b><extra></extra>'
                ),
                link=dict(
                    source=source_indices,
                    target=target_indices,
                    value=flow_values,
                    color=[
                        "rgba(6, 182, 212, 0.40)",
                        "rgba(236, 72, 153, 0.35)",
                        "rgba(236, 72, 153, 0.50)",
                        "rgba(139, 92, 246, 0.40)",
                        "rgba(245, 158, 11, 0.50)",
                        "rgba(16, 185, 129, 0.50)",
                        "rgba(16, 185, 129, 0.50)"
                    ],
                    hovertemplate='Transmisi: <b>%{source.label}</b> ➔ <b>%{target.label}</b><br>Volume Loncatan: <b>%{value:,} Unit Sebaran</b><extra></extra>'
                )
            )])
            
            fig_sankey.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="JetBrains Mono", size=11, color="#F8FAFC"),
                margin=dict(t=25, b=20, l=15, r=15),
                height=390
            )
            st.plotly_chart(fig_sankey, use_container_width=True)
            
            # Panduan Edukasi Bahasa Awam Membaca Diagram Sankey
            with st.expander("💡 BAGAIMANA CARA MEMBACA & APA MAKSUD DARI DIAGRAM SANKEY INI? (KLIK UNTUK MEMBACA)", expanded=True):
                st.markdown(
                    """
                    **1. 🌊 Analogi 'Aliran Pipa Corong':**  
                    Diagram Sankey ini ibarat peta pipa aliran air. **Sisi Kiri (Hulu)** adalah tempat pertama kali hoaks dibuat, dan **Sisi Kanan (Hilir)** adalah tempat hoaks bermuara di masyarakat umum. Semakin tebal pita warna, semakin besar volume konten yang berpindah.

                    **2. 🔄 4 Tahap Loncatan Lintas Media:**  
                    • **Tahap 1 (Merah - Kiri):** Isu palsu sengaja dilempar di kanal tertutup (Telegram / Darknet) agar dalang aslinya tidak terlacak.  
                    • **Tahap 2 (Biru Muda):** Pasukan akun botnet menggandakan isu tersebut ke **X (Twitter)** agar masuk daftar trending topic.  
                    • **Tahap 3 (Pink & Ungu):** Kreator video mengemasnya menjadi video vertikal dramatis di **TikTok & Reels**, sementara portal berita online mulai mengutipnya demi klik/iklan.  
                    • **Tahap 4 (Hijau - Kanan):** Isu meledak menjadi konsumsi umum dan masuk ke grup-grup **WhatsApp keluarga/warga**.

                    **3. 🛡️ Sasaran Taktis Militer TNI AD:**  
                    Operasi pertahanan siber harus memotong aliran pipa pada **Tahap 2 (X) atau Tahap 3 (TikTok)** dalam kurun waktu **<60 menit (Golden Hour)** sebelum menyentuh WhatsApp masyarakat agar wibawa institusi dan ketenangan publik tetap terjaga.
                    """
                )
            
        with col_stages:
            st.markdown("#### ⏱️ Linimasa Tahapan Loncatan (Jump Velocity)")
            st.caption("Kronologi waktu loncatan dari inisiasi hingga resonansi publik:")
            
            stages = [
                {
                    "stage": "Tahap 1: Inisiasi (T+00:00)",
                    "platform": curr_inc["root_platform"],
                    "actor": "Akun Anonim Darknet / Channel Khusus",
                    "action": "Unggahan perdana audio/dokumen manipulasi.",
                    "audience": "1.2K Views",
                    "status_color": "#EF4444",
                    "latency": "Titik Awal (0 Menit)"
                },
                {
                    "stage": "Tahap 2: Amplifikasi X (T+00:14m)",
                    "platform": "X (Twitter)",
                    "actor": "Klaster 48 Akun CIB Terkoordinasi",
                    "action": "Penyebaran masif dengan tagar provokatif dan potongan narasi.",
                    "audience": "24.5K Impressions",
                    "status_color": "#06B6D4",
                    "latency": "+14 Menit Loncatan"
                },
                {
                    "stage": "Tahap 3: Visualisasi Viral (T+00:48m)",
                    "platform": "TikTok & IG Reels",
                    "actor": "Akun Agregator Konten Militer",
                    "action": "Dibuat video format vertikal dengan latar belakang dramatis & audio synthesizer.",
                    "audience": "185.0K Plays",
                    "status_color": "#EC4899",
                    "latency": "+34 Menit Loncatan"
                },
                {
                    "stage": "Tahap 4: Spillover Arus Utama (T+02:15j)",
                    "platform": "Media Online & WhatsApp Group",
                    "actor": "Portal Berita Clickbait & Komunitas Warga",
                    "action": "Muncul artikel spekulasi dan diteruskan berantai ke grup percakapan keluarga.",
                    "audience": "Publik Luas / Resonansi Nasional",
                    "status_color": "#10B981",
                    "latency": "+87 Menit Loncatan"
                }
            ]
            
            for stg in stages:
                card_html = f"""
                <div style="
                    border-left: 3px solid {stg['status_color']};
                    background: #111C2E;
                    padding: 10px 14px;
                    border-radius: 0 6px 6px 0;
                    margin-bottom: 10px;
                    font-size: 0.8rem;
                ">
                    <div style="display: flex; justify-content: space-between; font-family: 'JetBrains Mono'; font-size: 0.72rem; color: #38BDF8;">
                        <span>{stg['stage']}</span>
                        <span style="color: {stg['status_color']}; font-weight: bold; background: rgba(0,0,0,0.3); padding: 1px 6px; border-radius: 3px;">{stg['platform']}</span>
                    </div>
                    <div style="font-weight: 600; color: #F8FAFC; margin: 4px 0; line-height: 1.4;">{stg['action']}</div>
                    <div style="display: flex; justify-content: space-between; color: #94A3B8; font-size: 0.72rem; font-family: 'JetBrains Mono'; margin-top: 4px;">
                        <span>👤 Aktor: {stg['actor']}</span>
                        <span style="color: #34D399; font-weight: bold;">{stg['audience']}</span>
                    </div>
                    <div style="font-size: 0.68rem; color: #F59E0B; font-family: 'JetBrains Mono'; margin-top: 2px;">
                        ⏱️ Latensi Transmisi: {stg['latency']}
                    </div>
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)

    # -------------------------------------------------------------
    # TAB 2: REAL-TIME FEED WITH FILTERS
    # -------------------------------------------------------------
    with tab_feed:
        st.markdown("### 📋 UMPAN TELEMETRI ANCAMAN SIBER REAL-TIME")
        
        # Filter Bar in columns
        f_col1, f_col2, f_col3, f_col4 = st.columns(4)
        
        with f_col1:
            sel_plat = st.multiselect(
                "Filter Platform:",
                options=["Semua"] + list(feed_df["platform"].unique()),
                default=["Semua"]
            )
            
        with f_col2:
            sel_level = st.multiselect(
                "Tingkat Ancaman:",
                options=["Semua", "Kritis", "Tinggi", "Sedang", "Rendah"],
                default=["Semua"]
            )
            
        with f_col3:
            sel_kodam = st.selectbox(
                "Wilayah Kodam:",
                options=["Semua Kodam"] + list(KODAM_REGIONS.keys())
            )
            
        with f_col4:
            sel_term = st.selectbox(
                "Kamus Istilah Pertahanan:",
                options=["Semua Istilah"] + DEFENSE_LEXICON
            )
            
        # Apply Filters
        filtered_df = feed_df.copy()
        
        if "Semua" not in sel_plat and sel_plat:
            filtered_df = filtered_df[filtered_df["platform"].isin(sel_plat)]
            
        if "Semua" not in sel_level and sel_level:
            filtered_df = filtered_df[filtered_df["threat_level"].isin(sel_level)]
            
        if sel_kodam != "Semua Kodam":
            filtered_df = filtered_df[filtered_df["kodam"] == sel_kodam]
            
        if sel_term != "Semua Istilah":
            filtered_df = filtered_df[filtered_df["text"].str.contains(sel_term, case=False, na=False) | 
                                      filtered_df["headline"].str.contains(sel_term, case=False, na=False)]
                                      
        st.markdown(
            f"<div style='font-family: JetBrains Mono; font-size: 0.8rem; color: #22D3EE; margin: 8px 0;'>"
            f"Ditemukan {len(filtered_df)} entri telemetri terfilter dari total {len(feed_df)} pemantauan sensor."
            f"</div>",
            unsafe_allow_html=True
        )
        
        # Format DataFrame for high-tech display
        display_cols = ["id", "timestamp", "platform", "kodam", "threat_level", "headline", "virality_score", "cib_probability", "status"]
        
        st.dataframe(
            filtered_df[display_cols],
            column_config={
                "id": st.column_config.TextColumn("ID Telemetri", width="small"),
                "timestamp": st.column_config.TextColumn("Waktu (WIB)", width="small"),
                "platform": st.column_config.TextColumn("Platform", width="small"),
                "kodam": st.column_config.TextColumn("Yurisdiksi Kodam", width="medium"),
                "threat_level": st.column_config.TextColumn("Tingkat", width="small"),
                "headline": st.column_config.TextColumn("Deskripsi Deteksi", width="large"),
                "virality_score": st.column_config.ProgressColumn("Virality", min_value=0, max_value=100, format="%d"),
                "cib_probability": st.column_config.ProgressColumn("CIB / Bot %", min_value=0, max_value=100, format="%d%%"),
                "status": st.column_config.TextColumn("Status Penanganan", width="medium")
            },
            hide_index=True,
            use_container_width=True,
            height=400
        )

    # -------------------------------------------------------------
    # TAB 3: RADAR KHUSUS KODAM XIV/HASANUDDIN (LIVE DATA)
    # -------------------------------------------------------------
    with tab_hasanuddin:
        st.markdown("### 📍 MONITORING INTELIJEN SIBER & MEDIA SOSIAL SATUAN TERITORIAL KODAM")
        st.markdown(
            "<p style='color: #94A3B8; font-size: 0.9rem; margin-top: -8px;'>"
            "Pemantauan terintegrasi percakapan media sosial (TikTok, Instagram, X, Facebook, YouTube, Media Daring) di 27 Komando Daerah Militer se-Indonesia."
            "</p>",
            unsafe_allow_html=True
        )
        
        c_sel_k, c_sync_k = st.columns([8, 4])
        with c_sel_k:
            selected_deep_kodam = st.selectbox(
                "Pilih Wilayah Kodam Teritorial (27 Kodam):",
                options=list(KODAM_REGIONS.keys()),
                index=list(KODAM_REGIONS.keys()).index("Kodam XIV/Hasanuddin") if "Kodam XIV/Hasanuddin" in KODAM_REGIONS else 0,
                key="tracker_deep_kodam_sel"
            )
        with c_sync_k:
            st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
            if st.button("📡 Sinkronkan Telemetri Satuan", type="primary", use_container_width=True, key="btn_sync_deep_kodam"):
                st.session_state["live_feed_cache"] = None
                st.toast(f"Telemetri intelijen teritorial {selected_deep_kodam} berhasil disinkronkan!", icon="📍")
                st.rerun()

        k_info = KODAM_REGIONS.get(selected_deep_kodam, {})
        k_abbr = k_info.get("abbr", "KODAM")
        k_hq = k_info.get("hq", "Indonesia")
        k_prov = k_info.get("province", "Teritorial")

        # Kodam Profile Card
        st.markdown(
            f"""
            <div style="background: linear-gradient(135deg, #111C2E 0%, #0F172A 100%); border: 1px solid #334155; border-left: 4px solid #06B6D4; padding: 14px 18px; border-radius: 6px; margin-bottom: 16px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                    <span style="font-family: 'Chakra Petch'; font-size: 1.15rem; font-weight: bold; color: #FFFFFF;">
                        KOMANDO DAERAH MILITER {selected_deep_kodam.upper()} [{k_abbr}]
                    </span>
                    <span style="font-family: 'JetBrains Mono'; font-size: 0.72rem; color: #10B981; background: rgba(16,185,129,0.15); border: 1px solid #10B981; padding: 2px 8px; border-radius: 12px; font-weight: bold;">
                        STATUS: TERKONEKSI SENSOR LIVE
                    </span>
                </div>
                <div style="font-size: 0.82rem; color: #94A3B8; margin-bottom: 8px;">
                    Wilayah Pertahanan: <b style="color: #22D3EE;">{k_prov}</b> | Markas Komando: <b>{k_hq}</b>
                </div>
                <div style="display: flex; flex-wrap: wrap; gap: 14px; font-family: 'JetBrains Mono'; font-size: 0.74rem;">
                    <span style="color: #CBD5E1;">🌐 Yurisdiksi: <b style="color: #38BDF8;">Pangdam & Danrem Jajaran</b></span>
                    <span style="color: #CBD5E1;">📡 Radar: <b style="color: #E2E8F0;">TikTok, IG, X, FB, YT, Media Daring</b></span>
                    <span style="color: #CBD5E1;">⚔️ Gelar Pasukan: <b style="color: #F59E0B;">Korem • Kodim • Koramil • Babinsa</b></span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        col_real_news, col_social_track = st.columns([7, 5])
        kodam_threats = feed_df[feed_df["kodam"] == selected_deep_kodam]
        
        with col_real_news:
            st.markdown(f"#### 📰 Telemetri Isu Teritorial ({selected_deep_kodam})")
            
            if not kodam_threats.empty:
                for _, row in kodam_threats.iterrows():
                    th_color = "#EF4444" if row["threat_level"] == "Kritis" else ("#F59E0B" if row["threat_level"] == "Tinggi" else "#38BDF8")
                    card_html = f"""
                    <div style="background: #111C2E; border: 1px solid #1E293B; border-left: 3px solid {th_color}; padding: 10px 14px; border-radius: 4px; margin-bottom: 8px;">
                        <div style="display: flex; justify-content: space-between; font-family: 'JetBrains Mono'; font-size: 0.7rem; color: #94A3B8; margin-bottom: 2px;">
                            <span>🕒 {row['timestamp'][:19]} • {row['platform']}</span>
                            <span style="color: {th_color}; font-weight: bold;">{row['threat_level']} (CIB: {row['cib_probability']}%)</span>
                        </div>
                        <div style="font-weight: 700; color: #F8FAFC; font-size: 0.85rem; margin-bottom: 4px;">{row['headline']}</div>
                        <div style="font-size: 0.78rem; color: #CBD5E1; line-height: 1.35;">{row['text']}</div>
                    </div>
                    """
                    st.markdown(card_html, unsafe_allow_html=True)
            elif selected_deep_kodam == "Kodam XIV/Hasanuddin":
                real_articles = [
                    {
                        "title": "HUT ke-81 TNI Digelar Sederhana, 1.992 Prajurit Tiga Matra Teguhkan Soliditas dan Empati",
                        "date": "05 Oktober 2026",
                        "author": "Operator Kodam XIV Hasanuddin",
                        "category": "Operasional & Soliditas Tiga Matra",
                        "summary": "Peringatan HUT TNI ke-81 dipusatkan di Makassar melibatkan ribuan prajurit TNI AD, AL, dan AU dengan fokus peneguhan empati kemasyarakatan dan stabilitas wilayah."
                    },
                    {
                        "title": "Terima Kunjungan Deputi Geoekonomi DPN, Pangdam XIV/Hasanuddin Dukung Ketahanan Nasional",
                        "date": "30 September 2026",
                        "author": "Operator Kodam XIV Hasanuddin",
                        "category": "Geoekonomi & Ketahanan Pangan",
                        "summary": "Pangdam Mayjen TNI menerima audiensi penguatan ketahanan pangan strategis dan integrasi logistik teritorial di koridor Sulawesi Selatan dan Tenggara."
                    },
                    {
                        "title": "Atlet Pentathlon Kodam Hasanuddin Ukir Prestasi Gemilang, Juara 1 Umum Piala Panglima TNI",
                        "date": "30 September 2026",
                        "author": "Operator Kodam XIV Hasanuddin",
                        "category": "Prestasi Prajurit",
                        "summary": "Kontingen Kodam XIV/Hasanuddin menyabet gelar juara umum pada kejuaraan militer nasional, meningkatkan moril dan citra positif matra darat."
                    }
                ]
                for art in real_articles:
                    card_html = f"""
                    <div style="background: #111C2E; border: 1px solid #1E293B; border-left: 3px solid #38BDF8; padding: 10px 14px; border-radius: 4px; margin-bottom: 8px;">
                        <div style="display: flex; justify-content: space-between; font-family: 'JetBrains Mono'; font-size: 0.7rem; color: #94A3B8; margin-bottom: 2px;">
                            <span>📅 {art['date']} • {art['author']}</span>
                            <span style="color: #38BDF8; font-weight: bold;">{art['category']}</span>
                        </div>
                        <div style="font-weight: 700; color: #F8FAFC; font-size: 0.85rem; margin-bottom: 4px;">{art['title']}</div>
                        <div style="font-size: 0.78rem; color: #CBD5E1; line-height: 1.35;">{art['summary']}</div>
                    </div>
                    """
                    st.markdown(card_html, unsafe_allow_html=True)
            else:
                st.markdown(
                    f"""
                    <div style="background: rgba(16, 185, 129, 0.08); border: 1px solid #10B981; border-radius: 6px; padding: 16px; text-align: center;">
                        <span style="font-size: 1.5rem;">🟢</span>
                        <div style="font-family: 'Chakra Petch'; color: #10B981; font-weight: bold; font-size: 0.95rem; margin-top: 4px;">
                            WILAYAH TERITORIAL KONDUSIF
                        </div>
                        <p style="font-size: 0.8rem; color: #94A3B8; margin: 6px 0 0 0;">
                            Sensor intelijen siber tidak mendeteksi ancaman kognitif aktif yang menargetkan yurisdiksi <b>{selected_deep_kodam}</b> pada rentang 24 jam terakhir. Jajaran Korem, Kodim, dan Babinsa dalam status siaga stabil.
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
        with col_social_track:
            st.markdown(f"#### 🔍 Sinyal & Radar Medsos Satuan ({k_abbr})")
            
            if selected_deep_kodam == "Kodam XIV/Hasanuddin":
                social_signals = [
                    {
                        "platform": "TikTok & Reels",
                        "handle": "@lensa.makassar.update",
                        "issue": "Video Apel Prajurit Yonif 726/Tamalatea",
                        "risk": "Sedang (Perlu Pemantauan)",
                        "note": "Netizen membagikan ulang video apel dengan audio dramatis. Sentimen publik 85% positif bangga TNI, 15% bertanya-tanya kesiapsiagaan.",
                        "color": "#F59E0B"
                    },
                    {
                        "platform": "X (Twitter)",
                        "handle": "@suara_celebes_44",
                        "issue": "Diskusi Ketahanan Pangan Babinsa Sulsel",
                        "risk": "Aman (Organik)",
                        "note": "Apresiasi warga Gowa dan Maros terhadap pendampingan Babinsa pada panen raya padi.",
                        "color": "#10B981"
                    },
                    {
                        "platform": "YouTube",
                        "handle": "Channel Kabar Makassar 24",
                        "issue": "Liputan Baksos Pomdam XIV Bagi Masker",
                        "risk": "Positif Kognitif",
                        "note": "Telah ditonton 18K kali. Respon warga sangat positif terhadap aksi sosial prajurit Kodam di jalanan protokol Makassar.",
                        "color": "#10B981"
                    }
                ]
            else:
                social_signals = [
                    {
                        "platform": "TikTok & Reels",
                        "handle": f"@lensa.{k_abbr.lower().replace('/', '_')}.update",
                        "issue": f"Patroli Wilayah Korem & Kodim Jajaran {k_abbr}",
                        "risk": "Kondusif (Aman)",
                        "note": f"Monitoring respon masyarakat terhadap kehadiran pos teritorial {selected_deep_kodam}.",
                        "color": "#10B981"
                    },
                    {
                        "platform": "X (Twitter)",
                        "handle": f"@suara_warga_{k_abbr.lower().replace('/', '_')}",
                        "issue": f"Program Bakti Babinsa & Ketahanan Teritorial {k_prov}",
                        "risk": "Organik / Netral",
                        "note": "Percakapan warganet didominasi apresiasi kegiatan kemanunggalan TNI dan rakyat.",
                        "color": "#10B981"
                    },
                    {
                        "platform": "Media Daring",
                        "handle": f"Radar Teritorial {k_abbr}",
                        "issue": f"Publikasi Kegiatan Forkopimda & Kodam di {k_hq.split(',')[0]}",
                        "risk": "Informasi Resmi",
                        "note": "Pemberitaan netral dan positif mendukung soliditas jajaran forkopimda daerah.",
                        "color": "#38BDF8"
                    }
                ]
            
            for sig in social_signals:
                sig_html = f"""
                <div style="background: #0B1120; border: 1px solid #1E293B; border-left: 3px solid {sig['color']}; padding: 10px 12px; border-radius: 4px; margin-bottom: 8px;">
                    <div style="display: flex; justify-content: space-between; font-family: 'JetBrains Mono'; font-size: 0.7rem;">
                        <span style="color: #38BDF8;">{sig['platform']} • {sig['handle']}</span>
                        <span style="color: {sig['color']}; font-weight: bold;">{sig['risk']}</span>
                    </div>
                    <div style="font-weight: 600; font-size: 0.82rem; color: #F8FAFC; margin: 2px 0;">{sig['issue']}</div>
                    <div style="font-size: 0.74rem; color: #94A3B8;">{sig['note']}</div>
                </div>
                """
                st.markdown(sig_html, unsafe_allow_html=True)
                
            st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
            if st.button(f"📡 Sinkronkan Telemetri Live {selected_deep_kodam}", type="secondary", use_container_width=True, key="btn_sync_kodam_bottom"):
                st.session_state["live_feed_cache"] = None
                st.toast(f"Telemetri satelit media sosial {selected_deep_kodam} berhasil disinkronkan!", icon="📍")
                st.rerun()

