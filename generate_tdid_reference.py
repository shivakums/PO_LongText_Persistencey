from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

OUTPUT = r"C:\Users\I308878\PO_LongText_Persistencey\PO_Text_TDID_Reference.pdf"

SAP_DARK  = colors.HexColor("#003366")
SAP_BLUE  = colors.HexColor("#0070F2")
SAP_LIGHT = colors.HexColor("#E8F4FD")
ORANGE    = colors.HexColor("#E87722")
ORANGE_LT = colors.HexColor("#FFF3E8")
TEAL      = colors.HexColor("#007B8A")
TEAL_LT   = colors.HexColor("#E0F5F7")
GOLD      = colors.HexColor("#F0AB00")
GOLD_LT   = colors.HexColor("#FFFBE6")
RED       = colors.HexColor("#BB0000")
RED_LT    = colors.HexColor("#FFF0F0")
GREEN_OK  = colors.HexColor("#188918")
GREEN_LT  = colors.HexColor("#E6F4EA")
PURPLE    = colors.HexColor("#6B3FA0")
PURPLE_LT = colors.HexColor("#F0EAF8")
GREY_BG   = colors.HexColor("#F5F5F5")
GREY_BDR  = colors.HexColor("#CCCCCC")
CODE_BG   = colors.HexColor("#1E1E2E")
CODE_FG   = colors.HexColor("#CDD6F4")
WHITE     = colors.white
BLACK     = colors.black

W, H = A4
styles = getSampleStyleSheet()
def ms(name, **kw):
    return ParagraphStyle(name=name, parent=styles["Normal"], **kw)

TITLE  = ms("T",  fontSize=20, textColor=WHITE,   fontName="Helvetica-Bold", alignment=TA_CENTER, spaceAfter=4)
SUB    = ms("ST", fontSize=10, textColor=colors.HexColor("#AACCFF"), fontName="Helvetica", alignment=TA_CENTER, spaceAfter=2)
META   = ms("M",  fontSize=8,  textColor=colors.HexColor("#AACCFF"), fontName="Helvetica", alignment=TA_CENTER)
H1     = ms("H1", fontSize=12, textColor=WHITE,   fontName="Helvetica-Bold", spaceAfter=3)
H2     = ms("H2", fontSize=10, textColor=SAP_DARK,fontName="Helvetica-Bold", spaceAfter=3, spaceBefore=6)
BODY   = ms("B",  fontSize=8.5,textColor=BLACK,   leading=13, spaceAfter=3, alignment=TA_JUSTIFY)
BSML   = ms("BS", fontSize=8,  textColor=BLACK,   leading=12, spaceAfter=2)
CODE_S = ms("CS", fontSize=7.5,textColor=CODE_FG, fontName="Courier", leading=11, spaceAfter=1)
TH     = ms("TH", fontSize=8,  textColor=WHITE,   fontName="Helvetica-Bold", alignment=TA_CENTER)
TC     = ms("TC", fontSize=8,  textColor=BLACK,   leading=11)
TC_C   = ms("TCC",fontSize=8,  textColor=BLACK,   leading=11, alignment=TA_CENTER)
TC_G   = ms("TCG",fontSize=8,  textColor=GREEN_OK,fontName="Helvetica-Bold", leading=11, alignment=TA_CENTER)
TC_B   = ms("TCB",fontSize=8,  textColor=SAP_DARK,fontName="Helvetica-Bold", leading=11)
TC_O   = ms("TCO",fontSize=8,  textColor=ORANGE,  fontName="Helvetica-Bold", leading=11, alignment=TA_CENTER)
TC_T   = ms("TCT",fontSize=8,  textColor=TEAL,    fontName="Helvetica-Bold", leading=11, alignment=TA_CENTER)
PILL   = ms("PI", fontSize=8,  textColor=WHITE,   fontName="Helvetica-Bold", alignment=TA_CENTER)

def sp(n=5): return Spacer(1, n)

