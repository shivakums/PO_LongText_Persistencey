from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

OUTPUT = r"C:\Users\I308878\PO_LongText_Persistencey\PO_LongText_TestCases.pdf"

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

# ── Styles ────────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()
def ms(name, **kw):
    return ParagraphStyle(name=name, parent=styles["Normal"], **kw)

TITLE    = ms("T",  fontSize=20, textColor=WHITE,   fontName="Helvetica-Bold", alignment=TA_CENTER, spaceAfter=4)
SUBTITLE = ms("ST", fontSize=10, textColor=colors.HexColor("#AACCFF"), fontName="Helvetica", alignment=TA_CENTER, spaceAfter=2)
META     = ms("M",  fontSize=8,  textColor=colors.HexColor("#AACCFF"), fontName="Helvetica", alignment=TA_CENTER)
H1       = ms("H1", fontSize=13, textColor=WHITE,   fontName="Helvetica-Bold", spaceAfter=3)
H2       = ms("H2", fontSize=11, textColor=SAP_DARK,fontName="Helvetica-Bold", spaceAfter=4, spaceBefore=8)
BODY     = ms("B",  fontSize=8.5,textColor=BLACK,   leading=13, spaceAfter=3, alignment=TA_JUSTIFY)
BODY_SML = ms("BS", fontSize=8,  textColor=BLACK,   leading=12, spaceAfter=2)
CODE_S   = ms("CS", fontSize=7.5,textColor=CODE_FG, fontName="Courier", leading=11, spaceAfter=1)
TH       = ms("TH", fontSize=8,  textColor=WHITE,   fontName="Helvetica-Bold", alignment=TA_CENTER)
TC       = ms("TC", fontSize=8,  textColor=BLACK,   leading=11)
STEPNUM  = ms("SN", fontSize=18, textColor=WHITE,   fontName="Helvetica-Bold", alignment=TA_CENTER)
STEPTIT  = ms("STt",fontSize=10, textColor=WHITE,   fontName="Helvetica-Bold")
STEPSUB  = ms("SSb",fontSize=8,  textColor=colors.HexColor("#AACCFF"), fontName="Helvetica-Oblique")

def sp(n=6): return Spacer(1, n)

# ── Helpers ───────────────────────────────────────────────────────────────────
def sec_hdr(title, subtitle="", color=SAP_DARK):
    rows = [[Paragraph(title, H1)]]
    if subtitle:
        rows.append([Paragraph(subtitle, STEPSUB)])
    t = Table(rows, colWidths=[17.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), color),
        ("TOPPADDING",    (0,0),(-1,-1), 9),
        ("BOTTOMPADDING", (0,0),(-1,-1), 9),
        ("LEFTPADDING",   (0,0),(-1,-1), 14),
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

def warn_box(text): return info_box(text, bg=RED_LIGHT,    border=RED)
def ok_box(text):   return info_box(text, bg=GREEN_LIGHT,  border=GREEN_OK)
def note_box(text): return info_box(text, bg=GOLD_LIGHT,   border=GOLD)

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

