from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

OUTPUT = r"C:\Users\I308878\PO_LongText_Persistencey\PO_LongText_4Steps_Guide.pdf"

# ── Colours ───────────────────────────────────────────────────────────────────
SAP_DARK      = colors.HexColor("#003366")
SAP_BLUE      = colors.HexColor("#0070F2")
SAP_LIGHT     = colors.HexColor("#E8F4FD")
BTP_GREEN     = colors.HexColor("#1A6632")
BTP_LIGHT     = colors.HexColor("#E6F4EA")
ORANGE        = colors.HexColor("#E87722")
ORANGE_LIGHT  = colors.HexColor("#FFF3E8")
PURPLE        = colors.HexColor("#6B3FA0")
PURPLE_LIGHT  = colors.HexColor("#F0EAF8")
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
H1       = ms("H1", fontSize=13, textColor=WHITE,   fontName="Helvetica-Bold", spaceAfter=3)
H2       = ms("H2", fontSize=11, textColor=SAP_DARK,fontName="Helvetica-Bold", spaceAfter=4, spaceBefore=6)
H3       = ms("H3", fontSize=9,  textColor=SAP_BLUE,fontName="Helvetica-Bold", spaceAfter=3, spaceBefore=4)
BODY     = ms("B",  fontSize=8.5,textColor=BLACK,   leading=13, spaceAfter=3, alignment=TA_JUSTIFY)
BODY_SML = ms("BS", fontSize=8,  textColor=BLACK,   leading=12, spaceAfter=2)
CODE_S   = ms("CS", fontSize=7.5,textColor=CODE_FG, fontName="Courier", leading=11, spaceAfter=1)
QUOTE_S  = ms("QS", fontSize=8,  textColor=DARK_GREY,fontName="Helvetica-Oblique", leading=12, leftIndent=10, spaceAfter=3)
TH       = ms("TH", fontSize=8,  textColor=WHITE,   fontName="Helvetica-Bold", alignment=TA_CENTER)
TC       = ms("TC", fontSize=8,  textColor=BLACK,   leading=11)
STEP_N   = ms("SN", fontSize=22, textColor=WHITE,   fontName="Helvetica-Bold", alignment=TA_CENTER)
STEP_T   = ms("STt",fontSize=11, textColor=WHITE,   fontName="Helvetica-Bold")
STEP_S   = ms("SSb",fontSize=8,  textColor=colors.HexColor("#AACCFF"), fontName="Helvetica-Oblique")

def sp(n=6): return Spacer(1, n)

# ── Helpers ───────────────────────────────────────────────────────────────────
def sec_hdr(num, title, subtitle, hdr_color=SAP_DARK, num_color=None):
    if not num_color: num_color = hdr_color
    num_t = Table([[Paragraph(str(num), STEP_N)]],
                  colWidths=[1.6*cm], rowHeights=[1.4*cm])
    num_t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), num_color),
        ("VALIGN",    (0,0),(-1,-1),"MIDDLE"),
    ]))
    txt_t = Table([
        [Paragraph(title,    STEP_T)],
        [Paragraph(subtitle, STEP_S)],
    ], colWidths=[15.9*cm])
    txt_t.setStyle(TableStyle([
        ("BACKGROUND",   (0,0),(-1,-1), hdr_color),
        ("TOPPADDING",   (0,0),(-1,-1), 8),
        ("BOTTOMPADDING",(0,0),(-1,-1), 8),
        ("LEFTPADDING",  (0,0),(-1,-1), 12),
    ]))
    t = Table([[num_t, txt_t]], colWidths=[1.6*cm, 15.9*cm])
    t.setStyle(TableStyle([
        ("TOPPADDING",   (0,0),(-1,-1), 0),
        ("BOTTOMPADDING",(0,0),(-1,-1), 0),
        ("LEFTPADDING",  (0,0),(-1,-1), 0),
        ("VALIGN",       (0,0),(-1,-1), "MIDDLE"),
    ]))
    return t

def tbl(headers, rows, widths=None):
    n = len(headers)
    if not widths: widths = [17.5*cm/n]*n
    data = [[Paragraph(h, TH) for h in headers]]
    for row in rows:
        data.append([Paragraph(str(c), TC) for c in row])
    t = Table(data, colWidths=widths)
    t.setStyle(TableStyle([
        ("BACKGROUND",     (0,0),(-1,0),  SAP_BLUE),
        ("ROWBACKGROUNDS", (0,1),(-1,-1), [WHITE, GREY_BG]),
        ("GRID",           (0,0),(-1,-1), 0.4, GREY_BORDER),
        ("TOPPADDING",     (0,0),(-1,-1), 5),
        ("BOTTOMPADDING",  (0,0),(-1,-1), 5),
        ("LEFTPADDING",    (0,0),(-1,-1), 6),
        ("VALIGN",         (0,0),(-1,-1), "TOP"),
    ]))
    return t

