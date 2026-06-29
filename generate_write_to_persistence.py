from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

OUTPUT = r"C:\Users\I308878\PO_LongText_Persistencey\WRITE_TO_PERSISTENCE_Deep_Dive.pdf"

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
H3     = ms("H3", fontSize=9,  textColor=SAP_BLUE,fontName="Helvetica-Bold", spaceAfter=2, spaceBefore=4)
BODY   = ms("B",  fontSize=8.5,textColor=BLACK,   leading=13, spaceAfter=3, alignment=TA_JUSTIFY)
BSML   = ms("BS", fontSize=8,  textColor=BLACK,   leading=12, spaceAfter=2)
CODE_S = ms("CS", fontSize=7.5,textColor=CODE_FG, fontName="Courier", leading=11, spaceAfter=1)
TH     = ms("TH", fontSize=8,  textColor=WHITE,   fontName="Helvetica-Bold", alignment=TA_CENTER)
TC     = ms("TC", fontSize=8,  textColor=BLACK,   leading=11)
TC_B   = ms("TCB",fontSize=8,  textColor=SAP_DARK,fontName="Helvetica-Bold", leading=11)
TC_O   = ms("TCO",fontSize=8,  textColor=ORANGE,  fontName="Helvetica-Bold", leading=11, alignment=TA_CENTER)
TC_G   = ms("TCG",fontSize=8,  textColor=GREEN_OK,fontName="Helvetica-Bold", leading=11, alignment=TA_CENTER)
STEP_N = ms("SN", fontSize=20, textColor=WHITE,   fontName="Helvetica-Bold", alignment=TA_CENTER)
STEP_T = ms("STt",fontSize=11, textColor=WHITE,   fontName="Helvetica-Bold")
STEP_S = ms("SSb",fontSize=8,  textColor=colors.HexColor("#AACCFF"), fontName="Helvetica-Oblique")

def sp(n=5): return Spacer(1, n)

def sec_hdr(num, title, subtitle, hdr=SAP_DARK, nc=None):
    if not nc: nc=hdr
    nt=Table([[Paragraph(str(num),STEP_N)]],colWidths=[1.4*cm],rowHeights=[1.2*cm])
    nt.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),nc),("VALIGN",(0,0),(-1,-1),"MIDDLE")]))
    tt=Table([[Paragraph(title,STEP_T)],[Paragraph(subtitle,STEP_S)]],colWidths=[16.1*cm])
    tt.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),hdr),
                             ("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),7),
                             ("LEFTPADDING",(0,0),(-1,-1),12)]))
    t=Table([[nt,tt]],colWidths=[1.4*cm,16.1*cm])
    t.setStyle(TableStyle([("TOPPADDING",(0,0),(-1,-1),0),("BOTTOMPADDING",(0,0),(-1,-1),0),
                            ("LEFTPADDING",(0,0),(-1,-1),0),("VALIGN",(0,0),(-1,-1),"MIDDLE")]))
    return t

def tbl(headers, rows, widths=None):
    n=len(headers)
    if not widths: widths=[17.5*cm/n]*n
    data=[[Paragraph(h,TH) for h in headers]]
    for row in rows: data.append([Paragraph(str(c),TC) for c in row])
    t=Table(data,colWidths=widths)
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),SAP_BLUE),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[WHITE,GREY_BG]),
        ("GRID",(0,0),(-1,-1),0.4,GREY_BDR),
        ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
        ("LEFTPADDING",(0,0),(-1,-1),5),("VALIGN",(0,0),(-1,-1),"TOP"),
    ]))
    return t

def ibox(text, bg=SAP_LIGHT, bdr=SAP_BLUE):
    t=Table([[Paragraph(text,BSML)]],colWidths=[17.5*cm])
    t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),bg),("LINEABOVE",(0,0),(-1,0),2,bdr),
                            ("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6),
                            ("LEFTPADDING",(0,0),(-1,-1),10),("RIGHTPADDING",(0,0),(-1,-1),8)]))
    return t

def ok(t):   return ibox(t,GREEN_LT,GREEN_OK)
def note(t): return ibox(t,GOLD_LT, GOLD)
def warn(t): return ibox(t,RED_LT,  RED)