def tc_card(number, title, phase, system, steps_rows,
            verify_rows, pass_txt, fail_txt,
            hdr_color=SAP_BLUE, note=None):
    els = []
    # header
    num_t = Table([[Paragraph(str(number), STEPNUM)]],
                  colWidths=[1.4*cm], rowHeights=[1.3*cm])
    num_t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), hdr_color),
        ("VALIGN",    (0,0),(-1,-1),"MIDDLE"),
    ]))
    pha_t = Table([[Paragraph(phase, ms(f"ph{number}", fontSize=7.5, textColor=WHITE,
                   fontName="Helvetica-Bold", alignment=TA_CENTER))]],
                  colWidths=[2.8*cm], rowHeights=[1.3*cm])
    pha_color = GREEN_OK if "Phase 2" in phase else (ORANGE if "Validate" in phase else SAP_DARK)
    pha_t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), pha_color),
        ("VALIGN",    (0,0),(-1,-1),"MIDDLE"),
    ]))
    tit_t = Table([
        [Paragraph(title, STEPTIT)],
        [Paragraph(f"System: {system}", STEPSUB)],
    ], colWidths=[13.3*cm])
    tit_t.setStyle(TableStyle([
        ("BACKGROUND",   (0,0),(-1,-1), hdr_color),
        ("TOPPADDING",   (0,0),(-1,-1), 8),
        ("BOTTOMPADDING",(0,0),(-1,-1), 8),
        ("LEFTPADDING",  (0,0),(-1,-1), 10),
    ]))
    hdr = Table([[num_t, tit_t, pha_t]], colWidths=[1.4*cm, 13.3*cm, 2.8*cm])
    hdr.setStyle(TableStyle([
        ("TOPPADDING",   (0,0),(-1,-1), 0),
        ("BOTTOMPADDING",(0,0),(-1,-1), 0),
        ("LEFTPADDING",  (0,0),(-1,-1), 0),
        ("VALIGN",       (0,0),(-1,-1), "MIDDLE"),
    ]))
    els.append(hdr)

    # Steps
    sd = [[Paragraph("Step", TH), Paragraph("Action", TH), Paragraph("Detail / Input", TH)]]
    for i, (action, detail) in enumerate(steps_rows):
        sd.append([
            Paragraph(str(i+1), ms(f"sn{number}{i}", fontSize=9, textColor=hdr_color,
                      fontName="Helvetica-Bold", alignment=TA_CENTER)),
            Paragraph(action,   ms(f"sa{number}{i}", fontSize=8, textColor=BLACK, fontName="Helvetica-Bold")),
            Paragraph(detail, BODY_SML),
        ])
    st = Table(sd, colWidths=[0.9*cm, 4.2*cm, 12.4*cm])
    st.setStyle(TableStyle([
        ("BACKGROUND",     (0,0),(-1,0),  SAP_DARK),
        ("ROWBACKGROUNDS", (0,1),(-1,-1), [WHITE, GREY_BG]),
        ("GRID",           (0,0),(-1,-1), 0.4, GREY_BORDER),
        ("TOPPADDING",     (0,0),(-1,-1), 5),
        ("BOTTOMPADDING",  (0,0),(-1,-1), 5),
        ("LEFTPADDING",    (0,0),(-1,-1), 6),
        ("VALIGN",         (0,0),(-1,-1), "TOP"),
    ]))
    els.append(st)

    # Verify
    els.append(sp(3))
    vd = [[Paragraph("Verify Where", TH), Paragraph("What to Check", TH)]]
    for where, what in verify_rows:
        vd.append([Paragraph(where, ms(f"vw{number}", fontSize=8, textColor=TEAL,
                   fontName="Helvetica-Bold")), Paragraph(what, BODY_SML)])
    vt = Table(vd, colWidths=[4.5*cm, 13*cm])
    vt.setStyle(TableStyle([
        ("BACKGROUND",     (0,0),(-1,0),  TEAL),
        ("ROWBACKGROUNDS", (0,1),(-1,-1), [TEAL_LIGHT, WHITE]),
        ("GRID",           (0,0),(-1,-1), 0.4, GREY_BORDER),
        ("TOPPADDING",     (0,0),(-1,-1), 5),
        ("BOTTOMPADDING",  (0,0),(-1,-1), 5),
        ("LEFTPADDING",    (0,0),(-1,-1), 6),
        ("VALIGN",         (0,0),(-1,-1), "TOP"),
    ]))
    els.append(vt)

    # Pass/Fail
    els.append(sp(3))
    pf = Table([[
        Paragraph("✓  PASS", ms(f"pl{number}", fontSize=8, textColor=WHITE, fontName="Helvetica-Bold")),
        Paragraph(pass_txt, BODY_SML),
        Paragraph("✗  FAIL", ms(f"fl{number}", fontSize=8, textColor=WHITE, fontName="Helvetica-Bold", alignment=TA_CENTER)),
        Paragraph(fail_txt, BODY_SML),
    ]], colWidths=[1.8*cm, 6.95*cm, 1.8*cm, 6.95*cm])
    pf.setStyle(TableStyle([
        ("BACKGROUND",   (0,0),(0,0),  GREEN_OK),
        ("BACKGROUND",   (1,0),(1,0),  GREEN_LIGHT),
        ("BACKGROUND",   (2,0),(2,0),  RED),
        ("BACKGROUND",   (3,0),(3,0),  RED_LIGHT),
        ("TOPPADDING",   (0,0),(-1,-1), 6),
        ("BOTTOMPADDING",(0,0),(-1,-1), 6),
        ("LEFTPADDING",  (0,0),(-1,-1), 8),
        ("VALIGN",       (0,0),(-1,-1), "MIDDLE"),
    ]))
    els.append(pf)

    if note:
        els.append(sp(3))
        els.append(note_box(note))

    bot = Table([[""]], colWidths=[17.5*cm], rowHeights=[2])
    bot.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1), hdr_color)]))
    els.append(bot)
    els.append(sp(10))
    return KeepTogether(els)

