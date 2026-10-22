"""
app.py - Main Entrypoint for SENTINEL-AD
Defense-Grade Cognitive Operations & Threat Intelligence System for TNI AD
# (Indonesian Army Cyber & Cognitive Defense Command) - Build v2.4.1
"""

import streamlit as st

# Configure Page
st.set_page_config(
    page_title="SENTINEL-AD | TNI AD Cognitive Operations",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import Utilities and Modules
from utils.theme import inject_tactical_theme, render_tactical_header
from modules.dashboard import render_dashboard
from modules.ingestion_tracker import render_ingestion_tracker
from modules.cib_screener import render_cib_screener
from modules.wargaming_sandbox import render_wargaming_sandbox
from modules.threat_graph import render_threat_graph
from modules.soar_approval import render_soar_approval

def main():
    # 1. Inject Military Tactical Dark Theme CSS
    inject_tactical_theme()
    
    # 1b. Initialize Global SOAR Persistent State
    from utils.soar_storage import get_escalated_incidents, get_approved_incidents, get_rejected_incidents, get_audit_logs
    if "approved_incidents" not in st.session_state:
        st.session_state["approved_incidents"] = get_approved_incidents()
    if "rejected_incidents" not in st.session_state:
        st.session_state["rejected_incidents"] = get_rejected_incidents()
    if "escalated_soar_incidents" not in st.session_state:
        st.session_state["escalated_soar_incidents"] = get_escalated_incidents()
    if "audit_logs" not in st.session_state:
        st.session_state["audit_logs"] = get_audit_logs()
    
    # 2. Sidebar Navigation & Tactical Role Switcher
    with st.sidebar:
        st.markdown(
            """
            <div style="text-align: center; padding: 12px 6px; border-bottom: 1px solid #1E293B; margin-bottom: 16px;">
                <div style="font-size: 2.2rem; margin-bottom: 4px;">🛡️</div>
                <div style="font-family: 'Chakra Petch', sans-serif; font-size: 1.35rem; font-weight: 800; color: #22D3EE; letter-spacing: 0.1em;">
                    SENTINEL-AD
                </div>
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.68rem; color: #94A3B8; text-transform: uppercase; margin-top: 2px;">
                    TNI AD Cognitive Defense System
                </div>
                <div style="margin-top: 6px;">
                    <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.62rem; background: rgba(6, 182, 212, 0.15); color: #06B6D4; border: 1px solid rgba(6, 182, 212, 0.4); padding: 2px 6px; border-radius: 4px;">
                        PUSSIBERAD × DISPENAD
                    </span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown("### 👤 OTORISASI PERAN (RBAC)")
        role_options = [
            "Analis Siber (Pussiberad)",
            "Komunikasi Publik / Penerangan (Dispenad)",
            "Perwira Menengah / Komandan (Pengambil Keputusan)"
        ]
        
        # Preserve active role in session state
        if "active_role" not in st.session_state:
            st.session_state["active_role"] = role_options[0]
            
        current_role = st.selectbox(
            "Pilih Peran Personel Operasi:",
            options=role_options,
            index=role_options.index(st.session_state["active_role"]),
            key="role_selector"
        )
        st.session_state["active_role"] = current_role
        
        st.markdown("### ⚠️ STATUS KESIAPSIAGAAN (DEFCON)")
        defcon_levels = ["DEFCON 1", "DEFCON 2", "DEFCON 3", "DEFCON 4", "DEFCON 5"]
        selected_defcon = st.selectbox(
            "Tingkat Ancaman Kognitif:",
            options=defcon_levels,
            index=2  # DEFCON 3 by default
        )
        
        st.markdown("### 🌐 SUMBER TELEMETRI (GO-LIVE)")
        st.session_state["data_source_mode"] = "live"
        
        st.markdown(
            """
            <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid #10B981; border-radius: 6px; padding: 7px 10px; margin-bottom: 10px; display: flex; align-items: center; justify-content: space-between;">
                <span style="color: #34D399; font-weight: bold; font-size: 0.78rem; font-family: 'JetBrains Mono', monospace;">
                    🟢 LIVE ONLINE OSINT
                </span>
                <span style="font-size: 0.68rem; background: #064E3B; color: #A7F3D0; padding: 2px 6px; border-radius: 4px; border: 1px solid #059669; font-weight: bold;">
                    REAL-TIME
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        if st.button("🔄 Tarik Data Nyata Terbaru (Sync OSINT)", use_container_width=True):
            st.session_state["live_feed_cache"] = None
            st.toast("Menarik data online real-time dari TikTok, IG, X, FB, YouTube & Media Daring...", icon="🌐")
            st.rerun()
        st.caption("📡 **Radar Terhubung:** TikTok, Instagram, X (Twitter), Facebook, YouTube, Media Daring")
                
        with st.expander("⚙️ Konfigurasi API Resmi Lembaga"):
            st.text_input("X (Twitter) Bearer Token", type="password", placeholder="Bearer AAAA...", key="x_bearer_token")
            st.text_input("YouTube Data API Key", type="password", placeholder="AIzaSy...", key="youtube_api_key")
            st.text_input("Meta (Instagram & FB) Graph Token", type="password", placeholder="EAAX...", key="meta_access_token")
            st.text_input("Telegram Bot Token / MTProto", type="password", placeholder="bot123456:ABC-...", key="telegram_token")
            st.text_input("BSSN Gateway API Key", type="password", placeholder="bssn-csirt-token-...", key="bssn_api_key")
            st.caption("ℹ️ **Mode Hybrid OSINT Aktif:** Sistem otomatis menarik stream data nyata dari TikTok, Instagram, X, Facebook, YouTube, dan Berita secara real-time. Jika token API resmi diisi, sistem akan memprioritaskan endpoint resmi lembaga.")
        
        st.markdown("<hr style='border: 0.5px solid #1E293B; margin: 15px 0;'/>", unsafe_allow_html=True)
        
        st.markdown("### 🧭 MODUL TAKTIS")
        menu_options = [
            "🛡️ Pusat Komando (C2 Overview & Peta)",
            "📡 Ingesti & Loncatan Narasi",
            "🔍 CIB & Deepfake Screener",
            "🧠 Wargaming Sandbox Persona",
            "🕸️ Graf Jaringan Ancaman (SNA)",
            "⚡ Tactical SOAR & Otorisasi"
        ]
        
        selected_menu = st.radio(
            "Pilih Menu Navigasi:",
            menu_options,
            index=0,
            label_visibility="collapsed"
        )
        
        st.markdown("<hr style='border: 0.5px solid #1E293B; margin: 15px 0;'/>", unsafe_allow_html=True)
        
        # Telemetry Quick Status
        st.markdown(
            """
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; color: #64748B; background: #070D18; padding: 10px; border-radius: 4px; border: 1px solid #1E293B;">
                <div style="color: #10B981;">● SENSOR RADAR: AKTIF (6 EKOSISTEM LINTAS-MEDSOS)</div>
                <div style="color: #10B981;">● ENKRIPSI: AES-256-GCM / SHA-256</div>
                <div style="color: #38BDF8;">● JARINGAN: MILNET SECURE GATEWAY</div>
                <div style="margin-top: 6px; font-size: 0.65rem; color: #475569;">
                    SENTINEL-AD v2.5 BUILD 2026.10-MULTI-OSINT<br/>
                    KLASIFIKASI: RAHASIA / DEFENSE ONLY
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # 3. Tactical Header Bar
    render_tactical_header(current_role=current_role, threat_level=selected_defcon)
    
    # 4. Route to Selected Tactical Module
    if "Pusat Komando" in selected_menu:
        render_dashboard(current_role=current_role)
    elif "Ingesti & Loncatan" in selected_menu:
        render_ingestion_tracker()
    elif "CIB & Deepfake" in selected_menu:
        render_cib_screener()
    elif "Wargaming Sandbox" in selected_menu:
        render_wargaming_sandbox()
    elif "Graf Jaringan" in selected_menu:
        render_threat_graph()
    elif "Tactical SOAR" in selected_menu:
        render_soar_approval(current_role=current_role)

if __name__ == "__main__":
    main()
