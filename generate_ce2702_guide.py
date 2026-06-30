from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

OUTPUT = r"C:\Users\I308878\PO_LongText_Persistencey\CE2702_Implementation_Steps.pdf"

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

def step_row(num, action, detail, color=SAP_BLUE):
    n_t=Table([[Paragraph(str(num),ms(f"sn{num}{color}",fontSize=9,textColor=WHITE,
               fontName="Helvetica-Bold",alignment=TA_CENTER))]],colWidths=[0.8*cm])
    n_t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),color),
                              ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
                              ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5)]))
    a_t=Table([[Paragraph(action,ms(f"sa{num}{color}",fontSize=8,textColor=BLACK,fontName="Helvetica-Bold"))],
               [Paragraph(detail,BSML)]],colWidths=[16.7*cm])
    a_t.setStyle(TableStyle([("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
                              ("LEFTPADDING",(0,0),(-1,-1),8)]))
    t=Table([[n_t,a_t]],colWidths=[0.8*cm,16.7*cm])
    t.setStyle(TableStyle([("LINEABOVE",(0,0),(-1,0),0.5,color),
                            ("LINEBELOW",(0,0),(-1,0),0.5,GREY_BDR),
                            ("TOPPADDING",(0,0),(-1,-1),0),("BOTTOMPADDING",(0,0),(-1,-1),0),
                            ("LEFTPADDING",(0,0),(-1,-1),0),("VALIGN",(0,0),(-1,-1),"TOP")]))
    return [t, sp(3)]

# ══════════════════════════════════════════════════════════════════════════════
def cover():
    els=[]
    cov=Table([
        [Paragraph("CE2702 Scope — Implementation Guide", TITLE)],
        [Paragraph("PO Notes New Persistency — 7 Activities with Why and How", SUB)],
        [Paragraph("EKKT_TEXT  |  Handler Class  |  TTXOB Registration  |  SDM  |  OData V4 POC", SUB)],
        [Paragraph("SAP S/4HANA Procurement  |  EKKO / EKPO  |  2026-06-30", META)],
    ],colWidths=[17.5*cm])
    cov.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),SAP_DARK),
                              ("TOPPADDING",(0,0),(-1,-1),24),("BOTTOMPADDING",(0,0),(-1,-1),24),
                              ("LEFTPADDING",(0,0),(-1,-1),20)]))
    els.append(cov)
    els.append(sp(12))

    els.append(tbl(
        ["#","Activity","Why Required","Deliverable"],
        [
            ["1","Clarify Notes Reuse Compatibility",
             "Entire architecture decision depends on this — blocks table design",
             "Architecture Decision Record signed off"],
            ["2","Design EKKT_TEXT Table",
             "Handler class cannot be coded without table structure",
             "EKKT_TEXT Active in SE11"],
            ["3","Implement ZCL_PO_RSTXT_PERSISTENCE",
             "Without it STXH/STXL always used — new table never populated",
             "Handler class Active in SE24"],
            ["4","Register in TTXOB for EKKO/EKPO",
             "Without TTXOB registration handler class is never called",
             "EKKO+EKPO routing active"],
            ["5","Add SDM_VERSION to EKKO",
             "SDM framework needs status field to track migration progress",
             "SDM_VERSION field in EKKO via Append"],
            ["6","Implement ZCL_SDM_EKKO_TEXT_MIGRATION",
             "Historic texts in STXH never migrated without SDM class",
             "SDM class Active — ready to run"],
            ["7","POC dual-write via OData V4 API",
             "Proves 2708 delivery works before committing full effort",
             "POC proven in DDCI system"],
        ],
        widths=[0.8*cm,4.5*cm,6.5*cm,5.7*cm]
    ))
    els.append(sp(8))

    els.append(Paragraph("Dependency Chain", H2))
    els.append(code([
        "Activity 1 (Clarify Notes Reuse) — decision made",
        "        │",
        "        ▼",
        "Activity 2 (Design EKKT_TEXT) — table exists in SE11",
        "        │",
        "        ▼",
        "Activity 3 (Handler Class)            Activity 5 (SDM_VERSION to EKKO)",
        "        │  class active                        │  field in EKKO",
        "        ▼                                      ▼",
        "Activity 4 (TTXOB Registration)       Activity 6 (SDM Class)",
        "        │  routing active                      │  SDM class ready",
        "        │                                      │",
        "        └──────────────┬────────────────────────┘",
        "                       ▼",
        "               Activity 7 (POC in DDCI)",
        "                       │",
        "                       ▼",
        "               POC results → 2708 full implementation",
    ]))
    els.append(PageBreak())
    return els

