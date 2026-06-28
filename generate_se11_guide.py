from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

OUTPUT = r"C:\Users\I308878\PO_LongText_Persistencey\ZPO_LONGTEXT_SE11_Creation_Guide.pdf"

SAP_DARK      = colors.HexColor("#003366")
SAP_BLUE      = colors.HexColor("#0070F2")
SAP_LIGHT     = colors.HexColor("#E8F4FD")
ORANGE        = colors.HexColor("#E87722")
ORANGE_LIGHT  = colors.HexColor("#FFF3E8")
TEAL          = colors.HexColor("#007B8A")
TEAL_LIGHT    = colors.HexColor("#E0F5F7")
GOLD          = colors.HexColor("#F0AB00")
GOLD_LIGHT    = colors.HexColor("#FFFBE6")
RED           = colors.HexColor("#BB0000")
RED_LIGHT     = colors.HexColor("#FFF0F0")
GREEN_OK      = colors.HexColor("#188918")
GREEN_LIGHT   = colors.HexColor("#E6F4EA")
GREY_BG       = colors.HexColor("#F5F5F5")
GREY_BORDER   = colors.HexColor("#CCCCCC")
CODE_BG       = colors.HexColor("#1E1E2E")
CODE_FG       = colors.HexColor("#CDD6F4")
WHITE         = colors.white
BLACK         = colors.black
DARK_GREY     = colors.HexColor("#444444")

W, H = A4
styles = getSampleStyleSheet()

def ms(name, **kw):
    return ParagraphStyle(name=name, parent=styles["Normal"], **kw)

TITLE    = ms("T",  fontSize=20, textColor=WHITE,   fontName="Helvetica-Bold", alignment=TA_CENTER, spaceAfter=4)
SUBTITLE = ms("ST", fontSize=10, textColor=colors.HexColor("#AACCFF"), fontName="Helvetica", alignment=TA_CENTER, spaceAfter=2)
META     = ms("M",  fontSize=8,  textColor=colors.HexColor("#AACCFF"), fontName="Helvetica", alignment=TA_CENTER)
H1       = ms("H1", fontSize=12, textColor=WHITE,   fontName="Helvetica-Bold", spaceAfter=3)
H2       = ms("H2", fontSize=10, textColor=SAP_DARK,fontName="Helvetica-Bold", spaceAfter=3, spaceBefore=6)
BODY     = ms("B",  fontSize=8.5,textColor=BLACK,   leading=13, spaceAfter=3, alignment=TA_JUSTIFY)
BODY_SML = ms("BS", fontSize=8,  textColor=BLACK,   leading=12, spaceAfter=2)
CODE_S   = ms("CS", fontSize=7.5,textColor=CODE_FG, fontName="Courier", leading=11, spaceAfter=1)
TH       = ms("TH", fontSize=8,  textColor=WHITE,   fontName="Helvetica-Bold", alignment=TA_CENTER)
TC       = ms("TC", fontSize=8,  textColor=BLACK,   leading=11)
TC_C     = ms("TCC",fontSize=8,  textColor=BLACK,   leading=11, alignment=TA_CENTER)
TC_G     = ms("TCG",fontSize=8,  textColor=colors.HexColor("#188918"), fontName="Helvetica-Bold", leading=11, alignment=TA_CENTER)
STEP_N   = ms("SN", fontSize=18, textColor=WHITE,   fontName="Helvetica-Bold", alignment=TA_CENTER)
STEP_T   = ms("STt",fontSize=10, textColor=WHITE,   fontName="Helvetica-Bold")
STEP_S   = ms("SSb",fontSize=8,  textColor=colors.HexColor("#AACCFF"), fontName="Helvetica-Oblique")

def sp(n=5): return Spacer(1, n)

