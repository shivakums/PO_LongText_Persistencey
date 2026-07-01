from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

OUTPUT = r"C:\Users\I308878\PO_LongText_Persistencey\PO_Notes_Teams_Code_Reference.pdf"

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

TITLE  = ms("T",  fontSize=19, textColor=WHITE,   fontName="Helvetica-Bold", alignment=TA_CENTER, spaceAfter=4)
SUB    = ms("ST", fontSize=9,  textColor=colors.HexColor("#AACCFF"), fontName="Helvetica", alignment=TA_CENTER, spaceAfter=2)
META   = ms("M",  fontSize=7.5,textColor=colors.HexColor("#AACCFF"), fontName="Helvetica", alignment=TA_CENTER)
H1     = ms("H1", fontSize=12, textColor=WHITE,   fontName="Helvetica-Bold", spaceAfter=3)
H2     = ms("H2", fontSize=10, textColor=SAP_DARK,fontName="Helvetica-Bold", spaceAfter=3, spaceBefore=5)
H3     = ms("H3", fontSize=9,  textColor=SAP_BLUE,fontName="Helvetica-Bold", spaceAfter=2, spaceBefore=4)
BODY   = ms("B",  fontSize=8.5,textColor=BLACK,   leading=13, spaceAfter=3, alignment=TA_JUSTIFY)
BSML   = ms("BS", fontSize=8,  textColor=BLACK,   leading=12, spaceAfter=2)
CODE_S = ms("CS", fontSize=7,  textColor=CODE_FG, fontName="Courier", leading=10.5, spaceAfter=1)
TH     = ms("TH", fontSize=7.5,textColor=WHITE,   fontName="Helvetica-Bold", alignment=TA_CENTER)
TC     = ms("TC", fontSize=7.5,textColor=BLACK,   leading=10)
SN     = ms("SN", fontSize=18, textColor=WHITE,   fontName="Helvetica-Bold", alignment=TA_CENTER)
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

def quote_box(text, speaker=""):
    c = f'"{text}"'
    if speaker: c += f"  — <i>{speaker}</i>"
    t=Table([[Paragraph(c, ms("qs",fontSize=8,textColor=colors.HexColor("#333333"),
              fontName="Helvetica-Oblique",leading=12,leftIndent=8))]],colWidths=[17.5*cm])
    t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),GOLD_LT),
                            ("LINEBEFORE",(0,0),(0,-1),3,GOLD),
                            ("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6),
                            ("LEFTPADDING",(0,0),(-1,-1),12),("RIGHTPADDING",(0,0),(-1,-1),8)]))
    return t

def obj_row(name, obj_type, purpose, color):
    t=Table([[
        Paragraph(name,   ms(f"on{name[:3]}",fontSize=8,textColor=WHITE,fontName="Helvetica-Bold")),
        Paragraph(obj_type,ms(f"ot{name[:3]}",fontSize=7.5,textColor=colors.HexColor("#AACCFF"),fontName="Helvetica-Oblique")),
        Paragraph(purpose, BSML),
    ]],colWidths=[4.5*cm,3*cm,10*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(1,0),color),
        ("BACKGROUND",(2,0),(2,0),WHITE),
        ("LINEABOVE",(0,0),(-1,0),0.3,color),
        ("LINEBELOW",(0,0),(-1,0),0.3,GREY_BDR),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
        ("LEFTPADDING",(0,0),(-1,-1),8),("VALIGN",(0,0),(-1,-1),"MIDDLE"),
    ]))
    return t

