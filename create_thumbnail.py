"""
create_thumbnail.py - Generates official 1200x630 px Thumbnail for Kartika Cyber Hackathon 2026.
Strictly adheres to:
- Dimensions: 1200 x 630 pixels
- Formats: JPG, PNG, and WebP
- Size limit: < 500 KB
- High-contrast defense typography, military HUD badges, and 27 Kodam cognitive defense credentials.
"""

import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def create_hackathon_thumbnail():
    width = 1200
    height = 630
    
    # 1. Base Image - Tactical Command Center
    art_path = r"C:\Users\User\.gemini\antigravity-ide\brain\b7fe58a5-1462-4444-a83d-1511705a2fbb\sentinel_art_1792848486787.jpg"
    
    if os.path.exists(art_path):
        base_img = Image.open(art_path).convert("RGBA")
        # Resize & center-crop to 1200x630
        art_w, art_h = base_img.size
        target_ratio = width / height
        art_ratio = art_w / art_h
        
        if art_ratio > target_ratio:
            new_w = int(art_h * target_ratio)
            left = (art_w - new_w) // 2
            base_img = base_img.crop((left, 0, left + new_w, art_h))
        else:
            new_h = int(art_w / target_ratio)
            top = (art_h - new_h) // 2
            base_img = base_img.crop((0, top, art_w, top + new_h))
            
        base_img = base_img.resize((width, height), Image.Resampling.LANCZOS)
    else:
        base_img = Image.new("RGBA", (width, height), color=(11, 17, 32, 255))
        
    # 2. Gradient Vignette / Dark Glass Overlay for Text Readability
    overlay = Image.new("RGBA", (width, height), color=(0, 0, 0, 0))
    d_overlay = ImageDraw.Draw(overlay)
    
    # Left-to-right deep dark blue gradient (#070D1A)
    for x in range(width):
        p = x / width
        if p < 0.45:
            alpha = int(245 - p * 30) # Solid dark on left
        elif p < 0.75:
            alpha = int(230 - (p - 0.45) * (180 / 0.30)) # Smooth fade
        else:
            alpha = int(50 - (p - 0.75) * (40 / 0.25)) # Subtle tint over map
        alpha = max(10, min(252, alpha))
        d_overlay.line([(x, 0), (x, height)], fill=(7, 13, 26, alpha))
        
    # Top and bottom dark edge vignettes
    for y in range(80):
        alpha = int(180 * (1 - y / 80))
        d_overlay.line([(0, y), (width, y)], fill=(4, 8, 16, alpha))
    for y in range(height - 80, height):
        alpha = int(220 * ((y - (height - 80)) / 80))
        d_overlay.line([(0, y), (width, y)], fill=(4, 8, 16, alpha))
        
    # Composite overlay
    canvas = Image.alpha_composite(base_img, overlay)
    draw = ImageDraw.Draw(canvas)
    
    # 3. Fonts
    font_bahn_large = ImageFont.truetype(r"C:\Windows\Fonts\bahnschrift.ttf", 52)
    font_bahn_title = ImageFont.truetype(r"C:\Windows\Fonts\bahnschrift.ttf", 20)
    font_bahn_h2 = ImageFont.truetype(r"C:\Windows\Fonts\bahnschrift.ttf", 15)
    font_bahn_bold = ImageFont.truetype(r"C:\Windows\Fonts\bahnschrift.ttf", 13)
    font_bahn_regular = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 11)
    font_mono = ImageFont.truetype(r"C:\Windows\Fonts\consola.ttf", 11)
    font_badge = ImageFont.truetype(r"C:\Windows\Fonts\bahnschrift.ttf", 11)
    
    # 4. Tactical Frame & Grid Lines
    draw.rectangle([14, 14, width - 15, height - 15], outline=(30, 41, 59, 180), width=1)
    draw.rectangle([18, 18, width - 19, height - 19], outline=(6, 182, 212, 60), width=1)
    
    # Corner tactical brackets (Cyan accent)
    bracket_len = 24
    c_color = (6, 182, 212, 220)
    # Top-Left
    draw.line([(18, 18), (18 + bracket_len, 18)], fill=c_color, width=2)
    draw.line([(18, 18), (18, 18 + bracket_len)], fill=c_color, width=2)
    # Top-Right
    draw.line([(width - 19, 18), (width - 19 - bracket_len, 18)], fill=c_color, width=2)
    draw.line([(width - 19, 18), (width - 19, 18 + bracket_len)], fill=c_color, width=2)
    # Bottom-Left
    draw.line([(18, height - 19), (18 + bracket_len, height - 19)], fill=c_color, width=2)
    draw.line([(18, height - 19), (18, height - 19 - bracket_len)], fill=c_color, width=2)
    # Bottom-Right
    draw.line([(width - 19, height - 19), (width - 19 - bracket_len, height - 19)], fill=c_color, width=2)
    draw.line([(width - 19, height - 19), (width - 19, height - 19 - bracket_len)], fill=c_color, width=2)

    # 5. HEADER BAR: Event Tag & Classification
    top_y = 36
    event_text = "KARTIKA CYBER HACKATHON 2026 // KATEGORI 04: SIBER SOSIAL"
    draw.rounded_rectangle([48, top_y, 450, top_y + 24], radius=4, fill=(220, 38, 38, 220), outline=(239, 68, 68, 255), width=1)
    draw.text((58, top_y + 5), event_text, font=font_badge, fill=(255, 255, 255))
    
    user_text = "DOKTRIN: PUSSIBERAD • DISPENAD • SINTELAD TNI AD"
    draw.rounded_rectangle([460, top_y, 760, top_y + 24], radius=4, fill=(15, 23, 42, 200), outline=(56, 189, 248, 180), width=1)
    draw.text((472, top_y + 5), user_text, font=font_badge, fill=(56, 189, 248))
    
    draw.rounded_rectangle([width - 240, top_y, width - 48, top_y + 24], radius=4, fill=(6, 78, 59, 200), outline=(16, 185, 129, 220), width=1)
    draw.text((width - 228, top_y + 5), "LIVE // TELEMETRI 27 KODAM", font=font_badge, fill=(167, 243, 208))

    # 6. MAIN BRAND TITLE: SENTINEL-AD
    main_y = 80
    
    # Shield graphic
    shield_pts = [(50, main_y + 12), (72, main_y + 12), (80, main_y + 24), (72, main_y + 60), (61, main_y + 72), (50, main_y + 60)]
    draw.polygon(shield_pts, fill=(6, 182, 212, 40), outline=(6, 182, 212, 255))
    draw.line([(61, main_y + 28), (61, main_y + 56)], fill=(56, 189, 248), width=2)
    draw.line([(53, main_y + 42), (69, main_y + 42)], fill=(56, 189, 248), width=2)

    # Glow shadow behind main text
    title_text = "SENTINEL-AD"
    for ox, oy in [(-2,0),(2,0),(0,-2),(0,2)]:
        draw.text((94 + ox, main_y + oy), title_text, font=font_bahn_large, fill=(6, 182, 212, 100))
    draw.text((94, main_y), title_text, font=font_bahn_large, fill=(255, 255, 255))
    
    # Sub-Brand line
    sub_y = main_y + 62
    draw.text((96, sub_y), "TNI AD COGNITIVE DEFENSE & THREAT INTELLIGENCE SYSTEM", font=font_bahn_title, fill=(56, 189, 248))
    
    # Explanatory tagline
    tag_y = sub_y + 28
    draw.text((96, tag_y), "Sistem Intelijen Siber Sosial & Pertahanan Kognitif Ruang Siber Teritorial Terintegrasi", font=font_bahn_h2, fill=(203, 213, 225))
    
    # Divider line
    draw.line([(50, tag_y + 26), (620, tag_y + 26)], fill=(30, 41, 59, 220), width=1)
    draw.line([(50, tag_y + 26), (220, tag_y + 26)], fill=(6, 182, 212, 220), width=2)

    # 7. FOUR CAPABILITY PILLARS (Matching Kategori 04 Rubric 100%)
    cards_start_y = tag_y + 36
    card_w = 275
    card_h = 76
    gap_x = 18
    gap_y = 14
    
    pillars = [
        {
            "col": 0, "row": 0,
            "badge": "1. 27 KODAM GEOINT TRACKER",
            "title": "Sentimen Teritorial Se-Indonesia",
            "desc_l1": "Pemetaan radar satelit & DEFCON 27 Kodam",
            "desc_l2": "(Renstra Transformasi 1 Provinsi 1 Kodam).",
            "color": (6, 182, 212) # Cyan
        },
        {
            "col": 1, "row": 0,
            "badge": "2. CIB BOTNET SCREENER",
            "title": "Sinkronisasi Waktu <60s",
            "desc_l1": "Deteksi burst botnet serempak & Narrative Jump",
            "desc_l2": "dari kanal Telegram menuju X dan TikTok.",
            "color": (239, 68, 68) # Red
        },
        {
            "col": 0, "row": 1,
            "badge": "3. FORENSIK MULTIMODAL",
            "title": "Audio Deepfake FFT & ELA Dokumen",
            "desc_l1": "Uji cutoff 16kHz kloning vokal buatan AI &",
            "desc_l2": "deteksi stempel Sprin rotasi 14.2 derajat.",
            "color": (245, 158, 11) # Orange/Gold
        },
        {
            "col": 1, "row": 1,
            "badge": "4. COGNITIVE WARGAMING",
            "title": "Simulasi 10 Persona Publik & SOAR",
            "desc_l1": "Prediksi reaksi netizen, cegah blunder publik,",
            "desc_l2": "dan otomasi berkas Dossier Takedown BSSN.",
            "color": (16, 185, 129) # Emerald
        }
    ]
    
    for p in pillars:
        cx = 50 + p["col"] * (card_w + gap_x)
        cy = cards_start_y + p["row"] * (card_h + gap_y)
        
        draw.rounded_rectangle([cx, cy, cx + card_w, cy + card_h], radius=6, fill=(15, 23, 42, 220), outline=(30, 41, 59, 255), width=1)
        draw.rounded_rectangle([cx, cy, cx + 4, cy + card_h], radius=2, fill=p["color"])
        
        draw.text((cx + 12, cy + 7), p["badge"], font=font_bahn_bold, fill=p["color"])
        draw.text((cx + 12, cy + 23), p["title"], font=font_bahn_bold, fill=(248, 250, 252))
        draw.text((cx + 12, cy + 42), p["desc_l1"], font=font_bahn_regular, fill=(148, 163, 184))
        draw.text((cx + 12, cy + 56), p["desc_l2"], font=font_bahn_regular, fill=(148, 163, 184))

    # 8. BOTTOM TRUST CREDENTIALS & DEPLOYMENT BAR
    bottom_y = height - 55
    
    draw.rounded_rectangle([50, bottom_y, 290, bottom_y + 26], radius=4, fill=(6, 182, 212, 30), outline=(6, 182, 212, 180), width=1)
    draw.text((62, bottom_y + 6), "DEMO: sentinel-ad.streamlit.app", font=font_mono, fill=(56, 189, 248))
    
    draw.rounded_rectangle([302, bottom_y, 505, bottom_y + 26], radius=4, fill=(16, 185, 129, 30), outline=(16, 185, 129, 180), width=1)
    draw.text((314, bottom_y + 6), "MILNET AIR-GAPPED DOCKER READY", font=font_mono, fill=(52, 211, 153))

    draw.rounded_rectangle([517, bottom_y, 715, bottom_y + 26], radius=4, fill=(15, 23, 42, 200), outline=(71, 85, 105, 180), width=1)
    draw.text((528, bottom_y + 6), "PURE PYTHON - ZERO GPU COST", font=font_mono, fill=(203, 213, 225))

    draw.rounded_rectangle([width - 320, bottom_y, width - 48, bottom_y + 26], radius=4, fill=(15, 23, 42, 220), outline=(220, 38, 38, 200), width=1)
    draw.text((width - 308, bottom_y + 6), "100% LIVE PURWARUPA // KARYA RESMI", font=font_mono, fill=(248, 113, 113))

    final_rgb = canvas.convert("RGB")
    
    # 9. EXPORT FORMATS (<500 KB limit)
    jpg_path = "THUMBNAIL_SENTINEL_AD.jpg"
    png_path = "THUMBNAIL_SENTINEL_AD.png"
    webp_path = "THUMBNAIL_SENTINEL_AD.webp"
    
    final_rgb.save(jpg_path, format="JPEG", quality=90, optimize=True)
    jpg_size_kb = os.path.getsize(jpg_path) / 1024.0
    
    final_rgb.save(webp_path, format="WEBP", quality=90, method=6)
    webp_size_kb = os.path.getsize(webp_path) / 1024.0
    
    # Quantize to 256 colors for clean crisp edges & strictly <500 KB limit
    png_img = final_rgb.quantize(colors=256)
    png_img.save(png_path, format="PNG", optimize=True)
    png_size_kb = os.path.getsize(png_path) / 1024.0

    print("=== THUMBNAIL KARYA SENTINEL-AD GENERATED ===")
    print(f"Dimensions: {width} x {height} px")
    print(f"1. JPG  : {jpg_path}  -> Size: {jpg_size_kb:.1f} KB (Limit: <500 KB) -> {'PASS' if jpg_size_kb < 500 else 'FAIL'}")
    print(f"2. WEBP : {webp_path} -> Size: {webp_size_kb:.1f} KB (Limit: <500 KB) -> {'PASS' if webp_size_kb < 500 else 'FAIL'}")
    print(f"3. PNG  : {png_path}  -> Size: {png_size_kb:.1f} KB (Limit: <500 KB) -> {'PASS' if png_size_kb < 500 else 'FAIL'}")

if __name__ == "__main__":
    create_hackathon_thumbnail()