def sec_hdr(title, subtitle, color=SAP_DARK):
    t = Table([[Paragraph(title, H1)],[Paragraph(subtitle, ms("sh",fontSize=8,
               textColor=colors.HexColor("#AACCFF"),fontName="Helvetica-Oblique"))]],
              colWidths=[17.5*cm])
    t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),color),
                            ("TOPPADDING",(0,0),(-1,-1),9),("BOTTOMPADDING",(0,0),(-1,-1),9),
                            ("LEFTPADDING",(0,0),(-1,-1),14)]))
    return t

def ibox(text, bg=SAP_LIGHT, bdr=SAP_BLUE):
    t=Table([[Paragraph(text,BSML)]],colWidths=[17.5*cm])
    t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),bg),("LINEABOVE",(0,0),(-1,0),2,bdr),
                            ("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6),
                            ("LEFTPADDING",(0,0),(-1,-1),10),("RIGHTPADDING",(0,0),(-1,-1),8)]))
    return t

def ok_box(t):   return ibox(t, GREEN_LT, GREEN_OK)
def note_box(t): return ibox(t, GOLD_LT,  GOLD)
def warn_box(t): return ibox(t, RED_LT,   RED)

def code_block(lines):
    rows=[[Paragraph(l.replace(" ","&nbsp;").replace("<","&lt;").replace(">","&gt;") or "&nbsp;",CODE_S)] for l in lines]
    t=Table(rows,colWidths=[17.5*cm])
    t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),CODE_BG),
                            ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
                            ("LEFTPADDING",(0,0),(-1,-1),8),("RIGHTPADDING",(0,0),(-1,-1),6)]))
    return t

def tdid_table(headers, rows, widths, confirmed_rows=None):
    """Table with optional green highlight for confirmed rows."""
    data=[[Paragraph(h,TH) for h in headers]]
    for i,row in enumerate(rows):
        data.append([Paragraph(str(c),TC) for c in row])
    t=Table(data,colWidths=widths)
    style=[
        ("BACKGROUND",(0,0),(-1,0),SAP_BLUE),
        ("GRID",(0,0),(-1,-1),0.4,GREY_BDR),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
        ("LEFTPADDING",(0,0),(-1,-1),6),("VALIGN",(0,0),(-1,-1),"TOP"),
    ]
    if confirmed_rows:
        for r in confirmed_rows:
            style.append(("BACKGROUND",(0,r+1),(-1,r+1),colors.HexColor("#E6F9E6")))
    else:
        for i in range(len(rows)):
            style.append(("BACKGROUND",(0,i+1),(-1,i+1),WHITE if i%2==0 else GREY_BG))
    t.setStyle(TableStyle(style))
    return t

def badge(text, bg):
    t=Table([[Paragraph(text,PILL)]],colWidths=[2.5*cm])
    t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),bg),
                            ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
                            ("LEFTPADDING",(0,0),(-1,-1),4),("RIGHTPADDING",(0,0),(-1,-1),4)]))
    return t

