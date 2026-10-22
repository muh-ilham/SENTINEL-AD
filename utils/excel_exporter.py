"""
utils/excel_exporter.py - Military-Grade Excel & Formatted Spreadsheet Exporter for SENTINEL-AD
Generates beautifully styled, executive-ready Excel (.xlsx) workbooks and Excel-compatible CSVs
for Social Network Analysis (SNA) threat matrices and intelligence reports.
"""

import io
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from datetime import datetime

def generate_sna_excel_bytes(nodes_data, edges_data, degree_dict, betweenness_dict, is_live=True, operator_role="Analis Siber (Pussiberad)"):
    """
    Generates a defense-grade, beautifully formatted Microsoft Excel (.xlsx) file
    with styled headers, military classification banners, category-based cell highlights,
    and automatic column width adjustments.
    """
    wb = openpyxl.Workbook()
    
    # -------------------------------------------------------------
    # SHEET 1: Matriks Simpul Ancaman (SNA)
    # -------------------------------------------------------------
    ws1 = wb.active
    ws1.title = "Matriks Simpul SNA"
    ws1.views.sheetView[0].showGridLines = True
    
    # Border styles
    thin_border_side = Side(border_style="thin", color="CBD5E1")
    cell_border = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=thin_border_side)
    
    header_border_side = Side(border_style="medium", color="0F172A")
    header_border = Border(left=thin_border_side, right=thin_border_side, top=header_border_side, bottom=header_border_side)

    # 1. Row 1: Title Banner
    ws1.merge_cells("A1:I1")
    title_cell = ws1["A1"]
    title_cell.value = "SENTINEL-AD | TNI AD COGNITIVE DEFENSE COMMAND - MATRIKS SIMPUL ANCAMAN (SNA)"
    title_cell.font = Font(name="Calibri", size=13, bold=True, color="FFFFFF")
    title_cell.fill = PatternFill(start_color="0F172A", end_color="0F172A", fill_type="solid")
    title_cell.alignment = Alignment(horizontal="center", vertical="center")
    ws1.row_dimensions[1].height = 32

    # 2. Row 2: Metadata & Classification Notice
    now_str = datetime.now().strftime("%d-%m-%Y %H:%M:%S WIB")
    mode_text = "LIVE ONLINE OSINT (6 Ekosistem Medsos)"
    
    ws1.merge_cells("A2:I2")
    meta_cell = ws1["A2"]
    meta_cell.value = f"KLASIFIKASI: RAHASIA / DEFENSE CONFIDENTIAL  |  Waktu Ekspor: {now_str}  |  Operator: {operator_role}  |  Telemetri: {mode_text}"
    meta_cell.font = Font(name="Calibri", size=9, bold=True, color="E2E8F0")
    meta_cell.fill = PatternFill(start_color="1E293B", end_color="1E293B", fill_type="solid")
    meta_cell.alignment = Alignment(horizontal="center", vertical="center")
    ws1.row_dimensions[2].height = 20

    # 3. Row 3: Blank separator
    ws1.row_dimensions[3].height = 8

    # 4. Row 4: Column Headers
    headers = [
        "No",
        "Node ID",
        "Label Akun / Kanal",
        "Kategori Peran",
        "Platform",
        "Koneksi (Degree)",
        "Betweenness Centrality",
        "Rekomendasi Tindakan Taktis Pussiberad",
        "Profil Aktivitas & Bukti Forensik"
    ]
    
    ws1.row_dimensions[4].height = 26
    for col_idx, h in enumerate(headers, start=1):
        c = ws1.cell(row=4, column=col_idx, value=h)
        c.font = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
        c.fill = PatternFill(start_color="1E293B", end_color="1E293B", fill_type="solid")
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = header_border

    # Color definitions for category badges
    CATEGORY_STYLES = {
        "Seed Account": {
            "fill": PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid"),
            "font": Font(name="Calibri", size=10, bold=True, color="991B1B"),
            "rec_text": "🚨 PRIORITAS 1: Takedown Darurat BSSN & Pelacakan IP"
        },
        "Bridge Node": {
            "fill": PatternFill(start_color="FEF3C7", end_color="FEF3C7", fill_type="solid"),
            "font": Font(name="Calibri", size=10, bold=True, color="92400E"),
            "rec_text": "⚠️ PRIORITAS 2: Kanal Kunci - Putus Rantai Transmisi"
        },
        "Amplifier Cluster": {
            "fill": PatternFill(start_color="FFEDD5", end_color="FFEDD5", fill_type="solid"),
            "font": Font(name="Calibri", size=10, bold=True, color="9A3412"),
            "rec_text": "ℹ️ PRIORITAS 3: Botnet Farm - Blacklist Hash Akun"
        },
        "Organic Audience": {
            "fill": PatternFill(start_color="F1F5F9", end_color="F1F5F9", fill_type="solid"),
            "font": Font(name="Calibri", size=10, bold=False, color="334155"),
            "rec_text": "✅ AUDIENS ORGANIK: Edukasi Kognitif / Debunk Dispenad"
        }
    }

    # 5. Populate Data Rows
    for row_idx, n in enumerate(nodes_data, start=5):
        grp = n.get("group", "Organic Audience")
        style = CATEGORY_STYLES.get(grp, CATEGORY_STYLES["Organic Audience"])
        deg = degree_dict.get(n["id"], 0)
        bet = round(betweenness_dict.get(n["id"], 0.0), 3)
        plat = n.get("platform", "Multi-Platform")
        
        # Row zebra background for general cells
        row_bg_color = "FAFAFA" if row_idx % 2 == 0 else "FFFFFF"
        zebra_fill = PatternFill(start_color=row_bg_color, end_color=row_bg_color, fill_type="solid")
        
        ws1.row_dimensions[row_idx].height = 24
        
        # Col 1: No
        c1 = ws1.cell(row=row_idx, column=1, value=row_idx - 4)
        c1.alignment = Alignment(horizontal="center", vertical="center")
        c1.fill = zebra_fill
        c1.border = cell_border
        
        # Col 2: Node ID
        c2 = ws1.cell(row=row_idx, column=2, value=n["id"].upper())
        c2.font = Font(name="Consolas", size=9.5, bold=True, color="0284C7")
        c2.alignment = Alignment(horizontal="center", vertical="center")
        c2.fill = zebra_fill
        c2.border = cell_border
        
        # Col 3: Label Akun / Kanal
        c3 = ws1.cell(row=row_idx, column=3, value=n["label"])
        c3.font = Font(name="Calibri", size=10, bold=True, color="0F172A")
        c3.alignment = Alignment(horizontal="left", vertical="center")
        c3.fill = zebra_fill
        c3.border = cell_border
        
        # Col 4: Kategori Peran (Highlighted Badge)
        c4 = ws1.cell(row=row_idx, column=4, value=grp.upper())
        c4.font = style["font"]
        c4.fill = style["fill"]
        c4.alignment = Alignment(horizontal="center", vertical="center")
        c4.border = cell_border
        
        # Col 5: Platform
        c5 = ws1.cell(row=row_idx, column=5, value=plat)
        c5.alignment = Alignment(horizontal="center", vertical="center")
        c5.fill = zebra_fill
        c5.border = cell_border
        
        # Col 6: Degree Connections
        c6 = ws1.cell(row=row_idx, column=6, value=deg)
        c6.number_format = "#,##0"
        c6.font = Font(name="Calibri", size=10, bold=True, color="0369A1")
        c6.alignment = Alignment(horizontal="center", vertical="center")
        c6.fill = zebra_fill
        c6.border = cell_border
        
        # Col 7: Betweenness Centrality
        c7 = ws1.cell(row=row_idx, column=7, value=bet)
        c7.number_format = "0.000"
        c7.font = Font(name="Calibri", size=10, bold=True, color="B45309")
        c7.alignment = Alignment(horizontal="center", vertical="center")
        c7.fill = zebra_fill
        c7.border = cell_border
        
        # Col 8: Rekomendasi Tindakan
        c8 = ws1.cell(row=row_idx, column=8, value=style["rec_text"])
        c8.font = Font(name="Calibri", size=9.5, bold=True, color="0F172A")
        c8.alignment = Alignment(horizontal="left", vertical="center")
        c8.fill = zebra_fill
        c8.border = cell_border
        
        # Col 9: Profil & Bukti Forensik
        c9 = ws1.cell(row=row_idx, column=9, value=n.get("info", ""))
        c9.font = Font(name="Calibri", size=9, color="475569")
        c9.alignment = Alignment(horizontal="left", vertical="center")
        c9.fill = zebra_fill
        c9.border = cell_border

    # Auto-adjust column widths
    col_widths = {
        1: 6,   # No
        2: 16,  # Node ID
        3: 32,  # Label
        4: 20,  # Kategori
        5: 18,  # Platform
        6: 18,  # Degree
        7: 22,  # Betweenness
        8: 46,  # Rekomendasi
        9: 75   # Profil Aktivitas
    }
    for col_idx, width in col_widths.items():
        col_letter = get_column_letter(col_idx)
        ws1.column_dimensions[col_letter].width = width

    # -------------------------------------------------------------
    # SHEET 2: Topologi Garis & Transmisi (Edges)
    # -------------------------------------------------------------
    ws2 = wb.create_sheet(title="Topologi Garis (Edges)")
    ws2.views.sheetView[0].showGridLines = True
    
    # Title
    ws2.merge_cells("A1:E1")
    t2 = ws2["A1"]
    t2.value = "SENTINEL-AD | JALUR TRANSMISI PROPAGASI & AMPLIFIKASI (SNA EDGES)"
    t2.font = Font(name="Calibri", size=12, bold=True, color="FFFFFF")
    t2.fill = PatternFill(start_color="0F172A", end_color="0F172A", fill_type="solid")
    t2.alignment = Alignment(horizontal="center", vertical="center")
    ws2.row_dimensions[1].height = 28
    
    # Headers
    edge_headers = ["No", "Simpul Asal (Source)", "Simpul Tujuan (Target)", "Bobot Koneksi (Weight)", "Tipe Transmisi"]
    ws2.row_dimensions[3].height = 24
    for c_idx, eh in enumerate(edge_headers, start=1):
        cell = ws2.cell(row=3, column=c_idx, value=eh)
        cell.font = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
        cell.fill = PatternFill(start_color="1E293B", end_color="1E293B", fill_type="solid")
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = header_border
        
    for r_idx, (u, v, w) in enumerate(edges_data, start=4):
        ws2.row_dimensions[r_idx].height = 20
        c_no = ws2.cell(row=r_idx, column=1, value=r_idx - 3)
        c_no.alignment = Alignment(horizontal="center", vertical="center")
        c_no.border = cell_border
        
        c_src = ws2.cell(row=r_idx, column=2, value=u)
        c_src.font = Font(name="Consolas", size=9.5, bold=True, color="0F172A")
        c_src.alignment = Alignment(horizontal="center", vertical="center")
        c_src.border = cell_border
        
        c_tgt = ws2.cell(row=r_idx, column=3, value=v)
        c_tgt.font = Font(name="Consolas", size=9.5, bold=True, color="0F172A")
        c_tgt.alignment = Alignment(horizontal="center", vertical="center")
        c_tgt.border = cell_border
        
        c_w = ws2.cell(row=r_idx, column=4, value=w)
        c_w.alignment = Alignment(horizontal="center", vertical="center")
        c_w.border = cell_border
        
        ttype = "Inisiasi -> Botnet" if "seed" in u else ("Botnet -> Kanal Bridge" if "bridge" in v else "Kanal -> Publik Organik")
        c_type = ws2.cell(row=r_idx, column=5, value=ttype)
        c_type.alignment = Alignment(horizontal="left", vertical="center")
        c_type.border = cell_border

    ws2.column_dimensions["A"].width = 6
    ws2.column_dimensions["B"].width = 22
    ws2.column_dimensions["C"].width = 22
    ws2.column_dimensions["D"].width = 22
    ws2.column_dimensions["E"].width = 30

    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    return buffer.getvalue()

