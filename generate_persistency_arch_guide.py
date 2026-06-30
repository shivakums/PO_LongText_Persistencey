from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

OUTPUT = r"C:\Users\I308878\PO_LongText_Persistencey\PO_Notes_Persistency_Architecture_Guide.pdf"

SAP_DARK  = colors.HexColor("#003366")
SAP_BLUE  = colors.HexColor("#0070F2")
SAP_LIGHT = colors.HexColor("#E8F4FD")
BTP_GREEN = colors.HexColor("#1A6632")
BTP_LT    = colors.HexColor("#E6F4EA")
ORANGE    = colors.HexColor("#E87722")
ORANGE_LT = colors.HexColor("#FFF3E8")
TEAL      = colors.HexColor("#007B8A")
TEAL_LT   = colors.HexColor("#E0F5F7")
PURPLE    = colors.HexColor("#6B3FA0")
PURPLE_LT = colors.HexColor("#F0EAF8")
GOLD      = colors.HexColor("#F0AB00")
GOLD_LT   = colors.HexColor("#FFFBE6")
RED       = colors.HexColor("#BB0000")
RED_LT    = colors.HexColor("#FFF0F0")
GREEN_OK  = colors.HexColor("#188918")
GREEN_LT  = colors.HexColor("#E6F4EA")
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

TITLE  = ms("T",  fontSize=18, textColor=WHITE,   fontName="Helvetica-Bold", alignment=TA_CENTER, spaceAfter=4)
SUB    = ms("ST", fontSize=9,  textColor=colors.HexColor("#AACCFF"), fontName="Helvetica", alignment=TA_CENTER, spaceAfter=2)
META   = ms("M",  fontSize=7.5,textColor=colors.HexColor("#AACCFF"), fontName="Helvetica", alignment=TA_CENTER)
H1     = ms("H1", fontSize=12, textColor=WHITE,   fontName="Helvetica-Bold", spaceAfter=3)
H2     = ms("H2", fontSize=10, textColor=SAP_DARK,fontName="Helvetica-Bold", spaceAfter=3, spaceBefore=6)
H3     = ms("H3", fontSize=9,  textColor=SAP_BLUE,fontName="Helvetica-Bold", spaceAfter=2, spaceBefore=4)
BODY   = ms("B",  fontSize=8.5,textColor=BLACK,   leading=13, spaceAfter=3, alignment=TA_JUSTIFY)
BSML   = ms("BS", fontSize=8,  textColor=BLACK,   leading=12, spaceAfter=2)
CODE_S = ms("CS", fontSize=7,  textColor=CODE_FG, fontName="Courier", leading=10.5, spaceAfter=1)
TH     = ms("TH", fontSize=7.5,textColor=WHITE,   fontName="Helvetica-Bold", alignment=TA_CENTER)
TC     = ms("TC", fontSize=7.5,textColor=BLACK,   leading=10)
TC_B   = ms("TCB",fontSize=7.5,textColor=SAP_DARK,fontName="Helvetica-Bold", leading=10)
SN     = ms("SN", fontSize=16, textColor=WHITE,   fontName="Helvetica-Bold", alignment=TA_CENTER)
ST     = ms("STt",fontSize=10, textColor=WHITE,   fontName="Helvetica-Bold")
SS     = ms("SSb",fontSize=8,  textColor=colors.HexColor("#AACCFF"), fontName="Helvetica-Oblique")

def sp(n=5): return Spacer(1, n)

def sec_hdr(num, title, subtitle, hdr=SAP_DARK, nc=None):
    if not nc: nc=hdr
    nt=Table([[Paragraph(str(num),SN)]],colWidths=[1.3*cm],rowHeights=[1.1*cm])
    nt.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),nc),("VALIGN",(0,0),(-1,-1),"MIDDLE")]))
    tt=Table([[Paragraph(title,ST)],[Paragraph(subtitle,SS)]],colWidths=[16.2*cm])
    tt.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),hdr),
                             ("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),7),
                             ("LEFTPADDING",(0,0),(-1,-1),12)]))
    t=Table([[nt,tt]],colWidths=[1.3*cm,16.2*cm])
    t.setStyle(TableStyle([("TOPPADDING",(0,0),(-1,-1),0),("BOTTOMPADDING",(0,0),(-1,-1),0),
                            ("LEFTPADDING",(0,0),(-1,-1),0),("VALIGN",(0,0),(-1,-1),"MIDDLE")]))
    return t

def tbl(headers, rows, widths=None, hdr_color=SAP_BLUE):
    n=len(headers)
    if not widths: widths=[17.5*cm/n]*n
    data=[[Paragraph(h,TH) for h in headers]]
    for row in rows: data.append([Paragraph(str(c),TC) for c in row])
    t=Table(data,colWidths=widths)
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),hdr_color),
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

def table_struct(title, fields, color):
    """Renders a table structure box."""
    hdr=Table([[Paragraph(title,ms(f"ts{title[:3]}",fontSize=8.5,textColor=WHITE,fontName="Helvetica-Bold"))]],
              colWidths=[17.5*cm])
    hdr.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),color),
                              ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
                              ("LEFTPADDING",(0,0),(-1,-1),10)]))
    rows=[[Paragraph(f[0],ms(f"fn{f[0]}",fontSize=7.5,textColor=color,fontName="Helvetica-Bold")),
           Paragraph(f[1],TC),
           Paragraph(f[2],BSML)] for f in fields]
    body=Table(rows,colWidths=[4.5*cm,3*cm,10*cm])
    body.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(0,-1),colors.HexColor("#F5F5F5")),
        ("GRID",(0,0),(-1,-1),0.3,GREY_BDR),
        ("TOPPADDING",(0,0),(-1,-1),3),("BOTTOMPADDING",(0,0),(-1,-1),3),
        ("LEFTPADDING",(0,0),(-1,-1),6),("VALIGN",(0,0),(-1,-1),"MIDDLE"),
    ]))
    bot=Table([[""]], colWidths=[17.5*cm],rowHeights=[2])
    bot.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),color)]))
    return KeepTogether([hdr,body,bot,sp(6)])

