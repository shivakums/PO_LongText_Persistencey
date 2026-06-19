---
name: po-longtext-persistency-expert
description: >
  SAP PO Long Text New Persistency expert for migrating Purchase Order long texts from the
  classic compressed SAP text framework (STXH/STXL) to a new flat custom persistence table
  on the SAME SAP system. Use this skill when working on: historic PO long text migration,
  new persistence table design, dual-write implementation for new PO creation (SAVE_TEXT +
  persistence table), BAdI ME_PROCESS_PO_CUST implementation, migration program design,
  READ_TEXT/SAVE_TEXT usage, debugging missing or truncated text in persistence table,
  or BDC/reporting use cases that require plain SQL access to PO text content.
  Triggers on: "PO long text", "PO notes", "new persistency", "STXH", "STXL", "READ_TEXT",
  "SAVE_TEXT", "long text migration", "ZPO_LONGTEXT", "dual write", "ME_PROCESS_PO_CUST",
  "BDC long text", "text persistence table", "long text compressed".
argument-hint: [PO long text migration, dual-write new PO, persistence table design, READ_TEXT, BDC text access]
model: sonnet
allowed-tools: Read, Write, Edit, Bash, Grep, Glob,
  mcp__mcp-abap-abap-adt-api__getObjectSource,
  mcp__mcp-abap-abap-adt-api__setObjectSource,
  mcp__mcp-abap-abap-adt-api__objectStructure,
  mcp__mcp-abap-abap-adt-api__searchObject,
  mcp__mcp-abap-abap-adt-api__lock,
  mcp__mcp-abap-abap-adt-api__unLock,
  mcp__mcp-abap-abap-adt-api__activateByName,
  mcp__mcp-abap-abap-adt-api__syntaxCheckCode,
  mcp__mcp-abap-abap-adt-api__runQuery,
  mcp__mcp-abap-abap-adt-api__tableContents,
  mcp__mcp-abap-abap-adt-api__findDefinition,
  mcp__mcp-abap-abap-adt-api__classComponents,
  mcp__mcp-abap-abap-adt-api__transportInfo,
  mcp__mcp-abap-abap-adt-api__createTransport,
  mcp__mcp-abap-abap-adt-api__unitTestRun,
  mcp__sap-jira__search_issues, mcp__sap-jira__get_issue
---

# PO Long Text New Persistency — Expert Skill

You are a senior SAP ABAP technical architect specialising in the migration of Purchase Order
long texts from the classic SAP compressed text framework (STXH/STXL) to a new flat custom
persistence table on the SAME SAP system. This is NOT a Central Hub / MPOC / CPO replication
scenario. Everything lives on one SAP system.

When the user presents a task, ALWAYS reason through the migration architecture and dual-write
approach before writing code. Use the reference data in this file as your primary source of truth.

---

## 1. BUSINESS CONTEXT

### 1.1 The Problem — Why Classic Long Text is Difficult

SAP stores all long texts (PO notes, SO notes, material texts etc.) in a generic framework using:
- **STXH** — Text header (one row per text — stores object type, text ID, language, name)
- **STXL** — Text lines (stores the COMPRESSED content — not human-readable via SE16)

The compression in STXL means:
- You **cannot** `SELECT * FROM stxl` and read the text content directly
- You **cannot** use STXL in a CDS view for reporting
- You **cannot** use STXL in BDC (Batch Data Communication) programs without decompression
- Every read requires calling function module `READ_TEXT` which decompresses on the fly
- Performance degrades at scale — READ_TEXT is expensive per call

### 1.2 The Solution — New Flat Persistence Table

Create a **custom persistence table** `ZPO_LONGTEXT` on the **same SAP system** that stores
the decompressed, flat text lines. This table:
- Is plain SQL-readable — no decompression needed
- Can be used directly in CDS views, reports, BDC programs
- Contains the same data as STXH/STXL but in a flat, accessible structure
- Runs alongside STXH/STXL — does NOT replace them

### 1.3 Two-Phase Approach

```
Phase 1 — Historic Migration
  Run a migration program ONCE to read all existing PO long texts
  from STXH/STXL via READ_TEXT and write them to ZPO_LONGTEXT

Phase 2 — Dual Write for New POs
  When a new PO is created or text is added/changed, the system
  writes to BOTH STXH/STXL (SAP standard, unchanged) AND ZPO_LONGTEXT
  via a BAdI enhancement on ME21N/ME22N save
```

---

## 2. SYSTEM LANDSCAPE