def info_box(text, bg=SAP_LIGHT, border=SAP_BLUE):
    t = Table([[Paragraph(text, BODY_SML)]], colWidths=[17.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",   (0,0),(-1,-1), bg),
        ("LINEABOVE",    (0,0),(-1,0),  2, border),
        ("TOPPADDING",   (0,0),(-1,-1), 7),
        ("BOTTOMPADDING",(0,0),(-1,-1), 7),
        ("LEFTPADDING",  (0,0),(-1,-1), 12),
        ("RIGHTPADDING", (0,0),(-1,-1), 8),
    ]))
    return t

def warn_box(t): return info_box(t, RED_LIGHT,    RED)
def ok_box(t):   return info_box(t, GREEN_LIGHT,  GREEN_OK)
def note_box(t): return info_box(t, GOLD_LIGHT,   GOLD)

def code_block(lines):
    rows = [[Paragraph(
        l.replace(" ","&nbsp;").replace("<","&lt;").replace(">","&gt;") or "&nbsp;",
        CODE_S)] for l in lines]
    t = Table(rows, colWidths=[17.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), CODE_BG),
        ("TOPPADDING",    (0,0),(-1,-1), 6),
        ("BOTTOMPADDING", (0,0),(-1,-1), 6),
        ("LEFTPADDING",   (0,0),(-1,-1), 10),
        ("RIGHTPADDING",  (0,0),(-1,-1), 6),
    ]))
    return t

def flow_arrow(label=""):
    rows = []
    if label:
        rows.append(Table([[Paragraph(label, ms(f"fl{label[:3]}", fontSize=7.5,
                    textColor=SAP_BLUE, fontName="Helvetica-Bold", alignment=TA_CENTER))]],
                    colWidths=[17.5*cm]))
    rows.append(Table([[Paragraph("▼", ms("arr", fontSize=14, textColor=SAP_BLUE,
                alignment=TA_CENTER))]],colWidths=[17.5*cm]))
    return rows

# ══════════════════════════════════════════════════════════════════════════════
def cover():
    els = []
    cov = Table([
        [Paragraph("PO Long Text New Persistency", TITLE)],
        [Paragraph("4-Step Implementation Guide", SUBTITLE)],
        [Paragraph("SE11 Table → SE24 Handler Class → SE19 BAdI → Test &amp; Verify", SUBTITLE)],
        [Paragraph("SAP ERP / S4HANA  |  Single System  |  STXH/STXL → ZPO_LONGTEXT  |  2026-06-28", META)],
    ], colWidths=[17.5*cm])
    cov.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), SAP_DARK),
        ("TOPPADDING",    (0,0),(-1,-1), 28),
        ("BOTTOMPADDING", (0,0),(-1,-1), 28),
        ("LEFTPADDING",   (0,0),(-1,-1), 20),
    ]))
    els.append(cov)
    els.append(sp(14))

    # System-specific finding
    els.append(warn_box(
        "⚠  System-Specific Finding: TDNAME for EKPO (item text) on this system is constructed "
        "WITHOUT a space between PO number and item number.\n"
        "  Correct for this system:  CONCATENATE iv_ebeln iv_ebelp INTO lv_tdname.  "
        "(e.g. '450007774400010')\n"
        "  Standard documentation says: EBELN + SPACE + EBELP — NOT valid here.\n"
        "  Header EKKO TDNAME = EBELN only (e.g. '4500077744') — unchanged."
    ))
    els.append(sp(10))

    # Overview table
    els.append(Paragraph("The 4 Steps at a Glance", H2))
    els.append(tbl(
        ["Step", "Transaction", "Object Name", "Purpose"],
        [
            ["1", "SE11", "ZPO_LONGTEXT",          "Create custom table — stores plain readable text lines"],
            ["2", "SE24", "ZCL_PO_LONGTEXT_HANDLER","Create handler class — reads STXL via READ_TEXT, writes to ZPO_LONGTEXT"],
            ["3", "SE19", "ZCL_PO_TEXT_BADI_IMPL",  "Create BAdI — fires on PO save, calls handler automatically"],
            ["4", "ME21N + SE16N", "—",             "Test end-to-end — create PO with text, verify ZPO_LONGTEXT populated"],
        ],
        widths=[1.2*cm, 3*cm, 6.3*cm, 7*cm]
    ))
    els.append(sp(10))

    # TDID reference
    els.append(Paragraph("Text ID (TDID) Reference — Confirmed for This System", H2))
    els.append(tbl(
        ["TDOBJECT", "TDID", "Description", "TDNAME Format", "EBELP in ZPO_LONGTEXT"],
        [
            ["EKKO", "F01", "PO Header General Note",   "EBELN only (e.g. 4500077744)",        "00000"],
            ["EKKO", "F02", "PO Header Delivery Text",  "EBELN only",                           "00000"],
            ["EKPO", "F01*","PO Item General Note",     "EBELN+EBELP no space (450007774400010)","item no. e.g. 00010"],
            ["EKPO", "F09*","PO Item GR Text",          "EBELN+EBELP no space",                 "item no."],
        ],
        widths=[2.5*cm, 1.8*cm, 4.5*cm, 5.7*cm, 3*cm]
    ))
    els.append(sp(4))
    els.append(note_box(
        "* Confirm TDID from the STXH row you found. "
        "The TDID shown in STXH result is the one to use in READ_TEXT calls."
    ))
    els.append(PageBreak())
    return els

