# PO Long Text New Persistency — Architecture Flow Diagram

---

## 1. System Landscape — Single System

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    SINGLE SAP SYSTEM (ERP / S/4HANA)                    │
│                                                                          │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │  PURCHASE ORDER DOCUMENT                                            │ │
│  │  EKKO — PO Header (EBELN, BUKRS, LIFNR, BEDAT...)                  │ │
│  │  EKPO — PO Item   (EBELN, EBELP, MATNR, MENGE...)                  │ │
│  └──────────────────────────────┬─────────────────────────────────────┘ │
│                                 │ SAVE_TEXT (SAP standard)               │
│                                 ▼                                        │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │  CLASSIC SAP TEXT FRAMEWORK (SAP Standard — not modified)          │ │
│  │                                                                     │ │
│  │  STXH (Text Header)                                                 │ │
│  │  ┌─────────────────────────────────────────────────────────────┐   │ │
│  │  │ TDOBJECT │ TDID │ TDSPRAS │ TDNAME                          │   │ │
│  │  │ EKKO     │ F01  │ E       │ 4500001234                      │   │ │
│  │  │ EKPO     │ F01  │ E       │ 4500001234 00010                │   │ │
│  │  └─────────────────────────────────────────────────────────────┘   │ │
│  │                                                                     │ │
│  │  STXL (Text Lines — COMPRESSED, not SE16-readable)                 │ │
│  │  ┌─────────────────────────────────────────────────────────────┐   │ │
│  │  │ CLUSTR — binary compressed content (cannot SELECT directly) │   │ │
│  │  │ Must use READ_TEXT function module to decompress             │   │ │
│  │  └─────────────────────────────────────────────────────────────┘   │ │
│  └──────────────────────────────┬─────────────────────────────────────┘ │
│                                 │                                        │
│          READ_TEXT FM           │   decompresses STXL → flat lines       │
│                                 ▼                                        │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │  ZPO_LONGTEXT — New Custom Persistence Table                       │ │
│  │                                                                     │ │
│  │  ┌──────────────────────────────────────────────────────────────┐  │ │
│  │  │ Key: EBELN + EBELP + TDOBJECT + TDID + TDSPRAS + LINE_COUNTER│  │ │
│  │  │ Data: TDFORMAT, TDLINE (132 chars), MIGRATED_AT, SOURCE      │  │ │
│  │  └──────────────────────────────────────────────────────────────┘  │ │
│  │                                                                     │ │
│  │  Plain SQL — no decompression — BDC-ready — CDS-ready              │ │
│  └────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Phase 1 — Historic Migration Flow

```
TRIGGER: Run report ZPO_LONGTEXT_MIGRATE once
         (Selection: Test mode first, then productive)

Step 1: Read all PO text headers from STXH
  ┌──────────────────────────────────────────────────────────┐
  │ SELECT tdobject, tdid, tdspras, tdname FROM stxh         │
  │   WHERE tdobject IN ('EKKO', 'EKPO')                    │
  └────────────────────────────┬─────────────────────────────┘
                               │
  Step 2: Parse TDNAME         │
  ┌──────────────────────────────────────────────────────────┐
  │ EKKO: EBELN = TDNAME(10), EBELP = '00000'               │
  │ EKPO: EBELN = TDNAME(1,10), EBELP = TDNAME(12,5)        │
  └────────────────────────────┬─────────────────────────────┘
                               │
  Step 3: Decompress           │
  ┌──────────────────────────────────────────────────────────┐
  │ CALL FUNCTION 'READ_TEXT'                                │
  │   EXPORTING id=TDID, language=TDSPRAS,                  │
  │             name=TDNAME, object=TDOBJECT                 │
  │   TABLES lines = lt_lines  ← flat text lines            │
  └────────────────────────────┬─────────────────────────────┘
                               │
  Step 4: Persist flat lines   │
  ┌──────────────────────────────────────────────────────────┐
  │ DELETE FROM zpo_longtext (old lines for this text)       │
  │ INSERT INTO zpo_longtext (one row per line, SOURCE='M')  │
  │ COMMIT WORK every 1000 POs                               │
  └─────────────────────────────────────────────────────────-┘
                               │
  Step 5: Validate             │
  ┌──────────────────────────────────────────────────────────┐
  │ Count STXH rows vs ZPO_LONGTEXT rows                    │
  │ Spot-check 10 POs                                        │
  └──────────────────────────────────────────────────────────┘
```

---

## 3. Phase 2 — Dual Write for New PO Creation

```
User saves PO in ME21N / ME22N / Fiori Create PO
        │
        ▼
SAP standard: SAVE_TEXT called
        │ writes STXH + STXL (unchanged — SAP standard continues as always)
        │
        ▼
BAdI: ME_PROCESS_PO_CUST fires (Enhancement Spot: ME_PURCHORD)
  Method: PROCESS_HEADER → for header texts (EKKO)
  Method: PROCESS_ITEM   → for item texts   (EKPO)
        │
        ▼
ZCL_PO_TEXT_BADI_IMPL (BAdI implementation class)
        │
        ▼
ZCL_PO_LONGTEXT_HANDLER→write_to_persistence(
  iv_ebeln, iv_ebelp, iv_tdobject, iv_tdid, iv_tdspras )
        │
        ▼
READ_TEXT called to get lines just saved by SAVE_TEXT
        │
        ▼
DELETE old lines + INSERT new lines into ZPO_LONGTEXT
  SOURCE = 'D' (Dual-write)
        │
        ▼
┌──────────────────────────────────────────────────────────────┐
│  RESULT: Both tables in sync after every PO save             │
│  STXH/STXL  ← SAP standard (unchanged)                      │
│  ZPO_LONGTEXT ← flat, readable, BDC-ready (new)             │
└──────────────────────────────────────────────────────────────┘
```

---

## 4. BDC / Reporting Read Flow

```
BDC program or report needs PO long text
        │
        ▼  OLD WAY (slow, requires decompression)
  CALL FUNCTION 'READ_TEXT'
    EXPORTING id='F01', language='E', name='4500001234', object='EKKO'
    TABLES lines = lt_lines.

        │
        ▼  NEW WAY (fast, direct SQL, no decompression)
  SELECT * FROM zpo_longtext
    WHERE ebeln    = '4500001234'
      AND tdobject = 'EKKO'
      AND tdid     = 'F01'
      AND tdspras  = 'E'
    ORDER BY line_counter.
```

---

## 5. TDNAME Construction Reference

```
STXH TDNAME field — how it is built per text object:

EKKO (PO Header text):
  TDNAME = EBELN (10 chars, left-justified, space-padded)
  Example: '4500001234'

EKPO (PO Item text):
  TDNAME = EBELN + ' ' + EBELP
  Example: '4500001234 00010'
            ──────────   ─────
            10 chars     5 chars (item)
            EBELN        space + EBELP

WARNING: Getting TDNAME wrong means READ_TEXT returns nothing.
Always check STXH directly in SE16 to verify the exact TDNAME format.
```

---

## 6. Debugging Decision Tree

```
"Text missing in ZPO_LONGTEXT for PO 4500001234"
        │
        ▼
Does STXH have the text?
  SE16 → STXH WHERE TDOBJECT='EKKO' AND TDNAME='4500001234' AND TDID='F01'
  │
  ├── NO → Text was never created. Not a persistence issue.
  │        Create text in ME23N/ME22N, then BAdI will write to ZPO_LONGTEXT.
  │
  └── YES
           │
           ▼
  Does ZPO_LONGTEXT have the text?
    SE16 → ZPO_LONGTEXT WHERE EBELN='4500001234' AND TDOBJECT='EKKO' AND TDID='F01'
    │
    ├── NO — SOURCE='M' rows missing
    │         → Migration not run. Run ZPO_LONGTEXT_MIGRATE.
    │
    ├── NO — This is a recently created PO
    │         → BAdI not active. Check SE19 → ME_PROCESS_PO_CUST
    │           → ZCL_PO_TEXT_BADI_IMPL must be active.
    │           → Run ZCL_PO_LONGTEXT_HANDLER manually for this PO.
    │
    └── YES — rows exist
               │
               ▼
    Is LINE_COUNTER sequence correct?
      SELECT ORDER BY line_counter — check for gaps
      Gaps → partial migration failure → re-run for this PO
```