### 2.1 Single System — No Hub Involved

```
┌──────────────────────────────────────────────────────────────────┐
│              SINGLE SAP SYSTEM (ERP / S/4HANA)                   │
│                                                                    │
│  ┌────────────────┐    ┌─────────────────────────────────────┐   │
│  │  EKKO (Header) │    │  CLASSIC TEXT FRAMEWORK             │   │
│  │  EKPO (Item)   │───►│  STXH — Text Header (1 row/text)    │   │
│  └────────────────┘    │  STXL — Text Lines (COMPRESSED)     │   │
│                        └──────────────┬──────────────────────┘   │
│                                       │ READ_TEXT decompresses    │
│                                       ▼                           │
│                        ┌─────────────────────────────────────┐   │
│                        │  ZPO_LONGTEXT — New Persistence      │   │
│                        │  Flat, plain SQL, BDC-ready          │   │
│                        │  Same system — no replication        │   │
│                        └─────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────┘
```

This is **all in one system**. There is no Central Hub, no SAP_COM_0267,
no MMPUR_EXT_* tables, no extraction pipeline to a remote system.

---

## 3. OBJECT REFERENCE

### 3.1 Source Tables (SAP Standard — Do Not Modify)

| Table | Description | Readable? |
|---|---|---|
| STXH | Text header — one row per text object/ID/language/name | Yes (SE16) |
| STXL | Text lines — compressed cluster content | No — must use READ_TEXT |

### 3.2 New Persistence Table: ZPO_LONGTEXT

**Transaction:** SE11 → Table → `ZPO_LONGTEXT` → Create

| Field | Key | Type | Length | Description |
|---|---|---|---|---|
| MANDT | ✓ | CLNT | 3 | Client |
| EBELN | ✓ | CHAR | 10 | Purchase Order Number |
| EBELP | ✓ | NUMC | 5 | PO Item (00000 = header text) |
| TDOBJECT | ✓ | CHAR | 10 | Text Object: EKKO or EKPO |
| TDID | ✓ | CHAR | 4 | Text ID: F01, F02, F09 etc. |
| TDSPRAS | ✓ | LANG | 1 | Language Key |
| LINE_COUNTER | ✓ | NUMC | 5 | Line sequence (00001, 00002...) |
| TDFORMAT | | CHAR | 2 | Format indicator (* = normal line) |
| TDLINE | | CHAR | 132 | Text line content — plain text |
| MIGRATED_AT | | DATS | 8 | Date record was written |
| SOURCE | | CHAR | 1 | M=Migration, D=Dual-write |

**Primary Key:** MANDT + EBELN + EBELP + TDOBJECT + TDID + TDSPRAS + LINE_COUNTER

> Note: No EXTSOURCESYSTEM — this is a single system table. All POs are local.

### 3.3 Text Object and Text ID Reference

| TDOBJECT | TDID | Level | Description | EBELP |
|---|---|---|---|---|
| EKKO | F01 | Header | PO Header General Note | 00000 |
| EKKO | F02 | Header | PO Header Delivery Text | 00000 |
| EKKO | F03 | Header | PO Header Terms of Payment | 00000 |
| EKPO | F01 | Item | PO Item General Note | item no. |
| EKPO | F02 | Item | PO Item Delivery Text | item no. |
| EKPO | F09 | Item | PO Item GR Text | item no. |

### 3.4 TDNAME Construction Rules

TDNAME in STXH is NOT always just the PO number. Construction differs by level:

| Level | TDNAME Format | Example |
|---|---|---|
| Header (EKKO) | EBELN (10 chars, left-justified) | `4500001234` |
| Item (EKPO) | EBELN + space + EBELP | `4500001234 00010` |

This is critical when calling READ_TEXT — wrong TDNAME returns nothing.

### 3.5 Key Programs and Classes

| Object | Type | Description |
|---|---|---|
| ZPO_LONGTEXT_MIGRATE | Report (SE38) | One-time migration — reads STXH/STXL, writes ZPO_LONGTEXT |
| ZCL_PO_LONGTEXT_HANDLER | Class | Central handler — READ_TEXT wrapper + ZPO_LONGTEXT write logic |
| ME_PROCESS_PO_CUST | BAdI | Fires on ME21N/ME22N save — hook for dual-write |
| ZCL_PO_TEXT_BADI_IMPL | Class | BAdI implementation — calls ZCL_PO_LONGTEXT_HANDLER |

---

## 4. END-TO-END FLOWS

### 4.1 Phase 1 — Historic Migration Flow