def code(lines):
    rows=[[Paragraph(l.replace(" ","&nbsp;").replace("<","&lt;").replace(">","&gt;") or "&nbsp;",CODE_S)] for l in lines]
    t=Table(rows,colWidths=[17.5*cm])
    t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),CODE_BG),
                            ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
                            ("LEFTPADDING",(0,0),(-1,-1),8),("RIGHTPADDING",(0,0),(-1,-1),6)]))
    return t

def step_card(number, title, subtitle, content_els, color=SAP_BLUE):
    """A numbered step card with content."""
    els = []
    nt=Table([[Paragraph(str(number),STEP_N)]],colWidths=[1.2*cm],rowHeights=[1.1*cm])
    nt.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),color),("VALIGN",(0,0),(-1,-1),"MIDDLE")]))
    tt=Table([[Paragraph(title,ms(f"st{number}",fontSize=9,textColor=WHITE,fontName="Helvetica-Bold"))],
              [Paragraph(subtitle,STEP_S)]],colWidths=[16.3*cm])
    tt.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),color),
                             ("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6),
                             ("LEFTPADDING",(0,0),(-1,-1),10)]))
    hdr=Table([[nt,tt]],colWidths=[1.2*cm,16.3*cm])
    hdr.setStyle(TableStyle([("TOPPADDING",(0,0),(-1,-1),0),("BOTTOMPADDING",(0,0),(-1,-1),0),
                              ("LEFTPADDING",(0,0),(-1,-1),0),("VALIGN",(0,0),(-1,-1),"MIDDLE")]))
    els.append(hdr)
    for el in content_els:
        els.append(el)
    bot=Table([[""]], colWidths=[17.5*cm],rowHeights=[2])
    bot.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),color)]))
    els.append(bot)
    els.append(sp(8))
    return KeepTogether(els)

# ══════════════════════════════════════════════════════════════════════════════
def cover():
    els=[]
    cov=Table([
        [Paragraph("WRITE_TO_PERSISTENCE", TITLE)],
        [Paragraph("Method Deep Dive — ZCL_PO_LONGTEXT_HANDLER", SUB)],
        [Paragraph("Every parameter explained  |  5-step internal flow  |  All field meanings  |  2026-06-28", META)],
    ],colWidths=[17.5*cm])
    cov.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),SAP_DARK),
                              ("TOPPADDING",(0,0),(-1,-1),24),("BOTTOMPADDING",(0,0),(-1,-1),24),
                              ("LEFTPADDING",(0,0),(-1,-1),20)]))
    els.append(cov)
    els.append(sp(12))

    els.append(Paragraph("One-Line Summary", H2))
    els.append(ibox(
        '"Read compressed text from SAP → decompress it → delete old version → '
        'store each line as plain readable row in ZPO_LONGTEXT."'
    ))
    els.append(sp(8))

    els.append(Paragraph("Why This Method Exists", H2))
    els.append(Paragraph(
        "SAP stores long texts in STXL in compressed binary format. You cannot read STXL "
        "with a plain SELECT — it is unreadable. Every time you need the text you must call "
        "READ_TEXT to decompress it. This is slow, cannot be used in CDS views, and cannot "
        "be used in BDC programs easily. WRITE_TO_PERSISTENCE solves this by decompressing "
        "ONCE and storing the result as plain rows in ZPO_LONGTEXT where any program can "
        "SELECT directly.", BODY))
    els.append(sp(8))

    els.append(tbl(
        ["Without ZPO_LONGTEXT","With ZPO_LONGTEXT (after WRITE_TO_PERSISTENCE)"],
        [
            ["CALL FUNCTION 'READ_TEXT' for every read — slow at scale",
             "SELECT * FROM zpo_longtext WHERE ebeln = '...' — instant"],
            ["STXL is compressed binary — cannot use in CDS view",
             "TDLINE is plain text — fully usable in CDS, reports, BDC"],
            ["Cannot join PO text with other tables in SQL",
             "Can join ZPO_LONGTEXT with EKKO, EKPO etc. in one SELECT"],
            ["READ_TEXT fails in background jobs silently",
             "Plain SQL always works in any context"],
        ],
        widths=[8.75*cm,8.75*cm]
    ))
    els.append(PageBreak())
    return els

