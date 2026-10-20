"""
utils/data_generator.py - Comprehensive Tactical Data Generator for SENTINEL-AD
Generates realistic Indonesian defense disinformation data, CIB clusters,
multimodal mock signals, network graph topologies, and Kodam geospatial profiles.
"""

import random
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# Kodam Geographic Coordinates and Regional Commands
KODAM_REGIONS = {
    "Kodam I/Bukit Barisan": {"lat": 3.5952, "lon": 98.6722, "hq": "Medan, Sumatera Utara", "abbr": "I/BB"},
    "Kodam II/Sriwijaya": {"lat": -2.9909, "lon": 104.7565, "hq": "Palembang, Sumatera Selatan", "abbr": "II/SWJ"},
    "Kodam Jaya/Jayakarta": {"lat": -6.2088, "lon": 106.8456, "hq": "Jakarta Timur, DKI Jakarta", "abbr": "JAYA"},
    "Kodam III/Siliwangi": {"lat": -6.9175, "lon": 107.6191, "hq": "Bandung, Jawa Barat", "abbr": "III/SLW"},
    "Kodam IV/Diponegoro": {"lat": -7.0051, "lon": 110.4381, "hq": "Semarang, Jawa Tengah", "abbr": "IV/DIP"},
    "Kodam V/Brawijaya": {"lat": -7.2575, "lon": 112.7521, "hq": "Surabaya, Jawa Timur", "abbr": "V/BRW"},
    "Kodam VI/Mulawarman": {"lat": -1.2654, "lon": 116.8312, "hq": "Balikpapan, Kalimantan Timur (IKN)", "abbr": "VI/MLW"},
    "Kodam IX/Udayana": {"lat": -8.6705, "lon": 115.2126, "hq": "Denpasar, Bali & Nusa Tenggara", "abbr": "IX/UDY"},
    "Kodam XII/Tanjungpura": {"lat": -0.0263, "lon": 109.3425, "hq": "Kubu Raya, Kalimantan Barat", "abbr": "XII/TPR"},
    "Kodam XIII/Merdeka": {"lat": 1.4748, "lon": 124.8421, "hq": "Manado, Sulawesi Utara", "abbr": "XIII/MDK"},
    "Kodam XIV/Hasanuddin": {"lat": -5.1477, "lon": 119.4327, "hq": "Makassar, Sulawesi Selatan", "abbr": "XIV/HSN"},
    "Kodam XVI/Pattimura": {"lat": -3.6547, "lon": 128.1906, "hq": "Ambon, Maluku", "abbr": "XVI/PTM"},
    "Kodam XVII/Cenderawasih": {"lat": -2.5337, "lon": 140.7181, "hq": "Jayapura, Papua", "abbr": "XVII/CEN"},
    "Kodam XVIII/Kasuari": {"lat": -0.8615, "lon": 134.0620, "hq": "Manokwari, Papua Barat", "abbr": "XVIII/KSR"}
}