# ── Step 1: ZPO_LONGTEXT ──────────────────────────────────────────────────────
def step1():
    els = []
    els.append(sec_hdr("1", "SE11 — Create ZPO_LONGTEXT Table",
                       "Custom persistence table — stores decompressed plain text lines",
                       SAP_BLUE, SAP_DARK))
    els.append(sp(8))

    els.append(Paragraph("Why This Table Is Needed", H2))
    els.append(Paragraph(
        "SAP stores all long texts in STXH (header) and STXL (content). "
        "The content in STXL is COMPRESSED — it cannot be read by plain SQL SELECT. "
        "Every read requires calling function module READ_TEXT which decompresses on the fly. "
        "ZPO_LONGTEXT solves this by storing the same text in plain, human-readable format "
        "in a flat table — one row per text line.", BODY))
    els.append(sp(6))

    els.append(Paragraph("Table Definition — SE11 → Database Table → ZPO_LONGTEXT → Create", H2))
    els.append(tbl(
        ["Field", "Key", "Type", "Length", "Description"],
        [
            ["MANDT",        "✓", "CLNT",  "3",   "Client"],
            ["EBELN",        "✓", "CHAR",  "10",  "Purchase Order Number"],
            ["EBELP",        "✓", "NUMC",  "5",   "PO Item — 00000 for Header texts"],
            ["TDOBJECT",     "✓", "CHAR",  "10",  "Text Object: EKKO (header) or EKPO (item)"],
            ["TDID",         "✓", "CHAR",  "4",   "Text ID: F01, F02, F09 etc."],
            ["TDSPRAS",      "✓", "LANG",  "1",   "Language Key: D for German"],
            ["LINE_COUNTER", "✓", "NUMC",  "5",   "Line sequence: 00001, 00002, 00003..."],
            ["TDFORMAT",     "",  "CHAR",  "2",   "Format indicator — * = normal text line"],
            ["TDLINE",       "",  "CHAR",  "132", "Text line content — PLAIN readable text"],
            ["MIGRATED_AT",  "",  "DATS",  "8",   "Date this row was written"],
            ["MIGRATED_BY",  "",  "CHAR",  "12",  "User who wrote this row"],
            ["SOURCE",       "",  "CHAR",  "1",   "M = Migration program, D = Dual-write BAdI"],
        ],
        widths=[3.5*cm, 1.2*cm, 1.8*cm, 2*cm, 9*cm]
    ))
    els.append(sp(6))

    els.append(Paragraph("Technical Settings", H2))
    els.append(tbl(
        ["Setting", "Value", "Reason"],
        [
            ["Delivery Class",        "A",                       "Application data — written by customer processes"],
            ["Data Browser",          "Display/Maintenance Allowed", "Allows SE16N browsing"],
            ["Enhancement Category",  "Can Be Enhanced (Deep)",  "Future extensibility"],
            ["Buffering",             "Not buffered",            "Table is frequently written — no buffer"],
        ],
        widths=[5*cm, 6*cm, 6.5*cm]
    ))
    els.append(sp(6))

    els.append(Paragraph("What the Table Looks Like After Population", H2))
    els.append(code_block([
        "ZPO_LONGTEXT — sample data after BAdI dual-write:",
        "",
        "EBELN       EBELP  TDOBJECT TDID TDSPRAS LINE_COUNTER TDLINE                                    SOURCE",
        "─────────────────────────────────────────────────────────────────────────────────────────────────────",
        "4500077744  00000  EKKO     F01  D        00001        PO header note line 1                     D",
        "4500077744  00000  EKKO     F01  D        00002        PO header note line 2                     D",
        "4500077744  00010  EKPO     F01  D        00001        PO item 10 general note - test line 1     D",
        "4500077744  00010  EKPO     F01  D        00002        PO item 10 general note - test line 2 te  D",
        "",
        "Key points:",
        "  EBELP = 00000 for EKKO (header texts)",
        "  EBELP = 00010 for EKPO item 10 texts",
        "  TDLINE is PLAIN TEXT — no compression, no binary characters",
        "  LINE_COUNTER drives ORDER BY for correct text sequence",
        "  SOURCE = D means written by BAdI (Dual-write)",
    ]))
    els.append(sp(6))

    els.append(Paragraph("Recommended Secondary Index", H2))
    els.append(info_box(
        "SE11 → ZPO_LONGTEXT → Indexes → Create Index: ZPO_LT_I01\n"
        "Fields: EBELN, TDOBJECT, TDID\n"
        "Why: Most queries filter by EBELN + TDOBJECT + TDID. "
        "Without this index, large table scans slow down BDC programs."
    ))
    els.append(ok_box("✅  Step 1 complete when ZPO_LONGTEXT is Active in SE11 with all fields and primary key correct."))
    els.append(PageBreak())
    return els