# ── Activity 1 ────────────────────────────────────────────────────────────────
def act1():
    els=[]
    els.append(sec_hdr("1","Clarify Notes Reuse Compatibility",
                        "The single most critical question — blocks all other activities",
                        RED, RED))
    els.append(sp(8))
    els.append(warn(
        "This is a BLOCKER. Until this is answered, Activities 2-7 could go in the wrong direction. "
        "If Notes Reuse RAP only supports generic table SGBT_NTCEONT, then EKKT_TEXT design changes completely."
    ))
    els.append(sp(6))

    els.append(Paragraph("What Must Be Clarified", H2))
    els.append(tbl(
        ["Open Question","Why It Blocks"],
        [
            ["Can Notes Reuse RAP consume EKKT_TEXT (own table) instead of SGBT_NTCEONT?",
             "If NO → must use SGBT_NTCEONT → redesign entire table approach"],
            ["Has Notes Reuse RAP improved since Sales team evaluated and rejected it?",
             "If YES → generic table may now be viable → avoid building own table"],
            ["Is there a supported way to register own table with Notes Reuse RAP?",
             "If YES → defines EKKT_TEXT structure and handler interface requirements"],
        ],
        widths=[8*cm,9.5*cm]
    ))
    els.append(sp(6))

    els.append(Paragraph("Step-by-Step — How to Clarify", H2))
    steps=[
        ("Schedule sync with Notes Reuse RAP team",
         "Contact: Notes Reuse RAP team (contact TBD from CE2702/CE2708 meeting)\n"
         "Bring: Sales SDD design doc, EKKT_TEXT draft design, open questions list\n"
         "Ask: Can own table be registered? What interface is needed?"),
        ("Schedule sync with SAP Script X team",
         "Ask: Is their own-table migration guideline compatible with Notes Reuse RAP?\n"
         "Ask: What interface does the handler class need to expose for Notes Reuse?"),
        ("Schedule sync with Sales team (Chris, Karen Fang)",
         "Ask: Did they evaluate Notes Reuse RAP? Why was it rejected?\n"
         "Ask: Can SDTP_TEXT now be used with Notes Reuse? What changed?"),
        ("Document the Architecture Decision",
         "Write Architecture Decision Record (ADR):\n"
         "  Chosen option: EKKT_TEXT (own table) OR SGBT_NTCEONT (generic)\n"
         "  Reasoning and trade-offs\n"
         "  Sign-off: Nils Hartmann + Rajesh + architects"),
    ]
    for i,(a,d) in enumerate(steps,1):
        for row in step_row(i,a,d,RED): els.append(row)
    els.append(sp(5))
    els.append(ok("✅  Deliverable: Architecture Decision Record signed off by PO product team."))
    els.append(PageBreak())
    return els