# ══════════════════════════════════════════════════════════════════════════════
def cover():
    els=[]
    cov=Table([
        [Paragraph("PO Notes New Persistency", TITLE)],
        [Paragraph("Architecture Comparison &amp; Recommendation Guide", SUB)],
        [Paragraph("Notes Reuse RAP  |  Sales SDD Own Table  |  ZPO_LONGTEXT  |  SAPScript Handler  |  SDM", SUB)],
        [Paragraph("SAP S/4HANA Procurement  |  EKKO / EKPO  |  CE2702 / CE2708 Planning  |  2026-06-30", META)],
    ],colWidths=[17.5*cm])
    cov.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),SAP_DARK),
                              ("TOPPADDING",(0,0),(-1,-1),24),("BOTTOMPADDING",(0,0),(-1,-1),24),
                              ("LEFTPADDING",(0,0),(-1,-1),20)]))
    els.append(cov)
    els.append(sp(12))

    els.append(Paragraph("What This Document Covers", H2))
    els.append(tbl(
        ["Section","Title","Key Content"],
        [
            ["1","Three Persistency Approaches","Generic table, Own table, RAP Notes Reuse — table structures"],
            ["2","Sales SDD Table Design","SDTP_TEXT fields, ITF conversion, auth encoding"],
            ["3","ZPO_LONGTEXT Current Design","Current Lift & Shift table structure"],
            ["4","Full Comparison Table","All aspects side by side across all 3 approaches"],
            ["5","Recommendation for PO","Which approach and why — proposed EKKT_TEXT design"],
            ["6","SAPScript Handler Class","What it is, how it works, analogy"],
            ["7","SDM — Silent Data Migration","What SDM does, step by step, how it connects to handler"],
            ["8","Handler vs SDM — Key Difference","Summary table and one-line definitions"],
        ],
        widths=[1.5*cm,5.5*cm,10.5*cm]
    ))
    els.append(sp(8))
    els.append(note(
        "Context: CE2702/CE2708 sync-up meeting (2026-06-25) identified 3 persistency options for PO notes "
        "migration. Sales team completed their migration in CE2608 as the reference implementation. "
        "The critical open question — can application-specific own table work with Notes Reuse RAP — "
        "is pending with the Notes Reuse team."
    ))
    els.append(PageBreak())
    return els

# ── Section 1: Three approaches ───────────────────────────────────────────────
def section1():
    els=[]
    els.append(sec_hdr("1","Three Persistency Approaches — Table Structures",
                        "Generic Basis table vs Application-specific own table vs Current ZPO_LONGTEXT",
                        SAP_DARK))
    els.append(sp(8))

    # Approach 1 — Generic
    els.append(table_struct("Approach 1 — Generic Table: SGBT_NTCEONT (Basis/BCSRV Team)", [
        ("MANDT",        "CLNT 3",    "Client"),
        ("OBJECT_TYPE",  "CHAR 10",   "Business Object Type — generic, not EKKO/EKPO specific"),
        ("OBJECT_ID",    "CHAR 70",   "Generic document ID — CHAR70 (same limitation as STXH TDNAME)"),
        ("NOTE_ID",      "CHAR 4",    "Note/Text type"),
        ("LANGUAGE",     "LANG 1",    "Language key"),
        ("NOTE_CONTENT", "STRG —",    "Long string — plain text content"),
        ("CREATED_BY",   "CHAR 12",   "Created by user"),
        ("CREATED_AT",   "DATS 8",    "Created date"),
        ("CHANGED_BY",   "CHAR 12",   "Last changed by"),
        ("CHANGED_AT",   "DATS 8",    "Last changed date"),
    ], TEAL))

    els.append(ibox(
        "Owner: BCSRV component (Basis team). Already used by Supplier Confirmation (new feature, no migration needed). "
        "Notes Reuse RAP Business Object is built on this table. CDS views and C1 contract views owned by Basis — not by PO team. "
        "CHAR70 OBJECT_ID = same generic limitation as STXH TDNAME.",
        TEAL_LT, TEAL
    ))
    els.append(sp(8))

    # Approach 2 — Sales SDD
    els.append(table_struct("Approach 2 — Application-Specific Own Table: SDTP_TEXT (Sales Reference)", [
        ("MANDT",            "CLNT 3",   "Client"),
        ("SD_DOCUMENT_ID",   "CHAR 10",  "Properly typed Sales Order number (= VBELN) — NOT generic CHAR70"),
        ("SD_DOCUMENT_ITEM", "NUMC 6",   "Item number (= POSNR) — properly typed"),
        ("TEXT_OBJECT",      "CHAR 10",  "VBBK (header) or VBBP (item)"),
        ("TEXT_ID",          "CHAR 4",   "Text type (0001, 0002 etc.)"),
        ("LANGUAGE",         "LANG 1",   "Language key"),
        ("TEXT_CONTENT",     "STRG —",   "Plain text string — converted from ITF format via CONVERT_ITF_TO_STREAM_TEXT"),
        ("REF_TEXT_OBJECT",  "CHAR 10",  "Reference chain — source object"),
        ("REF_TEXT_ID",      "CHAR 4",   "Reference chain — source text ID"),
        ("REF_TEXT_NAME",    "CHAR 70",  "Reference chain — source text name"),
        ("CREATED_BY/AT",    "CHAR+DATS","Administrative fields"),
        ("CHANGED_BY/AT",    "CHAR+DATS","Administrative fields"),
        ("AUTH_ENCODED",     "CHAR ~20", "Auth fields encoded via TDTITLE: DocCategory+DocType+SalesOrg+DistCh+Division"),
        ("SDM_VERSION",      "NUMC 2",   "Migration status — in root table VBAK (not in text table itself)"),
    ], SAP_BLUE))

    els.append(ibox(
        "Owner: SD LOB team. Handler class registered in TTXOB for VBBK/VBBP. "
        "SAP Script X team explicitly recommended this approach for all LOBs. "
        "Sales completed PoC in CE2608. SDM migrated 2.67M records in CCW/720 in 3.5 hours. "
        "ITF format converted to plain text string during migration.",
        SAP_LIGHT, SAP_BLUE
    ))
    els.append(sp(8))

    # Approach 3 — ZPO_LONGTEXT
    els.append(table_struct("Approach 3 — Current Lift & Shift Table: ZPO_LONGTEXT", [
        ("MANDT",        "CLNT 3",   "Client"),
        ("EBELN",        "CHAR 10",  "PO Number — properly typed ✓"),
        ("EBELP",        "NUMC 5",   "Item number — 00000 = header, 00010 = item 10"),
        ("TDOBJECT",     "CHAR 10",  "EKKO (header) or EKPO (item)"),
        ("TDID",         "CHAR 4",   "F01, F02, F09 etc."),
        ("TDSPRAS",      "LANG 1",   "Language key: D confirmed for this system"),
        ("LINE_COUNTER", "NUMC 5",   "Line sequence 00001, 00002... — ORDER BY field"),
        ("TDFORMAT",     "CHAR 2",   "Format indicator: * = normal text line"),
        ("TDLINE",       "CHAR 132", "PLAIN TEXT content — one 132-char line per row (NOT a string)"),
        ("MIGRATED_AT",  "DATS 8",   "Date row was written"),
        ("MIGRATED_BY",  "CHAR 12",  "User who wrote this row (sy-uname)"),
        ("SOURCE",       "CHAR 1",   "D = Dual-write by BAdI,  M = Migration report"),
    ], ORANGE))

    els.append(ibox(
        "Integration: BAdI ME_PROCESS_PO_CUST fires AFTER SAVE_TEXT. "
        "No SDM_VERSION tracking, no handler class, no automatic read/write switching. "
        "Always dual-write (BAdI always fires). PoC/Lift & Shift approach only. "
        "EKPO TDNAME confirmed: NO space between EBELN and EBELP on this system (e.g. 450007774400010).",
        ORANGE_LT, ORANGE
    ))
    els.append(PageBreak())
    return els