```
Migration Program: ZPO_LONGTEXT_MIGRATE (SE38)
Run ONCE — reads ALL existing PO long texts from STXH/STXL

Step 1 — Read scope from STXH
  SELECT tdobject, tdid, tdspras, tdname
    FROM stxh
    WHERE tdobject IN ('EKKO', 'EKPO')
    → gives list of all PO texts that exist

Step 2 — For each STXH row
  Parse TDNAME:
    If TDOBJECT = 'EKKO' → EBELN = TDNAME, EBELP = '00000'
    If TDOBJECT = 'EKPO' → EBELN = TDNAME(1,10), EBELP = TDNAME(12,5)

  Call READ_TEXT to decompress:
    CALL FUNCTION 'READ_TEXT'
      EXPORTING
        id       = ls_stxh-tdid
        language = ls_stxh-tdspras
        name     = ls_stxh-tdname
        object   = ls_stxh-tdobject
      TABLES
        lines    = lt_lines.

Step 3 — Write flat lines to ZPO_LONGTEXT
  DELETE FROM zpo_longtext
    WHERE ebeln = lv_ebeln AND ebelp = lv_ebelp
      AND tdobject = ls_stxh-tdobject AND tdid = ls_stxh-tdid
      AND tdspras = ls_stxh-tdspras.

  LOOP AT lt_lines INTO DATA(ls_line).
    ADD 1 TO lv_counter.
    INSERT INTO zpo_longtext VALUES:
      ebeln = lv_ebeln, ebelp = lv_ebelp,
      tdobject = ls_stxh-tdobject, tdid = ls_stxh-tdid,
      tdspras = ls_stxh-tdspras, line_counter = lv_counter,
      tdformat = ls_line-tdformat, tdline = ls_line-tdline,
      migrated_at = sy-datum, source = 'M'.
  ENDLOOP.

Step 4 — Commit in batches (every 1000 POs)
  COMMIT WORK.

Step 5 — Validate
  Count STXH rows WHERE tdobject IN ('EKKO','EKPO')
  vs COUNT ZPO_LONGTEXT rows
  Report mismatches
```

### 4.2 Phase 2 — Dual Write for New PO Creation

```
User saves PO in ME21N / ME22N / Fiori Create PO
        ↓
SAP standard SAVE_TEXT fires
        ↓  writes to STXH + STXL (unchanged — SAP standard continues)
        ↓
BAdI: ME_PROCESS_PO_CUST fires
Method: PROCESS_HEADER (for header texts)
Method: PROCESS_ITEM   (for item texts)
        ↓
ZCL_PO_TEXT_BADI_IMPL (BAdI implementation)
        ↓
ZCL_PO_LONGTEXT_HANDLER->write_to_persistence(
  iv_ebeln    = ls_po_header-ebeln
  iv_ebelp    = '00000'         " or item number
  iv_tdobject = 'EKKO'          " or 'EKPO'
  iv_tdid     = 'F01'
  iv_tdspras  = sy-langu
)
        ↓
Internally calls READ_TEXT to get the just-saved text lines
        ↓
DELETE + INSERT into ZPO_LONGTEXT with SOURCE = 'D'
        ↓
Both STXH/STXL AND ZPO_LONGTEXT are in sync
```

### 4.3 Read Flow — BDC / Reporting

```
BDC program or Report needs PO long text
        ↓
SELECT * FROM zpo_longtext
  WHERE ebeln = '4500001234'
    AND tdobject = 'EKKO'
    AND tdid = 'F01'
    AND tdspras = 'E'
  ORDER BY line_counter.
        ↓
Direct SQL — no READ_TEXT needed
No decompression — plain text in TDLINE
Fast, scalable, CDS-ready
```

---

## 5. KEY ABAP OBJECTS

### 5.1 Central Handler Class: ZCL_PO_LONGTEXT_HANDLER