# ── Activity 2 ────────────────────────────────────────────────────────────────
def act2():
    els=[]
    els.append(sec_hdr("2","Design EKKT_TEXT Table",
                        "Application-specific PO text table — must be designed before coding handler",
                        SAP_BLUE))
    els.append(sp(8))
    els.append(ibox(
        "Why better than STXH: TEXT_CONTENT = plain SQL readable string. "
        "EBELN+EBELP = typed keys (not generic CHAR70). "
        "Auth fields stored directly. CDS views can be built on top."
    ))
    els.append(sp(5))

    els.append(Paragraph("Proposed EKKT_TEXT Field Structure", H2))
    els.append(tbl(
        ["Field","Type","Length","Key","Description"],
        [
            ["MANDT",        "CLNT","3",  "✓","Client"],
            ["EBELN",        "CHAR","10", "✓","PO Number — typed, NOT generic CHAR70"],
            ["EBELP",        "NUMC","5",  "✓","Item — 00000 = header texts"],
            ["TEXT_OBJECT",  "CHAR","10", "✓","EKKO (header) or EKPO (item)"],
            ["TEXT_ID",      "CHAR","4",  "✓","F01, F02, F04 etc."],
            ["LANGUAGE",     "LANG","1",  "✓","Language key"],
            ["TEXT_CONTENT", "STRG","—",  "","Plain text string — ITF converted"],
            ["REF_TEXT_OBJ", "CHAR","10", "","Reference source object"],
            ["REF_TEXT_ID",  "CHAR","4",  "","Reference source text ID"],
            ["REF_TEXT_NAME","CHAR","70", "","Reference source document ID"],
            ["CREATED_BY",   "CHAR","12", "","Created by (sy-uname)"],
            ["CREATED_AT",   "DATS","8",  "","Created date"],
            ["CHANGED_BY",   "CHAR","12", "","Changed by"],
            ["CHANGED_AT",   "DATS","8",  "","Changed date"],
            ["AUTH_EKORG",   "CHAR","4",  "","Purchase Organization — for auth/DCL"],
            ["AUTH_BUKRS",   "CHAR","4",  "","Company Code — for auth/DCL"],
            ["AUTH_BSART",   "CHAR","4",  "","Document Type (NB, UB etc.)"],
        ],
        widths=[3.5*cm,1.8*cm,2*cm,1.2*cm,9*cm]
    ))
    els.append(sp(6))

    els.append(Paragraph("Step-by-Step — How to Create in SE11", H2))
    steps=[
        ("Review and agree table structure with architect",
         "Present EKKT_TEXT design to Nils Hartmann / Rajesh\n"
         "Confirm: field names, auth fields, TEXT_CONTENT as STRG vs CHAR132 rows\n"
         "Get sign-off before creating in SE11"),
        ("SE11 → Database Table → EKKT_TEXT → Create",
         "Short Description: PO New Text Persistency Table\n"
         "Delivery Class: A\n"
         "Data Browser: Display/Maintenance Allowed\n"
         "Enhancement Category: Can Be Enhanced (Deep)"),
        ("Add all fields from the table above",
         "Key fields first (MANDT through LANGUAGE)\n"
         "Then non-key fields (TEXT_CONTENT through AUTH_BSART)\n"
         "Use standard data elements where possible (EBELN, EBELP, TDSPRAS etc.)"),
        ("Set Technical Settings",
         "Data Class: APPL0 (Application transaction data)\n"
         "Size Category: 2 (10,000–100,000 rows — will grow with PO volume)\n"
         "Buffering: Not Allowed (frequently written)"),
        ("Save → Activate (Ctrl+F3)",
         "Status must show: Active\n"
         "Package: ZMMPOC (or agreed package)\n"
         "Transport: assign to CE2702 workbench transport"),
        ("Create secondary index",
         "SE11 → EKKT_TEXT → Indexes → Create → ZPO_TXT_I01\n"
         "Fields: EBELN, TEXT_OBJECT, TEXT_ID\n"
         "Activate index"),
    ]
    for i,(a,d) in enumerate(steps,1):
        for row in step_row(i,a,d,SAP_BLUE): els.append(row)
    els.append(sp(5))
    els.append(ok("✅  Deliverable: EKKT_TEXT Active in SE11 with all fields and index."))
    els.append(PageBreak())
    return els

