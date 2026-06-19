# Business Rules — PO Long Text Persistency

## Rule 1 — ZPO_LONGTEXT Runs Parallel to STXH/STXL

**Rule:** Never replace or modify STXH/STXL. ZPO_LONGTEXT is a parallel copy only.
**Why:** SAP standard processes depend on STXH/STXL. Modifying them breaks standard.
**How to apply:** All writes to ZPO_LONGTEXT are ADDITIONAL to SAP standard SAVE_TEXT.

---

## Rule 2 — EBELP = '00000' for Header Texts

**Rule:** When TDOBJECT = 'EKKO', always set EBELP = '00000' in ZPO_LONGTEXT.
**Why:** EBELP is part of the primary key. Header texts have no item number.
**How to apply:** In all INSERT/SELECT on ZPO_LONGTEXT, set EBELP = '00000' when TDOBJECT = 'EKKO'.

---

## Rule 3 — TDNAME Parsing for EKPO

**Rule:** For TDOBJECT = 'EKPO', TDNAME = EBELN (chars 1-10) + space + EBELP (chars 12-16).
**Why:** Wrong TDNAME makes READ_TEXT return nothing.
**How to apply:** `lv_ebeln = tdname(10). lv_ebelp = tdname+11(5).`

---

## Rule 4 — LINE_COUNTER Sequence

**Rule:** Always SELECT ORDER BY LINE_COUNTER ASCENDING. Never re-order by other fields.
**Why:** Text lines are multi-line notes. Wrong order destroys meaning.
**How to apply:** Every SELECT includes `ORDER BY tdobject, tdid, tdspras, line_counter`.

---

## Rule 5 — DELETE + INSERT (Not UPSERT)

**Rule:** DELETE existing rows before INSERT. Never UPDATE or MODIFY.
**Why:** User may delete lines in ME22N — UPSERT leaves orphan old lines.
**How to apply:** DELETE WHERE ebeln+ebelp+tdobject+tdid+tdspras, then INSERT new lines.

---

## Rule 6 — BAdI Fires AFTER SAVE_TEXT

**Rule:** BAdI ME_PROCESS_PO_CUST fires AFTER SAVE_TEXT. READ_TEXT inside BAdI reads fresh text.
**Why:** READ_TEXT before SAVE_TEXT returns nothing — text not yet committed.
**How to apply:** Never call ZPO_LONGTEXT write logic outside of the BAdI context.

---

## Rule 7 — Run Migration in Test Mode First

**Rule:** Run ZPO_LONGTEXT_MIGRATE with P_TEST = 'X' first. Confirm counts. Then productive.
**Why:** Prevents partial writes. Confirms scope before DB commit.
**How to apply:** P_TEST defaults to 'X'. Change to blank only after test run confirmed.

---

## OLD CONTENT BELOW — SUPERSEDED

## EXTSOURCESYSTEM Invariant (REMOVED — not applicable, single system)

**Rule:** EXTSOURCESYSTEM is part of MMPUR_EXT_PO_TEXT primary key. Every SELECT, INSERT, UPDATE,
or DELETE on MMPUR_EXT_PO_TEXT MUST include EXTSOURCESYSTEM in the WHERE clause.

**Why:** Failure causes cross-system data contamination — multiple backend ERPs share Hub storage.

**How to apply:** Always flag missing EXTSOURCESYSTEM during code review.

---

## EBELP Header Text Rule

**Rule:** Header-level texts (TDOBJECT = 'EKKO') must use EBELP = '00000' (5-digit zero-padded).

**Why:** MMPUR_EXT_PO_TEXT uses EBELP as a key field for both header and item texts. Using empty
or NULL for header texts breaks key integrity.

**How to apply:** Always set EBELP = '00000' when TDOBJECT = 'EKKO'.

---

## LINE_COUNTER Sequence Rule

**Rule:** TEXT lines must be inserted and read in LINE_COUNTER ascending order. Never sort by any
other field.

**Why:** PO notes are written line by line. Rendering in wrong order destroys the meaning.

**How to apply:** Always add `ORDER BY line_counter ASCENDING` in SELECT from MMPUR_EXT_PO_TEXT.

---

## Full Refresh per PO Rule

**Rule:** Persistence uses DELETE + INSERT per PO (not UPSERT). Always delete existing rows for
a PO before inserting new ones.

**Why:** Ensures deleted text lines on ERP are removed from Hub on next extraction run.

**How to apply:**
```abap
DELETE FROM mmpur_ext_po_text
  WHERE ebeln = @lv_ebeln
    AND extsourcesystem = @lv_sys.

INSERT mmpur_ext_po_text FROM TABLE @lt_new_lines.
```

---

## Job Sequence Dependency

**Rule:** SAP_MM_PO_TEXT_EXTRACTION must run AFTER SAP_MM_PO_EXTRACTION completes.

**Why:** Text extraction reads the PO list from MMPUR_EXT_EKKO. If main extraction has not run,
the PO list is empty or stale and texts will not be extracted.

**How to apply:** Schedule SAP_MM_PO_TEXT_EXTRACTION as a dependent step after SAP_MM_PO_EXTRACTION
in the application job chain.

---

## Language Extraction Rule

**Rule:** Extract ALL languages present in STXH for each PO, not just the logon language.

**Why:** Multilingual environments may have notes in DE, EN, FR etc. Extracting only one language
means other language notes are silently lost.

**How to apply:** Do not filter on TDSPRAS in the extraction scope. Let the extractor read all
STXH rows for a given TDOBJECT + TDNAME + TDID combination.