PRIMARY_INCIDENTS = [
    {
        "id": "INC-2026-ALPHA",
        "title": "AI Voice Clone Panglima TNI AD Isu SARA Perbatasan",
        "category": "Audio Deepfake / SARA Provocation",
        "level": "Kritis",
        "root_platform": "Telegram",
        "jump_sequence": ["Telegram", "X (Twitter)", "TikTok", "YouTube", "Media Daring"],
        "target_kodam": "Kodam XVII/Cenderawasih",
        "cib_cluster_size": 48,
        "sample_text": "Beredar rekaman audio berdurasi 42 detik menirukan suara KSAD terkait pengerahan satuan operasi dengan sentimen SARA di daerah rawan perbatasan. Terverifikasi kloning suara AI sintetik 94.2%.",
        "sentiment": -0.85
    },
    {
        "id": "INC-2026-BRAVO",
        "title": "Dokumen Surat Edaran Palsu Mutasi Pejabat Dispenad",
        "category": "Forged Military Document / CIB Disruption",
        "level": "Tinggi",
        "root_platform": "X (Twitter)",
        "jump_sequence": ["X (Twitter)", "Telegram", "Media Daring"],
        "target_kodam": "Kodam Jaya/Jayakarta",
        "cib_cluster_size": 32,
        "sample_text": "Beredar PDF berkop lambang Mabesad dan tanda tangan digital Danpuspomad palsu mengenai restrukturisasi mendadak perwira staf Dispenad. Font dan nomor registrasi Sprin tidak valid.",
        "sentiment": -0.65
    },
    {
        "id": "INC-2026-CHARLIE",
        "title": "Video Daur Ulang Latihan Militer 2021 yang Diklaim Konflik Baru",
        "category": "Visual Misinformation / Deceptive Context",
        "level": "Kritis",
        "root_platform": "TikTok",
        "jump_sequence": ["TikTok", "YouTube", "Telegram", "X (Twitter)"],
        "target_kodam": "Kodam VI/Mulawarman",
        "cib_cluster_size": 65,
        "sample_text": "Video manuver tank Leopard Yonkav 1 dilaporkan sebagai 'Pengerahan Darurat TNI AD Menuju Wilayah Perbatasan IKN'. Rekaman asli merupakan Latma 2021 di Baturaja.",
        "sentiment": -0.78
    },
    {
        "id": "INC-2026-DELTA",
        "title": "Disinformasi Pemotongan Tunjangan Kinerja Babinsa",
        "category": "Societal Cohesion Attack / Rumor",
        "level": "Sedang",
        "root_platform": "YouTube",
        "jump_sequence": ["YouTube", "Telegram", "TikTok"],
        "target_kodam": "Kodam IV/Diponegoro",
        "cib_cluster_size": 22,
        "sample_text": "Komentar massal dan konten clickbait YouTube mengklaim pemotongan remunerasi Bintara Pembina Desa hingga 40% demi efisiensi anggaran pengadaan pertahanan.",
        "sentiment": -0.52
    },
    {
        "id": "INC-2026-ECHO",
        "title": "Kampanye Botnet Separatisme Tagar Luar Negeri",
        "category": "Coordinated Inauthentic Behavior (CIB)",
        "level": "Tinggi",
        "root_platform": "X (Twitter)",
        "jump_sequence": ["X (Twitter)", "Telegram", "TikTok"],
        "target_kodam": "Kodam XVIII/Kasuari",
        "cib_cluster_size": 74,
        "sample_text": "Lonjakan anomali trafik 12,000 cuitan per jam menggunakan tagar bertema separatisme oleh akun-akun bot berumur kurang dari 7 hari dengan geolokasi VPN acak.",
        "sentiment": -0.91
    },
    {
        "id": "INC-2026-HASANUDDIN",
        "title": "Manipulasi Konteks Video Manuver Yonif Kodam XIV/Hasanuddin di Medsos Makassar",
        "category": "Visual Misinformation / Deceptive Context",
        "level": "Tinggi",
        "root_platform": "TikTok",
        "jump_sequence": ["TikTok", "X (Twitter)", "Instagram", "Media Daring"],
        "target_kodam": "Kodam XIV/Hasanuddin",
        "cib_cluster_size": 42,
        "sample_text": "Potongan video apel siaga Yonif 726/Tamalatea di Makassar dipelintir akun anonim TikTok @lensa.sulsel sebagai 'Pengamanan Darurat Konflik Tambang Sultra'. Terverifikasi konten daur ulang kegiatan HUT TNI.",
        "sentiment": -0.68
    }
]

