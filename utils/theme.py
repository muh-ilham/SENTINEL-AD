"""
utils/theme.py - Tactical Defense Dark Theme for SENTINEL-AD
Military-grade visual styling, HUD overlays, typography, and tactical components.
"""

import streamlit as st
from datetime import datetime, timezone, timedelta

def inject_tactical_theme():
    """Injects high-fidelity military tactical CSS styling into Streamlit."""
    css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Chakra+Petch:wght@400;600;700&family=JetBrains+Mono:wght@400;600;800&family=Inter:wght@300;400;500;600;700&display=swap');

    :root {
        --bg-tactical: #0F172A;
        --card-tactical: #1E293B;
        --border-tactical: #334155;
        --accent-cyan: #06B6D4;
        --accent-cyan-glow: rgba(6, 182, 212, 0.25);
        --alert-critical: #EF4444;
        --alert-warning: #F59E0B;
        --alert-safe: #10B981;
        --text-primary: #F8FAFC;
        --text-secondary: #94A3B8;
        --text-muted: #64748B;
        --tactical-mono: 'JetBrains Mono', monospace;
        --tactical-title: 'Chakra Petch', sans-serif;
    }

    /* Overall Layout & Background */
    .stApp {
        background: radial-gradient(circle at 10% 20%, #172554 0%, #0F172A 60%, #020617 100%);
        font-family: 'Inter', sans-serif;
        color: var(--text-primary);
    }

    /* Subtle Tactical Grid Overlay */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background-image: 
            linear-gradient(rgba(6, 182, 212, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(6, 182, 212, 0.03) 1px, transparent 1px);
        background-size: 32px 32px;
        pointer-events: none;
        z-index: 0;
    }

    /* Headers and Titles */
    h1, h2, h3, h4 {
        font-family: var(--tactical-title) !important;
        letter-spacing: 0.04em !important;
        text-transform: uppercase;
        color: #F8FAFC !important;
    }
    
    h1 {
        border-bottom: 2px solid rgba(6, 182, 212, 0.4);
        padding-bottom: 8px;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #0B1120 !important;
        border-right: 1px solid #1E293B !important;
    }

    /* Tactical Cards */
    .tactical-card {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.9), rgba(15, 23, 42, 0.95));
        border: 1px solid var(--border-tactical);
        border-left: 3px solid var(--accent-cyan);
        border-radius: 8px;
        padding: 16px 20px;
        margin-bottom: 16px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
        position: relative;
    }
    
    .tactical-card.danger {
        border-left-color: var(--alert-critical);
        box-shadow: 0 4px 20px rgba(239, 68, 68, 0.15);
    }

    .tactical-card.warning {
        border-left-color: var(--alert-warning);
        box-shadow: 0 4px 20px rgba(245, 158, 11, 0.15);
    }

    .tactical-card.success {
        border-left-color: var(--alert-safe);
        box-shadow: 0 4px 20px rgba(16, 185, 129, 0.15);
    }

    /* Monospace Tech Badges */
    .tactical-code {
        font-family: var(--tactical-mono);
        font-size: 0.82rem;
        background: #020617;
        color: #22D3EE;
        padding: 3px 8px;
        border-radius: 4px;
        border: 1px solid #1E293B;
    }

    /* Tactical Metric Display */
    .metric-hud-container {
        display: flex;
        flex-direction: column;
        background: #111C2E;
        border: 1px solid #1E293B;
        border-radius: 6px;
        padding: 12px 16px;
        position: relative;
        overflow: hidden;
    }

    .metric-hud-container::after {
        content: "";
        position: absolute;
        top: 0;
        right: 0;
        width: 12px;
        height: 12px;
        border-top: 2px solid var(--accent-cyan);
        border-right: 2px solid var(--accent-cyan);
    }

    .metric-label {
        font-family: var(--tactical-mono);
        font-size: 0.72rem;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    .metric-value {
        font-family: var(--tactical-title);
        font-size: 1.8rem;
        font-weight: 700;
        color: #FFFFFF;
        line-height: 1.2;
        margin: 4px 0;
    }

    .metric-delta {
        font-family: var(--tactical-mono);
        font-size: 0.75rem;
        font-weight: 600;
    }

    /* Status Pills */
    .status-pill {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 12px;
        font-family: var(--tactical-mono);
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
    }
    .pill-critical {
        background-color: rgba(239, 68, 68, 0.2);
        color: #F87171;
        border: 1px solid rgba(239, 68, 68, 0.5);
    }
    .pill-warning {
        background-color: rgba(245, 158, 11, 0.2);
        color: #FBBF24;
        border: 1px solid rgba(245, 158, 11, 0.5);
    }
    .pill-safe {
        background-color: rgba(16, 185, 129, 0.2);
        color: #34D399;
        border: 1px solid rgba(16, 185, 129, 0.5);
    }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(180deg, #1E293B, #0F172A) !important;
        border: 1px solid #06B6D4 !important;
        color: #22D3EE !important;
        font-family: var(--tactical-title) !important;
        font-weight: 600 !important;
        letter-spacing: 0.05em !important;
        text-transform: uppercase !important;
        border-radius: 4px !important;
        transition: all 0.2s ease !important;
        padding: 0.5rem 1rem !important;
    }

    .stButton>button:hover {
        background: #06B6D4 !important;
        color: #0F172A !important;
        box-shadow: 0 0 15px rgba(6, 182, 212, 0.5) !important;
        transform: translateY(-1px);
    }

    /* Primary CTA buttons */
    .stButton>button[kind="primary"] {
        background: linear-gradient(180deg, #0891B2, #0E7490) !important;
        color: #FFFFFF !important;
        border: 1px solid #22D3EE !important;
    }

    /* Tables & DataFrames */
    div[data-testid="stDataFrame"] {
        border: 1px solid #1E293B !important;
        border-radius: 6px !important;
        background: #0F172A !important;
    }

    /* Tab navigation */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #0B1120;
        padding: 6px;
        border-radius: 6px;
        border: 1px solid #1E293B;
    }

    .stTabs [data-baseweb="tab"] {
        font-family: var(--tactical-title) !important;
        font-weight: 600;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        border-radius: 4px;
        color: #94A3B8;
        padding: 6px 16px;
    }

    .stTabs [aria-selected="true"] {
        background-color: #1E293B !important;
        color: #22D3EE !important;
        border: 1px solid rgba(6, 182, 212, 0.4) !important;
    }

    /* Expanders */
    div[data-testid="stExpander"] {
        border: 1px solid #1E293B !important;
        background-color: #0F172A !important;
        border-radius: 6px !important;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def render_tactical_header(current_role="Analis Siber (Pussiberad)", threat_level="DEFCON 3"):
    """
    Renders tactical top telemetry bar with DEFCON level, live UTC/WIB timestamps, 
    and role indicator.
    """
    wib_tz = timezone(timedelta(hours=7))
    now_wib = datetime.now(wib_tz).strftime('%d %b %Y %H:%M:%S WIB')
    now_utc = datetime.now(timezone.utc).strftime('%H:%M:%S UTC')
    
    # DEFCON styling
    defcon_styles = {
        "DEFCON 1": ("#EF4444", "CRITICAL / IMMINENT THREAT"),
        "DEFCON 2": ("#F97316", "SEVERE COGNITIVE CAMPAIGN"),
        "DEFCON 3": ("#F59E0B", "ELEVATED CIB PROPAGATION"),
        "DEFCON 4": ("#3B82F6", "MODERATE / MONITORING"),
        "DEFCON 5": ("#10B981", "NORMAL READINESS")
    }
    
    accent_color, desc = defcon_styles.get(threat_level, ("#F59E0B", "ELEVATED"))
    
    col_l, col_r = st.columns([5, 7])
    with col_l:
        st.markdown(
            f'<div style="background:#0B1120; border:1px solid #334155; border-left:4px solid {accent_color}; padding:8px 14px; border-radius:6px; display:inline-flex; align-items:center; gap:10px; margin-bottom:12px;">'
            f'<span style="width:10px; height:10px; border-radius:50%; background:{accent_color}; box-shadow:0 0 8px {accent_color}; display:inline-block;"></span>'
            f'<span style="font-family:\'JetBrains Mono\', monospace; font-weight:800; color:{accent_color}; font-size:0.85rem; letter-spacing:0.05em;">THREAT: {threat_level}</span>'
            f'<span style="font-family:\'JetBrains Mono\', monospace; font-size:0.75rem; color:#CBD5E1;">[{desc}]</span>'
            f'</div>',
            unsafe_allow_html=True
        )
    with col_r:
        st.markdown(
            f'<div style="background:#0B1120; border:1px solid #334155; padding:8px 14px; border-radius:6px; display:flex; justify-content:flex-end; align-items:center; gap:18px; font-family:\'JetBrains Mono\', monospace; font-size:0.78rem; margin-bottom:12px;">'
            f'<div><span style="color:#06B6D4;">WIB:</span> <span style="color:#F8FAFC;">{now_wib}</span></div>'
            f'<div><span style="color:#06B6D4;">ZULU:</span> <span style="color:#F8FAFC;">{now_utc}</span></div>'
            f'<div style="background:#020617; border:1px solid #334155; padding:3px 8px; border-radius:4px; color:#38BDF8; font-size:0.72rem;">'
            f'<span style="opacity:0.7;">ROLE:</span> <b>{current_role}</b>'
            f'</div>'
            f'</div>',
            unsafe_allow_html=True
        )

def render_metric_card(label, value, delta=None, delta_color="normal", tag=None):
    """Renders a defense telemetry HUD metric card."""
    delta_style = ""
    if delta:
        d_color = "#10B981" if delta_color == "inverse" or "+" in str(delta) and delta_color != "danger" else "#EF4444"
        if delta_color == "danger":
            d_color = "#EF4444"
        elif delta_color == "success":
            d_color = "#10B981"
        elif delta_color == "warning":
            d_color = "#F59E0B"
        delta_style = f'<div class="metric-delta" style="color: {d_color}; margin-top: 4px;">{delta}</div>'
    
    tag_html = f'<span class="tactical-code" style="position: absolute; top: 8px; right: 8px; font-size: 0.65rem;">{tag}</span>' if tag else ""

    html = f"""
    <div class="metric-hud-container">
        {tag_html}
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        {delta_style}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
