from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

OUTPUT = r"C:\Users\I308878\PO_LongText_Persistencey\ZCL_PO_LONGTEXT_HANDLER_SE24_Guide.pdf"

SAP_DARK  = colors.HexColor("#003366")
SAP_BLUE  = colors.HexColor("#0070F2")
SAP_LIGHT = colors.HexColor("#E8F4FD")
ORANGE    = colors.HexColor("#E87722")
TEAL      = colors.HexColor("#007B8A")
TEAL_LIGHT= colors.HexColor("#E0F5F7")
GOLD      = colors.HexColor("#F0AB00")
GOLD_LIGHT= colors.HexColor("#FFFBE6")
RED       = colors.HexColor("#BB0000")
RED_LIGHT = colors.HexColor("#FFF0F0")
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
BODY   = ms("B",  fontSize=8.5,textColor=BLACK,   leading=13, spaceAfter=3, alignment=TA_JUSTIFY)
BSML   = ms("BS", fontSize=8,  textColor=BLACK,   leading=12, spaceAfter=2)
CODE_S = ms("CS", fontSize=7.5,textColor=CODE_FG, fontName="Courier", leading=11, spaceAfter=1)
TH     = ms("TH", fontSize=8,  textColor=WHITE,   fontName="Helvetica-Bold", alignment=TA_CENTER)
TC     = ms("TC", fontSize=8,  textColor=BLACK,   leading=11)
TC_C   = ms("TCC",fontSize=8,  textColor=BLACK,   leading=11, alignment=TA_CENTER)
TC_G   = ms("TCG",fontSize=8,  textColor=GREEN_OK,fontName="Helvetica-Bold", leading=11, alignment=TA_CENTER)
TC_B   = ms("TCB",fontSize=8,  textColor=SAP_DARK,fontName="Helvetica-Bold", leading=11)
SN     = ms("SN", fontSize=16, textColor=WHITE,   fontName="Helvetica-Bold", alignment=TA_CENTER)
ST     = ms("STt",fontSize=10, textColor=WHITE,   fontName="Helvetica-Bold")
SS     = ms("SSb",fontSize=8,  textColor=colors.HexColor("#AACCFF"), fontName="Helvetica-Oblique")

def sp(n=5): return Spacer(1, n)

def sec_hdr(num, title, subtitle, hdr=SAP_DARK, nc=None):
    if not nc: nc=hdr
    nt=Table([[Paragraph(str(num),SN)]],colWidths=[1.4*cm],rowHeights=[1.2*cm])
    nt.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),nc),("VALIGN",(0,0),(-1,-1),"MIDDLE")]))
    tt=Table([[Paragraph(title,ST)],[Paragraph(subtitle,SS)]],colWidths=[16.1*cm])
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

def warn(t): return ibox(t,RED_LIGHT,RED)
def ok(t):   return ibox(t,GREEN_LT,GREEN_OK)
def note(t): return ibox(t,GOLD_LIGHT,GOLD)

def code(lines):
    rows=[[Paragraph(l.replace(" ","&nbsp;").replace("<","&lt;").replace(">","&gt;") or "&nbsp;",CODE_S)] for l in lines]
    t=Table(rows,colWidths=[17.5*cm])
    t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),CODE_BG),
                            ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
                            ("LEFTPADDING",(0,0),(-1,-1),8),("RIGHTPADDING",(0,0),(-1,-1),6)]))
    return t

def step_row(num, action, detail, color=SAP_BLUE):
    n_t=Table([[Paragraph(str(num),ms(f"sn{num}",fontSize=10,textColor=WHITE,
               fontName="Helvetica-Bold",alignment=TA_CENTER))]],
              colWidths=[0.8*cm])
    n_t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),color),
                              ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
                              ("TOPPADDING",(0,0),(-1,-1),6),
                              ("BOTTOMPADDING",(0,0),(-1,-1),6)]))
    a_t=Table([[Paragraph(action,ms(f"sa{num}",fontSize=8,textColor=BLACK,fontName="Helvetica-Bold"))],
               [Paragraph(detail,BSML)]],colWidths=[16.7*cm])
    a_t.setStyle(TableStyle([("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
                              ("LEFTPADDING",(0,0),(-1,-1),8)]))
    t=Table([[n_t,a_t]],colWidths=[0.8*cm,16.7*cm])
    t.setStyle(TableStyle([("LINEABOVE",(0,0),(-1,0),0.5,color),
                            ("LINEBELOW",(0,0),(-1,0),0.5,GREY_BDR),
                            ("TOPPADDING",(0,0),(-1,-1),0),("BOTTOMPADDING",(0,0),(-1,-1),0),
                            ("LEFTPADDING",(0,0),(-1,-1),0),("VALIGN",(0,0),(-1,-1),"TOP")]))
    return [t, sp(3)]

def param_table(rows_data, title=""):
    if title:
        pass
    hdr=[[Paragraph(h,TH) for h in ["Parameter","Type","Typing Method","Associated Type","Default","Purpose"]]]
    rows=[]
    for p,typ,tm,at,dv,pur in rows_data:
        rows.append([Paragraph(p, TC_B),
                     Paragraph(typ, TC_C),
                     Paragraph(tm, TC_C),
                     Paragraph(at, ms(f"at{p}",fontSize=8,textColor=TEAL,fontName="Helvetica-Bold")),
                     Paragraph(dv, TC_C),
                     Paragraph(pur, BSML)])
    t=Table(hdr+rows,colWidths=[3.2*cm,2*cm,2*cm,2.8*cm,1.8*cm,5.7*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),TEAL),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[TEAL_LIGHT,WHITE]),
        ("GRID",(0,0),(-1,-1),0.4,GREY_BDR),
        ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
        ("LEFTPADDING",(0,0),(-1,-1),5),("VALIGN",(0,0),(-1,-1),"TOP"),
    ]))
    return t

# ══════════════════════════════════════════════════════════════════════════════
def cover():
    els=[]
    cov=Table([
        [Paragraph("Step 2 — Create ZCL_PO_LONGTEXT_HANDLER", TITLE)],
        [Paragraph("SE24 Class Builder — Field-by-Field Creation Guide", SUB)],
        [Paragraph("Handler Class: reads STXL via READ_TEXT · writes plain rows to ZPO_LONGTEXT", SUB)],
        [Paragraph("TDID=F01  |  Language=D  |  EKPO TDNAME=no space  |  2026-06-28", META)],
    ],colWidths=[17.5*cm])
    cov.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),SAP_DARK),
                              ("TOPPADDING",(0,0),(-1,-1),24),("BOTTOMPADDING",(0,0),(-1,-1),24),
                              ("LEFTPADDING",(0,0),(-1,-1),20)]))
    els.append(cov)
    els.append(sp(12))

    els.append(Paragraph("What This Class Does", H2))
    els.append(Paragraph(
        "ZCL_PO_LONGTEXT_HANDLER is the engine of the PO Long Text persistency solution. "
        "It has two methods: WRITE_TO_PERSISTENCE reads the compressed text from STXL using "
        "SAP function module READ_TEXT, then writes each plain line as a row into ZPO_LONGTEXT. "
        "READ_FROM_PERSISTENCE does a simple SELECT from ZPO_LONGTEXT — no READ_TEXT needed.", BODY))
    els.append(sp(6))

    els.append(tbl(
        ["Method","Level","Visibility","Purpose"],
        [
            ["WRITE_TO_PERSISTENCE","Static","Public",
             "Builds TDNAME → calls READ_TEXT → deletes old rows → inserts plain lines to ZPO_LONGTEXT"],
            ["READ_FROM_PERSISTENCE","Static","Public",
             "SELECT * FROM ZPO_LONGTEXT WHERE EBELN = ... ORDER BY LINE_COUNTER"],
        ],
        widths=[5.5*cm,2.5*cm,2.5*cm,7*cm]
    ))
    els.append(sp(8))
    els.append(warn(
        "⚠  EKPO TDNAME — System-Specific (confirmed from STXH):\n"
        "  EKKO: lv_tdname = iv_ebeln              → e.g. 4500077744\n"
        "  EKPO: CONCATENATE iv_ebeln iv_ebelp      → e.g. 450007774400010  (NO space)\n"
        "  Standard SAP documentation says EBELN + SPACE + EBELP — NOT valid for this system."
    ))
    els.append(PageBreak())
    return els

# ── Phase A: Create Class ─────────────────────────────────────────────────────
def phaseA():
    els=[]
    els.append(sec_hdr("A","Open SE24 and Create the Class",
                        "Transaction SE24 — Class Builder", SAP_DARK))
    els.append(sp(8))
    steps=[
        ("Open SE24",
         "Transaction code: SE24 → press Enter"),
        ("Enter class name",
         "Object Type: select radio button 'Class/Interface'\n"
         "Object Name: ZCL_PO_LONGTEXT_HANDLER\n"
         "Click Create button (or press F5)"),
        ("Fill class properties",
         "Description:    PO Long Text Handler — Read and Write Persistency\n"
         "Instantiation:  Public\n"
         "Final:          ✓ tick (prevents subclassing)\n"
         "Class Type:     Regular Class\n"
         "Click Save"),
        ("Assign package and transport",
         "Package: ZMM (or your development package)\n"
         "Transport: assign to your active workbench transport\n"
         "Save — class is created in New status"),
    ]
    for i,(a,d) in enumerate(steps,1):
        for row in step_row(i,a,d,SAP_DARK): els.append(row)
    els.append(PageBreak())
    return els

# ── Phase B: Method 1 definition ─────────────────────────────────────────────
def phaseB():
    els=[]
    els.append(sec_hdr("B","Add Method: WRITE_TO_PERSISTENCE",
                        "Methods tab — Static Public method with 5 importing parameters",
                        SAP_BLUE))
    els.append(sp(8))
    steps=[
        ("Go to Methods tab",
         "Click the Methods tab at the top of the SE24 screen"),
        ("Add method row",
         "Click in the empty row under 'Method' column and enter:\n"
         "  Method:      WRITE_TO_PERSISTENCE\n"
         "  Level:       Static Method\n"
         "  Visibility:  Public\n"
         "  Description: Write text lines to ZPO_LONGTEXT"),
        ("Open Parameters for this method",
         "With the WRITE_TO_PERSISTENCE row selected (highlighted blue)\n"
         "Click the Parameters button in the toolbar at the top\n"
         "The Parameters screen opens"),
    ]
    for i,(a,d) in enumerate(steps,1):
        for row in step_row(i,a,d,SAP_BLUE): els.append(row)

    els.append(sp(6))
    els.append(Paragraph("Parameters for WRITE_TO_PERSISTENCE", H2))
    els.append(ibox(
        "Add one row per parameter. For each: enter Parameter name → select Type (Importing) "
        "→ select Typing Method (Type) → enter Associated Type name."
    ))
    els.append(sp(4))
    els.append(param_table([
        ("IV_EBELN",    "Importing","Type","EBELN",    "—",       "Purchase Order Number"),
        ("IV_EBELP",    "Importing","Type","EBELP",    "00000",   "PO Item — default 00000 for header texts"),
        ("IV_TDOBJECT", "Importing","Type","TDOBJECT", "—",       "Text Object: EKKO or EKPO"),
        ("IV_TDID",     "Importing","Type","TDID",     "—",       "Text ID: F01 (confirmed for this system)"),
        ("IV_TDSPRAS",  "Importing","Type","TDSPRAS",  "—",       "Language key: D"),
    ]))
    els.append(sp(4))
    els.append(note(
        "To set default value for IV_EBELP:\n"
        "  Click the IV_EBELP row → Default Value column → enter: 00000\n"
        "  This means callers can omit IV_EBELP for header texts (defaults to 00000 = header)"
    ))
    els.append(sp(6))
    steps2=[
        ("Press F3 or Back",
         "Press F3 to return to the Methods tab after entering all 5 parameters"),
        ("Save",
         "Ctrl+S to save the method definition"),
    ]
    for i,(a,d) in enumerate(steps2,4):
        for row in step_row(i,a,d,SAP_BLUE): els.append(row)
    els.append(PageBreak())
    return els

# ── Phase C: Method 2 definition ─────────────────────────────────────────────
def phaseC():
    els=[]
    els.append(sec_hdr("C","Add Method: READ_FROM_PERSISTENCE",
                        "Methods tab — Static Public method with 1 importing + 1 returning parameter",
                        TEAL))
    els.append(sp(8))
    steps=[
        ("Add second method row",
         "On the Methods tab, click next empty row and enter:\n"
         "  Method:      READ_FROM_PERSISTENCE\n"
         "  Level:       Static Method\n"
         "  Visibility:  Public\n"
         "  Description: Read text lines from ZPO_LONGTEXT"),
        ("Open Parameters",
         "With READ_FROM_PERSISTENCE row selected → click Parameters button"),
        ("Add parameters",
         "Add two rows:"),
    ]
    for i,(a,d) in enumerate(steps,1):
        for row in step_row(i,a,d,TEAL): els.append(row)

    els.append(sp(4))
    els.append(param_table([
        ("IV_EBELN",  "Importing","Type",     "EBELN",             "—", "Purchase Order Number to read"),
        ("RT_LINES",  "Returning","Type (Ref)","TABLE OF ZPO_LONGTEXT","—","Returns all text rows for this PO"),
    ]))
    els.append(sp(4))
    els.append(note(
        "For RT_LINES Returning parameter:\n"
        "  Typing Method: select 'Type'\n"
        "  Associated Type: enter TABLE OF ZPO_LONGTEXT\n"
        "  Pass By Value: ✓ tick (Returning parameters must be passed by value)"
    ))
    els.append(sp(6))
    steps2=[
        ("Press F3",
         "Return to Methods tab"),
        ("Save",
         "Ctrl+S"),
    ]
    for i,(a,d) in enumerate(steps2,4):
        for row in step_row(i,a,d,TEAL): els.append(row)
    els.append(PageBreak())
    return els

# ── Phase D: Implement WRITE ──────────────────────────────────────────────────
def phaseD():
    els=[]
    els.append(sec_hdr("D","Implement WRITE_TO_PERSISTENCE — Full Code",
                        "Double-click method name → source editor opens → paste code",
                        ORANGE))
    els.append(sp(8))
    steps=[
        ("Open method source editor",
         "Methods tab → double-click WRITE_TO_PERSISTENCE\n"
         "Source code editor opens showing METHOD ... ENDMETHOD skeleton"),
        ("Replace the skeleton with the full code below",
         "Select all existing content → delete → paste the code exactly as shown"),
    ]
    for i,(a,d) in enumerate(steps,1):
        for row in step_row(i,a,d,ORANGE): els.append(row)
    els.append(sp(5))

    els.append(code([
        "METHOD write_to_persistence.",
        "",
        "  DATA: lt_lines     TYPE TABLE OF tline,",
        "        lv_tdname    TYPE tdname,",
        "        lv_counter   TYPE numc5,",
        "        ls_persist   TYPE zpo_longtext.",
        "",
        "  \" Build TDNAME — system-specific: NO space between EBELN and EBELP for EKPO",
        "  \" Confirmed from STXH: EKPO TDNAME = 450007774400010 (no space)",
        "  IF iv_tdobject = 'EKKO'.",
        "    lv_tdname = iv_ebeln.                    \" Header: TDNAME = PO number only",
        "  ELSE.",
        "    CONCATENATE iv_ebeln iv_ebelp INTO lv_tdname.  \" Item: no space",
        "  ENDIF.",
        "",
        "  \" Read and decompress text from STXH/STXL via SAP standard READ_TEXT",
        "  CALL FUNCTION 'READ_TEXT'",
        "    EXPORTING",
        "      id       = iv_tdid",
        "      language = iv_tdspras",
        "      name     = lv_tdname",
        "      object   = iv_tdobject",
        "    TABLES",
        "      lines    = lt_lines",
        "    EXCEPTIONS",
        "      OTHERS   = 4.",
        "",
        "  \" If no text found — exit cleanly, nothing to write",
        "  IF sy-subrc <> 0 OR lt_lines IS INITIAL.",
        "    RETURN.",
        "  ENDIF.",
        "",
        "  \" Full refresh: delete all existing rows for this exact text",
        "  \" This ensures deleted lines are removed (not just updated)",
        "  DELETE FROM zpo_longtext",
        "    WHERE ebeln    = iv_ebeln",
        "      AND ebelp    = iv_ebelp",
        "      AND tdobject = iv_tdobject",
        "      AND tdid     = iv_tdid",
        "      AND tdspras  = iv_tdspras.",
        "",
        "  \" Insert one flat row per plain text line",
        "  LOOP AT lt_lines INTO DATA(ls_line).",
        "    ADD 1 TO lv_counter.",
        "    CLEAR ls_persist.",
        "    ls_persist-ebeln        = iv_ebeln.",
        "    ls_persist-ebelp        = iv_ebelp.",
        "    ls_persist-tdobject     = iv_tdobject.",
        "    ls_persist-tdid         = iv_tdid.",
        "    ls_persist-tdspras      = iv_tdspras.",
        "    ls_persist-line_counter = lv_counter.",
        "    ls_persist-tdformat     = ls_line-tdformat.",
        "    ls_persist-tdline       = ls_line-tdline.   \" PLAIN TEXT — no compression",
        "    ls_persist-migrated_at  = sy-datum.",
        "    ls_persist-migrated_by  = sy-uname.",
        "    ls_persist-source       = 'D'.              \" D = Dual-write by BAdI",
        "    INSERT zpo_longtext FROM ls_persist.",
        "  ENDLOOP.",
        "",
        "ENDMETHOD.",
    ]))
    els.append(sp(6))
    steps2=[
        ("Save the method",
         "Ctrl+S → save after pasting — do NOT activate yet"),
    ]
    for i,(a,d) in enumerate(steps2,3):
        for row in step_row(i,a,d,ORANGE): els.append(row)
    els.append(PageBreak())
    return els

# ── Phase E: Implement READ ───────────────────────────────────────────────────
def phaseE():
    els=[]
    els.append(sec_hdr("E","Implement READ_FROM_PERSISTENCE — Full Code",
                        "Double-click method name → paste code → simple SELECT",
                        SAP_BLUE))
    els.append(sp(8))
    steps=[
        ("Open method source editor",
         "Methods tab → double-click READ_FROM_PERSISTENCE\n"
         "Source code editor opens"),
        ("Replace with code below",
         "Select all → delete → paste:"),
    ]
    for i,(a,d) in enumerate(steps,1):
        for row in step_row(i,a,d,SAP_BLUE): els.append(row)
    els.append(sp(5))

    els.append(code([
        "METHOD read_from_persistence.",
        "",
        "  \" Direct SQL on ZPO_LONGTEXT — no READ_TEXT needed",
        "  \" Plain text in TDLINE — no decompression",
        "  SELECT * FROM zpo_longtext",
        "    INTO TABLE @rt_lines",
        "    WHERE ebeln = @iv_ebeln",
        "    ORDER BY tdobject, tdid, tdspras, line_counter.",
        "",
        "ENDMETHOD.",
    ]))
    els.append(sp(6))
    steps2=[
        ("Save",
         "Ctrl+S"),
    ]
    for i,(a,d) in enumerate(steps2,3):
        for row in step_row(i,a,d,SAP_BLUE): els.append(row)
    els.append(PageBreak())
    return els