# ── Section 2: ITF and auth ───────────────────────────────────────────────────
def section2():
    els=[]
    els.append(sec_hdr("2","Sales SDD — ITF Conversion and Auth Encoding",
                        "How text format is converted and authorization info is transferred",
                        SAP_BLUE))
    els.append(sp(8))

    els.append(Paragraph("ITF Format Conversion (Critical for Migration)", H2))
    els.append(Paragraph(
        "SAPscript stores text in ITF (Interchange Text Format) — a proprietary SAP format. "
        "The new persistency stores PLAIN TEXT strings. Conversion happens during migration:", BODY))
    els.append(sp(4))
    els.append(code([
        "\" ITF table (TLINE rows) → Plain text string",
        "CALL FUNCTION 'CONVERT_ITF_TO_STREAM_TEXT'",
        "  EXPORTING i_type = 'TEXT'  TABLES i_text = lt_tline_table",
        "  IMPORTING e_text = lv_plain_string.",
        "",
        "\" Plain text string → ITF table (for reverse — e.g. display in editor)",
        "\" Step 1: Split string into 132-char chunks",
        "\" Step 2: Convert",
        "CALL FUNCTION 'CONVERT_STREAM_TO_ITF_TEXT'",
        "  EXPORTING i_type = 'TEXT'  TABLES i_text = lt_stream_table",
        "  IMPORTING e_text = lt_tline_table.",
    ]))
    els.append(sp(8))

    els.append(Paragraph("Authorization Encoding via TDTITLE Field", H2))
    els.append(Paragraph(
        "Auth fields are application-specific — not part of the SAPscript framework interface. "
        "Confirmed by text framework colleague Rene Zink: THEAD-TDTITLE field can be reused "
        "to pass application-specific data to the handler class.", BODY))
    els.append(sp(4))
    els.append(tbl(
        ["Auth Field","From","Example Value"],
        [
            ["SD Document Category","VBAK-VBTYP","C"],
            ["Sales Document Type", "VBAK-AUART","TA"],
            ["Sales Organization",  "VBAK-VKORG","1000"],
            ["Distribution Channel","VBAK-VTWEG","10"],
            ["Division",            "VBAK-SPART","00"],
        ],
        widths=[5*cm,5*cm,7.5*cm]
    ))
    els.append(sp(4))
    els.append(code([
        "\" Concatenated value in TDTITLE (Option 1 — preferred):",
        "\" SD Doc Category + Sales Doc Type + Sales Org + Dist Ch + Division",
        "\" Example: 'C   TA  10001000'  (values padded with spaces)",
        "",
        "\" PO equivalent would be:",
        "\" Purch Org + Company Code + Document Type + ... encoded similarly",
    ]))
    els.append(PageBreak())
    return els

# ── Section 3: Full comparison ────────────────────────────────────────────────
def section3():
    els=[]
    els.append(sec_hdr("3","Full Comparison — All Three Approaches",
                        "Every architectural aspect side by side",
                        PURPLE))
    els.append(sp(8))

    rows=[
        ["Table owner","Basis / BCSRV","SD LOB team","Lift & Shift / PO team"],
        ["Table name","SGBT_NTCEONT","SDTP_TEXT","ZPO_LONGTEXT"],
        ["Key design","CHAR70 OBJECT_ID (generic)","Typed VBELN + POSNR ✓","Typed EBELN + EBELP ✓"],
        ["Text storage","Long string (plain)","Long string (ITF→plain)","One row per 132-char line"],
        ["Integration method","RAP Business Subject in BO model","Handler class in TTXOB","BAdI ME_PROCESS_PO_CUST"],
        ["SAVE_TEXT routing","Not used — RAP APIs only","Auto via framework","Separate hook after SAVE_TEXT"],
        ["Migration mechanism","N/A — new feature only","SDM CL_SDM_PACKAGE_MIGRATION","Manual report — no SDM"],
        ["Dual-write control","N/A","Auto via IS_MIGRATION_FINISHED","Always on — BAdI always fires"],
        ["Read switching","N/A","Auto at SDM completion","No cutover logic — always reads ZPO"],
        ["CDS views","Built by Basis (C1 released)","Built by SD team on SDTP_TEXT","Not built yet"],
        ["Analytics/BW","Via Basis CDS views","Via SD CDS views","Not supported"],
        ["Auth fields","Not possible","YES — via TDTITLE encoding","Not stored"],
        ["Text references","Not supported (confirmed)","Stored in REF_ fields","Not handled"],
        ["App-specific attributes","NOT possible","YES — any field","YES — custom table"],
        ["SDM_VERSION in root","Not required","Required in VBAK","Not required"],
        ["Notes Reuse RAP compat.","YES — designed for it","UNKNOWN (open question)","UNKNOWN (open question)"],
        ["SAP Script X recommendation","Not mentioned","YES — recommended","Aligned with this"],
        ["Production ready","Yes — Supplier Confirmation","Yes — Sales CE2608 PoC","PoC only"],
    ]

    data=[[Paragraph(h,TH) for h in ["Aspect","RAP Generic Table\n(SGBT_NTCEONT)","Sales SDD Own Table\n(SDTP_TEXT)","ZPO_LONGTEXT\n(Current)"]]]
    colors_map = {
        "YES — designed for it": GREEN_LT,
        "YES — recommended": GREEN_LT,
        "UNKNOWN (open question)": GOLD_LT,
        "NOT possible": RED_LT,
        "Not built yet": ORANGE_LT,
        "PoC only": ORANGE_LT,
    }
    for i,row in enumerate(rows):
        data_row=[]
        for j,cell in enumerate(row):
            style_name=f"rc{i}{j}"
            if j==0:
                p=Paragraph(cell, ms(style_name,fontSize=7.5,textColor=SAP_DARK,fontName="Helvetica-Bold"))
            else:
                p=Paragraph(cell, TC)
            data_row.append(p)
        data.append(data_row)

    t=Table(data,colWidths=[4.5*cm,4.5*cm,4.5*cm,4*cm])
    style=[
        ("BACKGROUND",(0,0),(-1,0),PURPLE),
        ("GRID",(0,0),(-1,-1),0.4,GREY_BDR),
        ("TOPPADDING",(0,0),(-1,-1),3),("BOTTOMPADDING",(0,0),(-1,-1),3),
        ("LEFTPADDING",(0,0),(-1,-1),5),("VALIGN",(0,0),(-1,-1),"TOP"),
    ]
    for i in range(len(rows)):
        bg=WHITE if i%2==0 else GREY_BG
        style.append(("BACKGROUND",(0,i+1),(0,i+1),colors.HexColor("#F0EAF8")))
        style.append(("BACKGROUND",(1,i+1),(3,i+1),bg))
    t.setStyle(TableStyle(style))
    els.append(t)
    els.append(PageBreak())
    return els