def generate_sna_clean_csv_bytes(nodes_data, degree_dict, betweenness_dict):
    """
    Generates an Excel-friendly CSV with semicolon (;) delimiter and UTF-8 with BOM (utf-8-sig)
    so double-clicking opens automatically into neat separate columns on Indonesian & international Excel.
    """
    lines = [
        "No;Node ID;Label Akun / Kanal;Kategori Peran;Platform;Koneksi (Degree);Betweenness Centrality;Profil Aktivitas"
    ]
    for idx, n in enumerate(nodes_data, start=1):
        deg = degree_dict.get(n["id"], 0)
        bet = f"{betweenness_dict.get(n['id'], 0.0):.3f}"
        plat = n.get("platform", "Multi-Platform")
        # Clean info text of semicolons or line breaks
        info = n.get("info", "").replace(";", ",").replace("\n", " ").strip()
        label = n.get("label", "").replace(";", ",")
        grp = n.get("group", "").replace(";", ",")
        
        line = f'{idx};"{n["id"].upper()}";"{label}";"{grp}";"{plat}";{deg};"{bet}";"{info}"'
        lines.append(line)
        
    csv_str = "\r\n".join(lines)
    # utf-8-sig adds the Byte Order Mark (BOM: \xef\xbb\xbf) which instructs Excel to parse UTF-8 cleanly
    return csv_str.encode("utf-8-sig")