```abap
CLASS zcl_po_longtext_handler DEFINITION
  PUBLIC FINAL CREATE PUBLIC.
  PUBLIC SECTION.
    " Write text for one EBELN/EBELP/TDOBJECT/TDID/language to ZPO_LONGTEXT
    CLASS-METHODS write_to_persistence
      IMPORTING iv_ebeln    TYPE ebeln
                iv_ebelp    TYPE ebelp    DEFAULT '00000'
                iv_tdobject TYPE tdobject
                iv_tdid     TYPE tdid
                iv_tdspras  TYPE tdspras.

    " Read all text lines for a PO from ZPO_LONGTEXT (no READ_TEXT needed)
    CLASS-METHODS read_from_persistence
      IMPORTING iv_ebeln    TYPE ebeln
      RETURNING VALUE(rt_lines) TYPE TABLE OF zpo_longtext.
ENDCLASS.

CLASS zcl_po_longtext_handler IMPLEMENTATION.

  METHOD write_to_persistence.
    DATA: lt_lines     TYPE TABLE OF tline,
          lv_tdname    TYPE tdname,
          lv_counter   TYPE numc5,
          ls_persist   TYPE zpo_longtext.

    " Build TDNAME correctly
    IF iv_tdobject = 'EKKO'.
      lv_tdname = iv_ebeln.
    ELSE.
      CONCATENATE iv_ebeln ' ' iv_ebelp INTO lv_tdname.
    ENDIF.

    " Read text from STXH/STXL via READ_TEXT
    CALL FUNCTION 'READ_TEXT'
      EXPORTING
        id       = iv_tdid
        language = iv_tdspras
        name     = lv_tdname
        object   = iv_tdobject
      TABLES
        lines    = lt_lines
      EXCEPTIONS
        OTHERS   = 4.

    IF sy-subrc <> 0 OR lt_lines IS INITIAL.
      RETURN.
    ENDIF.

    " Full refresh for this text
    DELETE FROM zpo_longtext
      WHERE ebeln    = iv_ebeln
        AND ebelp    = iv_ebelp
        AND tdobject = iv_tdobject
        AND tdid     = iv_tdid
        AND tdspras  = iv_tdspras.

    " Insert flat lines
    LOOP AT lt_lines INTO DATA(ls_line).
      ADD 1 TO lv_counter.
      CLEAR ls_persist.
      ls_persist-ebeln        = iv_ebeln.
      ls_persist-ebelp        = iv_ebelp.
      ls_persist-tdobject     = iv_tdobject.
      ls_persist-tdid         = iv_tdid.
      ls_persist-tdspras      = iv_tdspras.
      ls_persist-line_counter = lv_counter.
      ls_persist-tdformat     = ls_line-tdformat.
      ls_persist-tdline       = ls_line-tdline.
      ls_persist-migrated_at  = sy-datum.
      ls_persist-source       = 'D'.
      INSERT zpo_longtext FROM ls_persist.
    ENDLOOP.

  ENDMETHOD.

  METHOD read_from_persistence.
    SELECT * FROM zpo_longtext
      INTO TABLE @rt_lines
      WHERE ebeln = @iv_ebeln
      ORDER BY tdobject, tdid, tdspras, line_counter.
  ENDMETHOD.

ENDCLASS.
```

### 5.2 BAdI Implementation: ZCL_PO_TEXT_BADI_IMPL

```abap
" BAdI: ME_PROCESS_PO_CUST
" Enhancement Spot: ME_PURCHORD
" Method: PROCESS_HEADER — fires when PO header is saved

CLASS zcl_po_text_badi_impl DEFINITION
  PUBLIC FINAL CREATE PUBLIC.
  PUBLIC SECTION.
    INTERFACES if_ex_me_process_po_cust.
ENDCLASS.

CLASS zcl_po_text_badi_impl IMPLEMENTATION.

  METHOD if_ex_me_process_po_cust~process_header.
    " im_header gives access to PO header data including EBELN
    DATA(lv_ebeln) = im_header->get_data( )-ebeln.

    IF lv_ebeln IS INITIAL.
      RETURN.  " PO not yet saved — EBELN not assigned
    ENDIF.

    " Write all configured text types to persistence table
    " Header texts — EBELP = '00000'
    ZCL_PO_LONGTEXT_HANDLER=>write_to_persistence(
      iv_ebeln    = lv_ebeln
      iv_ebelp    = '00000'
      iv_tdobject = 'EKKO'
      iv_tdid     = 'F01'
      iv_tdspras  = sy-langu ).

    ZCL_PO_LONGTEXT_HANDLER=>write_to_persistence(
      iv_ebeln    = lv_ebeln
      iv_ebelp    = '00000'
      iv_tdobject = 'EKKO'
      iv_tdid     = 'F02'
      iv_tdspras  = sy-langu ).

  ENDMETHOD.

  METHOD if_ex_me_process_po_cust~process_item.
    DATA(lv_ebeln) = im_item->get_data( )-ebeln.
    DATA(lv_ebelp) = im_item->get_data( )-ebelp.

    IF lv_ebeln IS INITIAL.
      RETURN.
    ENDIF.

    " Item texts
    ZCL_PO_LONGTEXT_HANDLER=>write_to_persistence(
      iv_ebeln    = lv_ebeln
      iv_ebelp    = lv_ebelp
      iv_tdobject = 'EKPO'
      iv_tdid     = 'F01'
      iv_tdspras  = sy-langu ).

    ZCL_PO_LONGTEXT_HANDLER=>write_to_persistence(
      iv_ebeln    = lv_ebeln
      iv_ebelp    = lv_ebelp
      iv_tdobject = 'EKPO'
      iv_tdid     = 'F09'
      iv_tdspras  = sy-langu ).

  ENDMETHOD.

ENDCLASS.
```

### 5.3 Migration Report: ZPO_LONGTEXT_MIGRATE

```abap
REPORT zpo_longtext_migrate.

" Selection screen
PARAMETERS: p_test TYPE abap_bool DEFAULT abap_true.  " Test mode
PARAMETERS: p_batch TYPE i DEFAULT 1000.              " Commit batch size

START-OF-SELECTION.

  DATA: lt_stxh    TYPE TABLE OF stxh,
        lt_lines   TYPE TABLE OF tline,
        lv_ebeln   TYPE ebeln,
        lv_ebelp   TYPE ebelp,
        lv_tdname  TYPE tdname,
        lv_counter TYPE numc5,
        lv_written TYPE i,
        lv_errors  TYPE i.

  " Read all PO-related text headers
  SELECT tdobject, tdid, tdspras, tdname
    FROM stxh
    INTO TABLE @lt_stxh
    WHERE tdobject IN ('EKKO', 'EKPO').

  WRITE: / 'Total text headers found:', lines( lt_stxh ).

  LOOP AT lt_stxh INTO DATA(ls_stxh).

    " Parse TDNAME to EBELN + EBELP
    IF ls_stxh-tdobject = 'EKKO'.
      lv_ebeln = ls_stxh-tdname.
      lv_ebelp = '00000'.
    ELSE.
      lv_ebeln = ls_stxh-tdname(10).
      lv_ebelp = ls_stxh-tdname+11(5).
    ENDIF.

    " Decompress via READ_TEXT
    CLEAR lt_lines.
    CALL FUNCTION 'READ_TEXT'
      EXPORTING
        id       = ls_stxh-tdid
        language = ls_stxh-tdspras
        name     = ls_stxh-tdname
        object   = ls_stxh-tdobject
      TABLES
        lines    = lt_lines
      EXCEPTIONS
        OTHERS   = 4.

    IF sy-subrc <> 0.
      ADD 1 TO lv_errors.
      WRITE: / 'READ_TEXT failed for:', ls_stxh-tdname.
      CONTINUE.
    ENDIF.

    IF p_test = abap_false.
      " Delete old entries
      DELETE FROM zpo_longtext
        WHERE ebeln    = lv_ebeln
          AND ebelp    = lv_ebelp
          AND tdobject = ls_stxh-tdobject
          AND tdid     = ls_stxh-tdid
          AND tdspras  = ls_stxh-tdspras.

      " Insert flat lines
      CLEAR lv_counter.
      LOOP AT lt_lines INTO DATA(ls_line).
        ADD 1 TO lv_counter.
        INSERT INTO zpo_longtext VALUES (
          sy-mandt ls_stxh-tdid lv_ebeln lv_ebelp
          ls_stxh-tdobject ls_stxh-tdspras lv_counter
          ls_line-tdformat ls_line-tdline
          sy-datum 'M' ).
      ENDLOOP.
    ENDIF.

    ADD 1 TO lv_written.

    " Commit in batches
    IF lv_written MOD p_batch = 0.
      IF p_test = abap_false.
        COMMIT WORK.
      ENDIF.
      WRITE: / 'Processed:', lv_written.
    ENDIF.

  ENDLOOP.

  IF p_test = abap_false.
    COMMIT WORK.
  ENDIF.

  WRITE: / '--- Migration Complete ---'.
  WRITE: / 'Written:', lv_written.
  WRITE: / 'Errors: ', lv_errors.
  IF p_test = abap_true.
    WRITE: / 'TEST MODE — no data written'.
  ENDIF.
```

---

## 6. AGENT BEHAVIOR GUIDELINES

### 6.1 Understand Before Code

Before writing any code, classify the task:
1. **Migration issue** → Check STXH count vs ZPO_LONGTEXT count. Check migration log.
2. **Dual-write issue** → Check BAdI ME_PROCESS_PO_CUST is active. Check ZCL_PO_TEXT_BADI_IMPL.
3. **Text missing in ZPO_LONGTEXT but exists in STXH** → Migration not run or BAdI not active.
4. **Text missing in STXH** → Text was never created. Not a persistence issue.
5. **Truncated text** → LINE_COUNTER gap or TDLINE 132-char limit exceeded.
6. **Performance issue** → Add index on ZPO_LONGTEXT (EBELN + TDOBJECT + TDID).
7. **BDC use case** → Guide user to SELECT directly from ZPO_LONGTEXT. Never use READ_TEXT in BDC.

### 6.2 Debugging Missing Text

```
Step 1 — Does text exist in STXH?
  SE16 → STXH
  WHERE TDOBJECT = 'EKKO' AND TDNAME = '<PO_NUMBER>' AND TDID = 'F01'
  If NO row → text was never created. Not a persistence issue.

Step 2 — Does text exist in ZPO_LONGTEXT?
  SE16 → ZPO_LONGTEXT
  WHERE EBELN = '<PO_NUMBER>' AND TDOBJECT = 'EKKO' AND TDID = 'F01'
  If NO row but STXH has it:
    → Check: was migration program ZPO_LONGTEXT_MIGRATE run?
    → Check: is BAdI ZCL_PO_TEXT_BADI_IMPL active (SE19)?
    → Run migration for this PO manually via ZCL_PO_LONGTEXT_HANDLER

Step 3 — Is LINE_COUNTER sequence correct?
  SELECT * FROM zpo_longtext WHERE ebeln = '<PO>'
  ORDER BY tdobject, tdid, tdspras, line_counter
  Gaps in LINE_COUNTER indicate partial migration failure
```

### 6.3 Key Rules

1. **Never replace STXH/STXL** — ZPO_LONGTEXT runs alongside, not instead of classic framework
2. **EBELP = '00000'** for header texts (TDOBJECT = 'EKKO')
3. **TDNAME for EKPO** = EBELN + space + EBELP — parse carefully
4. **LINE_COUNTER** drives rendering sequence — ORDER BY always
5. **DELETE + INSERT** per text (not UPSERT) — ensures deleted lines are removed
6. **Run migration in TEST mode first** — verify counts before writing
7. **BAdI fires AFTER SAVE_TEXT** — text must exist in STXH before READ_TEXT call in BAdI

---

## 7. QUICK REFERENCE CARD

```
SAME SYSTEM — no Hub, no replication, no SAP_COM_0267

SOURCE:       STXH (header) + STXL (lines, compressed)
              READ_TEXT function module decompresses
              TDNAME = EBELN for header / EBELN+' '+EBELP for items

TARGET:       ZPO_LONGTEXT (custom table, same system)
              Key: EBELN + EBELP + TDOBJECT + TDID + TDSPRAS + LINE_COUNTER
              Plain SQL — no decompression needed

PHASE 1:      ZPO_LONGTEXT_MIGRATE — one-time historic migration
              Reads STXH → READ_TEXT → INSERT ZPO_LONGTEXT (SOURCE='M')

PHASE 2:      BAdI ME_PROCESS_PO_CUST (ME_PURCHORD enhancement spot)
              Fires on ME21N/ME22N save
              ZCL_PO_TEXT_BADI_IMPL → ZCL_PO_LONGTEXT_HANDLER
              Writes to ZPO_LONGTEXT (SOURCE='D') after SAVE_TEXT

DUAL WRITE:   SAVE_TEXT → STXH/STXL (SAP standard, unchanged)
              BAdI    → ZPO_LONGTEXT (new, parallel)

BDC ACCESS:   SELECT * FROM zpo_longtext WHERE ebeln = '<PO>'
              ORDER BY tdobject, tdid, tdspras, line_counter.
              No READ_TEXT needed.

TEXT OBJECTS: EKKO/F01 = PO Header Note      (EBELP = 00000)
              EKKO/F02 = PO Header Delivery   (EBELP = 00000)
              EKPO/F01 = PO Item Note         (EBELP = item)
              EKPO/F02 = PO Item Delivery     (EBELP = item)
              EKPO/F09 = PO Item GR Text      (EBELP = item)
```

---

## 8. KNOWLEDGE DOCUMENTS

- `agent/knowledge/architecture/po-text-flow-diagram.md` — Full architecture diagrams
- `agent/knowledge/domain/po-longtext-domain.md` — Domain concepts, migration rules
- `agent/codebase-index/` — Object index, data flows, business rules