# ── Section 4: Recommendation ─────────────────────────────────────────────────
def section4():
    els=[]
    els.append(sec_hdr("4","Recommendation for Standard PO (EKKO / EKPO)",
                        "Sales SDD own table approach — pending Notes Reuse compatibility confirmation",
                        GREEN_OK))
    els.append(sp(8))

    els.append(ok(
        "RECOMMENDED: Sales SDD approach — Application-specific own table + "
        "SAPScript Handler Class Framework + SDM (Silent Data Migration)\n"
        "PENDING: Confirm with Notes Reuse team that own table is compatible with Notes Reuse RAP BO"
    ))
    els.append(sp(6))

    els.append(Paragraph("Why NOT Generic Table (SGBT_NTCEONT) for PO", H2))
    els.append(tbl(
        ["Concern","Detail"],
        [
            ["No migration path for existing texts",
             "SGBT_NTCEONT is for NEW business objects only. PO has millions of existing texts in STXH/STXL needing migration."],
            ["CDS views owned by Basis",
             "PO team cannot add EBELN-specific joins or PO analytics without Basis involvement."],
            ["CHAR70 OBJECT_ID",
             "Still generic — same JOIN difficulty as STXH TDNAME. No EBELN typed key."],
            ["No PO-specific fields",
             "Cannot add Purchase Org, Document Type for authorization or reporting."],
            ["References not supported",
             "Direct text references confirmed NOT supported in new persistency (SDD confirmed)."],
        ],
        widths=[4.5*cm,13*cm]
    ))
    els.append(sp(6))

    els.append(Paragraph("Why Sales SDD Own Table IS Recommended for PO", H2))
    els.append(tbl(
        ["Benefit","PO-Specific Reasoning"],
        [
            ["Typed keys EBELN + EBELP","Direct SQL joins with EKKO, EKPO — no CHAR70 parsing needed"],
            ["PO team owns the table","Can add EKKO-specific fields: Purchasing Org, Company Code, Doc Type for auth"],
            ["SAP Script X recommended","Explicit guideline to all LOBs — PO follows same path as Sales"],
            ["SDM framework proven","Sales completed this in CE2608 — reusable pattern for PO in CE2708"],
            ["Automatic read/write switching","IS_MIGRATION_FINISHED handles cutover — no manual steps needed"],
            ["AI and BDC ready","Plain text string in single field — AI can process directly"],
            ["CDS views on PO terms","Analytics CDS can join with I_PurchaseOrderBasic, I_PurchaseOrderItem directly"],
        ],
        widths=[5*cm,12.5*cm]
    ))
    els.append(sp(6))

    els.append(Paragraph("Proposed PO Table: EKKT_TEXT", H2))
    els.append(table_struct("EKKT_TEXT — Recommended PO New Text Table", [
        ("MANDT",         "CLNT 3",   "Client"),
        ("EBELN",         "CHAR 10",  "PO Number — properly typed (NOT generic CHAR70) ✓"),
        ("EBELP",         "NUMC 5",   "Item — 00000 = header, 00010 = item 10 ✓"),
        ("TEXT_OBJECT",   "CHAR 10",  "EKKO (header) or EKPO (item)"),
        ("TEXT_ID",       "CHAR 4",   "F01, F02, F09 etc."),
        ("LANGUAGE",      "LANG 1",   "Language key: D for this system"),
        ("TEXT_CONTENT",  "STRG —",   "Plain text string — ITF converted via CONVERT_ITF_TO_STREAM_TEXT"),
        ("REF_TEXT_OBJ",  "CHAR 10",  "Reference chain — source object"),
        ("REF_TEXT_ID",   "CHAR 4",   "Reference chain — source text ID"),
        ("REF_TEXT_NAME", "CHAR 70",  "Reference chain — source text name"),
        ("CREATED_BY/AT", "CHAR+DATS","Administrative — created by/date"),
        ("CHANGED_BY/AT", "CHAR+DATS","Administrative — changed by/date"),
        ("AUTH_PORG",     "CHAR 4",   "Purchase Organization — explicit auth field (better than encoding)"),
        ("AUTH_BUKRS",    "CHAR 4",   "Company Code — explicit auth field"),
        ("AUTH_BSART",    "CHAR 4",   "Document Type — explicit auth field"),
    ], BTP_GREEN))

    els.append(note(
        "KEY DIFFERENCE from ZPO_LONGTEXT:\n"
        "  TEXT_CONTENT = full plain text STRING (not one row per 132 chars — no LINE_COUNTER needed)\n"
        "  Auth fields stored EXPLICITLY (not encoded via TDTITLE like Sales)\n"
        "  Reference fields stored\n"
        "  No TDFORMAT / TDLINE / LINE_COUNTER columns"
    ))
    els.append(sp(6))

    els.append(Paragraph("Migration Sequence", H2))
    els.append(tbl(
        ["Release","Task"],
        [
            ["CE2702 — PoC","Clarify Notes Reuse compatibility. Design EKKT_TEXT. Implement ZCL_PO_RSTXT_PERSISTENCE handler class. Register in TTXOB for EKKO and EKPO. Add SDM_VERSION to EKKO. Implement ZCL_SDM_EKKO_TEXT_MIGRATION. POC: write to both STXH and EKKT_TEXT via modernized OData V4 API."],
            ["CE2708 — Full","SDM runs in background — migrates all historic PO texts. IS_MIGRATION_FINISHED → TRUE → read switches to EKKT_TEXT. Build CDS views. Plug notes into PO OData V4 API. Regression test for all EKKO/EKPO business objects."],
        ],
        widths=[3*cm,14.5*cm]
    ))
    els.append(PageBreak())
    return els

# ── Section 5: Handler Class ──────────────────────────────────────────────────
def section5():
    els=[]
    els.append(sec_hdr("5","SAPScript Handler Class Framework",
                        "Runtime plug-in that intercepts SAVE_TEXT and READ_TEXT — routes to new table",
                        SAP_BLUE))
    els.append(sp(8))

    els.append(ibox(
        "ANALOGY: Think of the Handler Class as a TRAFFIC CONTROLLER standing at the "
        "SAVE_TEXT/READ_TEXT junction. It redirects traffic to the new table. "
        "Without it, all traffic goes to STXH/STXL as before."
    ))
    els.append(sp(6))

    els.append(Paragraph("What It Is", H2))
    els.append(Paragraph(
        "A runtime plug-in registered in table TTXOB that intercepts every SAVE_TEXT "
        "and READ_TEXT call and routes them to your new table instead of STXH/STXL. "
        "It is a class that inherits from CL_RSTXT_PERSISTENCE_FRAMEWORK.", BODY))
    els.append(sp(5))

    els.append(code([
        "WITHOUT Handler Class (before registration):",
        "  SAVE_TEXT → always writes to STXH/STXL",
        "  READ_TEXT → always reads from STXH/STXL",
        "",
        "WITH Handler Class registered in TTXOB for EKKO and EKPO:",
        "  SAVE_TEXT → SAP framework checks TTXOB → calls ZCL_PO_RSTXT_PERSISTENCE",
        "               → your CREATE or CHANGE method runs",
        "               → writes to EKKT_TEXT",
        "               → AND writes to STXH/STXL if IS_MIGRATION_FINISHED = FALSE",
        "",
        "  READ_TEXT → SAP framework calls ZCL_PO_RSTXT_PERSISTENCE→READ",
        "               → if IS_MIGRATION_FINISHED = FALSE → reads STXH/STXL",
        "               → if IS_MIGRATION_FINISHED = TRUE  → reads EKKT_TEXT",
    ]))
    els.append(sp(6))

    els.append(Paragraph("5 Methods to Implement", H2))
    els.append(tbl(
        ["Method","When Called","What It Does"],
        [
            ["CREATE","Every SAVE_TEXT creating new text","Write new text to EKKT_TEXT (+ STXH during migration)"],
            ["CHANGE","Every SAVE_TEXT updating text","Update text in EKKT_TEXT (+ STXH during migration)"],
            ["DELETE","Every DELETE_TEXT call","Remove text from EKKT_TEXT (+ STXH during migration)"],
            ["READ","Every READ_TEXT call","Read from EKKT_TEXT (new) or STXH/STXL (old) based on IS_MIGRATION_FINISHED"],
            ["READ_HEADERS_VIA_RANGES","Every SELECT_TEXT call","Read text headers from EKKT_TEXT or STXH"],
        ],
        widths=[4*cm,5.5*cm,8*cm]
    ))
    els.append(sp(6))

    els.append(Paragraph("Registration in TTXOB", H2))
    els.append(code([
        "Table TTXOB — Text Object definition:",
        "  TDOBJECT = 'EKKO'  → HANDLER_CLASS = 'ZCL_PO_RSTXT_PERSISTENCE'",
        "  TDOBJECT = 'EKPO'  → HANDLER_CLASS = 'ZCL_PO_RSTXT_PERSISTENCE'",
        "",
        "After registration — ALL applications using SAVE_TEXT/READ_TEXT for EKKO/EKPO",
        "automatically route through your handler class — no code changes in ME21N/ME22N needed.",
        "",
        "Alternative: Register at TDID level in TTXID (per text type) instead of all TDIDs.",
    ]))
    els.append(PageBreak())
    return els