# ══════════════════════════════════════════════════════════════════════════════
# CONTENT
# ══════════════════════════════════════════════════════════════════════════════
def cover():
    els = []
    cov = Table([
        [Paragraph("PO Long Text Persistency", TITLE)],
        [Paragraph("Test Cases: Create PO with Header &amp; Line Item Long Text", SUBTITLE)],
        [Paragraph("Validate Existence in STXH/STXL and ZPO_LONGTEXT", SUBTITLE)],
        [Paragraph("SAP ERP / S4HANA  |  Single System  |  BAdI ME_PROCESS_PO_CUST  |  2026-06-26", META)],
    ], colWidths=[17.5*cm])
    cov.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), SAP_DARK),
        ("TOPPADDING",    (0,0),(-1,-1), 28),
        ("BOTTOMPADDING", (0,0),(-1,-1), 28),
        ("LEFTPADDING",   (0,0),(-1,-1), 20),
    ]))
    els.append(cov)
    els.append(sp(14))

    # Overview
    els.append(Paragraph("Test Scope Overview", H2))
    els.append(tbl(
        ["TC#", "Test Case", "Phase", "What Is Tested"],
        [
            ["TC-01", "Prerequisites check",                  "Setup",    "BAdI active, ZPO_LONGTEXT exists, ME21N accessible"],
            ["TC-02", "Create PO with Header Long Text",      "Phase 2",  "EKKO/F01 header note written via ME21N"],
            ["TC-03", "Create PO with multiple Header Texts", "Phase 2",  "EKKO/F01 + EKKO/F02 both captured"],
            ["TC-04", "Create PO with Line Item Long Text",   "Phase 2",  "EKPO/F01 item note written per line item"],
            ["TC-05", "Create PO with Header + Item Texts",   "Phase 2",  "Full dual-write — header and all item texts"],
            ["TC-06", "Validate STXH/STXL (classic store)",  "Validate", "Classic framework has the text (source of truth)"],
            ["TC-07", "Validate ZPO_LONGTEXT (new store)",   "Validate", "New persistence table has flat text rows"],
            ["TC-08", "Change header text in ME22N",          "Phase 2",  "Updated text replaces old rows in ZPO_LONGTEXT"],
            ["TC-09", "Change item text in ME22N",            "Phase 2",  "Updated item text replaces old rows"],
            ["TC-10", "Validate TDNAME construction rules",   "Validate", "Header TDNAME=EBELN, Item TDNAME=EBELN+' '+EBELP"],
            ["TC-11", "Read text via SELECT (BDC use case)",  "Validate", "Direct SQL on ZPO_LONGTEXT — no READ_TEXT needed"],
            ["TC-12", "Empty text — no ZPO_LONGTEXT rows",    "Validate", "No text entered → no rows in ZPO_LONGTEXT"],
        ],
        widths=[1.5*cm, 6*cm, 2.5*cm, 7.5*cm]
    ))
    els.append(sp(10))

    # Text reference
    els.append(Paragraph("Text Object Reference — What Each TDID Means", H2))
    els.append(tbl(
        ["TDOBJECT", "TDID", "Level", "Description", "EBELP in ZPO_LONGTEXT"],
        [
            ["EKKO", "F01", "Header", "PO Header General Note",          "00000"],
            ["EKKO", "F02", "Header", "PO Header Delivery Text",         "00000"],
            ["EKKO", "F03", "Header", "PO Header Terms of Payment Text", "00000"],
            ["EKPO", "F01", "Item",   "PO Item General Note",            "item number e.g. 00010"],
            ["EKPO", "F02", "Item",   "PO Item Delivery Text",           "item number e.g. 00010"],
            ["EKPO", "F09", "Item",   "PO Item Goods Receipt Text",      "item number e.g. 00010"],
        ],
        widths=[2.5*cm, 1.8*cm, 2*cm, 6.5*cm, 4.7*cm]
    ))
    els.append(sp(8))
    els.append(note_box(
        "TDNAME in STXH is constructed differently for header vs item:\n"
        "  Header (EKKO): TDNAME = EBELN (10 chars, e.g. 4500001234)\n"
        "  Item   (EKPO): TDNAME = EBELN + space + EBELP (e.g. 4500001234 00010)\n"
        "Wrong TDNAME = READ_TEXT returns nothing. Always parse carefully."
    ))
    els.append(PageBreak())
    return els

# ── TC-01 Prerequisites ───────────────────────────────────────────────────────
def tc01():
    return [tc_card(
        "01", "Prerequisites — Verify All Components Are in Place",
        "Setup", "SAP ERP / S4HANA",
        [
            ("Check ZPO_LONGTEXT exists",
             "SE11 → Database Table → ZPO_LONGTEXT → Display\n"
             "Table must exist with fields: EBELN, EBELP, TDOBJECT, TDID, TDSPRAS, LINE_COUNTER, TDFORMAT, TDLINE, MIGRATED_AT, SOURCE"),
            ("Check BAdI is active",
             "SE19 → BAdI Name: ME_PROCESS_PO_CUST → Display\n"
             "Verify implementation ZCL_PO_TEXT_BADI_IMPL exists and is ACTIVE (not deactivated)"),
            ("Check handler class exists",
             "SE24 → Class: ZCL_PO_LONGTEXT_HANDLER → Display\n"
             "Methods: WRITE_TO_PERSISTENCE and READ_FROM_PERSISTENCE must exist"),
            ("Check ME21N access",
             "Transaction: ME21N → confirm screen opens without errors"),
            ("Verify language setting",
             "System → User Profile → Own Data → Logon Language\n"
             "Note your language (EN = E, DE = D etc.) — texts will be stored with this language key"),
        ],
        [
            ("SE11 → ZPO_LONGTEXT",     "Table exists and is Active. All key fields present."),
            ("SE19 → ME_PROCESS_PO_CUST","ZCL_PO_TEXT_BADI_IMPL listed as Active implementation"),
            ("SE24 → ZCL_PO_LONGTEXT_HANDLER","Class exists with WRITE_TO_PERSISTENCE method"),
        ],
        "All components in place. Ready to run test cases.",
        "Missing component — implement ZPO_LONGTEXT table, BAdI, or handler class before proceeding.",
        hdr_color=SAP_DARK
    )]

# ── TC-02 Header Long Text ─────────────────────────────────────────────────────
def tc02():
    return [tc_card(
        "02", "Create PO with PO Header Long Text (EKKO / F01)",
        "Phase 2 — Dual Write", "ME21N",
        [
            ("Open ME21N",
             "Transaction: ME21N → press Enter → New PO creation screen opens"),
            ("Fill standard PO header fields",
             "Vendor: enter a valid vendor number\n"
             "Purchase Org, Purchase Group, Company Code: enter valid values\n"
             "Document Type: NB (Standard PO)"),
            ("Open Header Text",
             "Click 'Header' tab at the top → select 'Texts' sub-tab\n"
             "OR Menu: Header → Texts\n"
             "Text type list appears: General Note (F01), Delivery Text (F02) etc."),
            ("Enter Header General Note (F01)",
             "Click on 'General Note' text type (TDID = F01)\n"
             "A text editor opens. Type the following test text:\n"
             "  Line 1: This is PO header general note - test line 1\n"
             "  Line 2: This is PO header general note - test line 2\n"
             "  Line 3: Third line of header note"),
            ("Add at least one PO line item",
             "Go to 'Items' section → enter:\n"
             "  Material: any valid material\n"
             "  Quantity: 1\n"
             "  Delivery Date: future date\n"
             "  Plant: valid plant"),
            ("Save the PO",
             "Click Save (floppy disk icon) or press Ctrl+S\n"
             "Note the PO number displayed in the status bar (e.g. 4500001234)"),
        ],
        [
            ("Status bar after save",   "PO number displayed e.g. 'Standard PO 4500001234 created'"),
            ("ME23N → Header → Texts",  "Open saved PO → Header → Texts → General Note → text lines visible"),
            ("SE16 → STXH",             "Row exists: TDOBJECT=EKKO, TDID=F01, TDNAME=4500001234, TDSPRAS=E"),
            ("SE16 → ZPO_LONGTEXT",     "3 rows: EBELN=4500001234, EBELP=00000, TDOBJECT=EKKO, TDID=F01, LINE_COUNTER=00001/00002/00003"),
        ],
        "PO saved. STXH has header row. ZPO_LONGTEXT has 3 rows with correct TDLINE content. SOURCE=D.",
        "ZPO_LONGTEXT has no rows — check BAdI is active (SE19) and ZCL_PO_TEXT_BADI_IMPL is not deactivated.",
        hdr_color=SAP_BLUE
    )]

