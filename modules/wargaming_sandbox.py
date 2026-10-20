"""
modules/wargaming_sandbox.py - Cognitive Wargaming & Multi-Agent Persona Sandbox
Simulates societal, media, hostile, and inter-agency cognitive reactions across 10 distinct personas before releasing public statements.
"""

import streamlit as st
import random
from utils.data_generator import get_multi_agent_personas

PRESET_STATEMENTS = {
    "Pilihan 1: Faktual & Transparan dengan Bukti Digital Forensik (Rekomendasi Pussiberad)": (
        "Mabes TNI AD menegaskan rekaman audio yang beredar mengatasnamakan pimpinan TNI AD adalah 100% kloning suara sintetik (AI deepfake) "
        "yang sengaja disebarkan oleh pihak tidak bertanggung jawab untuk memecah belah persatuan. Tim Pussiberad telah memverifikasi anomali "
        "frekuensi dan berkas dossier takedown telah dikoordinasikan bersama Kominfo serta BSSN. TNI AD tetap berkomitmen menjaga stabilitas dan kedamaian di perbatasan."
    ),
    "Pilihan 2: Defensif, Bernada Emosional & Menyerang (Risiko Tinggi Backfire)": (
        "Beredar fitnah keji murahan di media sosial yang menyerang institusi TNI AD! Siapapun yang menyebarkan rekaman suara tersebut adalah pengkhianat bangsa "
        "dan akan kami buru sampai ke lubang semut tanpa ampun. Jangan berani-berani memfitnah pimpinan kami atau menghadapi akibat hukum yang sangat berat!"
    ),
    "Pilihan 3: Birokratis Kaku & Normatif Tanpa Pembuktian Teknis": (
        "Sehubungan dengan adanya berita yang beredar di media daring, dengan ini disampaikan bahwa hal tersebut tidak benar dan tidak sesuai dengan prosedur kedinasan. "
        "Masyarakat diimbau untuk selalu bijak bermedia sosial dan menaati peraturan perundang-undangan yang berlaku. Demikian untuk menjadi maklum."
    )
}

