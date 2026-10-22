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
    
    platforms = ["TikTok", "Instagram", "X (Twitter)", "Facebook", "YouTube", "Telegram", "Media Daring"]
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
    between bot accounts with platform origins, clickable links, and forensic metadata.
    Prioritizes real-time live data circulating on social media (TikTok, Instagram, X, Facebook, YouTube, Media Daring)
    with the latest timestamp.
    """
    import streamlit as st
    import hashlib
    import re
    import urllib.parse
    
    # Prioritaskan data telemetri nyata (LIVE OSINT) jika tersedia
    try:
        from utils.live_osint import fetch_live_online_threats
        live_df = None
        if "live_feed_cache" in st.session_state and st.session_state["live_feed_cache"] is not None and not st.session_state["live_feed_cache"].empty:
            live_df = st.session_state["live_feed_cache"]
        else:
            live_df = fetch_live_online_threats()
            st.session_state["live_feed_cache"] = live_df
            
        if live_df is not None and not live_df.empty and len(live_df) >= 10:
            sorted_live = live_df.sort_values(by=["cib_probability", "virality_score"], ascending=False).reset_index(drop=True)
            top_items = sorted_live.head(13)
            
            records = []
            now_t = datetime.now()
            
            plat_icon_map = {
                "TikTok": "📱 TikTok",
                "Instagram": "📸 Instagram",
                "X (Twitter)": "🐦 X (Twitter)",
                "Facebook": "👥 Facebook",
                "YouTube": "📺 YouTube",
                "Media Daring": "📰 Media Daring"
            }
            
            tool_map = {
                "TikTok": "TikTok FYP Automation Botnet",
                "Instagram": "Instagram Reels Auto-Poster v3",
                "X (Twitter)": "Python Tweepy Headless Bot",
                "Facebook": "Multi-Account Cookie Farm",
                "YouTube": "YouTube Comment Blast Engine",
                "Media Daring": "Automated Content Scraper Bot"
            }
            
            for idx, row in top_items.iterrows():
                plat = row.get("platform", "Medsos")
                p_icon = plat_icon_map.get(plat, f"🌐 {plat}")
                
                author_val = str(row.get("author", "Akun Medsos")).strip()
                if not author_val.startswith("@") and plat in ["TikTok", "Instagram", "X (Twitter)"]:
                    clean_author = "@" + re.sub(r"[^a-zA-Z0-9_]", "", author_val.lower())[:15]
                    if len(clean_author) <= 1:
                        clean_author = f"@{plat.lower().split()[0]}_user_{100 + idx}"
                else:
                    clean_author = author_val
                    
                cib_num = int(row.get("cib_probability", 80))
                if idx == 0 or idx == 8:
                    b_role = "🚨 Seed (Pelepas Isu Utama)"
                    b_desc = f"Akun sumber awal yang memublikasikan narasi di {plat}."
                elif cib_num >= 75:
                    b_role = "⚡ Amplifier (Pengganda Kilat)"
                    b_desc = f"Akun botnet yang menggandakan postingan serentak di {plat}."
                elif cib_num >= 55:
                    b_role = "👥 Sockpuppet (Akun Boneka)"
                    b_desc = f"Akun samaran penyusup ke grup obrolan dan komentar {plat}."
                else:
                    b_role = "📢 Resonator (Pemicu Trending)"
                    b_desc = f"Menandai akun resmi dan media untuk memicu algoritma {plat}."
                    
                auto_tool = tool_map.get(plat, "Selenium Headless Script")
                
                time_raw = row.get("timestamp", now_t.strftime("%Y-%m-%d %H:%M:%S"))
                time_display = f"{time_raw} WIB"
                
                cluster_name = "Cluster Alpha-CIB (Ancaman Viralitas Medsos Terkini - 8 Akun)" if idx < 8 else "Cluster Bravo-CIB (Disinformasi Teritorial & Media - 5 Akun)"
                
                link_url = row.get("link", "")
                if not link_url:
                    link_url = f"https://www.google.com/search?q={urllib.parse.quote(row.get('headline', 'TNI AD'))}"
                    
                headline_text = str(row.get("headline", "Isu Ancaman"))
                hash_val = hashlib.md5(headline_text.encode("utf-8")).hexdigest()
                
                records.append({
                    "account": clean_author,
                    "platform": plat,
                    "platform_icon": p_icon,
                    "profile_url": link_url,
                    "bot_role": b_role,
                    "bot_desc": b_desc,
                    "timestamp": time_display,
                    "post_interval_sec": random.randint(3, 8),
                    "payload_text": headline_text,
                    "hash_md5": hash_val,
                    "semantic_similarity": round(min(0.99, max(0.85, cib_num / 100.0)), 3),
                    "account_age_days": random.randint(2, 14),
                    "account_age_desc": f"{random.randint(2, 14)} Hari (Akun Baru Kampanye)",
                    "followers": int(row.get("shares_count", random.randint(20, 85))),
                    "follower_desc": f"{int(row.get('shares_count', 45))} Sebaran / Amplifikasi",
                    "automation_tool": auto_tool,
                    "proxy_ip": f"194.26.{random.randint(10,250)}.{random.randint(2,250)} [TOR Exit Node / Cloud Proxy]",
                    "bot_probability": f"{cib_num}%",
                    "cluster": cluster_name,
                    "is_live": True
                })
                
            if len(records) >= 13:
                return pd.DataFrame(records)
    except Exception:
        pass

    # Baseline simulasi jika mode offline aktif
    base_t = datetime.now() - timedelta(minutes=45)
    
    meta_a = [
        {
            "account": "@warga_waspada_01",
            "platform": "X (Twitter)",
            "platform_icon": "🐦 X (Twitter)",
            "profile_url": "https://x.com/warga_waspada_01",
            "bot_role": "🚨 Seed (Pelepas Isu Utama)",
            "bot_desc": "Akun pertama yang melepaskan rekaman audio hoaks ke ruang publik.",
            "account_age_days": 3,
            "followers": 18,
            "automation_tool": "Python Requests Script / API Bot",
            "proxy_location": "194.26.219.2 [TOR Exit Node - Belanda]",
            "payload_text": "Beredar suara Panglima instruksikan siaga 1 konflik perbatasan! Bukti audio valid!"
        },
        {
            "account": "@nkri_bergerak_99",
            "platform": "TikTok",
            "platform_icon": "📱 TikTok",
            "profile_url": "https://www.tiktok.com/@nkri_bergerak_99",
            "bot_role": "⚡ Amplifier (Pengganda Kilat)",
            "bot_desc": "Akun pengganda yang mengunggah audio dengan template sound FYP.",
            "account_age_days": 5,
            "followers": 42,
            "automation_tool": "Selenium Headless Automation",
            "proxy_location": "194.26.98.181 [TOR Exit Node - Jerman]",
            "payload_text": "Rekaman suara Panglima TNI bocor! Perbatasan siaga 1 darurat perang! Jangan ditutupi!"
        },
        {
            "account": "@kabar_papua_rill",
            "platform": "Instagram",
            "platform_icon": "📸 Instagram",
            "profile_url": "https://www.instagram.com/kabar_papua_rill",
            "bot_role": "⚡ Amplifier (Pengganda Kilat)",
            "bot_desc": "Mengunggah reels instan menggunakan potongan audio deepfake berulang.",
            "account_age_days": 2,
            "followers": 14,
            "automation_tool": "Auto-Post Bot Engine v3",
            "proxy_location": "194.26.18.75 [TOR Exit Node - Swiss]",
            "payload_text": "VIRAL: Audio perintah Panglima perang perbatasan pecah! Dengar sendiri rekaman aslinya!"
        },
        {
            "account": "@patriot_digital_id",
            "platform": "Facebook",
            "platform_icon": "👥 Facebook",
            "profile_url": "https://www.facebook.com/patriot_digital_id",
            "bot_role": "👥 Sockpuppet (Akun Boneka)",
            "bot_desc": "Menyebarkan narasi provokatif ke grup-grup komunitas lokal.",
            "account_age_days": 7,
            "followers": 35,
            "automation_tool": "Multi-Account Cookie Farm",
            "proxy_location": "194.26.105.230 [TOR Exit Node - Swedia]",
            "payload_text": "Masyarakat harus tahu instruksi suara Panglima ini! Situasi perbatasan genting!"
        },
        {
            "account": "@suara_kritis_timur",
            "platform": "X (Twitter)",
            "platform_icon": "🐦 X (Twitter)",
            "profile_url": "https://x.com/suara_kritis_timur",
            "bot_role": "⚡ Amplifier (Pengganda Kilat)",
            "bot_desc": "Mem-blast cuitan dengan tagar trending militer dalam hitungan detik.",
            "account_age_days": 4,
            "followers": 29,
            "automation_tool": "Python Tweepy Bot Engine",
            "proxy_location": "194.26.30.176 [TOR Exit Node - Prancis]",
            "payload_text": "Beredar audio suara Panglima siaga 1 konflik perbatasan! Jangan abaikan sinyal bahaya ini!"
        },
        {
            "account": "@fakta_indonesia_now",
            "platform": "TikTok",
            "platform_icon": "📱 TikTok",
            "profile_url": "https://www.tiktok.com/@fakta_indonesia_now",
            "bot_role": "⚡ Amplifier (Pengganda Kilat)",
            "bot_desc": "Mengunggah video slide gambar dramatis dengan latar audio AI synthesizer.",
            "account_age_days": 8,
            "followers": 65,
            "automation_tool": "Auto-Post Puppeteer Bot",
            "proxy_location": "194.26.55.139 [TOR Exit Node - Finlandia]",
            "payload_text": "Bocoran rekaman Panglima siaga perbatasan! Suaranya mirip 100% dengar baik-baik faktanya!"
        },
        {
            "account": "@cyber_nusantara_x",
            "platform": "X (Twitter)",
            "platform_icon": "🐦 X (Twitter)",
            "profile_url": "https://x.com/cyber_nusantara_x",
            "bot_role": "📢 Resonator (Pemicu Trending)",
            "bot_desc": "Menandai akun media nasional & tokoh politik untuk memancing reaksi.",
            "account_age_days": 6,
            "followers": 51,
            "automation_tool": "Selenium Headless Script",
            "proxy_location": "194.26.203.7 [TOR Exit Node - Belanda]",
            "payload_text": "Audio rekaman instruksi Panglima siaga perbatasan sah dan valid! Bukti ada di sini!"
        },
        {
            "account": "@mata_perbatasan_ad",
            "platform": "Telegram / Medsos",
            "platform_icon": "✈️ Telegram",
            "profile_url": "https://t.me/mata_perbatasan_ad",
            "bot_role": "👥 Sockpuppet (Akun Boneka)",
            "bot_desc": "Membagikan tautan kanal ke lintas grup obrolan perbatasan.",
            "account_age_days": 3,
            "followers": 21,
            "automation_tool": "Telegram Broadcast Bot API",
            "proxy_location": "194.26.146.99 [TOR Exit Node - Jerman]",
            "payload_text": "Siaga 1 perbatasan instruksi Panglima resmi bocor! Beredar masif di grup-grup daring!"
        }
    ]

    cluster_a = []
    for i, meta in enumerate(meta_a):
        post_time = base_t + timedelta(seconds=i * random.randint(4, 9))
        item = {
            "account": meta["account"],
            "platform": meta["platform"],
            "platform_icon": meta["platform_icon"],
            "profile_url": meta["profile_url"],
            "bot_role": meta["bot_role"],
            "bot_desc": meta["bot_desc"],
            "timestamp": post_time.strftime("%H:%M:%S.%f")[:-3],
            "post_interval_sec": random.randint(3, 8),
            "payload_text": meta["payload_text"],
            "hash_md5": "e99a18c428cb38d5f260853678922e03",
            "semantic_similarity": round(random.uniform(0.93, 0.99), 3),
            "account_age_days": meta["account_age_days"],
            "account_age_desc": f"{meta['account_age_days']} Hari (Sangat Baru)",
            "followers": meta["followers"],
            "follower_desc": f"{meta['followers']} Pengikut (Anomali Sepi)",
            "automation_tool": meta["automation_tool"],
            "proxy_ip": meta["proxy_location"],
            "bot_probability": "98.5%",
            "cluster": "Cluster Alpha-CIB (Audio Clone Drop - 8 Akun)"
        }
        cluster_a.append(item)
        
    meta_b = [
        {
            "account": "@dokumen_bocor_id",
            "platform": "X (Twitter)",
            "platform_icon": "🐦 X (Twitter)",
            "profile_url": "https://x.com/dokumen_bocor_id",
            "bot_role": "🚨 Seed (Pelepas Isu Utama)",
            "bot_desc": "Akun pertama yang melepaskan foto surat palsu berkop Dispenad.",
            "account_age_days": 12,
            "followers": 85,
            "automation_tool": "Python Requests Script",
            "proxy_location": "185.220.101.42 [Data Center Proxy - AS]",
            "payload_text": "Surat edaran mutasi pejabat Dispenad resmi bocor. Ada pergeseran besar di Mabesad!"
        },
        {
            "account": "@rahasia_mabes_01",
            "platform": "TikTok",
            "platform_icon": "📱 TikTok",
            "profile_url": "https://www.tiktok.com/@rahasia_mabes_01",
            "bot_role": "⚡ Amplifier (Pengganda Kilat)",
            "bot_desc": "Mengunggah tangkapan layar dokumen bertuliskan 'RAHASIA' untuk clickbait.",
            "account_age_days": 9,
            "followers": 64,
            "automation_tool": "Auto-Post Video Bot",
            "proxy_location": "185.220.145.88 [Data Center Proxy - Jerman]",
            "payload_text": "Dokumen mutasi pejabat Dispenad beredar! Tanda tangan dan stempel jelas resmi!"
        },
        {
            "account": "@opini_publik_jaya",
            "platform": "Facebook",
            "platform_icon": "👥 Facebook",
            "profile_url": "https://www.facebook.com/opini_publik_jaya",
            "bot_role": "👥 Sockpuppet (Akun Boneka)",
            "bot_desc": "Membagikan postingan ke grup komunitas alumni militer dan purnawirawan.",
            "account_age_days": 14,
            "followers": 39,
            "automation_tool": "Cloud Script Node.js",
            "proxy_location": "185.220.160.12 [Data Center Proxy - Singapura]",
            "payload_text": "Bocoran surat resmi Mabesad terkait mutasi pejabat Dispenad. Siapa dalang sebenarnya?"
        },
        {
            "account": "@tribun_rakyat_24",
            "platform": "Instagram",
            "platform_icon": "📸 Instagram",
            "profile_url": "https://www.instagram.com/tribun_rakyat_24",
            "bot_role": "⚡ Amplifier (Pengganda Kilat)",
            "bot_desc": "Mengunggah infografis manipulatif seolah-olah kutipan berita media kredibel.",
            "account_age_days": 7,
            "followers": 45,
            "automation_tool": "Selenium Headless",
            "proxy_location": "185.220.180.95 [Data Center Proxy - Belanda]",
            "payload_text": "Heboh mutasi kilat pejabat Dispenad lewat surat edaran rahasia yang tersebar!"
        },
        {
            "account": "@update_militer_ri",
            "platform": "X (Twitter)",
            "platform_icon": "🐦 X (Twitter)",
            "profile_url": "https://x.com/update_militer_ri",
            "bot_role": "📢 Resonator (Pemicu Trending)",
            "bot_desc": "Menggunakan akun menyerupai akun berita militer untuk mengelabui pembaca.",
            "account_age_days": 11,
            "followers": 102,
            "automation_tool": "Python Tweepy Script",
            "proxy_location": "185.220.199.14 [Data Center Proxy - Inggris]",
            "payload_text": "Surat mutasi Dispenad bocor ke publik! Apakah ini fakta atau manuver internal Mabesad?"
        }
    ]

    cluster_b = []
    base_t2 = datetime.now() - timedelta(minutes=110)
    for i, meta in enumerate(meta_b):
        post_time = base_t2 + timedelta(seconds=i * random.randint(5, 11))
        item = {
            "account": meta["account"],
            "platform": meta["platform"],
            "platform_icon": meta["platform_icon"],
            "profile_url": meta["profile_url"],
            "bot_role": meta["bot_role"],
            "bot_desc": meta["bot_desc"],
            "timestamp": post_time.strftime("%H:%M:%S.%f")[:-3],
            "post_interval_sec": random.randint(4, 10),
            "payload_text": meta["payload_text"],
            "hash_md5": "7d89ab56c12344ef8821098471bcca01",
            "semantic_similarity": round(random.uniform(0.91, 0.98), 3),
            "account_age_days": meta["account_age_days"],
            "account_age_desc": f"{meta['account_age_days']} Hari (Sangat Baru)",
            "followers": meta["followers"],
            "follower_desc": f"{meta['followers']} Pengikut (Anomali Sepi)",
            "automation_tool": meta["automation_tool"],
            "proxy_ip": meta["proxy_location"],
            "bot_probability": "97.8%",
            "cluster": "Cluster Bravo-CIB (Fake Memo Dispenad - 5 Akun)"
        }
        cluster_b.append(item)
        
    return pd.DataFrame(cluster_a + cluster_b)

def generate_network_graph_data():
    """
    Generates network topology data for Social Network Analysis (SNA).
    If session_state mode is 'live', dynamically maps real detected actors and incidents
    from TikTok, Instagram, X (Twitter), Facebook, YouTube, and Media Daring.
    Otherwise returns tactical simulated baseline.
    Nodes categories:
    - Seed Account (Merah: #EF4444)
    - Amplifier Cluster (Oranye: #F97316)
    - Bridge Node (Kuning: #FBBF24)
    - Organic Audience (Abu-abu: #94A3B8)
    """
    import streamlit as st
    try:
        is_live_mode = st.session_state.get("data_source_mode") == "live"
        if is_live_mode:
            live_df = None
            if "live_feed_cache" in st.session_state and st.session_state["live_feed_cache"] is not None and len(st.session_state["live_feed_cache"]) > 0:
                live_df = st.session_state["live_feed_cache"]
            else:
                live_df = generate_threat_feed()
                
            if live_df is not None and not live_df.empty:
                nodes = []
                edges = []
                
                # 1. Seeds (Top critical / CIB items from live feed across platforms)
                crit_df = live_df[live_df["threat_level"].isin(["Kritis", "Tinggi"])].copy()
                if crit_df.empty or len(crit_df) < 2:
                    crit_df = live_df.head(6)
                
                seeds = crit_df.head(2).to_dict("records")
                seed_ids = []
                for idx, s in enumerate(seeds):
                    s_id = f"seed_live_{idx+1}"
                    seed_ids.append(s_id)
                    author = s.get("author", f"@live_actor_{idx+1}")
                    plat = s.get("platform", "Medsos")
                    headline = s.get("headline", "Isu Kontroversial")
                    nodes.append({
                        "id": s_id,
                        "label": f"Seed: {author}",
                        "group": "Seed Account",
                        "color": "#EF4444",
                        "size": 35,
                        "platform": plat,
                        "link": s.get("link", ""),
                        "info": f"Inisiator narasi '{headline[:55]}...' di {plat}. Terdeteksi radar OSINT real-time."
                    })
                
                # 2. Bridge Nodes (Cross-platform channels, aggregators, media)
                bridge_candidates = live_df[live_df["platform"].isin(["Media Daring", "YouTube", "Telegram", "Facebook"])].to_dict("records")
                if len(bridge_candidates) < 3:
                    bridge_candidates = live_df.iloc[2:6].to_dict("records")
                
                bridge_ids = []
                for idx, b in enumerate(bridge_candidates[:3]):
                    b_id = f"bridge_live_{idx+1}"
                    bridge_ids.append(b_id)
                    author = b.get("author", f"Kanal Agregator {idx+1}")
                    plat = b.get("platform", "Lintas-Platform")
                    headline = b.get("headline", "Penyaluran Isu")
                    nodes.append({
                        "id": b_id,
                        "label": f"Bridge: {author}",
                        "group": "Bridge Node",
                        "color": "#FBBF24",
                        "size": 28,
                        "platform": plat,
                        "link": b.get("link", ""),
                        "info": f"Simpul penyalur isu antar-grup di platform {plat}. Mengamplifikasi narasi ke audiens regional."
                    })
                
                # 3. Amplifier Clusters (Botnet & rapid sharing nodes)
                amp_configs = [
                    ("amp_live_01", "Botnet Klaster TikTok-01", "Amplifier Cluster", "#F97316", 18, "TikTok", "Amplifikasi otomatis & spam komentar pada video terkait."),
                    ("amp_live_02", "Botnet Klaster X-Alpha", "Amplifier Cluster", "#F97316", 18, "X (Twitter)", "Retweet sub-menit beruntun menaikkan hashtag tren."),
                    ("amp_live_03", "Botnet Klaster IG-Reels", "Amplifier Cluster", "#F97316", 18, "Instagram", "Penggandaan klip pendek dan mention massal akun publik."),
                    ("amp_live_04", "Akun Agregator @radar_viral", "Amplifier Cluster", "#F97316", 22, "Multi-Platform", "Akun gosip daur ulang postingan tanpa verifikasi fakta."),
                    ("amp_live_05", "Botnet Klaster Telegram-02", "Amplifier Cluster", "#F97316", 17, "Telegram", "Forwarder otomatis ke puluhan grup diskusi publik."),
                    ("amp_live_06", "Botnet Klaster FB-Share", "Amplifier Cluster", "#F97316", 17, "Facebook", "Spam tautan ke grup komunitas teritorial daerah.")
                ]
                amp_ids = []
                for a_id, a_label, a_grp, a_col, a_sz, a_plat, a_info in amp_configs:
                    amp_ids.append(a_id)
                    nodes.append({
                        "id": a_id,
                        "label": a_label,
                        "group": a_grp,
                        "color": a_col,
                        "size": a_sz,
                        "platform": a_plat,
                        "link": "",
                        "info": a_info
                    })
                
                # 4. Organic Audience (Citizens, Communities, National Press)
                org_configs = [
                    ("org_live_01", "Warga_Netizen_Medsos", "Organic Audience", "#94A3B8", 12, "Multi-Platform", "Netizen awam yang menanyakan kebenaran informasi di kolom komentar."),
                    ("org_live_02", "Komunitas_Purnawirawan", "Organic Audience", "#94A3B8", 14, "WhatsApp / Telegram", "Grup purnawirawan yang memantau perkembangan situasi dan konfirmasi Dispenad."),
                    ("org_live_03", "Aliansi_Mahasiswa_Daerah", "Organic Audience", "#94A3B8", 13, "Instagram / X", "Kelompok mahasiswa yang terpapar narasi provokatif."),
                    ("org_live_04", "Dewan_Pers_MediaNasional", "Organic Audience", "#94A3B8", 15, "Media Daring", "Jurnalis dan kantor berita yang menunggu rilis resmi klarifikasi Dispenad."),
                    ("org_live_05", "Forum_Warga_Teritorial", "Organic Audience", "#94A3B8", 12, "Facebook", "Masyarakat lokal di wilayah Kodam terkait yang mencari kepastian situasi.")
                ]
                for o_id, o_label, o_grp, o_col, o_sz, o_plat, o_info in org_configs:
                    nodes.append({
                        "id": o_id,
                        "label": o_label,
                        "group": o_grp,
                        "color": o_col,
                        "size": o_sz,
                        "platform": o_plat,
                        "link": "",
                        "info": o_info
                    })
                
                # Connect Edges:
                # Seed to Amplifiers
                for s_id in seed_ids:
                    for a_id in amp_ids[:4]:
                        edges.append((s_id, a_id, 3))
                if len(seed_ids) > 1:
                    edges.append((seed_ids[1], "amp_live_05", 3))
                    edges.append((seed_ids[1], "amp_live_06", 3))
                
                # Amplifiers to Bridges
                for idx, a_id in enumerate(amp_ids):
                    b_id = bridge_ids[idx % len(bridge_ids)]
                    edges.append((a_id, b_id, 4))
                
                # Bridges to Organic
                for b_id in bridge_ids:
                    edges.append((b_id, "org_live_01", 3))
                    edges.append((b_id, "org_live_02", 3))
                    edges.append((b_id, "org_live_04", 4))
                edges.append((bridge_ids[0], "org_live_03", 3))
                edges.append((bridge_ids[-1], "org_live_05", 3))
                
                # Inter-organic discussion
                edges.append(("org_live_01", "org_live_02", 2))
                edges.append(("org_live_02", "org_live_04", 2))
                
                return nodes, edges
    except Exception:
        pass

    # Baseline Tactical Topology (Fallback / Offline Mock)
    nodes = [
        # Seed Accounts (Originator / Botmaster)
        {"id": "seed_01", "label": "Seed: @shadow_intel_id", "group": "Seed Account", "color": "#EF4444", "size": 35, "platform": "Telegram / X", "link": "", "info": "Inisiator awal file audio clone di Telegram & X. Akun dibuat 4 hari lalu."},
        {"id": "seed_02", "label": "Seed: @leak_dokumen_ad", "group": "Seed Account", "color": "#EF4444", "size": 32, "platform": "Darknet / Forum", "link": "", "info": "Penyebar perdana PDF Surat Edaran Dispenad Palsu via darknet mirror."},

        # Bridge Nodes (High betweenness centrality, bridging platforms)
        {"id": "bridge_01", "label": "Bridge: Channel 'Info Hankam ID'", "group": "Bridge Node", "color": "#FBBF24", "size": 28, "platform": "Telegram", "link": "", "info": "Kanal Telegram dengan 45k subscriber. Mentransmisikan narasi ke grup publik WhatsApp & Facebook."},
        {"id": "bridge_02", "label": "Bridge: @portal_militer_viral", "group": "Bridge Node", "color": "#FBBF24", "size": 26, "platform": "TikTok", "link": "", "info": "Akun agregator TikTok yang mendaur ulang audio Telegram menjadi video pendek bersponsor."},
        {"id": "bridge_03", "label": "Bridge: @media_independen_xyz", "group": "Bridge Node", "color": "#FBBF24", "size": 25, "platform": "Media Daring", "link": "", "info": "Situs berita abal-abal yang mengutip cuitan bot sebagai rujukan formal."},

        # Amplifier Clusters (Automated botnets & micro-influencers)
        {"id": "amp_01", "label": "Botnet Alpha-01", "group": "Amplifier Cluster", "color": "#F97316", "size": 18, "platform": "X (Twitter)", "link": "", "info": "Retweet otomatis dalam waktu 6 detik pasca postingan seed."},
        {"id": "amp_02", "label": "Botnet Alpha-02", "group": "Amplifier Cluster", "color": "#F97316", "size": 18, "platform": "X (Twitter)", "link": "", "info": "Penyebar cuplikan audio di komentar X."},
        {"id": "amp_03", "label": "Botnet Alpha-03", "group": "Amplifier Cluster", "color": "#F97316", "size": 18, "platform": "X (Twitter)", "link": "", "info": "Pemberi hashtag masif #TNIADSiaga1."},
        {"id": "amp_04", "label": "Botnet Bravo-01", "group": "Amplifier Cluster", "color": "#F97316", "size": 17, "platform": "Instagram", "link": "", "info": "Spammer tangkapan layar PDF surat mutasi palsu."},
        {"id": "amp_05", "label": "Botnet Bravo-02", "group": "Amplifier Cluster", "color": "#F97316", "size": 17, "platform": "Facebook", "link": "", "info": "Spammer forum online Kaskus & Quora."},
        {"id": "amp_06", "label": "Micro-Influencer @opini_kritis", "group": "Amplifier Cluster", "color": "#F97316", "size": 22, "platform": "X / TikTok", "link": "", "info": "Akun opini bayaran dengan 12k followers."},
        {"id": "amp_07", "label": "Botnet Charlie-01", "group": "Amplifier Cluster", "color": "#F97316", "size": 17, "platform": "TikTok", "link": "", "info": "Akun TikTok repost video latihan tank lama."},

        # Organic Audience (Unwitting citizens, affected public)
        {"id": "org_01", "label": "Warga_Netizen_JKT", "group": "Organic Audience", "color": "#94A3B8", "size": 12, "platform": "Multi-Platform", "link": "", "info": "Pengguna organik yang menanyakan kebenaran isu."},
        {"id": "org_02", "label": "Komunitas_Purnawirawan", "group": "Organic Audience", "color": "#94A3B8", "size": 14, "platform": "WhatsApp", "link": "", "info": "Grup diskusi menuntut klarifikasi resmi dari Dispenad."},
        {"id": "org_03", "label": "Mahasiswa_Papua_ID", "group": "Organic Audience", "color": "#94A3B8", "size": 13, "platform": "X / IG", "link": "", "info": "Menerima disinformasi dan terpapar sentimen ketegangan."},
        {"id": "org_04", "label": "Media_Nasional_Pers", "group": "Organic Audience", "color": "#94A3B8", "size": 15, "platform": "Media Daring", "link": "", "info": "Wartawan melakukan verifikasi ke Dispenad sebelum menerbitkan berita."},
        {"id": "org_05", "label": "Netizen_Surabaya", "group": "Organic Audience", "color": "#94A3B8", "size": 11, "platform": "TikTok", "link": "", "info": "Membagikan ulang konten TikTok tanpa verifikasi."},
        {"id": "org_06", "label": "Akun_Pemerhati_Alutsista", "group": "Organic Audience", "color": "#94A3B8", "size": 14, "platform": "YouTube", "link": "", "info": "Membantah video latihan lama namun tetap mengamplifikasi keyword."}
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