def generate_threat_feed(n=50, seed=42):
    """
    Returns threat intelligence records.
    If session_state mode is 'live', returns real live articles and social intelligence.
    Otherwise returns tactical simulated baseline.
    """
    import streamlit as st
    try:
        if st.session_state.get("data_source_mode") == "live":
            if "live_feed_cache" in st.session_state and st.session_state["live_feed_cache"] is not None and len(st.session_state["live_feed_cache"]) > 0:
                return st.session_state["live_feed_cache"]
            from utils.live_osint import fetch_live_online_threats
            live_df = fetch_live_online_threats()
            if not live_df.empty:
                st.session_state["live_feed_cache"] = live_df
                return live_df
    except Exception:
        pass

    random.seed(seed)
    np.random.seed(seed)
    
    platforms = ["X (Twitter)", "Telegram", "TikTok", "YouTube", "Media Daring"]
    threat_levels = ["Kritis", "Tinggi", "Sedang", "Rendah"]
    statuses = ["Investigasi Pussiberad", "Deepfake Terdeteksi", "Terkonfirmasi Hoaks", "Tindakan SOAR Siap", "Klarifikasi Dispenad Dirilis"]
    kodam_names = list(KODAM_REGIONS.keys())
    
    records = []
    base_time = datetime.now() - timedelta(hours=24)
    
    for i in range(n):
        inc = random.choice(PRIMARY_INCIDENTS)
        time_offset = random.randint(5, 1440)
        timestamp = base_time + timedelta(minutes=time_offset)
        
        # Determine platform based on incident jump sequence or random
        platform = random.choice(inc["jump_sequence"])
        kodam = inc["target_kodam"] if random.random() > 0.3 else random.choice(kodam_names)
        threat_level = inc["level"] if random.random() > 0.25 else random.choice(threat_levels)
        virality = random.randint(45, 99) if threat_level in ["Kritis", "Tinggi"] else random.randint(15, 60)
        cib_score = random.randint(70, 98) if threat_level in ["Kritis", "Tinggi"] else random.randint(25, 65)
        
        author_types = {
            "X (Twitter)": [f"@op_ghost_{random.randint(100,999)}", f"@nusantara_alert_{random.randint(1,99)}", f"@makassar_terkini_{random.randint(10,88)}", f"@suara_celebes_{random.randint(1,50)}"],
            "Telegram": [f"TNI Watch ID Channel", f"Kanal Info Hankam Terbuka", f"Suara Kedaulatan Cyber", f"Intelijen Rakyat Sulsel"],
            "TikTok": [f"@fakta.tersembunyi.{random.randint(10,99)}", f"@militer.update.viral", f"@lensa.makassar.update", f"@sorot.hasanuddin"],
            "YouTube": [f"Channel Kabar Nusantara 24", f"Sorotan Militer Aktual", f"Garuda Celebes News", f"Kanal Opini Publik"],
            "Instagram": [f"@lensa.sulsel.terkini", f"@kabar_makassar_hari_ini", f"@sorot_angkatan_darat"],
            "Media Daring": [f"wartanews-portal.xyz", f"makassar-teropong.net", f"suara-rakyat-indonesia.online", f"celebes-aktual-news.com"]
        }
        
        author = random.choice(author_types[platform])
        
        records.append({
            "id": f"THREAT-2026-{1000 + i}",
            "incident_id": inc["id"],
            "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "datetime": timestamp,
            "platform": platform,
            "author": author,
            "headline": f"[{platform.upper()}] {inc['title']}",
            "text": inc["sample_text"] + f" (Deteksi simpul: {author})",
            "kodam": kodam,
            "threat_level": threat_level,
            "virality_score": virality,
            "cib_probability": cib_score,
            "sentiment_score": round(inc["sentiment"] + random.uniform(-0.1, 0.1), 2),
            "status": random.choice(statuses),
            "shares_count": random.randint(150, 15400),
            "amplification_nodes": random.randint(12, 180)
        })
        
    df = pd.DataFrame(records)
    df = df.sort_values(by="datetime", ascending=False).reset_index(drop=True)
    return df