# ── Section 6: SDM ────────────────────────────────────────────────────────────
def section6():
    els=[]
    els.append(sec_hdr("6","SDM — Silent Data Migration",
                        "Background batch job that moves EXISTING historic texts from STXH/STXL to new table",
                        ORANGE))
    els.append(sp(8))

    els.append(ibox(
        "ANALOGY: Think of SDM as REMOVAL MEN moving all the furniture from your old house "
        "to your new house while you are still living there. The Handler Class is the new "
        "house address label (new deliveries go to new house). But someone still has to move "
        "everything already in the old house. That is what SDM does."
    ))
    els.append(sp(6))

    els.append(Paragraph("What Problem SDM Solves", H2))
    els.append(code([
        "After Handler Class is registered:",
        "",
        "  NEW texts (created after registration):",
        "    → Handler Class routes them to EKKT_TEXT immediately ✓",
        "",
        "  EXISTING historic texts (created BEFORE registration):",
        "    → Still ONLY in STXH/STXL ✗",
        "    → PO 4500001234 from 2020 — its text is ONLY in STXH/STXL",
        "",
        "SDM migrates all the HISTORIC data in background — silently.",
    ]))
    els.append(sp(6))

    els.append(Paragraph("SDM Step by Step — What It Actually Does", H2))
    els.append(tbl(
        ["Step","Action","Detail"],
        [
            ["1","Select package","SELECT ebeln FROM ekko WHERE sdm_version < target UP TO 30,000 ROWS"],
            ["2","Read old texts","CALL FUNCTION 'SELECT_TEXT' → get text headers\nCALL FUNCTION 'READ_TEXT_TABLE' → mass read text content (decompresses STXL)"],
            ["3","Convert format","CALL FUNCTION 'CONVERT_ITF_TO_STREAM_TEXT' → ITF table → plain text string"],
            ["4","Delete existing","DELETE FROM ekkt_text WHERE ebeln IN @lt_package — ensures restartability"],
            ["5","Insert new","INSERT ekkt_text FROM TABLE lt_new_texts — plain text rows in new table"],
            ["6","Update status","UPDATE ekko SET sdm_version = target WHERE ebeln IN @lt_package"],
            ["7","Repeat","Process next package until all POs have sdm_version = target"],
        ],
        widths=[1.2*cm,4*cm,12.3*cm]
    ))
    els.append(sp(6))

    els.append(Paragraph("Performance Numbers from Sales (Reference)", H2))
    els.append(tbl(
        ["System","VBAK Records","Text Records","Package Size","Duration"],
        [
            ["DDCI (test)","40,853","340","30,000","Fast"],
            ["CCW/720 (perf)","13.9 million","2.67 million","30,000","3.5 hours"],
        ],
        widths=[4*cm,4*cm,3.5*cm,3*cm,3*cm]
    ))
    els.append(sp(4))
    els.append(note(
        "Open SQL limit: max 32,767 entries in WHERE range table → package size set to 32,000.\n"
        "Internal packaging within SELECT_TEXT calls every 30,000 documents.\n"
        "Old STXH/STXL records are NOT deleted during SDM — kept as safety net for restart.\n"
        "PO estimate: if similar volume to Sales (~13M POs) → ~3.5 hours SDM duration."
    ))
    els.append(sp(6))

    els.append(Paragraph("IS_MIGRATION_FINISHED — The Bridge Between Handler and SDM", H2))
    els.append(code([
        "IS_MIGRATION_FINISHED = FALSE  (SDM still running — called in handler class):",
        "  Handler CREATE/CHANGE → writes to STXH/STXL AND EKKT_TEXT (dual-write)",
        "  Handler READ          → reads from STXH/STXL (complete data — SDM still running)",
        "",
        "IS_MIGRATION_FINISHED = TRUE   (SDM complete — all data in new table):",
        "  Handler CREATE/CHANGE → writes to EKKT_TEXT ONLY",
        "  Handler READ          → reads from EKKT_TEXT (new — complete)",
        "",
        "Implementation:",
        "  METHOD is_migration_finished.",
        "    rv_finished = cl_sdm_proc_status_api=>is_sdm_finished(",
        "      i_sdm_name = 'ZCL_SDM_EKKO_TEXT_MIGRATION' ).",
        "  ENDMETHOD.",
        "",
        "Result buffered for entire dialog session — avoids repeated SELECT statements.",
    ]))
    els.append(PageBreak())
    return els