# ── Step 2: ZCL_PO_LONGTEXT_HANDLER ──────────────────────────────────────────
def step2():
    els = []
    els.append(sec_hdr("2", "SE24 — Create ZCL_PO_LONGTEXT_HANDLER",
                       "Handler class — reads STXL via READ_TEXT, writes plain rows to ZPO_LONGTEXT",
                       ORANGE, SAP_DARK))
    els.append(sp(8))

    els.append(Paragraph("What This Class Does", H2))
    els.append(Paragraph(
        "This is the engine of the whole solution. It takes a PO number, text object, text ID "
        "and language — calls SAP function module READ_TEXT to decompress the text from STXL — "
        "then writes each plain text line as a separate row into ZPO_LONGTEXT. "
        "It is called by both the migration program and the BAdI.", BODY))
    els.append(sp(5))

    els.append(Paragraph("Class Definition — SE24 → ZCL_PO_LONGTEXT_HANDLER → Create", H2))
    els.append(tbl(
        ["Method", "Visibility", "Purpose"],
        [
            ["WRITE_TO_PERSISTENCE", "Public / Static",
             "Reads text from STXL via READ_TEXT. Deletes old rows. Inserts new plain rows into ZPO_LONGTEXT."],
            ["READ_FROM_PERSISTENCE", "Public / Static",
             "SELECT * FROM ZPO_LONGTEXT for a given EBELN. Returns plain text lines. No READ_TEXT needed."],
        ],
        widths=[5*cm, 3.5*cm, 9*cm]
    ))
    els.append(sp(6))

    els.append(Paragraph("WRITE_TO_PERSISTENCE — Full ABAP Code", H2))
    els.append(warn_box(
        "⚠  System-specific: TDNAME for EKPO uses NO SPACE between EBELN and EBELP on this system.\n"
        "  EKKO: lv_tdname = iv_ebeln  (e.g. '4500077744')\n"
        "  EKPO: CONCATENATE iv_ebeln iv_ebelp INTO lv_tdname  (e.g. '450007774400010')"
    ))
    els.append(sp(5))
    els.append(code_block([
        "CLASS zcl_po_longtext_handler DEFINITION PUBLIC FINAL CREATE PUBLIC.",
        "  PUBLIC SECTION.",
        "    CLASS-METHODS write_to_persistence",
        "      IMPORTING iv_ebeln    TYPE ebeln",
        "                iv_ebelp    TYPE ebelp    DEFAULT '00000'",
        "                iv_tdobject TYPE tdobject",
        "                iv_tdid     TYPE tdid",
        "                iv_tdspras  TYPE tdspras.",
        "",
        "    CLASS-METHODS read_from_persistence",
        "      IMPORTING iv_ebeln      TYPE ebeln",
        "      RETURNING VALUE(rt_lines) TYPE TABLE OF zpo_longtext.",
        "ENDCLASS.",
        "",
        "CLASS zcl_po_longtext_handler IMPLEMENTATION.",
        "",
        "  METHOD write_to_persistence.",
        "    DATA: lt_lines     TYPE TABLE OF tline,",
        "          lv_tdname    TYPE tdname,",
        "          lv_counter   TYPE numc5,",
        "          ls_persist   TYPE zpo_longtext.",
        "",
        "    \" Build TDNAME — system-specific: NO space for EKPO",
        "    IF iv_tdobject = 'EKKO'.",
        "      lv_tdname = iv_ebeln.",
        "    ELSE.",
        "      \" EKPO: concatenate WITHOUT space (confirmed for this system)",
        "      CONCATENATE iv_ebeln iv_ebelp INTO lv_tdname.",
        "    ENDIF.",
        "",
        "    \" Read and decompress text from STXH/STXL via READ_TEXT",
        "    CALL FUNCTION 'READ_TEXT'",
        "      EXPORTING",
        "        id       = iv_tdid",
        "        language = iv_tdspras",
        "        name     = lv_tdname",
        "        object   = iv_tdobject",
        "      TABLES",
        "        lines    = lt_lines",
        "      EXCEPTIONS",
        "        OTHERS   = 4.",
        "",
        "    IF sy-subrc <> 0 OR lt_lines IS INITIAL.",
        "      RETURN.  \" No text found — nothing to write",
        "    ENDIF.",
        "",
        "    \" Full refresh: delete existing rows for this text",
        "    DELETE FROM zpo_longtext",
        "      WHERE ebeln    = iv_ebeln",
        "        AND ebelp    = iv_ebelp",
        "        AND tdobject = iv_tdobject",
        "        AND tdid     = iv_tdid",
        "        AND tdspras  = iv_tdspras.",
        "",
        "    \" Insert one row per plain text line",
        "    LOOP AT lt_lines INTO DATA(ls_line).",
        "      ADD 1 TO lv_counter.",
        "      CLEAR ls_persist.",
        "      ls_persist-ebeln        = iv_ebeln.",
        "      ls_persist-ebelp        = iv_ebelp.",
        "      ls_persist-tdobject     = iv_tdobject.",
        "      ls_persist-tdid         = iv_tdid.",
        "      ls_persist-tdspras      = iv_tdspras.",
        "      ls_persist-line_counter = lv_counter.",
        "      ls_persist-tdformat     = ls_line-tdformat.",
        "      ls_persist-tdline       = ls_line-tdline.",
        "      ls_persist-migrated_at  = sy-datum.",
        "      ls_persist-migrated_by  = sy-uname.",
        "      ls_persist-source       = 'D'.",
        "      INSERT zpo_longtext FROM ls_persist.",
        "    ENDLOOP.",
        "  ENDMETHOD.",
        "",
        "  METHOD read_from_persistence.",
        "    SELECT * FROM zpo_longtext",
        "      INTO TABLE @rt_lines",
        "      WHERE ebeln = @iv_ebeln",
        "      ORDER BY tdobject, tdid, tdspras, line_counter.",
        "  ENDMETHOD.",
        "",
        "ENDCLASS.",
    ]))
    els.append(sp(6))
    els.append(ok_box("✅  Step 2 complete when class is Active (blue) in SE24 with no syntax errors."))
    els.append(PageBreak())
    return els