# ══════════════════════════════════════════════════════════════════════════════
def cover():
    els=[]
    cov=Table([
        [Paragraph("PO Long Text — TDID Reference Guide", TITLE)],
        [Paragraph("All Text IDs for Purchase Order Header and Item Texts", SUB)],
        [Paragraph("TDOBJECT: EKKO (Header)  |  EKPO (Item)  |  ME21N / ME22N  |  2026-06-28", META)],
    ],colWidths=[17.5*cm])
    cov.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),SAP_DARK),
                              ("TOPPADDING",(0,0),(-1,-1),26),("BOTTOMPADDING",(0,0),(-1,-1),26),
                              ("LEFTPADDING",(0,0),(-1,-1),20)]))
    els.append(cov)
    els.append(sp(12))

    els.append(Paragraph("What is TDID?", H2))
    els.append(Paragraph(
        "TDID (Text ID) is a 4-character key in the SAP text framework that identifies "
        "which type of text is stored. Every long text in SAP has three identifiers: "
        "TDOBJECT (which business object), TDNAME (which document), and TDID (which text type). "
        "For Purchase Orders: TDOBJECT is EKKO for header texts and EKPO for item texts. "
        "TDID tells you whether it is a General Note, Delivery Text, GR Text etc.", BODY))
    els.append(sp(8))

    els.append(Paragraph("Quick Summary", H2))
    # Summary badges
    badge_data = [
        [Paragraph("EKKO / F01", ms("b1",fontSize=9,textColor=WHITE,fontName="Helvetica-Bold",alignment=TA_CENTER)),
         Paragraph("EKKO / F02", ms("b2",fontSize=9,textColor=WHITE,fontName="Helvetica-Bold",alignment=TA_CENTER)),
         Paragraph("EKPO / F01", ms("b3",fontSize=9,textColor=WHITE,fontName="Helvetica-Bold",alignment=TA_CENTER)),
         Paragraph("EKPO / F02", ms("b4",fontSize=9,textColor=WHITE,fontName="Helvetica-Bold",alignment=TA_CENTER)),
         Paragraph("EKPO / F09", ms("b5",fontSize=9,textColor=WHITE,fontName="Helvetica-Bold",alignment=TA_CENTER)),],
        [Paragraph("Header\nGeneral Note", ms("d1",fontSize=7.5,textColor=BLACK,alignment=TA_CENTER,leading=10)),
         Paragraph("Header\nDelivery Text", ms("d2",fontSize=7.5,textColor=BLACK,alignment=TA_CENTER,leading=10)),
         Paragraph("Item\nGeneral Note", ms("d3",fontSize=7.5,textColor=BLACK,alignment=TA_CENTER,leading=10)),
         Paragraph("Item\nDelivery Text", ms("d4",fontSize=7.5,textColor=BLACK,alignment=TA_CENTER,leading=10)),
         Paragraph("Item\nGR Text", ms("d5",fontSize=7.5,textColor=BLACK,alignment=TA_CENTER,leading=10)),],
    ]
    bt=Table(badge_data,colWidths=[3.5*cm]*5)
    bt.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(0,0),SAP_DARK),
        ("BACKGROUND",(1,0),(1,0),SAP_BLUE),
        ("BACKGROUND",(2,0),(2,0),TEAL),
        ("BACKGROUND",(3,0),(3,0),ORANGE),
        ("BACKGROUND",(4,0),(4,0),PURPLE),
        ("BACKGROUND",(0,1),(-1,1),GREY_BG),
        ("GRID",(0,0),(-1,-1),0.5,GREY_BDR),
        ("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6),
        ("ALIGN",(0,0),(-1,-1),"CENTER"),("VALIGN",(0,0),(-1,-1),"MIDDLE"),
    ]))
    els.append(bt)
    els.append(sp(10))

    els.append(ok_box(
        "✅  Confirmed for PO 4500077744 on this system:\n"
        "  EKKO / F01 — Header General Note  (EBELP = 00000)\n"
        "  EKKO / F02 — Header Delivery Text (EBELP = 00000)\n"
        "  EKPO / F01 — Item General Note    (EBELP = item number)\n"
        "  EKPO / F02 — Item Delivery Text   (EBELP = item number)"
    ))
    els.append(sp(10))

    # ── Full forms section ────────────────────────────────────────────────────
    els.append(Paragraph("Full Forms of All TD* Abbreviations", H2))
    els.append(Paragraph(
        "All SAP text framework field names start with the prefix TD — standing for "
        "Text Definition. These abbreviations appear throughout SE16, SE11, ABAP code "
        "and function module READ_TEXT / SAVE_TEXT.", BODY))
    els.append(sp(5))

    td_data = [
        ["Abbreviation","Full Form","Description"],
        ["TDID",       "Text ID",
         "4-char key identifying the type of text. F01=General Note, F02=Delivery Text, F09=GR Text etc."],
        ["TDNAME",     "Text Name",
         "The document key the text belongs to. For PO header = PO number (e.g. 4500077744). "
         "For PO item = PO number + item number (e.g. 450007774400010 — no space on this system)."],
        ["TDOBJECT",   "Text Object",
         "The business object type. EKKO = PO Header, EKPO = PO Item. "
         "Other examples: VBBK = Sales Order, AUFK = Production Order."],
        ["TDSPRAS",    "Text Language",
         "Language key for the text. D = German, E = English. Same text can exist in multiple languages."],
        ["TDFORMAT",   "Text Format",
         "Line format indicator. * = normal text line (most common). "
         "/: = special SAPscript formatting command."],
        ["TDLINE",     "Text Line",
         "The actual plain text content — one line of text, max 132 characters. "
         "This is the main field in ZPO_LONGTEXT — stored decompressed and human-readable."],
        ["STXH",       "SAP Text Header",
         "Standard SAP table. Stores one row per text block — the header/index record. "
         "Human-readable via SE16."],
        ["STXL",       "SAP Text Lines",
         "Standard SAP table. Stores compressed binary content of all text lines. "
         "NOT human-readable — must use READ_TEXT to decompress."],
    ]
    hdr2 = [[Paragraph(h,TH) for h in td_data[0]]]
    rows2 = []
    for i, row in enumerate(td_data[1:]):
        abbrv_color = SAP_DARK if row[0].startswith("TD") else TEAL
        rows2.append([
            Paragraph(row[0], ms(f"td{i}", fontSize=9, textColor=WHITE,
                      fontName="Helvetica-Bold", alignment=TA_CENTER)),
            Paragraph(row[1], ms(f"tf{i}", fontSize=8.5, textColor=SAP_DARK,
                      fontName="Helvetica-Bold")),
            Paragraph(row[2], BSML),
        ])
    tdt = Table(hdr2+rows2, colWidths=[2.5*cm, 3.5*cm, 11.5*cm])
    style2 = [
        ("BACKGROUND",    (0,0),(-1,0),  SAP_BLUE),
        ("GRID",          (0,0),(-1,-1), 0.4, GREY_BDR),
        ("TOPPADDING",    (0,0),(-1,-1), 5),
        ("BOTTOMPADDING", (0,0),(-1,-1), 5),
        ("LEFTPADDING",   (0,0),(-1,-1), 6),
        ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
    ]
    td_colors = [SAP_DARK, SAP_DARK, SAP_DARK, SAP_DARK, SAP_DARK, SAP_DARK, TEAL, TEAL]
    for i, col in enumerate(td_colors):
        style2.append(("BACKGROUND", (0,i+1),(0,i+1), col))
        style2.append(("BACKGROUND", (1,i+1),(-1,i+1), WHITE if i%2==0 else GREY_BG))
    tdt.setStyle(TableStyle(style2))
    els.append(tdt)
    els.append(sp(6))
    els.append(note_box(
        "TD prefix = Text Definition — the SAP SAPscript/text framework prefix used since R/3.\n"
        "STXH and STXL are the two underlying storage tables for ALL long texts in SAP "
        "(not just PO texts — also Sales Orders, Material texts, Customer texts etc.).\n"
        "ZPO_LONGTEXT is our custom table that makes PO text content accessible without "
        "the STXL decompression requirement."
    ))
    els.append(PageBreak())
    return els