def generate_kodam_geo_summary():
    """Generates summarized threat metrics per Kodam for geospatial map."""
    geo_data = []
    feed = generate_threat_feed(80)
    
    for kodam_name, coords in KODAM_REGIONS.items():
        kodam_threats = feed[feed["kodam"] == kodam_name]
        total_threats = len(kodam_threats)
        critical_count = len(kodam_threats[kodam_threats["threat_level"] == "Kritis"])
        high_count = len(kodam_threats[kodam_threats["threat_level"] == "Tinggi"])
        avg_cib = round(kodam_threats["cib_probability"].mean(), 1) if total_threats > 0 else 0
        
        top_incident = kodam_threats.iloc[0]["headline"] if total_threats > 0 else "Nihil Anomali Signifikan"
        
        # Color coding for markers
        if critical_count > 1 or total_threats >= 8:
            color = "#EF4444"  # Red
            status_desc = "STATUS: MERAH (Waspada Penuh)"
        elif high_count >= 1 or total_threats >= 4:
            color = "#F59E0B"  # Yellow/Orange
            status_desc = "STATUS: KUNING (Pemantauan Aktif)"
        else:
            color = "#10B981"  # Green
            status_desc = "STATUS: HIJAU (Kondusif)"
            
        geo_data.append({
            "kodam": kodam_name,
            "abbr": coords["abbr"],
            "lat": coords["lat"],
            "lon": coords["lon"],
            "hq": coords["hq"],
            "total_threats": total_threats,
            "critical_count": critical_count,
            "high_count": high_count,
            "avg_cib": avg_cib,
            "top_incident": top_incident,
            "marker_color": color,
            "status_desc": status_desc
        })
        
    return pd.DataFrame(geo_data)

def generate_cib_synchronized_clusters():
    """
    Generates CIB synchronized posting burst events (<60 seconds latency)
    between bot accounts with semantic similarity metrics.
    """
    base_t = datetime.now() - timedelta(minutes=45)
    
    cluster_a = []
    # Burst 1: Voice Clone audio drop
    usernames_a = [
        "@warga_waspada_01", "@nkri_bergerak_99", "@kabar_papua_rill", 
        "@patriot_digital_id", "@suara_kritis_timur", "@fakta_indonesia_now",
        "@cyber_nusantara_x", "@mata_perbatasan_ad"
    ]
    for i, user in enumerate(usernames_a):
        post_time = base_t + timedelta(seconds=i * random.randint(4, 9))  # Burst within 50s
        cluster_a.append({
            "account": user,
            "timestamp": post_time.strftime("%H:%M:%S.%f")[:-3],
            "post_interval_sec": random.randint(3, 8),
            "payload_text": "Beredar suara Panglima instruksikan siaga 1 konflik perbatasan! Bukti audio valid!",
            "hash_md5": "e99a18c428cb38d5f260853678922e03",
            "semantic_similarity": round(random.uniform(0.93, 0.99), 3),
            "account_age_days": random.randint(2, 14),
            "followers": random.randint(15, 80),
            "cluster": "Cluster Alpha-CIB (Audio Clone Drop)",
            "proxy_ip": f"194.26.{random.randint(10,250)}.{random.randint(2,250)} [TOR Exit Node]"
        })
        
    # Burst 2: Forged Dispenad letter
    cluster_b = []
    base_t2 = datetime.now() - timedelta(minutes=110)
    usernames_b = [
        "@dokumen_bocor_id", "@rahasia_mabes_01", "@opini_publik_jaya", 
        "@tribun_rakyat_24", "@update_militer_ri"
    ]
    for i, user in enumerate(usernames_b):
        post_time = base_t2 + timedelta(seconds=i * random.randint(5, 11))
        cluster_b.append({
            "account": user,
            "timestamp": post_time.strftime("%H:%M:%S.%f")[:-3],
            "post_interval_sec": random.randint(4, 10),
            "payload_text": "Surat edaran mutasi pejabat Dispenad resmi bocor. Ada pergeseran besar di Mabesad!",
            "hash_md5": "7d89ab56c12344ef8821098471bcca01",
            "semantic_similarity": round(random.uniform(0.91, 0.98), 3),
            "account_age_days": random.randint(5, 20),
            "followers": random.randint(30, 110),
            "cluster": "Cluster Bravo-CIB (Fake Memo Dispenad)",
            "proxy_ip": f"185.220.{random.randint(100,200)}.{random.randint(5,200)} [Data Center Proxy]"
        })
        
    return pd.DataFrame(cluster_a + cluster_b)

