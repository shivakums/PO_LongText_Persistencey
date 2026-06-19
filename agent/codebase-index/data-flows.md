# Data Flows — PO Long Text Persistency

---

## Flow 1 — Historic Migration (One-Time)

```
Trigger: Manual run of ZPO_LONGTEXT_MIGRATE in SE38

1.  SELECT tdobject, tdid, tdspras, tdname FROM stxh
      WHERE tdobject IN ('EKKO', 'EKPO')
    → gives complete list of all PO long texts on the system

2.  For each STXH row:
    Parse TDNAME:
      EKKO → EBELN = TDNAME, EBELP = '00000'
      EKPO → EBELN = TDNAME(1,10), EBELP = TDNAME(12,5)

3.  Call READ_TEXT to decompress STXL:
    CALL FUNCTION 'READ_TEXT'
      EXPORTING id=TDID, language=TDSPRAS, name=TDNAME, object=TDOBJECT
      TABLES lines = lt_lines

4.  DELETE FROM zpo_longtext
      WHERE ebeln=lv_ebeln AND ebelp=lv_ebelp
        AND tdobject=TDOBJECT AND tdid=TDID AND tdspras=TDSPRAS

5.  INSERT flat lines with LINE_COUNTER sequence, SOURCE = 'M'

6.  COMMIT WORK every 1000 POs

7.  Write migration log — count written vs errors
```

---

## Flow 2 — Dual Write (New PO Creation / Change)

```
Trigger: User saves PO in ME21N / ME22N / Fiori

1.  SAP standard SAVE_TEXT → STXH + STXL written (unchanged)

2.  BAdI ME_PROCESS_PO_CUST fires (Enhancement Spot ME_PURCHORD)
      PROCESS_HEADER → triggered for header text changes
      PROCESS_ITEM   → triggered for item text changes

3.  ZCL_PO_TEXT_BADI_IMPL calls ZCL_PO_LONGTEXT_HANDLER
      write_to_persistence(iv_ebeln, iv_ebelp, iv_tdobject, iv_tdid, iv_tdspras)

4.  READ_TEXT called for the just-saved text
      → gets flat lines from STXH/STXL

5.  DELETE old ZPO_LONGTEXT rows for this text

6.  INSERT new rows with SOURCE = 'D'

NOTE: If text was DELETED by user → READ_TEXT returns nothing
      → Only DELETE step runs → ZPO_LONGTEXT cleaned up correctly
```

---

## Flow 3 — BDC / Report Read

```
BDC program or report needs PO long text content

OLD WAY (before):
  CALL FUNCTION 'READ_TEXT'
    EXPORTING object='EKKO', id='F01', language='E', name='4500001234'
    TABLES lines = lt_lines.
  → Decompresses STXL on every call
  → Slow at scale, cannot be used in SELECT / CDS

NEW WAY (after migration):
  SELECT * FROM zpo_longtext
    WHERE ebeln    = '4500001234'
      AND tdobject = 'EKKO'
      AND tdid     = 'F01'
      AND tdspras  = 'E'
    ORDER BY line_counter.
  → Direct SQL — instant
  → No FM call, no decompression
  → Works in CDS views, reports, BDC
```

---

## Key Tables

| Table | System | Writeable By | Readable By | Notes |
|---|---|---|---|---|
| STXH | Same SAP | SAVE_TEXT (SAP std) | SE16, direct SELECT | Metadata only — no text content |
| STXL | Same SAP | SAVE_TEXT (SAP std) | READ_TEXT FM only | Compressed — not SE16-readable |
| ZPO_LONGTEXT | Same SAP | Migration + BAdI | Direct SELECT, CDS, BDC | New flat table — plain SQL |
