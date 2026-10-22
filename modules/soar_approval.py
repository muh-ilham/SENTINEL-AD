"""
modules/soar_approval.py - Tactical 1-Click SOAR, RBAC Approvals & Audit Trail
Handles automated defense response packages, RBAC commander approvals, and cryptographic audit logging.
"""

import streamlit as st
import pandas as pd
import json
from datetime import datetime
from utils.pdf_exporter import generate_sitrep_pdf, export_takedown_dossier_json
from utils.data_generator import PRIMARY_INCIDENTS
from utils.soar_storage import (
    get_escalated_incidents,
    get_approved_incidents,
    mark_incident_approved,
    get_audit_logs
)

def init_audit_logs():
    """Initializes session state audit trail and approvals from persistent storage."""
    if "audit_logs" not in st.session_state:
        st.session_state["audit_logs"] = get_audit_logs()
        
    if "approved_incidents" not in st.session_state:
        st.session_state["approved_incidents"] = get_approved_incidents()
        
    if "escalated_soar_incidents" not in st.session_state:
        st.session_state["escalated_soar_incidents"] = get_escalated_incidents()

def get_all_soar_incidents():
    """Returns combined list of dynamically escalated incidents from C2 Radar + baseline incidents."""
    escalated_dict = get_escalated_incidents()
    escalated_items = list(escalated_dict.values())
    
    # Combined with PRIMARY_INCIDENTS avoiding duplicate IDs
    existing_ids = {item["id"] for item in escalated_items}
    combined = escalated_items + [inc for inc in PRIMARY_INCIDENTS if inc["id"] not in existing_ids]
    return combined