# ── TC-03 Multiple Header Texts ────────────────────────────────────────────────
def tc03():
    return [tc_card(
        "03", "Create PO with Multiple Header Text Types (F01 + F02)",
        "Phase 2 — Dual Write", "ME21N",
        [
            ("Create PO as in TC-02",
             "Repeat TC-02 steps 1-5 to create a new PO with standard header fields."),
            ("Enter Header General Note (F01)",
             "Header → Texts → General Note (F01)\n"
             "Enter: 'Header general note for multiple text test'"),
            ("Enter Header Delivery Text (F02)",
             "Header → Texts → Delivery Text (F02)\n"
             "Enter: 'Deliver to main warehouse, attention: goods receiving team'"),
            ("Save the PO",
             "Save → note the new PO number (e.g. 4500001235)"),
        ],
        [
            ("SE16 → STXH",          "2 rows: TDOBJECT=EKKO, TDID=F01 AND TDID=F02, same TDNAME"),
            ("SE16 → ZPO_LONGTEXT",  "Rows for BOTH F01 and F02:\n"
                                     "  EBELN=4500001235, EBELP=00000, TDOBJECT=EKKO, TDID=F01, LINE_COUNTER=00001\n"
                                     "  EBELN=4500001235, EBELP=00000, TDOBJECT=EKKO, TDID=F02, LINE_COUNTER=00001"),
        ],
        "ZPO_LONGTEXT has rows for both TDID=F01 and TDID=F02 under the same EBELN.",
        "Only one TDID present — BAdI PROCESS_HEADER only writing one text type. Check handler calls for F02.",
        hdr_color=SAP_BLUE
    )]

# ── TC-04 Item Long Text ───────────────────────────────────────────────────────
def tc04():
    return [tc_card(
        "04", "Create PO with Line Item Long Text (EKPO / F01)",
        "Phase 2 — Dual Write", "ME21N",
        [
            ("Open ME21N and fill header",
             "ME21N → fill Vendor, Purchase Org, Company Code as before."),
            ("Add PO line item",
             "Items section → enter Material, Quantity, Delivery Date, Plant for item 10."),
            ("Open Item Text for line 10",
             "Click on item 10 row to select it → click 'Item' tab\n"
             "Go to 'Texts' sub-tab under Item details\n"
             "OR: with item row selected → Menu: Item → Texts"),
            ("Enter Item General Note (F01)",
             "Click 'General Note' (TDID = F01)\n"
             "Text editor opens. Enter:\n"
             "  Line 1: Item 10 general note - first line\n"
             "  Line 2: Item 10 general note - second line"),
            ("Enter Item GR Text (F09)",
             "Click 'GR Text' (TDID = F09)\n"
             "Enter: 'Goods Receipt instruction for item 10 - handle with care'"),
            ("Save the PO",
             "Save → note PO number (e.g. 4500001236) and item number (00010)"),
        ],
        [
            ("ME23N → Item 10 → Texts",  "Item text editor shows F01 and F09 text content"),
            ("SE16 → STXH",              "Rows: TDOBJECT=EKPO, TDID=F01+F09, TDNAME='4500001236 00010' (with space)"),
            ("SE16 → ZPO_LONGTEXT",      "Rows: EBELN=4500001236, EBELP=00010, TDOBJECT=EKPO, TDID=F01\n"
                                         "      EBELN=4500001236, EBELP=00010, TDOBJECT=EKPO, TDID=F09"),
        ],
        "ZPO_LONGTEXT has EKPO rows with correct EBELP=00010 (item number) and TDLINE content.",
        "EBELP=00000 for item text — TDNAME parsing bug. EKPO EBELP must be item number NOT 00000.",
        hdr_color=ORANGE,
        note="CRITICAL: For item texts (TDOBJECT=EKPO), EBELP in ZPO_LONGTEXT must be the actual item "
             "number (e.g. 00010), NOT 00000. 00000 is reserved for header texts only. "
             "If EBELP=00000 appears for item text rows — the PROCESS_ITEM BAdI method has a bug "
             "in how it reads im_item->get_data()-ebelp."
    )]

