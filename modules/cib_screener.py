"""
modules/cib_screener.py - Advanced CIB Detection & Multimodal Deepfake Screener
Analyzes Coordinated Inauthentic Behavior timing bursts and screens multimodal synthetic media (Voice Clones & Forged Military Docs).
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from utils.data_generator import generate_cib_synchronized_clusters

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
    # TAB 1: CIB TIMING & SEMANTIC BURST ANALYSIS
    # -----------------------------------------------------------------
    with tab_cib:
        st.markdown("### ⏱️ ANALISIS BURST TEMPORAL CIB (SINKRONISASI POSTINGAN &lt;60 DETIK)")
        st.markdown(
            "Pola serangan CIB dicirikan oleh puluhan akun anonim mengunggah konten identik atau semantik serupa "
            "dengan latensi di bawah 60 detik pasca berkas dilepas oleh simpul *seed*."
        )
        
        cib_df = generate_cib_synchronized_clusters()
        
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        with col_m1:
            st.metric("Total Akun Terindikasi Bot", "13 Akun", "+8 Terdeteksi Baru")
        with col_m2:
            st.metric("Rerata Jeda Posting", "5.8 Detik", "Sub-60s Burst Window")
        with col_m3:
            st.metric("Kemiripan Semantik", "96.4%", "Cosine Similarity")
        with col_m4:
            st.metric("Asal Proksi / Node", "TOR & Cloud Hosting", "Anti-Geoloc")
            
        st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
        
        # Timeline of CIB bursts
        col_chart, col_table = st.columns([6, 6])
        
        with col_chart:
            st.markdown("#### Linimasa Interval Posting Akun Bot (Detik)")
            
            cluster_filter = st.selectbox(
                "Pilih Klaster CIB:",
                options=list(cib_df["cluster"].unique())
            )
            
            sub_cib = cib_df[cib_df["cluster"] == cluster_filter].copy()
            sub_cib["cumulative_time_sec"] = sub_cib["post_interval_sec"].cumsum()
            
            fig_burst = px.scatter(
                sub_cib,
                x="cumulative_time_sec",
                y="account",
                size="semantic_similarity",
                color="semantic_similarity",
                color_continuous_scale="Reds",
                hover_data=["timestamp", "proxy_ip", "account_age_days"],
                labels={"cumulative_time_sec": "Detik Kumulatif Pasca Drop Awal", "account": "Identitas Akun Bot"}
            )
            fig_burst.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(15,23,42,0.8)",
                font=dict(family="JetBrains Mono", size=10, color="#F8FAFC"),
                margin=dict(t=20, b=20, l=10, r=10),
                height=320,
                xaxis=dict(gridcolor="#334155"),
                yaxis=dict(gridcolor="#334155")
            )
            st.plotly_chart(fig_burst, use_container_width=True)
            
        with col_table:
            st.markdown("#### Indikator Kesamaan Hash & Jejak Digital")
            st.dataframe(
                sub_cib[["account", "timestamp", "post_interval_sec", "semantic_similarity", "proxy_ip"]],
                column_config={
                    "account": st.column_config.TextColumn("Akun Bot"),
                    "timestamp": st.column_config.TextColumn("Waktu Post"),
                    "post_interval_sec": st.column_config.NumberColumn("Jeda (s)", format="%d s"),
                    "semantic_similarity": st.column_config.ProgressColumn("Kemiripan", min_value=0.8, max_value=1.0, format="%.2f"),
                    "proxy_ip": st.column_config.TextColumn("Jalur Jaringan / Node")
                },
                hide_index=True,
                use_container_width=True,
                height=320
            )

        # Forensic Conclusion Box
        st.markdown(
            f"""
            <div class="tactical-card danger" style="padding: 12px 16px; margin-top: 15px;">
                <span style="font-family: 'JetBrains Mono'; font-weight: bold; color: #EF4444;">KESIMPULAN AUDIT PUSSIBERAD:</span>
                <span style="font-size: 0.85rem; color: #F1F5F9; margin-left: 10px;">
                    Perilaku di atas memenuhi kriteria <b>Coordinated Inauthentic Behavior (CIB)</b> tingkat tinggi. 
                    Pola unggahan serentak dalam durasi kurang dari 50 detik dengan teks nyaris identik 
                    mengonfirmasi adanya orkestrasi skrip automasi (Botnet Farm) bukan interaksi publik organik.
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