def render_soar_approval(current_role="Analis Siber (Pussiberad)"):
    """Renders the Tactical SOAR & RBAC Approval Command Center."""
    init_audit_logs()
    
    st.markdown("## ⚡ TACTICAL SOAR & PENGAMBILAN KEPUTUSAN C2")
    st.markdown(
        "<p style='color: #94A3B8; font-size: 0.95rem; margin-top: -10px;'>"
        "Security Orchestration, Automation & Response (SOAR): Eksekusi Paket Aksi Pertahanan, Persetujuan Komando (RBAC), & Jejak Audit Kriptografi."
        "</p>",
        unsafe_allow_html=True
    )
    
    tab_soar, tab_rbac, tab_audit = st.tabs([
        "📦 PAKET AKSI PERTAHANAN 1-KLIK (SOAR)",
        "🎖️ ALUR PERSETUJUAN KOMANDAN (RBAC)",
        "📜 LOG JEJAK AUDIT TAKTIS (OPSEC AUDIT TRAIL)"
    ])
    
    # -------------------------------------------------------------
    # TAB 1: 1-CLICK DEFENSE ACTION PACKAGE
    # -------------------------------------------------------------
    with tab_soar:
        st.markdown("### 🚀 GENERATOR PAKET PENANGGULANGAN OPERASI KOGNITIF (1-CLICK SOAR)")
        st.markdown(
            "Mengompilasi berkas intelijen taktis lengkap menjadi format standar inter-agensi: "
            "Dossier Takedown BSSN/Kominfo, Executive SITREP Dokumen Resmi PDF, dan Brief Cek Fakta Media."
        )
        
        all_incidents = get_all_soar_incidents()
        inc_options = {}
        for inc in all_incidents:
            radar_prefix = "📡 [LIVE C2] " if inc.get("is_from_radar") else ""
            inc_options[inc["id"]] = f"{radar_prefix}[{inc.get('level', inc.get('threat_level', 'KRITIS')).upper()}] {inc['title']}"
            
        selected_inc_id = st.selectbox(
            "Pilih Insiden Ancaman untuk Dibuatkan Paket Penanggulangan:",
            options=list(inc_options.keys()),
            format_func=lambda x: inc_options[x]
        )
        
        active_inc = next(item for item in all_incidents if item["id"] == selected_inc_id)
        is_approved = selected_inc_id in st.session_state["approved_incidents"]
        
        col_summary, col_downloads = st.columns([7, 5])
        
        with col_summary:
            status_text = "DISETUJUI OLEH KOMANDAN" if is_approved else "MENUNGGU PERSETUJUAN PERWIRA MENENGAH"
            status_color = "#10B981" if is_approved else "#F59E0B"
            target_kodam_val = active_inc.get('target_kodam', active_inc.get('kodam', 'TNI AD'))
            cib_cluster_val = active_inc.get('cib_cluster_size', active_inc.get('amplification_nodes', 28))
            evidence_val = "Neural Vocoder 16kHz Cutoff / MD5 e99a18c4..." if not active_inc.get('is_from_radar') else f"Tautan Langsung {active_inc.get('platform', 'Medsos')} / Log Telemetri C2 SHA-256"
            
            card_html = f"""<div class="tactical-card" style="border-left: 3px solid {status_color}; padding: 16px; margin-bottom: 15px;">
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
<span style="font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #38BDF8;">REGISTER: SOAR/{active_inc['id']}/TNI-AD</span>
<span style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: {status_color}; font-weight: bold; background: rgba(0,0,0,0.4); padding: 2px 8px; border-radius: 4px; border: 1px solid {status_color};">{status_text}</span>
</div>
<h4 style="margin: 0 0 6px 0; color: #FFFFFF; font-family: 'Chakra Petch', sans-serif;">{active_inc['title']}</h4>
<p style="font-size: 0.82rem; color: #CBD5E1; margin-bottom: 10px; line-height: 1.4;">{active_inc['sample_text']}</p>
<div style="background: #0B1120; padding: 10px; border-radius: 4px; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #94A3B8;">
<div style="margin-bottom: 3px;">• Yurisdiksi: <b style="color: #F8FAFC;">{target_kodam_val}</b></div>
<div style="margin-bottom: 3px;">• Klaster Akun Sasaran Takedown: <b style="color: #EF4444;">{cib_cluster_val} Akun Bot Terverifikasi</b></div>
<div>• Bukti Sintetis / Telemetri: <b style="color: #22D3EE;">{evidence_val}</b></div>
</div>
</div>"""
            st.markdown(card_html, unsafe_allow_html=True)
            
            # Fact-Checking Infographic Brief
            st.markdown("#### 📢 Materi Briefing Komunikasi Publik Dispenad")
            if active_inc.get("is_from_radar"):
                brief_text = f"""
                **Poin Kunci Cek Fakta & Tindak Lanjut Dispenad/Pussiberad:**
                1. **Fakta 1:** Narasi mengenai "{active_inc.get('headline', active_inc['title'])}" terindikasi sebagai disinformasi/hoaks manipulatif.
                2. **Fakta 2:** Analisis laboratorium intelijen siber mencatat probabilitas botnet/CIB sebesar {active_inc.get('cib_probability', 80)}% dengan viralitas {active_inc.get('virality_score', 85)}/100 pada platform {active_inc.get('platform', 'Media')}.
                3. **Fakta 3:** Situasi satuan jajaran teritorial ({active_inc.get('target_kodam', active_inc.get('kodam', 'TNI AD'))}) dalam kondisi aman, solid, dan kondusif.
                4. **Visual Guideline:** Terbitkan rilis infografis berstempel resmi 'DISPENAD KLARIFIKASI' untuk menetralkan isu.
                """
            else:
                brief_text = f"""
                **Poin Kunci Cek Fakta (Talking Points Dispenad):**
                1. **Fakta 1:** Panglima TNI AD tidak pernah mengeluarkan instruksi suara tersebut.
                2. **Fakta 2:** Analisis laboratorium Pussiberad memastikan audio 94.2% diproduksi oleh software AI Voice Synthesizer.
                3. **Fakta 3:** Kondisi teritorial jajaran Kodam terkait saat ini dalam situasi aman, damai, dan solid bersama masyarakat.
                4. **Visual Guideline:** Publikasikan infografis 'Side-by-Side Debunk' mencantumkan watermark resmi DISPENAD.
                """
            st.info(brief_text)

        with col_downloads:
            st.markdown("#### 📥 Unduh Berkas Eksekusi Pertahanan")
            
            # Generate SITREP PDF
            approver_label = "Kolonel Inf. Bambang S. (Danpussiberad)" if is_approved else "Draf Belum Disahkan"
            pdf_bytes = generate_sitrep_pdf(active_inc, approver_name=approver_label)
            
            # Generate JSON Dossier
            json_str = export_takedown_dossier_json(active_inc)
            
            st.download_button(
                label="📄 Unduh Executive SITREP Resmi (PDF Standar Militer)",
                data=pdf_bytes,
                file_name=f"SITREP_{active_inc['id']}_TNI_AD.pdf",
                mime="application/pdf",
                use_container_width=True
            )
            
            st.markdown("<div style='margin-top: 8px;'></div>", unsafe_allow_html=True)
            
            st.download_button(
                label="⚡ Unduh Takedown Dossier (JSON Standar BSSN/Kominfo)",
                data=json_str,
                file_name=f"TAKEDOWN_DOSSIER_{active_inc['id']}_BSSN.json",
                mime="application/json",
                use_container_width=True
            )
            
            st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
            
            st.markdown("#### 🛰️ Interoperabilitas Sistem Mitra:")
            st.markdown(
                """
                <div style="background: #111C2E; border: 1px solid #1E293B; padding: 10px; border-radius: 4px; font-family: 'JetBrains Mono'; font-size: 0.75rem;">
                    <div style="color: #10B981;">● BSSN National CSIRT API: ONLINE</div>
                    <div style="color: #10B981;">● Kominfo AIS Engine: TERKONEKSI</div>
                    <div style="color: #10B981;">● Dittipidsiber Bareskrim: READY</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            if st.button("📡 Kirimkan Dossier Takedown Otomatis ke API BSSN", type="primary", use_container_width=True):
                if not is_approved:
                    st.warning("⚠️ Perhatian: Paket SOAR belum disetujui secara digital oleh Komandan. Hanya paket berstatus 'Approved' yang dapat dikirim otomatis.")
                else:
                    st.success(f"✅ Berhasil ditransmisikan ke BSSN Gateway! Tiket ID: #BSSN-TKD-{active_inc['id']}")
                    st.session_state["audit_logs"].insert(0, {
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S WIB"),
                        "user": current_role,
                        "role": current_role,
                        "action": "TRANSMISI DOSSIER BSSN",
                        "target": active_inc["id"],
                        "status": "TERKIRIM INTER-AGENCY",
                        "hash": "a4c7e190...77b2"
                    })

    # -------------------------------------------------------------
    # TAB 2: RBAC COMMANDER APPROVAL
    # -------------------------------------------------------------
    with tab_rbac:
        st.markdown("### 🎖️ RUKUN OTORISASI BERJENJANG (ROLE-BASED ACCESS CONTROL)")
        st.markdown(
            "Menjaga *Chain of Command* dan akuntabilitas hukum. Hanya peran **Perwira Menengah / Komandan** "
            "yang berhak memberikan otorisasi penindakan dan membubuhkan tanda tangan kriptografis."
        )
        
        # Display Current Active Role
        st.markdown(
            f"""
            <div style="background: #0B1120; border: 1px solid #334155; padding: 12px 18px; border-radius: 6px; margin-bottom: 15px;">
                <span style="font-family: 'JetBrains Mono'; font-size: 0.78rem; color: #94A3B8;">PERAN PENGGUNA SAAT INI:</span>
                <span style="font-family: 'Chakra Petch'; font-size: 1.15rem; font-weight: bold; color: #22D3EE; margin-left: 10px;">
                    {current_role}
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        col_approval_left, col_approval_right = st.columns([7, 5])
        
        with col_approval_left:
            st.markdown("#### Daftar Antrean Permohonan Otorisasi SOAR")
            all_incidents = get_all_soar_incidents()
            
            for inc in all_incidents:
                inc_id = inc["id"]
                already_approved = inc_id in st.session_state["approved_incidents"]
                btn_disabled = already_approved or ("Komandan" not in current_role)
                is_from_radar = inc.get("is_from_radar", False)
                
                with st.container():
                    radar_tag_html = f"<div style='font-family: JetBrains Mono; font-size: 0.68rem; color: #22D3EE; margin-bottom: 4px;'>📡 ESKALASI LANGSUNG DARI RADAR C2 ({inc.get('platform', 'Medsos')}) • {inc.get('escalated_at', 'Baru saja')}</div>" if is_from_radar else ""
                    approval_status_text = "[STATUS: DISETUJUI KOMANDAN]" if already_approved else "[MENUNGGU PERSETUJUAN]"
                    approval_status_color = "#10B981" if already_approved else "#F59E0B"
                    card_border_color = "#10B981" if already_approved else "#EF4444"
                    card_level = inc.get('level', inc.get('threat_level', 'Kritis'))
                    card_kodam = inc.get('target_kodam', inc.get('kodam', 'Mabesad'))
                    
                    card_tab2 = f"""<div style="background: #111C2E; border: 1px solid #1E293B; border-left: 3px solid {card_border_color}; padding: 12px; border-radius: 4px; margin-bottom: 8px;">
{radar_tag_html}
<div style="display: flex; justify-content: space-between; font-family: 'JetBrains Mono', monospace; font-size: 0.72rem;">
<span style="color: #38BDF8;">{inc_id}</span>
<span style="color: {approval_status_color}; font-weight: bold;">{approval_status_text}</span>
</div>
<div style="font-weight: 600; color: #FFFFFF; font-size: 0.88rem; margin: 4px 0;">{inc['title']}</div>
<div style="font-size: 0.78rem; color: #94A3B8;">Tingkat: <b style="color: #EF4444;">{card_level}</b> | Yurisdiksi: {card_kodam}</div>
</div>"""
                    st.markdown(card_tab2, unsafe_allow_html=True)
                    
                    if not already_approved:
                        if "Komandan" in current_role:
                            if st.button(f"✍️ Setujui & Tanda Tangan Digital ({inc_id})", key=f"appr_{inc_id}", type="primary"):
                                mark_incident_approved(inc_id, current_role)
                                st.session_state["approved_incidents"] = get_approved_incidents()
                                st.session_state["audit_logs"] = get_audit_logs()
                                st.success(f"Insiden {inc_id} berhasil disetujui dan ditandatangani secara digital!")
                                st.rerun()
                        else:
                            st.caption(f"🔒 Tombol persetujuan terkunci. Pindah ke peran 'Perwira Menengah / Komandan' di sidebar untuk menandatangani.")
                    else:
                        st.caption("✅ Dokumen telah ditandatangani secara kriptografis SHA-256.")

        with col_approval_right:
            st.markdown("#### Matriks Hak Akses (RBAC Matrix)")
            
            rbac_data = [
                {"Aksi Sistem": "Buat Draf Analisis Ancaman", "Pussiberad": "✅ YA", "Dispenad": "✅ YA", "Komandan": "✅ YA"},
                {"Aksi Sistem": "Uji Wargaming & Personas", "Pussiberad": "✅ YA", "Dispenad": "✅ YA", "Komandan": "✅ YA"},
                {"Aksi Sistem": "Klarifikasi Pers Dispenad", "Pussiberad": "❌ Tinjau", "Dispenad": "✅ Rilis", "Komandan": "✅ Otorisasi"},
                {"Aksi Sistem": "Persetujuan Takedown Eksternal", "Pussiberad": "❌ Draf", "Dispenad": "❌ Tinjau", "Komandan": "✅ MUTLAK"},
                {"Aksi Sistem": "Tanda Tangan Kriptografi", "Pussiberad": "❌ Dilarang", "Dispenad": "❌ Dilarang", "Komandan": "✅ SAH"}
            ]
            
            st.dataframe(
                pd.DataFrame(rbac_data),
                hide_index=True,
                use_container_width=True
            )

    # -------------------------------------------------------------
    # TAB 3: TACTICAL AUDIT TRAIL LOG (OPSEC)
    # -------------------------------------------------------------
    with tab_audit:
        st.markdown("### 📜 LOG JEJAK AUDIT TAKTIS (CRYPTOGRAPHIC AUDIT TRAIL)")
        st.markdown(
            "Pencatatan setiap aktivitas analisis, persetujuan komando, dan transmisi paket penanggulangan secara *tamper-evident* "
            "untuk menjamin kepatuhan hukum militer dan OPSEC (Operational Security)."
        )
        
        audit_records = get_audit_logs()
        audit_df = pd.DataFrame(audit_records)
        
        st.dataframe(
            audit_df,
            column_config={
                "timestamp": st.column_config.TextColumn("Waktu Kejadian", width="medium"),
                "user": st.column_config.TextColumn("Nama Personel", width="medium"),
                "role": st.column_config.TextColumn("Peran Jabatan", width="medium"),
                "action": st.column_config.TextColumn("Aksi Sistem", width="medium"),
                "target": st.column_config.TextColumn("Sasaran / Insiden", width="medium"),
                "status": st.column_config.TextColumn("Status Integritas", width="small"),
                "hash": st.column_config.TextColumn("SHA-256 Signature", width="small")
            },
            hide_index=True,
            use_container_width=True,
            height=340
        )
        
        st.download_button(
            label="📥 Ekspor Log Audit Lengkap (CSV Terenkripsi)",
            data=audit_df.to_csv(index=False),
            file_name="AUDIT_LOG_SENTINEL_AD.csv",
            mime="text/csv"
        )