# ── Parameters ────────────────────────────────────────────────────────────────
def params_section():
    els=[]
    els.append(sec_hdr("P","All 5 Parameters — Complete Reference",
                        "Every parameter with type, default, allowed values and purpose",
                        TEAL))
    els.append(sp(8))

    params=[
        ("IV_EBELN", "EBELN", "CHAR 10", "—", "Mandatory",
         "Purchase Order Number\n"
         "Example: '4500077744'\n"
         "Used for: (1) build TDNAME for READ_TEXT call  "
         "(2) stored as key in ZPO_LONGTEXT EBELN field"),
        ("IV_EBELP", "EBELP", "NUMC 5", "'00000'", "Optional",
         "PO Item Number\n"
         "Default '00000' = header text (TDOBJECT=EKKO)\n"
         "Pass explicitly for item texts: '00010', '00020' etc.\n"
         "Header call:  omit EBELP → defaults to 00000 automatically\n"
         "Item call:    must pass: iv_ebelp = '00010'"),
        ("IV_TDOBJECT", "TDOBJECT", "CHAR 10", "—", "Mandatory",
         "Text Object — identifies the SAP business object\n"
         "EKKO = Purchase Order Header text\n"
         "EKPO = Purchase Order Item text\n"
         "Controls TDNAME construction:\n"
         "  EKKO → TDNAME = EBELN only (e.g. 4500077744)\n"
         "  EKPO → TDNAME = EBELN+EBELP no space (e.g. 450007774400010)"),
        ("IV_TDID", "TDID", "CHAR 4", "—", "Mandatory",
         "Text ID — identifies which type of text\n"
         "F01 = General Note / Header Note  ← confirmed this system\n"
         "F02 = Delivery Text               ← confirmed this system\n"
         "F09 = Goods Receipt Text\n"
         "F03, F04, F05... other text types\n"
         "One PO can have F01 AND F02 — each requires a separate call"),
        ("IV_TDSPRAS", "TDSPRAS", "LANG 1", "—", "Mandatory",
         "Language Key\n"
         "D = German  ← confirmed this system\n"
         "E = English\n"
         "F = French etc.\n"
         "In BAdI: pass sy-langu (logged-in user language)\n"
         "Same PO text can exist in multiple languages — each language = separate rows"),
    ]

    for pname, ptype, plen, pdefault, pmand, pdesc in params:
        mand_color = GREEN_OK if pmand == "Mandatory" else ORANGE
        hdr_row = Table([[
            Paragraph(pname, ms(f"pn{pname}",fontSize=10,textColor=WHITE,fontName="Helvetica-Bold")),
            Paragraph(f"Type: {ptype} ({plen})", ms(f"pt{pname}",fontSize=8,textColor=colors.HexColor("#AACCFF"))),
            Paragraph(f"Default: {pdefault}", ms(f"pd{pname}",fontSize=8,textColor=colors.HexColor("#AACCFF"))),
            Paragraph(pmand, ms(f"pm{pname}",fontSize=8,textColor=WHITE,fontName="Helvetica-Bold",alignment=TA_CENTER)),
        ]], colWidths=[4.5*cm, 4*cm, 4*cm, 5*cm])
        hdr_row.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(2,0),SAP_DARK),
            ("BACKGROUND",(3,0),(3,0),mand_color),
            ("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6),
            ("LEFTPADDING",(0,0),(-1,-1),10),("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ]))
        desc_row = Table([[Paragraph(pdesc, BSML)]], colWidths=[17.5*cm])
        desc_row.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(-1,-1),GREY_BG),
            ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
            ("LEFTPADDING",(0,0),(-1,-1),14),
            ("LINEBELOW",(0,0),(-1,0),0.5,GREY_BDR),
        ]))
        els.append(hdr_row)
        els.append(desc_row)
        els.append(sp(5))

    els.append(sp(4))
    els.append(note(
        "IV_EBELP defaults to '00000' — this means for HEADER texts you can omit it:\n"
        "  write_to_persistence( iv_ebeln='4500077744' iv_tdobject='EKKO' iv_tdid='F01' iv_tdspras='D' )\n"
        "  ← IV_EBELP not passed → automatically = 00000\n"
        "For ITEM texts you MUST pass IV_EBELP explicitly:\n"
        "  write_to_persistence( iv_ebeln='4500077744' iv_ebelp='00010' iv_tdobject='EKPO' iv_tdid='F01' iv_tdspras='D' )"
    ))
    els.append(PageBreak())
    return els