# ══════════════════════════════════════════════════════════════════════════════
def cover():
    els=[]
    cov=Table([
        [Paragraph("PO Notes New Persistency", TITLE)],
        [Paragraph("Three Teams — Who They Are, What Code They Own, What They Built", SUB)],
        [Paragraph("SAP Script X Team  |  Notes Reuse RAP Team  |  Sales Team (Reference Implementation)", SUB)],
        [Paragraph("Sources: Sales SDD, PO Notes Handover PPT, CE2702/CE2708 Sync Meeting, FW S4 PR Support Meeting  |  2026-06-30", META)],
    ],colWidths=[17.5*cm])
    cov.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),SAP_DARK),
                              ("TOPPADDING",(0,0),(-1,-1),22),("BOTTOMPADDING",(0,0),(-1,-1),22),
                              ("LEFTPADDING",(0,0),(-1,-1),20)]))
    els.append(cov)
    els.append(sp(12))

    els.append(tbl(
        ["Team","What They Own","Role for PO Team","Contact"],
        [
            ["SAP Script X Team",
             "STXH/STXL framework + CL_RSTXT_PERSISTENCE_FRAMEWORK base class + TTXOB HANDLER_CLASS mechanism",
             "Provide plug-in framework + wiki guidelines — PO team registers handler class in TTXOB",
             "Via SAP Script X wiki"],
            ["Notes Reuse RAP Team",
             "SGBT_NTCEONT generic table + Notes Reuse RAP Business Object + CDS views (BCSRV owned)",
             "Provide reusable notes UI/logic — PO team must clarify if EKKT_TEXT is compatible",
             "BLR04: M K, Visakh and team"],
            ["Sales Team",
             "SDTP_TEXT own table + handler class + SDM classes (CE2608 PoC delivered)",
             "Reference implementation — PO team follows same pattern for EKKT_TEXT + SDM",
             "Karen Feng, Chris Xie"],
        ],
        widths=[3*cm,6*cm,5*cm,3.5*cm]
    ))
    els.append(sp(8))
    els.append(warn(
        "⚠  Critical Open Question (blocking Activity 1 of CE2702):\n"
        "  Notes Reuse RAP BO is currently documented to work ONLY with SGBT_NTCEONT.\n"
        "  If PO team builds own table EKKT_TEXT — can Notes Reuse RAP consume it?\n"
        "  This question must be answered by Notes Reuse RAP team BEFORE EKKT_TEXT is designed."
    ))
    els.append(PageBreak())
    return els