# ── Activity 3 ────────────────────────────────────────────────────────────────
def act3():
    els=[]
    els.append(sec_hdr("3","Implement ZCL_PO_RSTXT_PERSISTENCE Handler Class",
                        "Inherits CL_RSTXT_PERSISTENCE_FRAMEWORK — 5 methods + IS_MIGRATION_FINISHED",
                        ORANGE))
    els.append(sp(8))
    els.append(ibox(
        "This is the automatic routing mechanism. Once registered in TTXOB, "
        "every SAVE_TEXT/READ_TEXT call for EKKO/EKPO goes through this class. "
        "No changes needed in ME21N/ME22N — the framework handles routing transparently."
    ))
    els.append(sp(5))

    els.append(Paragraph("Class Definition", H2))
    els.append(code([
        "Class name:    ZCL_PO_RSTXT_PERSISTENCE",
        "Inherits from: CL_RSTXT_PERSISTENCE_FRAMEWORK",
        "Final:         Yes",
        "Instantiation: Public",
        "Description:   PO Notes New Persistency Handler",
    ]))
    els.append(sp(5))

    els.append(Paragraph("5 Methods to Redefine + IS_MIGRATION_FINISHED", H2))
    els.append(tbl(
        ["Method","Triggered By","Logic Summary"],
        [
            ["CREATE","SAVE_TEXT — new text",
             "Parse EBELN+EBELP from TDNAME. Check TDREF flag. "
             "Convert ITF→string. INSERT EKKT_TEXT. If SDM not done → also write STXH."],
            ["CHANGE","SAVE_TEXT — update text",
             "Same as CREATE but UPDATE. If user modified a reference → CLEAR REF fields permanently."],
            ["DELETE","DELETE_TEXT",
             "DELETE from EKKT_TEXT. If SDM not done → also delete from STXH."],
            ["READ","READ_TEXT",
             "If IS_MIGRATION_FINISHED=FALSE → read STXH/STXL.\n"
             "If TRUE → read EKKT_TEXT. Convert TEXT_CONTENT string→ITF for return."],
            ["READ_HEADERS_VIA_RANGES","SELECT_TEXT",
             "If IS_MIGRATION_FINISHED=FALSE → read STXH headers.\n"
             "If TRUE → read EKKT_TEXT headers."],
            ["IS_MIGRATION_FINISHED","Called internally",
             "CL_SDM_PROC_STATUS_API=>IS_SDM_FINISHED for ZCL_SDM_EKKO_TEXT_MIGRATION.\n"
             "Result buffered for dialog session — no repeated SELECT."],
        ],
        widths=[4.5*cm,4*cm,9*cm]
    ))
    els.append(sp(5))

    els.append(Paragraph("Key TDNAME Parsing for This System", H2))
    els.append(code([
        "\" EKKO (header): TDNAME = PO number only",
        "IF im_header-tdobject = 'EKKO'.",
        "  lv_ebeln = im_header-tdname.   \" e.g. '4500077744'",
        "  lv_ebelp = '00000'.",
        "ELSE.   \" EKPO (item): NO SPACE — confirmed for this system",
        "  lv_ebeln = im_header-tdname(10).    \" '4500077744'",
        "  lv_ebelp = im_header-tdname+10(5).  \" '00010' — offset 10, no space",
        "ENDIF.",
    ]))
    els.append(sp(5))

    steps=[
        ("SE24 → ZCL_PO_RSTXT_PERSISTENCE → Create",
         "Class type: Regular Class. Inherits: CL_RSTXT_PERSISTENCE_FRAMEWORK. Final: Yes."),
        ("Redefine IS_MIGRATION_FINISHED first",
         "METHOD is_migration_finished.\n"
         "  rv_finished = cl_sdm_proc_status_api=>is_sdm_finished(\n"
         "    i_sdm_name = 'ZCL_SDM_EKKO_TEXT_MIGRATION' ).\n"
         "ENDMETHOD.\n"
         "This controls all read/write routing — implement before other methods."),
        ("Implement CREATE method",
         "Parse TDNAME → EBELN+EBELP. Check TDREF='X' (reference) vs ' ' (copy).\n"
         "Call CONVERT_ITF_TO_STREAM_TEXT for copy. INSERT EKKT_TEXT.\n"
         "If IS_MIGRATION_FINISHED=FALSE → also call standard STXH write."),
        ("Implement CHANGE method",
         "Same as CREATE but UPDATE EKKT_TEXT.\n"
         "If content written and REF fields were populated → CLEAR REF fields (reference broken)."),
        ("Implement DELETE method",
         "DELETE FROM EKKT_TEXT by key.\n"
         "If IS_MIGRATION_FINISHED=FALSE → also delete from STXH."),
        ("Implement READ method",
         "If IS_MIGRATION_FINISHED=FALSE → call READ_TEXT to get from STXH/STXL.\n"
         "If TRUE → SELECT from EKKT_TEXT → CONVERT_STREAM_TO_ITF_TEXT → return ITF table."),
        ("Implement READ_HEADERS_VIA_RANGES",
         "Route to STXH or EKKT_TEXT based on IS_MIGRATION_FINISHED.\n"
         "Return text headers in expected THEAD format."),
        ("Activate all methods (Ctrl+F3)",
         "All 6 methods must be blue (active) before TTXOB registration."),
    ]
    for i,(a,d) in enumerate(steps,1):
        for row in step_row(i,a,d,ORANGE): els.append(row)
    els.append(sp(5))
    els.append(ok("✅  Deliverable: ZCL_PO_RSTXT_PERSISTENCE Active with all 6 methods."))
    els.append(PageBreak())
    return els