# ── Phase F: Activate ─────────────────────────────────────────────────────────
def phaseF():
    els=[]
    els.append(sec_hdr("F","Activate the Class and Verify",
                        "Ctrl+F3 — both methods must turn blue (Active)", SAP_DARK))
    els.append(sp(8))
    steps=[
        ("Activate the class",
         "Press Ctrl+F3 (Activate)\n"
         "OR Menu: Class → Activate\n"
         "If syntax errors appear → check code matches exactly and ZPO_LONGTEXT is Active in SE11"),
        ("Verify activation",
         "Status bar shows: Object ZCL_PO_LONGTEXT_HANDLER activated\n"
         "Methods tab: both method names turn BLUE = active\n"
         "Top of screen shows: Active (not Revised or New)"),
        ("Quick syntax test",
         "SE38 → new test program → add this code and run:\n"
         "  zcl_po_longtext_handler=>write_to_persistence(\n"
         "    iv_ebeln    = '4500077744'\n"
         "    iv_ebelp    = '00000'\n"
         "    iv_tdobject = 'EKKO'\n"
         "    iv_tdid     = 'F01'\n"
         "    iv_tdspras  = 'D' ).\n"
         "Then check SE16N → ZPO_LONGTEXT → filter EBELN=4500077744\n"
         "If rows appear → handler is working correctly ✓"),
    ]
    for i,(a,d) in enumerate(steps,1):
        for row in step_row(i,a,d,SAP_DARK): els.append(row)
    els.append(sp(8))
    els.append(ok(
        "✅  Step 2 complete when:\n"
        "  SE24 → ZCL_PO_LONGTEXT_HANDLER → Status = Active\n"
        "  Both methods show blue in Methods tab\n"
        "  SE16N → ZPO_LONGTEXT → rows appear after test call (2 rows for 2 text lines)"
    ))
    els.append(sp(8))
    els.append(Paragraph("Quick Reference — Both Methods", H2))
    els.append(tbl(
        ["Method","Called By","Input","What It Does","Output"],
        [
            ["WRITE_TO_PERSISTENCE",
             "BAdI (Step 3)\nMigration program",
             "EBELN, EBELP, TDOBJECT, TDID, TDSPRAS",
             "Calls READ_TEXT → decompresses STXL → DELETE old rows → INSERT plain rows",
             "Rows in ZPO_LONGTEXT with SOURCE=D"],
            ["READ_FROM_PERSISTENCE",
             "BDC programs\nReports\nCDS views",
             "EBELN only",
             "SELECT * FROM ZPO_LONGTEXT WHERE EBELN = ... ORDER BY LINE_COUNTER",
             "Table of ZPO_LONGTEXT rows — plain readable text"],
        ],
        widths=[4*cm,3.5*cm,4*cm,4.5*cm,1.5*cm]
    ))
    els.append(sp(8))
    els.append(note(
        "After Step 2 is complete — proceed to:\n"
        "Step 3: SE19 → Create ZCL_PO_TEXT_BADI_IMPL\n"
        "  BAdI ME_PROCESS_PO_CUST fires on every ME21N/ME22N save\n"
        "  Calls ZCL_PO_LONGTEXT_HANDLER=>WRITE_TO_PERSISTENCE automatically\n"
        "Full BAdI code is in: PO_LongText_4Steps_Guide.pdf → Step 3 section"
    ))
    return els

# ── Build ─────────────────────────────────────────────────────────────────────
def build():
    doc=SimpleDocTemplate(
        OUTPUT,pagesize=A4,
        leftMargin=2*cm,rightMargin=2*cm,
        topMargin=2*cm,bottomMargin=2*cm,
        title="ZCL_PO_LONGTEXT_HANDLER SE24 Guide",
        author="SAP PO Long Text Team",
    )
    story=[]
    story.extend(cover())
    story.extend(phaseA())
    story.extend(phaseB())
    story.extend(phaseC())
    story.extend(phaseD())
    story.extend(phaseE())
    story.extend(phaseF())

    def on_page(c,doc):
        c.saveState()
        c.setFont("Helvetica",7)
        c.setFillColor(colors.HexColor("#888888"))
        c.drawString(2*cm,1.2*cm,
            "ZCL_PO_LONGTEXT_HANDLER — SE24 Class Creation Guide | Step 2 of 4")
        c.drawRightString(19.5*cm,1.2*cm,f"Page {doc.page}")
        c.setStrokeColor(colors.HexColor("#CCCCCC"))
        c.setLineWidth(0.4)
        c.line(2*cm,1.5*cm,19.5*cm,1.5*cm)
        c.restoreState()

    doc.build(story,onFirstPage=on_page,onLaterPages=on_page)
    print(f"PDF created: {OUTPUT}")

build()