# ── Section 1: SAP Script X Team ─────────────────────────────────────────────
def section1():
    els=[]
    els.append(sec_hdr("1","SAP Script X Team — SAPScript / Forms Services",
                        "Owners of STXH/STXL framework and CL_RSTXT_PERSISTENCE_FRAMEWORK base class",
                        TEAL))
    els.append(sp(8))

    els.append(Paragraph("Who They Are", H2))
    els.append(Paragraph(
        "The SAP Script / Forms Services team owns the entire SAP text framework — "
        "STXH, STXL, STXB cluster tables and all text APIs (READ_TEXT, SAVE_TEXT, DELETE_TEXT). "
        "They enabled the new persistency plug-in mechanism by adding the HANDLER_CLASS field "
        "to TTXOB and building the base class CL_RSTXT_PERSISTENCE_FRAMEWORK. "
        "They published the wiki guidelines for all applications to follow.", BODY))
    els.append(sp(6))

    els.append(Paragraph("Tables and Objects They Own", H2))
    for name,typ,purpose in [
        ("STXH","Database Table","Text header — one row per text. TDOBJECT, TDNAME, TDID, TDSPRAS, TDREF/TDREFOBJ etc."),
        ("STXL","Cluster Table","Text lines — COMPRESSED binary. Cannot be read via plain SQL. Only via READ_TEXT."),
        ("STXB","Cluster Table","Text buffer — temporary text storage during editing session"),
        ("TTXOB","Customising Table","Text object definition. KEY FIELD: HANDLER_CLASS — application registers their class here"),
        ("TTXID","Customising Table","Text ID definition per object. Links text types to text schemas"),
        ("CL_RSTXT_PERSISTENCE_FRAMEWORK","ABAP Class","BASE CLASS all application handler classes must inherit. Provides the interface contract."),
        ("CL_SDM_PACKAGE_MIGRATION","ABAP Class","BASE CLASS all SDM migration classes must inherit"),
        ("CL_SDM_PROC_STATUS_API","ABAP Class","API to check if SDM migration is finished — IS_SDM_FINISHED method"),
    ]:
        els.append(obj_row(name, typ, purpose, TEAL))
        els.append(sp(2))

    els.append(sp(6))
    els.append(Paragraph("Standard Function Modules (SAP Standard — Do NOT Modify)", H2))
    els.append(tbl(
        ["Function Module","Purpose"],
        [
            ["READ_TEXT",                  "Decompress text from STXL and return plain TLINE table — main read API"],
            ["SAVE_TEXT",                  "Compress text to STXH/STXL — main write API. Triggers handler class if registered."],
            ["DELETE_TEXT",                "Delete a text entry from STXH/STXL — triggers handler class if registered"],
            ["SELECT_TEXT",                "Read text headers from STXH by range — used in SDM and handler class"],
            ["READ_TEXT_TABLE",            "Mass read multiple texts — used in SDM for performance"],
            ["READ_MULTIPLE_TEXTS",        "Alternative mass text reader"],
            ["CONVERT_ITF_TO_STREAM_TEXT", "Convert ITF table (TLINE) → plain text string — CRITICAL for migration"],
            ["CONVERT_STREAM_TO_ITF_TEXT", "Convert plain text string → ITF table — used in handler READ method"],
        ],
        widths=[6*cm,11.5*cm]
    ))
    els.append(sp(6))

    els.append(Paragraph("What They Enabled — The Plug-in Mechanism", H2))
    els.append(code([
        "BEFORE SAP Script X team enablement:",
        "  SAVE_TEXT → always writes to STXH/STXL (no routing possible)",
        "  READ_TEXT → always reads from STXH/STXL",
        "",
        "AFTER SAP Script X team added HANDLER_CLASS to TTXOB:",
        "  SAVE_TEXT called by ME21N",
        "        │",
        "        ▼",
        "  SAP Script framework checks TTXOB.HANDLER_CLASS for EKKO/EKPO",
        "        │",
        "        ├── HANDLER_CLASS empty → write to STXH/STXL (old behaviour)",
        "        │",
        "        └── HANDLER_CLASS = 'ZCL_PO_RSTXT_PERSISTENCE'",
        "               → call application's handler class",
        "               → application writes to EKKT_TEXT (new table)",
        "               → AND writes to STXH if IS_MIGRATION_FINISHED = FALSE",
    ]))
    els.append(sp(5))
    els.append(ibox(
        "From PO Notes Handover PPT (Slide 7):\n"
        "\"The SAPScript team has already published the guidelines to move to new persistency. "
        "Application-specific persistence of SAPscript texts — Forms Services — Wiki@SAP\"\n"
        "This wiki is the definitive guide for PO team to follow.",
        SAP_LIGHT, TEAL
    ))
    els.append(sp(5))
    els.append(Paragraph("Confirmed Registration — Text Object Level vs Text ID Level", H2))
    els.append(code([
        "Registration in TTXOB (text OBJECT level — all TDIDs):",
        "  TDOBJECT = 'EKKO'  →  HANDLER_CLASS = 'ZCL_PO_RSTXT_PERSISTENCE'",
        "  TDOBJECT = 'EKPO'  →  HANDLER_CLASS = 'ZCL_PO_RSTXT_PERSISTENCE'",
        "  Effect: ALL text IDs (F01, F02, F04...) for EKKO/EKPO route to handler",
        "",
        "Alternative — Registration in TTXID (text ID level — specific TDIDs only):",
        "  TDOBJECT = 'EKKO', TDID = 'F01'  →  HANDLER_CLASS = 'ZCL_PO_RSTXT_PERSISTENCE'",
        "  Effect: Only F01 routes to handler, other TDIDs still go to STXH",
        "",
        "From PO Notes Handover PPT (Slide 9):",
        "  'Currently all teams have done this at Text Object level'",
        "  Recommendation for PO: register at TDOBJECT level (EKKO + EKPO)",
    ]))
    els.append(PageBreak())
    return els