# ── 5 Steps ───────────────────────────────────────────────────────────────────
def steps_section():
    els=[]
    els.append(sec_hdr("5","5-Step Internal Flow",
                        "What happens inside WRITE_TO_PERSISTENCE when you call it",
                        SAP_BLUE))
    els.append(sp(8))

    # Step 1
    els.append(step_card("1","Build TDNAME","Construct the key that READ_TEXT needs",[
        sp(4),
        Paragraph("READ_TEXT requires a field called TDNAME — the document key for the text. "
                  "It is built differently for header vs item:", BSML),
        sp(3),
        code([
            "IF iv_tdobject = 'EKKO'.           ← Header text",
            "  lv_tdname = iv_ebeln.             ← TDNAME = PO number only",
            "  \" Example: lv_tdname = '4500077744'",
            "",
            "ELSE.                               ← Item text (EKPO)",
            "  CONCATENATE iv_ebeln iv_ebelp INTO lv_tdname.",
            "  \" Example: lv_tdname = '450007774400010'  (NO space — confirmed this system)",
            "ENDIF.",
        ]),
        sp(3),
        tbl(
            ["Text Level","TDOBJECT","TDNAME Format","Example"],
            [
                ["Header","EKKO","EBELN only","4500077744"],
                ["Item","EKPO","EBELN + EBELP (no space)","450007774400010"],
            ],
            widths=[3*cm,3*cm,5.5*cm,6*cm]
        ),
        sp(3),
        warn("⚠  TDNAME for EKPO has NO SPACE on this system (confirmed from STXH). "
             "Standard SAP documentation says EBELN + SPACE + EBELP — NOT valid here."),
        sp(4),
    ], color=SAP_DARK))

    # Step 2
    els.append(step_card("2","Call READ_TEXT","Decompress text from STXL — the only way to read it",[
        sp(4),
        Paragraph("READ_TEXT is SAP's standard function module that reads and decompresses "
                  "text stored in STXL. It returns a plain TLINE table.", BSML),
        sp(3),
        code([
            "CALL FUNCTION 'READ_TEXT'",
            "  EXPORTING",
            "    id       = iv_tdid        ← F01, F02 etc.",
            "    language = iv_tdspras     ← D, E etc.",
            "    name     = lv_tdname      ← built in Step 1",
            "    object   = iv_tdobject    ← EKKO or EKPO",
            "  TABLES",
            "    lines    = lt_lines        ← returns plain text lines here",
            "  EXCEPTIONS",
            "    OTHERS   = 4.             ← sy-subrc = 4 if text not found",
            "",
            "What READ_TEXT does internally:",
            "  → Looks up STXH for matching TDOBJECT + TDID + TDSPRAS + TDNAME",
            "  → Gets the STXL cluster row (binary compressed data)",
            "  → Decompresses the binary → returns plain TLINE table",
            "",
            "lt_lines result (example — 2 lines of text):",
            "  TDFORMAT  TDLINE",
            "  *         PO header note line 1    ← * = normal text line",
            "  *         PO header note line 2",
        ]),
        sp(4),
    ], color=SAP_BLUE))

    # Step 3
    els.append(step_card("3","Check if Text Exists","Exit cleanly if no text found",[
        sp(4),
        code([
            "IF sy-subrc <> 0 OR lt_lines IS INITIAL.",
            "  RETURN.   ← exit — nothing to write",
            "ENDIF.",
            "",
            "When does this happen?",
            "  sy-subrc <> 0  → READ_TEXT failed:",
            "                   PO has no text for this TDID",
            "                   Wrong TDNAME was constructed",
            "  lt_lines IS INITIAL → Text header exists in STXH but content is empty",
        ]),
        sp(3),
        ok("✅  This RETURN is safe — it means no text exists for this combination. "
           "The method exits without writing anything to ZPO_LONGTEXT. "
           "No error, no dump — just a clean exit."),
        sp(4),
    ], color=GREEN_OK))

    # Step 4
    els.append(step_card("4","Delete Old Rows","Full refresh — remove previous version before inserting new",[
        sp(4),
        code([
            "DELETE FROM zpo_longtext",
            "  WHERE ebeln    = iv_ebeln",
            "    AND ebelp    = iv_ebelp",
            "    AND tdobject = iv_tdobject",
            "    AND tdid     = iv_tdid",
            "    AND tdspras  = iv_tdspras.",
        ]),
        sp(3),
        Paragraph("Why DELETE before INSERT — the stale data problem:", BSML),
        sp(3),
        tbl(
            ["Scenario","Without DELETE","With DELETE + INSERT"],
            [
                ["User had 3 text lines, reduced to 2 in ME22N",
                 "Old line 3 stays in ZPO_LONGTEXT — WRONG data",
                 "All 3 old lines deleted → 2 fresh lines inserted — CORRECT"],
                ["User changed text content",
                 "Old content + new content coexist — DUPLICATE",
                 "Old content deleted → new content only — CORRECT"],
                ["User deleted the text entirely",
                 "Stale rows remain forever — GHOST DATA",
                 "All rows deleted → nothing inserted (Step 3 returns) — CORRECT"],
            ],
            widths=[4*cm,6*cm,7.5*cm]
        ),
        sp(4),
    ], color=ORANGE))

    # Step 5
    els.append(step_card("5","Insert Plain Rows","One row per text line into ZPO_LONGTEXT",[
        sp(4),
        code([
            "LOOP AT lt_lines INTO DATA(ls_line).",
            "  ADD 1 TO lv_counter.              ← 00001, 00002, 00003...",
            "  CLEAR ls_persist.",
            "  ls_persist-ebeln        = iv_ebeln.       ← PO number",
            "  ls_persist-ebelp        = iv_ebelp.       ← 00000 or item#",
            "  ls_persist-tdobject     = iv_tdobject.    ← EKKO or EKPO",
            "  ls_persist-tdid         = iv_tdid.        ← F01, F02 etc.",
            "  ls_persist-tdspras      = iv_tdspras.     ← D",
            "  ls_persist-line_counter = lv_counter.     ← sequence number",
            "  ls_persist-tdformat     = ls_line-tdformat. ← * = normal line",
            "  ls_persist-tdline       = ls_line-tdline.   ← PLAIN TEXT content",
            "  ls_persist-migrated_at  = sy-datum.       ← today's date",
            "  ls_persist-migrated_by  = sy-uname.       ← current user",
            "  ls_persist-source       = 'D'.            ← D = Dual-write by BAdI",
            "  INSERT zpo_longtext FROM ls_persist.",
            "ENDLOOP.",
        ]),
        sp(4),
    ], color=PURPLE))

    els.append(PageBreak())
    return els