# ── TC-05 Full PO Header + Item ────────────────────────────────────────────────
def tc05():
    return [tc_card(
        "05", "Create PO with Both Header and Line Item Long Texts",
        "Phase 2 — Dual Write", "ME21N",
        [
            ("Create PO with 2 line items",
             "ME21N → fill header → add TWO line items:\n"
             "  Item 10: Material A, Qty 5\n"
             "  Item 20: Material B, Qty 10"),
            ("Enter Header General Note",
             "Header → Texts → F01 → enter: 'Full test PO header note'"),
            ("Enter Item 10 General Note",
             "Select Item 10 → Item → Texts → F01 → enter: 'Item 10 note'"),
            ("Enter Item 20 General Note",
             "Select Item 20 → Item → Texts → F01 → enter: 'Item 20 note'"),
            ("Enter Item 20 GR Text",
             "Item 20 → Texts → F09 → enter: 'GR text for item 20'"),
            ("Save and note PO number",
             "Save → note PO number (e.g. 4500001237)"),
        ],
        [
            ("SE16 → ZPO_LONGTEXT count",
             "Filter EBELN=4500001237 → expect 4 distinct TDOBJECT+TDID combinations:\n"
             "  EKKO/F01 EBELP=00000 (header note)\n"
             "  EKPO/F01 EBELP=00010 (item 10 note)\n"
             "  EKPO/F01 EBELP=00020 (item 20 note)\n"
             "  EKPO/F09 EBELP=00020 (item 20 GR text)"),
            ("SE16 → STXH count",       "4 rows: EKKO/F01 + EKPO/F01 for 2 items + EKPO/F09 for item 20"),
            ("TDLINE content check",    "Each row in ZPO_LONGTEXT matches exactly what was typed in ME21N"),
        ],
        "ZPO_LONGTEXT has all 4 text combinations. Header EBELP=00000. Items EBELP=item number.",
        "Missing text combinations — check which BAdI method (PROCESS_HEADER or PROCESS_ITEM) is not triggering.",
        hdr_color=BTP_GREEN
    )]

# ── TC-06 Validate STXH/STXL ──────────────────────────────────────────────────
def tc06():
    return [tc_card(
        "06", "Validate Classic Text Store — STXH and STXL",
        "Validate — Classic Framework", "SE16 / SE16N",
        [
            ("Open SE16N for STXH",
             "SE16N → Table: STXH → press Enter"),
            ("Filter for PO header text",
             "Enter filter values:\n"
             "  TDOBJECT = EKKO\n"
             "  TDNAME   = <PO number e.g. 4500001234>\n"
             "  TDID     = F01\n"
             "Execute (F8)"),
            ("Note the STXH row fields",
             "Record: TDNAME, TDID, TDSPRAS, TDFM, TDLINESIZE\n"
             "This confirms the text header exists in classic framework"),
            ("Check STXL (compressed content)",
             "SE16N → STXL → filter RELID=TX, SRTF2=0, NAME=<same as STXH TDNAME>\n"
             "Rows exist but CLUSTD column content is NOT human-readable — compressed cluster"),
            ("Filter for PO item text",
             "STXH filter:\n"
             "  TDOBJECT = EKPO\n"
             "  TDNAME   = '4500001234 00010' (note the space between PO# and item#)\n"
             "  TDID     = F01"),
            ("Verify via READ_TEXT (optional)",
             "SE38 → run any test program or ABAP Console:\n"
             "  CALL FUNCTION 'READ_TEXT'\n"
             "    EXPORTING id='F01' language='E' name='4500001234' object='EKKO'\n"
             "    TABLES lines=lt_lines.\n"
             "  lt_lines should contain the text lines you entered"),
        ],
        [
            ("SE16N → STXH (header text)",  "Row exists: TDOBJECT=EKKO, TDID=F01, TDNAME=<PO#>, TDSPRAS=E"),
            ("SE16N → STXH (item text)",    "Row exists: TDOBJECT=EKPO, TDID=F01, TDNAME='<PO#> 00010' (with space)"),
            ("SE16N → STXL",               "Rows exist with same NAME — CLUSTD is unreadable compressed cluster"),
            ("READ_TEXT result",            "lt_lines table populated with the exact text entered in ME21N"),
        ],
        "STXH has rows for all texts entered. STXL has compressed content. READ_TEXT returns correct lines.",
        "STXH row missing — text was never saved (ME21N save issue). STXL missing — SAVE_TEXT not called.",
        hdr_color=PURPLE,
        note="STXL content is COMPRESSED — it will appear as unreadable binary characters in SE16. "
             "This is expected and correct. Do NOT try to read STXL content directly. "
             "Always use READ_TEXT to decompress. This is exactly why ZPO_LONGTEXT was created — "
             "to provide a plain-SQL-readable alternative."
    )]

# ── TC-07 Validate ZPO_LONGTEXT ───────────────────────────────────────────────
def tc07():
    return [tc_card(
        "07", "Validate New Persistence Table — ZPO_LONGTEXT",
        "Validate — New Store", "SE16N / SE16",
        [
            ("Open SE16N for ZPO_LONGTEXT",
             "SE16N → Table: ZPO_LONGTEXT → press Enter"),
            ("Filter for PO Header text",
             "Enter filter:\n"
             "  EBELN    = <PO number e.g. 4500001234>\n"
             "  EBELP    = 00000\n"
             "  TDOBJECT = EKKO\n"
             "  TDID     = F01\n"
             "Execute (F8)"),
            ("Verify header text rows",
             "Expect one row per line of text entered in ME21N.\n"
             "For 3 lines of text entered → 3 rows with LINE_COUNTER = 00001, 00002, 00003\n"
             "Check: TDLINE column contains the EXACT text entered (human-readable plain text)"),
            ("Filter for PO Item text",
             "New filter:\n"
             "  EBELN    = <same PO number>\n"
             "  EBELP    = 00010  (item number)\n"
             "  TDOBJECT = EKPO\n"
             "  TDID     = F01"),
            ("Verify item text rows",
             "One row per text line entered for item 10.\n"
             "LINE_COUNTER starts from 00001.\n"
             "EBELP must be 00010 — NOT 00000"),
            ("Check SOURCE field",
             "For new POs created via ME21N → SOURCE = D (Dual-write)\n"
             "For migrated historic POs → SOURCE = M (Migration)"),
            ("Check TDFORMAT field",
             "Most lines will have TDFORMAT = * (asterisk = normal text line)\n"
             "This is the standard SAVE_TEXT line format indicator"),
        ],
        [
            ("EBELN filter — header rows",   "Rows with EBELP=00000, TDOBJECT=EKKO, TDID=F01, TDLINE=text content, SOURCE=D"),
            ("EBELN filter — item rows",     "Rows with EBELP=00010, TDOBJECT=EKPO, TDID=F01, TDLINE=text content, SOURCE=D"),
            ("LINE_COUNTER sequence",        "00001, 00002, 00003... — no gaps in sequence"),
            ("TDLINE content",               "Matches exactly what was typed in ME21N text editor — no compression"),
            ("Cross-check row count",        "Number of ZPO_LONGTEXT rows per EBELN+EBELP+TDOBJECT+TDID = number of text lines entered"),
        ],
        "ZPO_LONGTEXT has correct rows. TDLINE is human-readable. SOURCE=D. EBELP correct for header and items.",
        "No rows or wrong EBELP — BAdI not firing or PROCESS_ITEM method has EBELP parsing bug.",
        hdr_color=TEAL
    )]