def sec_hdr(num, title, subtitle, hdr_color=SAP_DARK, num_color=None):
    if not num_color: num_color = hdr_color
    num_t = Table([[Paragraph(str(num), STEP_N)]],
                  colWidths=[1.4*cm], rowHeights=[1.2*cm])
    num_t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),num_color),("VALIGN",(0,0),(-1,-1),"MIDDLE")]))
    txt_t = Table([[Paragraph(title,STEP_T)],[Paragraph(subtitle,STEP_S)]],
                  colWidths=[16.1*cm])
    txt_t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1),hdr_color),
        ("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),7),
        ("LEFTPADDING",(0,0),(-1,-1),12),
    ]))
    t = Table([[num_t,txt_t]],colWidths=[1.4*cm,16.1*cm])
    t.setStyle(TableStyle([("TOPPADDING",(0,0),(-1,-1),0),("BOTTOMPADDING",(0,0),(-1,-1),0),
                            ("LEFTPADDING",(0,0),(-1,-1),0),("VALIGN",(0,0),(-1,-1),"MIDDLE")]))
    return t

def info_box(text, bg=SAP_LIGHT, border=SAP_BLUE):
    t=Table([[Paragraph(text,BODY_SML)]],colWidths=[17.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1),bg),("LINEABOVE",(0,0),(-1,0),2,border),
        ("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6),
        ("LEFTPADDING",(0,0),(-1,-1),10),("RIGHTPADDING",(0,0),(-1,-1),8),
    ]))
    return t

def warn_box(t): return info_box(t, RED_LIGHT, RED)
def ok_box(t):   return info_box(t, GREEN_LIGHT, GREEN_OK)
def note_box(t): return info_box(t, GOLD_LIGHT, GOLD)

def code_block(lines):
    rows=[[Paragraph(l.replace(" ","&nbsp;").replace("<","&lt;").replace(">","&gt;") or "&nbsp;",CODE_S)] for l in lines]
    t=Table(rows,colWidths=[17.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1),CODE_BG),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
        ("LEFTPADDING",(0,0),(-1,-1),8),("RIGHTPADDING",(0,0),(-1,-1),6),
    ]))
    return t