# ── Field meanings ────────────────────────────────────────────────────────────
def fields_section():
    els=[]
    els.append(sec_hdr("F","ZPO_LONGTEXT Field Meanings",
                        "What every field written by WRITE_TO_PERSISTENCE contains",
                        SAP_DARK))
    els.append(sp(8))

    els.append(tbl(
        ["Field","Set From","Example","Meaning"],
        [
            ["EBELN",        "iv_ebeln",       "4500077744",
             "PO number — links this row to the Purchase Order"],
            ["EBELP",        "iv_ebelp",       "00000 / 00010",
             "00000 = header text. 00010 = item 10 text. Drives header vs item distinction"],
            ["TDOBJECT",     "iv_tdobject",    "EKKO / EKPO",
             "EKKO = header, EKPO = item. Used in WHERE clauses to filter text level"],
            ["TDID",         "iv_tdid",        "F01 / F02",
             "Which text type. F01=General Note, F02=Delivery Text, F09=GR Text"],
            ["TDSPRAS",      "iv_tdspras",     "D",
             "Language key. Allows same PO to have texts in multiple languages"],
            ["LINE_COUNTER", "lv_counter",     "00001 / 00002",
             "Sequence within this text block. ORDER BY always uses this field"],
            ["TDFORMAT",     "ls_line-tdformat","*",
             "* = normal text line (what user typed). /: = SAPscript command (not user text)"],
            ["TDLINE",       "ls_line-tdline", "PO header note line 1",
             "THE MAIN FIELD — actual plain text content, max 132 chars. Human-readable."],
            ["MIGRATED_AT",  "sy-datum",       "20260628",
             "Date this row was written — audit trail for the persistence operation"],
            ["MIGRATED_BY",  "sy-uname",       "SUNDARAMURTS",
             "User who triggered the write — from BAdI save or manual migration run"],
            ["SOURCE",       "hard-coded 'D'", "D",
             "D = Dual-write by BAdI. M = written by migration report. Useful for debugging"],
        ],
        widths=[3*cm,3.5*cm,3.5*cm,7.5*cm]
    ))
    els.append(sp(8))

    els.append(Paragraph("SOURCE Field — D vs M", H2))
    els.append(tbl(
        ["Value","Full Meaning","When Written","How to Check"],
        [
            ["D","Dual-write",
             "Automatically by BAdI ZCL_PO_TEXT_BADI_IMPL on every ME21N/ME22N save",
             "SE16N → ZPO_LONGTEXT → SOURCE = D → new POs"],
            ["M","Migration",
             "By migration report ZTEST_PO_LONGTEXT_MIGRATE run manually for historic POs",
             "SE16N → ZPO_LONGTEXT → SOURCE = M → historic POs"],
        ],
        widths=[1.5*cm,3.5*cm,8*cm,4.5*cm]
    ))
    els.append(sp(8))

    els.append(Paragraph("LINE_COUNTER — Why It Matters", H2))
    els.append(code([
        "Without LINE_COUNTER you cannot guarantee text line order.",
        "",
        "Example — 3 lines of text in ZPO_LONGTEXT:",
        "  LINE_COUNTER=00001  TDLINE='First line of the header note'",
        "  LINE_COUNTER=00002  TDLINE='Second line of the header note'",
        "  LINE_COUNTER=00003  TDLINE='Third line of the header note'",
        "",
        "SELECT always includes:  ORDER BY tdobject, tdid, tdspras, line_counter",
        "This guarantees lines come back in correct sequence to reconstruct the text.",
        "",
        "If LINE_COUNTER had gaps (e.g. 00001, 00003 — missing 00002):",
        "  → Indicates a partial write failure during migration",
        "  → Re-run WRITE_TO_PERSISTENCE for that PO to fix",
    ]))
    els.append(sp(8))

    els.append(Paragraph("TDFORMAT = * — What It Means", H2))
    els.append(tbl(
        ["TDFORMAT Value","Meaning","In ZPO_LONGTEXT"],
        [
            ["*",   "Normal text line — what the user typed in ME21N", "TDLINE = readable text content"],
            ["/:",  "SAPscript formatting command line",               "TDLINE = formatting instruction — not user text"],
            ["/E",  "End of text marker",                              "Rarely appears in PO texts"],
        ],
        widths=[3.5*cm,8*cm,6*cm]
    ))
    els.append(sp(8))
    els.append(ok(
        "✅  Almost all ZPO_LONGTEXT rows will have TDFORMAT = *\n"
        "  This means TDLINE contains the actual readable text the user typed.\n"
        "  When reading ZPO_LONGTEXT in BDC or reports, you can typically ignore TDFORMAT\n"
        "  and just use TDLINE directly for display."
    ))
    els.append(PageBreak())
    return els