# ── TC-08 Change Header Text ───────────────────────────────────────────────────
def tc08():
    return [tc_card(
        "08", "Change Header Long Text in ME22N — ZPO_LONGTEXT Updated",
        "Phase 2 — Dual Write Update", "ME22N",
        [
            ("Open PO in ME22N",
             "ME22N → enter PO number from TC-02 (e.g. 4500001234) → press Enter"),
            ("Open Header Text",
             "Header → Texts → General Note (F01)"),
            ("Modify the text",
             "Change line 1 from original text to: 'UPDATED - Header general note line 1'\n"
             "Delete line 3 (so only 2 lines remain)\n"
             "Add new line: 'NEW LINE ADDED in ME22N update'"),
            ("Save the PO",
             "Save (Ctrl+S) → confirm save successful"),
        ],
        [
            ("SE16N → ZPO_LONGTEXT filter EBELN + F01",
             "Old rows DELETED and replaced with new rows.\n"
             "Now 3 rows: LINE_COUNTER 00001 (updated), 00002 (original), 00003 (new line).\n"
             "LINE_COUNTER 00003 old row (deleted line) NO LONGER exists."),
            ("STXH",    "Still has 1 row — TDNAME unchanged, just content updated"),
            ("STXL",    "Updated compressed content"),
        ],
        "ZPO_LONGTEXT rows fully replaced — DELETE + INSERT pattern. No stale old lines remain.",
        "Old rows still present alongside new rows — DELETE step missing in WRITE_TO_PERSISTENCE method.",
        hdr_color=SAP_BLUE
    )]

# ── TC-09 Change Item Text ─────────────────────────────────────────────────────
def tc09():
    return [tc_card(
        "09", "Change Item Long Text in ME22N — ZPO_LONGTEXT Updated",
        "Phase 2 — Dual Write Update", "ME22N",
        [
            ("Open PO in ME22N",
             "ME22N → enter PO number from TC-04 (e.g. 4500001236)"),
            ("Select item 10",
             "Click on item 10 row in Items section"),
            ("Open Item Text",
             "Item → Texts → General Note (F01)"),
            ("Modify item text",
             "Replace existing text with:\n"
             "  Line 1: UPDATED item 10 note - new content\n"
             "  Line 2: Additional update line"),
            ("Save the PO",
             "Save → confirm save"),
        ],
        [
            ("SE16N → ZPO_LONGTEXT",
             "Filter EBELN=4500001236, EBELP=00010, TDOBJECT=EKPO, TDID=F01\n"
             "Old rows gone — 2 new rows with updated TDLINE content. SOURCE=D."),
            ("STXH",  "Row still exists for EKPO/F01 with TDNAME='4500001236 00010'"),
        ],
        "ZPO_LONGTEXT item rows updated correctly. EBELP=00010 preserved.",
        "EBELP changed to 00000 after update — PROCESS_ITEM BAdI not reading item number correctly.",
        hdr_color=ORANGE
    )]

# ── TC-10 TDNAME Rules ─────────────────────────────────────────────────────────
def tc10():
    return [tc_card(
        "10", "Validate TDNAME Construction Rules in STXH",
        "Validate — TDNAME Format", "SE16N → STXH",
        [
            ("Filter STXH for header text",
             "SE16N → STXH → filter TDOBJECT=EKKO, TDNAME=<PO number>\n"
             "Example: TDNAME = '4500001234' (10 characters, no spaces, no item)"),
            ("Observe header TDNAME format",
             "TDNAME for EKKO = EBELN only (10 chars)\n"
             "Example: '4500001234' — left-justified, no padding needed"),
            ("Filter STXH for item text",
             "SE16N → STXH → filter TDOBJECT=EKPO, TDNAME like '4500001234*'\n"
             "Observe the TDNAME format for EKPO rows"),
            ("Observe item TDNAME format",
             "TDNAME for EKPO = EBELN (10 chars) + SPACE (1 char) + EBELP (5 chars)\n"
             "Example: '4500001234 00010' — total 16 chars with space at position 11"),
            ("Cross-check in ZPO_LONGTEXT",
             "Confirm ZPO_LONGTEXT stores EBELN and EBELP SEPARATELY (not as TDNAME):\n"
             "  SE16N → ZPO_LONGTEXT → EBELN=4500001234, EBELP=00010 in separate columns"),
        ],
        [
            ("STXH EKKO TDNAME",   "= EBELN only. '4500001234'. NO space, NO item number."),
            ("STXH EKPO TDNAME",   "= EBELN + ' ' + EBELP. '4500001234 00010'. ONE space between PO# and item#."),
            ("ZPO_LONGTEXT",       "EBELN and EBELP stored as separate key fields — no TDNAME column needed"),
        ],
        "TDNAME formats confirmed. Header=EBELN only. Item=EBELN+space+EBELP. ZPO_LONGTEXT splits correctly.",
        "Item TDNAME missing the space — parsed as '450000123400010' — READ_TEXT will return nothing.",
        hdr_color=RED,
        note="This is the most common bug in PO long text implementations. The SPACE between EBELN "
             "and EBELP in the EKPO TDNAME is mandatory. In ABAP: "
             "CONCATENATE iv_ebeln ' ' iv_ebelp INTO lv_tdname. "
             "Missing this space causes READ_TEXT to fail silently — sy-subrc=4, no error message, empty lines."
    )]

