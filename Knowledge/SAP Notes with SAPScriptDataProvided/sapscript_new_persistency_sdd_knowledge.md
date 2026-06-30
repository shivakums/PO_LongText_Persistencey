# SAP Script New Persistency — SDD Knowledge Extract
## Sales Order Notes Migration to New Persistency + SAPScript DataProvider Pattern

**Source:** SDD "New Persistency for Long Texts" (current working version)
**Wiki:** "How to implement Notes with SAPscript DataProvider and Richtext — Generic Business Services"
**Context:** Sales team completed this migration as the reference implementation that PO team is studying
**Date added to skill:** 2026-06-30

---

## 1. Why New Persistency Is Needed — The Root Problem

SAP stores all long texts in `STXL` — a **cluster table**. Cluster tables:
- Cannot be accessed via plain SQL SELECT
- Can only be read via proprietary ABAP command `IMPORT FROM DATABASE`
- Cannot be used in CDS views directly (only via workarounds like table functions or virtual elements)
- Table functions are NOT supported by CDC (Change Data Capture)
- Virtual elements are ONLY supported by SADL — not by other frameworks using CDC
- This blocks integration into the VDM (Virtual Data Model) for BW extraction, analytics, AI

**The solution:** Application-specific transparent persistency table where:
- Plain SQL is possible
- CDS views can be built on top
- BW extraction works
- AI and BDC access is possible
- Full-text search on HANA is possible

---

## 2. The SAPScript New Persistency Framework

SAP Script team provided a **framework** allowing applications to switch to their own
transparent table while still using standard SAPscript APIs (READ_TEXT, SAVE_TEXT etc.).

### How It Works

```
Application continues calling:
  SAVE_TEXT  → SAPscript framework → routes to application's new persistency class
  READ_TEXT  → SAPscript framework → reads from new table (after SDM) or old STXH/STXL (before SDM)

Application must provide a handler class inheriting from:
  CL_RSTXT_PERSISTENCE_FRAMEWORK

Methods the application must redefine:
  READ_HEADERS_VIA_RANGES   → Read multiple text headers via ranges table
  READ                      → Read a single text (header + content)
  CREATE                    → Create a new text in the new table
  CHANGE                    → Update an existing text
  DELETE                    → Delete a text

Registration:
  The handler class is registered in:
    TTXOB (text object level) — applies to all TDIDs for that object
    TTXID (text ID level)     — applies to specific TDID only
  Field: HANDLER_CLASS
  Example: Sales registered handler for text objects VBBK (header) and VBBP (item)
  PO equivalent: would register for EKKO (header) and EKPO (item)
```

---

## 3. Sales Order New Text Table Design (Reference for PO)

### Sales Text Table: `SDTP_TEXT` (or `VX_TEXT` in some references)

Key fields added to the new application-specific table:

| Field | Purpose |
|---|---|
| SD_DOCUMENT_ID | Properly typed key — better than generic CHAR70 TDNAME |
| SD_DOCUMENT_ITEM_ID | Item-level key |
| TEXT_CONTENT | Plain text string (converted from ITF format) |
| CREATED_BY, CREATED_AT | Administrative fields |
| CHANGED_BY, CHANGED_AT | Administrative fields |
| REF_TEXT_OBJECT, REF_TEXT_ID, REF_TEXT_NAME | Reference chain fields |
| Auth fields (encoded in TDTITLE) | SD Document Category, Sales Doc Type, Sales Org, Dist Channel, Division |

### Key Design Decisions for Sales

**Authorization transfer:** SD auth fields are passed from application buffer to the
new persistency class using the `THEAD-TDTITLE` field (confirmed by text framework
colleague Rene Zink). The 5 auth fields are concatenated: `SD Doc Category + Sales Doc Type + Sales Org + Dist Channel + Division` e.g. `C   TA  10001000`

**Copy vs Reference:**
- Option 1 (Copy only): Text content stored per document — SQL and CDS views work well. ~4M reference records (2% of 752M total) would be impacted.
- Option 2 (Copy + Reference): Feature parity but CDS view cannot search referenced text content, complex DELETE logic.

---

## 4. ITF Format Conversion — Critical for Migration

SAPscript stores text in **ITF (Interchange Text Format)** — proprietary format.
The new persistency stores plain text strings. Conversion is needed during migration:

```abap
" ITF → Plain text string
CALL FUNCTION 'CONVERT_ITF_TO_STREAM_TEXT'
  EXPORTING  ...  (converts TLINE table to plain text string)

" Plain text string → ITF
" Step 1: Split string into 132-char chunks
" Step 2: Call CONVERT_STREAM_TO_ITF_TEXT
CALL FUNCTION 'CONVERT_STREAM_TO_ITF_TEXT'
  EXPORTING  ...  (converts string to TLINE table)
```