def analyze_statement_cognitive_impact(text):
    """
    Simulates cognitive resonance, backfire probability, and per-persona reactions
    based on linguistic markers, fact-density, and emotional posture.
    """
    text_lower = text.lower()
    
    # Heuristics
    has_facts = any(w in text_lower for w in ["pussiberad", "deepfake", "kloning", "frekuensi", "dossier", "bukti", "kominfo", "bssn", "forensik", "faktual"])
    has_aggression = any(w in text_lower for w in ["fitnah keji", "lubang semut", "pengkhianat", "tanpa ampun", "murahan", "buru"])
    has_bureaucratic = any(w in text_lower for w in ["sehubungan", "dengan ini disampaikan", "menjadi maklum", "perundang-undangan"])
    
    if has_aggression:
        pos_sentiment = 24.0
        backfire_risk = 78.5
        overall_tone = "Agresif & Reaktif (Sangat Berisiko)"
        tone_color = "#EF4444"
        optimal_advice = "HINDARI DIKSI INI. Bahasa yang mengancam justru akan dieksploitasi oleh botnet lawan untuk membingkai aparat bersikap arogan. Ubah ke nada faktual dan dingin berbasis bukti forensik."
    elif has_facts:
        pos_sentiment = 86.5
        backfire_risk = 11.2
        overall_tone = "Taktis, Faktual & Kredibel (Sangat Optimal)"
        tone_color = "#10B981"
        optimal_advice = "DIREKOMENDASIKAN. Penggunaan bukti digital forensik dan keterlibatan BSSN/Kominfo melumpuhkan narasi buzzer lawan serta memberikan rasa aman kepada publik awam."
    elif has_bureaucratic:
        pos_sentiment = 48.0
        backfire_risk = 38.0
        overall_tone = "Birokratis & Normatif (Efektivitas Rendah)"
        tone_color = "#F59E0B"
        optimal_advice = "PERLU PERBAIKAN. Generasi muda (TikTok) dan media arus utama tidak terpuaskan dengan bahasa normatif. Sertakan visual perbandingan audio asli vs palsu."
    else:
        pos_sentiment = 55.0
        backfire_risk = 32.0
        overall_tone = "Netral Moderat"
        tone_color = "#3B82F6"
        optimal_advice = "Lengkapi dengan rincian teknis verifikasi forensik Pussiberad agar kredibilitas institusi terjaga maksimal."
        
    # Generate Reactions for each of the 10 personas
    personas = get_multi_agent_personas()
    reactions = []
    
    for p in personas:
        pid = p["id"]
        if pid == "persona_1": # Masyarakat Netral
            if has_facts:
                stance = "Lega & Percaya"; stance_color = "#10B981"
                quote = "Terima kasih atas klarifikasinya. Senang mendengar TNI AD cepat menjelaskan bahwa itu suara buatan AI."
            elif has_aggression:
                stance = "Cemas & Takut"; stance_color = "#EF4444"
                quote = "Kenapa bahasanya seram sekali ya? Apa situasinya memang sedang tegang di perbatasan?"
            else:
                stance = "Ragu-ragu"; stance_color = "#F59E0B"
                quote = "Hanya dibilang tidak benar, tapi tidak dijelaskan suara siapa yang sebenarnya beredar."

        elif pid == "persona_2": # Pro-Pertahanan
            if has_facts:
                stance = "Siap Amplifikasi"; stance_color = "#10B981"
                quote = "Sikap tegas dan cerdas! Kami siap bantu viralkan infografis sanggahan ini di grup relawan."
            elif has_aggression:
                stance = "Mendukung Emosional"; stance_color = "#F59E0B"
                quote = "Sikat habis pengacau keamanan! Tapi sebaiknya rilis data teknisnya juga biar netizen lain percaya."
            else:
                stance = "Menunggu Materi Visual"; stance_color = "#F59E0B"
                quote = "Mohon izin, kami butuh poster 'Hoaks Alert' resmi dari Dispenad untuk disebarkan di IG/FB."

        elif pid == "persona_3": # Kelompok Kritis / LSM
            if has_facts:
                stance = "Menghargai Transparansi"; stance_color = "#10B981"
                quote = "Langkah tepat menyertakan metodologi forensik audio dan melibatkan BSSN secara akuntabel."
            elif has_aggression:
                stance = "Kecam Ancaman"; stance_color = "#EF4444"
                quote = "Ancaman 'memburu sampai ke lubang semut' berpotensi mencederai iklim kebebasan berpendapat dan bertentangan dengan supremasi hukum."
            else:
                stance = "Skeptis"; stance_color = "#F59E0B"
                quote = "Bantahan normatif tanpa audit independen masih menyisakan tanda tanya besar."

        elif pid == "persona_4": # Jurnalis Investigasi
            if has_facts:
                stance = "Dapat Dikutip Lengkap"; stance_color = "#10B981"
                quote = "Kutipan sangat layak masuk 'Lead' berita. Data kloning suara 94% langsung kami muat dalam cek fakta media kami."
            elif has_aggression:
                stance = "Sensasional Framing"; stance_color = "#EF4444"
                quote = "Headline: 'TNI AD Naik Pitam! Ancam Pembocor Rekaman'. Diksi emosional mengalihkan substansi isu."
            else:
                stance = "Kurang Data"; stance_color = "#F59E0B"
                quote = "Pernyataan terlalu singkat. Kami butuh jadwal Doorstop dengan Kadispenad untuk konfirmasi detail."

        elif pid == "persona_5": # Warga Perbatasan
            if has_facts:
                stance = "Tenang & Kondusif"; stance_color = "#10B981"
                quote = "Puji syukur ternyata hanya hoaks rekaman palsu. Kami di kampung tetap beraktivitas normal bersama Babinsa."
            elif has_aggression:
                stance = "Panik & Bingung"; stance_color = "#EF4444"
                quote = "Mendengar kata-kata keras, warga sempat takut ada operasi penyisiran dadakan."
            else:
                stance = "Pasif Menunggu"; stance_color = "#94A3B8"
                quote = "Semoga aparat keamanan setempat segera mengadakan sosialisasi tatap muka langsung."

        elif pid == "persona_6": # Buzzer Lawan
            if has_facts:
                stance = "Gagal Eksploitasi (Lumpuh)"; stance_color = "#10B981"
                quote = "Sial, bukti forensik mereka terlalu kuat dan logis. Sulit membuat pelintiran narasi baru."
            elif has_aggression:
                stance = "Menyerang Balik (Backfire Target)"; stance_color = "#EF4444"
                quote = "Lihat respons mereka panik dan represif! Ini bukti mereka menyembunyikan sesuatu! Goreng terus tagar #ArogansiAparat!"
            else:
                stance = "Lanjut Pelintiran"; stance_color = "#EF4444"
                quote = "Bantahan mereka cuma formalitas template. Terus serang celah nomor surat mutasi!"

        elif pid == "persona_7": # Generasi Muda TikTok
            if has_facts:
                stance = "Resonansi Tinggi (Viral Positif)"; stance_color = "#10B981"
                quote = "Keren penjelasannya sci-fi banget, pake analisis AI segala. Bikin video POV debunk ah!"
            elif has_aggression:
                stance = "Dijadikan Meme Sarkas"; stance_color = "#EF4444"
                quote = "Waduh ngegas amat adminnya wkwk, masuk konten kompilasi netizen baper."
            else:
                stance = "Skip / Tidak Dibaca"; stance_color = "#94A3B8"
                quote = "TL;DR (terlalu panjang dan kaku kayak surat edaran RT)."

        elif pid == "persona_8": # Purnawirawan & KBT
            if has_facts:
                stance = "Bangga & Mantap"; stance_color = "#10B981"
                quote = "Komando menjaga martabat dengan kecanggihan modern. Rilis ini langsung kami forward ke grup WA letting."
            elif has_aggression:
                stance = "Cemas Citra Institusi"; stance_color = "#F59E0B"
                quote = "Tegas itu harus, tapi jangan sampai terpancing provokasi media sosial yang merugikan nama baik matra."
            else:
                stance = "Mendukung Normatif"; stance_color = "#3B82F6"
                quote = "Siap menjaga kekompakan prajurit di manapun bertugas."

        elif pid == "persona_9": # Pengamat Hankam
            if has_facts:
                stance = "Apresiasi Kapabilitas"; stance_color = "#10B981"
                quote = "Model komunikasi kognitif berbasis bukti teknis ini patut jadi standar doktrin perang informasi TNI masa depan."
            elif has_aggression:
                stance = "Kritik Strategis"; stance_color = "#EF4444"
                quote = "Komunikasi publik militer tergelincir dalam perangkap kognitif lawan yang memicu polarisasi sipil-militer."
            else:
                stance = "Catatan Konstruktif"; stance_color = "#F59E0B"
                quote = "Perlu peningkatan respon time dan integrasi ke dalam satu portal rujukan terpadu."

        else: # Mitra BSSN / Kominfo
            if has_facts:
                stance = "Sinkronisasi Takedown Cepat"; stance_color = "#10B981"
                quote = "Data verifikasi sinkron dengan telemetri SOC kami. Dossier takedown langsung kami eksekusi ke ISP & platform."
            elif has_aggression:
                stance = "Menunggu Kelengkapan Bukti"; stance_color = "#F59E0B"
                quote = "Pernyataan publik sudah keluar namun berkas bukti teknis URL dan hash belum lengkap untuk dasar regulasi blokir."
            else:
                stance = "Koordinasi Standar"; stance_color = "#3B82F6"
                quote = "Kami monitor dan siap mendukung langkah teknis lanjutan."

        reactions.append({
            "persona": p,
            "stance": stance,
            "stance_color": stance_color,
            "quote": quote
        })

    return pos_sentiment, backfire_risk, overall_tone, tone_color, optimal_advice, reactions