# ── Activity 4 ────────────────────────────────────────────────────────────────
def act4():
    els=[]
    els.append(sec_hdr("4","Register in TTXOB for EKKO and EKPO",
                        "Without TTXOB registration the handler class is NEVER called",
                        TEAL))
    els.append(sp(8))
    els.append(warn(
        "⚠  This is the activation step. Once TTXOB is updated, ALL applications using "
        "SAVE_TEXT/READ_TEXT for EKKO/EKPO will route through ZCL_PO_RSTXT_PERSISTENCE. "
        "Test in sandbox first — do NOT register in production until POC is verified."
    ))
    els.append(sp(5))

    steps=[
        ("SE11 → Table TTXOB → Change mode",
         "TTXOB is the text object definition table.\n"
         "Alternative: SPRO → MM → Purchasing → Purchase Order → Texts for Purchase Order\n"
         "  → Define Text Types for Purchase Order Header → check HANDLER_CLASS field"),
        ("Find row: TDOBJECT = 'EKKO'",
         "Set field: HANDLER_CLASS = 'ZCL_PO_RSTXT_PERSISTENCE'\n"
         "Save → assign transport"),
        ("Find row: TDOBJECT = 'EKPO'",
         "Set field: HANDLER_CLASS = 'ZCL_PO_RSTXT_PERSISTENCE'\n"
         "Save → assign transport"),
        ("Verify registration",
         "SE16N → TTXOB → filter TDOBJECT = EKKO → confirm HANDLER_CLASS populated\n"
         "SE16N → TTXOB → filter TDOBJECT = EKPO → confirm HANDLER_CLASS populated"),
        ("Test dual-write immediately in sandbox",
         "ME21N → create PO with header text → Save\n"
         "Check 1: SE16N → EKKT_TEXT → row exists with TEXT_CONTENT ✓ (new table)\n"
         "Check 2: SE16N → STXH → row exists for EKKO (old table) ✓ (IS_MIGRATION_FINISHED=FALSE)\n"
         "Both must be written — dual-write confirmed"),
        ("Test READ routing",
         "ME23N → open same PO → Header → Texts → text still visible ✓\n"
         "IS_MIGRATION_FINISHED=FALSE → reads from STXH → legacy apps unchanged"),
    ]
    for i,(a,d) in enumerate(steps,1):
        for row in step_row(i,a,d,TEAL): els.append(row)
    els.append(sp(5))
    els.append(ok("✅  Deliverable: EKKO and EKPO routing active. Dual-write confirmed in sandbox."))
    els.append(PageBreak())
    return els

# ── Activity 5 ────────────────────────────────────────────────────────────────
def act5():
    els=[]
    els.append(sec_hdr("5","Add SDM_VERSION Field to EKKO",
                        "SDM framework tracks migration progress via this field in root table",
                        PURPLE))
    els.append(sp(8))
    els.append(ibox(
        "WHY: SDM class selects packages of unmigrated POs using WHERE sdm_version < target. "
        "IS_MIGRATION_FINISHED checks if ALL EKKO rows have sdm_version = target. "
        "Without this field the SDM class cannot track which POs are migrated."
    ))
    els.append(sp(5))

    steps=[
        ("Coordinate with PO standard team (Nils/Jiss)",
         "EKKO may already have SDM_VERSION from another SDM (e.g. SDSLS_SOFI clash in Sales)\n"
         "Agree on: field name, version constant value, numbering sequence\n"
         "Ensure no clash with other active SDMs on EKKO"),
        ("Create Append Structure ZEKKO_TEXT_SDM",
         "SE11 → Structure → ZEKKO_TEXT_SDM → Create\n"
         "Add field: SDM_VERSION  TYPE NUMC  LENGTH 2\n"
         "Short Description: SDM Version — PO Text Migration\n"
         "Activate structure"),
        ("Assign Append Structure to EKKO",
         "SE11 → EKKO → Change → Extras → Append Structure\n"
         "Enter: ZEKKO_TEXT_SDM → Activate\n"
         "NOTE: Direct EKKO modification not allowed in public cloud — must use Append"),
        ("Set SDM_VERSION in PO save processing",
         "When NEW PO created: set SDM_VERSION = target version constant\n"
         "When PO CHANGED:\n"
         "  If SDM_VERSION < target → keep old (not yet migrated by SDM)\n"
         "  If SDM_VERSION = target → write to EKKT_TEXT only (migration complete for this PO)"),
        ("Define version constant",
         "Create constant in class or interface:\n"
         "  IF_ZPO_SDM_CONSTANTS=>PO_TEXT_SDM_VERSION = '03' (or agreed value)\n"
         "  Used in: SDM class GET_STATUS_VALUE_DONE + handler IS_MIGRATION_FINISHED"),
        ("Verify",
         "ME21N → create new PO → SE16N → EKKO → confirm SDM_VERSION field populated\n"
         "Value = target version constant ✓"),
    ]
    for i,(a,d) in enumerate(steps,1):
        for row in step_row(i,a,d,PURPLE): els.append(row)
    els.append(sp(5))
    els.append(ok("✅  Deliverable: SDM_VERSION field in EKKO via Append Structure. Version constant defined."))
    els.append(PageBreak())
    return els