---

## 5. SDM — Silent Data Migration (Most Relevant to PO)

### What SDM Is

SDM = Silent Data Migration. SAP-standard mechanism for background migration of data
from old format (STXH/STXL) to new format (new text table) without system downtime.

### Sales SDM Implementation Reference

**SDM Class:** `CL_SDM_SD_VBAK_TEXT_MIGRATION` (package `SD_BF_TEXT_DET`)
**Inherits from:** `CL_SDM_PACKAGE_MIGRATION`

### Key SDM Methods (Must Be Implemented)

| Method | Purpose |
|---|---|
| `IF_SDM_MIGRATION~MIGRATE_DATA` | Main migration: SELECT headers from VBAK → read texts via SELECT_TEXT → convert ITF to plain text → INSERT into new table (DELETE first for restartability) |
| `IF_SDM_MIGRATION~MIGRATE_DATA_FINISHED` | Check if migration is complete: SELECT VBAK where SDM_VERSION < target → if none found = done |
| `IF_SDM_MIGRATION~GET_PACKAGE_SIZE` | Returns 1000 (initial value) — tune so each package takes ~1 minute |
| `IF_SDM_MIGRATION~GET_TABLE_NAME` | Returns root table name: VBAK (or VBRK, LIKP) |
| `IF_SDM_MIGRATION~GET_CLIENT_FIELD` | Returns MANDT |
| `IF_SDM_MIGRATION~GET_SELECTIVE_FIELD` | Key field for packages: VBELN (or EBELN for PO) |
| `IF_SDM_MIGRATION~GET_STATUS_FIELD` | Returns SDM_VERSION field name |
| `IF_SDM_MIGRATION~GET_STATUS_VALUE_DONE` | Returns constant for "migration done" status |
| `IF_SDM_MIGRATION~MUST_RUN` | Returns abap_true |
| `IS_MIGRATION_FINISHED` | Calls `CL_SDM_PROC_STATUS_API=>IS_SDM_FINISHED` — used by handler class to decide which table to read from |

### SDM Phases and Dual-Write Pattern

```
PHASE 1 — Before upgrade (old release):
  Documents saved → write to STXH/STXL only
  SDM_VERSION = current release value

PHASE 2 — After upgrade, SDM NOT yet complete:
  New document created → write to BOTH old (STXH/STXL) AND new table
  Existing document changed → write to BOTH tables
  SDM_VERSION = target version for new records
  Application reads from: OLD persistence (STXH/STXL) — unchanged

  Background: SDM migration runs in packages:
    → SELECT 30,000 documents at a time
    → DELETE existing records from new table first (restartability)
    → SELECT_TEXT for all documents in package
    → READ_TEXT_TABLE for mass text retrieval
    → Convert ITF → plain text
    → INSERT into new table
    → Old STXH/STXL records NOT deleted (safety net for restart)

PHASE 3 — SDM complete:
  IS_MIGRATION_FINISHED returns TRUE
  Application switches READ to new table
  New documents: write to new table only (old SDM_VERSION check)
  Old STXH/STXL records can eventually be cleaned up
```

### SDM Performance Numbers from Sales POC

| System | VBAK records | Text records | Package size | Duration |
|---|---|---|---|---|
| DDCI (test) | 40,853 | 340 | 30,000 | Fast |
| CCW/720 (perf test) | 13.9M | 2.67M | 30,000 | 3.5 hours |

- Open SQL limit: max 32,767 in range table WHERE clause → package size set to 32,000
- Internal packaging within SELECT_TEXT calls every 30,000 documents
- CCW/720 test: 464 packages, 8-15 seconds per package (first package took 494 seconds for initialization)

### IS_MIGRATION_FINISHED Controls Dual-Write

This method is called by the handler class at runtime:
```
IS_MIGRATION_FINISHED returns FALSE:
  → All READ_TEXT / SELECT_TEXT calls → read from STXH/STXL (old)
  → All SAVE_TEXT / DELETE_TEXT calls → write to STXH/STXL AND new table

IS_MIGRATION_FINISHED returns TRUE:
  → All READ_TEXT / SELECT_TEXT calls → read from new table
  → All SAVE_TEXT / DELETE_TEXT calls → write to new table only
```

Result is buffered for entire dialog session (performance — avoids repeated SELECTs).

---

## 6. Text References — Design Challenge

### The Problem
SAPscript supports text **references** — a document can reference another document's text
instead of copying it. This creates reference chains:
```
KNA1 text → Sales Order text → Quotation text → ... (N levels deep)
```