# ── Section 2: Notes Reuse RAP Team ──────────────────────────────────────────
def section2():
    els=[]
    els.append(sec_hdr("2","Notes Reuse RAP Team — Procurement Notes Reuse BLR04",
                        "Owners of SGBT_NTCEONT generic table and Notes Reuse RAP Business Object",
                        PURPLE))
    els.append(sp(8))

    els.append(Paragraph("Who They Are", H2))
    els.append(Paragraph(
        "The Notes Reuse RAP team built a reusable RAP Business Object for notes "
        "so that any application can include notes functionality without building it from scratch. "
        "The Procurement-specific notes reuse topic is owned by the BLR04 team "
        "(M K, Visakh and team). Any architectural guideline for PO notes must be "
        "aligned with this team in addition to the WDF11 team.", BODY))
    els.append(sp(6))

    els.append(Paragraph("Objects They Own", H2))
    for name,typ,purpose in [
        ("SGBT_NTCEONT","Database Table (BCSRV component)",
         "Generic notes content table. OBJECT_TYPE + OBJECT_ID (CHAR70) + NOTE_ID + LANGUAGE + NOTE_CONTENT (plain string). "
         "Owned by BCSRV — NOT by PO team. CDS views and C1 contract views also owned by BCSRV."),
        ("Notes Reuse RAP Business Object","RAP Business Object",
         "Reusable BO providing CRUD for notes. Applications include this as composition in their own RAP BO. "
         "Currently documented to work with SGBT_NTCEONT. "
         "Already used by: Supplier Confirmation (new feature — no migration needed)."),
        ("CDS Views on SGBT_NTCEONT","CDS Views (BCSRV owned)",
         "Basic view + analytics view on SGBT_NTCEONT. C1 released for external consumption. "
         "Owned by Basis/BCSRV team — PO team cannot add PO-specific joins without Basis involvement."),
    ]:
        els.append(obj_row(name, typ, purpose, PURPLE))
        els.append(sp(2))

    els.append(sp(6))
    els.append(Paragraph("SGBT_NTCEONT Table Structure", H2))
    els.append(tbl(
        ["Field","Type","Length","Description"],
        [
            ["MANDT",        "CLNT","3", "Client"],
            ["OBJECT_TYPE",  "CHAR","10","Business Object Type — generic"],
            ["OBJECT_ID",    "CHAR","70","Generic document ID — CHAR70 (same limitation as STXH TDNAME)"],
            ["NOTE_ID",      "CHAR","4", "Note/Text type"],
            ["LANGUAGE",     "LANG","1", "Language key"],
            ["NOTE_CONTENT", "STRG","—", "Plain text content — long string"],
            ["CREATED_BY",   "CHAR","12","Created by"],
            ["CREATED_AT",   "DATS","8", "Created date"],
            ["CHANGED_BY",   "CHAR","12","Changed by"],
            ["CHANGED_AT",   "DATS","8", "Changed date"],
        ],
        widths=[3.5*cm,2*cm,2*cm,10*cm]
    ))
    els.append(sp(6))

    els.append(Paragraph("Key Limitations Confirmed", H2))
    els.append(tbl(
        ["Limitation","Source","Impact on PO"],
        [
            ["Text references NOT supported out of the box",
             "PO Notes Handover PPT Slide 8",
             "PO has many reference texts (F02, F04 from Info Record/Vendor) — must handle separately"],
            ["CHAR70 OBJECT_ID — same as STXH TDNAME",
             "Table design analysis",
             "Cannot JOIN with EKKO on typed EBELN — same limitation as STXH"],
            ["No PO-specific attributes possible",
             "Table design analysis",
             "Cannot add Purchase Org, Doc Type for auth or reporting"],
            ["CDS views owned by BCSRV/Basis",
             "Architecture — BCSRV component ownership",
             "PO team cannot add EKKO-specific joins without Basis approval"],
            ["Only works with SGBT_NTCEONT currently",
             "CE2702/CE2708 sync meeting",
             "EKKT_TEXT compatibility UNKNOWN — critical open question"],
        ],
        widths=[5*cm,4.5*cm,8*cm]
    ))
    els.append(sp(5))
    els.append(warn(
        "⚠  Critical Open Question for CE2702 Activity 1:\n"
        "  'Can Notes Reuse RAP BO consume an application-specific own table (EKKT_TEXT) "
        "instead of SGBT_NTCEONT?'\n"
        "  Contact: BLR04 team (M K, Visakh) + Notes Reuse RAP team\n"
        "  If YES → EKKT_TEXT can be built and registered with Notes Reuse\n"
        "  If NO  → must use SGBT_NTCEONT → different table design entirely"
    ))
    els.append(PageBreak())
    return els