def step_row(num, action, detail, color=SAP_BLUE):
    n_t=Table([[Paragraph(str(num),ms(f"sn{num}",fontSize=11,textColor=WHITE,
               fontName="Helvetica-Bold",alignment=TA_CENTER))]],
              colWidths=[0.8*cm])
    n_t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),color),("VALIGN",(0,0),(-1,-1),"MIDDLE"),
                              ("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6)]))
    a_t=Table([[Paragraph(action,ms(f"sa{num}",fontSize=8,textColor=BLACK,fontName="Helvetica-Bold"))],
               [Paragraph(detail,BODY_SML)]],colWidths=[16.7*cm])
    a_t.setStyle(TableStyle([
        ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
        ("LEFTPADDING",(0,0),(-1,-1),8),
    ]))
    t=Table([[n_t,a_t]],colWidths=[0.8*cm,16.7*cm])
    t.setStyle(TableStyle([
        ("LINEABOVE",(0,0),(-1,0),0.5,color),("LINEBELOW",(0,0),(-1,0),0.5,GREY_BORDER),
        ("TOPPADDING",(0,0),(-1,-1),0),("BOTTOMPADDING",(0,0),(-1,-1),0),
        ("LEFTPADDING",(0,0),(-1,-1),0),("VALIGN",(0,0),(-1,-1),"TOP"),
    ]))
    return [t, sp(3)]

def fields_table(rows_data):
    """Coloured field table with Key column highlighted."""
    headers = ["#", "Field Name", "Key", "Data Type", "Length", "Data Element / Note", "Description"]
    widths   = [0.8*cm, 3.8*cm, 1*cm, 2.2*cm, 1.8*cm, 4.9*cm, 3*cm]
    data = [[Paragraph(h, TH) for h in headers]]
    for i, (field, key, dtype, length, de, desc) in enumerate(rows_data):
        key_para = Paragraph("✓" if key else "", TC_G if key else TC_C)
        bg = colors.HexColor("#FFF9E6") if key else (WHITE if i%2==0 else GREY_BG)
        row = [
            Paragraph(str(i+1), TC_C),
            Paragraph(field, ms(f"fn{i}", fontSize=8, textColor=SAP_DARK,
                      fontName="Helvetica-Bold" if key else "Helvetica")),
            key_para,
            Paragraph(dtype,   TC_C),
            Paragraph(length,  TC_C),
            Paragraph(de,      BODY_SML),
            Paragraph(desc,    BODY_SML),
        ]
        data.append(row)
    t = Table(data, colWidths=widths)
    style = [
        ("BACKGROUND",    (0,0), (-1,0),  SAP_BLUE),
        ("GRID",          (0,0), (-1,-1), 0.4, GREY_BORDER),
        ("TOPPADDING",    (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
        ("LEFTPADDING",   (0,0), (-1,-1), 5),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ]
    for i, (field, key, *_) in enumerate(rows_data):
        if key:
            style.append(("BACKGROUND", (0,i+1),(-1,i+1), colors.HexColor("#FFF9E6")))
        else:
            style.append(("BACKGROUND", (0,i+1),(-1,i+1), WHITE if i%2==0 else GREY_BG))
    t.setStyle(TableStyle(style))
    return t

# ══════════════════════════════════════════════════════════════════════════════
def cover():
    els = []
    cov = Table([
        [Paragraph("Step 1 — Create ZPO_LONGTEXT in SE11", TITLE)],
        [Paragraph("Field-by-Field SE11 Creation Guide", SUBTITLE)],
        [Paragraph("Confirmed: TDID = F01  |  Language = D  |  EKPO TDNAME = no space  |  2026-06-28", META)],
    ], colWidths=[17.5*cm])
    cov.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),SAP_DARK),
                              ("TOPPADDING",(0,0),(-1,-1),26),("BOTTOMPADDING",(0,0),(-1,-1),26),
                              ("LEFTPADDING",(0,0),(-1,-1),20)]))
    els.append(cov)
    els.append(sp(12))

    els.append(ok_box(
        "✅  Confirmed from your system:\n"
        "  TDID = F01 for both Header (EKKO) and Item (EKPO) texts\n"
        "  Language = D (German)\n"
        "  EKPO TDNAME = 450007774400010 (no space between PO# and item#)"
    ))
    els.append(sp(8))

    els.append(Paragraph("What You Will Create", H2))
    els.append(Paragraph(
        "ZPO_LONGTEXT is a custom database table that stores the decompressed, plain-text content "
        "of PO long texts. Each row in this table = one line of text. Once created and populated "
        "by the BAdI (Step 3), any ABAP program can read PO long texts with a simple SELECT — "
        "no READ_TEXT function module needed.", BODY))
    els.append(sp(8))

    els.append(Paragraph("Quick Field Summary", H2))
    els.append(fields_table([
        ("MANDT",        True,  "CLNT", "3",   "MANDT",    "Client — always first key field"),
        ("EBELN",        True,  "CHAR", "10",  "EBELN",    "Purchase Order Number"),
        ("EBELP",        True,  "NUMC", "5",   "EBELP",    "Item — 00000 for header texts"),
        ("TDOBJECT",     True,  "CHAR", "10",  "TDOBJECT", "EKKO or EKPO"),
        ("TDID",         True,  "CHAR", "4",   "TDID",     "F01, F02, F09 etc."),
        ("TDSPRAS",      True,  "LANG", "1",   "SPRAS",    "Language key: D"),
        ("LINE_COUNTER", True,  "NUMC", "5",   "—",        "Line sequence 00001, 00002..."),
        ("TDFORMAT",     False, "CHAR", "2",   "TDFORMAT", "Format indicator (* = normal)"),
        ("TDLINE",       False, "CHAR", "132", "TDLINE",   "Plain text content"),
        ("MIGRATED_AT",  False, "DATS", "8",   "—",        "Date row was written"),
        ("MIGRATED_BY",  False, "CHAR", "12",  "UNAME",    "User who wrote this row"),
        ("SOURCE",       False, "CHAR", "1",   "—",        "M=Migration, D=Dual-write"),
    ]))
    els.append(PageBreak())
    return els