def generate_network_graph_data():
    """
    Generates network topology data for Social Network Analysis (SNA).
    Nodes categories:
    - Seed Account (Merah: #EF4444)
    - Amplifier Cluster (Oranye: #F97316)
    - Bridge Node (Kuning: #FBBF24)
    - Organic Audience (Abu-abu: #94A3B8)
    """
    nodes = [
        # Seed Accounts (Originator / Botmaster)
        {"id": "seed_01", "label": "Seed: @shadow_intel_id", "group": "Seed Account", "color": "#EF4444", "size": 35, "info": "Inisiator awal file audio clone di Telegram & X. Akun dibuat 4 hari lalu."},
        {"id": "seed_02", "label": "Seed: @leak_dokumen_ad", "group": "Seed Account", "color": "#EF4444", "size": 32, "info": "Penyebar perdana PDF Surat Edaran Dispenad Palsu via darknet mirror."},

        # Bridge Nodes (High betweenness centrality, bridging platforms)
        {"id": "bridge_01", "label": "Bridge: Channel 'Info Hankam ID'", "group": "Bridge Node", "color": "#FBBF24", "size": 28, "info": "Kanal Telegram dengan 45k subscriber. Mentransmisikan narasi ke grup publik WhatsApp & Facebook."},
        {"id": "bridge_02", "label": "Bridge: @portal_militer_viral", "group": "Bridge Node", "color": "#FBBF24", "size": 26, "info": "Akun agregator TikTok yang mendaur ulang audio Telegram menjadi video pendek bersponsor."},
        {"id": "bridge_03", "label": "Bridge: @media_independen_xyz", "group": "Bridge Node", "color": "#FBBF24", "size": 25, "info": "Situs berita abal-abal yang mengutip cuitan bot sebagai rujukan formal."},

        # Amplifier Clusters (Automated botnets & micro-influencers)
        {"id": "amp_01", "label": "Botnet Alpha-01", "group": "Amplifier Cluster", "color": "#F97316", "size": 18, "info": "Retweet otomatis dalam waktu 6 detik pasca postingan seed."},
        {"id": "amp_02", "label": "Botnet Alpha-02", "group": "Amplifier Cluster", "color": "#F97316", "size": 18, "info": "Penyebar cuplikan audio di komentar X."},
        {"id": "amp_03", "label": "Botnet Alpha-03", "group": "Amplifier Cluster", "color": "#F97316", "size": 18, "info": "Pemberi hashtag masif #TNIADSiaga1."},
        {"id": "amp_04", "label": "Botnet Bravo-01", "group": "Amplifier Cluster", "color": "#F97316", "size": 17, "info": "Spammer tangkapan layar PDF surat mutasi palsu."},
        {"id": "amp_05", "label": "Botnet Bravo-02", "group": "Amplifier Cluster", "color": "#F97316", "size": 17, "info": "Spammer forum online Kaskus & Quora."},
        {"id": "amp_06", "label": "Micro-Influencer @opini_kritis", "group": "Amplifier Cluster", "color": "#F97316", "size": 22, "info": "Akun opini bayaran dengan 12k followers."},
        {"id": "amp_07", "label": "Botnet Charlie-01", "group": "Amplifier Cluster", "color": "#F97316", "size": 17, "info": "Akun TikTok repost video latihan tank lama."},

        # Organic Audience (Unwitting citizens, affected public)
        {"id": "org_01", "label": "Warga_Netizen_JKT", "group": "Organic Audience", "color": "#94A3B8", "size": 12, "info": "Pengguna organik yang menanyakan kebenaran isu."},
        {"id": "org_02", "label": "Komunitas_Purnawirawan", "group": "Organic Audience", "color": "#94A3B8", "size": 14, "info": "Grup diskusi menuntut klarifikasi resmi dari Dispenad."},
        {"id": "org_03", "label": "Mahasiswa_Papua_ID", "group": "Organic Audience", "color": "#94A3B8", "size": 13, "info": "Menerima disinformasi dan terpapar sentimen ketegangan."},
        {"id": "org_04", "label": "Media_Nasional_Pers", "group": "Organic Audience", "color": "#94A3B8", "size": 15, "info": "Wartawan melakukan verifikasi ke Dispenad sebelum menerbitkan berita."},
        {"id": "org_05", "label": "Netizen_Surabaya", "group": "Organic Audience", "color": "#94A3B8", "size": 11, "info": "Membagikan ulang konten TikTok tanpa verifikasi."},
        {"id": "org_06", "label": "Akun_Pemerhati_Alutsista", "group": "Organic Audience", "color": "#94A3B8", "size": 14, "info": "Membantah video latihan lama namun tetap mengamplifikasi keyword."}
    ]
    
    edges = [
        # Seed to Amplifiers
        ("seed_01", "amp_01", 3), ("seed_01", "amp_02", 3), ("seed_01", "amp_03", 3),
        ("seed_02", "amp_04", 3), ("seed_02", "amp_05", 3),
        
        # Amplifiers to Bridges
        ("amp_01", "bridge_01", 4), ("amp_02", "bridge_01", 4),
        ("amp_03", "bridge_02", 5), ("amp_06", "bridge_02", 4),
        ("amp_04", "bridge_03", 3), ("amp_05", "bridge_03", 3),
        ("amp_07", "bridge_02", 5),

        # Bridges to Organic
        ("bridge_01", "org_01", 2), ("bridge_01", "org_02", 3),
        ("bridge_01", "org_03", 4), ("bridge_02", "org_03", 4),
        ("bridge_02", "org_05", 3), ("bridge_03", "org_04", 4),
        ("bridge_02", "org_06", 2),

        # Inter-organic discussion
        ("org_02", "org_04", 2), ("org_06", "org_01", 2)
    ]
    
    return nodes, edges