# ── Section 3: Sales Team ─────────────────────────────────────────────────────
def section3():
    els=[]
    els.append(sec_hdr("3","Sales Team — Reference Implementation (CE2608)",
                        "Karen Feng + Chris Xie — completed the migration that PO team will follow",
                        BTP_GREEN))
    els.append(sp(8))

    els.append(Paragraph("Who They Are", H2))
    els.append(Paragraph(
        "Karen Feng and Chris Xie are the SD (Sales & Distribution) development team who "
        "completed the reference implementation of the new text persistency in CE2608. "
        "They are the go-to team for PO to understand the implementation pattern, "
        "lessons learned, and SDM challenges.", BODY))
    els.append(sp(6))

    els.append(Paragraph("What They Built — Complete List", H2))
    for name,typ,purpose in [
        ("SDTP_TEXT / VX_TEXT","Database Table (SD-owned)",
         "New SD text table. Typed keys: SD_DOCUMENT_ID (VBELN), SD_DOCUMENT_ITEM (POSNR). "
         "TEXT_CONTENT as plain text string. REF_ fields for reference chain. "
         "Auth fields encoded via TDTITLE. SDM_VERSION tracked in VBAK/VBRK/LIKP."),
        ("SD Text Handler Class","ABAP Class (handler)",
         "Inherits CL_RSTXT_PERSISTENCE_FRAMEWORK. "
         "Registered in TTXOB for: VBBK (Sales header), VBBP (Sales item). "
         "5 methods: CREATE, CHANGE, DELETE, READ, READ_HEADERS_VIA_RANGES. "
         "IS_MIGRATION_FINISHED → calls CL_SDM_PROC_STATUS_API."),
        ("CL_SDM_SD_VBAK_TEXT_MIGRATION","ABAP Class (SDM)",
         "SDM for Sales Order documents. Inherits CL_SDM_PACKAGE_MIGRATION. "
         "Package size 30,000. Duration: 3.5 hours for 13.9M records in CCW/720 performance test."),
        ("CL_SDM_VBRK_TEXT_MIGRATION","ABAP Class (SDM)",
         "SDM for Billing documents. Same pattern as VBAK SDM."),
        ("(Delivery SDM — not built)","Gap",
         "Due to capacity issues, Delivery SDM was NOT delivered in 2608. "
         "This means IS_MIGRATION_FINISHED is ALWAYS FALSE for Sales — reads always from STXH. "
         "PO team does not have this dependency — can potentially finish faster."),
        ("P_SalesDocumentText","CDS View (table function)",
         "Existing CDS view — reads from STXH via CL_SD_S4H_STXL_UTILS. "
         "Still used in 2608 — CDS on new table not released yet (data incomplete)."),
        ("Basic CDS View on SDTP_TEXT","CDS View (planned)",
         "Will be released AFTER SDM is confirmed complete for all customers. "
         "Analytics view on top (C1 released). This is WHY they did all the work."),
    ]:
        els.append(obj_row(name, typ, purpose, BTP_GREEN))
        els.append(sp(2))

    els.append(sp(6))
    els.append(Paragraph("What Chris Xie Explained — Key Quotes from Meeting", H2))

    quotes=[
        ("On dual-write — two handler classes called simultaneously",
         "The text framework will dedicate the call to two handler classes. "
         "One is the defaulted handler class which will take care of old persistence like STXH/STXL, "
         "and we will also pass the same information to this text-object-specific handler class — "
         "this class will only take care of the new table.",
         "Chris Xie, FW Further S4 PR Support Meeting 2026-06-18"),
        ("On IS_MIGRATION_FINISHED — true/false routing",
         "There is a method to control which table will be used — old table, new table. "
         "It is very simple, just return true or false. Based on that parameter, "
         "it will decide which table to use — at text object level.",
         "Chris Xie"),
        ("On Delivery blocker — always FALSE",
         "Since delivery is not joining our development in 2608, that means we will always "
         "not finish — because we don't foresee when delivery will finish the migration. "
         "So we always set IS_MIGRATION_FINISHED to FALSE. That means READ always goes "
         "to the older persistence.",
         "Chris Xie"),
        ("On SDM execution in customer system",
         "After customer upgrades to 2608, a few days later, the SDM will be triggered "
         "automatically by SDM framework. It will work like a background job — silently "
         "in business uptime. Customer will not be aware. We will get SP incident "
         "in case there is an error.",
         "Chris Xie"),
        ("On when to release CDS views",
         "CDS views will not deliver in 2608 because we cannot ensure all customers "
         "finished migration — data is incomplete. We cannot release CDS views to "
         "customers when data is incomplete.",
         "Chris Xie"),
    ]
    for title, quote, speaker in quotes:
        hdr=Table([[Paragraph(title,ms(f"qh{title[:5]}",fontSize=8,textColor=WHITE,
                   fontName="Helvetica-Bold"))]],colWidths=[17.5*cm])
        hdr.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),BTP_GREEN),
                                  ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
                                  ("LEFTPADDING",(0,0),(-1,-1),10)]))
        els.append(hdr)
        els.append(quote_box(quote, speaker))
        els.append(sp(4))

    els.append(sp(5))
    els.append(Paragraph("Why Sales Chose Own Table (Not SGBT_NTCEONT)", H2))
    els.append(tbl(
        ["Reason","Detail"],
        [
            ["Performance","Needed application-specific attributes for joins — generic table too slow at SD data volumes"],
            ["Flexibility","Needed to add SD-specific fields: auth fields (Sales Org, Doc Type), reference chain fields"],
            ["AI / BDC access","Own table enables plain SQL without decompression — SGBT_NTCEONT also plain SQL but no SD-specific joins"],
            ["Data model","New table for Sales, Billing, Delivery are COMMON — but Procurement and Sales use different text objects so PO can choose different"],
        ],
        widths=[3.5*cm,14*cm]
    ))
    els.append(sp(5))
    els.append(note(
        "Karen Fang on PO team's choice (from meeting):\n"
        "\"For procurement — whether you want to follow the same approach or create something "
        "different, I don't know. The old table is common [STXH]. The new table for sales, "
        "billing, delivery are common. But for procurement, whether you want to follow the "
        "same or create something different — if there is no further dependency, you could "
        "create a table and migrate everything.\""
    ))
    els.append(PageBreak())
    return els