# ── Phase A: Open SE11 ────────────────────────────────────────────────────────
def phaseA():
    els = []
    els.append(sec_hdr("A", "Open SE11 and Start Table Creation",
                       "Transaction SE11 — Database Table — ZPO_LONGTEXT", SAP_DARK))
    els.append(sp(8))
    steps = [
        ("Open SE11",
         "Enter transaction code: SE11 → press Enter"),
        ("Select Database Table",
         "In the Object Type section, select the radio button: Database Table"),
        ("Enter table name",
         "In the input field enter exactly: ZPO_LONGTEXT\n"
         "Click Create button (or press F5)"),
        ("Enter Short Description",
         "Short Description field: PO Long Text New Persistency\n"
         "Press Enter to move to the Fields tab"),
    ]
    for i,(a,d) in enumerate(steps,1):
        for row in step_row(i,a,d,SAP_DARK): els.append(row)

    els.append(sp(8))
    els.append(Paragraph("Initial Table Properties to Set", H2))
    items = [
        ("Delivery Class", "A",
         "A = Application table (customer data). Set in Attributes tab."),
        ("Data Browser/Table View Maintenance", "Display/Maintenance Allowed",
         "Allows SE16N browsing and SM30 maintenance. Set in Attributes tab."),
        ("Enhancement Category", "Can Be Enhanced (Deep)",
         "Set via menu: Extras → Enhancement Category. Allows future structure appends."),
    ]
    for label, value, note in items:
        t = Table([[
            Paragraph(label, ms(f"pl{label[:3]}", fontSize=8, textColor=SAP_DARK, fontName="Helvetica-Bold")),
            Paragraph(value, ms(f"pv{label[:3]}", fontSize=8, textColor=GREEN_OK, fontName="Helvetica-Bold")),
            Paragraph(note, BODY_SML),
        ]], colWidths=[4.5*cm, 3.5*cm, 9.5*cm])
        t.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(0,0),GREY_BG),
            ("BACKGROUND",(1,0),(1,0),GREEN_LIGHT),
            ("BACKGROUND",(2,0),(2,0),WHITE),
            ("GRID",(0,0),(-1,-1),0.4,GREY_BORDER),
            ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
            ("LEFTPADDING",(0,0),(-1,-1),8),("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ]))
        els.append(t)
        els.append(sp(3))
    els.append(PageBreak())
    return els

# ── Phase B: Fields ───────────────────────────────────────────────────────────
def phaseB():
    els = []
    els.append(sec_hdr("B", "Add Fields — One Row at a Time",
                       "Fields tab — add each field in order, key fields first", SAP_BLUE))
    els.append(sp(8))
    els.append(info_box(
        "In SE11 Fields tab: each row = one field. "
        "Tick the 'Key' checkbox for key fields. "
        "Enter the Data Element name — SE11 auto-fills Data Type and Length from the data element. "
        "For fields without a standard data element, enter Data Type and Length manually."
    ))
    els.append(sp(6))

    # KEY FIELDS
    els.append(Paragraph("Key Fields (tick Key checkbox ✓)", H2))
    key_data = [
        ["1", "MANDT",        "✓", "MANDT",
         "CLNT", "3",
         "Enter field name MANDT → Data Element: MANDT → SE11 auto-fills CLNT/3\n"
         "Tick Key checkbox ✓"],
        ["2", "EBELN",        "✓", "EBELN",
         "CHAR", "10",
         "Enter field name EBELN → Data Element: EBELN → SE11 auto-fills CHAR/10\n"
         "Tick Key checkbox ✓"],
        ["3", "EBELP",        "✓", "EBELP",
         "NUMC", "5",
         "Enter field name EBELP → Data Element: EBELP → SE11 auto-fills NUMC/5\n"
         "Tick Key checkbox ✓\n"
         "NOTE: Header texts use EBELP = 00000, item texts use actual item number"],
        ["4", "TDOBJECT",     "✓", "TDOBJECT",
         "CHAR", "10",
         "Enter field name TDOBJECT → Data Element: TDOBJECT → SE11 auto-fills CHAR/10\n"
         "Tick Key checkbox ✓\n"
         "Values: EKKO (header) or EKPO (item)"],
        ["5", "TDID",         "✓", "TDID",
         "CHAR", "4",
         "Enter field name TDID → Data Element: TDID → SE11 auto-fills CHAR/4\n"
         "Tick Key checkbox ✓\n"
         "Values: F01 (confirmed), F02, F09 etc."],
        ["6", "TDSPRAS",      "✓", "SPRAS",
         "LANG", "1",
         "Enter field name TDSPRAS → Data Element: SPRAS → SE11 auto-fills LANG/1\n"
         "Tick Key checkbox ✓\n"
         "Value: D (German in this system)"],
        ["7", "LINE_COUNTER", "✓", "—",
         "NUMC", "5",
         "Enter field name LINE_COUNTER → NO standard data element\n"
         "Enter manually: Data Type = NUMC, Length = 5\n"
         "Tick Key checkbox ✓\n"
         "This drives ORDER BY for correct text line sequence"],
    ]
    hdr = [[Paragraph(h,TH) for h in ["#","Field Name","Key","Data Element","Type","Len","SE11 Entry Instructions"]]]
    rows = []
    for r in key_data:
        rows.append([
            Paragraph(r[0], TC_C),
            Paragraph(r[1], ms(f"kf{r[0]}", fontSize=8, textColor=SAP_DARK, fontName="Helvetica-Bold")),
            Paragraph(r[2], TC_G),
            Paragraph(r[3], ms(f"kd{r[0]}", fontSize=8, textColor=TEAL, fontName="Helvetica-Bold")),
            Paragraph(r[4], TC_C),
            Paragraph(r[5], TC_C),
            Paragraph(r[6], BODY_SML),
        ])
    kt = Table(hdr+rows, colWidths=[0.7*cm,2.8*cm,0.8*cm,2.5*cm,1.2*cm,0.9*cm,8.6*cm])
    kt.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,0),  SAP_BLUE),
        ("BACKGROUND",    (0,1),(-1,-1), colors.HexColor("#FFFDE6")),
        ("GRID",          (0,0),(-1,-1), 0.4, GREY_BORDER),
        ("TOPPADDING",    (0,0),(-1,-1), 4),
        ("BOTTOMPADDING", (0,0),(-1,-1), 4),
        ("LEFTPADDING",   (0,0),(-1,-1), 5),
        ("VALIGN",        (0,0),(-1,-1), "TOP"),
    ]))
    els.append(kt)
    els.append(sp(8))

    # NON-KEY FIELDS
    els.append(Paragraph("Non-Key Fields (do NOT tick Key checkbox)", H2))
    nk_data = [
        ["8",  "TDFORMAT",    "TDFORMAT",
         "CHAR", "2",
         "Data Element: TDFORMAT → auto-fills CHAR/2\n"
         "Stores format indicator. Value * = normal text line (standard SAP)."],
        ["9",  "TDLINE",      "TDLINE",
         "CHAR", "132",
         "Data Element: TDLINE → auto-fills CHAR/132\n"
         "THE MAIN FIELD — stores the actual plain text content of each line.\n"
         "Max 132 characters per line (SAP standard text line limit)."],
        ["10", "MIGRATED_AT", "—",
         "DATS", "8",
         "NO data element. Enter manually: Data Type = DATS, Length = 8\n"
         "Stores the date this row was written (sy-datum at write time)."],
        ["11", "MIGRATED_BY", "UNAME",
         "CHAR", "12",
         "Data Element: UNAME → auto-fills CHAR/12\n"
         "Stores the user who wrote this row (sy-uname at write time)."],
        ["12", "SOURCE",      "—",
         "CHAR", "1",
         "NO data element. Enter manually: Data Type = CHAR, Length = 1\n"
         "M = written by migration program\n"
         "D = written by BAdI dual-write on PO save"],
    ]
    hdr2 = [[Paragraph(h,TH) for h in ["#","Field Name","Data Element","Type","Len","SE11 Entry Instructions"]]]
    rows2 = []
    for i,r in enumerate(nk_data):
        rows2.append([
            Paragraph(r[0], TC_C),
            Paragraph(r[1], ms(f"nf{r[0]}", fontSize=8, textColor=SAP_DARK, fontName="Helvetica-Bold")),
            Paragraph(r[2], ms(f"nd{r[0]}", fontSize=8, textColor=TEAL, fontName="Helvetica-Bold")),
            Paragraph(r[3], TC_C),
            Paragraph(r[4], TC_C),
            Paragraph(r[5], BODY_SML),
        ])
    nkt = Table(hdr2+rows2, colWidths=[0.7*cm,2.8*cm,2.5*cm,1.2*cm,0.9*cm,9.4*cm])
    nkt.setStyle(TableStyle([
        ("BACKGROUND",     (0,0),(-1,0),  SAP_BLUE),
        ("ROWBACKGROUNDS", (0,1),(-1,-1), [WHITE, GREY_BG]),
        ("GRID",           (0,0),(-1,-1), 0.4, GREY_BORDER),
        ("TOPPADDING",     (0,0),(-1,-1), 4),
        ("BOTTOMPADDING",  (0,0),(-1,-1), 4),
        ("LEFTPADDING",    (0,0),(-1,-1), 5),
        ("VALIGN",         (0,0),(-1,-1), "TOP"),
    ]))
    els.append(nkt)
    els.append(PageBreak())
    return els