# ── Section 1: Header TDIDs ───────────────────────────────────────────────────
def section1():
    els=[]
    els.append(sec_hdr("PO Header Text IDs — TDOBJECT = EKKO",
                        "Entered via: ME21N / ME22N → Header menu → Texts → Text Overview",
                        SAP_DARK))
    els.append(sp(8))
    els.append(Paragraph(
        "Header texts apply to the entire Purchase Order — not to individual line items. "
        "In STXH, the TDNAME for header texts = the PO number only (e.g. 4500077744). "
        "In ZPO_LONGTEXT, EBELP = 00000 for all header texts.", BODY))
    els.append(sp(6))

    els.append(tdid_table(
        ["TDID","Screen Label in ME21N/ME22N","Common Use","EBELP in ZPO_LONGTEXT","Confirmed"],
        [
            ["F01","Header text / Header note",
             "General notes about the PO — instructions to vendor, internal notes",
             "00000","✓ Confirmed"],
            ["F02","Delivery text",
             "Delivery instructions — packing, shipping, handling requirements",
             "00000","✓ Confirmed"],
            ["F03","Pricing types",
             "Notes about pricing conditions or price basis",
             "00000","—"],
            ["F04","Deadlines",
             "Important dates and deadline information for the vendor",
             "00000","—"],
            ["F05","Terms of delivery",
             "Incoterms, delivery conditions, freight terms",
             "00000","—"],
            ["F06","Shipping instructions",
             "Specific shipping instructions e.g. carrier, routing",
             "00000","—"],
            ["F07","Header memo",
             "Internal memo — not printed on PO output to vendor",
             "00000","—"],
        ],
        widths=[1.5*cm,4.5*cm,6*cm,3.5*cm,2*cm],
        confirmed_rows=[0,1]
    ))
    els.append(sp(8))

    els.append(note_box(
        "STXH TDNAME for EKKO = PO number only (e.g. 4500077744)\n"
        "All header TDIDs share the same TDNAME — they differ only by TDID.\n"
        "ZPO_LONGTEXT: EBELP = 00000 for ALL header texts regardless of TDID."
    ))
    els.append(sp(6))

    els.append(Paragraph("How to Check Which Header TDIDs Exist for Your PO", H2))
    els.append(code_block([
        "SE16 → STXH",
        "Filter: Text object = EKKO",
        "        Text Name   = 4500077744",
        "        Text ID     = (leave empty)",
        "Execute (F8) → shows ALL header TDIDs for this PO",
        "",
        "Example result:",
        "  EKKO  F01  DE  4500077744  ← General note",
        "  EKKO  F02  DE  4500077744  ← Delivery text",
    ]))
    els.append(PageBreak())
    return els