# ── Section 7: Comparison ─────────────────────────────────────────────────────
def section7():
    els=[]
    els.append(sec_hdr("7","Handler Class vs SDM — Key Differences",
                        "They are two completely different mechanisms that work together",
                        SAP_DARK))
    els.append(sp(8))

    els.append(ibox(
        "They Are NOT the Same Thing:\n"
        "  Handler Class = RUNTIME routing (where does NEW text go?)\n"
        "  SDM           = BACKGROUND migration (how do EXISTING historic texts get moved?)"
    ))
    els.append(sp(6))

    els.append(tbl(
        ["Aspect","SAPScript Handler Class Framework","SDM — Silent Data Migration"],
        [
            ["What it is","Runtime plug-in registered in TTXOB","Background batch migration job"],
            ["What it solves","Routes NEW SAVE_TEXT/READ_TEXT to new table","Moves EXISTING historic data to new table"],
            ["When it runs","Every time SAVE_TEXT or READ_TEXT is called","Once in background — packages of 30,000"],
            ["How activated","Register handler class in TTXOB.HANDLER_CLASS","Execute SDM job from SDM cockpit"],
            ["Duration","Instant — runs per transaction","Hours (3.5h for 13M records)"],
            ["Who drives it","SAP Script framework — automatic","SDM cockpit — background job"],
            ["Controls read switch","YES — via IS_MIGRATION_FINISHED","NO — it just migrates data"],
            ["SAP class to inherit","CL_RSTXT_PERSISTENCE_FRAMEWORK","CL_SDM_PACKAGE_MIGRATION"],
            ["Sales class name","Part of SD text persistency class","CL_SDM_SD_VBAK_TEXT_MIGRATION"],
            ["PO equivalent to build","ZCL_PO_RSTXT_PERSISTENCE","ZCL_SDM_EKKO_TEXT_MIGRATION"],
        ],
        widths=[4.5*cm,6.5*cm,6.5*cm]
    ))
    els.append(sp(8))

    els.append(Paragraph("Full Timeline — How They Work Together", H2))
    els.append(code([
        "BEFORE any change:",
        "  STXH/STXL has all PO texts (old house — all furniture here)",
        "  EKKT_TEXT is empty (new house — empty)",
        "",
        "STEP 1 — Register Handler Class in TTXOB for EKKO/EKPO:",
        "  New texts → go to EKKT_TEXT (AND STXH/STXL while SDM running)",
        "  Historic texts → still only in STXH/STXL",
        "  IS_MIGRATION_FINISHED = FALSE → reads still from STXH/STXL",
        "",
        "STEP 2 — SDM runs in background (hours/days):",
        "  Package by package: reads STXH/STXL → converts → inserts EKKT_TEXT",
        "  Updates SDM_VERSION in EKKO for each completed package",
        "  System continues working normally throughout",
        "",
        "STEP 3 — SDM completes (all SDM_VERSION updated):",
        "  IS_MIGRATION_FINISHED = TRUE",
        "  Handler Class now reads from EKKT_TEXT",
        "  Handler Class now writes to EKKT_TEXT only",
        "  STXH/STXL = frozen/legacy (kept as safety net)",
        "",
        "STEP 4 — After validation period:",
        "  STXH/STXL rows for PO texts cleaned up (archiving)",
        "  EKKT_TEXT is the single source of truth ✓",
    ]))
    els.append(sp(6))

    els.append(Paragraph("In One Sentence Each", H2))
    els.append(tbl(
        ["Mechanism","One-Line Definition"],
        [
            ["SAPScript Handler Class Framework",
             "A plug-in that intercepts every SAVE_TEXT and READ_TEXT call and routes it to your new table — effective immediately for all new transactions."],
            ["SDM (Silent Data Migration)",
             "A background job that moves all the existing historic text data from STXH/STXL to your new table silently while the system keeps running normally."],
        ],
        widths=[5.5*cm,12*cm]
    ))
    return els

# ── Section 8: REF fields ─────────────────────────────────────────────────────
def section8():
    els=[]
    els.append(sec_hdr("8","SDTP_TEXT — REF Fields vs TEXT Fields Explained",
                        "What REF_TEXT_OBJECT, REF_TEXT_ID, REF_TEXT_NAME store and when they are populated",
                        TEAL))
    els.append(sp(8))

    els.append(Paragraph("Identity Fields vs Reference Pointer Fields", H2))
    els.append(tbl(
        ["Field","Type","Populated When","Contains"],
        [
            ["TEXT_OBJECT",     "Identity",  "Always",
             "Which SAP business object this text belongs to — e.g. VBBK or EKKO"],
            ["TEXT_ID",         "Identity",  "Always",
             "Which type of text within that object — e.g. F01, F02, F09"],
            ["TEXT_CONTENT",    "Content",   "Only when text is a COPY (own text)",
             "The actual plain text string the user typed — empty if reference"],
            ["REF_TEXT_OBJECT", "Reference pointer","Only when text is a REFERENCE",
             "Object to look up for real content — e.g. LFA1, MATERIAL, EINE, EKKO"],
            ["REF_TEXT_ID",     "Reference pointer","Only when text is a REFERENCE",
             "Text type to look up in the referenced object — e.g. 0002"],
            ["REF_TEXT_NAME",   "Reference pointer","Only when text is a REFERENCE",
             "Document/record ID to look up — e.g. vendor number 0000001000"],
        ],
        widths=[3.5*cm,2.8*cm,4*cm,7.2*cm]
    ))
    els.append(sp(6))

    els.append(Paragraph("Two Types of Rows in SDTP_TEXT", H2))
    els.append(code([
        "TYPE A — Copy (own text — user typed it directly):",
        "  SD_DOCUMENT_ID  = 230001",
        "  TEXT_OBJECT     = VBBK",
        "  TEXT_ID         = 0001",
        "  TEXT_CONTENT    = 'Deliver before Christmas'  ← HAS CONTENT",
        "  REF_TEXT_OBJECT = ''   ← EMPTY — not a reference",
        "  REF_TEXT_ID     = ''   ← EMPTY",
        "  REF_TEXT_NAME   = ''   ← EMPTY",
        "",
        "TYPE B — Reference (pointer to another document's text):",
        "  SD_DOCUMENT_ID  = 230002",
        "  TEXT_OBJECT     = VBBK",
        "  TEXT_ID         = 0001",
        "  TEXT_CONTENT    = ''   ← EMPTY — no own content",
        "  REF_TEXT_OBJECT = 'KNA1'        ← Points to: Customer master",
        "  REF_TEXT_ID     = '0001'         ← Points to: text type 0001 in KNA1",
        "  REF_TEXT_NAME   = '0000012345'   ← Points to: Customer ID",
        "",
        "Reading Sales Order 230002 header note:",
        "  → TEXT_CONTENT is empty → check REF fields",
        "  → Go read KNA1/0001/0000012345 to get the actual text",
    ]))
    els.append(sp(6))

    els.append(Paragraph("Where REF Fields Are Populated From", H2))
    els.append(tbl(
        ["Source","How REF Fields Are Set"],
        [
            ["During SDM Migration (historic documents)",
             "Read from STXH fields: TDREF='X' → reference. "
             "TDREFOBJ→REF_TEXT_OBJECT, TDREFNAME→REF_TEXT_NAME, TDREFID→REF_TEXT_ID. "
             "If TDREF=' ' (copy) → TEXT_CONTENT set, REF fields empty."],
            ["Runtime — Handler CREATE/CHANGE",
             "SAVE_TEXT passes THEAD structure. If THEAD-TDREF='X' → store REF fields, TEXT_CONTENT=''. "
             "If TDREF=' ' → convert ITF→string, store TEXT_CONTENT, clear REF fields."],
            ["User edits a referenced text",
             "CHANGE method detects content is being written → clears REF_TEXT_OBJECT, "
             "REF_TEXT_ID, REF_TEXT_NAME → stores new content in TEXT_CONTENT. "
             "Reference is permanently broken."],
        ],
        widths=[4.5*cm,13*cm]
    ))
    els.append(sp(6))

    els.append(Paragraph("The Reference Chain Problem", H2))
    els.append(code([
        "Reference chain example (can be N levels deep):",
        "",
        "  KNA1 (Customer master)",
        "    text 0001: 'Standard delivery instructions'",
        "        │  REF_TEXT_OBJECT=KNA1, NAME=0000012345",
        "        └── VBBK (Quotation 100001) references KNA1",
        "                │  REF_TEXT_OBJECT=VBBK, NAME=100001",
        "                └── VBBK (Sales Order 230001) references Quotation",
        "                        │  REF_TEXT_OBJECT=VBBK, NAME=230001",
        "                        └── VBBK (Delivery 800001) references Sales Order",
        "",
        "To read Delivery 800001 text:",
        "  Step 1: Read SDTP_TEXT Delivery 800001 → empty → follow REF to Sales Order 230001",
        "  Step 2: Read SDTP_TEXT Sales Order 230001 → empty → follow REF to Quotation 100001",
        "  Step 3: Read SDTP_TEXT Quotation 100001 → empty → follow REF to KNA1",
        "  Step 4: Read KNA1 text table → 'Standard delivery instructions' ✓",
        "",
        "CANNOT be resolved via CDS JOIN — chain depth is unknown.",
        "Only 1-level self-join supported (like CRM solution).",
        "Cross-object refs (EKKO→LFA1, EKKO→MATERIAL) impossible without missing CDS views.",
    ]))
    els.append(sp(4))
    els.append(warn(
        "⚠  ~2% of text records in customer systems have cross-object references. "
        "98% are copy records or same-object references — these are manageable. "
        "Cross-object references remain a known limitation — KBA note to customers required."
    ))
    els.append(PageBreak())
    return els