# ── Phase C: Save & Activate ──────────────────────────────────────────────────
def phaseC():
    els = []
    els.append(sec_hdr("C", "Save, Activate and Verify",
                       "Final steps after adding all 12 fields", SAP_DARK))
    els.append(sp(8))
    steps = [
        ("Save the table",
         "Press Ctrl+S → assign to package: ZMM (or your development package)\n"
         "Transport request: assign to your active workbench transport\n"
         "Save"),
        ("Activate the table",
         "Press Ctrl+F3 (Activate)\n"
         "OR Menu: Table → Activate\n"
         "Status bar must show: Object ZPO_LONGTEXT activated\n"
         "If errors appear → check field definitions match the table above"),
        ("Verify in SE11",
         "SE11 → Database Table → ZPO_LONGTEXT → Display\n"
         "Top area shows: Active\n"
         "Fields tab shows all 12 fields with correct Key ticks"),
        ("Create Secondary Index (recommended)",
         "SE11 → ZPO_LONGTEXT → Display → Indexes button → Create\n"
         "Index name: ZPO_LT_I01\n"
         "Add fields: EBELN, TDOBJECT, TDID\n"
         "Save → Activate\n"
         "This speeds up queries filtering by PO number + text type"),
        ("Verify table is empty",
         "SE16N → ZPO_LONGTEXT → Execute (no filters)\n"
         "Result: No entries — expected at this stage\n"
         "Table will be populated after Step 3 (BAdI) is active"),
    ]
    for i,(a,d) in enumerate(steps,1):
        for row in step_row(i,a,d,SAP_DARK): els.append(row)

    els.append(sp(8))
    els.append(ok_box(
        "✅  Step 1 complete when:\n"
        "  SE11 → ZPO_LONGTEXT → Status = Active\n"
        "  All 12 fields present with correct Key ticks (7 key fields)\n"
        "  SE16N → ZPO_LONGTEXT → table accessible (empty = correct)"
    ))
    els.append(PageBreak())
    return els

