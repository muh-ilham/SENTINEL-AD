"""
modules/threat_graph.py - Social Network Analysis (SNA) Interactive Threat Graph
Renders interactive Pyvis network graph revealing Seed Accounts, Amplifiers, Bridges, and Organic Audiences.
"""

import streamlit as st
import streamlit.components.v1 as components
import networkx as nx
from pyvis.network import Network
import tempfile
import os
from utils.data_generator import generate_network_graph_data

def render_threat_graph():
    """Renders the Interactive Pyvis SNA Network Graph and Node Intelligence Panel."""
    st.markdown("## 🕸️ GRAF JARINGAN ANCAMAN & ANALISIS SIMPUL (SNA THREAT GRAPH)")
    st.markdown(
        "<p style='color: #94A3B8; font-size: 0.95rem; margin-top: -10px;'>"
        "Pemetaan Topologi Operasi Disinformasi: Pelacakan Akun Seed (Merah), Klaster Amplifikasi (Oranye), Simpul Jembatan (Kuning), dan Audiens Organik (Abu-abu)."
        "</p>",
        unsafe_allow_html=True
    )
    
    nodes_data, edges_data = generate_network_graph_data()
    
    # 1. Top SNA Metrics
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Total Simpul (Nodes)", f"{len(nodes_data)} Akun", "Terpetakan")
    with m2:
        st.metric("Simpul Seed Utama", "2 Aktor Inisiator", "Penyebar Dokumen & Audio")
    with m3:
        st.metric("Simpul Jembatan (Bridge)", "3 Kanal Kunci", "Betweenness Centrality Tinggi")
    with m4:
        st.metric("Klaster Amplifikasi", "7 Botnet / Influencer", "Sub-Menit Retweet")

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
            hover_title = f"{n['label']}\nKategori: {n['group']}\nKoneksi (Degree): {deg}\nBetweenness Centrality: {bet}\nCatatan: {n['info']}"
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
                    NODE ID: {curr_node['id'].upper()}
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

        st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
        if st.button("🚨 Tambahkan Simpul ke Target Paket Takedown SOAR", type="primary", use_container_width=True):
            st.toast(f"Simpul {curr_node['label']} berhasil ditambahkan ke dalam antrean SOAR!", icon="🛡️")