def render_wargaming_sandbox():
    """Renders the Cognitive Wargaming Persona Sandbox UI."""
    st.markdown("## 🧠 COGNITIVE WARGAMING & MULTI-AGENT PERSONA SANDBOX")
    st.markdown(
        "<p style='color: #94A3B8; font-size: 0.95rem; margin-top: -10px;'>"
        "Simulasi Uji Reaksi Psikososial & Resonansi Kognitif Terhadap 10 Multi-Agent Persona Sebelum Siaran Pers Diluncurkan."
        "</p>",
        unsafe_allow_html=True
    )
    
    # Preset Selector
    col_preset, col_clear = st.columns([10, 2])
    with col_preset:
        preset_key = st.selectbox(
            "⚡ Muat Contoh Draf Pernyataan Taktis (Preset Simulasi):",
            list(PRESET_STATEMENTS.keys())
        )
    with col_clear:
        st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
        if st.button("Reset Draf"):
            st.session_state["draft_text"] = ""
            
    initial_text = PRESET_STATEMENTS[preset_key]
    
    draft_input = st.text_area(
        "📝 Draf Pernyataan Klarifikasi / Counter-Narrative Dispenad:",
        value=initial_text,
        height=120,
        help="Ketik atau edit draf pernyataan resmi untuk diuji reaksi kognitifnya ke 10 segmen audiens."
    )
    
    col_btn, col_info = st.columns([4, 8])
    with col_btn:
        run_sim = st.button("🚀 Jalankan Simulasi 10+ Multi-Agent Persona", type="primary", use_container_width=True)
    with col_info:
        st.markdown(
            "<div style='font-family: JetBrains Mono; font-size: 0.78rem; color: #94A3B8; padding-top: 8px;'>"
            "Simulasi mengevaluasi sentimen, bias kognitif, kerentanan backfire, dan kepatuhan kode etik komunikasi pertahanan."
            "</div>",
            unsafe_allow_html=True
        )

    # Always compute analysis
    pos_sent, backfire_risk, tone_title, tone_color, advice, reactions = analyze_statement_cognitive_impact(draft_input)
    
    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
    
    # 1. High-Level Impact Telemetry
    st.markdown("### 📊 INDIKATOR DAMPAK KOGNITIF & RISIKO BACKFIRE")
    
    c1, c2, c3 = st.columns([4, 4, 4])
    with c1:
        st.markdown(
            f"""
            <div class="metric-hud-container" style="border-left: 3px solid #10B981;">
                <div class="metric-label">PROBABILITAS SENTIMEN POSITIF</div>
                <div class="metric-value" style="color: #34D399;">{pos_sent}%</div>
                <div class="metric-delta" style="color: #10B981;">Penerimaan Publik & Keyakinan Fakta</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with c2:
        risk_color = "#EF4444" if backfire_risk > 50 else ("#F59E0B" if backfire_risk > 25 else "#10B981")
        st.markdown(
            f"""
            <div class="metric-hud-container" style="border-left: 3px solid {risk_color};">
                <div class="metric-label">RISIKO EFEK BUMERANG (BACKFIRE)</div>
                <div class="metric-value" style="color: {risk_color};">{backfire_risk}%</div>
                <div class="metric-delta" style="color: {risk_color};">Potensi Serangan Balik / Boomerang Effect</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with c3:
        st.markdown(
            f"""
            <div class="metric-hud-container" style="border-left: 3px solid {tone_color};">
                <div class="metric-label">KLASIFIKASI NADA KOMUNIKASI</div>
                <div class="metric-value" style="font-size: 1.25rem; color: {tone_color}; padding-top: 5px;">{tone_title}</div>
                <div class="metric-delta" style="color: #94A3B8;">Rekomendasi Doktrin Komunikasi</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # 2. AI Optimal Tone Recommendation Box
    st.markdown(
        f"""
        <div class="tactical-card" style="border-left: 3px solid {tone_color}; padding: 14px 18px; margin-top: 15px;">
            <div style="font-family: 'JetBrains Mono'; font-weight: bold; color: {tone_color}; font-size: 0.85rem; margin-bottom: 4px;">
                💡 REKOMENDASI NADA OPTIMAL AI (STRATEGIC COGNITIVE ADVISOR):
            </div>
            <div style="font-size: 0.88rem; color: #F1F5F9; line-height: 1.4;">
                {advice}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 3. Grid of 10 Persona Reaction Cards
    st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
    st.markdown("### 👥 MATRIKS SIMULASI RESPON 10 MULTI-AGENT PERSONA")
    st.markdown(
        "<span style='font-family: JetBrains Mono; font-size: 0.8rem; color: #38BDF8;'>"
        "Evaluasi reaksi otomatis tiap segmen masyarakat sipil, pemerhati, media, hingga kelompok lawan."
        "</span>",
        unsafe_allow_html=True
    )
    
    # 2 Columns grid for 10 personas
    cols = st.columns(2)
    for idx, r in enumerate(reactions):
        p = r["persona"]
        col_target = cols[idx % 2]
        
        with col_target:
            card_html = f"""
            <div style="
                background: #111C2E;
                border: 1px solid #1E293B;
                border-top: 2px solid {r['stance_color']};
                border-radius: 6px;
                padding: 12px 16px;
                margin-bottom: 12px;
                min-height: 135px;
            ">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                    <div style="font-weight: 700; font-size: 0.88rem; color: #F8FAFC; display: flex; align-items: center; gap: 8px;">
                        <span>{p['icon']}</span>
                        <span>{p['name']}</span>
                    </div>
                    <span style="
                        font-family: 'JetBrains Mono';
                        font-size: 0.7rem;
                        font-weight: bold;
                        color: {r['stance_color']};
                        background: rgba(15, 23, 42, 0.8);
                        border: 1px solid {r['stance_color']};
                        padding: 2px 8px;
                        border-radius: 12px;
                    ">
                        {r['stance']}
                    </span>
                </div>
                <div style="font-size: 0.75rem; color: #94A3B8; margin-bottom: 6px;">
                    <i>Peran: {p['role']}</i> • <span style="color: #64748B;">Sensitivitas: {p['sensitivity']}</span>
                </div>
                <div style="
                    font-size: 0.8rem;
                    color: #E2E8F0;
                    background: #0B1120;
                    border-left: 2px solid {r['stance_color']};
                    padding: 8px 10px;
                    border-radius: 4px;
                    font-style: italic;
                ">
                    "{r['quote']}"
                </div>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)