# ── Calling examples ──────────────────────────────────────────────────────────
def examples_section():
    els=[]
    els.append(sec_hdr("E","Complete Calling Examples",
                        "Copy-paste ready ABAP for all common scenarios",
                        TEAL))
    els.append(sp(8))

    els.append(Paragraph("Example 1 — Write Header General Note (F01)", H2))
    els.append(code([
        "\" Header text — IV_EBELP omitted (defaults to 00000)",
        "zcl_po_longtext_handler=>write_to_persistence(",
        "  iv_ebeln    = '4500077744'",
        "  iv_tdobject = 'EKKO'",
        "  iv_tdid     = 'F01'",
        "  iv_tdspras  = 'D' ).",
    ]))
    els.append(sp(6))

    els.append(Paragraph("Example 2 — Write Header Delivery Text (F02)", H2))
    els.append(code([
        "\" Different TDID — separate call for each text type",
        "zcl_po_longtext_handler=>write_to_persistence(",
        "  iv_ebeln    = '4500077744'",
        "  iv_ebelp    = '00000'   \" explicit — same as default",
        "  iv_tdobject = 'EKKO'",
        "  iv_tdid     = 'F02'",
        "  iv_tdspras  = 'D' ).",
    ]))
    els.append(sp(6))

    els.append(Paragraph("Example 3 — Write Item 10 General Note (EKPO/F01)", H2))
    els.append(code([
        "\" Item text — IV_EBELP MUST be passed explicitly",
        "zcl_po_longtext_handler=>write_to_persistence(",
        "  iv_ebeln    = '4500077744'",
        "  iv_ebelp    = '00010'   \" ← item number — mandatory for EKPO",
        "  iv_tdobject = 'EKPO'",
        "  iv_tdid     = 'F01'",
        "  iv_tdspras  = 'D' ).",
    ]))
    els.append(sp(6))

    els.append(Paragraph("Example 4 — Write All Texts for One PO (Migration Pattern)", H2))
    els.append(code([
        "\" Read all STXH entries for this PO and migrate each one",
        "DATA lv_ebeln  TYPE ebeln.",
        "DATA lt_stxh   TYPE TABLE OF stxh.",
        "DATA lv_ebelp  TYPE ebelp.",
        "DATA lv_tdname_lo TYPE thead-tdname.",
        "DATA lv_tdname_hi TYPE thead-tdname.",
        "",
        "lv_ebeln = '4500077744'.",
        "",
        "\" Header texts",
        "SELECT tdobject, tdid, tdspras FROM stxh",
        "  INTO CORRESPONDING FIELDS OF TABLE @lt_stxh",
        "  WHERE tdobject = 'EKKO' AND tdname = @lv_ebeln.",
        "",
        "\" Item texts (all items)",
        "CONCATENATE lv_ebeln '00000' INTO lv_tdname_lo.",
        "CONCATENATE lv_ebeln '99999' INTO lv_tdname_hi.",
        "SELECT tdobject, tdid, tdspras, tdname FROM stxh",
        "  APPENDING CORRESPONDING FIELDS OF TABLE @lt_stxh",
        "  WHERE tdobject = 'EKPO'",
        "    AND tdname >= @lv_tdname_lo AND tdname <= @lv_tdname_hi.",
        "",
        "LOOP AT lt_stxh INTO DATA(ls_stxh).",
        "  IF ls_stxh-tdobject = 'EKKO'.",
        "    lv_ebelp = '00000'.",
        "  ELSE.",
        "    lv_ebelp = ls_stxh-tdname+10(5).  \" parse item from TDNAME",
        "  ENDIF.",
        "",
        "  zcl_po_longtext_handler=>write_to_persistence(",
        "    iv_ebeln    = lv_ebeln",
        "    iv_ebelp    = lv_ebelp",
        "    iv_tdobject = ls_stxh-tdobject",
        "    iv_tdid     = ls_stxh-tdid",
        "    iv_tdspras  = ls_stxh-tdspras ).",
        "ENDLOOP.",
    ]))
    els.append(sp(6))

    els.append(Paragraph("Example 5 — Read Back from ZPO_LONGTEXT", H2))
    els.append(code([
        "DATA lt_texts TYPE ztt_po_longtext.",
        "",
        "zcl_po_longtext_handler=>read_from_persistence(",
        "  EXPORTING iv_ebeln = '4500077744'",
        "  IMPORTING et_lines = lt_texts ).",
        "",
        "LOOP AT lt_texts INTO DATA(ls_text).",
        "  WRITE: / ls_text-tdobject, ls_text-tdid,",
        "           'EBELP:', ls_text-ebelp,",
        "           'Line:', ls_text-line_counter,",
        "           ls_text-tdline.",
        "ENDLOOP.",
        "",
        "\" Output:",
        "\" EKKO F01 EBELP: 00000 Line: 00001 PO header note line 1",
        "\" EKKO F01 EBELP: 00000 Line: 00002 PO header note line 2",
        "\" EKPO F01 EBELP: 00010 Line: 00001 Item 10 note line 1",
    ]))
    return els