# ── Activity 6 ────────────────────────────────────────────────────────────────
def act6():
    els=[]
    els.append(sec_hdr("6","Implement ZCL_SDM_EKKO_TEXT_MIGRATION",
                        "Background batch job — migrates ALL historic STXH/STXL texts to EKKT_TEXT",
                        BTP_GREEN))
    els.append(sp(8))
    els.append(ibox(
        "WHY: The handler class (Activity 3) handles NEW texts from registration date onwards. "
        "But millions of EXISTING PO texts are only in STXH/STXL and will never trigger SAVE_TEXT again. "
        "This SDM class migrates all historic data in background — without it IS_MIGRATION_FINISHED can never become TRUE."
    ))
    els.append(sp(5))

    els.append(Paragraph("SDM Methods to Implement", H2))
    els.append(tbl(
        ["Method","Returns","Purpose"],
        [
            ["GET_TABLE_NAME",         "'EKKO'",             "Root table for packaging"],
            ["GET_CLIENT_FIELD",       "'MANDT'",            "Client field name"],
            ["GET_SELECTIVE_FIELD",    "'EBELN'",            "Key field for packages"],
            ["GET_STATUS_FIELD",       "'SDM_VERSION'",      "Migration status field"],
            ["GET_STATUS_VALUE_DONE",  "target version const","Value meaning migration done"],
            ["GET_PACKAGE_SIZE",       "30000",              "POs per package — ~1 min per package"],
            ["MUST_RUN",               "abap_true",          "Always run this SDM"],
            ["MIGRATE_DATA",           "—",                  "Main migration logic (see below)"],
            ["MIGRATE_DATA_FINISHED",  "—",                  "Check if all EKKO rows migrated"],
        ],
        widths=[5*cm,4*cm,8.5*cm]
    ))
    els.append(sp(5))

    els.append(Paragraph("MIGRATE_DATA — Logic Summary", H2))
    els.append(code([
        "MIGRATE_DATA logic for each package of EKKO rows:",
        "",
        "Step 1: Select package of unmigrated POs",
        "  SELECT ebeln, ekorg, bukrs, bsart FROM ekko",
        "    WHERE sdm_version < target_version  (using framework where condition)",
        "    UP TO 30000 ROWS.",
        "",
        "Step 2: For each PO — read all text headers from STXH",
        "  Header:  STXH WHERE tdobject='EKKO' AND tdname = ebeln",
        "  Items:   STXH WHERE tdobject='EKPO' AND tdname BETWEEN ebeln+'00000' AND ebeln+'99999'",
        "",
        "Step 3: For each STXH row — read content via READ_TEXT",
        "  CALL FUNCTION 'READ_TEXT'",
        "    EXPORTING id=tdid language=tdspras name=tdname object=tdobject",
        "    TABLES lines=lt_lines.",
        "",
        "Step 4: Convert ITF → plain text string",
        "  CALL FUNCTION 'CONVERT_ITF_TO_STREAM_TEXT'",
        "    TABLES i_text=lt_lines IMPORTING e_text=lv_content.",
        "",
        "Step 5: DELETE existing from EKKT_TEXT (restartability)",
        "  DELETE FROM ekkt_text WHERE ebeln=... AND text_id=... AND language=...",
        "",
        "Step 6: INSERT into EKKT_TEXT",
        "  INSERT ekkt_text: ebeln, ebelp, text_object, text_id, language,",
        "                    text_content, ref_text_obj, ref_text_id, ref_text_name,",
        "                    auth_ekorg, auth_bukrs, auth_bsart, created_by, created_at.",
        "",
        "Step 7: UPDATE EKKO SDM_VERSION = target (marks PO as migrated)",
        "  UPDATE ekko SET sdm_version = target WHERE ebeln = ...",
        "",
        "  Old STXH/STXL records NOT deleted — safety net for restart.",
    ]))
    els.append(sp(5))

    steps=[
        ("Create SDM class in SE24",
         "Class name: ZCL_SDM_EKKO_TEXT_MIGRATION\n"
         "Inherits from: CL_SDM_PACKAGE_MIGRATION\n"
         "Package: ZMMPOC  Description: PO Notes SDM Migration Class"),
        ("Implement all GET_* methods",
         "These are simple one-liners returning constants:\n"
         "  GET_TABLE_NAME → 'EKKO'\n"
         "  GET_SELECTIVE_FIELD → 'EBELN'\n"
         "  GET_STATUS_FIELD → 'SDM_VERSION'\n"
         "  GET_PACKAGE_SIZE → 30000\n"
         "  GET_STATUS_VALUE_DONE → IF_ZPO_SDM_CONSTANTS=>PO_TEXT_SDM_VERSION"),
        ("Implement MIGRATE_DATA",
         "Follow logic above — SELECT EKKO → read STXH → READ_TEXT → CONVERT → DELETE+INSERT EKKT_TEXT → UPDATE EKKO"),
        ("Implement MIGRATE_DATA_FINISHED",
         "SELECT COUNT(*) FROM ekko WHERE sdm_version < target\n"
         "If = 0 → migration complete\n"
         "If > 0 → raise error with count of remaining records"),
        ("Activate class (Ctrl+F3)",
         "All methods must be active before SDM can be executed"),
        ("Test in DDCI sandbox — run SDM for test POs",
         "Execute via SDM cockpit or direct ABAP call\n"
         "Expected: 3.5 hours for 13M records based on Sales performance test\n"
         "Package size 30,000 stays within Open SQL limit of 32,767"),
    ]
    for i,(a,d) in enumerate(steps,1):
        for row in step_row(i,a,d,BTP_GREEN): els.append(row)
    els.append(sp(5))
    els.append(ok("✅  Deliverable: ZCL_SDM_EKKO_TEXT_MIGRATION Active and tested on DDCI."))
    els.append(PageBreak())
    return els

