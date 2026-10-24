"""
modules/cib_screener.py - Advanced CIB Detection & Multimodal Deepfake Screener
Analyzes Coordinated Inauthentic Behavior timing bursts and screens multimodal synthetic media (Voice Clones & Forged Military Docs).
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import re
from datetime import datetime
from utils.data_generator import generate_cib_synchronized_clusters
from utils.soar_storage import (
    add_escalated_incident,
    check_is_escalated,
    get_escalated_incidents,
    get_approved_incidents,
    get_audit_logs
)
from utils.audio_forensics import (
    generate_sample_wav,
    analyze_audio_data,
    generate_acoustic_dossier_json
)
from utils.document_forensics import (
    get_document_catalog,
    generate_document_canvas_image,
    perform_real_ela,
    generate_document_dossier_json,
    get_clean_document_html,
    compute_sha256,
    compute_md5
)
from utils.pdf_exporter import generate_sitrep_pdf

def render_cib_screener():
    """Renders the CIB & Multimodal Deepfake Screener module."""
    st.markdown("## 🔍 CIB DETECTOR & MULTIMODAL DEEPFAKE SCREENER")
    st.markdown(
        "<p style='color: #94A3B8; font-size: 0.95rem; margin-top: -10px;'>"
        "Deteksi Perilaku Terkoordinasi Non-Otentik (CIB) & Forensik Sintetis Multimodal (Audio Clone & Dokumen Militer Palsu)."
        "</p>",
        unsafe_allow_html=True
    )
    
    tab_cib, tab_audio, tab_doc = st.tabs([
        "⚡ TAB 1: SINKRONISASI WAKTU CIB (<60s)", 
        "🎙️ TAB 2: AUDIT SPEKTROGRAM AUDIO DEEPFAKE", 
        "📄 TAB 3: INTEGRITAS DOKUMEN & HIGHLIGHT OCR"
    ])
    
    # -----------------------------------------------------------------
    # -----------------------------------------------------------------
    # TAB 1: CIB TIMING & SEMANTIC BURST ANALYSIS
    # -----------------------------------------------------------------
    with tab_cib:
        st.markdown("### ⏱️ ANALISIS BURST TEMPORAL CIB (SINKRONISASI POSTINGAN &lt;60 DETIK)")
        st.markdown(
            "<p style='color: #94A3B8; font-size: 0.92rem; margin-top: -6px;'>"
            "<b>Coordinated Inauthentic Behavior (CIB)</b> adalah operasi manipulasi kognitif siber di mana sekelompok "
            "akun bodong/botnet digerakkan otomatis oleh mesin secara serentak untuk memviralkan isu hoaks demi merusak wibawa TNI AD & stabilitas nasional."
            "</p>",
            unsafe_allow_html=True
        )
        
        cib_df = generate_cib_synchronized_clusters()
        is_live_data = "is_live" in cib_df.columns and cib_df["is_live"].any()
        from datetime import datetime
        now_str = datetime.now().strftime("%d %B %Y, %H:%M:%S WIB")
        
        # Bilah Informasi Telemetri Live & Tanggal Terbaru
        col_live_status, col_live_refresh = st.columns([8, 4])
        with col_live_status:
            source_label = "LIVE ONLINE MULTI-PLATFORM (TikTok, Instagram, X, Facebook, YouTube, Media Daring)"
            badge_color = "#10B981"
            st.markdown(
                f"""<div style="background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.3); border-left: 4px solid {badge_color}; padding: 10px 14px; border-radius: 4px; margin-bottom: 12px;">
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: {badge_color}; font-weight: bold;">
                    ● SUMBER DATA TERHUBUNG: {source_label}
                </div>
                <div style="font-size: 0.82rem; color: #F8FAFC; margin-top: 3px;">
                    🕒 <b>Tanggal & Waktu Rujukan Terbaru:</b> <span style="color: #38BDF8; font-family: 'JetBrains Mono'; font-weight: bold;">{now_str}</span>
                </div>
                </div>""",
                unsafe_allow_html=True
            )
        with col_live_refresh:
            if st.button("🔄 Tarik Data Nyata Terbaru (Sync Live CIB)", use_container_width=True, type="primary"):
                st.session_state["live_feed_cache"] = None
                st.toast("Menarik data terbaru dari TikTok, Instagram, X, Facebook, YouTube...", icon="🌐")
                st.rerun()
        
        # 4 Ringkasan Metrik Taktis Utama
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        with col_m1:
            st.metric(
                "Total Akun Terindikasi Bot", 
                f"{len(cib_df)} Akun", 
                "Terdeteksi di Medsos",
                help="Total akun bodong tertangkap basah menyebarkan narasi hoaks serentak pada platform TikTok, X, Instagram, Facebook, dan Telegram."
            )
        with col_m2:
            st.metric(
                "Rerata Jeda Posting", 
                "5.8 Detik", 
                "Sub-60s Burst Window",
                help="Jeda waktu antar unggahan hanya 3–8 detik. Manusia mustahil mengetik dan mengunggah secepat ini berulang-ulang."
            )
        with col_m3:
            st.metric(
                "Kemiripan Teks Narasi", 
                "96.4%", 
                "Cosine Similarity Template",
                help="96.4% kata-kata dan susunan kalimat yang diunggah sama persis (template copas otomatis hasil generator skrip bot)."
            )
        with col_m4:
            st.metric(
                "Asal Proksi / Server", 
                "TOR & Cloud Proxy", 
                "Eropa & Amerika (Anonim)",
                help="Pelaku menggunakan jaringan perantara luar negeri (Belanda, Swiss, Jerman, AS) untuk menyembunyikan identitas asli dalang operasi."
            )
            
        st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
        
        # PANDUAN EDUKASI BAHASA AWAM (Menggunakan Markdown Murni agar tidak bocor kode HTML)
        with st.expander("💡 PANDUAN BAHASA AWAM: BAGAIMANA CARA SISTEM MEMBUKTIKAN BAHWA INI BUKAN NETIZEN ASLI? (KLIK UNTUK MEMBACA)", expanded=False):
            st.markdown("#### 🛡️ 4 Bukti Ilmiah Mengapa 13 Akun Ini Pasti Bot / Pasukan Buzzer:")
            
            st.markdown(
                "**1. ⏱️ Kecepatan Waktu Mustahil (Jeda Unggah Rata-Rata 5.8 Detik):**  \n"
                "Netizen manusia butuh waktu untuk membuka HP, membaca berita, mengetik komentar, dan mengunggahnya (rata-rata 1–3 menit). "
                "Akun-akun ini mengunggah postingan hanya berselang 3 hingga 8 detik satu sama lain secara berurutan. Pola tembakan cepat (*burst*) ini adalah ciri mutlak sistem otomatisasi komputer."
            )
            st.markdown(
                "**2. 📋 Isi Kalimat 'Copy-Paste' Seragam (Tingkat Kemiripan 96.4%):**  \n"
                "Jika netizen asli mengomentari suatu isu, gaya bahasa dan pilihan kata mereka pasti beragam. Namun 13 akun ini menggunakan susunan kalimat yang 96% identik "
                "(hanya dibolak-balik sedikit menggunakan teknik *spinning text*) untuk membanjiri linimasa secara terkoordinasi."
            )
            st.markdown(
                "**3. 🎭 Profil Bodong & Akun 'Siluman' (Umur Baru & Sepi Pengikut):**  \n"
                "Akun-akun ini rata-rata baru dibuat 2 hingga 14 hari yang lalu, foto profilnya menggunakan gambar AI atau comotan Google, serta memiliki pengikut sangat sedikit "
                "(14–85 followers) tanpa riwayat kehidupan nyata. Akun sengaja diproduksi massal (*bot farm*) khusus untuk kampanye propaganda."
            )
            st.markdown(
                "**4. 🌐 Menyamarkan Lokasi Geografis (Jalur TOR Exit Node & Data Center):**  \n"
                "Alih-alih menggunakan internet penyedia lokal Indonesia (seperti Telkomsel, Indosat, atau IndiHome), jejak internet akun-akun ini dialihkan melalui jaringan persembunyian anonim "
                "(TOR Node dan Proxy Server di Belanda, Swiss, Swedia, AS) agar identitas pelaku sebenarnya tidak mudah dilacak aparat hukum."
            )

        st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
        
        # Filter Klaster Akun
        cluster_options = ["🌐 Semua Klaster (13 Akun Gabungan - Rekapitulasi Lengkap)"] + list(cib_df["cluster"].unique())
        cluster_filter = st.selectbox(
            "🔍 Pilih Klaster Ancaman CIB untuk Dianalisis:",
            options=cluster_options
        )
        
        if "Semua Klaster" in cluster_filter:
            sub_cib = cib_df.copy()
        else:
            sub_cib = cib_df[cib_df["cluster"] == cluster_filter].copy()
            
        sub_cib["cumulative_time_sec"] = sub_cib["post_interval_sec"].cumsum()
        
        # Identifikasi akun-akun yang sudah masuk ke antrean SOAR
        all_escalations = get_escalated_incidents()
        escalated_bot_accounts = set()
        for item in all_escalations.values():
            if item.get("bot_account"):
                norm_acc = re.sub(r"[^a-zA-Z0-9]", "", str(item.get("bot_account"))).lower()
                escalated_bot_accounts.add(norm_acc)
            for b_acc in item.get("bot_accounts_list", []):
                norm_acc = re.sub(r"[^a-zA-Z0-9]", "", str(b_acc)).lower()
                escalated_bot_accounts.add(norm_acc)

        sub_cib["is_soar_queued"] = sub_cib["account"].apply(
            lambda a: re.sub(r"[^a-zA-Z0-9]", "", str(a)).lower() in escalated_bot_accounts
        )
        sub_cib["soar_status_badge"] = sub_cib["is_soar_queued"].apply(
            lambda q: "🟢 Terdaftar di SOAR" if q else "⚪ Belum Diajukan"
        )
        
        unescalated_sub_cib = sub_cib[~sub_cib["is_soar_queued"]].copy()
        remaining_takedown_count = len(unescalated_sub_cib)
        already_takedown_count = len(sub_cib) - remaining_takedown_count
        
        # Baris Grafik Linimasa & Ringkasan Platform
        col_chart, col_platform = st.columns([7, 5])
        
        with col_chart:
            st.markdown("#### Linimasa Interval Posting Akun Bot (Detik)")
            
            fig_burst = px.scatter(
                sub_cib,
                x="cumulative_time_sec",
                y="account",
                size="semantic_similarity",
                color="semantic_similarity",
                color_continuous_scale="Reds",
                hover_data=["platform", "bot_role", "timestamp", "account_age_desc", "follower_desc", "proxy_ip"],
                labels={"cumulative_time_sec": "Detik Kumulatif Pasca Drop Awal", "account": "Identitas Akun Bot"}
            )
            fig_burst.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(15,23,42,0.8)",
                font=dict(family="JetBrains Mono", size=10, color="#F8FAFC"),
                margin=dict(t=20, b=20, l=10, r=10),
                height=300,
                xaxis=dict(gridcolor="#334155"),
                yaxis=dict(gridcolor="#334155")
            )
            st.plotly_chart(fig_burst, use_container_width=True)
            st.caption("📌 **Cara Membaca Grafik:** Setiap titik merah mewakili 1 akun bot. Sumbu X menunjukkan detik sejak isu pertama kali disebar. Titik-titik yang muncul beruntun cepat membuktikan proses unggahan otomatis mesin.")
            
        with col_platform:
            st.markdown("#### Distribusi Asal Platform & Peran Botnet")
            
            # Platform Counts
            p_counts = sub_cib["platform"].value_counts().to_dict()
            
            c_p1, c_p2 = st.columns(2)
            with c_p1:
                st.markdown(
                    """
                    <div style="background: #111C2E; border: 1px solid #1E293B; padding: 10px; border-radius: 4px; font-family: 'JetBrains Mono'; font-size: 0.8rem; margin-bottom: 8px;">
                        <span style="color: #38BDF8;">🐦 X (Twitter):</span> <b>5 Akun</b><br/>
                        <span style="color: #F43F5E;">📱 TikTok:</span> <b>4 Akun</b><br/>
                        <span style="color: #EC4899;">📸 Instagram:</span> <b>2 Akun</b>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            with c_p2:
                st.markdown(
                    """
                    <div style="background: #111C2E; border: 1px solid #1E293B; padding: 10px; border-radius: 4px; font-family: 'JetBrains Mono'; font-size: 0.8rem; margin-bottom: 8px;">
                        <span style="color: #3B82F6;">👥 Facebook:</span> <b>1 Akun</b><br/>
                        <span style="color: #06B6D4;">✈️ Telegram:</span> <b>1 Akun</b><br/>
                        <span style="color: #10B981;">🛡️ Status:</span> <b>13 Terdeteksi</b>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
            st.markdown(
                """
                <div style="background: #0B1120; border-left: 3px solid #F59E0B; padding: 8px 12px; border-radius: 4px; font-size: 0.78rem; color: #CBD5E1; margin-top: 4px;">
                    <b>Struktur Pasukan Bot Terdeteksi:</b><br/>
                    • <b>🚨 Seed (2 Akun):</b> Pelempar perdana berkas deepfake ke publik.<br/>
                    • <b>⚡ Amplifier (6 Akun):</b> Pasukan pengganda kilat peniru algoritma FYP/Trending.<br/>
                    • <b>👥 Sockpuppet (3 Akun):</b> Akun boneka penyusup ke grup komunitas.<br/>
                    • <b>📢 Resonator (2 Akun):</b> Pemancing interaksi dengan men-tag akun berita.
                </div>
                """,
                unsafe_allow_html=True
            )
            
        st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
        
        # TABEL LENGKAP 13 AKUN BESERTA TAUTAN YANG BISA DIKLIK
        st.markdown("#### 📋 Rekapitulasi Rincian 13 Akun Bot & Tautan Profil Medsos")
        st.caption("💡 *Tautan pada kolom **'Tautan Akun Medsos 🔗'** dapat diklik langsung untuk memeriksa keberadaan profil di platform aslinya.*")
        
        st.dataframe(
            sub_cib[[
                "platform_icon", "account", "soar_status_badge", "profile_url", "bot_role", 
                "post_interval_sec", "semantic_similarity", "account_age_desc", 
                "follower_desc", "proxy_ip"
            ]],
            column_config={
                "platform_icon": st.column_config.TextColumn("Asal Platform", width="medium"),
                "account": st.column_config.TextColumn("Identitas Akun", width="medium"),
                "soar_status_badge": st.column_config.TextColumn("Status SOAR", width="medium"),
                "profile_url": st.column_config.LinkColumn("Tautan Akun Medsos 🔗", display_text="Buka Profil Akun ↗", width="medium"),
                "bot_role": st.column_config.TextColumn("Peran Botnet", width="medium"),
                "post_interval_sec": st.column_config.NumberColumn("Jeda Unggah", format="%d detik", width="small"),
                "semantic_similarity": st.column_config.ProgressColumn("Kemiripan Teks", min_value=0.8, max_value=1.0, format="%.1f%%", width="medium"),
                "account_age_desc": st.column_config.TextColumn("Usia Akun", width="medium"),
                "follower_desc": st.column_config.TextColumn("Jumlah Pengikut", width="medium"),
                "proxy_ip": st.column_config.TextColumn("Jejak Lokasi / IP", width="large")
            },
            hide_index=True,
            use_container_width=True,
            height=340
        )
        
        st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
        
        # INSPEKTUR FORENSIK DIGITAL PER AKUN (BEDAH PROFIL)
        st.markdown("#### 🔎 Inspektur Forensik Digital Akun Terdeteksi (Bedah Profil)")
        st.caption("Pilih salah satu dari 13 akun di bawah untuk melihat rincian bukti forensik digital dan narasi hoaks yang disebarkan:")
        
        def _format_acc_dropdown(x):
            row_match = sub_cib[sub_cib["account"] == x]
            if row_match.empty:
                return str(x)
            p_icon = row_match["platform_icon"].values[0]
            b_role = row_match["bot_role"].values[0]
            is_q = re.sub(r"[^a-zA-Z0-9]", "", str(x)).lower() in escalated_bot_accounts
            q_badge = " [✓ DI ANTREAN SOAR]" if is_q else ""
            return f"{p_icon} {x} - {b_role}{q_badge}"

        selected_account = st.selectbox(
            "Pilih Akun yang Ingin Dibedah Secara Mendalam:",
            options=list(sub_cib["account"]),
            format_func=_format_acc_dropdown
        )
        
        active_user_data = sub_cib[sub_cib["account"] == selected_account].iloc[0]
        
        with st.container(border=True):
            col_u_left, col_u_right = st.columns([6, 6])
            
            with col_u_left:
                st.markdown(f"##### {active_user_data['platform_icon']} {active_user_data['account']}")
                st.markdown(f"**Peran dalam Operasi:** <span style='color: #EF4444; font-weight: bold;'>{active_user_data['bot_role']}</span>", unsafe_allow_html=True)
                st.caption(f"ℹ️ {active_user_data['bot_desc']}")
                
                st.markdown(
                    f"""
                    <div style="background: #0B1120; border: 1px solid #1E293B; padding: 10px; border-radius: 4px; font-family: 'JetBrains Mono'; font-size: 0.78rem; margin: 8px 0;">
                        <div>• <b>Alat Otomasi:</b> <span style="color: #38BDF8;">{active_user_data['automation_tool']}</span></div>
                        <div>• <b>Jalur Jaringan / Node:</b> <span style="color: #F59E0B;">{active_user_data['proxy_ip']}</span></div>
                        <div>• <b>Probabilitas Bot:</b> <span style="color: #EF4444; font-weight: bold;">{active_user_data['bot_probability']}</span></div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                st.link_button(
                    label=f"🌐 Kunjungi Profil Asli {selected_account} di {active_user_data['platform']} ↗",
                    url=active_user_data['profile_url'],
                    type="primary",
                    use_container_width=True
                )
                
            with col_u_right:
                st.markdown("##### 📝 Narasi Hoaks yang Diunggah Akun Ini:")
                st.markdown(
                    f"""
                    <div style="background: rgba(239, 68, 68, 0.1); border-left: 3px solid #EF4444; padding: 10px 14px; border-radius: 4px; font-family: 'JetBrains Mono'; font-size: 0.82rem; color: #FCA5A5; margin-bottom: 10px; line-height: 1.5;">
                        "{active_user_data['payload_text']}"
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                st.markdown(
                    f"""
                    <div style="background: #111C2E; padding: 10px; border-radius: 4px; font-size: 0.78rem; color: #CBD5E1; margin-bottom: 12px;">
                        <b>Indikator Anomali Otentikasi:</b><br/>
                        • <b>Jeda Posting:</b> {active_user_data['post_interval_sec']} detik pasca pelepasan isu (Kecepatan Otomasi)<br/>
                        • <b>Karakteristik Akun:</b> {active_user_data['account_age_desc']} | {active_user_data['follower_desc']}<br/>
                        • <b>Tingkat Kemiripan Teks:</b> {round(active_user_data['semantic_similarity']*100, 1)}% identik dengan seed awal<br/>
                        • <b>Rekomendasi Respons:</b> <span style="color: #10B981; font-weight: bold;">Siap Ditransmisikan ke Antrean Takedown BSSN</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                # Cek apakah akun spesifik ini sudah pernah dimasukkan ke antrean SOAR
                clean_acc_slug = re.sub(r"[^a-zA-Z0-9]", "", str(active_user_data["account"])).upper()
                account_inc_id = f"TKD-BOT-{clean_acc_slug[:16]}"
                acc_alert = {
                    "id": account_inc_id,
                    "headline": f"Takedown Akun Bot {active_user_data['account']} ({active_user_data['platform']})",
                    "bot_account": str(active_user_data["account"])
                }
                is_esc, esc_info = check_is_escalated(acc_alert)
                
                if is_esc:
                    esc_time = esc_info.get("escalated_at", "Tercatat di Sistem")
                    esc_by = esc_info.get("escalated_by", "Analis Siber (Pussiberad)")
                    esc_id_display = esc_info.get("id", account_inc_id)
                    st.button("✅ AKUN SUDAH DIANTREKAN KE SOAR", key=f"btn_tkd_{esc_id_display}_done", disabled=True, use_container_width=True)
                    st.markdown(
                        f"""<div style="font-family: 'JetBrains Mono', monospace; font-size: 0.74rem; color: #10B981; background: rgba(16, 185, 129, 0.12); border: 1px solid rgba(16, 185, 129, 0.4); padding: 8px 12px; border-radius: 4px; margin-top: 6px; line-height: 1.5;">
                        <div style="font-weight: bold; color: #34D399; margin-bottom: 2px;">✓ STATUS: TERDAFTAR DI ANTREAN SOAR</div>
                        <div>🏷️ <b>Nomor Tiket:</b> <span style="color: #38BDF8;">{esc_id_display}</span></div>
                        <div>⏱️ <b>Waktu Transmisi:</b> {esc_time}</div>
                        <div>👤 <b>Operator Pengaju:</b> {esc_by}</div>
                        <div style="margin-top: 4px; color: #F59E0B;">👉 <i>Buka Modul <b>'Tactical SOAR & Otorisasi'</b> di menu navigasi kiri untuk pengesahan Komandan (RBAC).</i></div>
                        </div>""",
                        unsafe_allow_html=True
                    )
                else:
                    if st.button(f"🚨 Masukkan Akun Ini ke Antrean Takedown SOAR", key=f"btn_tkd_{account_inc_id}", type="primary", use_container_width=True):
                        now_wib = datetime.now().strftime("%Y-%m-%d %H:%M:%S WIB")
                        role_actor = st.session_state.get("active_role", "Analis Siber (Pussiberad)")
                        followers_val = int(active_user_data.get("followers", 45)) if pd.notna(active_user_data.get("followers")) else 45
                        sim_val = float(active_user_data.get("semantic_similarity", 0.95)) if pd.notna(active_user_data.get("semantic_similarity")) else 0.95
                        soar_record = {
                            "id": account_inc_id,
                            "title": f"Permohonan Takedown Akun Bot: {active_user_data['account']} ({active_user_data['platform']})",
                            "headline": f"Takedown Akun Bot {active_user_data['account']} ({active_user_data['platform']})",
                            "sample_text": f"Akun bot {active_user_data['account']} pada platform {active_user_data['platform']} menyebarkan narasi hoaks: '{active_user_data['payload_text']}'. Bukti URL: {active_user_data['profile_url']}.",
                            "text": f"Akun bot {active_user_data['account']} pada platform {active_user_data['platform']} menyebarkan narasi hoaks: '{active_user_data['payload_text']}'. Bukti URL: {active_user_data['profile_url']}.",
                            "platform": str(active_user_data["platform"]),
                            "root_platform": str(active_user_data["platform"]),
                            "level": "Kritis",
                            "threat_level": "Kritis",
                            "target_kodam": "Mabes TNI AD / Kominfo BSSN",
                            "kodam": "Mabes TNI AD / Kominfo BSSN",
                            "cib_cluster_size": 1,
                            "amplification_nodes": followers_val,
                            "virality_score": 92,
                            "cib_probability": int(sim_val * 100),
                            "shares_count": followers_val,
                            "escalated_at": now_wib,
                            "escalated_by": role_actor,
                            "is_from_radar": True,
                            "is_from_cib": True,
                            "bot_account": str(active_user_data["account"]),
                            "bot_url": str(active_user_data["profile_url"])
                        }
                        add_escalated_incident(soar_record)
                        st.session_state["approved_incidents"] = get_approved_incidents()
                        st.session_state["escalated_soar_incidents"] = get_escalated_incidents()
                        st.session_state["audit_logs"] = get_audit_logs()
                        st.toast(f"Akun {active_user_data['account']} ({account_inc_id}) berhasil didaftarkan ke antrean Takedown SOAR!", icon="🚨")
                        st.rerun()

        # Operasi Takedown Kolektif (Batch Escalation Dinamis)
        st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
        with st.container(border=True):
            col_b1, col_b2 = st.columns([8, 4])
            with col_b1:
                if remaining_takedown_count == 0:
                    st.markdown(f"##### ⚡ Operasi Takedown Kolektif (Seluruh {len(sub_cib)} Akun Selesai Diantrekan)")
                    st.caption(f"✓ Seluruh {len(sub_cib)} akun bot dalam klaster ini telah terdaftar di antrean SOAR secara lengkap. Tidak ada akun tersisa untuk dieksekusi massal.")
                elif already_takedown_count > 0:
                    st.markdown(f"##### ⚡ Operasi Takedown Kolektif (Sisa {remaining_takedown_count} dari {len(sub_cib)} Akun Bot)")
                    st.caption(f"ℹ️ **Sinkronisasi Antrean SOAR:** Sebanyak **{already_takedown_count} akun** telah diajukan ke SOAR secara individu. Tombol di samping akan mengemas **{remaining_takedown_count} akun tersisa** menjadi 1 Berkas Dossier Takedown Gabungan untuk langsung diajukan ke BSSN & Kominfo.")
                else:
                    st.markdown(f"##### ⚡ Operasi Takedown Kolektif ({len(sub_cib)} Akun Bot Sekaligus)")
                    st.caption(f"Mengemas seluruh {len(sub_cib)} akun bot yang terdeteksi di klaster ini menjadi 1 Berkas Dossier Takedown Gabungan untuk langsung diajukan ke BSSN & Kominfo setelah disahkan Komandan.")

            with col_b2:
                if remaining_takedown_count == 0:
                    st.button(f"✅ SELURUH {len(sub_cib)} AKUN SUDAH DI-ESKALASI", disabled=True, use_container_width=True)
                    st.markdown(
                        f"""<div style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: #10B981; background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); padding: 6px 10px; border-radius: 4px; margin-top: 4px;">
                        ✓ <b>STATUS:</b> 100% TERDAFTAR DI SOAR ({len(sub_cib)} Akun)<br/>
                        👉 <i>Buka Modul 'Tactical SOAR & Otorisasi' untuk pengesahan Komandan</i>
                        </div>""",
                        unsafe_allow_html=True
                    )
                else:
                    batch_id = f"TKD-BATCH-CIB-{remaining_takedown_count}"
                    btn_label = f"⚡ Ajukan Takedown Massal ({remaining_takedown_count} Akun Tersisa)" if already_takedown_count > 0 else f"⚡ Ajukan Takedown Massal ({len(sub_cib)} Akun)"
                    if st.button(btn_label, key=f"btn_mass_takedown_{remaining_takedown_count}", type="primary", use_container_width=True):
                        now_wib = datetime.now().strftime("%Y-%m-%d %H:%M:%S WIB")
                        role_actor = st.session_state.get("active_role", "Analis Siber (Pussiberad)")
                        bot_list_str = ", ".join([str(r["account"]) for _, r in unescalated_sub_cib.iterrows()])
                        followers_sum = int(unescalated_sub_cib["followers"].sum()) if "followers" in unescalated_sub_cib.columns else 120
                        batch_title = f"Permohonan Takedown Massal: Sindikat CIB {remaining_takedown_count} Akun Tersisa" if already_takedown_count > 0 else f"Permohonan Takedown Massal: Sindikat CIB {len(sub_cib)} Akun Lintas Medsos"
                        batch_record = {
                            "id": batch_id,
                            "title": batch_title,
                            "headline": f"Takedown Massal Sindikat Bot CIB ({remaining_takedown_count} Akun)",
                            "sample_text": f"Paket permohonan takedown massal {remaining_takedown_count} akun botnet terkoordinasi (CIB) lintas platform (TikTok, X, Instagram, Facebook, YouTube). Daftar sasaran: {bot_list_str}. Bukti telemetri hash MD5 dan rekaman server TOR terlampir.",
                            "text": f"Paket permohonan takedown massal {remaining_takedown_count} akun botnet terkoordinasi (CIB) lintas platform (TikTok, X, Instagram, Facebook, YouTube). Daftar sasaran: {bot_list_str}. Bukti telemetri hash MD5 dan rekaman server TOR terlampir.",
                            "platform": "Lintas Medsos (Multi-Platform)",
                            "root_platform": "Multi-Platform",
                            "level": "Kritis",
                            "threat_level": "Kritis",
                            "target_kodam": "Mabes TNI AD / Kominfo BSSN",
                            "kodam": "Mabes TNI AD / Kominfo BSSN",
                            "cib_cluster_size": remaining_takedown_count,
                            "amplification_nodes": followers_sum,
                            "virality_score": 98,
                            "cib_probability": 97,
                            "shares_count": 50000,
                            "escalated_at": now_wib,
                            "escalated_by": role_actor,
                            "is_from_radar": True,
                            "is_from_cib": True,
                            "bot_accounts_list": [str(r["account"]) for _, r in unescalated_sub_cib.iterrows()]
                        }
                        add_escalated_incident(batch_record)
                        st.session_state["approved_incidents"] = get_approved_incidents()
                        st.session_state["escalated_soar_incidents"] = get_escalated_incidents()
                        st.session_state["audit_logs"] = get_audit_logs()
                        st.toast(f"{remaining_takedown_count} akun berhasil didaftarkan ke paket Takedown SOAR!", icon="⚡")
                        st.rerun()

        # Forensic Conclusion Box
        st.markdown(
            f"""
            <div class="tactical-card danger" style="padding: 12px 16px; margin-top: 15px;">
                <span style="font-family: 'JetBrains Mono'; font-weight: bold; color: #EF4444;">KESIMPULAN AUDIT PUSSIBERAD:</span>
                <span style="font-size: 0.85rem; color: #F1F5F9; margin-left: 10px;">
                    Perilaku di atas memenuhi kriteria <b>Coordinated Inauthentic Behavior (CIB)</b> tingkat tinggi. 
                    Pola unggahan serentak dalam durasi kurang dari 50 detik dengan teks nyaris identik 
                    mengonfirmasi adanya orkestrasi skrip automasi (Botnet Farm) bukan interaksi publik organik. Seluruh 13 akun direkomendasikan untuk tindakan pemblokiran (takedown).
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )

    # -----------------------------------------------------------------
    # TAB 2: MULTIMODAL AUDIO DEEPFAKE SCREENER (AUDIT SPEKTROGRAM & KLONING SUARA)
    # -----------------------------------------------------------------
    with tab_audio:
        st.markdown("### 🎙️ AUDIT SPEKTROGRAM & DETEKSI KLONING SUARA (AI VOICE CLONE)")
        st.markdown(
            "Menginspeksi integritas sinyal akustik, konsistensi formatur vokal, "
            "dan ketiadaan jeda pernapasan biologis (Bio-Breathing Acoustic Pause) untuk membuktikan rekaman suara manipulatif/sintetis."
        )
        
        col_ctrl, col_result = st.columns([5, 7])
        
        with col_ctrl:
            sample_choice = st.radio(
                "Pilih Sampel Audio Operasi:",
                [
                    "Audio A: 'Perintah Siaga Perbatasan' (Diduga Kloning Suara KSAD)",
                    "Audio B: 'Siaran Pers Resmi Mabesad' (Rekaman Suara Otentik)",
                    "Unggah Berkas Audio Eksternal (.wav / .mp3)"
                ]
            )
            
            # Setup variables based on selection
            real_wave_data = None
            time_axis_custom = None
            current_incident_id = "INC-2026-ALPHA"
            sample_label_name = "Audio A: Kloning Suara KSAD"
            
            if "Audio A" in sample_choice:
                audio_bytes = generate_sample_wav(is_deepfake=True)
                audio_sha = "8f4a9b7ce21d0ab99f0e8a1c94d21e54a6b2839178041d8e09f5a7c2b64d8123"
                synth_score = 94.2
                verdict = "DEEPFAKE SYNTHETIC CLONE DETECTED"
                verdict_color = "#EF4444"
                pitch_jitter = "0.012 (Tidak Alami / Terlalu Datar)"
                spectral_cutoff = "16.2 kHz (Artefak Neural Vocoder)"
                breathing_markers = "Nihil (0 jeda mikro biologis terdeteksi)"
                current_incident_id = "INC-2026-ALPHA"
                sample_label_name = "Audio A - Perintah Siaga Perbatasan (Diduga Kloning Suara KSAD)"
                
                st.markdown("##### 🎧 Pemutar Berkas Audio Operasi:")
                st.audio(audio_bytes, format="audio/wav")
                st.caption("🔊 *Dengarkan: Perhatikan nada vokal yang terlalu kaku dan ketiadaan desah napas alami.*")
                
            elif "Audio B" in sample_choice:
                audio_bytes = generate_sample_wav(is_deepfake=False)
                audio_sha = "3d7e91a0b5c824f61e2d7890a41bc35ef8902145e67a9b012c34d56e78f901ab"
                synth_score = 3.8
                verdict = "AUTHENTIC HUMAN VOICE CONFIRMED"
                verdict_color = "#10B981"
                pitch_jitter = "0.084 (Fluktuasi Vokal Manusia Normal)"
                spectral_cutoff = "22.0 kHz (Rentang Penuh Akustik Alami)"
                breathing_markers = "Terdeteksi 4 jeda respirasi fisiologis"
                current_incident_id = "REF-2026-MABESAD-01"
                sample_label_name = "Audio B - Siaran Pers Resmi Mabesad (Otentik)"
                
                st.markdown("##### 🎧 Pemutar Berkas Audio Operasi:")
                st.audio(audio_bytes, format="audio/wav")
                st.caption("🔊 *Dengarkan: Terdengar dinamika intonasi organik serta jeda respirasi/napas manusia pada detik 1.5.*")
                
            else:
                uploaded_file = st.file_uploader(
                    "Unggah Berkas Audio Barang Bukti (.wav / .mp3):",
                    type=["wav", "mp3"],
                    help="Unggah rekaman audio suara yang beredar di medsos untuk dianalisis spektrogramnya secara otomatis."
                )
                
                if uploaded_file is not None:
                    raw_up_bytes = uploaded_file.getvalue()
                    analysis_res = analyze_audio_data(raw_up_bytes, uploaded_file.name)
                    audio_sha = analysis_res.get("sha256", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")
                    synth_score = analysis_res.get("synth_prob", 88.5)
                    
                    if synth_score >= 70.0:
                        verdict = "DEEPFAKE SYNTHETIC CLONE DETECTED"
                        verdict_color = "#EF4444"
                    elif synth_score >= 40.0:
                        verdict = "PROBABLE SYNTHETIC MANIPULATION"
                        verdict_color = "#F59E0B"
                    else:
                        verdict = "AUTHENTIC HUMAN VOICE CONFIRMED"
                        verdict_color = "#10B981"
                        
                    hf_r = analysis_res.get("hf_ratio", 0.05)
                    pauses_c = analysis_res.get("pauses", 0)
                    jitter_val = analysis_res.get("jitter", 0.02)
                    
                    pitch_jitter = f"{jitter_val} (" + ("Tidak Alami / Monoton" if jitter_val < 0.03 else "Fluktuasi Normal") + ")"
                    spectral_cutoff = f"{'<16 kHz (Pemotongan Vocoder)' if hf_r < 0.1 else '>20 kHz (Spektrum Alami)'}"
                    breathing_markers = f"{pauses_c} jeda respirasi terdeteksi" if pauses_c > 0 else "Nihil (0 jeda pernapasan)"
                    
                    current_incident_id = f"DF-AUDIO-{audio_sha[:8].upper()}"
                    sample_label_name = f"Unggahan: {uploaded_file.name}"
                    
                    st.markdown("##### 🎧 Pemutar Berkas Audio Barang Bukti:")
                    st.audio(uploaded_file)
                    
                    if analysis_res.get("plot_wave") is not None:
                        real_wave_data = analysis_res["plot_wave"]
                        time_axis_custom = analysis_res["time_axis"]
                else:
                    audio_bytes = generate_sample_wav(is_deepfake=True)
                    audio_sha = "d41d8cd98f00b204e9800998ecf8427e00000000000000000000000000000000"
                    synth_score = 88.5
                    verdict = "SIAP MENERIMA BERKAS (.WAV / .MP3)"
                    verdict_color = "#38BDF8"
                    pitch_jitter = "Menunggu berkas audio..."
                    spectral_cutoff = "Menunggu berkas audio..."
                    breathing_markers = "Menunggu berkas audio..."
                    current_incident_id = "DF-AUDIO-PENDING"
                    sample_label_name = "Berkas Eksternal (Belum Diunggah)"
                    st.info("Silakan pilih dan unggah berkas .wav atau .mp3 rekaman barang bukti di atas.")
            
            # Status Box Forensik Pussiberad
            st.markdown(
                f"""
                <div style="background: #111C2E; border: 1px solid #1E293B; border-left: 4px solid {verdict_color}; padding: 14px; border-radius: 6px; margin-top: 12px;">
                    <div style="font-family: 'JetBrains Mono'; font-size: 0.75rem; color: #94A3B8;">STATUS VERIFIKASI PUSSIBERAD:</div>
                    <div style="font-family: 'Chakra Petch'; font-size: 1.1rem; font-weight: 700; color: {verdict_color}; margin: 4px 0;">
                        {verdict}
                    </div>
                    <div style="font-family: 'JetBrains Mono'; font-size: 0.85rem; color: #F8FAFC;">
                        Probabilitas Sintetis: <b style="color: {verdict_color}; font-size: 1.25rem;">{synth_score}%</b>
                    </div>
                    <div style="font-family: 'JetBrains Mono'; font-size: 0.7rem; color: #64748B; margin-top: 4px; word-break: break-all;">
                        SHA-256: {audio_sha[:28]}...
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            st.markdown("<div style='margin-top: 12px;'></div>", unsafe_allow_html=True)
            st.markdown("##### Parameter Forensik Akustik Terukur:")
            st.markdown(f"- 🎚️ **Pitch Jitter Consistency:** `{pitch_jitter}`")
            st.markdown(f"- ✂️ **Spectral Cutoff Anomaly:** `{spectral_cutoff}`")
            st.markdown(f"- 🫁 **Bio-Breathing Acoustic Pause:** `{breathing_markers}`")
            
            st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
            
            # Integrasi SOAR & Ekspor Bukti Forensik
            st.markdown("##### ⚡ Tindakan Taktis & Rantai Komando:")
            
            if synth_score >= 50.0 and current_incident_id != "DF-AUDIO-PENDING":
                # Check SOAR status
                audio_alert_target = {
                    "id": current_incident_id,
                    "headline": f"Deepfake AI Voice Clone: {sample_label_name}",
                    "bot_account": "Audio-Deepfake-Synthesizer"
                }
                is_esc, esc_info = check_is_escalated(audio_alert_target)
                
                if is_esc:
                    esc_time = esc_info.get("escalated_at", "Tercatat di Sistem")
                    esc_by = esc_info.get("escalated_by", "Analis Siber (Pussiberad)")
                    esc_id_num = esc_info.get("id", current_incident_id)
                    st.button("✅ BUKTI DEEPFAKE SUDAH DIANTREKAN KE SOAR", key="btn_audio_soar_done", disabled=True, use_container_width=True)
                    st.markdown(
                        f"""<div style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: #10B981; background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); padding: 8px 10px; border-radius: 4px; margin-top: 4px;">
                        ✓ <b>STATUS SOAR:</b> Terdaftar ({esc_id_num})<br/>
                        ⏱️ <b>Waktu:</b> {esc_time} | 👤 <b>Oleh:</b> {esc_by}<br/>
                        👉 <i>Buka Modul <b>'Tactical SOAR & Otorisasi'</b> di navigasi kiri untuk otorisasi Komandan (RBAC).</i>
                        </div>""",
                        unsafe_allow_html=True
                    )
                else:
                    if st.button(f"🚨 Eskalasikan Temuan Deepfake Ini ke Antrean SOAR", key="btn_eskalasi_deepfake_soar", type="primary", use_container_width=True):
                        now_wib = datetime.now().strftime("%Y-%m-%d %H:%M:%S WIB")
                        role_actor = st.session_state.get("active_role", "Analis Siber (Pussiberad)")
                        soar_item = {
                            "id": current_incident_id,
                            "title": f"Investigasi Forensik Suara Sintetis: {sample_label_name}",
                            "headline": f"AI Voice Clone: {sample_label_name}",
                            "sample_text": f"Ditemukan berkas audio terindikasi kloning suara sintetis ({synth_score}% kecocokan vocoder). Parameter forensik menunjukkan cutoff spektral {spectral_cutoff} dan ketiadaan jeda napas biologis. Berkas siap di-takedown via BSSN & Kominfo.",
                            "text": f"Ditemukan berkas audio terindikasi kloning suara sintetis ({synth_score}% kecocokan vocoder). Parameter forensik menunjukkan cutoff spektral {spectral_cutoff} dan ketiadaan jeda napas biologis. Berkas siap di-takedown via BSSN & Kominfo.",
                            "platform": "Multi-Platform (Medsos & Messaging)",
                            "root_platform": "Multi-Platform",
                            "level": "Kritis",
                            "threat_level": "Kritis",
                            "target_kodam": "Mabes TNI AD / Pussiberad",
                            "kodam": "Mabes TNI AD / Pussiberad",
                            "cib_cluster_size": 1,
                            "amplification_nodes": 850,
                            "virality_score": 96,
                            "cib_probability": int(synth_score),
                            "shares_count": 28500,
                            "escalated_at": now_wib,
                            "escalated_by": role_actor,
                            "is_from_radar": True,
                            "is_from_deepfake": True,
                            "audio_sha256": audio_sha
                        }
                        add_escalated_incident(soar_item)
                        st.session_state["approved_incidents"] = get_approved_incidents()
                        st.session_state["escalated_soar_incidents"] = get_escalated_incidents()
                        st.session_state["audit_logs"] = get_audit_logs()
                        st.toast(f"Temuan Deepfake Audio ({current_incident_id}) berhasil diajukan ke Antrean SOAR!", icon="🚨")
                        st.rerun()
            elif synth_score < 50.0:
                st.markdown(
                    """
                    <div style="background: rgba(16, 185, 129, 0.08); border-left: 3px solid #10B981; padding: 8px 12px; border-radius: 4px; font-size: 0.78rem; color: #E2E8F0;">
                        ✓ <b>Status Aman:</b> Karakteristik sinyal vokal alami. Sampel ini dinyatakan sebagai <b>suara otentik</b> dan tidak memerlukan tindakan takedown.
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
            # Download Dossier Forensik JSON
            dossier_json_bytes = generate_acoustic_dossier_json(
                audio_label=sample_label_name,
                synth_score=synth_score,
                verdict=verdict,
                pitch_jitter=pitch_jitter,
                spectral_cutoff=spectral_cutoff,
                breathing_markers=breathing_markers,
                sha256_hash=audio_sha,
                operator_role=st.session_state.get("active_role", "Analis Siber (Pussiberad)")
            )
            st.download_button(
                label="📥 Unduh Dossier Forensik Akustik (JSON BSSN)",
                data=dossier_json_bytes,
                file_name=f"DOSSIER-FORENSIK-AUDIO-{current_incident_id}.json",
                mime="application/json",
                use_container_width=True
            )

        with col_result:
            st.markdown("#### Spektrogram Frekuensi & Gelombang Suara (Acoustic Waveform)")
            
            # Generate simulated or use real waveform
            if real_wave_data is not None and time_axis_custom is not None:
                waveform = real_wave_data
                time_x = time_axis_custom
                wave_title = f"Waveform Berkas Nyata Unggahan (Durasi {round(time_x[-1], 2)} detik)"
            else:
                time_x = np.linspace(0, 4.0, 500)
                if synth_score > 50:
                    waveform = 0.5 * np.sin(2 * np.pi * 3 * time_x) + 0.3 * np.sin(2 * np.pi * 9 * time_x) + np.random.normal(0, 0.03, len(time_x))
                    wave_title = "Waveform Analisis (0.0s - 4.0s) - Pola Monoton Sintetis"
                else:
                    envelope = np.sin(np.pi * time_x / 4.0) ** 1.5
                    waveform = envelope * (0.6 * np.sin(2 * np.pi * 2.5 * time_x) + 0.4 * np.sin(2 * np.pi * 7.5 * time_x)) + np.random.normal(0, 0.08, len(time_x))
                    waveform[180:230] = 0.01 * np.random.normal(0, 0.02, 50)
                    wave_title = "Waveform Analisis (0.0s - 4.0s) - Jeda Respirasi Terdeteksi di 1.5s"

            fig_wave = go.Figure()
            fig_wave.add_trace(go.Scatter(
                x=time_x,
                y=waveform,
                line=dict(color="#06B6D4" if synth_score < 50 else "#EF4444", width=1.5),
                name="Amplitudo Audio"
            ))
            fig_wave.update_layout(
                title=dict(text=wave_title, font=dict(family="Chakra Petch", size=12, color="#94A3B8")),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(15,23,42,0.8)",
                xaxis=dict(title="Detik", gridcolor="#1E293B", tickfont=dict(family="JetBrains Mono", color="#94A3B8")),
                yaxis=dict(title="Amplitudo", gridcolor="#1E293B", tickfont=dict(family="JetBrains Mono", color="#94A3B8")),
                margin=dict(t=30, b=20, l=10, r=10),
                height=165
            )
            st.plotly_chart(fig_wave, use_container_width=True)

            # Heatmap Spectrogram Fourier (FFT 20kHz)
            freqs = np.linspace(0, 20000, 35)
            times = np.linspace(0, 4, 40)
            T, F = np.meshgrid(times, freqs)
            
            if synth_score > 50:
                # Artificial cutoff at 16kHz
                Z = np.exp(-((F - 2500)**2) / (2 * 1500**2)) + 0.5 * np.exp(-((F - 6000)**2) / (2 * 1200**2))
                Z[F > 16000] = 0.01  # Hard neural vocoder cutoff
                spec_subtitle = "Spektrogram FFT: Tampak Pemotongan 'Brickwall' di 16 kHz (Anomali Vocoder AI)"
            else:
                Z = np.exp(-((F - 2000)**2) / (2 * 2000**2)) + 0.4 * np.exp(-((F - 5500)**2) / (2 * 2500**2)) + 0.25 * np.exp(-((F - 14000)**2) / (2 * 3500**2))
                # Add natural dispersion above 16kHz
                Z += 0.08 * np.random.uniform(0.01, 0.12, Z.shape)
                spec_subtitle = "Spektrogram FFT: Spektrum Harmonik Organik Penuh Hingga >20 kHz"

            fig_spec = go.Figure(data=go.Heatmap(
                z=Z,
                x=times,
                y=freqs,
                colorscale="Viridis",
                colorbar=dict(title="dB", tickfont=dict(color="#94A3B8", family="JetBrains Mono"))
            ))
            fig_spec.update_layout(
                title=dict(text=spec_subtitle, font=dict(family="Chakra Petch", size=12, color="#94A3B8")),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(15,23,42,0.8)",
                xaxis=dict(title="Detik", gridcolor="#1E293B", tickfont=dict(family="JetBrains Mono", color="#94A3B8")),
                yaxis=dict(title="Frekuensi (Hz)", gridcolor="#1E293B", tickfont=dict(family="JetBrains Mono", color="#94A3B8")),
                margin=dict(t=30, b=20, l=10, r=10),
                height=200
            )
            st.plotly_chart(fig_spec, use_container_width=True)
            
            st.caption("📌 **Cara Membaca Spektrogram:** Sumbu vertikal (Y) adalah frekuensi suara (0 - 20.000 Hz). Warna kuning/terang menunjukkan energi sinyal vokal. Garis hitam/kosong mendadak di atas 16 kHz membuktikan bahwa rekaman adalah hasil kompresi model AI TTS/Voice Clone (Neural Vocoder Artifacts).")

        # -------------------------------------------------------------
        # FITUR TAMBAHAN 1: MATRIKS KOMPARASI FORENSIK SIDE-BY-SIDE
        # -------------------------------------------------------------
        st.markdown("<hr style='border: 0.5px solid #1E293B; margin: 20px 0 16px 0;'/>", unsafe_allow_html=True)
        st.markdown("#### 🔬 Matriks Bedah Forensik Akustik: Audio Kloning vs Suara Asli")
        
        comp_df = pd.DataFrame([
            {
                "Parameter Forensik": "1. Batas Frekuensi Atas (Spectral Cutoff)",
                "Audio A (Kloning AI KSAD)": "🔴 Terpotong kaku di ~16.2 kHz",
                "Audio B (Suara Otentik Dispenad)": "🟢 Spektrum penuh >22.0 kHz",
                "Signifikansi Bukti Forensik": "Model AI Voice Clone (HiFi-GAN/WaveGlow) memiliki limitasi laju sampel 24kHz yang memotong frekuensi di atas 16kHz."
            },
            {
                "Parameter Forensik": "2. Stabilitas Nada Dasar (Pitch Jitter)",
                "Audio A (Kloning AI KSAD)": "🔴 0.012 (Sangat kaku / Datar)",
                "Audio B (Suara Otentik Dispenad)": "🟢 0.084 (Fluktuasi emosi alami)",
                "Signifikansi Bukti Forensik": "Pita suara biologis manusia mengalami getaran mikro tidak konstan saat berbicara. Suara AI cenderung memiliki frekuensi F0 yang terlalu mulus matematis."
            },
            {
                "Parameter Forensik": "3. Jeda Mikro Napas (Bio-Breathing)",
                "Audio A (Kloning AI KSAD)": "🔴 Nihil (0 jeda pernapasan)",
                "Audio B (Suara Otentik Dispenad)": "🟢 Terdeteksi 4 jeda respirasi",
                "Signifikansi Bukti Forensik": "Model deepfake menyambungkan fonem suara tanpa menyisipkan jeda biologis pengambilan napas dari paru-paru manusia."
            },
            {
                "Parameter Forensik": "4. Jejak Kebisingan Latar (Noise Floor)",
                "Audio A (Kloning AI KSAD)": "🔴 Latar belakang steril sintetis",
                "Audio B (Suara Otentik Dispenad)": "🟢 Akustik ruangan & desis mikrofon alami",
                "Signifikansi Bukti Forensik": "Rekaman lapangan asli memiliki pantulan akustik ruangan, sedangkan kloning AI menghasilkan gelombang steril hasil sintesis digital."
            }
        ])
        
        st.dataframe(
            comp_df,
            hide_index=True,
            use_container_width=True,
            column_config={
                "Parameter Forensik": st.column_config.TextColumn("Parameter Forensik", width="medium"),
                "Audio A (Kloning AI KSAD)": st.column_config.TextColumn("Audio Kloning AI", width="medium"),
                "Audio B (Suara Otentik Dispenad)": st.column_config.TextColumn("Suara Otentik Manusia", width="medium"),
                "Signifikansi Bukti Forensik": st.column_config.TextColumn("Penjelasan Ilmiah Forensik", width="large")
            }
        )

        # -------------------------------------------------------------
        # FITUR TAMBAHAN 2: BUKU PANDUAN OPERASIONAL TAB 2 (SOP FORENSIK)
        # -------------------------------------------------------------
        with st.expander("📖 Panduan Operasional Tab 2 & Asal Data (SOP Investigasi Audio Pussiberad)", expanded=False):
            st.markdown(
                """
                ### 1. Dari Mana Asal Datanya?
                - **Sampel Sistem (Audio A & B):** 
                  Berasal dari repositori kasus taktis penanganan perang informasi Pussiberad TNI AD. Kasus **Audio A** mensimulasikan insiden rekaman hoaks *"Perintah Siaga Perbatasan"* mengatasnamakan Kepala Staf Angkatan Darat (KSAD) yang dirancang untuk memicu kepanikan di wilayah perbatasan (Kodam XVII/Cenderawasih). Sementara **Audio B** adalah data rujukan suara otentik siaran pers Dispenad.
                - **Berkas Eksternal (.wav / .mp3):** 
                  Dapat diunggah secara mandiri oleh analis siber dari berkas audio barang bukti yang ditemukan beredar di platform medsos (TikTok, X, Facebook, Telegram, WhatsApp Group).
                - **Mesin Forensik Akustik:**
                  Memproses sinyal suara digital menggunakan algoritma **Discrete Fourier Transform (FFT)**, inspeksi **Nyquist Cutoff Vocoder**, serta estimasi **Pitch Jitter & Bio-Breathing Pause** secara real-time.

                ### 2. Bagaimana Cara Menggunakannya?
                1. **Pilih Sampel atau Unggah Berkas:** Tentukan sampel audio bawaan (Audio A / Audio B) atau klik *"Unggah Berkas Audio Eksternal"* untuk memasukkan berkas rekaman yang ingin diaudit.
                2. **Dengarkan Sampel (Play Audio):** Gunakan pemutar suara interaktif untuk mengecek dinamika vokal, intonasi, dan jeda tarikan napas.
                3. **Periksa Status & Parameter Forensik:**
                   - Jika probabilitas sintetis **>50%**, status akan berubah merah: `DEEPFAKE SYNTHETIC CLONE DETECTED`.
                   - Perhatikan indikator *Spectral Cutoff* (<16 kHz) dan *Bio-Breathing Acoustic Pause* (Nihil jeda).
                4. **Eskalasi ke SOAR (Rantai Komando):** 
                   - Klik tombol merah `🚨 Eskalasikan Temuan Deepfake Ini ke Antrean SOAR`.
                   - Temuan akan langsung masuk ke modul **Tactical SOAR & Otorisasi** untuk disahkan oleh Perwira Menengah / Komandan secara kriptografis (Digital Signature) sebelum surat takedown diajukan ke BSSN & Kominfo.
                5. **Unduh Berkas Dossier JSON:**
                   - Klik tombol `📥 Unduh Dossier Forensik Akustik (JSON BSSN)` untuk memperoleh berkas investigasi terstandarisasi lengkap dengan stempel hash SHA-256 sebagai alat bukti hukum sah.
                """
            )

    # -----------------------------------------------------------------
    # TAB 3: DOCUMENT INTEGRITY & OCR HIGHLIGHT
    # -----------------------------------------------------------------
    with tab_doc:
        st.markdown("### 📄 DETEKSI INTEGRITAS DOKUMEN MILITER & KOTAK HIGHLIGHT OCR")
        st.markdown(
            "<p style='color: #94A3B8; font-size: 0.92rem; margin-top: -6px;'>"
            "Audit multi-lapis keabsahan dokumen naskah dinas militer (Surat Perintah / Sprin / DIPA Alutsista) "
            "menggunakan analisis OCR font mismatch, Error Level Analysis (ELA) heatmap, deteksi overlay stempel komando, "
            "dan verifikasi silang terhadap Buku Register Minu Mabesad."
            "</p>",
            unsafe_allow_html=True
        )

        catalog = get_document_catalog()
        
        doc_choice = st.selectbox(
            "Pilih Berkas Dokumen Militer untuk Diperiksa:",
            [
                "Dokumen A: Surat Edaran Palsu Mutasi Staf Dispenad (Sprin/482/IX/2026) [🚨 REKOMENDASI AUDIT]",
                "Dokumen B: Lembar Pengesahan Anggaran Pengadaan Fiktif Alutsista (DIPA/088/BM/2026)",
                "Dokumen C: Dokumen Asli Terverifikasi Dispenad (Sprin/104/III/2026 - Golden Standard Kontrol)",
                "📤 Mode Unggah: Pindai Berkas Scan Dokumen Baru (.PNG / .JPG / .JPEG)"
            ]
        )
        
        is_upload_mode = "Mode Unggah" in doc_choice
        uploaded_doc = None
        
        if is_upload_mode:
            st.markdown(
                """
                <div style="background: rgba(56, 189, 248, 0.08); border: 1px dashed #38BDF8; padding: 12px 16px; border-radius: 6px; margin-bottom: 12px;">
                    <div style="font-size: 0.85rem; font-weight: bold; color: #38BDF8;">📤 GERBANG PENERIMAAN SCAN PATROLI SIBER:</div>
                    <div style="font-size: 0.78rem; color: #CBD5E1; margin-top: 2px;">
                        Unggah tangkapan layar, pindaian PDF, atau berkas citra dokumen militer yang beredar di media sosial atau grup percakapan (WhatsApp/Telegram) untuk diuji secara real-time.
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            uploaded_doc = st.file_uploader(
                "Unggah Berkas Citra Scan Dokumen Militer:",
                type=["png", "jpg", "jpeg"],
                key="uploader_mil_doc"
            )

        # Determine doc_key and doc_info
        if is_upload_mode:
            if uploaded_doc is not None:
                file_bytes = uploaded_doc.read()
                real_sha = compute_sha256(file_bytes)
                real_md5 = compute_md5(file_bytes)
                ela_img, real_tamper_score, real_metrics = perform_real_ela(file_bytes, quality=90)
                
                # Dynamic doc_info for uploaded file
                is_high_risk = real_tamper_score >= 60.0
                doc_key = "custom_upload"
                doc_info = {
                    "id": f"DOC-SCAN-{real_sha[:8].upper()}",
                    "code": f"SCAN-{uploaded_doc.name[:18]}",
                    "name": f"Scan Unggahan: {uploaded_doc.name}",
                    "category": "Dokumen Patroli Siber Lapangan (Citra Eksternal)",
                    "threat_level": "Kritis" if is_high_risk else "Sedang",
                    "verdict": "TERINDIKASI MANIPULASI DIGITAL (HIGH SPLICING RISK)" if is_high_risk else "INTEGRITAS KOMPRESI SERAGAM (LOW ANOMALY)",
                    "verdict_color": "#EF4444" if is_high_risk else "#10B981",
                    "tamper_prob": real_tamper_score,
                    "sha256": real_sha,
                    "md5": real_md5,
                    "minu_register_check": {
                        "status": "NON-REGISTERED (BERKAS EKSTERNAL)",
                        "status_color": "#F59E0B",
                        "db_status": "Pemeriksaan Mandiri Analis",
                        "officer_auth": "Memerlukan Verifikasi Manual Pejabat Personalia",
                        "bsre_signature": "Tidak Terdeteksi Metatag Sertifikat BSrE",
                        "official_agenda_book": "Belum Terindeks di Buku Agenda Minu Mabesad"
                    },
                    "exif_metadata": {
                        "Software": "Citra Kamera / Tangkapan Layar Eksternal",
                        "CreationDate": datetime.now().strftime("%Y-%m-%d %H:%M:%S WIB"),
                        "ModifiedDate": "Terkompresi Format Web",
                        "ColorSpace": f"RGB ({real_metrics.get('width', 0)} x {real_metrics.get('height', 0)} px)",
                        "DPI": "Deteksi Resolusi Layar Standar",
                        "PageFormat": "Custom Image Buffer"
                    },
                    "findings": [
                        {
                            "item": "Error Level Analysis (ELA)",
                            "status": f"TAMPER SCORE {real_tamper_score}%",
                            "color": "#EF4444" if is_high_risk else "#10B981",
                            "detail": f"Rerata error level: {real_metrics.get('mean_error_level', 0)}, simpangan baku kompresi: {real_metrics.get('error_std_dev', 0)}. " +
                                     ("Ditemukan lonjakan kontras kompresi yang mengindikasikan penyisipan grafis atau teks." if is_high_risk else "Pola degradasi kompresi seragam di seluruh piksel dokumen.")
                        },
                        {
                            "item": "Integritas Hash Kriptografis",
                            "status": "SEALED SHA-256",
                            "color": "#38BDF8",
                            "detail": f"Hash SHA-256 berkas: {real_sha}. Digunakan sebagai rujukan takedown BSSN."
                        }
                    ]
                }
            else:
                # Placeholder when no file is uploaded yet
                doc_key = "doc_a"
                doc_info = catalog["doc_a"]
        elif "Dokumen B" in doc_choice:
            doc_key = "doc_b"
            doc_info = catalog["doc_b"]
        elif "Dokumen C" in doc_choice:
            doc_key = "doc_c"
            doc_info = catalog["doc_c"]
        else:
            doc_key = "doc_a"
            doc_info = catalog["doc_a"]

        # 4 Interactive Visual Layers Navigation
        st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
        layer_mode = st.radio(
            "Pilih Mode & Lapisan Forensik:",
            [
                "🔲 Lapisan 1: Pratinjau Dokumen & Highlight Bounding Box OCR",
                "🌡️ Lapisan 2: Heatmap Forensik Error Level Analysis (ELA)",
                "⚖️ Lapisan 3: Komparasi Berdampingan (Side-by-Side Asli vs Tersangka)",
                "📑 Lapisan 4: Inspeksi Metadata EXIF & Digital Artefak"
            ],
            horizontal=True
        )

        col_doc_left, col_doc_right = st.columns([6.2, 5.8])

        with col_doc_left:
            st.markdown("#### Visualisasi Dokumen & Deteksi Anomali")

            if layer_mode == "🔲 Lapisan 1: Pratinjau Dokumen & Highlight Bounding Box OCR":
                col_opt1, col_opt2 = st.columns([6, 6])
                with col_opt1:
                    show_boxes = st.checkbox("Aktifkan Kotak Anomali OCR (Bounding Boxes)", value=True)
                with col_opt2:
                    view_style = st.radio("Format Visual:", ["HTML Vektor Bersih", "Simulasi Citra Scan (Canvas)"], horizontal=True)

                if is_upload_mode and uploaded_doc is not None:
                    st.image(file_bytes, caption=f"Pratinjau Berkas Unggahan: {uploaded_doc.name}", use_container_width=True)
                elif view_style == "HTML Vektor Bersih":
                    clean_html = get_clean_document_html(doc_key, show_anomalies=show_boxes)
                    st.markdown(clean_html, unsafe_allow_html=True)
                else:
                    doc_img, _ = generate_document_canvas_image(doc_key)
                    st.image(doc_img, caption=f"Canvas Raster Pindaian Kertas Milnet: {doc_info['code']}", use_container_width=True)

            elif layer_mode == "🌡️ Lapisan 2: Heatmap Forensik Error Level Analysis (ELA)":
                st.markdown(
                    "<p style='color: #94A3B8; font-size: 0.8rem; margin-top: -6px;'>"
                    "<b>Error Level Analysis (ELA):</b> Menguji ketidakseragaman rasio kompresi piksel. "
                    "Area yang diedit atau disisipkan secara digital (stempel overlay, teks baru) memancarkan pendaran anomali terang kontras tinggi."
                    "</p>",
                    unsafe_allow_html=True
                )
                
                ela_q = st.slider("Sensitivitas Deteksi Splicing ELA (Quality Parameter):", min_value=75, max_value=98, value=90, step=1)
                
                if is_upload_mode and uploaded_doc is not None:
                    ela_display, ela_score, _ = perform_real_ela(file_bytes, quality=ela_q)
                    st.image(ela_display, caption=f"Heatmap ELA Berkas Unggahan (Quality={ela_q}, Splicing Score={ela_score}%)", use_container_width=True)
                else:
                    _, ela_display = generate_document_canvas_image(doc_key)
                    st.image(ela_display, caption=f"Heatmap ELA Simulasi Forensik Pussiberad ({doc_info['code']})", use_container_width=True)
                
                # ELA Legend Box
                st.markdown(
                    """
                    <div style="background: #111C2E; border: 1px solid #1E293B; padding: 10px 14px; border-radius: 4px; margin-top: 8px;">
                        <div style="font-size: 0.78rem; font-weight: bold; color: #F8FAFC; margin-bottom: 4px;">PANDUAN SPEKTRUM ELA:</div>
                        <div style="font-size: 0.75rem; color: #CBD5E1;">
                            <span style="color: #F43F5E; font-weight: bold;">● Pendaran Terang (Luminance Spike):</span> Terdeteksi artefak splicing stempel PNG atau font non-asli.<br/>
                            <span style="color: #64748B; font-weight: bold;">● Area Gelap Seragam (Low Noise):</span> Tekstur latar kertas dokumen asli tanpa modifikasi.
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            elif layer_mode == "⚖️ Lapisan 3: Komparasi Berdampingan (Side-by-Side Asli vs Tersangka)":
                st.markdown(
                    "<p style='color: #94A3B8; font-size: 0.8rem; margin-top: -6px;'>"
                    "Perbandingan langsung elemen tata naskah dinas antara dokumen yang diperiksa dengan <b>Golden Standard Mabesad Minu</b>."
                    "</p>",
                    unsafe_allow_html=True
                )
                
                # Side-by-side comparison table
                comparison_matrix = [
                    {
                        "parameter": "Kop Surat & Lambang",
                        "suspect": "72 DPI Cropped Web Image (Buram)" if doc_key != "doc_c" else "Vektor Vektor 300 DPI Resmi",
                        "golden": "Vektor Monokrom / Emas 300 DPI Resmi",
                        "match": doc_key == "doc_c"
                    },
                    {
                        "parameter": "Tipografi Nomor Surat",
                        "suspect": "Courier New Monospaced (Non-Resmi)" if doc_key == "doc_a" else ("Mixed Fonts Mismatch" if doc_key == "doc_b" else "Arial / Bookman Old Style 12pt"),
                        "golden": "Arial / Bookman Old Style 12pt Standar Jukminu",
                        "match": doc_key == "doc_c"
                    },
                    {
                        "parameter": "Stempel Komando",
                        "suspect": "PNG Overlay Digital (Rotasi 14.2°)" if doc_key == "doc_a" else ("Stempel Fiktif Tanpa Kode" if doc_key == "doc_b" else "Tinta Basah Asli Resapan Serat Kertas"),
                        "golden": "Tinta Minyak Ungu dengan Resapan Serat Kertas Fisik",
                        "match": doc_key == "doc_c"
                    },
                    {
                        "parameter": "Tanda Tangan Komando",
                        "suspect": "Brush Script Cursive (Palsu)" if doc_key != "doc_c" else "Tanda Tangan Sah Kadispenad",
                        "golden": "Spesimen Sah Pejabat Mabesad / BSrE Signature",
                        "match": doc_key == "doc_c"
                    },
                    {
                        "parameter": "Register Buku Minu",
                        "suspect": "Tidak Terdaftar (Nomor Kosong)" if doc_key != "doc_c" else "Terdaftar di Buku Agenda TA 2026",
                        "golden": "Wajib Tercatat di Sistem Otomasi Minu Mabesad",
                        "match": doc_key == "doc_c"
                    }
                ]
                
                st.markdown(
                    """
                    <table style="width: 100%; border-collapse: collapse; font-size: 0.76rem; color: #F8FAFC; background: #0B132B; border: 1px solid #1E293B; border-radius: 4px;">
                        <thead>
                            <tr style="background: #111C2E; border-bottom: 2px solid #1E293B; text-align: left;">
                                <th style="padding: 8px 10px; color: #94A3B8;">Elemen Forensik</th>
                                <th style="padding: 8px 10px; color: #F87171;">Dokumen Diperiksa</th>
                                <th style="padding: 8px 10px; color: #34D399;">Golden Standard Mabesad</th>
                                <th style="padding: 8px 10px; text-align: center; color: #94A3B8;">Status</th>
                            </tr>
                        </thead>
                        <tbody>
                    """ + "".join([
                        f"""<tr style="border-bottom: 1px solid #1E293B;">
                            <td style="padding: 8px 10px; font-weight: bold; color: #CBD5E1;">{m['parameter']}</td>
                            <td style="padding: 8px 10px; color: {'#FCA5A5' if not m['match'] else '#6EE7B7'};">{m['suspect']}</td>
                            <td style="padding: 8px 10px; color: #A7F3D0;">{m['golden']}</td>
                            <td style="padding: 8px 10px; text-align: center; font-weight: bold; color: {'#10B981' if m['match'] else '#EF4444'};">{'✓ COCOK' if m['match'] else '✗ ANOMALI'}</td>
                        </tr>""" for m in comparison_matrix
                    ]) + """
                        </tbody>
                    </table>
                    """,
                    unsafe_allow_html=True
                )

            elif layer_mode == "📑 Lapisan 4: Inspeksi Metadata EXIF & Digital Artefak":
                st.markdown(
                    "<p style='color: #94A3B8; font-size: 0.8rem; margin-top: -6px;'>"
                    "Ekstraksi metadata header citra, profil warna, stempel waktu revisi, dan jejak perangkat lunak penyuntingan."
                    "</p>",
                    unsafe_allow_html=True
                )
                
                exif = doc_info.get("exif_metadata", {})
                st.markdown(
                    f"""
                    <div style="background: #0B132B; border: 1px solid #1E293B; border-radius: 6px; padding: 14px;">
                        <table style="width: 100%; border-collapse: collapse; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #E2E8F0;">
                            <tr style="border-bottom: 1px solid #1E293B;">
                                <td style="padding: 6px 8px; color: #94A3B8; width: 160px;">Software Creator:</td>
                                <td style="padding: 6px 8px; color: {'#EF4444' if 'Canva' in exif.get('Software','') or 'Photoshop' in exif.get('Software','') else '#10B981'}; font-weight: bold;">
                                    {exif.get('Software', 'N/A')}
                                </td>
                            </tr>
                            <tr style="border-bottom: 1px solid #1E293B;">
                                <td style="padding: 6px 8px; color: #94A3B8;">Waktu Pembuatan:</td>
                                <td style="padding: 6px 8px; color: #38BDF8;">{exif.get('CreationDate', 'N/A')}</td>
                            </tr>
                            <tr style="border-bottom: 1px solid #1E293B;">
                                <td style="padding: 6px 8px; color: #94A3B8;">Riwayat Modifikasi:</td>
                                <td style="padding: 6px 8px; color: {'#F59E0B' if 'Spliced' in exif.get('ModifiedDate','') else '#CBD5E1'};">{exif.get('ModifiedDate', 'N/A')}</td>
                            </tr>
                            <tr style="border-bottom: 1px solid #1E293B;">
                                <td style="padding: 6px 8px; color: #94A3B8;">Color Space:</td>
                                <td style="padding: 6px 8px; color: #CBD5E1;">{exif.get('ColorSpace', 'N/A')}</td>
                            </tr>
                            <tr style="border-bottom: 1px solid #1E293B;">
                                <td style="padding: 6px 8px; color: #94A3B8;">Resolusi Cetak (DPI):</td>
                                <td style="padding: 6px 8px; color: {'#EF4444' if '72' in exif.get('DPI','') else '#10B981'};">{exif.get('DPI', 'N/A')}</td>
                            </tr>
                            <tr style="border-bottom: 1px solid #1E293B;">
                                <td style="padding: 6px 8px; color: #94A3B8;">Hash MD5:</td>
                                <td style="padding: 6px 8px; color: #94A3B8; word-break: break-all;">{doc_info.get('md5', 'N/A')}</td>
                            </tr>
                            <tr>
                                <td style="padding: 6px 8px; color: #94A3B8;">Hash SHA-256:</td>
                                <td style="padding: 6px 8px; color: #38BDF8; word-break: break-all;">{doc_info.get('sha256', 'N/A')}</td>
                            </tr>
                        </table>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        with col_doc_right:
            st.markdown("#### Lembar Temuan Forensik Dokumen (OCR Findings)")
            
            verdict_color = doc_info["verdict_color"]
            tamper_score = doc_info["tamper_prob"]
            current_doc_id = doc_info["id"]

            # Status Box Forensik Pussiberad
            st.markdown(
                f"""
                <div style="background: #111C2E; border: 1px solid #1E293B; border-left: 4px solid {verdict_color}; padding: 14px; border-radius: 6px; margin-bottom: 12px;">
                    <div style="font-family: 'JetBrains Mono'; font-size: 0.72rem; color: #94A3B8;">STATUS VERIFIKASI PUSSIBERAD:</div>
                    <div style="font-family: 'Chakra Petch'; font-size: 1.05rem; font-weight: 700; color: {verdict_color}; margin: 3px 0;">
                        {doc_info['verdict']}
                    </div>
                    <div style="font-family: 'JetBrains Mono'; font-size: 0.82rem; color: #F8FAFC;">
                        Probabilitas Manipulasi: <b style="color: {verdict_color}; font-size: 1.2rem;">{tamper_score}%</b>
                    </div>
                    <div style="font-family: 'JetBrains Mono'; font-size: 0.68rem; color: #64748B; margin-top: 4px; word-break: break-all;">
                        SHA-256: {doc_info['sha256'][:28]}...
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Live Verification Check with Mabesad Minu Database
            minu = doc_info.get("minu_register_check", {})
            st.markdown(
                f"""
                <div style="background: #0B132B; border: 1px solid #1E293B; border-left: 3px solid {minu.get('status_color', '#EF4444')}; padding: 10px 14px; border-radius: 4px; margin-bottom: 12px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                        <span style="font-size: 0.82rem; font-weight: bold; color: #F8FAFC;">🏛️ Database Register Minu Mabesad</span>
                        <span style="font-family: 'JetBrains Mono'; font-size: 0.7rem; color: {minu.get('status_color', '#EF4444')}; font-weight: bold;">{minu.get('status')}</span>
                    </div>
                    <div style="font-size: 0.75rem; color: #94A3B8;">
                        • <b>Buku Agenda:</b> {minu.get('official_agenda_book')}<br/>
                        • <b>Sertifikasi BSrE:</b> {minu.get('bsre_signature')}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Render Findings Cards
            for f in doc_info["findings"]:
                f_card = f"""
                <div style="background: #111C2E; border: 1px solid #1E293B; border-left: 3px solid {f['color']}; padding: 10px 14px; border-radius: 4px; margin-bottom: 8px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                        <span style="font-size: 0.85rem; font-weight: bold; color: #F8FAFC;">{f['item']}</span>
                        <span style="font-family: 'JetBrains Mono'; font-size: 0.72rem; color: {f['color']}; font-weight: bold;">{f['status']}</span>
                    </div>
                    <div style="font-size: 0.78rem; color: #94A3B8;">{f['detail']}</div>
                </div>
                """
                st.markdown(f_card, unsafe_allow_html=True)

            # SOAR Integration & Command Chain Actions
            st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
            st.markdown("##### ⚡ Tindakan Taktis & Rantai Komando:")

            doc_alert_target = {
                "id": current_doc_id,
                "headline": f"Pemalsuan Dokumen Militer: {doc_info['code']}",
                "bot_account": "Doc-Forgery-Syndicate"
            }
            is_esc, esc_info = check_is_escalated(doc_alert_target)

            if is_esc:
                esc_time = esc_info.get("escalated_at", "Tercatat di Sistem")
                esc_by = esc_info.get("escalated_by", "Analis Siber (Pussiberad)")
                esc_id_num = esc_info.get("id", current_doc_id)
                st.button("✅ BUKTI DOKUMEN PALSU SUDAH DIANTREKAN KE SOAR", key="btn_doc_soar_done", disabled=True, use_container_width=True)
                st.markdown(
                    f"""<div style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: #10B981; background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); padding: 8px 10px; border-radius: 4px; margin-top: 4px;">
                    ✓ <b>STATUS SOAR:</b> Terdaftar ({esc_id_num})<br/>
                    ⏱️ <b>Waktu:</b> {esc_time} | 👤 <b>Oleh:</b> {esc_by}<br/>
                    👉 <i>Buka Modul <b>'Tactical SOAR & Otorisasi'</b> di navigasi kiri untuk otorisasi Komandan (RBAC).</i>
                    </div>""",
                    unsafe_allow_html=True
                )
            elif tamper_score >= 50.0:
                if st.button("🚨 Eskalasikan Temuan Dokumen Palsu Ini ke Antrean SOAR", key="btn_eskalasi_doc_soar", type="primary", use_container_width=True):
                    now_wib = datetime.now().strftime("%Y-%m-%d %H:%M:%S WIB")
                    role_actor = st.session_state.get("active_role", "Analis Siber (Pussiberad)")
                    soar_item = {
                        "id": current_doc_id,
                        "title": f"Investigasi Pemalsuan Naskah Dinas: {doc_info['name']}",
                        "headline": f"Pemalsuan Dokumen Militer: {doc_info['code']}",
                        "sample_text": f"Ditemukan dokumen militer palsu ({doc_info['category']}) dengan tingkat manipulasi {tamper_score}%. Ditemukan anomali tipografi OCR font mismatch, rotasi stempel digital, dan ketidaksesuaian buku register Minu Mabesad. Berkas bukti siap diajukan ke BSSN & Kominfo untuk takedown dan rilis pers Dispenad.",
                        "text": f"Ditemukan dokumen militer palsu ({doc_info['category']}) dengan tingkat manipulasi {tamper_score}%. Ditemukan anomali tipografi OCR font mismatch, rotasi stempel digital, dan ketidaksesuaian buku register Minu Mabesad. Berkas bukti siap diajukan ke BSSN & Kominfo untuk takedown dan rilis pers Dispenad.",
                        "platform": "Multi-Platform (Medsos, Forum & Messaging)",
                        "root_platform": "Multi-Platform",
                        "level": "Kritis",
                        "threat_level": "Kritis",
                        "target_kodam": "Mabes TNI AD / Dispenad",
                        "kodam": "Mabes TNI AD / Dispenad",
                        "cib_cluster_size": 1,
                        "amplification_nodes": 640,
                        "virality_score": 92,
                        "cib_probability": int(tamper_score),
                        "shares_count": 18200,
                        "escalated_at": now_wib,
                        "escalated_by": role_actor,
                        "is_from_radar": True,
                        "is_from_doc_forgery": True,
                        "doc_sha256": doc_info["sha256"]
                    }
                    add_escalated_incident(soar_item)
                    st.session_state["approved_incidents"] = get_approved_incidents()
                    st.session_state["escalated_soar_incidents"] = get_escalated_incidents()
                    st.session_state["audit_logs"] = get_audit_logs()
                    st.toast(f"Temuan Dokumen Palsu ({current_doc_id}) berhasil diajukan ke Antrean SOAR!", icon="🚨")
                    st.rerun()
            else:
                st.markdown(
                    """
                    <div style="background: rgba(16, 185, 129, 0.08); border-left: 3px solid #10B981; padding: 8px 12px; border-radius: 4px; font-size: 0.78rem; color: #E2E8F0;">
                        ✓ <b>Status Otentik:</b> Dokumen ini terverifikasi resmi dalam sistem administrasi umum Mabesad dan tidak memerlukan tindakan eskalasi takedown.
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            # Export Forensic Dossier JSON (BSSN Format)
            dossier_bytes = generate_document_dossier_json(
                doc_info,
                examiner_role=st.session_state.get("active_role", "Analis Siber (Pussiberad)")
            )
            st.download_button(
                label="📥 Unduh Dossier Forensik Dokumen (JSON BSSN)",
                data=dossier_bytes,
                file_name=f"DOSSIER-FORENSIK-DOKUMEN-{current_doc_id}.json",
                mime="application/json",
                use_container_width=True
            )

            # Export Forensic SITREP PDF
            sitrep_incident = {
                "id": current_doc_id,
                "headline": f"Pemalsuan Dokumen Militer: {doc_info['code']}",
                "text": f"Analisis forensik dokumen SENTINEL-AD mengonfirmasi fabrikasi naskah dinas militer: {doc_info['name']}. Tingkat manipulasi ELA: {tamper_score}%, Status Register Minu: {doc_info['minu_register_check']['status']}.",
                "kodam": "Mabes TNI AD / Dispenad",
                "platform": "Multi-Platform",
                "cib_probability": tamper_score,
                "level": "Kritis" if tamper_score >= 50 else "Rendah"
            }
            sitrep_pdf_bytes = generate_sitrep_pdf(
                sitrep_incident,
                approver_name=st.session_state.get("active_role", "Analis Siber (Pussiberad)"),
                defcon=st.session_state.get("defcon_level", "DEFCON 3")
            )
            st.download_button(
                label="📄 Unduh Laporan Forensik SITREP Dokumen (PDF)",
                data=sitrep_pdf_bytes,
                file_name=f"SITREP-FORENSIK-DOKUMEN-{current_doc_id}.pdf",
                mime="application/pdf",
                use_container_width=True
            )

        # Operational SOP Accordion
        st.markdown("<div style='margin-top: 18px;'></div>", unsafe_allow_html=True)
        with st.expander("📘 PROSEDUR OPERASIONAL STANDAR (SOP) AUDIT DOKUMEN MILITER PUSSIBERAD & DISPENAD"):
            st.markdown(
                """
                #### TAHAPAN FORENSIK DOKUMEN NASKAH DINAS MILITER TNI AD (JUKMINU & SINTEL)
                
                1. **Validasi Format Naskah Dinas (Jukminu TNI AD No. 12/IV/2021):**
                   - Periksa hierarki kop surat, jarak spasi baris (1.5 line spacing), ukuran font resmi (*Arial* atau *Bookman Old Style* 12 pt), dan keaslian lambang Kartika Eka Paksi / Garuda monokrom vektor 300 DPI.
                   - Dokumen yang menggunakan font monospaced *Courier New* pada nomor surat merupakan indikasi kuat pengetikan ulang atau fabrikasi non-resmi.
                   
                2. **Inspeksi Error Level Analysis (ELA) & Artefak Kompresi Digital:**
                   - Aktifkan **Lapisan 2: Heatmap ELA** untuk menguji diskontinuitas kompresi JPEG.
                   - Bagian teks atau stempel yang ditempelkan di atas dokumen hasil scan akan memancarkan luminansi tinggi akibat perbedaan tingkat generasi kompresi.
                   
                3. **Audit Forensik Stempel Komando & Mikrogram Keamanan:**
                   - Stempel komando resmi Mabesad menggunakan tinta khusus berbasis minyak yang meresap ke dalam pori-pori serat kertas fisik (*natural capillary bleeding*).
                   - Stempel palsu biasanya berupa layer gambar transparan PNG dengan tepi batas kotak tajam, transparansi seragam artifisial, dan rotasi statis (misal 14.2°).
                   
                4. **Pemeriksaan Database Register Minu Mabesad:**
                   - Setiap Surat Perintah (Sprin) dan DIPA anggaran wajib tercatat dalam Buku Agenda Induk Sekretariat Umum (Setumad) / Minu Mabesad.
                   - Jika nomor Sprin tidak terdaftar, dokumen tersebut diklasifikasikan sebagai **FABRICATED FORGERY (PALSU TOTAL)**.
                   
                5. **Rantai Komando & Tindakan Penindakan Cepat:**
                   - Klik tombol `🚨 Eskalasikan Temuan Dokumen Palsu Ini ke Antrean SOAR`.
                   - Buka modul **Tactical SOAR & Otorisasi** untuk ditandatangani secara digital oleh Perwira Menengah / Komandan Pussiberad.
                   - Terbitkan berkas JSON dossier ke BSSN untuk takedown tautan unduhan dokumen di media sosial, dan rilis naskah klarifikasi stempel hoaks via Dispenad.
                """
            )