**This cannot be resolved via CDS JOIN** because:
- Chain can be N levels deep (unknown depth)
- Reference can point to ANY text object (KNA1, EKKO, MATERIAL etc.)
- CDS views for many target objects don't exist yet

### Sales Decision
- Short term: Table function CDS view (P_SalesDocumentText) — reads from STXH
- Medium term (CE2702+): Transactional CDS view with 1-level self-join (like CRM solution)
- Long term: Replace table function data source with new text table after SDM complete

### Reference Impact Numbers
- 752 million total VBBK/VBBP records in customer systems
- ~4 million records have non-VBBK/VBBP references (2%)
- 98% are copy records (no reference issues)

---

## 7. CDS View Integration

### Current State (Before SDM)
```abap
" Table function CDS view (existing — reads from STXH via ABAP class):
CDS View: P_SalesDocumentText      → uses CL_SD_S4H_STXL_UTILS (reads STXH)
CDS View: P_SalesDocumentItemText  → same pattern for items
CDS View: P_BillingDocumentText    → uses CL_SD_BIL_S4H_STXL

These P-views are used in RAP layer: R_SalesOrderItemTextTP etc.
```

### After SDM Complete
- Replace data source in table function CDS view from STXH to new text table
- Build basic CDS view on new text table with properly typed key fields
- Build analytics CDS view on top — C1 released for external consumption
- DCL0 used for authorization on basic view

---

## 8. Key Differences: SAPScript New Persistency vs ZPO_LONGTEXT Approach

| Aspect | SAPScript New Persistency (Sales/SDD approach) | ZPO_LONGTEXT (Current Lift & Shift approach) |
|---|---|---|
| Integration | Uses SAPScript HANDLER_CLASS framework — SAVE_TEXT/READ_TEXT route automatically | BAdI ME_PROCESS_PO_CUST — fires AFTER SAVE_TEXT |
| Table design | Application-specific with typed keys, auth fields, ITF→plain conversion | Plain flat table with LINE_COUNTER per line |
| Text format stored | Plain text string (converted from ITF) | One row per line (TDLINE = 132 chars) |
| SDM | Uses CL_SDM_PACKAGE_MIGRATION framework — automatic routing via IS_MIGRATION_FINISHED | Manual migration report — no SDM_VERSION tracking |
| Read switching | Automatic via IS_MIGRATION_FINISHED in handler class | Manual — always reads from ZPO_LONGTEXT (no cutover logic) |
| Dual-write | Handled internally by framework during SDM | BAdI writes to both STXH (standard) + ZPO_LONGTEXT |
| References | Stored in table, partially handled | Not handled — only copies stored |
| VDM/CDS | CDS views built on new table — analytics + RAP | No CDS view yet — plain SQL only |

---

## 9. Impact on PO Decision (CE2702/CE2708)

Based on the SDD, the **SAPScript New Persistency framework approach** for PO would require:

1. **Handler class** inheriting from `CL_RSTXT_PERSISTENCE_FRAMEWORK`
   - Implement READ, CREATE, CHANGE, DELETE, READ_HEADERS_VIA_RANGES
   - Register in TTXOB for text objects EKKO and EKPO
   - This replaces the BAdI approach

2. **New PO text table** (equivalent to SDTP_TEXT for SD)
   - Typed key fields: EBELN, EBELP (instead of generic CHAR70 TDNAME)
   - Plain text content (ITF converted to string)
   - Auth fields: Purchase Org, Company Code, Document Type etc.

3. **SDM class** inheriting from `CL_SDM_PACKAGE_MIGRATION`
   - Root table: EKKO (equivalent to VBAK for SD)
   - SDM_VERSION field needs to be added to EKKO (coordination needed)
   - Package size: ~30,000 POs per package
   - Performance estimate: ~3.5 hours for 13M records (similar to Sales)

4. **CDS views** on new text table
   - Basic view, analytics view (C1 released), RAP integration view

**Critical open question:** Is this full framework approach required to work with the
Notes Reuse RAP Business Object, or can ZPO_LONGTEXT-style own table also be plugged in?
This is the question pending with the Notes Reuse team (from CE2702/CE2708 sync meeting).

---

## 10. Key Contacts from SDD

| Name | Role |
|---|---|
| Rene Zink | SAPScript text framework — confirmed TDTITLE field usage for auth transfer |
| Toralf, Thomas | Architecture alignment for auth encoding approach |
| Maximilian Denne | SD Billing — confirmed VBRK/VBRP not used productively |
| Juergen Reidl | Performance expert — CCW/720 SDM testing guidance |
| Chris, Karen Fang | Sales team — reference implementation owners |