# ── Activity 7 ────────────────────────────────────────────────────────────────
def act7():
    els=[]
    els.append(sec_hdr("7","POC — Write to Both STXH and EKKT_TEXT via Modernized OData V4 API",
                        "Prove the end-to-end flow works in DDCI before committing 2708 effort",
                        SAP_DARK))
    els.append(sp(8))
    els.append(ibox(
        "WHY POC: Without this proof, 2708 delivery could discover blockers mid-sprint. "
        "The POC runs in DDCI — completely separate from 2702 development. "
        "If POC works → cross-port to main development for 2708. "
        "Effort is NOT wasted — proven code can be reused directly."
    ))
    els.append(sp(5))

    els.append(Paragraph("POC Goal Statement (as agreed in CE2702/CE2708 meeting)", H2))
    els.append(ibox(
        "Prove that when a PO is created via the new modernized PO OData V4 API:\n"
        "  1. Notes can be written to EKKT_TEXT (new persistency)\n"
        "  2. Notes are ALSO written to STXH/STXL (old — dual-write)\n"
        "  3. CDS view on EKKT_TEXT returns the text content correctly\n"
        "  4. Legacy transaction ME23N still shows the text (reads from STXH)"
    ))
    els.append(sp(5))

    steps=[
        ("Set up DDCI system — spin off from current Maple/MEPO state",
         "Do NOT use the main 2702 development system\n"
         "Spin off DDCI from current state of Maple (modernized PO)\n"
         "This isolates POC work — no risk to 2702 delivery"),
        ("Model Notes in PO OData V4 API (coordinate with MEPO/Maple team)",
         "Option A: Use Notes Reuse RAP component (if compatible with EKKT_TEXT — from Activity 1)\n"
         "Option B: Model own text entity in PO RAP Business Object\n"
         "Minimum for POC: a simple CREATE action that accepts text content + text ID"),
        ("Wire dual-write in OData V4 save flow",
         "When PO saved via new API:\n"
         "  Call SAVE_TEXT → handler class routes to EKKT_TEXT (Activity 4 registered)\n"
         "  IS_MIGRATION_FINISHED=FALSE → BOTH EKKT_TEXT and STXH written"),
        ("Build basic CDS view on EKKT_TEXT",
         "CDS view: ZI_POText\n"
         "  Basic view on EKKT_TEXT with typed EBELN+EBELP keys\n"
         "  DCL for authorization using AUTH_EKORG, AUTH_BUKRS\n"
         "  Analytics annotation for BW extraction (full C1 release in 2708)"),
        ("Run end-to-end verification",
         "Create PO via new OData V4 API with text → Verify:\n"
         "  ✓ SE16N → EKKT_TEXT: row with plain TEXT_CONTENT, SOURCE equivalent\n"
         "  ✓ SE16N → STXH: row also exists (dual-write working)\n"
         "  ✓ SELECT from CDS view ZI_POText: text content visible\n"
         "  ✓ ME23N (legacy): text still visible (reads from STXH — IS_MIGRATION_FINISHED=FALSE)"),
        ("Document POC results",
         "Write POC findings document:\n"
         "  What worked, what did not, blockers found\n"
         "  Performance data from DDCI\n"
         "  Recommendations for 2708 full implementation"),
        ("Cross-port to main development for 2708",
         "If POC passes → transport proven code to main development landscape\n"
         "2708 starts from proven base — not from scratch"),
    ]
    for i,(a,d) in enumerate(steps,1):
        for row in step_row(i,a,d,SAP_DARK): els.append(row)
    els.append(sp(5))
    els.append(ok("✅  Deliverable: POC documented, DDCI proof available, cross-port plan confirmed."))
    els.append(PageBreak())
    return els

