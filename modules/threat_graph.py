"""
modules/threat_graph.py - Social Network Analysis (SNA) Interactive Threat Graph
Renders interactive Pyvis network graph revealing Seed Accounts, Amplifiers, Bridges, and Organic Audiences.
Fully synchronized with Live Multi-Platform OSINT Telemetry and Tactical SOAR Execution.
"""

import streamlit as st
import streamlit.components.v1 as components
import networkx as nx
from pyvis.network import Network
import tempfile
import os
import json
import pandas as pd
from datetime import datetime
from utils.data_generator import generate_network_graph_data
from utils.soar_storage import (
    check_is_escalated,
    add_escalated_incident,
    get_escalated_incidents,
    get_approved_incidents,
    get_audit_logs
)

def render_threat_graph():
    """Renders the Interactive Pyvis SNA Network Graph, Live Status, and Node Intelligence Panel."""
    st.markdown("## 🕸️ GRAF JARINGAN ANCAMAN & ANALISIS SIMPUL (SNA THREAT GRAPH)")
    st.markdown(
        "<p style='color: #94A3B8; font-size: 0.95rem; margin-top: -10px;'>"
        "Pemetaan Topologi Operasi Disinformasi: Pelacakan Akun Seed (Merah), Klaster Amplifikasi (Oranye), Simpul Jembatan (Kuning), dan Audiens Organik (Abu-abu)."
        "</p>",
        unsafe_allow_html=True
    )
    
    # Telemetry Synchronization Status Banner
    is_live = st.session_state.get("data_source_mode") == "live"
    if is_live:
        st.markdown(
            """
            <div style="background: rgba(34, 197, 94, 0.08); border: 1px solid #16A34A; border-radius: 6px; padding: 10px 16px; margin-bottom: 14px; display: flex; align-items: center; justify-content: space-between;">
                <div>
                    <span style="font-family: 'JetBrains Mono'; font-size: 0.82rem; color: #4ADE80; font-weight: bold;">
                        🟢 SINKRONISASI AKTIF: 6 EKOSISTEM MEDSOS (TikTok, Instagram, X, Facebook, YouTube, Media Daring)
                    </span><br/>
                    <span style="font-size: 0.76rem; color: #94A3B8;">
                        Graf SNA memetakan aktor nyata hasil ekstraksi telemetri OSINT real-time TNI AD.
                    </span>
                </div>
                <div style="text-align: right;">
                    <span style="font-family: 'JetBrains Mono'; font-size: 0.72rem; background: #14532D; color: #86EFAC; padding: 2px 8px; border-radius: 4px; border: 1px solid #22C55E;">
                        LIVE RADAR CONNECTED
                    </span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <div style="background: rgba(234, 179, 8, 0.08); border: 1px solid #EAB308; border-radius: 6px; padding: 10px 16px; margin-bottom: 14px; display: flex; align-items: center; justify-content: space-between;">
                <div>
                    <span style="font-family: 'JetBrains Mono'; font-size: 0.82rem; color: #FACC15; font-weight: bold;">
                        🟡 MODE SIMULASI TAKTIS CADANGAN (Offline Mock Topology)
                    </span><br/>
                    <span style="font-size: 0.76rem; color: #94A3B8;">
                        Topologi arsitektur berbasis skenario latihan serangan siber kognitif Pussiberad.
                    </span>
                </div>
                <div style="text-align: right;">
                    <span style="font-family: 'JetBrains Mono'; font-size: 0.72rem; background: #713F12; color: #FEF08A; padding: 2px 8px; border-radius: 4px; border: 1px solid #EAB308;">
                        SIMULATION SCENARIO
                    </span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    nodes_data, edges_data = generate_network_graph_data()
    
    # 1. Top SNA Metrics
    seed_count = len([n for n in nodes_data if n["group"] == "Seed Account"])
    bridge_count = len([n for n in nodes_data if n["group"] == "Bridge Node"])
    amp_count = len([n for n in nodes_data if n["group"] == "Amplifier Cluster"])

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Total Simpul (Nodes)", f"{len(nodes_data)} Akun", "Terpetakan Radar")
    with m2:
        st.metric("Simpul Seed Utama", f"{seed_count} Aktor Inisiator", "Penyebar Dokumen & Audio")
    with m3:
        st.metric("Simpul Jembatan (Bridge)", f"{bridge_count} Kanal Kunci", "Betweenness Centrality Tinggi")
    with m4:
        st.metric("Klaster Amplifikasi", f"{amp_count} Botnet / Agregator", "Sub-Menit Retweet")

    st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
    
    # Filters & Layout
    col_graph, col_panel = st.columns([8, 4])
    
    # Initialize NetworkX Graph to compute metrics
    G = nx.Graph()
    for n in nodes_data:
        G.add_node(n["id"], label=n["label"], group=n["group"], info=n["info"])
    for u, v, w in edges_data:
        G.add_edge(u, v, weight=w)
        
    degree_dict = dict(G.degree())
    betweenness_dict = nx.betweenness_centrality(G)
    
    with col_graph:
        st.markdown("#### Kanvas Visualisasi Interaktif Pyvis (Drag, Zoom & Inspect)")
        
        # Legend bar
        legend_html = """
        <div style="display: flex; gap: 15px; background: #0B1120; border: 1px solid #1E293B; padding: 6px 14px; border-radius: 4px; font-family: 'JetBrains Mono'; font-size: 0.75rem; margin-bottom: 8px;">
            <span><b style="color: #EF4444;">●</b> Seed Account (Inisiator)</span>
            <span><b style="color: #F97316;">●</b> Amplifier Cluster (Botnet)</span>
            <span><b style="color: #FBBF24;">●</b> Bridge Node (Penyalur Antar-Grup)</span>
            <span><b style="color: #94A3B8;">●</b> Audiens Organik (Masyarakat)</span>
        </div>
        """
        st.markdown(legend_html, unsafe_allow_html=True)
        
        # Build Pyvis Network
        net = Network(height="520px", width="100%", bgcolor="#0F172A", font_color="#F8FAFC")
        net.barnes_hut(gravity=-3000, central_gravity=0.3, spring_length=120, spring_strength=0.05, damping=0.9)
        
        for n in nodes_data:
            deg = degree_dict.get(n["id"], 1)
            bet = round(betweenness_dict.get(n["id"], 0.0), 3)
            hover_title = f"{n['label']}\nKategori: {n['group']}\nPlatform: {n.get('platform', 'Multi-Platform')}\nKoneksi (Degree): {deg}\nBetweenness Centrality: {bet}\nCatatan: {n['info']}"
            net.add_node(
                n["id"],
                label=n["label"],
                title=hover_title,
                color=n["color"],
                size=n["size"],
                borderWidth=2,
                borderWidthSelected=4,
                font={"face": "JetBrains Mono", "size": 11, "color": "#F8FAFC"}
            )
            
        for u, v, w in edges_data:
            net.add_edge(u, v, value=w, color="rgba(148, 163, 184, 0.35)", width=w)
            
        # Generate temporary HTML
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_file:
            net.save_graph(tmp_file.name)
            with open(tmp_file.name, 'r', encoding='utf-8') as f:
                html_content = f.read()
            tmp_path = tmp_file.name

        try:
            os.remove(tmp_path)
        except Exception:
            pass

        # Embed interactive HTML in Streamlit
        components.html(html_content, height=540, scrolling=False)

    with col_panel:
        st.markdown("#### Detail Intelijen Simpul Terpilih")
        
        node_options = {n["id"]: f"[{n['group']}] {n['label']}" for n in nodes_data}
        selected_node_id = st.selectbox(
            "Pilih Simpul untuk Investigasi Mendalam:",
            options=list(node_options.keys()),
            format_func=lambda x: node_options[x]
        )
        
        curr_node = next(item for item in nodes_data if item["id"] == selected_node_id)
        n_deg = degree_dict.get(curr_node["id"], 0)
        n_bet = round(betweenness_dict.get(curr_node["id"], 0.0), 3)
        
        # Detailed Card for Selected Node
        st.markdown(
            f"""
            <div style="background: #111C2E; border: 1px solid #1E293B; border-top: 3px solid {curr_node['color']}; padding: 14px; border-radius: 6px;">
                <div style="font-family: 'JetBrains Mono'; font-size: 0.72rem; color: #38BDF8; margin-bottom: 4px;">
                    NODE ID: {curr_node['id'].upper()} | PLATFORM: {curr_node.get('platform', 'Multi-Platform').upper()}
                </div>
                <div style="font-family: 'Chakra Petch'; font-size: 1.05rem; font-weight: bold; color: #FFFFFF; margin-bottom: 6px;">
                    {curr_node['label']}
                </div>
                <div style="margin-bottom: 10px;">
                    <span style="font-family: 'JetBrains Mono'; font-size: 0.72rem; background: {curr_node['color']}22; color: {curr_node['color']}; border: 1px solid {curr_node['color']}; padding: 2px 8px; border-radius: 12px; font-weight: bold;">
                        {curr_node['group'].upper()}
                    </span>
                </div>
                <div style="font-size: 0.8rem; color: #CBD5E1; margin-bottom: 12px; line-height: 1.4;">
                    <b>Profil Aktivitas:</b><br/>{curr_node['info']}
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; font-family: 'JetBrains Mono'; font-size: 0.75rem; background: #0B1120; padding: 8px; border-radius: 4px;">
                    <div>Koneksi (Degree): <b style="color: #22D3EE;">{n_deg} Tautan</b></div>
                    <div>Betweenness: <b style="color: #FBBF24;">{n_bet}</b></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
        st.markdown("##### 🎯 Rekomendasi Tindakan Taktis Pussiberad:")
        
        if curr_node["group"] == "Seed Account":
            st.error("🚨 PRIORITAS 1: SEED NODE. Ajukan takedown darurat ke BSSN & koordinasikan pelacakan IP data center.")
        elif curr_node["group"] == "Bridge Node":
            st.warning("⚠️ PRIORITAS 2: BRIDGE NODE. Kanal transmisi utama. Potong rantai amplifikasi sebelum menjangkau publik luas.")
        elif curr_node["group"] == "Amplifier Cluster":
            st.info("ℹ️ PRIORITAS 3: BOTNET FARM. Masukkan ke dalam daftar blokir terkoordinasi (Blacklist Hash).")
        else:
            st.success("✅ AUDIENS ORGANIK. Lakukan edukasi kognitif melalui rilis visual 'Debunking Hoaks' Dispenad.")

        st.markdown("<div style='margin-top: 12px;'></div>", unsafe_allow_html=True)
        
        # SOAR Escalation Status & Action
        node_inc_id = f"SNA-{curr_node['id'].upper()}"
        is_in_soar, _ = check_is_escalated({
            "id": node_inc_id,
            "headline": curr_node["label"],
            "bot_account": curr_node["label"]
        })
        
        if is_in_soar:
            st.success(f"✅ SIMPUL TERDAFTAR DI SOAR ({node_inc_id})")
            st.caption("Target ini telah masuk ke dalam antrean Tactical SOAR untuk disahkan Komandan dalam paket takedown BSSN.")
        else:
            if st.button("🚨 Tambahkan Simpul ke Target Paket Takedown SOAR", type="primary", use_container_width=True):
                now_wib = datetime.now().strftime("%Y-%m-%d %H:%M:%S WIB")
                role_actor = st.session_state.get("active_role", "Analis Siber (Pussiberad)")
                soar_record = {
                    "id": node_inc_id,
                    "title": f"Target Takedown Simpul SNA: {curr_node['label']}",
                    "headline": f"Penindakan Jaringan Disinformasi: Simpul {curr_node['label']} ({curr_node['group']})",
                    "sample_text": f"Terdeteksi melalui Social Network Analysis (SNA). Profil: {curr_node['info']}. Betweenness: {n_bet}, Degree: {n_deg}.",
                    "text": f"Terdeteksi melalui Social Network Analysis (SNA). Profil: {curr_node['info']}. Betweenness: {n_bet}, Degree: {n_deg}.",
                    "platform": curr_node.get("platform", "Multi-Platform"),
                    "root_platform": curr_node.get("platform", "Multi-Platform"),
                    "level": "Kritis" if curr_node["group"] == "Seed Account" else ("Tinggi" if curr_node["group"] == "Bridge Node" else "Sedang"),
                    "threat_level": "Kritis" if curr_node["group"] == "Seed Account" else ("Tinggi" if curr_node["group"] == "Bridge Node" else "Sedang"),
                    "target_kodam": "Mabes TNI AD / Teritorial",
                    "kodam": "Mabes TNI AD / Teritorial",
                    "cib_cluster_size": max(1, n_deg),
                    "amplification_nodes": max(1, n_deg),
                    "virality_score": int(n_bet * 100) if n_bet > 0 else 65,
                    "cib_probability": 94 if curr_node["group"] == "Seed Account" else (88 if curr_node["group"] == "Bridge Node" else 75),
                    "shares_count": max(1, n_deg) * 250,
                    "escalated_at": now_wib,
                    "escalated_by": role_actor,
                    "is_from_radar": True,
                    "is_from_sna": True,
                    "bot_account": curr_node["label"],
                    "bot_url": curr_node.get("link", f"https://sentinel-ad.mil.id/sna/{curr_node['id']}")
                }
                add_escalated_incident(soar_record)
                st.session_state["approved_incidents"] = get_approved_incidents()
                st.session_state["escalated_soar_incidents"] = get_escalated_incidents()
                st.session_state["audit_logs"] = get_audit_logs()
                st.toast(f"Simpul {curr_node['label']} ({node_inc_id}) berhasil didaftarkan ke antrean Takedown SOAR!", icon="🚨")
                st.rerun()

    # 2. Section: Dokumen Hasil Akhir & Ekspor Intelijen SNA
    st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### 📁 DOKUMEN HASIL AKHIR & EKSPOR INTELIJEN SNA")
    st.markdown(
        "<p style='color: #94A3B8; font-size: 0.9rem; margin-top: -8px;'>"
        "Hasil akhir analisis topologi jaringan dapat diunduh langsung dalam format Dossier JSON Terstandarisasi BSSN/Pussiberad, Matriks Simpul CSV, serta diteruskan ke Paket Takedown SOAR resmi."
        "</p>",
        unsafe_allow_html=True
    )
    
    # Prepare JSON Dossier
    topology_export = {
        "dossier_id": f"SNA-TOPOLOGY-{datetime.now().strftime('%Y%m%d-%H%M')}",
        "classification": "RAHASIA / DEFENSE CONFIDENTIAL",
        "system": "SENTINEL-AD TNI AD Cognitive Defense Command",
        "generated_at": datetime.now().isoformat(),
        "operator_role": st.session_state.get("active_role", "Analis Siber (Pussiberad)"),
        "telemetry_mode": "LIVE ONLINE OSINT (6 Ekosistem: TikTok, Instagram, X, Facebook, YouTube, Media Daring)" if is_live else "SIMULASI TAKTIS CADANGAN (Offline Mock)",
        "network_metrics": {
            "total_nodes": len(nodes_data),
            "seed_accounts_count": seed_count,
            "bridge_nodes_count": bridge_count,
            "amplifier_clusters_count": amp_count,
            "organic_audience_count": len([n for n in nodes_data if n["group"] == "Organic Audience"]),
            "total_edges": len(edges_data)
        },
        "nodes": [
            {
                "id": n["id"],
                "label": n["label"],
                "group": n["group"],
                "platform": n.get("platform", "Multi-Platform"),
                "degree_connections": degree_dict.get(n["id"], 0),
                "betweenness_centrality": round(betweenness_dict.get(n["id"], 0.0), 3),
                "activity_profile": n["info"],
                "priority_recommendation": (
                    "PRIORITAS 1 (Takedown Darurat BSSN & Pelacakan IP)" if n["group"] == "Seed Account"
                    else ("PRIORITAS 2 (Kanal Kunci - Putus Rantai Transmisi)" if n["group"] == "Bridge Node"
                    else ("PRIORITAS 3 (Botnet Farm - Blacklist Hash)" if n["group"] == "Amplifier Cluster"
                    else "AUDIENS ORGANIK (Edukasi Kognitif / Debunk Dispenad)"))
                )
            }
            for n in nodes_data
        ],
        "edges": [{"source": u, "target": v, "weight": w} for u, v, w in edges_data]
    }
    json_bytes = json.dumps(topology_export, indent=2, ensure_ascii=False).encode("utf-8")
    
    # Prepare CSV Matrix
    csv_rows = []
    for n in nodes_data:
        csv_rows.append({
            "Node ID": n["id"],
            "Label": n["label"],
            "Kategori": n["group"],
            "Platform": n.get("platform", "Multi-Platform"),
            "Degree (Koneksi)": degree_dict.get(n["id"], 0),
            "Betweenness Centrality": round(betweenness_dict.get(n["id"], 0.0), 3),
            "Profil Aktivitas": n["info"]
        })
    df_nodes = pd.DataFrame(csv_rows)
    csv_bytes = df_nodes.to_csv(index=False).encode("utf-8")
    
    e_col1, e_col2, e_col3 = st.columns([4, 4, 4])
    with e_col1:
        st.download_button(
            "📄 Unduh Laporan Topologi SNA (JSON Dossier)",
            data=json_bytes,
            file_name=f"SNA_Topologi_Dossier_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
            mime="application/json",
            use_container_width=True
        )
        st.caption("Format pertukaran data standar BSSN, CSIRT & Kominfo.")
    with e_col2:
        st.download_button(
            "📊 Unduh Matriks Simpul Ancaman (CSV)",
            data=csv_bytes,
            file_name=f"SNA_Matriks_Simpul_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
            use_container_width=True
        )
        st.caption("Tabel data lengkap simpul dan metrik centrality.")
    with e_col3:
        st.markdown(
            """
            <div style="background: #0B1120; border: 1px solid #1E293B; border-left: 3px solid #06B6D4; padding: 10px 14px; border-radius: 4px;">
                <b style="color: #38BDF8; font-size: 0.82rem;">🔗 Integrasi Dokumen SOAR & SITREP:</b><br/>
                <span style="font-size: 0.75rem; color: #94A3B8;">
                    Simpul yang ditambahkan ke SOAR secara otomatis disertakan ke dalam <b>Executive SITREP Resmi (PDF)</b> dan <b>Takedown Dossier (JSON)</b> setelah disahkan Komandan.
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )

