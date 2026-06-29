from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

OUTPUT = r"C:\Users\I308878\PO_LongText_Persistencey\ZCL_PO_TEXT_BADI_IMPL_SE19_Guide_v2.pdf"

SAP_DARK  = colors.HexColor("#003366")
SAP_BLUE  = colors.HexColor("#0070F2")
SAP_LIGHT = colors.HexColor("#E8F4FD")
BTP_GREEN = colors.HexColor("#1A6632")
BTP_LT    = colors.HexColor("#E6F4EA")
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

def warn(t): return ibox(t,RED_LT,RED)
def ok(t):   return ibox(t,GREEN_LT,GREEN_OK)
def note(t): return ibox(t,GOLD_LT,GOLD)

def code(lines):
    rows=[[Paragraph(l.replace(" ","&nbsp;").replace("<","&lt;").replace(">","&gt;") or "&nbsp;",CODE_S)] for l in lines]
    t=Table(rows,colWidths=[17.5*cm])
    t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),CODE_BG),
                            ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
                            ("LEFTPADDING",(0,0),(-1,-1),8),("RIGHTPADDING",(0,0),(-1,-1),6)]))
    return t

def step_row(num, action, detail, color=SAP_BLUE):
    n_t=Table([[Paragraph(str(num),ms(f"sn{num}",fontSize=10,textColor=WHITE,
               fontName="Helvetica-Bold",alignment=TA_CENTER))]],colWidths=[0.8*cm])
    n_t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),color),
                              ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
                              ("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6)]))
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

# ══════════════════════════════════════════════════════════════════════════════
def cover():
    els=[]
    cov=Table([
        [Paragraph("Step 3 — Create ZCL_PO_TEXT_BADI_IMPL", TITLE)],
        [Paragraph("SE19 BAdI Implementation — Dual Write on Every PO Save", SUB)],
        [Paragraph("BAdI: ME_PROCESS_PO_CUST  |  Enhancement Spot: ME_PURCHORD  |  2026-06-28", META)],
    ],colWidths=[17.5*cm])
    cov.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),SAP_DARK),
                              ("TOPPADDING",(0,0),(-1,-1),24),("BOTTOMPADDING",(0,0),(-1,-1),24),
                              ("LEFTPADDING",(0,0),(-1,-1),20)]))
    els.append(cov)
    els.append(sp(12))

    els.append(Paragraph("What This BAdI Does", H2))
    els.append(Paragraph(
        "The BAdI ME_PROCESS_PO_CUST is a SAP hook that fires automatically "
        "AFTER a Purchase Order is saved in ME21N or ME22N — after SAP standard "
        "SAVE_TEXT has already written the text to STXH/STXL. At that point the "
        "text is readable via READ_TEXT. The BAdI calls ZCL_PO_LONGTEXT_HANDLER "
        "to write the same text as plain rows into ZPO_LONGTEXT automatically. "
        "No manual migration needed for new POs after this is active.", BODY))
    els.append(sp(6))

    # Flow diagram
    els.append(code([
        "User saves PO in ME21N / ME22N",
        "        │",
        "        ▼",
        "SAP Standard (always, unchanged)",
        "  SAVE_TEXT → STXH (text header) + STXL (compressed content)",
        "        │",
        "        ▼  ◄── BAdI fires HERE after SAVE_TEXT completes",
        "ZCL_PO_TEXT_BADI_IMPL (this implementation)",
        "  PROCESS_HEADER → calls handler for all EKKO texts",
        "  PROCESS_ITEM   → calls handler for all EKPO texts per item",
        "        │",
        "        ▼",
        "ZCL_PO_LONGTEXT_HANDLER=>WRITE_TO_PERSISTENCE",
        "  → Reads STXL via READ_TEXT (decompresses)",
        "  → Deletes old ZPO_LONGTEXT rows for this text",
        "  → Inserts fresh plain rows → SOURCE = D",
        "        │",
        "        ▼",
        "ZPO_LONGTEXT now has plain readable rows ✓",
        "SELECT * FROM ZPO_LONGTEXT WHERE EBELN = ... → no READ_TEXT needed",
    ]))
    els.append(sp(8))

    els.append(tbl(
        ["Step","Object","Transaction","Purpose"],
        [
            ["1","Create BAdI implementation","SE19","Register ZCL_PO_TEXT_BADI_IMPL for ME_PROCESS_PO_CUST"],
            ["2","Implement PROCESS_HEADER","SE24 via SE19","Writes all EKKO texts for the saved PO"],
            ["3","Implement PROCESS_ITEM","SE24 via SE19","Writes all EKPO texts for each saved item"],
            ["4","Activate","SE19 / SE24","BAdI goes live — fires on every ME21N/ME22N save"],
            ["5","Test","ME21N + SE16N","Create new PO → verify ZPO_LONGTEXT populated"],
        ],
        widths=[1.2*cm,5*cm,3.5*cm,7.8*cm]
    ))
    els.append(PageBreak())
    return els

# ── Phase A: Create BAdI ──────────────────────────────────────────────────────
def phaseA():
    els=[]
    els.append(sec_hdr("A","Open SE19 and Create the BAdI Implementation",
                        "Transaction SE19 — Business Add-In Builder", SAP_DARK))
    els.append(sp(8))
    steps=[
        ("Open SE19",
         "Transaction code: SE19 → press Enter"),
        ("Select Classic BAdI",
         "Screen shows two options: Classic BAdI and New BAdI.\n"
         "Select: Classic BAdI (radio button)\n"
         "Enter BAdI Name: ME_PROCESS_PO_CUST\n"
         "Click Create Implementation button"),
        ("Enter Implementation Name",
         "Implementation Name: ZCL_PO_TEXT_BADI_IMPL\n"
         "Click Continue (green tick or Enter)"),
        ("Fill Implementation Properties",
         "Short Text: PO Long Text Dual Write — ZPO_LONGTEXT\n"
         "The interface IF_EX_ME_PROCESS_PO_CUST is automatically assigned\n"
         "Click Save"),
        ("Assign package and transport",
         "Package: ZMM (or your development package)\n"
         "Transport: assign to your active workbench transport\n"
         "Save"),
    ]
    for i,(a,d) in enumerate(steps,1):
        for row in step_row(i,a,d,SAP_DARK): els.append(row)
    els.append(sp(6))
    els.append(note(
        "After creating the implementation, SE19 opens the class ZCL_PO_TEXT_BADI_IMPL "
        "in SE24 automatically. You will see the Methods tab with PROCESS_HEADER and "
        "PROCESS_ITEM already listed — these come from the interface IF_EX_ME_PROCESS_PO_CUST."
    ))
    els.append(PageBreak())
    return els

# ── Phase B: PROCESS_HEADER ───────────────────────────────────────────────────
def phaseB():
    els=[]
    els.append(sec_hdr("B","Implement PROCESS_HEADER Method",
                        "Fires when PO header is saved — writes all EKKO texts to ZPO_LONGTEXT",
                        SAP_BLUE))
    els.append(sp(8))
    steps=[
        ("Go to Methods tab",
         "In SE24 for ZCL_PO_TEXT_BADI_IMPL → click Methods tab"),
        ("Open PROCESS_HEADER source",
         "Double-click IF_EX_ME_PROCESS_PO_CUST~PROCESS_HEADER\n"
         "Source code editor opens showing the empty METHOD...ENDMETHOD skeleton"),
        ("Replace with full code below",
         "Select all existing content → Delete → Paste the code:"),
    ]
    for i,(a,d) in enumerate(steps,1):
        for row in step_row(i,a,d,SAP_BLUE): els.append(row)
    els.append(sp(5))
    els.append(warn(
        "⚠  TEST GUARD included — BAdI only fires for user SUNDARAMURTS during testing.\n"
        "   Remove the 4 marked guard lines before moving to production (see Phase G)."
    ))
    els.append(sp(4))
    els.append(code([
        "METHOD if_ex_me_process_po_cust~process_header.",
        "",
        "  \" ══ TEST GUARD — REMOVE BEFORE PRODUCTION ══════════════════",
        "  \" Only process POs saved by test user — protects other users",
        "  IF sy-uname <> 'SUNDARAMURTS'.",
        "    RETURN.",
        "  ENDIF.",
        "  \" ════════════════════════════════════════════════════════════",
        "",
        "  \" Get PO number from header object",
        "  DATA(lv_ebeln) = im_header->get_data( )-ebeln.",
        "",
        "  \" PO not yet committed — EBELN is initial — exit safely",
        "  IF lv_ebeln IS INITIAL.",
        "    RETURN.",
        "  ENDIF.",
        "",
        "  \" Read ALL header text entries for this PO from STXH dynamically",
        "  \" Handles F01 General Note, F02 Delivery Text, F03 etc.",
        "  \" No TDID hardcoding — future text types handled automatically",
        "  DATA lt_stxh   TYPE TABLE OF stxh.",
        "  DATA lv_tdname TYPE thead-tdname.",
        "  lv_tdname = lv_ebeln.",
        "",
        "  SELECT tdobject, tdid, tdspras, tdname",
        "    FROM stxh",
        "    INTO CORRESPONDING FIELDS OF TABLE @lt_stxh",
        "    WHERE tdobject = 'EKKO'",
        "      AND tdname   = @lv_tdname.",
        "",
        "  \" Write each TDID to ZPO_LONGTEXT — EBELP = 00000 for all header texts",
        "  LOOP AT lt_stxh INTO DATA(ls_stxh).",
        "    zcl_po_longtext_handler=>write_to_persistence(",
        "      iv_ebeln    = lv_ebeln",
        "      iv_ebelp    = '00000'",
        "      iv_tdobject = ls_stxh-tdobject",
        "      iv_tdid     = ls_stxh-tdid",
        "      iv_tdspras  = ls_stxh-tdspras ).",
        "  ENDLOOP.",
        "",
        "ENDMETHOD.",
    ]))
    els.append(sp(5))
    for row in step_row(4,"Save","Ctrl+S",SAP_BLUE): els.append(row)
    els.append(PageBreak())
    return els

# ── Phase C: PROCESS_ITEM ─────────────────────────────────────────────────────
def phaseC():
    els=[]
    els.append(sec_hdr("C","Implement PROCESS_ITEM Method",
                        "Fires per item when PO is saved — writes all EKPO texts to ZPO_LONGTEXT",
                        TEAL))
    els.append(sp(8))
    steps=[
        ("Open PROCESS_ITEM source",
         "Methods tab → double-click IF_EX_ME_PROCESS_PO_CUST~PROCESS_ITEM\n"
         "Source code editor opens"),
        ("Replace with full code below",
         "Select all → Delete → Paste:"),
    ]
    for i,(a,d) in enumerate(steps,1):
        for row in step_row(i,a,d,TEAL): els.append(row)
    els.append(sp(5))
    els.append(code([
        "METHOD if_ex_me_process_po_cust~process_item.",
        "",
        "  \" ══ TEST GUARD — REMOVE BEFORE PRODUCTION ══════════════════",
        "  \" Only process POs saved by test user — protects other users",
        "  IF sy-uname <> 'SUNDARAMURTS'.",
        "    RETURN.",
        "  ENDIF.",
        "  \" ════════════════════════════════════════════════════════════",
        "",
        "  \" Get PO number and item number",
        "  DATA(lv_ebeln) = im_item->get_data( )-ebeln.",
        "  DATA(lv_ebelp) = im_item->get_data( )-ebelp.",
        "",
        "  IF lv_ebeln IS INITIAL.",
        "    RETURN.",
        "  ENDIF.",
        "",
        "  \" Build TDNAME for this item — NO SPACE (confirmed for this system)",
        "  \" e.g. EBELN=4500077744 + EBELP=00010 → TDNAME=450007774400010",
        "  DATA lv_tdname TYPE thead-tdname.",
        "  CONCATENATE lv_ebeln lv_ebelp INTO lv_tdname.",
        "",
        "  \" Read ALL item text entries for this PO item from STXH dynamically",
        "  \" Picks up F01 Item Note, F02 Delivery Text, F09 GR Text etc.",
        "  DATA lt_stxh TYPE TABLE OF stxh.",
        "",
        "  SELECT tdobject, tdid, tdspras, tdname",
        "    FROM stxh",
        "    INTO CORRESPONDING FIELDS OF TABLE @lt_stxh",
        "    WHERE tdobject = 'EKPO'",
        "      AND tdname   = @lv_tdname.",
        "",
        "  \" Write each TDID to ZPO_LONGTEXT — EBELP = actual item number",
        "  LOOP AT lt_stxh INTO DATA(ls_stxh).",
        "    zcl_po_longtext_handler=>write_to_persistence(",
        "      iv_ebeln    = lv_ebeln",
        "      iv_ebelp    = lv_ebelp",
        "      iv_tdobject = ls_stxh-tdobject",
        "      iv_tdid     = ls_stxh-tdid",
        "      iv_tdspras  = ls_stxh-tdspras ).",
        "  ENDLOOP.",
        "",
        "ENDMETHOD.",
    ]))
    els.append(sp(5))
    for row in step_row(3,"Save","Ctrl+S",TEAL): els.append(row)
    els.append(sp(4))
    els.append(note(
        "Why both methods read STXH dynamically:\n"
        "  Each PO/item may have different text types (F01, F02, F09 etc.).\n"
        "  Reading from STXH at runtime ensures ALL text types are migrated.\n"
        "  No TDID hardcoding — adding a new text type in future requires no code change."
    ))
    els.append(PageBreak())
    return els

# ── Phase D: Activate ─────────────────────────────────────────────────────────
def phaseD():
    els=[]
    els.append(sec_hdr("D","Activate the Class and BAdI Implementation",
                        "Ctrl+F3 in SE24 → then verify in SE19", SAP_DARK))
    els.append(sp(8))
    steps=[
        ("Activate the class in SE24",
         "Press Ctrl+F3 (Activate)\n"
         "Status bar must show: Object ZCL_PO_TEXT_BADI_IMPL activated\n"
         "Both method names turn BLUE in Methods tab"),
        ("Verify in SE19",
         "Go back to SE19 → Classic BAdI → Implementation → ZCL_PO_TEXT_BADI_IMPL\n"
         "Status must show: Active (green indicator)\n"
         "If grey/inactive → click Activate button in SE19 toolbar"),
        ("Confirm BAdI is registered",
         "SE19 → Classic BAdI → BAdI Definition → ME_PROCESS_PO_CUST\n"
         "Click 'Display' → Implementation tab\n"
         "ZCL_PO_TEXT_BADI_IMPL must appear in the list with Active status"),
    ]
    for i,(a,d) in enumerate(steps,1):
        for row in step_row(i,a,d,SAP_DARK): els.append(row)
    els.append(sp(6))
    els.append(ok(
        "✅  BAdI is active when:\n"
        "  SE19 → ZCL_PO_TEXT_BADI_IMPL → Status = Active\n"
        "  SE24 → ZCL_PO_TEXT_BADI_IMPL → both methods are blue (active)\n"
        "  ME_PROCESS_PO_CUST implementation list shows ZCL_PO_TEXT_BADI_IMPL"
    ))
    els.append(PageBreak())
    return els

# ── Phase E: Test ─────────────────────────────────────────────────────────────
def phaseE():
    els=[]
    els.append(sec_hdr("E","Test the BAdI — Create New PO and Verify",
                        "ME21N → save with text → SE16N → ZPO_LONGTEXT must have rows",
                        BTP_GREEN))
    els.append(sp(8))
    steps=[
        ("Create a new PO in ME21N",
         "Transaction: ME21N → Enter\n"
         "Fill: Vendor, Purchase Org 0001, Company Code 0001, Document Type NB"),
        ("Add Header text",
         "Header → Texts → Text Overview\n"
         "Type in first field next to Header text:\n"
         "  Line 1: BAdI test header note line 1\n"
         "  Line 2: BAdI test header note line 2\n"
         "Press F3 to return"),
        ("Add line item",
         "Items section: add Material, Quantity 1, Delivery Date, Plant 0001"),
        ("Add Item text",
         "Select Item 10 → Item → Texts → Text Overview\n"
         "Type in first field next to Item text:\n"
         "  Line 1: BAdI test item note line 1\n"
         "Press F3 to return"),
        ("Save the PO",
         "Ctrl+S → wait for status bar message:\n"
         "  Standard PO xxxxxxxxxx saved\n"
         "Note the new PO number"),
        ("Verify STXH",
         "SE16 → STXH → Text object: EKKO, Text Name: <new PO#>, Language: D\n"
         "Expect: 1 row confirming header text was saved by SAP standard"),
        ("Verify ZPO_LONGTEXT",
         "SE16N → ZPO_LONGTEXT → EBELN: <new PO#> → Execute\n"
         "Expect rows:\n"
         "  EKKO / F01 / 00000 / LINE_COUNTER 00001 / TDLINE: BAdI test header note line 1 / SOURCE: D\n"
         "  EKKO / F01 / 00000 / LINE_COUNTER 00002 / TDLINE: BAdI test header note line 2 / SOURCE: D\n"
         "  EKPO / F01 / 00010 / LINE_COUNTER 00001 / TDLINE: BAdI test item note line 1   / SOURCE: D"),
    ]
    for i,(a,d) in enumerate(steps,1):
        for row in step_row(i,a,d,BTP_GREEN): els.append(row)
    els.append(sp(6))
    els.append(ok(
        "✅  BAdI is working correctly when:\n"
        "  ZPO_LONGTEXT rows appear for the NEW PO immediately after save\n"
        "  SOURCE = D (Dual-write by BAdI — not M for migration)\n"
        "  All text types (header + items) are present\n"
        "  No manual migration program run needed"
    ))
    els.append(PageBreak())
    return els

# ── Phase F: Troubleshooting ──────────────────────────────────────────────────
def phaseF():
    els=[]
    els.append(sec_hdr("F","Troubleshooting — If ZPO_LONGTEXT Has No Rows After Save",
                        "Debug checklist — check in this order", RED))
    els.append(sp(8))
    els.append(tbl(
        ["#","Check","How","Fix"],
        [
            ["1","BAdI is Active",
             "SE19 → ZCL_PO_TEXT_BADI_IMPL → Status",
             "Must be Active (green). If grey → activate in SE19."],
            ["2","Class is Active",
             "SE24 → ZCL_PO_TEXT_BADI_IMPL → status bar",
             "Methods must be blue. If inactive → Ctrl+F3."],
            ["3","PO was saved (not held)",
             "Status bar after save shows 'saved' not 'held'",
             "Edit → Release Hold → Ctrl+S again."],
            ["4","Text exists in STXH",
             "SE16 → STXH → Text object=EKKO, Text Name=<PO#>",
             "If no STXH row → text was not saved. Re-enter text in ME22N."],
            ["5","ZPO_LONGTEXT table exists",
             "SE11 → ZPO_LONGTEXT → Display → Active",
             "Must be Active. If not → complete Step 1 guide."],
            ["6","Handler class is Active",
             "SE24 → ZCL_PO_LONGTEXT_HANDLER → methods blue",
             "Must be Active. If not → Ctrl+F3 in SE24."],
            ["7","TDNAME no-space confirmed",
             "SE16 → STXH → check EKPO TDNAME column",
             "Must be 450007774400010 format (no space). Handler uses CONCATENATE without space."],
        ],
        widths=[0.7*cm,4*cm,5.5*cm,7.3*cm]
    ))
    els.append(sp(8))

    els.append(Paragraph("How to Add a Breakpoint for Debugging", H2))
    els.append(ibox(
        "If BAdI is active but ZPO_LONGTEXT still has no rows:\n"
        "  SE24 → ZCL_PO_TEXT_BADI_IMPL → PROCESS_HEADER method\n"
        "  Set a breakpoint on the first line (click left margin — red dot appears)\n"
        "  Run ME21N → save PO → debugger opens at breakpoint\n"
        "  Check: lv_ebeln has a value (not initial)\n"
        "  Check: lt_stxh is populated after the SELECT\n"
        "  Step through LOOP → check ZCL_PO_LONGTEXT_HANDLER call\n"
        "  If lt_stxh is empty → text not in STXH yet at this point (timing issue)"
    ))
    els.append(sp(8))

    # Final summary
    els.append(Paragraph("All 4 Steps — Complete Summary", H2))
    els.append(tbl(
        ["Step","Object","Status","Result"],
        [
            ["Step 1","ZPO_LONGTEXT (SE11)",
             "✅ Complete","Custom table — stores plain text lines. Active in SE11."],
            ["Step 2","ZCL_PO_LONGTEXT_HANDLER (SE24)",
             "✅ Complete","Handler class — READ_TEXT → writes to ZPO_LONGTEXT. Active."],
            ["Step 3","ZCL_PO_TEXT_BADI_IMPL (SE19)",
             "→ This guide","BAdI — fires on ME21N/ME22N save → calls handler automatically."],
            ["Step 4","Test ME21N + SE16N",
             "After Step 3","New PO with text → ZPO_LONGTEXT populated with SOURCE=D."],
        ],
        widths=[2*cm,6*cm,3.5*cm,6*cm]
    ))
    els.append(sp(6))
    els.append(note(
        "After all 4 steps are complete:\n"
        "  ✓ Historic POs: run ZTEST_PO_LONGTEXT_MIGRATE to populate ZPO_LONGTEXT\n"
        "  ✓ New POs: BAdI automatically writes to ZPO_LONGTEXT on every save\n"
        "  ✓ Reports / BDC: SELECT * FROM ZPO_LONGTEXT WHERE EBELN = ... — no READ_TEXT needed"
    ))
    return els

def phaseG():
    els=[]
    els.append(sec_hdr("G","Production Go-Live — Remove the Test Guard",
                        "Delete 4 lines from both methods before transport to production",
                        RED, RED))
    els.append(sp(8))
    els.append(warn(
        "⚠  The test guard IF sy-uname <> 'SUNDARAMURTS' MUST be removed before production.\n"
        "   With the guard in place: only POs saved by SUNDARAMURTS will be written to ZPO_LONGTEXT.\n"
        "   All other users' POs will be silently skipped — ZPO_LONGTEXT will be incomplete."
    ))
    els.append(sp(6))

    els.append(Paragraph("Lines to Remove from PROCESS_HEADER and PROCESS_ITEM", H2))
    els.append(code([
        "  \" ══ TEST GUARD — REMOVE BEFORE PRODUCTION ══════════════════",
        "  \" Only process POs saved by test user — protects other users",
        "  IF sy-uname <> 'SUNDARAMURTS'.",
        "    RETURN.",
        "  ENDIF.",
        "  \" ════════════════════════════════════════════════════════════",
    ]))
    els.append(sp(6))

    steps=[
        ("Open PROCESS_HEADER in SE24",
         "SE24 → ZCL_PO_TEXT_BADI_IMPL → Methods tab\n"
         "Double-click IF_EX_ME_PROCESS_PO_CUST~PROCESS_HEADER"),
        ("Delete the 6 guard lines",
         "Select the 6 lines shown above (from \" ══ TEST GUARD to \" ════════)\n"
         "Delete them completely — leave no blank lines in their place"),
        ("Production PROCESS_HEADER should start like this",
         "METHOD if_ex_me_process_po_cust~process_header.\n"
         "  DATA(lv_ebeln) = im_header->get_data( )-ebeln.\n"
         "  IF lv_ebeln IS INITIAL.\n"
         "    RETURN.\n"
         "  ENDIF.\n"
         "  ... (rest of method unchanged)"),
        ("Repeat for PROCESS_ITEM",
         "Double-click IF_EX_ME_PROCESS_PO_CUST~PROCESS_ITEM\n"
         "Delete the same 6 guard lines\n"
         "Save"),
        ("Activate",
         "Ctrl+F3 → Activate\n"
         "BAdI now processes ALL users — every PO save writes to ZPO_LONGTEXT"),
        ("Test with another user",
         "Ask a colleague to create a PO with text\n"
         "SE16N → ZPO_LONGTEXT → filter EBELN = their PO number\n"
         "Rows must appear → confirms guard is removed correctly"),
    ]
    for i,(a,d) in enumerate(steps,1):
        for row in step_row(i,a,d,RED): els.append(row)

    els.append(sp(8))
    els.append(Paragraph("Production Code — PROCESS_HEADER (No Guard)", H2))
    els.append(code([
        "METHOD if_ex_me_process_po_cust~process_header.",
        "",
        "  DATA(lv_ebeln) = im_header->get_data( )-ebeln.",
        "  IF lv_ebeln IS INITIAL.",
        "    RETURN.",
        "  ENDIF.",
        "",
        "  DATA lt_stxh   TYPE TABLE OF stxh.",
        "  DATA lv_tdname TYPE thead-tdname.",
        "  lv_tdname = lv_ebeln.",
        "",
        "  SELECT tdobject, tdid, tdspras, tdname",
        "    FROM stxh",
        "    INTO CORRESPONDING FIELDS OF TABLE @lt_stxh",
        "    WHERE tdobject = 'EKKO'",
        "      AND tdname   = @lv_tdname.",
        "",
        "  LOOP AT lt_stxh INTO DATA(ls_stxh).",
        "    zcl_po_longtext_handler=>write_to_persistence(",
        "      iv_ebeln    = lv_ebeln",
        "      iv_ebelp    = '00000'",
        "      iv_tdobject = ls_stxh-tdobject",
        "      iv_tdid     = ls_stxh-tdid",
        "      iv_tdspras  = ls_stxh-tdspras ).",
        "  ENDLOOP.",
        "",
        "ENDMETHOD.",
    ]))
    els.append(sp(6))

    els.append(Paragraph("Production Code — PROCESS_ITEM (No Guard)", H2))
    els.append(code([
        "METHOD if_ex_me_process_po_cust~process_item.",
        "",
        "  DATA(lv_ebeln) = im_item->get_data( )-ebeln.",
        "  DATA(lv_ebelp) = im_item->get_data( )-ebelp.",
        "  IF lv_ebeln IS INITIAL.",
        "    RETURN.",
        "  ENDIF.",
        "",
        "  DATA lv_tdname TYPE thead-tdname.",
        "  CONCATENATE lv_ebeln lv_ebelp INTO lv_tdname.",
        "",
        "  DATA lt_stxh TYPE TABLE OF stxh.",
        "",
        "  SELECT tdobject, tdid, tdspras, tdname",
        "    FROM stxh",
        "    INTO CORRESPONDING FIELDS OF TABLE @lt_stxh",
        "    WHERE tdobject = 'EKPO'",
        "      AND tdname   = @lv_tdname.",
        "",
        "  LOOP AT lt_stxh INTO DATA(ls_stxh).",
        "    zcl_po_longtext_handler=>write_to_persistence(",
        "      iv_ebeln    = lv_ebeln",
        "      iv_ebelp    = lv_ebelp",
        "      iv_tdobject = ls_stxh-tdobject",
        "      iv_tdid     = ls_stxh-tdid",
        "      iv_tdspras  = ls_stxh-tdspras ).",
        "  ENDLOOP.",
        "",
        "ENDMETHOD.",
    ]))
    els.append(sp(6))
    els.append(ok(
        "✅  Production ready when:\n"
        "  Guard lines removed from both methods\n"
        "  Class activated\n"
        "  Tested with another user's PO — ZPO_LONGTEXT rows appear with SOURCE=D"
    ))
    return els

# ── Build ─────────────────────────────────────────────────────────────────────
def build():
    doc=SimpleDocTemplate(
        OUTPUT,pagesize=A4,
        leftMargin=2*cm,rightMargin=2*cm,
        topMargin=2*cm,bottomMargin=2*cm,
        title="ZCL_PO_TEXT_BADI_IMPL SE19 Creation Guide",
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
    story.extend(phaseG())

    def on_page(c,doc):
        c.saveState()
        c.setFont("Helvetica",7)
        c.setFillColor(colors.HexColor("#888888"))
        c.drawString(2*cm,1.2*cm,
            "ZCL_PO_TEXT_BADI_IMPL — SE19 BAdI Implementation Guide | Step 3 of 4")
        c.drawRightString(19.5*cm,1.2*cm,f"Page {doc.page}")
        c.setStrokeColor(colors.HexColor("#CCCCCC"))
        c.setLineWidth(0.4)
        c.line(2*cm,1.5*cm,19.5*cm,1.5*cm)
        c.restoreState()

    doc.build(story,onFirstPage=on_page,onLaterPages=on_page)
    print(f"PDF created: {OUTPUT}")

build()