# ── Section 9: PO Reference Scenarios ────────────────────────────────────────
def section9():
    els=[]
    els.append(sec_hdr("9","PO Reference Notes — 6 Scenarios",
                        "When and why reference texts are created for EKKO and EKPO",
                        PURPLE))
    els.append(sp(8))

    els.append(Paragraph("Configuration Control — VOTXN and SPRO Paths Clarified", H2))
    els.append(warn(
        "⚠  Two separate text configurations exist for PO — they serve DIFFERENT purposes:\n"
        "  1. VOTXN / Text Determination = controls copy/reference rules when PO is CREATED\n"
        "  2. SPRO → Messages → Texts for Messages → Define Texts for PO = controls which texts "
        "are PRINTED on PO output form sent to vendor\n"
        "  For REF fields and reference behaviour → use VOTXN (path 1)."
    ))
    els.append(sp(5))

    els.append(Paragraph("Path 1 — Text Determination (Copy/Reference Rules): VOTXN", H2))
    els.append(code([
        "Transaction: VOTXN → press Enter",
        "",
        "Text Object list → scroll to find EKKO and EKPO:",
        "  EKKO   ← Purchase Order Header — click + click 'Text types' button",
        "  EKPO   ← Purchase Order Item   — click + click 'Text types' button",
        "",
        "Shows: Text ID, Description, Access Sequence, Refer/Duplicate flag",
        "This controls: whether text is COPIED or REFERENCED when PO is created",
    ]))
    els.append(sp(5))

    els.append(Paragraph("Path 2 — Texts for Output Messages (What Gets Printed): SPRO", H2))
    els.append(ibox(
        "SPRO → Materials Management → Purchasing\n"
        "  → Messages\n"
        "    → Texts for Messages\n"
        "      → Define Texts for Purchase Order    ← as shown in SPRO screenshot\n\n"
        "Purpose: defines which Text IDs are included in the PO output message (print/email to vendor).\n"
        "This is NOT about copy/reference rules — it is about which texts appear on the PO form.",
        SAP_LIGHT, SAP_BLUE
    ))
    els.append(sp(5))

    els.append(tbl(
        ["Configuration","Transaction / SPRO Path","Controls","Used For REF Fields?"],
        [
            ["Text Determination",
             "VOTXN → EKKO / EKPO → Text types",
             "Copy or Reference rules per Text ID. Access Sequence priority.",
             "YES — this is where REF_TEXT_OBJECT source is defined"],
            ["Texts for Output Messages",
             "SPRO → MM → Purchasing → Messages → Texts for Messages → Define Texts for PO",
             "Which Text IDs are printed on PO output form sent to vendor",
             "NO — output format only, no impact on REF fields"],
        ],
        widths=[3.5*cm,6*cm,5*cm,3*cm]
    ))
    els.append(sp(6))
    els.append(Paragraph("PO Header Text Types — EKKO (Confirmed from This System)", H2))
    els.append(ibox(
        "Source: SPRO → MM → Purchasing → Purchase Order → Texts for Purchase Order "
        "→ Texts for Document Header. Doc. Category = F (Purchase Order).",
        SAP_LIGHT, SAP_BLUE
    ))
    els.append(sp(4))
    els.append(tbl(
        ["Seq.","Description","TDID","EBELP in ZPO","Notes"],
        [
            ["01","Header text",           "F01","00000","User types directly — COPY"],
            ["02","Header note",           "F02","00000","Usually referenced from Vendor Master"],
            ["03","Pricing types",         "F03","00000","COPY"],
            ["04","Deadlines",             "F04","00000","COPY"],
            ["05","Terms of delivery",     "F05","00000","May reference from Vendor Master"],
            ["06","Shipping instructions", "F06","00000","COPY or REF"],
            ["07","Terms of payment",      "F07","00000","COPY"],
            ["08","Warranties",            "F08","00000","COPY"],
            ["09","Penalty for breach",    "F09","00000","COPY — NOTE: NOT GR text for EKKO"],
            ["10","Guarantees",            "F10","00000","COPY"],
            ["11","Contract riders",       "F11","00000","COPY"],
            ["12","Attachment",            "F12","00000","COPY"],
            ["13","Other contractual",     "F13","00000","COPY"],
            ["14","Delivery",              "F14","00000","COPY"],
            ["15","Vendor memo (general)", "F15","00000","COPY"],
            ["16","Vendor memo (special)", "F16","00000","COPY"],
        ],
        widths=[1.2*cm,5.3*cm,1.8*cm,3*cm,6.2*cm]
    ))
    els.append(sp(6))

    els.append(Paragraph("PO Item Text Types — EKPO (Confirmed from This System)", H2))
    els.append(ibox(
        "Source: SPRO → MM → Purchasing → Purchase Order → Texts for Purchase Order "
        "→ Texts for Document Item. Doc. Category = F (Purchase Order).",
        TEAL_LT, TEAL
    ))
    els.append(sp(4))
    els.append(tbl(
        ["Seq.","Description","TDID","EBELP in ZPO","Reference Source"],
        [
            ["01","Item text",                "F01","item no.","User types directly — COPY"],
            ["02","Info record PO text",      "F02","item no.","REFERENCE from EINE/EINA info record"],
            ["03","Material PO text",         "F03","item no.","REFERENCE from Material Master"],
            ["04","Delivery text",            "F04","item no.","REFERENCE from Info Record / Vendor"],
            ["05","Info record note",         "F05","item no.","REFERENCE from EINE/EINA info record"],
            ["06","MRP Cockpit",              "F06","item no.","System generated — MRP"],
            ["10","Item Text for SPEC2000",   "L01","item no.","SPEC2000 aerospace standard"],
            ["11","Supplier Comments at Item","F11","item no.","Supplier-entered comments"],
            ["12","Terms and Conditions",     "F12","item no.","REFERENCE from Info Record"],
            ["13","PO Item Closure Text",     "F13","item no.","System generated on PO closure"],
        ],
        widths=[1.2*cm,5.3*cm,1.8*cm,3*cm,6.2*cm]
    ))
    els.append(sp(4))
    els.append(warn(
        "⚠  Important finding for this system:\n"
        "  EKPO F09 = 'Penalty for breach of contract' on EKKO (header) — NOT GR text\n"
        "  EKPO item list does NOT show F09 as GR text — GR text may use a different TDID or not be configured\n"
        "  Always verify actual TDIDs via: SE16N → STXH → TDOBJECT=EKPO, TDNAME=<your PO>+item\n"
        "  The actual TDIDs stored in STXH are the ground truth for migration handler coding"
    ))
    els.append(sp(6))

    els.append(Paragraph("The 6 Reference Scenarios for PO", H2))
    scenarios=[
        ("1","PO from Vendor Master text",
         "Vendor master LFA1/LFM1 has delivery instructions. PO created for this vendor.",
         "LFA1/LFM1","Header text F02 (Header note) appears in PO — referenced, not copied. "
         "If vendor updates delivery hours, ALL POs referencing it auto-update.",
         "EKKO → LFA1"),
        ("2","PO Item text from Purchasing Info Record",
         "Info record (EINE/EINA) for vendor+material has a PO text or delivery note.",
         "EINE/EINA","PO item F02 (Info record PO text) and F04 (Delivery text) reference the info record. "
         "Text appears on PO without being stored per item.",
         "EKPO → EINE"),
        ("3","PO Item text from Material Master",
         "Material master has a standard purchase order text for the material.",
         "MATERIAL","PO item F03 (Material PO text) references material master. "
         "Appears on PO output to vendor without storing per PO item.",
         "EKPO → MATERIAL"),
        ("4","PO from Purchase Requisition",
         "PO created with reference to PR 1000012345 which had requestor notes.",
         "BANF/EBAN","PO text may reference PR text depending on VOTXN config. "
         "Requestor's urgency note appears on PO without copying.",
         "EKKO/EKPO → EBAN"),
        ("5","PO from RFQ/Quotation",
         "PO created with reference to RFQ 6000001234. Vendor terms noted in RFQ.",
         "EKKO (RFQ)","PO header text references RFQ header text. "
         "Vendor's quoted delivery terms appear in PO — reference chain EKKO→EKKO.",
         "EKKO → EKKO"),
        ("6","User edits referenced text in ME22N",
         "User opens PO, sees referenced text, modifies it.",
         "—","Reference BROKEN — becomes own copy. REF fields cleared. "
         "TEXT_CONTENT set to new value. Changes to source no longer affect this PO.",
         "EKKO: REF→COPY"),
    ]

    for num,title,when,source,result,chain in scenarios:
        hdr=Table([[
            Paragraph(num, ms(f"sn{num}",fontSize=12,textColor=WHITE,fontName="Helvetica-Bold",alignment=TA_CENTER)),
            Paragraph(title, ms(f"st{num}",fontSize=9,textColor=WHITE,fontName="Helvetica-Bold")),
            Paragraph(f"Chain: {chain}", ms(f"sc{num}",fontSize=8,textColor=colors.HexColor("#AACCFF"),fontName="Helvetica-Oblique")),
        ]],colWidths=[1.2*cm,10.8*cm,5.5*cm])
        hdr.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(0,0),PURPLE),
            ("BACKGROUND",(1,0),(2,0),SAP_DARK),
            ("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6),
            ("LEFTPADDING",(0,0),(-1,-1),8),("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ]))
        body_rows=[
            [Paragraph("When",ms(f"bw{num}",fontSize=7.5,textColor=SAP_DARK,fontName="Helvetica-Bold")),
             Paragraph(when, BSML)],
            [Paragraph("Source",ms(f"bs{num}",fontSize=7.5,textColor=SAP_DARK,fontName="Helvetica-Bold")),
             Paragraph(source, ms(f"bsv{num}",fontSize=8,textColor=TEAL,fontName="Helvetica-Bold"))],
            [Paragraph("Result",ms(f"br{num}",fontSize=7.5,textColor=SAP_DARK,fontName="Helvetica-Bold")),
             Paragraph(result, BSML)],
        ]
        body=Table(body_rows,colWidths=[2*cm,15.5*cm])
        body.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(0,-1),GREY_BG),
            ("BACKGROUND",(1,0),(1,-1),WHITE),
            ("GRID",(0,0),(-1,-1),0.3,GREY_BDR),
            ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
            ("LEFTPADDING",(0,0),(-1,-1),8),("VALIGN",(0,0),(-1,-1),"TOP"),
        ]))
        bot=Table([[""]], colWidths=[17.5*cm],rowHeights=[2])
        bot.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),PURPLE)]))
        els.append(KeepTogether([hdr,body,bot,sp(6)]))

    els.append(sp(4))
    els.append(Paragraph("Reference vs Copy — Decision Table", H2))
    els.append(tbl(
        ["Trigger","Reference Created","Copy Created"],
        [
            ["VOTXN: Refer/Duplicate = checked","✓",""],
            ["VOTXN: Refer/Duplicate = unchecked","","✓"],
            ["User types NEW text in ME21N/ME22N","","✓ Own text"],
            ["User EDITS existing reference in ME22N","","✓ Reference broken → copy"],
            ["No source text found in access sequence","","Neither — text empty"],
        ],
        widths=[8*cm,4.75*cm,4.75*cm]
    ))
    els.append(sp(6))
    els.append(note(
        "Migration Impact for PO EKKO/EKPO:\n"
        "  Records with TEXT_CONTENT = '' and REF fields populated = REFERENCES\n"
        "  During SDM: REF fields are migrated as-is (pointer preserved in new table)\n"
        "  Cross-object references (EKKO→LFA1, EKPO→MATERIAL) cannot be resolved "
        "in CDS joins because LFA1/MATERIAL text CDS views do not exist yet.\n"
        "  Same-object references (EKKO→EKKO e.g. PO from RFQ) can be resolved with 1-level self-join."
    ))
    return els