# ── Step 3: BAdI ──────────────────────────────────────────────────────────────
def step3():
    els = []
    els.append(sec_hdr("3", "SE19 — Create BAdI ZCL_PO_TEXT_BADI_IMPL",
                       "Fires automatically on every ME21N/ME22N PO save — dual-write trigger",
                       BTP_GREEN, SAP_DARK))
    els.append(sp(8))

    els.append(Paragraph("What This BAdI Does", H2))
    els.append(Paragraph(
        "A BAdI (Business Add-In) is a hook that SAP fires at a specific point in standard processing. "
        "ME_PROCESS_PO_CUST fires after a PO is saved in ME21N or ME22N — AFTER SAVE_TEXT has already "
        "written the text to STXH/STXL. At that point, the text exists in STXH and can be read by "
        "READ_TEXT. This BAdI calls the handler class to write the same text to ZPO_LONGTEXT in plain format.", BODY))
    els.append(sp(5))

    els.append(Paragraph("BAdI Registration Details", H2))
    els.append(tbl(
        ["Field", "Value"],
        [
            ["BAdI Name",          "ME_PROCESS_PO_CUST"],
            ["Enhancement Spot",   "ME_PURCHORD"],
            ["Implementation Class","ZCL_PO_TEXT_BADI_IMPL"],
            ["Interface",          "IF_EX_ME_PROCESS_PO_CUST"],
            ["Methods to implement","PROCESS_HEADER (header texts), PROCESS_ITEM (item texts)"],
        ],
        widths=[5*cm, 12.5*cm]
    ))
    els.append(sp(6))

    els.append(Paragraph("BAdI Implementation — Full ABAP Code", H2))
    els.append(code_block([
        "CLASS zcl_po_text_badi_impl DEFINITION PUBLIC FINAL CREATE PUBLIC.",
        "  PUBLIC SECTION.",
        "    INTERFACES if_ex_me_process_po_cust.",
        "ENDCLASS.",
        "",
        "CLASS zcl_po_text_badi_impl IMPLEMENTATION.",
        "",
        "  \" PROCESS_HEADER — fires when PO header is saved",
        "  \" Writes header texts (EKKO) to ZPO_LONGTEXT",
        "  METHOD if_ex_me_process_po_cust~process_header.",
        "    DATA(lv_ebeln) = im_header->get_data( )-ebeln.",
        "    IF lv_ebeln IS INITIAL. RETURN. ENDIF.",
        "",
        "    \" Write Header text (TDID confirmed from STXH — check your system)",
        "    zcl_po_longtext_handler=>write_to_persistence(",
        "      iv_ebeln    = lv_ebeln",
        "      iv_ebelp    = '00000'",
        "      iv_tdobject = 'EKKO'",
        "      iv_tdid     = 'F01'   \" Replace with actual TDID from STXH",
        "      iv_tdspras  = sy-langu ).",
        "",
        "    \" Write Header Delivery text if needed",
        "    zcl_po_longtext_handler=>write_to_persistence(",
        "      iv_ebeln    = lv_ebeln",
        "      iv_ebelp    = '00000'",
        "      iv_tdobject = 'EKKO'",
        "      iv_tdid     = 'F02'",
        "      iv_tdspras  = sy-langu ).",
        "  ENDMETHOD.",
        "",
        "  \" PROCESS_ITEM — fires when PO item is saved",
        "  \" Writes item texts (EKPO) to ZPO_LONGTEXT",
        "  METHOD if_ex_me_process_po_cust~process_item.",
        "    DATA(lv_ebeln) = im_item->get_data( )-ebeln.",
        "    DATA(lv_ebelp) = im_item->get_data( )-ebelp.",
        "    IF lv_ebeln IS INITIAL. RETURN. ENDIF.",
        "",
        "    \" Write Item text (TDID confirmed from STXH — check your system)",
        "    zcl_po_longtext_handler=>write_to_persistence(",
        "      iv_ebeln    = lv_ebeln",
        "      iv_ebelp    = lv_ebelp",
        "      iv_tdobject = 'EKPO'",
        "      iv_tdid     = 'F01'   \" Replace with actual TDID from STXH",
        "      iv_tdspras  = sy-langu ).",
        "  ENDMETHOD.",
        "",
        "ENDCLASS.",
    ]))
    els.append(sp(6))

    els.append(Paragraph("How to Create the BAdI in SE19", H2))
    els.append(tbl(
        ["Step", "Action"],
        [
            ["1", "SE19 → Create Implementation → enter BAdI Name: ME_PROCESS_PO_CUST → Enter"],
            ["2", "Implementation Name: ZCL_PO_TEXT_BADI_IMPL → Create"],
            ["3", "Interface tab → IF_EX_ME_PROCESS_PO_CUST → double-click PROCESS_HEADER → paste code"],
            ["4", "Double-click PROCESS_ITEM → paste code"],
            ["5", "Save → Activate (Ctrl+F3)"],
            ["6", "SE19 → verify implementation shows as Active (green dot, not grey)"],
        ],
        widths=[1.2*cm, 16.3*cm]
    ))
    els.append(sp(6))
    els.append(ok_box("✅  Step 3 complete when SE19 shows ZCL_PO_TEXT_BADI_IMPL as Active."))
    els.append(PageBreak())
    return els