# ── TC-11 BDC Read via SQL ─────────────────────────────────────────────────────
def tc11():
    return [tc_card(
        "11", "Read PO Long Text via Direct SQL — BDC Use Case",
        "Validate — BDC / Reporting", "SE16N or ABAP Console",
        [
            ("Query header text via SE16N",
             "SE16N → ZPO_LONGTEXT → filter:\n"
             "  EBELN = <PO number>\n"
             "  EBELP = 00000\n"
             "  TDOBJECT = EKKO\n"
             "  TDID = F01\n"
             "  TDSPRAS = E\n"
             "Sort by LINE_COUNTER ascending"),
            ("Confirm TDLINE is plain text",
             "TDLINE column shows human-readable text — no binary characters, no compression"),
            ("Query item text via SE16N",
             "Filter: EBELN=<PO#>, EBELP=00010, TDOBJECT=EKPO, TDID=F01\n"
             "Rows ordered by LINE_COUNTER — text lines in correct sequence"),
            ("Simulate BDC ABAP SELECT",
             "ABAP Console or SE38 test:\n"
             "  SELECT * FROM zpo_longtext\n"
             "    WHERE ebeln = '4500001234'\n"
             "      AND tdobject = 'EKKO'\n"
             "      AND tdid = 'F01'\n"
             "      AND tdspras = 'E'\n"
             "    ORDER BY line_counter.\n"
             "Concatenate TDLINE values to reconstruct full text"),
        ],
        [
            ("SE16N result",        "Plain text in TDLINE — no decompression needed. ORDER BY LINE_COUNTER gives correct sequence."),
            ("ABAP SELECT result",  "Same lines as entered in ME21N — no READ_TEXT required. Fast and scalable."),
            ("Compare to READ_TEXT","Run READ_TEXT for same PO/TDID — lines must match ZPO_LONGTEXT TDLINE values exactly"),
        ],
        "Direct SQL on ZPO_LONGTEXT returns correct text. No READ_TEXT needed. BDC use case validated.",
        "TDLINE content differs from READ_TEXT — migration/dual-write wrote wrong content. Debug handler class.",
        hdr_color=BTP_GREEN
    )]

# ── TC-12 Empty Text ───────────────────────────────────────────────────────────
def tc12():
    return [tc_card(
        "12", "No Text Entered — No ZPO_LONGTEXT Rows Created",
        "Validate — Empty Text Handling", "ME21N → SE16N",
        [
            ("Create PO without any long text",
             "ME21N → fill all mandatory fields (Vendor, Items etc.)\n"
             "Do NOT enter any text in Header Texts or Item Texts\n"
             "Save the PO → note PO number"),
            ("Check STXH",
             "SE16N → STXH → filter TDOBJECT=EKKO, TDNAME=<new PO number>\n"
             "No rows expected — text was never saved"),
            ("Check ZPO_LONGTEXT",
             "SE16N → ZPO_LONGTEXT → filter EBELN=<new PO number>\n"
             "No rows expected — nothing to write if no text entered"),
            ("Verify BAdI behavior",
             "The BAdI PROCESS_HEADER fires but ZCL_PO_LONGTEXT_HANDLER calls READ_TEXT\n"
             "READ_TEXT returns sy-subrc ≠ 0 (text not found) → RETURN immediately\n"
             "No insert to ZPO_LONGTEXT — correct behavior"),
        ],
        [
            ("SE16N → STXH",          "No rows for this PO — confirmed no text was saved"),
            ("SE16N → ZPO_LONGTEXT",  "No rows for this PO — handler correctly skipped empty text"),
        ],
        "No rows in STXH or ZPO_LONGTEXT for PO with no text. Handler exits cleanly on empty READ_TEXT.",
        "Empty rows inserted (TDLINE blank) — BAdI missing the IF sy-subrc <> 0 OR lt_lines IS INITIAL check.",
        hdr_color=DARK_GREY
    )]