# ── Summary ───────────────────────────────────────────────────────────────────
def summary():
    els=[]
    els.append(sec_hdr("→","CE2702 Complete Summary",
                        "All 7 activities — why, what and deliverable", GREEN_OK))
    els.append(sp(8))

    els.append(tbl(
        ["#","Activity","Why Required","Key Steps","Deliverable"],
        [
            ["1","Clarify Notes Reuse",
             "Blocks table design decision",
             "3 team syncs → Architecture Decision Record",
             "ADR signed off"],
            ["2","Design EKKT_TEXT",
             "Handler cannot be coded without table",
             "SE11 create → 17 fields → index",
             "EKKT_TEXT Active"],
            ["3","Handler Class",
             "STXH always used without it",
             "SE24 → inherit CL_RSTXT_PERSISTENCE_FRAMEWORK → 6 methods",
             "ZCL_PO_RSTXT_PERSISTENCE Active"],
            ["4","TTXOB Registration",
             "Handler never called without it",
             "TTXOB EKKO+EKPO → HANDLER_CLASS = class name",
             "Routing active, dual-write proven"],
            ["5","SDM_VERSION to EKKO",
             "SDM tracks progress via this field",
             "Append Structure → SE11 → version constant",
             "SDM_VERSION field in EKKO"],
            ["6","SDM Class",
             "Historic texts never migrated without it",
             "SE24 → inherit CL_SDM_PACKAGE_MIGRATION → 7 methods",
             "ZCL_SDM_EKKO_TEXT_MIGRATION Active"],
            ["7","POC in DDCI",
             "Blocks unknown 2708 delivery risks",
             "DDCI setup → model notes in API → dual-write → CDS → verify",
             "POC proven, cross-port plan ready"],
        ],
        widths=[0.8*cm,3.5*cm,4*cm,5*cm,4.2*cm]
    ))
    els.append(sp(8))

    els.append(Paragraph("Key Technical Objects Created in CE2702", H2))
    els.append(tbl(
        ["Object","Type","Transaction","Purpose"],
        [
            ["EKKT_TEXT",                    "Database Table",  "SE11","New PO text persistency table"],
            ["ZCL_PO_RSTXT_PERSISTENCE",     "ABAP Class",      "SE24","Handler class — routes SAVE_TEXT/READ_TEXT"],
            ["ZEKKO_TEXT_SDM",               "Append Structure", "SE11","Adds SDM_VERSION to EKKO"],
            ["IF_ZPO_SDM_CONSTANTS",         "Interface",       "SE24","Version constants for SDM"],
            ["ZCL_SDM_EKKO_TEXT_MIGRATION",  "ABAP Class",      "SE24","SDM migration class"],
            ["ZI_POText",                    "CDS View",        "ADT", "Basic CDS view on EKKT_TEXT"],
            ["TTXOB (updated)",              "Customizing Table","SE11","Handler class registered for EKKO/EKPO"],
        ],
        widths=[5*cm,4*cm,2.5*cm,6*cm]
    ))
    return els

# ── Build ─────────────────────────────────────────────────────────────────────
def build():
    doc=SimpleDocTemplate(
        OUTPUT,pagesize=A4,
        leftMargin=2*cm,rightMargin=2*cm,
        topMargin=2*cm,bottomMargin=2*cm,
        title="CE2702 PO Notes New Persistency Implementation Guide",
        author="SAP PO Long Text Team",
    )
    story=[]
    story.extend(cover())
    story.extend(act1())
    story.extend(act2())
    story.extend(act3())
    story.extend(act4())
    story.extend(act5())
    story.extend(act6())
    story.extend(act7())
    story.extend(summary())

    def on_page(c,doc):
        c.saveState()
        c.setFont("Helvetica",7)
        c.setFillColor(colors.HexColor("#888888"))
        c.drawString(2*cm,1.2*cm,
            "CE2702 PO Notes New Persistency — 7 Activities Implementation Guide")
        c.drawRightString(19.5*cm,1.2*cm,f"Page {doc.page}")
        c.setStrokeColor(colors.HexColor("#CCCCCC"))
        c.setLineWidth(0.4)
        c.line(2*cm,1.5*cm,19.5*cm,1.5*cm)
        c.restoreState()

    doc.build(story,onFirstPage=on_page,onLaterPages=on_page)
    print(f"PDF created: {OUTPUT}")

build()