# ── Step 4: Test ──────────────────────────────────────────────────────────────
def step4():
    els = []
    els.append(sec_hdr("4", "Test End-to-End — ME21N + SE16N Verify",
                       "Create PO with text → save → verify ZPO_LONGTEXT populated",
                       PURPLE, SAP_DARK))
    els.append(sp(8))

    els.append(Paragraph("Test Scenario — New PO with Header and Item Text", H2))
    els.append(tbl(
        ["Step", "Action", "Detail"],
        [
            ["1", "Create PO in ME21N",
             "ME21N → enter Vendor, Purchase Org, Company Code, Document Type NB"],
            ["2", "Add Header text",
             "Header → Texts → Text Overview → type in fields next to 'Header text'\n"
             "Line 1: Test header note line 1\nLine 2: Test header note line 2"],
            ["3", "Add PO line item",
             "Items section → Material, Quantity, Delivery Date, Plant"],
            ["4", "Add Item text",
             "Select Item 10 → Item → Texts → Text Overview\n"
             "Type in fields next to 'Item text'\n"
             "Line 1: Test item note line 1\nLine 2: Test item note line 2"],
            ["5", "Save PO",
             "Ctrl+S → status bar must show: Standard PO xxxxxxxxxx saved\nNote the new PO number"],
            ["6", "Verify STXH",
             "SE16 → STXH → TDOBJECT=EKKO, TDNAME=<PO#>, Language=D → 1 row ✓\n"
             "SE16 → STXH → TDOBJECT=EKPO, TDNAME=<PO#>00010, Language=D → 1 row ✓"],
            ["7", "Verify ZPO_LONGTEXT",
             "SE16N → ZPO_LONGTEXT → EBELN=<PO#> → Execute\n"
             "Expect 4 rows: 2 for EKKO/F01 + 2 for EKPO/F01\n"
             "TDLINE must contain plain readable text\n"
             "SOURCE must = D (Dual-write by BAdI)"],
        ],
        widths=[1*cm, 3.5*cm, 13*cm]
    ))
    els.append(sp(8))

    els.append(Paragraph("Expected ZPO_LONGTEXT Result", H2))
    els.append(code_block([
        "SE16N → ZPO_LONGTEXT → filter EBELN = <new PO number>",
        "",
        "EBELN       EBELP  TDOBJECT TDID TDSPRAS LINE_COUNTER TDLINE                      SOURCE",
        "────────────────────────────────────────────────────────────────────────────────────────",
        "<PO#>       00000  EKKO     F01  D        00001        Test header note line 1     D",
        "<PO#>       00000  EKKO     F01  D        00002        Test header note line 2     D",
        "<PO#>       00010  EKPO     F01  D        00001        Test item note line 1       D",
        "<PO#>       00010  EKPO     F01  D        00002        Test item note line 2       D",
    ]))
    els.append(sp(8))

    els.append(Paragraph("If ZPO_LONGTEXT Has No Rows — Debug Checklist", H2))
    els.append(tbl(
        ["Check", "How", "Fix"],
        [
            ["BAdI is Active",
             "SE19 → ME_PROCESS_PO_CUST → ZCL_PO_TEXT_BADI_IMPL → status",
             "Must show Active (green). If grey → activate."],
            ["Handler class is Active",
             "SE24 → ZCL_PO_LONGTEXT_HANDLER → status bar",
             "Must show Active. If inactive → Ctrl+F3 to activate."],
            ["ZPO_LONGTEXT exists",
             "SE11 → ZPO_LONGTEXT → Display",
             "Must exist and be Active. If not → complete Step 1."],
            ["TDID is correct",
             "Check STXH TDID column for your PO",
             "Update TDID in PROCESS_HEADER and PROCESS_ITEM to match."],
            ["TDNAME for EKPO correct",
             "STXH TDNAME for EKPO = 450007774400010 (no space)",
             "Confirm CONCATENATE in handler has no space for EKPO."],
            ["PO was saved not held",
             "Status bar after save shows 'saved' not 'held'",
             "If held → Edit → Release Hold → Ctrl+S again."],
        ],
        widths=[4*cm, 6*cm, 7.5*cm]
    ))
    els.append(sp(6))
    els.append(ok_box(
        "✅  Step 4 complete when ZPO_LONGTEXT shows rows with plain TDLINE text "
        "and SOURCE=D after saving a new PO with text in ME21N."
    ))
    els.append(PageBreak())
    return els