# ── Build ─────────────────────────────────────────────────────────────────────
def build():
    doc=SimpleDocTemplate(
        OUTPUT,pagesize=A4,
        leftMargin=2*cm,rightMargin=2*cm,
        topMargin=2*cm,bottomMargin=2*cm,
        title="PO Notes New Persistency Architecture Guide",
        author="SAP PO Long Text Team",
    )
    story=[]
    story.extend(cover())
    story.extend(section1())
    story.extend(section2())
    story.extend(section3())
    story.extend(section4())
    story.extend(section5())
    story.extend(section6())
    story.extend(section7())
    story.extend(section8())
    story.extend(section9())

    def on_page(c,doc):
        c.saveState()
        c.setFont("Helvetica",7)
        c.setFillColor(colors.HexColor("#888888"))
        c.drawString(2*cm,1.2*cm,
            "PO Notes New Persistency — Architecture Comparison & Recommendation | EKKO/EKPO | CE2702/CE2708")
        c.drawRightString(19.5*cm,1.2*cm,f"Page {doc.page}")
        c.setStrokeColor(colors.HexColor("#CCCCCC"))
        c.setLineWidth(0.4)
        c.line(2*cm,1.5*cm,19.5*cm,1.5*cm)
        c.restoreState()

    doc.build(story,onFirstPage=on_page,onLaterPages=on_page)
    print(f"PDF created: {OUTPUT}")

build()