# ── Section 2: Item TDIDs ─────────────────────────────────────────────────────
def section2():
    els=[]
    els.append(sec_hdr("PO Item Text IDs — TDOBJECT = EKPO",
                        "Entered via: ME21N / ME22N → select item → Item menu → Texts → Text Overview",
                        TEAL))
    els.append(sp(8))
    els.append(Paragraph(
        "Item texts apply to individual line items. Each item has its own set of texts. "
        "In STXH, the TDNAME for item texts = PO number + item number with NO space "
        "(confirmed for this system: e.g. 450007774400010 for item 00010). "
        "In ZPO_LONGTEXT, EBELP = the actual item number (e.g. 00010, 00020).", BODY))
    els.append(sp(6))

    els.append(tdid_table(
        ["TDID","Screen Label in ME21N/ME22N","Common Use","EBELP in ZPO_LONGTEXT","Confirmed"],
        [
            ["F01","Item text / Item note",
             "General notes about this line item — specifications, instructions",
             "Item no. e.g. 00010","✓ Confirmed"],
            ["F02","Delivery text",
             "Delivery instructions specific to this item",
             "Item no.","✓ Confirmed"],
            ["F03","Item memo",
             "Internal memo for this item — not printed on PO output",
             "Item no.","—"],
            ["F09","GR text / Goods Receipt text",
             "Instructions shown during goods receipt posting for this item",
             "Item no.","—"],
            ["F11","Info record PO text",
             "Text copied from the purchasing info record — vendor/material specific",
             "Item no.","—"],
            ["F12","Material PO text",
             "Text copied from the material master — material description etc.",
             "Item no.","—"],
            ["F14","Info record note",
             "Additional note from the purchasing info record",
             "Item no.","—"],
        ],
        widths=[1.5*cm,4.5*cm,5.5*cm,3.5*cm,2.5*cm],
        confirmed_rows=[0,1]
    ))
    els.append(sp(8))

    els.append(warn_box(
        "⚠  System-Specific: EKPO TDNAME on this system has NO SPACE.\n"
        "  Item 00010: TDNAME = 450007774400010  (not '4500077744 00010')\n"
        "  Item 00020: TDNAME = 450007774400020\n"
        "  This is confirmed from STXH. The handler uses CONCATENATE without space."
    ))
    els.append(sp(6))

    els.append(Paragraph("How to Check Which Item TDIDs Exist for Your PO", H2))
    els.append(code_block([
        "SE16 → STXH",
        "Filter: Text object = EKPO",
        "        Text Name   = 450007774400010   ← item 00010",
        "        Text ID     = (leave empty)",
        "Execute (F8) → shows ALL TDIDs for item 00010",
        "",
        "Example result:",
        "  EKPO  F01  DE  450007774400010  ← Item general note",
        "  EKPO  F02  DE  450007774400010  ← Item delivery text",
        "",
        "Repeat for item 00020:",
        "  Text Name = 450007774400020",
    ]))
    els.append(PageBreak())
    return els