def get_multi_agent_personas():
    """Returns 10 distinct persona definitions for Cognitive Wargaming Sandbox."""
    return [
        {
            "id": "persona_1",
            "name": "Masyarakat Netral & Awam",
            "role": "General Public / Silent Majority",
            "bias": "Cenderung cemas terhadap isu perang/konflik; membutuhkan bahasa lugas, menenangkan, dan penjelasan bukti otentik.",
            "reaction_tendency": "Bila klarifikasi dingin/birokratis -> Masih bingung. Bila ada bukti perbandingan audio asli vs palsu -> Tenang dan percaya TNI AD.",
            "icon": "👥",
            "sensitivity": "Tinggi terhadap stabilitas harga & rasa aman"
        },
        {
            "id": "persona_2",
            "name": "Komunitas Pro-Pertahanan & Sahabat TNI",
            "role": "Organic Patriotic Advocates",
            "bias": "Mendukung institusi TNI AD, namun butuh materi infografis / talking point yang kuat untuk membantu meluruskan narasi di media sosial.",
            "reaction_tendency": "Siap mengamplifikasi rilis resmi Dispenad jika disajikan dalam format ringkas visual.",
            "icon": "🛡️",
            "sensitivity": "Membutuhkan amunisi argumen faktual cepat"
        },
        {
            "id": "persona_3",
            "name": "Kelompok Kritis & LSM Kebijakan Publik",
            "role": "Civil Society & Watchdogs",
            "bias": "Skeptis terhadap bantahan defensif satu arah. Menuntut transparansi investigasi forensik siber dan legalitas proses komando.",
            "reaction_tendency": "Akan mengkritik jika TNI AD terkesan reaktif atau menuduh tanpa bukti digital forensik.",
            "icon": "⚖️",
            "sensitivity": "Sangat peka terhadap kebebasan berpendapat & akuntabilitas"
        },
        {
            "id": "persona_4",
            "name": "Jurnalis Investigasi & Media Nasional Arus Utama",
            "role": "Mainstream Fact-Checking Journalists",
            "bias": "Netral, mematuhi KEJ (Kode Etik Jurnalistik), butuh konfirmasi resmi cepat dari Dispenad sebelum deadline cetak/online.",
            "reaction_tendency": "Bila Dispenad lambat merespons -> Mengutip sumber alternatif/rumor. Bila siaran pers cepat dengan bukti teknis -> Memuat bantahan hoaks secara berimbang.",
            "icon": "📰",
            "sensitivity": "Kecepatan pernyataan resmi Dispenad & akses narasumber"
        },
        {
            "id": "persona_5",
            "name": "Masyarakat Lokal Daerah Perbatasan / Wilayah Terdampak",
            "role": "Borderline Regional Population",
            "bias": "Sangat rentan terhadap rumor provokasi perbatasan; langsung merasakan psikologis ketegangan di lapangan.",
            "reaction_tendency": "Memerlukan kehadiran fisik babinsa/komandan setempat + pesan damai yang humanis dan merangkul tokoh adat.",
            "icon": "📍",
            "sensitivity": "Isu keamanan lokal, ketenangan ibadah, dan mata pencaharian"
        },
        {
            "id": "persona_6",
            "name": "Buzzer Lawan & Akun Proksi Eksternal",
            "role": "Hostile Disinformation Operatives",
            "bias": "Mencari celah kata, diksi emosional, atau kesalahan tata bahasa dalam klarifikasi untuk dipelintir menjadi serangan lanjutan (backfire effect).",
            "reaction_tendency": "Menyerang bila klarifikasi arogan atau defensif berlebihan. Mati kutu bila klarifikasi berbasis data audit forensik hash file.",
            "icon": "🤖",
            "sensitivity": "Mengeksploitasi blunder komunikasi institusi"
        },
        {
            "id": "persona_7",
            "name": "Generasi Muda & Netizen TikTok/Gen-Z",
            "role": "Digital Natives & Viral Amplifiers",
            "bias": "Minim membaca rilis formal PDF 3 lembar. Tertarik pada visual 'Side-by-side Debunk', meme edukasi, dan video pendek penjelasan mikro.",
            "reaction_tendency": "Bila klarifikasi kaku berbahasa kedinasan -> Diabaikan atau dijadikan bahan sarkasme. Bila format video debunk interaktif -> Cepat viral mendukung kebenaran.",
            "icon": "📱",
            "sensitivity": "Format konten (video pendek/reels, to-the-point)"
        },
        {
            "id": "persona_8",
            "name": "Keluarga Besar Tentara (KBT) & Purnawirawan",
            "role": "Veteran & Military Family Network",
            "bias": "Sangat peduli marwah pimpinan dan soliditas prajurit. Aktif menyebarkan informasi lewat grup WhatsApp keluarga.",
            "reaction_tendency": "Merasa lega jika pimpinan segera tampil memberikan arahan tegas yang menjaga martabat komando.",
            "icon": "🎖️",
            "sensitivity": "Wibawa Panglima dan hirarki rantai komando"
        },
        {
            "id": "persona_9",
            "name": "Pengamat Pertahanan & Akademisi Hankam",
            "role": "Defense Academics & Geopolitical Analysts",
            "bias": "Menganalisis aktor di balik layar (Camerawork, motif geopolitik, pola perang kognitif hibrida).",
            "reaction_tendency": "Mengapresiasi jika TNI AD mendemonstrasikan kapabilitas Cognitive Warfare & CIB Screener modern.",
            "icon": "🎓",
            "sensitivity": "Kedalaman metodologi deteksi & konteks doktrin pertahanan"
        },
        {
            "id": "persona_10",
            "name": "Mitra Lembaga Terkait (BSSN, Kominfo, Polri)",
            "role": "Inter-Agency Strategic Partners",
            "bias": "Membutuhkan data teknis (IP address, URL, Telegram channel ID, file hash) untuk eksekusi blokir taktis terpadu.",
            "reaction_tendency": "Langsung menindaklanjuti Takedown Dossier jika sesuai format standar interoperabilitas regulasi.",
            "icon": "🏢",
            "sensitivity": "Standar kelengkapan bukti hukum & forensik siber"
        }
    ]
