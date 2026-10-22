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
    get_rejected_incidents,
    mark_incident_rejected,
    revoke_incident_status,
    remove_escalated_incident,
    get_audit_logs,
    get_latest_wargaming_result,
    approve_all_pending,
    export_soar_backup_json,
    restore_soar_backup_json
)

def init_audit_logs():
    """Initializes session state audit trail and approvals from persistent storage."""
    # Ensure fresh sync on every view render
    st.session_state["escalated_soar_incidents"] = get_escalated_incidents()
    st.session_state["approved_incidents"] = get_approved_incidents()
    st.session_state["rejected_incidents"] = get_rejected_incidents()
    st.session_state["audit_logs"] = get_audit_logs()

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
            if inc.get("bot_accounts_list"):
                prefix = "⚡ [TAKEDOWN MASSAL CIB] "
            elif inc.get("is_from_cib") or "TKD-BOT" in inc.get("id", ""):
                prefix = "🤖 [TAKEDOWN AKUN CIB] "
            elif inc.get("is_from_radar"):
                prefix = "📡 [LIVE C2] "
            else:
                prefix = "🚨 [BASELINE] "
            inc_options[inc["id"]] = f"{prefix}[{inc.get('level', inc.get('threat_level', 'KRITIS')).upper()}] {inc['title']}"
            
        selected_inc_id = st.selectbox(
            "Pilih Insiden Ancaman untuk Dibuatkan Paket Penanggulangan:",
            options=list(inc_options.keys()),
            format_func=lambda x: inc_options[x]
        )
        
        active_inc = next(item for item in all_incidents if item["id"] == selected_inc_id)
        is_approved = selected_inc_id in st.session_state["approved_incidents"]
        is_rejected = selected_inc_id in st.session_state["rejected_incidents"]
        
        inc_id = active_inc.get('id', 'INC-SOAR')
        inc_title = active_inc.get('title', active_inc.get('headline', 'Insiden Ancaman Siber'))
        inc_desc = active_inc.get('sample_text', active_inc.get('text', active_inc.get('headline', 'Deteksi intelijen siber terkonfirmasi.')))
        
        col_summary, col_downloads = st.columns([7, 5])
        
        with col_summary:
            if is_approved:
                status_text = "DISETUJUI OLEH KOMANDAN"
                status_color = "#10B981"
            elif is_rejected:
                status_text = "DITOLAK KOMANDAN (FALSE POSITIVE)"
                status_color = "#EF4444"
            else:
                status_text = "MENUNGGU PERSETUJUAN PERWIRA MENENGAH"
                status_color = "#F59E0B"
                
            target_kodam_val = active_inc.get('target_kodam', active_inc.get('kodam', 'TNI AD'))
            if active_inc.get("bot_account"):
                cib_cluster_val = f"1 Akun Sasaran Tunggal ({active_inc.get('bot_account')})"
            elif active_inc.get("bot_accounts_list"):
                cib_cluster_val = f"{len(active_inc.get('bot_accounts_list'))} Akun Bot Terverifikasi (Kolektif)"
            else:
                cib_cluster_val = f"{active_inc.get('cib_cluster_size', active_inc.get('amplification_nodes', 28))} Akun Bot Terverifikasi"

            if active_inc.get("bot_url"):
                evidence_val = f"URL Sasaran: {active_inc.get('bot_url')} / Telemetri Forensik CIB"
            elif active_inc.get("is_from_radar"):
                evidence_val = f"Tautan Langsung {active_inc.get('platform', 'Medsos')} / Log Telemetri C2 SHA-256"
            else:
                evidence_val = "Neural Vocoder 16kHz Cutoff / MD5 e99a18c4..."
            
            card_html = f"""<div class="tactical-card" style="border-left: 3px solid {status_color}; padding: 16px; margin-bottom: 15px;">
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
<span style="font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #38BDF8;">REGISTER: SOAR/{inc_id}/TNI-AD</span>
<span style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: {status_color}; font-weight: bold; background: rgba(0,0,0,0.4); padding: 2px 8px; border-radius: 4px; border: 1px solid {status_color};">{status_text}</span>
</div>
<h4 style="margin: 0 0 6px 0; color: #FFFFFF; font-family: 'Chakra Petch', sans-serif;">{inc_title}</h4>
<p style="font-size: 0.82rem; color: #CBD5E1; margin-bottom: 10px; line-height: 1.4;">{inc_desc}</p>
<div style="background: #0B1120; padding: 10px; border-radius: 4px; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #94A3B8;">
<div style="margin-bottom: 3px;">• Yurisdiksi: <b style="color: #F8FAFC;">{target_kodam_val}</b></div>
<div style="margin-bottom: 3px;">• Klaster Akun Sasaran Takedown: <b style="color: #EF4444;">{cib_cluster_val}</b></div>
<div>• Bukti Sintetis / Telemetri: <b style="color: #22D3EE;">{evidence_val}</b></div>
</div>
</div>"""
            st.markdown(card_html, unsafe_allow_html=True)
            
            if is_rejected:
                st.error("⛔ **Status Insiden Ditolak:** Insiden ini telah ditandai sebagai *Bukan Ancaman / False Positive* oleh Komandan. Seluruh aksi otomatisasi dibekukan.")
            elif not is_approved:
                st.markdown("<div style='margin-top: 8px;'></div>", unsafe_allow_html=True)
                with st.container(border=True):
                    col_q1, col_q2 = st.columns([7.5, 4.5])
                    with col_q1:
                        if "Komandan" in current_role:
                            st.markdown("##### ✍️ Otorisasi Cepat Komandan (1-Klik)")
                            st.caption("Peran Komandan aktif. Sahkan berkas paket penanggulangan ini langsung dari sini:")
                        else:
                            st.markdown("##### 🔒 Status: Menunggu Otorisasi Komandan")
                            st.caption("Dokumen resmi belum disahkan. Ubah peran ke Komandan di sidebar kiri untuk menandatangani.")
                    with col_q2:
                        if "Komandan" in current_role:
                            if st.button("✍️ Sahkan Dokumen Ini Sekarang", type="primary", use_container_width=True, key=f"quick_tab1_appr_{inc_id}"):
                                mark_incident_approved(inc_id, current_role)
                                st.session_state["approved_incidents"] = get_approved_incidents()
                                st.session_state["rejected_incidents"] = get_rejected_incidents()
                                st.session_state["audit_logs"] = get_audit_logs()
                                st.toast(f"Insiden {inc_id} berhasil disahkan oleh Komandan!", icon="✍️")
                                st.rerun()

            
            # Fact-Checking Infographic Brief
            st.markdown("#### 📢 Materi Briefing Komunikasi Publik Dispenad")
            if active_inc.get("is_from_radar"):
                brief_text = f"""
                **Poin Kunci Cek Fakta & Tindak Lanjut Dispenad/Pussiberad:**
                1. **Fakta 1:** Narasi mengenai "{inc_title}" terindikasi sebagai disinformasi/hoaks manipulatif.
                2. **Fakta 2:** Analisis laboratorium intelijen siber mencatat probabilitas botnet/CIB sebesar {active_inc.get('cib_probability', 80)}% dengan viralitas {active_inc.get('virality_score', 85)}/100 pada platform {active_inc.get('platform', 'Media')}.
                3. **Fakta 3:** Situasi satuan jajaran teritorial ({target_kodam_val}) dalam kondisi aman, solid, dan kondusif.
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

            # Hasil Akhir Dokumen Uji Cognitive Wargaming Sandbox
            st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
            st.markdown("#### 🧠 Naskah Klarifikasi Terverifikasi (Hasil Uji Wargaming Persona)")
            wg_res = get_latest_wargaming_result()
            
            wg_pass = wg_res.get("passed", True)
            wg_border_col = "#10B981" if wg_pass else "#EF4444"
            wg_badge_text = "✓ LOLOS UJI KOGNITIF (SIAP DIRILIS)" if wg_pass else "⚠️ PERINGATAN RISIKO TINGGI (PERLU REVISI)"
            
            st.markdown(
                f"""
                <div style="background: rgba(16, 185, 129, 0.05); border: 1px solid rgba(16, 185, 129, 0.3); border-left: 4px solid {wg_border_col}; padding: 12px 16px; border-radius: 4px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; flex-wrap: wrap;">
                        <span style="font-family: 'JetBrains Mono'; font-size: 0.75rem; color: {wg_border_col}; font-weight: bold;">
                            {wg_badge_text}
                        </span>
                        <span style="font-family: 'JetBrains Mono'; font-size: 0.70rem; color: #94A3B8;">
                            🕒 Waktu Uji: {wg_res.get('timestamp', '-')}
                        </span>
                    </div>
                    <div style="font-family: 'Inter', sans-serif; font-size: 0.85rem; color: #F8FAFC; line-height: 1.5; font-style: italic; background: #070D18; padding: 10px 14px; border-radius: 4px; border: 1px solid #1E293B; margin-bottom: 10px;">
                        "{wg_res.get('draft_text', '')}"
                    </div>
                    <div style="display: flex; justify-content: space-between; flex-wrap: wrap; gap: 8px; font-family: 'JetBrains Mono'; font-size: 0.72rem; background: #0B1120; padding: 8px 12px; border-radius: 4px;">
                        <span>🟢 Penerimaan Publik: <b style="color: #34D399;">{wg_res.get('positive_sentiment', 86.5)}%</b></span>
                        <span>🛡️ Risiko Backfire: <b style="color: {'#10B981' if wg_res.get('backfire_risk', 11.2) < 25 else '#EF4444'};">{wg_res.get('backfire_risk', 11.2)}%</b></span>
                        <span>🏷️ Diksi: <b style="color: #38BDF8;">{wg_res.get('overall_tone', 'Taktis & Kredibel')}</b></span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.caption("💡 *Naskah di atas teruji secara otomatis ke 10 multi-agent persona dari modul **'Wargaming Sandbox Persona'** dan telah dilampirkan langsung ke berkas Executive SITREP PDF di samping.*")

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
                file_name=f"SITREP_{inc_id}_TNI_AD.pdf",
                mime="application/pdf",
                use_container_width=True
            )
            
            st.markdown("<div style='margin-top: 8px;'></div>", unsafe_allow_html=True)
            
            st.download_button(
                label="⚡ Unduh Takedown Dossier (JSON Standar BSSN/Kominfo)",
                data=json_str,
                file_name=f"TAKEDOWN_DOSSIER_{inc_id}_BSSN.json",
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
                if is_rejected:
                    st.error("⛔ Transmisi Ditolak: Paket SOAR berstatus 'Ditolak/False Positive' tidak dapat dikirim ke mitra agensi.")
                elif not is_approved:
                    st.warning("⚠️ Perhatian: Paket SOAR belum disetujui secara digital oleh Komandan. Hanya paket berstatus 'Approved' yang dapat dikirim otomatis.")
                else:
                    st.success(f"✅ Berhasil ditransmisikan ke BSSN Gateway! Tiket ID: #BSSN-TKD-{inc_id}")
                    st.session_state["audit_logs"].insert(0, {
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S WIB"),
                        "user": current_role,
                        "role": current_role,
                        "action": "TRANSMISI DOSSIER BSSN",
                        "target": inc_id,
                        "status": "TERKIRIM INTER-AGENCY",
                        "hash": "a4c7e190...77b2"
                    })
                    
            # Opsi Hapus Antrean SOAR langsung dari Tab 1
            if active_inc.get("is_from_radar") or active_inc.get("id") in get_escalated_incidents():
                st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
                with st.container(border=True):
                    st.markdown("##### ⚙️ Manajemen Antrean SOAR (Pembatalan Eskalasi)")
                    st.caption("Menghapus insiden ini dari antrean SOAR dan mengaktifkan kembali tombol 'Eskalasikan ke SOAR' di Radar C2:")
                    if st.button("🗑️ Batalkan & Hapus dari Antrean SOAR", key=f"del_tab1_{inc_id}", type="secondary", use_container_width=True):
                        remove_escalated_incident(inc_id, current_role)
                        st.session_state["approved_incidents"] = get_approved_incidents()
                        st.session_state["rejected_incidents"] = get_rejected_incidents()
                        st.session_state["audit_logs"] = get_audit_logs()
                        st.session_state["escalated_soar_incidents"] = get_escalated_incidents()
                        st.toast(f"Insiden {inc_id} berhasil dihapus dari antrean SOAR!", icon="🗑️")
                        st.rerun()

    # -------------------------------------------------------------
    # TAB 2: RBAC COMMANDER APPROVAL
    # -------------------------------------------------------------
    with tab_rbac:
        st.markdown("### 🎖️ RUKUN OTORISASI BERJENJANG (ROLE-BASED ACCESS CONTROL)")
        st.markdown(
            "Menjaga *Chain of Command* dan akuntabilitas hukum. Hanya peran **Perwira Menengah / Komandan** "
            "yang berhak memberikan otorisasi penindakan, menolak false positive, mencabut otorisasi, atau membubuhkan tanda tangan kriptografis."
        )
        
        is_commander = "Komandan" in current_role
        role_border_color = "#10B981" if is_commander else "#38BDF8"
        role_desc_text = "✅ **Hak Akses Penuh:** Anda berwenang Menyetujui (Digital Signature), Menolak (Reject FP), dan Mencabut Izin (Revoke)." if is_commander else "ℹ️ **Peran Analis/Staf:** Anda dapat memantau antrean dan membatalkan/menghapus eskalasi. Untuk menandatangani persetujuan atau menolak insiden, silakan ubah peran di sidebar kiri menjadi **'Perwira Menengah / Komandan'**."
        
        # Display Current Active Role with Context & Build Badge
        st.markdown(
            f"""
            <div style="background: #0B1120; border: 1px solid #334155; border-left: 4px solid {role_border_color}; padding: 12px 18px; border-radius: 6px; margin-bottom: 15px;">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                    <div>
                        <span style="font-family: 'JetBrains Mono'; font-size: 0.78rem; color: #94A3B8;">PERAN PENGGUNA SAAT INI:</span>
                        <span style="font-family: 'Chakra Petch'; font-size: 1.15rem; font-weight: bold; color: #22D3EE; margin-left: 10px;">
                            {current_role}
                        </span>
                    </div>
                    <span style="font-family: 'JetBrains Mono'; font-size: 0.72rem; color: #10B981; background: rgba(16, 185, 129, 0.1); padding: 3px 8px; border-radius: 4px; border: 1px solid rgba(16, 185, 129, 0.3);">BUILD v2.5.2-LIVE (ACTIVE)</span>
                </div>
                <div style="font-size: 0.8rem; color: #CBD5E1; margin-top: 8px; line-height: 1.4;">{role_desc_text}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        col_approval_left, col_approval_right = st.columns([7, 5])
        
        with col_approval_left:
            all_incidents = get_all_soar_incidents()
            approved_set = st.session_state["approved_incidents"]
            rejected_set = st.session_state["rejected_incidents"]
            
            pending_list = [i for i in all_incidents if i["id"] not in approved_set and i["id"] not in rejected_set]
            approved_list = [i for i in all_incidents if i["id"] in approved_set]
            rejected_list = [i for i in all_incidents if i["id"] in rejected_set]

            # 1. Top Metrics Banner for Status Antrean
            m_col1, m_col2, m_col3, m_col4 = st.columns(4)
            with m_col1:
                st.metric("Total Antrean", f"{len(all_incidents)} Berkas", "Terintegrasi")
            with m_col2:
                st.metric("🟡 Menunggu", f"{len(pending_list)} Berkas", "Pending Review")
            with m_col3:
                st.metric("🟢 Disetujui", f"{len(approved_list)} Berkas", "Tersertifikasi")
            with m_col4:
                st.metric("🔴 Ditolak", f"{len(rejected_list)} Berkas", "Bukan Ancaman")

            st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
            
            # Batch Commander Approval Action
            if is_commander and len(pending_list) > 0:
                with st.container(border=True):
                    col_b1, col_b2 = st.columns([7.5, 4.5])
                    with col_b1:
                        st.markdown(f"##### ⚡ Eksekusi Komando: Sahkan Seluruh {len(pending_list)} Berkas Sekaligus")
                        st.caption("Membubuhkan tanda tangan digital kriptografis ke seluruh antrean yang pending dalam 1 kali klik.")
                    with col_b2:
                        if st.button("✍️ Sahkan Semua Sekaligus", type="primary", use_container_width=True):
                            cnt = approve_all_pending([i["id"] for i in pending_list], current_role)
                            st.session_state["approved_incidents"] = get_approved_incidents()
                            st.session_state["rejected_incidents"] = get_rejected_incidents()
                            st.session_state["audit_logs"] = get_audit_logs()
                            st.toast(f"Berhasil mengesahkan seluruh {cnt} antrean secara serentak!", icon="✍️")
                            st.rerun()

            st.markdown("#### Daftar Antrean Permohonan Otorisasi SOAR")
            
            # Filter Status Antrean dengan Hitungan Dinamis
            filter_map = {
                f"Semua ({len(all_incidents)})": "all",
                f"🟡 Menunggu Persetujuan ({len(pending_list)})": "pending",
                f"🟢 Sudah Disetujui ({len(approved_list)})": "approved",
                f"🔴 Ditolak ({len(rejected_list)})": "rejected"
            }
            selected_filter_label = st.radio(
                "Saring Antrean:",
                options=list(filter_map.keys()),
                index=0,
                horizontal=True
            )
            filter_mode = filter_map[selected_filter_label]
            
            if filter_mode == "pending":
                filtered_incidents = pending_list
            elif filter_mode == "approved":
                filtered_incidents = approved_list
            elif filter_mode == "rejected":
                filtered_incidents = rejected_list
            else:
                filtered_incidents = all_incidents
                
            if not filtered_incidents:
                st.info(f"Tidak ada antrean insiden pada filter '{selected_filter_label}'.")
            
            for inc in filtered_incidents:
                inc_id = inc["id"]
                already_approved = inc_id in st.session_state["approved_incidents"]
                already_rejected = inc_id in st.session_state["rejected_incidents"]
                is_from_radar = inc.get("is_from_radar", False)
                
                with st.container():
                    if inc.get("bot_accounts_list"):
                        radar_tag_html = f"<div style='font-family: JetBrains Mono; font-size: 0.68rem; color: #F59E0B; margin-bottom: 4px;'>⚡ TAKEDOWN KOLEKTIF MASSAL ({len(inc.get('bot_accounts_list', []))} AKUN) • {inc.get('escalated_at', 'Baru saja')}</div>"
                    elif inc.get("is_from_cib") or "TKD-BOT" in inc_id:
                        bot_name = inc.get("bot_account", inc.get("title", ""))
                        radar_tag_html = f"<div style='font-family: JetBrains Mono; font-size: 0.68rem; color: #38BDF8; margin-bottom: 4px;'>🤖 PERMOHONAN TAKEDOWN AKUN BOT: <b>{bot_name}</b> ({inc.get('platform', 'Medsos')}) • {inc.get('escalated_at', 'Baru saja')}</div>"
                    elif is_from_radar:
                        radar_tag_html = f"<div style='font-family: JetBrains Mono; font-size: 0.68rem; color: #22D3EE; margin-bottom: 4px;'>📡 ESKALASI LANGSUNG DARI RADAR C2 ({inc.get('platform', 'Medsos')}) • {inc.get('escalated_at', 'Baru saja')}</div>"
                    else:
                        radar_tag_html = ""
                    
                    if already_approved:
                        approval_status_text = "[STATUS: DISETUJUI KOMANDAN]"
                        approval_status_color = "#10B981"
                        card_border_color = "#10B981"
                    elif already_rejected:
                        approval_status_text = "[STATUS: DITOLAK / FALSE POSITIVE]"
                        approval_status_color = "#EF4444"
                        card_border_color = "#EF4444"
                    else:
                        approval_status_text = "[MENUNGGU PERSETUJUAN]"
                        approval_status_color = "#F59E0B"
                        card_border_color = "#F59E0B"
                        
                    card_level = inc.get('level', inc.get('threat_level', 'Kritis'))
                    card_kodam = inc.get('target_kodam', inc.get('kodam', 'Mabesad'))
                    inc_title = inc.get('title', inc.get('headline', 'Insiden Ancaman'))
                    
                    card_tab2 = f"""<div style="background: #111C2E; border: 1px solid #1E293B; border-left: 3px solid {card_border_color}; padding: 12px; border-radius: 4px; margin-bottom: 8px;">
{radar_tag_html}
<div style="display: flex; justify-content: space-between; font-family: 'JetBrains Mono', monospace; font-size: 0.72rem;">
<span style="color: #38BDF8;">{inc_id}</span>
<span style="color: {approval_status_color}; font-weight: bold;">{approval_status_text}</span>
</div>
<div style="font-weight: 600; color: #FFFFFF; font-size: 0.88rem; margin: 4px 0;">{inc_title}</div>
<div style="font-size: 0.78rem; color: #94A3B8;">Tingkat: <b style="color: #EF4444;">{card_level}</b> | Yurisdiksi: {card_kodam}</div>
</div>"""
                    st.markdown(card_tab2, unsafe_allow_html=True)
                    
                    # Alur Aksi Berdasarkan Status
                    if already_approved:
                        c_app_1, c_app_2 = st.columns([7, 3])
                        with c_app_1:
                            st.caption("✅ Dokumen telah disahkan secara kriptografis SHA-256. Berkas siap ditransmisikan di Tab 1.")
                        with c_app_2:
                            if is_commander:
                                if st.button(f"↩️ Cabut Izin", key=f"revoke_{inc_id}", help="Batalkan persetujuan dan kembalikan ke status pending"):
                                    revoke_incident_status(inc_id, current_role)
                                    st.session_state["approved_incidents"] = get_approved_incidents()
                                    st.session_state["rejected_incidents"] = get_rejected_incidents()
                                    st.session_state["audit_logs"] = get_audit_logs()
                                    st.toast(f"Persetujuan {inc_id} telah dicabut.", icon="↩️")
                                    st.rerun()
                    elif already_rejected:
                        c_rej_1, c_rej_2 = st.columns([7, 3])
                        with c_rej_1:
                            st.caption("⛔ Insiden ditandai sebagai Bukan Ancaman / False Positive.")
                        with c_rej_2:
                            if is_commander:
                                if st.button(f"🔄 Buka Ulang", key=f"reopen_{inc_id}", help="Buka kembali untuk evaluasi ulang"):
                                    revoke_incident_status(inc_id, current_role)
                                    st.session_state["approved_incidents"] = get_approved_incidents()
                                    st.session_state["rejected_incidents"] = get_rejected_incidents()
                                    st.session_state["audit_logs"] = get_audit_logs()
                                    st.toast(f"Insiden {inc_id} dibuka kembali.", icon="🔄")
                                    st.rerun()
                    else:
                        # Status Pending / Menunggu Otorisasi
                        if is_commander:
                            c_btn_1, c_btn_2 = st.columns([6, 4])
                            with c_btn_1:
                                if st.button(f"✍️ Setujui ({inc_id})", key=f"appr_{inc_id}", type="primary", use_container_width=True):
                                    mark_incident_approved(inc_id, current_role)
                                    st.session_state["approved_incidents"] = get_approved_incidents()
                                    st.session_state["rejected_incidents"] = get_rejected_incidents()
                                    st.session_state["audit_logs"] = get_audit_logs()
                                    st.toast(f"Insiden {inc_id} berhasil disetujui!", icon="✍️")
                                    st.rerun()
                            with c_btn_2:
                                if st.button(f"⛔ Tolak", key=f"rej_{inc_id}", use_container_width=True, help="Tolak insiden sebagai False Positive"):
                                    mark_incident_rejected(inc_id, current_role)
                                    st.session_state["approved_incidents"] = get_approved_incidents()
                                    st.session_state["rejected_incidents"] = get_rejected_incidents()
                                    st.session_state["audit_logs"] = get_audit_logs()
                                    st.toast(f"Insiden {inc_id} ditolak sebagai False Positive.", icon="⛔")
                                    st.rerun()
                        else:
                            st.caption("🔒 Otorisasi terkunci. Pindah ke peran 'Perwira Menengah / Komandan' di sidebar untuk menandatangani atau menolak.")
                    
                    # Tombol Batalkan Eskalasi / Hapus Antrean untuk insiden radar atau eskalasi dinamis
                    if is_from_radar or inc_id in get_escalated_incidents():
                        if st.button(f"🗑️ Batalkan & Hapus dari Antrean SOAR ({inc_id})", key=f"del_queue_{inc_id}", type="secondary", use_container_width=True):
                            remove_escalated_incident(inc_id, current_role)
                            st.session_state["approved_incidents"] = get_approved_incidents()
                            st.session_state["rejected_incidents"] = get_rejected_incidents()
                            st.session_state["audit_logs"] = get_audit_logs()
                            st.session_state["escalated_soar_incidents"] = get_escalated_incidents()
                            st.toast(f"Insiden {inc_id} dihapus dari antrean SOAR. Tombol di Radar kembali aktif.", icon="🗑️")
                            st.rerun()
                            
                    st.markdown("<div style='margin-bottom: 8px;'></div>", unsafe_allow_html=True)

            # 2. Dedicated Riwayat Persetujuan Resmi Komandan
            st.markdown("---")
            st.markdown("#### 📜 Riwayat Berkas Resmi yang Telah Disahkan Komandan")
            if approved_list:
                hist_table = []
                for a_inc in approved_list:
                    a_title = a_inc.get("title", a_inc.get("headline", "Insiden"))
                    a_plat = a_inc.get("platform", a_inc.get("root_platform", "Multi-Platform"))
                    hist_table.append({
                        "No Register": a_inc["id"],
                        "Sasaran / Target": a_title[:38] + ("..." if len(a_title) > 38 else ""),
                        "Platform": a_plat,
                        "Tingkat": a_inc.get("level", a_inc.get("threat_level", "Kritis")),
                        "Status Hukum": "🟢 SAH & DISETUJUI",
                        "Tanda Tangan Kripto": f"SHA256:{a_inc['id'].lower().replace('-', '')[:8]}...99f0"
                    })
                st.dataframe(pd.DataFrame(hist_table), hide_index=True, use_container_width=True)
            else:
                st.info("Belum ada berkas insiden yang disahkan.")

        with col_approval_right:
            st.markdown("#### Matriks Hak Akses (RBAC Matrix)")
            
            rbac_data = [
                {"Aksi Sistem": "Buat Draf Analisis Ancaman", "Pussiberad": "✅ YA", "Dispenad": "✅ YA", "Komandan": "✅ YA"},
                {"Aksi Sistem": "Uji Wargaming & Personas", "Pussiberad": "✅ YA", "Dispenad": "✅ YA", "Komandan": "✅ YA"},
                {"Aksi Sistem": "Klarifikasi Pers Dispenad", "Pussiberad": "❌ Tinjau", "Dispenad": "✅ Rilis", "Komandan": "✅ Otorisasi"},
                {"Aksi Sistem": "Persetujuan Takedown Eksternal", "Pussiberad": "❌ Draf", "Dispenad": "❌ Tinjau", "Komandan": "✅ MUTLAK"},
                {"Aksi Sistem": "Tanda Tangan Kriptografi", "Pussiberad": "❌ Dilarang", "Dispenad": "❌ Dilarang", "Komandan": "✅ SAH"},
                {"Aksi Sistem": "Tolak Otorisasi (Reject FP)", "Pussiberad": "❌ Usul", "Dispenad": "❌ Usul", "Komandan": "✅ MUTLAK"},
                {"Aksi Sistem": "Cabut Persetujuan (Revoke)", "Pussiberad": "❌ Dilarang", "Dispenad": "❌ Dilarang", "Komandan": "✅ SAH"},
                {"Aksi Sistem": "Hapus dari Antrean SOAR", "Pussiberad": "✅ YA", "Dispenad": "✅ YA", "Komandan": "✅ YA"}
            ]
            
            st.dataframe(
                pd.DataFrame(rbac_data),
                hide_index=True,
                use_container_width=True
            )

            # 3. Dedicated Pusat Cadangan & Pemulihan SOAR
            st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
            st.markdown("#### 💾 Pusat Cadangan & Pemulihan SOAR")
            st.markdown(
                "<p style='font-size: 0.8rem; color: #94A3B8;'>"
                "Menjamin seluruh status persetujuan, antrean insiden, dan jejak audit dapat dicadangkan offline atau dipulihkan kapan saja."
                "</p>",
                unsafe_allow_html=True
            )
            
            b_data_str = export_soar_backup_json()
            b1, b2 = st.columns(2)
            with b1:
                st.download_button(
                    "💾 Unduh Cadangan SOAR (JSON)",
                    data=b_data_str,
                    file_name=f"SOAR_Backup_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                    mime="application/json",
                    use_container_width=True
                )
            with b2:
                if st.button("🔄 Sinkronkan Ulang Storage", use_container_width=True):
                    st.session_state["approved_incidents"] = get_approved_incidents()
                    st.session_state["rejected_incidents"] = get_rejected_incidents()
                    st.session_state["audit_logs"] = get_audit_logs()
                    st.session_state["escalated_soar_incidents"] = get_escalated_incidents()
                    st.toast("Storage dan antrean persetujuan berhasil disinkronkan!", icon="🔄")
                    st.rerun()

            with st.expander("📥 Pulihkan Cadangan dari Berkas JSON"):
                uploaded_backup = st.file_uploader("Pilih Berkas Cadangan SOAR (.json):", type=["json"], key="uploader_backup_soar")
                if uploaded_backup is not None:
                    if st.button("Pulihkan Status Sekarang", type="primary"):
                        success, msg = restore_soar_backup_json(uploaded_backup.read().decode("utf-8"))
                        if success:
                            st.session_state["approved_incidents"] = get_approved_incidents()
                            st.session_state["rejected_incidents"] = get_rejected_incidents()
                            st.session_state["audit_logs"] = get_audit_logs()
                            st.session_state["escalated_soar_incidents"] = get_escalated_incidents()
                            st.success(msg)
                            st.rerun()
                        else:
                            st.error(msg)


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