# ── Section 4: Summary ────────────────────────────────────────────────────────
def section4():
    els=[]
    els.append(sec_hdr("→","Summary — Three Teams Compared",
                        "Side by side: what each team owns and what PO team must do",
                        SAP_DARK))
    els.append(sp(8))

    els.append(tbl(
        ["Aspect","SAP Script X Team","Notes Reuse RAP Team","Sales Team"],
        [
            ["What they own",
             "STXH/STXL framework\nCL_RSTXT_PERSISTENCE_FRAMEWORK\nTTXOB HANDLER_CLASS field",
             "SGBT_NTCEONT generic table\nNotes Reuse RAP BO\nCDS views (BCSRV)",
             "SDTP_TEXT own table\nSD handler class\nSDM classes (VBAK, VBRK)\nCDS views on SDTP_TEXT (planned)"],
            ["Their role for PO",
             "Provide plug-in framework — PO registers handler class in TTXOB",
             "Provide reusable notes BO — PO must clarify EKKT_TEXT compatibility",
             "Reference implementation — PO follows same EKKT_TEXT+SDM pattern"],
            ["Key deliverable",
             "HANDLER_CLASS mechanism\nWiki guidelines published",
             "Notes RAP BO with SGBT_NTCEONT\nC1 CDS views (BCSRV)",
             "Proven SDM pattern\nHandler class pattern\nPerformance data (3.5h/13M records)"],
            ["Open question",
             "None — framework available",
             "Can EKKT_TEXT be used?\n(CRITICAL BLOCKER)",
             "None — implementation complete"],
            ["PO team must",
             "Register ZCL_PO_RSTXT_PERSISTENCE in TTXOB for EKKO+EKPO",
             "Schedule sync — answer compatibility question before designing EKKT_TEXT",
             "Use SDD + meeting insights as blueprint for EKKT_TEXT + SDM class"],
            ["Contact",
             "SAP Script X wiki\n(Rene Zink — confirmed TDTITLE usage)",
             "BLR04: M K, Visakh and team",
             "Karen Feng (karen.feng@sap.com)\nChris Xie (chris.xie@sap.com)"],
        ],
        widths=[3.5*cm,4.7*cm,4.7*cm,4.6*cm]
    ))
    els.append(sp(8))

    els.append(Paragraph("Key Technical Objects — Who Owns What", H2))
    els.append(tbl(
        ["Object","Owner Team","PO Action"],
        [
            ["STXH / STXL / STXB",             "SAP Script X",         "Do NOT modify — read via READ_TEXT only"],
            ["TTXOB",                            "SAP Script X",         "Register HANDLER_CLASS for EKKO + EKPO"],
            ["CL_RSTXT_PERSISTENCE_FRAMEWORK",  "SAP Script X",         "Inherit in ZCL_PO_RSTXT_PERSISTENCE"],
            ["CL_SDM_PACKAGE_MIGRATION",        "SAP Script X",         "Inherit in ZCL_SDM_EKKO_TEXT_MIGRATION"],
            ["CL_SDM_PROC_STATUS_API",          "SAP Script X",         "Call IS_SDM_FINISHED in handler IS_MIGRATION_FINISHED"],
            ["SGBT_NTCEONT",                    "BCSRV / Basis",        "Use only if Notes Reuse compat confirmed — ask team"],
            ["Notes Reuse RAP BO",              "Notes Reuse RAP team", "Include in PO RAP model — if EKKT_TEXT is compatible"],
            ["SDTP_TEXT (Sales)",               "SD / Sales team",      "Use as blueprint — NOT as shared table"],
            ["EKKT_TEXT (to build)",            "PO team (CE2702)",     "Build and own — follows Sales pattern"],
            ["ZCL_PO_RSTXT_PERSISTENCE",        "PO team (CE2702)",     "Build — inherits SAP Script X framework class"],
            ["ZCL_SDM_EKKO_TEXT_MIGRATION",     "PO team (CE2702)",     "Build — inherits SAP Script X SDM class"],
        ],
        widths=[5*cm,4*cm,8.5*cm]
    ))
    return els

# ── Build ─────────────────────────────────────────────────────────────────────
def build():
    doc=SimpleDocTemplate(
        OUTPUT,pagesize=A4,
        leftMargin=2*cm,rightMargin=2*cm,
        topMargin=2*cm,bottomMargin=2*cm,
        title="PO Notes Teams Code Reference Guide",
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
        c.drawString(2*cm,1.2*cm,
            "PO Notes New Persistency — SAP Script X | Notes Reuse RAP | Sales Team — Code Reference")
        c.drawRightString(19.5*cm,1.2*cm,f"Page {doc.page}")
        c.setStrokeColor(colors.HexColor("#CCCCCC"))
        c.setLineWidth(0.4)
        c.line(2*cm,1.5*cm,19.5*cm,1.5*cm)
        c.restoreState()

    doc.build(story,onFirstPage=on_page,onLaterPages=on_page)
    print(f"PDF created: {OUTPUT}")

build()