# ── Phase D: Quick Reference ──────────────────────────────────────────────────
def phaseD():
    els = []
    els.append(sec_hdr("D", "Quick Reference — All 12 Fields at a Glance",
                       "Print this page and keep it open while creating the table in SE11",
                       TEAL))
    els.append(sp(8))

    els.append(fields_table([
        ("MANDT",        True,  "CLNT", "3",   "MANDT — standard",    "Client"),
        ("EBELN",        True,  "CHAR", "10",  "EBELN — standard",    "Purchase Order Number"),
        ("EBELP",        True,  "NUMC", "5",   "EBELP — standard",    "PO Item (00000 = header)"),
        ("TDOBJECT",     True,  "CHAR", "10",  "TDOBJECT — standard", "Text Object: EKKO / EKPO"),
        ("TDID",         True,  "CHAR", "4",   "TDID — standard",     "Text ID: F01 confirmed"),
        ("TDSPRAS",      True,  "LANG", "1",   "SPRAS — standard",    "Language: D confirmed"),
        ("LINE_COUNTER", True,  "NUMC", "5",   "Manual — no DE",      "Line sequence 00001..."),
        ("TDFORMAT",     False, "CHAR", "2",   "TDFORMAT — standard", "Format indicator (* = normal)"),
        ("TDLINE",       False, "CHAR", "132", "TDLINE — standard",   "Plain text content ← main field"),
        ("MIGRATED_AT",  False, "DATS", "8",   "Manual — no DE",      "Date row was written"),
        ("MIGRATED_BY",  False, "CHAR", "12",  "UNAME — standard",    "User who wrote this row"),
        ("SOURCE",       False, "CHAR", "1",   "Manual — no DE",      "M=Migration D=Dual-write"),
    ]))
    els.append(sp(8))

    # Data elements summary
    els.append(Paragraph("Data Elements — Standard vs Manual Entry", H2))
    de_data = [
        ["Field", "Data Element", "Entry Method"],
        ["MANDT",        "MANDT",    "Type DE name → SE11 auto-fills Type+Length"],
        ["EBELN",        "EBELN",    "Type DE name → SE11 auto-fills Type+Length"],
        ["EBELP",        "EBELP",    "Type DE name → SE11 auto-fills Type+Length"],
        ["TDOBJECT",     "TDOBJECT", "Type DE name → SE11 auto-fills Type+Length"],
        ["TDID",         "TDID",     "Type DE name → SE11 auto-fills Type+Length"],
        ["TDSPRAS",      "SPRAS",    "Type DE name → SE11 auto-fills Type+Length"],
        ["LINE_COUNTER", "—",        "NO data element — enter NUMC / 5 manually"],
        ["TDFORMAT",     "TDFORMAT", "Type DE name → SE11 auto-fills Type+Length"],
        ["TDLINE",       "TDLINE",   "Type DE name → SE11 auto-fills CHAR/132"],
        ["MIGRATED_AT",  "—",        "NO data element — enter DATS / 8 manually"],
        ["MIGRATED_BY",  "UNAME",    "Type DE name → SE11 auto-fills CHAR/12"],
        ["SOURCE",       "—",        "NO data element — enter CHAR / 1 manually"],
    ]
    de_t = Table(
        [[Paragraph(h, TH) for h in de_data[0]]] +
        [[Paragraph(str(c), TC) for c in row] for row in de_data[1:]],
        colWidths=[3.5*cm, 3.5*cm, 10.5*cm]
    )
    de_t.setStyle(TableStyle([
        ("BACKGROUND",     (0,0),(-1,0),  SAP_BLUE),
        ("ROWBACKGROUNDS", (0,1),(-1,-1), [WHITE, GREY_BG]),
        ("GRID",           (0,0),(-1,-1), 0.4, GREY_BORDER),
        ("TOPPADDING",     (0,0),(-1,-1), 4),("BOTTOMPADDING",(0,0),(-1,-1),4),
        ("LEFTPADDING",    (0,0),(-1,-1), 6),("VALIGN",(0,0),(-1,-1),"TOP"),
    ]))
    els.append(de_t)
    els.append(sp(8))

    els.append(note_box(
        "After Step 1 is done — proceed to:\n"
        "Step 2: SE24 → Create ZCL_PO_LONGTEXT_HANDLER (handler class)\n"
        "Step 3: SE19 → Create ZCL_PO_TEXT_BADI_IMPL (BAdI implementation)\n"
        "Step 4: ME21N → create PO with text → SE16N → verify ZPO_LONGTEXT populated\n"
        "Full ABAP code for Steps 2 and 3 is in: PO_LongText_4Steps_Guide.pdf"
    ))
    return els

# ── Build ─────────────────────────────────────────────────────────────────────
def build():
    doc = SimpleDocTemplate(
        OUTPUT, pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2*cm, bottomMargin=2*cm,
        title="ZPO_LONGTEXT SE11 Creation Guide",
        author="SAP PO Long Text Team",
    )
    story = []
    story.extend(cover())
    story.extend(phaseA())
    story.extend(phaseB())
    story.extend(phaseC())
    story.extend(phaseD())

    def on_page(c, doc):
        c.saveState()
        c.setFont("Helvetica", 7)
        c.setFillColor(colors.HexColor("#888888"))
        c.drawString(2*cm, 1.2*cm,
            "ZPO_LONGTEXT — SE11 Field-by-Field Creation Guide | TDID=F01 | Language=D")
        c.drawRightString(19.5*cm, 1.2*cm, f"Page {doc.page}")
        c.setStrokeColor(colors.HexColor("#CCCCCC"))
        c.setLineWidth(0.4)
        c.line(2*cm, 1.5*cm, 19.5*cm, 1.5*cm)
        c.restoreState()

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print(f"PDF created: {OUTPUT}")

build()