# ── Build ─────────────────────────────────────────────────────────────────────
def build():
    doc=SimpleDocTemplate(
        OUTPUT,pagesize=A4,
        leftMargin=2*cm,rightMargin=2*cm,
        topMargin=2*cm,bottomMargin=2*cm,
        title="WRITE_TO_PERSISTENCE Deep Dive",
        author="SAP PO Long Text Team",
    )
    story=[]
    story.extend(cover())
    story.extend(params_section())
    story.extend(steps_section())
    story.extend(fields_section())
    story.extend(examples_section())

    def on_page(c,doc):
        c.saveState()
        c.setFont("Helvetica",7)
        c.setFillColor(colors.HexColor("#888888"))
        c.drawString(2*cm,1.2*cm,
            "ZCL_PO_LONGTEXT_HANDLER — WRITE_TO_PERSISTENCE Deep Dive | All Parameters & Internal Flow")
        c.drawRightString(19.5*cm,1.2*cm,f"Page {doc.page}")
        c.setStrokeColor(colors.HexColor("#CCCCCC"))
        c.setLineWidth(0.4)
        c.line(2*cm,1.5*cm,19.5*cm,1.5*cm)
        c.restoreState()

    doc.build(story,onFirstPage=on_page,onLaterPages=on_page)
    print(f"PDF created: {OUTPUT}")

build()