# ── Validation SQL Reference ───────────────────────────────────────────────────
def validation_reference():
    els = []
    els.append(sec_hdr("Quick Validation SQL Reference",
                       "Copy-paste queries for validating long text in all three tables", TEAL))
    els.append(sp(10))

    els.append(Paragraph("SE16N Quick Filters — Cheat Sheet", H2))
    els.append(tbl(
        ["What to Check", "Table", "Filter Values", "Expected Result"],
        [
            ["PO Header text exists (classic)",
             "STXH",
             "TDOBJECT=EKKO, TDNAME=<PO#>, TDID=F01",
             "1 row — text header record"],
            ["PO Item text exists (classic)",
             "STXH",
             "TDOBJECT=EKPO, TDNAME='<PO#> <item#>' (with space), TDID=F01",
             "1 row — item text header"],
            ["Compressed content exists",
             "STXL",
             "NAME=<same as STXH TDNAME>",
             "Rows with unreadable CLUSTD — expected"],
            ["Header text in new store",
             "ZPO_LONGTEXT",
             "EBELN=<PO#>, EBELP=00000, TDOBJECT=EKKO, TDID=F01",
             "1 row per text line, TDLINE=plain text, SOURCE=D"],
            ["Item text in new store",
             "ZPO_LONGTEXT",
             "EBELN=<PO#>, EBELP=<item#>, TDOBJECT=EKPO, TDID=F01",
             "1 row per text line, EBELP=item number NOT 00000"],
            ["All texts for one PO",
             "ZPO_LONGTEXT",
             "EBELN=<PO#> only",
             "All header + item texts combined, sorted by TDOBJECT+TDID+LINE_COUNTER"],
            ["Migration vs Dual-write",
             "ZPO_LONGTEXT",
             "EBELN=<PO#>, SOURCE=D or SOURCE=M",
             "D=written by BAdI (new PO), M=written by migration program"],
        ],
        widths=[4*cm, 3.5*cm, 5.5*cm, 4.5*cm]
    ))
    els.append(sp(8))

    els.append(Paragraph("ABAP SELECT Templates", H2))
    els.append(code_block([
        "\" === 1. Read all texts for a PO from ZPO_LONGTEXT (BDC use case) ===",
        "SELECT * FROM zpo_longtext",
        "  INTO TABLE @DATA(lt_all_texts)",
        "  WHERE ebeln = '4500001234'",
        "  ORDER BY tdobject, tdid, tdspras, line_counter.",
        "",
        "\" === 2. Read header general note (EKKO/F01) ===",
        "SELECT * FROM zpo_longtext",
        "  INTO TABLE @DATA(lt_header_note)",
        "  WHERE ebeln    = '4500001234'",
        "    AND ebelp    = '00000'",
        "    AND tdobject = 'EKKO'",
        "    AND tdid     = 'F01'",
        "    AND tdspras  = 'E'",
        "  ORDER BY line_counter.",
        "",
        "\" === 3. Read item note for item 10 (EKPO/F01) ===",
        "SELECT * FROM zpo_longtext",
        "  INTO TABLE @DATA(lt_item_note)",
        "  WHERE ebeln    = '4500001234'",
        "    AND ebelp    = '00010'",
        "    AND tdobject = 'EKPO'",
        "    AND tdid     = 'F01'",
        "    AND tdspras  = 'E'",
        "  ORDER BY line_counter.",
        "",
        "\" === 4. Count check — STXH vs ZPO_LONGTEXT (after migration) ===",
        "SELECT COUNT(*) FROM stxh",
        "  INTO @DATA(lv_stxh_count)",
        "  WHERE tdobject IN ('EKKO','EKPO').",
        "",
        "SELECT COUNT( DISTINCT ebeln, ebelp, tdobject, tdid, tdspras )",
        "  FROM zpo_longtext",
        "  INTO @DATA(lv_zpo_count).",
        "",
        "\" lv_stxh_count and lv_zpo_count should match after full migration.",
        "",
        "\" === 5. Find POs with text in STXH but missing from ZPO_LONGTEXT ===",
        "SELECT tdobject, tdid, tdspras, tdname",
        "  FROM stxh",
        "  INTO TABLE @DATA(lt_stxh)",
        "  WHERE tdobject IN ('EKKO','EKPO').",
        "",
        "\" Then check each against ZPO_LONGTEXT — rows missing = not migrated/dual-written",
    ]))
    els.append(sp(8))
    els.append(warn_box(
        "⚠  STXL content is ALWAYS compressed and unreadable via SE16. This is expected. "
        "Never try to read STXL directly. "
        "If TDLINE in ZPO_LONGTEXT appears compressed — the READ_TEXT call in the handler returned "
        "compressed content, which means an incorrect text framework was called. "
        "TDLINE in ZPO_LONGTEXT should always contain plain readable text."
    ))
    return els

# ── Build ─────────────────────────────────────────────────────────────────────
def build():
    doc = SimpleDocTemplate(
        OUTPUT, pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2*cm, bottomMargin=2*cm,
        title="PO Long Text Persistency Test Cases",
        author="SAP PO Long Text Team",
    )
    story = []
    story.extend(cover())
    story.extend(tc01())
    story.extend(tc02())
    story.extend(tc03())
    story.extend(tc04())
    story.extend(tc05())
    story.extend(tc06())
    story.extend(tc07())
    story.extend(tc08())
    story.extend(tc09())
    story.extend(tc10())
    story.extend(tc11())
    story.extend(tc12())
    story.extend(validation_reference())

    def on_page(c, doc):
        c.saveState()
        c.setFont("Helvetica", 7)
        c.setFillColor(colors.HexColor("#888888"))
        c.drawString(2*cm, 1.2*cm,
            "PO Long Text Persistency — Create PO with Header & Item Long Text | Validate STXH/STXL/ZPO_LONGTEXT")
        c.drawRightString(19.5*cm, 1.2*cm, f"Page {doc.page}")
        c.setStrokeColor(colors.HexColor("#CCCCCC"))
        c.setLineWidth(0.4)
        c.line(2*cm, 1.5*cm, 19.5*cm, 1.5*cm)
        c.restoreState()

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print(f"PDF created: {OUTPUT}")

build()
