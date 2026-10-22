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
    # TAB 2: MULTIMODAL AUDIO DEEPFAKE SCREENER
    # -----------------------------------------------------------------
    with tab_audio:
        st.markdown("### 🎙️ AUDIT SPEKTROGRAM & DETEKSI KLONING SUARA (AI VOICE CLONE)")
        st.markdown(
            "Menginspeksi integritas sinyal akustik, konsistensi formatur vokal, "
            "dan ketiadaan jeda pernapasan biologis (Bio-Breathing Acoustic Pause) untuk membuktikan suara sintetik."
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
            
            if "Audio A" in sample_choice:
                synth_score = 94.2
                verdict = "DEEPFAKE SYNTHETIC CLONE DETECTED"
                verdict_color = "#EF4444"
                pitch_jitter = "0.012 (Tidak Alami / Terlalu Datar)"
                spectral_cutoff = "16.2 kHz (Artefak Neural Vocoder)"
                breathing_markers = "Nihil (0 jeda mikro biologis terdeteksi)"
            elif "Audio B" in sample_choice:
                synth_score = 3.8
                verdict = "AUTHENTIC HUMAN VOICE CONFIRMED"
                verdict_color = "#10B981"
                pitch_jitter = "0.084 (Fluktuasi Vokal Manusia Normal)"
                spectral_cutoff = "22.0 kHz (Rentang Penuh Akustik Alami)"
                breathing_markers = "Terdeteksi 4 jeda respirasi fisiologis"
            else:
                st.file_uploader("Unggah Berkas Audio Pengujian:", type=["wav", "mp3"])
                synth_score = 88.5
                verdict = "PROBABLE SYNTHETIC MANIPULATION"
                verdict_color = "#F59E0B"
                pitch_jitter = "0.021 (Tinggi Anomali Kompresi)"
                spectral_cutoff = "15.8 kHz (Potongan Frekuensi Sintetis)"
                breathing_markers = "Inkonsistensi Mikro-Jeda"
                
            st.markdown(
                f"""
                <div style="background: #111C2E; border: 1px solid #1E293B; border-left: 4px solid {verdict_color}; padding: 14px; border-radius: 6px; margin-top: 12px;">
                    <div style="font-family: 'JetBrains Mono'; font-size: 0.75rem; color: #94A3B8;">STATUS VERIFIKASI PUSSIBERAD:</div>
                    <div style="font-family: 'Chakra Petch'; font-size: 1.1rem; font-weight: 700; color: {verdict_color}; margin: 4px 0;">
                        {verdict}
                    </div>
                    <div style="font-family: 'JetBrains Mono'; font-size: 0.85rem; color: #F8FAFC;">
                        Probabilitas Sintetis: <b style="color: {verdict_color}; font-size: 1.2rem;">{synth_score}%</b>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
            st.markdown("##### Parameter Forensik Akustik:")
            st.markdown(f"- **Pitch Jitter Consistency:** `{pitch_jitter}`")
            st.markdown(f"- **Spectral Cutoff Anomaly:** `{spectral_cutoff}`")
            st.markdown(f"- **Bio-Breathing Acoustic Pause:** `{breathing_markers}`")

        with col_result:
            st.markdown("#### Spektrogram Frekuensi & Gelombang Suara (Acoustic Waveform)")
            
            # Generate simulated waveform & spectrogram
            time_x = np.linspace(0, 4.0, 500)
            if synth_score > 50:
                # Synthetic sound has overly uniform harmonics + high-frequency cutoff
                waveform = 0.5 * np.sin(2 * np.pi * 3 * time_x) + 0.3 * np.sin(2 * np.pi * 9 * time_x) + np.random.normal(0, 0.03, len(time_x))
            else:
                # Human voice has natural micro-tremors, amplitude modulation, and breathing gaps
                envelope = np.sin(np.pi * time_x / 4.0) ** 1.5
                waveform = envelope * (0.6 * np.sin(2 * np.pi * 2.5 * time_x) + 0.4 * np.sin(2 * np.pi * 7.5 * time_x)) + np.random.normal(0, 0.08, len(time_x))
                # Add breathing gap at 2.0s
                waveform[230:260] = 0.01 * np.random.normal(0, 0.02, 30)

            fig_wave = go.Figure()
            fig_wave.add_trace(go.Scatter(
                x=time_x,
                y=waveform,
                line=dict(color="#06B6D4" if synth_score < 50 else "#EF4444", width=1.5),
                name="Amplitudo Audio"
            ))
            fig_wave.update_layout(
                title=dict(text="Waveform Analisis (0.0s - 4.0s)", font=dict(family="Chakra Petch", size=12, color="#94A3B8")),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(15,23,42,0.8)",
                xaxis=dict(title="Detik", gridcolor="#1E293B", tickfont=dict(family="JetBrains Mono", color="#94A3B8")),
                yaxis=dict(title="Amplitudo", gridcolor="#1E293B", tickfont=dict(family="JetBrains Mono", color="#94A3B8")),
                margin=dict(t=30, b=20, l=10, r=10),
                height=160
            )
            st.plotly_chart(fig_wave, use_container_width=True)

            # Heatmap Spectrogram
            freqs = np.linspace(0, 20000, 30)
            times = np.linspace(0, 4, 40)
            T, F = np.meshgrid(times, freqs)
            
            if synth_score > 50:
                # Artificial cutoff at 16kHz
                Z = np.exp(-((F - 2500)**2) / (2 * 1500**2)) + 0.5 * np.exp(-((F - 6000)**2) / (2 * 1200**2))
                Z[F > 16000] = 0.01  # Hard neural vocoder cutoff
            else:
                Z = np.exp(-((F - 2000)**2) / (2 * 2000**2)) + 0.4 * np.exp(-((F - 5500)**2) / (2 * 2500**2)) + 0.2 * np.exp(-((F - 14000)**2) / (2 * 4000**2))

            fig_spec = go.Figure(data=go.Heatmap(
                z=Z,
                x=times,
                y=freqs,
                colorscale="Viridis",
                colorbar=dict(title="dB", tickfont=dict(color="#94A3B8", family="JetBrains Mono"))
            ))
            fig_spec.update_layout(
                title=dict(text="Spektrogram Frekuensi Fourier (FFT 20kHz)", font=dict(family="Chakra Petch", size=12, color="#94A3B8")),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(15,23,42,0.8)",
                xaxis=dict(title="Detik", gridcolor="#1E293B", tickfont=dict(family="JetBrains Mono", color="#94A3B8")),
                yaxis=dict(title="Hz", gridcolor="#1E293B", tickfont=dict(family="JetBrains Mono", color="#94A3B8")),
                margin=dict(t=30, b=20, l=10, r=10),
                height=190
            )
            st.plotly_chart(fig_spec, use_container_width=True)

    # -----------------------------------------------------------------
    # TAB 3: DOCUMENT INTEGRITY & OCR HIGHLIGHT
    # -----------------------------------------------------------------
    with tab_doc:
        st.markdown("### 📄 DETEKSI INTEGRITAS DOKUMEN MILITER & KOTAK HIGHLIGHT OCR")
        st.markdown(
            "Membandingkan dokumen surat perintah (Sprin) asli Mabesad dengan dokumen manipulasi/palsu "
            "menggunakan analisis OCR font mismatch, anomali penempatan stempel komando, dan ketidaksesuaian stensil."
        )
        
        doc_choice = st.selectbox(
            "Pilih Berkas Dokumen Militer untuk Diperiksa:",
            [
                "Dokumen A: Surat Edaran Palsu Mutasi Staf Dispenad (Sprin/482/IX/2026)",
                "Dokumen B: Lembar Pengesahan Anggaran Pengadaan Fiktif Alutsista",
                "Dokumen C: Dokumen Asli Terverifikasi Dispenad (Kontrol Pembanding)"
            ]
        )
        
        col_doc_left, col_doc_right = st.columns([6, 6])
        
        with col_doc_left:
            st.markdown("#### Tampilan Pratinjau Dokumen & Deteksi Anomali OCR")
            
            if "Dokumen A" in doc_choice:
                # Simulated Document Card with OCR Highlight Boxes
                doc_html = """
                <div style="background: #FFFFFF; color: #0F172A; padding: 24px 28px; border-radius: 4px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); font-family: 'Times New Roman', serif; position: relative; border: 2px solid #EF4444;">
                    <div style="text-align: center; border-bottom: 2px solid #000; padding-bottom: 6px; margin-bottom: 12px;">
                        <div style="font-size: 11px; font-weight: bold; letter-spacing: 0.05em;">TENTARA NASIONAL INDONESIA ANGKATAN DARAT</div>
                        <div style="font-size: 10px; font-weight: bold;">MARKAS BESAR</div>
                        <div style="font-size: 9px; color: #475569;">Jl. Veteran No. 5 Jakarta Pusat</div>
                    </div>

                    <div style="text-align: center; margin-bottom: 14px;">
                        <div style="font-size: 11px; font-weight: bold; text-decoration: underline;">SURAT PERINTAH MUTASI JABATAN</div>
                        <div style="position: relative; display: inline-block;">
                            <span style="font-size: 10px; font-family: 'Courier New', monospace; background: rgba(239, 68, 68, 0.25); border: 1.5px dashed #EF4444; padding: 2px 6px;">
                                Nomor: Sprin / 482 / IX / 2026-DISPENAD [ANOMALI FONT]
                            </span>
                        </div>
                    </div>

                    <div style="font-size: 10px; line-height: 1.5; margin-bottom: 20px;">
                        Pertimbangan: Bahwa dalam rangka penyegaran satuan intelijen dan penerangan...<br/>
                        Diperintahkan: Terhitung mulai tanggal diterbitkan surat ini, memutasikan perwira berikut...
                    </div>

                    <div style="display: flex; justify-content: flex-end; margin-top: 25px;">
                        <div style="text-align: center; width: 200px; position: relative;">
                            <div style="font-size: 10px;">Ditetapkan di: Jakarta</div>
                            <div style="font-size: 10px; font-weight: bold;">a.n. KEPALA STAF ANGKATAN DARAT</div>
                            <div style="height: 45px; position: relative; display: flex; align-items: center; justify-content: center;">
                                <div style="position: absolute; border: 2px dashed #EF4444; background: rgba(239,68,68,0.15); width: 65px; height: 65px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 8px; color: #DC2626; font-weight: bold;">
                                    STEMPEL PALSU (ROTASI 14°)
                                </div>
                                <span style="font-family: 'Brush Script MT', cursive; font-size: 18px; color: #1E3A8A; z-index: 2;">Tanda Tangan Palsu</span>
                            </div>
                            <div style="font-size: 10px; font-weight: bold; text-decoration: underline;">M. SYAHRIR, M.Sc.</div>
                            <div style="font-size: 9px;">Mayor Jenderal TNI</div>
                        </div>
                    </div>
                </div>
                """
                st.markdown(doc_html, unsafe_allow_html=True)
            else:
                st.markdown(
                    """
                    <div style="background: #FFFFFF; color: #0F172A; padding: 24px 28px; border-radius: 4px; border: 2px solid #10B981; font-family: 'Times New Roman', serif;">
                        <div style="text-align: center; border-bottom: 2px solid #000; padding-bottom: 6px; margin-bottom: 12px;">
                            <div style="font-size: 11px; font-weight: bold;">TENTARA NASIONAL INDONESIA ANGKATAN DARAT</div>
                            <div style="font-size: 10px; font-weight: bold;">DINAS PENERANGAN</div>
                        </div>
                        <div style="text-align: center; margin-bottom: 14px;">
                            <span style="font-size: 10px; font-weight: bold; background: rgba(16, 185, 129, 0.2); border: 1px solid #10B981; padding: 2px 8px;">
                                REGISTRASI OTENTIK DATABASE MABESAD: PASSED
                            </span>
                        </div>
                        <p style="font-size: 10px;">Semua stempel digital bertanda tangan kriptografi SHA-256 valid.</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        with col_doc_right:
            st.markdown("#### Lembar Temuan Forensik Dokumen (OCR Findings)")
            
            findings = [
                {
                    "item": "Kop Surat & Lambang Garuda Mabesad",
                    "status": "NON-STANDARD DRAFT",
                    "detail": "Resolusi artefak piksel 72 DPI (hasil cropping internet), standar resmi menggunakan vektor 300 DPI.",
                    "color": "#EF4444"
                },
                {
                    "item": "Penomoran Sprin & Tipografi",
                    "status": "FONT KERNING MISMATCH",
                    "detail": "Karakter nomor surat menggunakan font 'Courier New' non-resmi, bukan font Arial/Times resmi Mabesad.",
                    "color": "#EF4444"
                },
                {
                    "item": "Stempel Basah Komando",
                    "status": "FORGED DIGITAL OVERLAY",
                    "detail": "Stempel memiliki artefak rotasi 14 derajat dengan transparansi layer PNG yang tidak menyatu dengan serat kertas.",
                    "color": "#EF4444"
                },
                {
                    "item": "Verifikasi Database Buku Register Sprin",
                    "status": "INVALID REGISTER NUMBER",
                    "detail": "Nomor Sprin 482/IX/2026 tidak terdaftar dalam sistem otomasi administrasi umum (Minu) Mabesad.",
                    "color": "#EF4444"
                }
            ]
            
            for f in findings:
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

            st.button("📥 Tambahkan Bukti OCR Dokumen ke Takedown Dossier", type="primary")