# ── Section 3: ZPO_LONGTEXT mapping ──────────────────────────────────────────
def section3():
    els=[]
    els.append(sec_hdr("How TDIDs Map to ZPO_LONGTEXT",
                        "Complete field mapping — STXH → ZPO_LONGTEXT", SAP_BLUE))
    els.append(sp(8))

    els.append(tdid_table(
        ["STXH TDOBJECT","STXH TDID","STXH TDNAME","ZPO TDOBJECT","ZPO TDID","ZPO EBELP","Description"],
        [
            ["EKKO","F01","4500077744",          "EKKO","F01","00000","Header General Note"],
            ["EKKO","F02","4500077744",          "EKKO","F02","00000","Header Delivery Text"],
            ["EKKO","F03","4500077744",          "EKKO","F03","00000","Header Pricing Types"],
            ["EKKO","F04","4500077744",          "EKKO","F04","00000","Header Deadlines"],
            ["EKKO","F05","4500077744",          "EKKO","F05","00000","Header Terms of Delivery"],
            ["EKPO","F01","450007774400010",     "EKPO","F01","00010","Item 10 General Note"],
            ["EKPO","F02","450007774400010",     "EKPO","F02","00010","Item 10 Delivery Text"],
            ["EKPO","F09","450007774400010",     "EKPO","F09","00010","Item 10 GR Text"],
            ["EKPO","F01","450007774400020",     "EKPO","F01","00020","Item 20 General Note"],
            ["EKPO","F02","450007774400020",     "EKPO","F02","00020","Item 20 Delivery Text"],
        ],
        widths=[2.5*cm,1.5*cm,4*cm,2.5*cm,1.5*cm,2*cm,3.5*cm]
    ))
    els.append(sp(8))

    els.append(Paragraph("Key Rules", H2))
    rules=[
        ("EBELP = 00000",
         "Always used for EKKO (header) texts — regardless of which TDID"),
        ("EBELP = item number",
         "Always used for EKPO (item) texts — 00010 for item 10, 00020 for item 20 etc."),
        ("TDNAME is NOT stored in ZPO_LONGTEXT",
         "ZPO_LONGTEXT stores EBELN + EBELP separately — TDNAME is reconstructed at runtime"),
        ("Handler reads ALL TDIDs",
         "ZTEST_PO_LONGTEXT_MIGRATE loops all STXH entries — no TDID hardcoding needed"),
        ("Each TDID = separate text block",
         "F01 and F02 for the same item are separate rows in STXH and separate groups in ZPO_LONGTEXT"),
    ]
    for rule, detail in rules:
        t=Table([[
            Paragraph(f"▸  {rule}", ms(f"rl{rule[:3]}",fontSize=8,textColor=SAP_DARK,
                      fontName="Helvetica-Bold")),
            Paragraph(detail, BSML),
        ]],colWidths=[5.5*cm,12*cm])
        t.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(0,0),SAP_LIGHT),
            ("BACKGROUND",(1,0),(1,0),WHITE),
            ("LINEABOVE",(0,0),(-1,0),0.3,GREY_BDR),
            ("LINEBELOW",(0,0),(-1,0),0.3,GREY_BDR),
            ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
            ("LEFTPADDING",(0,0),(-1,-1),8),("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ]))
        els.append(t)
        els.append(sp(3))
    els.append(PageBreak())
    return els

# ── Section 4: SE16 verification queries ─────────────────────────────────────
def section4():
    els=[]
    els.append(sec_hdr("How to Verify TDIDs in SE16 — Quick Reference",
                        "Copy these filters to confirm what texts exist for any PO", SAP_DARK))
    els.append(sp(8))

    els.append(Paragraph("SE16 → STXH — Filter Templates", H2))
    els.append(tdid_table(
        ["What to Check","Text object","Text Name","Text ID","Language"],
        [
            ["All header texts for PO",     "EKKO","4500077744",      "(empty)","DE"],
            ["Header General Note only",     "EKKO","4500077744",      "F01",    "DE"],
            ["Header Delivery Text only",    "EKKO","4500077744",      "F02",    "DE"],
            ["All item 10 texts",            "EKPO","450007774400010", "(empty)","DE"],
            ["Item 10 General Note only",    "EKPO","450007774400010", "F01",    "DE"],
            ["Item 10 Delivery Text only",   "EKPO","450007774400010", "F02",    "DE"],
            ["Item 10 GR Text only",         "EKPO","450007774400010", "F09",    "DE"],
            ["All item 20 texts",            "EKPO","450007774400020", "(empty)","DE"],
            ["All EKPO texts for this PO",   "EKPO","450007774499999", "(empty)","DE"],
        ],
        widths=[5.5*cm,2.5*cm,4.5*cm,2*cm,3*cm]
    ))
    els.append(sp(8))

    els.append(Paragraph("SE16N → ZPO_LONGTEXT — Verification Filters", H2))
    els.append(tdid_table(
        ["What to Check","EBELN","EBELP","TDOBJECT","TDID"],
        [
            ["All texts for PO",              "4500077744","(empty)","(empty)","(empty)"],
            ["All header texts",              "4500077744","00000",  "EKKO",   "(empty)"],
            ["Header General Note",           "4500077744","00000",  "EKKO",   "F01"],
            ["Header Delivery Text",          "4500077744","00000",  "EKKO",   "F02"],
            ["All item 10 texts",             "4500077744","00010",  "EKPO",   "(empty)"],
            ["Item 10 General Note",          "4500077744","00010",  "EKPO",   "F01"],
            ["Item 10 Delivery Text",         "4500077744","00010",  "EKPO",   "F02"],
            ["Item 20 General Note",          "4500077744","00020",  "EKPO",   "F01"],
        ],
        widths=[5.5*cm,3.5*cm,2.5*cm,3*cm,2.5*cm]
    ))
    els.append(sp(8))
    els.append(ok_box(
        "After running ZTEST_PO_LONGTEXT_MIGRATE — all STXH entries for PO 4500077744 "
        "should appear in ZPO_LONGTEXT. The updated migration report reads ALL TDIDs "
        "dynamically from STXH — no TDID needs to be hardcoded."
    ))
    return els

# ── Build ─────────────────────────────────────────────────────────────────────
def build():
    doc=SimpleDocTemplate(
        OUTPUT,pagesize=A4,
        leftMargin=2*cm,rightMargin=2*cm,
        topMargin=2*cm,bottomMargin=2*cm,
        title="PO Text TDID Reference Guide",
        author="SAP PO Long Text Team",
    )
    story=[]
    story.extend(cover())
    story.extend(section1())
    story.extend(section2())
    story.extend(section3())
    story.extend(section4())

    def on_page(c,doc):
        c.saveState()
        c.setFont("Helvetica",7)
        c.setFillColor(colors.HexColor("#888888"))
        c.drawString(2*cm,1.2*cm,"PO Long Text TDID Reference — EKKO Header & EKPO Item Text IDs")
        c.drawRightString(19.5*cm,1.2*cm,f"Page {doc.page}")
        c.setStrokeColor(colors.HexColor("#CCCCCC"))
        c.setLineWidth(0.4)
        c.line(2*cm,1.5*cm,19.5*cm,1.5*cm)
        c.restoreState()

    doc.build(story,onFirstPage=on_page,onLaterPages=on_page)
    print(f"PDF created: {OUTPUT}")

build()