# ── Full Picture ──────────────────────────────────────────────────────────────
def full_picture():
    els = []
    els.append(sec_hdr("→", "Full Picture — How All 4 Steps Work Together",
                       "The complete dual-write flow from PO save to plain SQL access",
                       TEAL, SAP_DARK))
    els.append(sp(10))

    els.append(code_block([
        "┌─────────────────────────────────────────────────────────────────────────┐",
        "│              SINGLE SAP SYSTEM                                          │",
        "│                                                                         │",
        "│  User saves PO in ME21N / ME22N with Header and/or Item long text       │",
        "│        │                                                                │",
        "│        ▼                                                                │",
        "│  ┌─────────────────────────────────────────────────────────────┐       │",
        "│  │  SAP STANDARD — always runs, unchanged                       │       │",
        "│  │                                                              │       │",
        "│  │  SAVE_TEXT function module fires                             │       │",
        "│  │    → STXH: text header row (TDOBJECT, TDID, TDNAME, LANG)   │       │",
        "│  │    → STXL: compressed binary content (NOT human-readable)   │       │",
        "│  └──────────────────────────┬──────────────────────────────────┘       │",
        "│                             │                                           │",
        "│        ▼                                                                │",
        "│  ┌─────────────────────────────────────────────────────────────┐       │",
        "│  │  STEP 3 — BAdI: ZCL_PO_TEXT_BADI_IMPL (SE19)                │       │",
        "│  │  ME_PROCESS_PO_CUST fires AFTER SAVE_TEXT                   │       │",
        "│  │                                                              │       │",
        "│  │  PROCESS_HEADER: calls handler for EKKO texts                │       │",
        "│  │  PROCESS_ITEM:   calls handler for EKPO texts per item       │       │",
        "│  └──────────────────────────┬──────────────────────────────────┘       │",
        "│                             │                                           │",
        "│        ▼                                                                │",
        "│  ┌─────────────────────────────────────────────────────────────┐       │",
        "│  │  STEP 2 — ZCL_PO_LONGTEXT_HANDLER (SE24)                    │       │",
        "│  │                                                              │       │",
        "│  │  1. Build TDNAME:                                            │       │",
        "│  │     EKKO: lv_tdname = iv_ebeln           (4500077744)        │       │",
        "│  │     EKPO: CONCATENATE ebeln ebelp         (450007774400010)  │       │",
        "│  │          ← NO SPACE (system-specific)                        │       │",
        "│  │                                                              │       │",
        "│  │  2. CALL FUNCTION READ_TEXT                                  │       │",
        "│  │     → reads STXL, decompresses, returns plain TLINE table    │       │",
        "│  │                                                              │       │",
        "│  │  3. DELETE old rows from ZPO_LONGTEXT                        │       │",
        "│  │  4. INSERT one row per text line into ZPO_LONGTEXT           │       │",
        "│  └──────────────────────────┬──────────────────────────────────┘       │",
        "│                             │                                           │",
        "│        ▼                                                                │",
        "│  ┌─────────────────────────────────────────────────────────────┐       │",
        "│  │  STEP 1 — ZPO_LONGTEXT (SE11)                                │       │",
        "│  │                                                              │       │",
        "│  │  EBELN  EBELP  TDOBJECT TDID TDSPRAS LINE_COUNTER TDLINE    │       │",
        "│  │  PO#    00000  EKKO     F01  D        00001        Plain txt │       │",
        "│  │  PO#    00000  EKKO     F01  D        00002        Plain txt │       │",
        "│  │  PO#    00010  EKPO     F01  D        00001        Plain txt │       │",
        "│  │  PO#    00010  EKPO     F01  D        00002        Plain txt │       │",
        "│  │                                                              │       │",
        "│  │  → Plain SQL readable — no decompression needed              │       │",
        "│  │  → Used by BDC programs, reports, CDS views                 │       │",
        "│  └─────────────────────────────────────────────────────────────┘       │",
        "│                                                                         │",
        "│  BDC / Report reads text:                                               │",
        "│    SELECT * FROM zpo_longtext                                           │",
        "│      WHERE ebeln = '4500077744'                                         │",
        "│      ORDER BY tdobject, tdid, tdspras, line_counter.                   │",
        "│    → FAST, no READ_TEXT call needed                                     │",
        "└─────────────────────────────────────────────────────────────────────────┘",
    ]))

    els.append(sp(10))
    els.append(Paragraph("Key Rules — Never Forget", H2))
    els.append(tbl(
        ["Rule", "Detail"],
        [
            ["Never replace STXH/STXL",
             "ZPO_LONGTEXT runs ALONGSIDE classic framework. SAP standard continues writing to STXH/STXL unchanged."],
            ["EBELP = 00000 for header",
             "All EKKO texts (Header text, Delivery text etc.) use EBELP = 00000 in ZPO_LONGTEXT."],
            ["TDNAME for EKPO — NO SPACE",
             "This system: CONCATENATE iv_ebeln iv_ebelp INTO lv_tdname (e.g. 450007774400010)."],
            ["Always ORDER BY LINE_COUNTER",
             "Text lines must be read in LINE_COUNTER order to reconstruct the correct text sequence."],
            ["DELETE + INSERT not UPSERT",
             "Always delete old rows before inserting new ones — ensures deleted lines are removed too."],
            ["BAdI fires AFTER SAVE_TEXT",
             "Text must already be in STXH before READ_TEXT is called in the BAdI — this is guaranteed."],
            ["Confirm TDID from STXH",
             "Always verify the actual TDID from the STXH row before coding it into the handler."],
        ],
        widths=[5*cm, 12.5*cm]
    ))
    return els

# ── Build ─────────────────────────────────────────────────────────────────────
def build():
    doc = SimpleDocTemplate(
        OUTPUT, pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2*cm, bottomMargin=2*cm,
        title="PO Long Text 4-Step Implementation Guide",
        author="SAP PO Long Text Team",
    )
    story = []
    story.extend(cover())
    story.extend(step1())
    story.extend(step2())
    story.extend(step3())
    story.extend(step4())
    story.extend(full_picture())

    def on_page(c, doc):
        c.saveState()
        c.setFont("Helvetica", 7)
        c.setFillColor(colors.HexColor("#888888"))
        c.drawString(2*cm, 1.2*cm,
            "PO Long Text Persistency — 4-Step Implementation: SE11 → SE24 → SE19 → Test")
        c.drawRightString(19.5*cm, 1.2*cm, f"Page {doc.page}")
        c.setStrokeColor(colors.HexColor("#CCCCCC"))
        c.setLineWidth(0.4)
        c.line(2*cm, 1.5*cm, 19.5*cm, 1.5*cm)
        c.restoreState()

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print(f"PDF created: {OUTPUT}")

build()
