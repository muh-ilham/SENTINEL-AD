"""
modules/dashboard.py - C2 Executive Overview & Geospatial Tactical Heatmap
Command & Control situational awareness dashboard for TNI AD leadership,
featuring a dedicated High-Priority Incident Radar Hub with full filtering & pagination.
"""

import streamlit as st
import folium
from streamlit_folium import st_folium
import plotly.express as px
import plotly.graph_objects as go
import math
from datetime import datetime
from utils.theme import render_metric_card
from utils.data_generator import generate_threat_feed, generate_kodam_geo_summary, KODAM_REGIONS
from utils.soar_storage import check_is_escalated, add_escalated_incident

def render_dashboard(current_role="Analis Siber (Pussiberad)"):
    """Renders the executive C2 dashboard and dedicated Full Incident Radar Hub."""
    st.markdown("## 🛡️ PUSAT KOMANDO & KENDALI KOGNITIF (C2 OVERVIEW)")
    st.markdown(
        "<p style='color: #94A3B8; font-size: 0.95rem; margin-top: -10px;'>"
        "Sistem Pemantauan Ketahanan Kognitif, Operasi Disinformasi Lintas Wilayah Kodam & Kewaspadaan Pertahanan Siber TNI AD."
        "</p>",
        unsafe_allow_html=True
    )
    
    # Load Telemetry Data
    feed_df = generate_threat_feed(60)
    geo_df = generate_kodam_geo_summary()
    is_live = st.session_state.get("data_source_mode") == "live"
    active_count = len(feed_df)
    critical_count = len(feed_df[feed_df["threat_level"].isin(["Kritis", "Tinggi"])])
    
    # 1. Telemetry Top HUD Metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        render_metric_card("ANCAMAN / ISU TERDETEKSI", str(active_count), "Sensor Real-Time Aktif", "danger", "LIVE OSINT")
    with col2:
        render_metric_card("PRIORITAS TINGGI", str(critical_count), "Isu Perlu Ditanggapi", "warning", "ALERT")
    with col3:
        render_metric_card("MODE TELEMETRI", "ONLINE", "Internet Real-Time", "success", "NET")
    with col4:
        render_metric_card("DEEPFAKE/SINTETIS", "9", "4 Audio, 5 Dokumen", "warning", "AUDIO/OCR")
    with col5:
        render_metric_card("KESIAPAN SOAR", "98.4%", "Inter-Agency Ready", "success", "C2")

    st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)

    # View Mode Switcher
    view_options = [
        "🗺️ Ringkasan C2 & Peta Geospasial",
        "⚡ Pusat Radar Insiden Lengkap (Semua Data, Filter & Paging)"
    ]
    
    if "dashboard_view_radio" not in st.session_state:
        st.session_state["dashboard_view_radio"] = view_options[0]

    def set_view_radar_hub():
        st.session_state["dashboard_view_radio"] = view_options[1]

    def set_view_overview():
        st.session_state["dashboard_view_radio"] = view_options[0]
        
    selected_view = st.radio(
        "Pilih Mode Tampilan Dashboard:",
        view_options,
        key="dashboard_view_radio",
        horizontal=True
    )
    
    st.markdown("<hr style='border: 0.5px solid #1E293B; margin: 12px 0 18px 0;'/>", unsafe_allow_html=True)

    # -----------------------------------------------------------------
    # MODE 1: RINGKASAN C2 & PETA GEOSPASIAL (OVERVIEW)
    # -----------------------------------------------------------------
    if selected_view == view_options[0]:
        col_map, col_list = st.columns([7, 5])
        
        with col_map:
            st.markdown("### 🗺️ PETA SITUASI GEOSPASIAL ANCAMAN KODAM")
            st.markdown(
                "<span style='font-family: JetBrains Mono; font-size: 0.8rem; color: #38BDF8;'>"
                "Satelit Pemantauan Disinformasi Teritorial di 27 Kodam se-Indonesia (Renstra Transformasi Satu Provinsi Satu Kodam)"
                "</span>", 
                unsafe_allow_html=True
            )
            
            # Initialize Folium Map with OpenStreetMap tiles (watermark-free)
            m = folium.Map(
                location=[-1.5, 118.0],
                zoom_start=5,
                tiles="OpenStreetMap",
                control_scale=True
            )
            
            # Add Kodam Markers and Circles
            for _, row in geo_df.iterrows():
                popup_html = f"""
                <div style="font-family: Arial, sans-serif; min-width: 200px; color: #0F172A;">
                    <h4 style="margin: 0 0 4px 0; color: #0284C7; font-weight: bold;">{row['kodam']}</h4>
                    <p style="margin: 0; font-size: 11px; color: #64748B;">Markas: {row['hq']}</p>
                    <hr style="margin: 6px 0; border: 0.5px solid #CBD5E1;"/>
                    <div style="font-size: 12px; margin-bottom: 4px;">
                        <b>Status:</b> <span style="color: {row['marker_color']}; font-weight: bold;">{row['status_desc']}</span>
                    </div>
                    <div style="font-size: 11px;">
                        • Total Deteksi: <b>{row['total_threats']}</b><br/>
                        • Insiden Kritis: <b style="color: #EF4444;">{row['critical_count']}</b><br/>
                        • Rata-rata Skor CIB: <b>{row['avg_cib']}%</b>
                    </div>
                    <div style="margin-top: 6px; font-size: 10px; background: #F1F5F9; padding: 4px; border-radius: 4px;">
                        <b>Isu Utama:</b> {row['top_incident'][:50]}...
                    </div>
                </div>
                """
                
                radius_size = 180000 if row['critical_count'] > 0 else (120000 if row['high_count'] > 0 else 70000)
                folium.Circle(
                    location=[row['lat'], row['lon']],
                    radius=radius_size,
                    color=row['marker_color'],
                    weight=1.5,
                    fill=True,
                    fill_color=row['marker_color'],
                    fill_opacity=0.25 if row['critical_count'] > 0 else 0.15
                ).add_to(m)
                
                folium.CircleMarker(
                    location=[row['lat'], row['lon']],
                    radius=7 if row['critical_count'] == 0 else 10,
                    color="#FFFFFF",
                    weight=1.5,
                    fill=True,
                    fill_color=row['marker_color'],
                    fill_opacity=0.9,
                    tooltip=f"[{row['abbr']}] {row['kodam']} - {row['total_threats']} Insiden ({row['status_desc'].split(':')[1].strip()})",
                    popup=folium.Popup(popup_html, max_width=300)
                ).add_to(m)
                
            st_folium(m, width=None, height=480, returned_objects=[])

            # Tactical Quick Status Bar directly under the map
            crit_kodams = geo_df[geo_df["critical_count"] > 0]
            crit_count = len(crit_kodams)
            high_kodams = geo_df[geo_df["high_count"] > 0]
            
            with st.container(border=True):
                m_c1, m_c2, m_c3 = st.columns(3)
                with m_c1:
                    st.caption("🌐 **KODAM TERPANTAU**")
                    st.markdown(f"<span style='font-family: JetBrains Mono; color: #38BDF8; font-weight: bold;'>{len(geo_df)} Komando Daerah</span>", unsafe_allow_html=True)
                with m_c2:
                    st.caption("⚠️ **SEKTOR RAWAN**")
                    if crit_count > 0:
                        st.markdown(f"<span style='font-family: JetBrains Mono; color: #EF4444; font-weight: bold;'>{crit_count} Sektor Kritis</span>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<span style='font-family: JetBrains Mono; color: #F59E0B; font-weight: bold;'>{len(high_kodams)} Sektor Atensi</span>", unsafe_allow_html=True)
                with m_c3:
                    st.caption("📡 **TELEMETRI GEOINT**")
                    st.markdown("<span style='font-family: JetBrains Mono; color: #10B981; font-weight: bold;'>AKTIF • 18ms Latency</span>", unsafe_allow_html=True)


        with col_list:
            col_radar_title, col_radar_btn = st.columns([7, 5])
            with col_radar_title:
                st.markdown("### ⚡ RADAR INSIDEN PRIORITAS")
            with col_radar_btn:
                st.button(
                    "🚀 Buka Radar Penuh ➔",
                    key="btn_open_full_radar",
                    on_click=set_view_radar_hub,
                    use_container_width=True,
                    type="secondary"
                )
                    
            st.markdown(
                "<span style='font-family: JetBrains Mono; font-size: 0.78rem; color: #94A3B8;'>"
                "4 Isu Paling Mendesak • Klik tombol untuk triage penuh, filter & paging"
                "</span>",
                unsafe_allow_html=True
            )
            
            # Display top 4 Critical/High alerts in compact, tactical defense cards
            priority_df = feed_df[feed_df["threat_level"].isin(["Kritis", "Tinggi"])].head(4)
            if priority_df.empty:
                priority_df = feed_df.head(4)
            
            for _, alert in priority_df.iterrows():
                level = alert["threat_level"]
                card_class = "danger" if level == "Kritis" else "warning"
                badge_bg = "rgba(239, 68, 68, 0.15)" if level == "Kritis" else "rgba(245, 158, 11, 0.15)"
                badge_border = "#EF4444" if level == "Kritis" else "#F59E0B"
                badge_text = "#EF4444" if level == "Kritis" else "#F59E0B"
                
                with st.container(border=True):
                    # Header: ID + Time + Kodam + Badge
                    c_hdr_l, c_hdr_r = st.columns([8, 4])
                    with c_hdr_l:
                        st.caption(f"🆔 **{alert['id']}** &nbsp;•&nbsp; 🕒 {alert['timestamp'][11:19]} WIB &nbsp;•&nbsp; 📍 **{alert['kodam']}**")
                    with c_hdr_r:
                        st.markdown(
                            f"<div style='text-align:right;'><span style='background:{badge_bg}; color:{badge_text}; border:1px solid {badge_border}; padding:2px 8px; border-radius:4px; font-family:JetBrains Mono; font-weight:700; font-size:0.7rem;'>{level.upper()}</span></div>",
                            unsafe_allow_html=True
                        )
                    
                    # Headline
                    headline_text = alert['headline']
                    if len(headline_text) > 85:
                        headline_display = headline_text[:82] + "..."
                    else:
                        headline_display = headline_text
                    st.markdown(f"<div style='font-weight: 600; font-size: 0.86rem; color: #F8FAFC; margin: 2px 0 6px 0; line-height: 1.3;'>{headline_display}</div>", unsafe_allow_html=True)
                    
                    # Compact Inline Telemetry Grid
                    cib_val = alert['cib_probability']
                    cib_color = "#EF4444" if cib_val >= 75 else "#F59E0B"
                    
                    tc1, tc2, tc3 = st.columns([1.1, 1.1, 1.2])
                    with tc1:
                        st.caption(f"🤖 CIB: <b style='color: {cib_color};'>{cib_val}%</b>", unsafe_allow_html=True)
                    with tc2:
                        st.caption(f"🔥 Viral: <b style='color: #38BDF8;'>{alert['virality_score']}/100</b>", unsafe_allow_html=True)
                    with tc3:
                        st.caption(f"📱 Plat: <b style='color: #E2E8F0;'>{alert['platform']}</b>", unsafe_allow_html=True)

        # Analytics & Platform Breakdown
        st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
        st.markdown("### 📊 ANALITIK VEKTOR DISTRIBUSI & TREN SENTIMEN")
        
        col_chart1, col_chart2, col_chart3 = st.columns([4, 4, 4])
        
        with col_chart1:
            plat_counts = feed_df["platform"].value_counts().reset_index()
            plat_counts.columns = ["Platform", "Total"]
            platform_color_map = {
                "TikTok": "#FE2C55",
                "Instagram": "#E1306C",
                "X (Twitter)": "#38BDF8",
                "Facebook": "#1877F2",
                "YouTube": "#EF4444",
                "Media Daring": "#06B6D4",
                "Telegram": "#0088CC"
            }
            fig_plat = px.pie(
                plat_counts, values="Total", names="Platform", hole=0.55,
                color="Platform",
                color_discrete_map=platform_color_map
            )
            fig_plat.update_layout(
                title={"text": "Vektor Sebaran Platform", "font": {"family": "Chakra Petch", "size": 14, "color": "#F8FAFC"}},
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", showlegend=True,
                legend=dict(font=dict(family="JetBrains Mono", size=10, color="#94A3B8")),
                margin=dict(t=40, b=10, l=10, r=10), height=260
            )
            st.plotly_chart(fig_plat, use_container_width=True)

        with col_chart2:
            kodam_threat_summary = feed_df.groupby(["kodam", "threat_level"]).size().reset_index(name="Count")
            kodam_top = feed_df["kodam"].value_counts().head(5).index
            kodam_threat_top = kodam_threat_summary[kodam_threat_summary["kodam"].isin(kodam_top)]
            fig_kodam = px.bar(
                kodam_threat_top, x="Count", y="kodam", color="threat_level", orientation='h',
                color_discrete_map={"Kritis": "#EF4444", "Tinggi": "#F59E0B", "Sedang": "#3B82F6", "Rendah": "#10B981"}
            )
            fig_kodam.update_layout(
                title={"text": "Top 5 Kodam Terdampak Ancaman", "font": {"family": "Chakra Petch", "size": 14, "color": "#F8FAFC"}},
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(title="", tickfont=dict(color="#94A3B8", family="JetBrains Mono")),
                yaxis=dict(title="", tickfont=dict(color="#F8FAFC", size=10)),
                legend=dict(title="", font=dict(family="JetBrains Mono", size=9, color="#94A3B8")),
                margin=dict(t=40, b=10, l=10, r=10), height=260
            )
            st.plotly_chart(fig_kodam, use_container_width=True)

        with col_chart3:
            fig_scatter = px.scatter(
                feed_df.head(30), x="cib_probability", y="virality_score", color="threat_level",
                size="shares_count", hover_data=["headline", "platform"],
                color_discrete_map={"Kritis": "#EF4444", "Tinggi": "#F59E0B", "Sedang": "#3B82F6", "Rendah": "#10B981"}
            )
            fig_scatter.update_layout(
                title={"text": "Korelasi CIB vs Virality Index", "font": {"family": "Chakra Petch", "size": 14, "color": "#F8FAFC"}},
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(title="CIB / Bot Probability (%)", tickfont=dict(color="#94A3B8", family="JetBrains Mono"), gridcolor="#1E293B"),
                yaxis=dict(title="Virality Score (0-100)", tickfont=dict(color="#94A3B8", family="JetBrains Mono"), gridcolor="#1E293B"),
                legend=dict(title="", font=dict(family="JetBrains Mono", size=9, color="#94A3B8")),
                margin=dict(t=40, b=10, l=10, r=10), height=260
            )
            st.plotly_chart(fig_scatter, use_container_width=True)

    # -----------------------------------------------------------------
    # MODE 2: PUSAT RADAR INSIDEN PENUH (ALL INCIDENTS, FILTER & PAGING)
    # -----------------------------------------------------------------
    else:
        col_hub_head, col_back_btn = st.columns([9, 3])
        with col_hub_head:
            st.markdown("### ⚡ PUSAT RADAR INSIDEN LENGKAP (RADAR HUB & INVESTIGASI PENUH)")
            st.markdown(
                "<span style='font-family: JetBrains Mono; font-size: 0.85rem; color: #38BDF8;'>"
                "Pusat Triage Menyeluruh: Menampilkan Seluruh Isu Siber Pertahanan dengan Filter Multi-Kriteria, Pencarian Kata Kunci & Sistem Paginasi Cepat."
                "</span>",
                unsafe_allow_html=True
            )
        with col_back_btn:
            st.button(
                "⬅ Kembali ke Peta C2",
                key="btn_back_to_c2_overview",
                on_click=set_view_overview,
                use_container_width=True
            )

        st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
        
        # 1. Search Bar & Sorting
        col_search, col_sort = st.columns([8, 4])
        with col_search:
            search_query = st.text_input(
                "🔍 Cari Judul Isu / Kata Kunci / Sumber Berita / Nama Oknum:",
                placeholder="Ketik kata kunci pencarian (contoh: judi online, mutasi, perbatasan, klaten, dll)..."
            )
        with col_sort:
            sort_by = st.selectbox(
                "Urutkan Daftar Berdasarkan:",
                [
                    "Viralitas Tertinggi (Virality Index)",
                    "Probabilitas Bot Tertinggi (CIB %)",
                    "Tingkat Ancaman Paling Kritis",
                    "Waktu Deteksi Terbaru"
                ]
            )

        # 2. Multi-Criteria Filter Dropdowns
        f_col1, f_col2, f_col3, f_col4 = st.columns(4)
        with f_col1:
            filter_level = st.selectbox(
                "Filter Tingkat Ancaman:",
                ["Semua Tingkat", "Kritis", "Tinggi", "Sedang", "Rendah"]
            )
        with f_col2:
            filter_kodam = st.selectbox(
                "Filter Yurisdiksi Kodam:",
                ["Semua Kodam"] + list(KODAM_REGIONS.keys())
            )
        with f_col3:
            all_known_plats = ["TikTok", "Instagram", "X (Twitter)", "Facebook", "YouTube", "Telegram", "Media Daring"]
            present_plats = [p for p in all_known_plats if p in feed_df["platform"].values]
            filter_platform = st.selectbox(
                "Filter Platform Media:",
                ["Semua Platform"] + present_plats
            )
        with f_col4:
            items_per_page = st.selectbox(
                "Jumlah Isu per Halaman (Paging):",
                [5, 10, 15, 20],
                index=1  # Default 10 per page
            )

        # Apply Filters
        filtered_df = feed_df.copy()

        if search_query:
            query_lower = search_query.lower()
            filtered_df = filtered_df[
                filtered_df["headline"].str.lower().str.contains(query_lower, na=False) |
                filtered_df["text"].str.lower().str.contains(query_lower, na=False) |
                filtered_df["author"].str.lower().str.contains(query_lower, na=False) |
                filtered_df["kodam"].str.lower().str.contains(query_lower, na=False)
            ]

        if filter_level != "Semua Tingkat":
            filtered_df = filtered_df[filtered_df["threat_level"] == filter_level]

        if filter_kodam != "Semua Kodam":
            filtered_df = filtered_df[filtered_df["kodam"] == filter_kodam]

        if filter_platform != "Semua Platform":
            filtered_df = filtered_df[filtered_df["platform"] == filter_platform]

        # Apply Sorting
        if "Viralitas" in sort_by:
            filtered_df = filtered_df.sort_values(by="virality_score", ascending=False)
        elif "Probabilitas Bot" in sort_by:
            filtered_df = filtered_df.sort_values(by="cib_probability", ascending=False)
        elif "Paling Kritis" in sort_by:
            level_map = {"Kritis": 4, "Tinggi": 3, "Sedang": 2, "Rendah": 1}
            filtered_df["_rank"] = filtered_df["threat_level"].map(level_map)
            filtered_df = filtered_df.sort_values(by="_rank", ascending=False).drop(columns=["_rank"])
        else:
            filtered_df = filtered_df.sort_values(by="timestamp", ascending=False)

        # Summary Telemetry Bar for Filtered Results
        total_filtered = len(filtered_df)
        crit_count = len(filtered_df[filtered_df["threat_level"] == "Kritis"])
        high_count = len(filtered_df[filtered_df["threat_level"] == "Tinggi"])
        avg_cib_val = round(filtered_df["cib_probability"].mean(), 1) if total_filtered > 0 else 0
        avg_virality_val = round(filtered_df["virality_score"].mean(), 1) if total_filtered > 0 else 0

        with st.container(border=True):
            s_c1, s_c2, s_c3, s_c4, s_c5 = st.columns(5)
            s_c1.metric("HASIL FILTER", f"{total_filtered} Isu")
            s_c2.metric("ISU KRITIS", f"{crit_count}", delta="Perlu Respons Darurat" if crit_count > 0 else "Nihil", delta_color="inverse" if crit_count > 0 else "normal")
            s_c3.metric("PRIORITAS TINGGI", f"{high_count}", delta="Atensi Khusus" if high_count > 0 else "Nihil", delta_color="inverse" if high_count > 0 else "normal")
            s_c4.metric("RERATA CIB", f"{avg_cib_val}%")
            s_c5.metric("RERATA VIRALITY", f"{avg_virality_val}/100")

        if total_filtered == 0:
            st.warning("⚠️ Tidak ada isu yang cocok dengan kriteria filter atau pencarian Anda. Silakan sesuaikan kata kunci atau pilih 'Semua Tingkat'.")
        else:
            # Pagination Logic
            total_pages = max(1, math.ceil(total_filtered / items_per_page))
            
            if "radar_page_num" not in st.session_state:
                st.session_state["radar_page_num"] = 1
                
            # Clamp page number
            if st.session_state["radar_page_num"] > total_pages:
                st.session_state["radar_page_num"] = total_pages
            if st.session_state["radar_page_num"] < 1:
                st.session_state["radar_page_num"] = 1

            current_page = st.session_state["radar_page_num"]
            start_idx = (current_page - 1) * items_per_page
            end_idx = min(start_idx + items_per_page, total_filtered)
            page_slice = filtered_df.iloc[start_idx:end_idx]

            # Render Paginated Incident Cards using native tactical container
            for idx, alert in page_slice.iterrows():
                level = alert["threat_level"]
                card_class = "danger" if level == "Kritis" else ("warning" if level == "Tinggi" else "success")
                
                cib_num = alert["cib_probability"]
                if cib_num >= 80:
                    cib_desc = "Sangat Kuat Terkoordinasi / Botnet"
                elif cib_num >= 50:
                    cib_desc = "Indikasi Amplifikasi Buatan"
                else:
                    cib_desc = "Pola Percakapan Alami Organik"

                with st.container(border=True):
                    col_h_l, col_h_r = st.columns([9, 3])
                    with col_h_l:
                        st.caption(f"🆔 **{alert['id']}** &nbsp;•&nbsp; 🕒 {alert['timestamp']} WIB &nbsp;•&nbsp; 📱 {alert['platform']} &nbsp;•&nbsp; 📍 **{alert['kodam']}**")
                    with col_h_r:
                        st.markdown(f"<div style='text-align:right;'><span class='status-pill pill-{card_class}'>{level.upper()}</span></div>", unsafe_allow_html=True)
                        
                    st.markdown(f"#### {alert['headline']}")
                    st.write(alert['text'])
                    if alert.get("link"):
                        st.caption(f"[🔗 Buka Tautan Sumber Berita / Rujukan Online ↗]({alert['link']})")
                    
                    col_tel1, col_tel2, col_tel3 = st.columns([5, 3, 4])
                    with col_tel1:
                        st.metric("INDIKASI CIB", f"{alert['cib_probability']}%", cib_desc, delta_color="inverse" if alert['cib_probability'] >= 50 else "normal")
                    with col_tel2:
                        st.metric("VIRALITY INDEX", f"{alert['virality_score']}/100")
                    with col_tel3:
                        st.metric("STATUS DETEKSI", alert['status'])
                
                # Expandable Decision & Forensic Drawer for each item
                with st.expander(f"🔎 Buka Analisis Dampak Kognitif & Rencana Respons Taktis ({alert['id']})"):
                    col_act_left, col_act_right = st.columns([8, 4])
                    with col_act_left:
                        st.markdown(
                            f"""
                            **Analisis Dampak Kognitif Terhadap Citra TNI AD:**
                            - **Potensi Risiko:** Isu ini berpotensi dimanipulasi oleh bot proksi untuk mendegradasi kepercayaan publik terhadap jajaran `{alert['kodam']}`.
                            - **Rekomendasi Dispenad:** Rilis sanggahan berbasis data resmi dan tampilkan rujukan aturan kedinasan agar rumor tidak merembes ke ruang publik yang lebih luas.
                            - **Rekomendasi Pussiberad:** Pantau lonjakan anomali akun pengganda (*amplification nodes*) dan masukkan tautan sumber ke antrean takedown.
                            """
                        )
                    with col_act_right:
                        st.markdown("**Aksi Cepat Pengambil Keputusan:**")
                        
                        # Check persistent storage (matches by ID and by headline across refreshes)
                        is_escalated, esc_info = check_is_escalated(alert)
                        
                        if is_escalated:
                            st.button(
                                f"✅ TELAH DIESKALASIKAN KE SOAR",
                                key=f"soar_btn_{alert['id']}_done",
                                disabled=True,
                                use_container_width=True
                            )
                            esc_time = esc_info.get('escalated_at', 'Terekam di Sistem')
                            esc_user = esc_info.get('escalated_by', current_role)
                            status_badge_html = f"""<div style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: #10B981; background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); padding: 6px 8px; border-radius: 4px; margin: 4px 0 8px 0;">✓ <b>STATUS:</b> DIESKALASI KE SOAR<br/>⏱ <b>Waktu:</b> {esc_time}<br/>👤 <b>Oleh:</b> {esc_user}</div>"""
                            st.markdown(status_badge_html, unsafe_allow_html=True)
                        else:
                            if st.button(f"🚨 Eskalasikan ke SOAR ({alert['id']})", key=f"soar_btn_{alert['id']}", type="primary", use_container_width=True):
                                now_wib = datetime.now().strftime("%Y-%m-%d %H:%M:%S WIB")
                                role_actor = st.session_state.get("active_role", current_role)
                                
                                # Package into standardized SOAR incident payload
                                soar_payload = {
                                    "id": alert["id"],
                                    "title": alert["headline"],
                                    "headline": alert["headline"],
                                    "category": f"Deteksi Radar {alert.get('platform', 'Medsos')} / Operasi Disinformasi",
                                    "level": alert["threat_level"],
                                    "threat_level": alert["threat_level"],
                                    "root_platform": alert.get("platform", "Media Daring"),
                                    "platform": alert.get("platform", "Media Daring"),
                                    "jump_sequence": [alert.get("platform", "Media Daring"), "X (Twitter)", "Media Daring"],
                                    "target_kodam": alert["kodam"],
                                    "kodam": alert["kodam"],
                                    "cib_cluster_size": int(alert.get("amplification_nodes", 28)),
                                    "amplification_nodes": int(alert.get("amplification_nodes", 28)),
                                    "sample_text": alert.get("text", alert["headline"]),
                                    "text": alert.get("text", alert["headline"]),
                                    "sentiment": alert.get("sentiment_score", -0.72),
                                    "sentiment_score": alert.get("sentiment_score", -0.72),
                                    "virality_score": alert.get("virality_score", 85),
                                    "cib_probability": alert.get("cib_probability", 80),
                                    "shares_count": alert.get("shares_count", 3200),
                                    "author": alert.get("author", "Akun Publik"),
                                    "link": alert.get("link", ""),
                                    "escalated_at": now_wib,
                                    "escalated_by": role_actor,
                                    "is_from_radar": True
                                }
                                
                                # Save permanently to disk storage
                                add_escalated_incident(soar_payload)
                                
                                # Also update session state for immediate UI reaction
                                if "escalated_soar_incidents" not in st.session_state:
                                    st.session_state["escalated_soar_incidents"] = {}
                                st.session_state["escalated_soar_incidents"][alert["id"]] = soar_payload
                                
                                st.toast(f"Insiden {alert['id']} berhasil dimasukkan ke Antrean Persetujuan SOAR!", icon="🛡️")
                                st.rerun()
                            
                        # If there is a real online link from live OSINT
                        link_url = alert.get("link")
                        if link_url:
                            st.link_button("🌐 Buka Tautan Sumber Asli", url=link_url, use_container_width=True)

            # Pagination Navigation Bar
            st.markdown("<hr style='border: 0.5px solid #1E293B; margin: 15px 0;'/>", unsafe_allow_html=True)
            col_p_prev, col_p_info, col_p_next = st.columns([3, 6, 3])
            
            with col_p_prev:
                if st.button("◀ Halaman Sebelumnya", disabled=(current_page <= 1), use_container_width=True):
                    st.session_state["radar_page_num"] = max(1, current_page - 1)
                    st.rerun()

            with col_p_info:
                st.markdown(
                    f"""
                    <div style="text-align: center; font-family: 'JetBrains Mono'; font-size: 0.82rem; color: #94A3B8; padding-top: 8px;">
                        Halaman <b style="color: #38BDF8; font-size: 1rem;">{current_page}</b> dari <b>{total_pages}</b> 
                        &nbsp;|&nbsp; Menampilkan isu ke-<b>{start_idx + 1}</b> s/d <b>{end_idx}</b> dari total <b>{total_filtered}</b> isu
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with col_p_next:
                if st.button("Halaman Berikutnya ▶", disabled=(current_page >= total_pages), use_container_width=True):
                    st.session_state["radar_page_num"] = min(total_pages, current_page + 1)
                    st.rerun()
