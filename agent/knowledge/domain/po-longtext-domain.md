# PO Long Text New Persistency — Domain Knowledge

---

## 1. Business Domain

### 1.1 Why Does This Exist?

SAP stores all document long texts (PO notes, SO notes, material texts etc.) in a generic
compressed framework using STXH and STXL. The compression makes STXL unreadable via plain SQL.

This creates three problems:
1. **BDC programs** — cannot read long text content directly; must call READ_TEXT FM
2. **Reporting / CDS** — STXL cannot be used in SELECT or CDS views
3. **Performance** — READ_TEXT decompresses on every call; expensive at scale

The new persistence table `ZPO_LONGTEXT` solves all three by storing the same content
in a flat, SQL-readable format **on the same system**.

### 1.2 What Changes and What Does NOT Change

| Aspect | Before | After |
|---|---|---|
| User creating PO text in ME21N | SAP standard — unchanged | SAP standard — unchanged |
| STXH table | Written by SAVE_TEXT — unchanged | Written by SAVE_TEXT — unchanged |
| STXL table | Written by SAVE_TEXT — unchanged | Written by SAVE_TEXT — unchanged |
| ZPO_LONGTEXT | Does not exist | Populated in parallel by BAdI |
| BDC reading text | Must call READ_TEXT | Can SELECT directly from ZPO_LONGTEXT |
| Classic READ_TEXT | Still works | Still works (STXH/STXL unchanged) |

**Key principle: ZPO_LONGTEXT is a parallel copy — it does not replace STXH/STXL.**

---

## 2. Classic SAP Text Framework — How It Works

### 2.1 STXH — Text Header

One row per text. Stores metadata only — no text content.

| Field | Description | Example |
|---|---|---|
| TDOBJECT | Which SAP object type owns this text | `EKKO` (PO Header) |
| TDID | Which type of note | `F01` (General note) |
| TDSPRAS | Language | `E` (English) |
| TDNAME | Key of the owning document | `4500001234` |

### 2.2 STXL — Text Lines

Stores the actual text content but in **compressed binary cluster format**.
Cannot be read with SE16 or SELECT. Must use `READ_TEXT` function module.

```abap
" The ONLY correct way to read long text
CALL FUNCTION 'READ_TEXT'
  EXPORTING
    id       = 'F01'           " Text ID from STXH-TDID
    language = 'E'             " Language from STXH-TDSPRAS
    name     = '4500001234'    " TDNAME from STXH
    object   = 'EKKO'          " TDOBJECT from STXH
  TABLES
    lines    = lt_lines        " Returns TLINE table (TDFORMAT + TDLINE)
  EXCEPTIONS
    OTHERS   = 4.
```

### 2.3 SAVE_TEXT — How Text is Written

When a user types a note in ME21N and saves, SAP calls:

```abap
CALL FUNCTION 'SAVE_TEXT'
  EXPORTING
    header   = ls_thead      " STXH fields
  TABLES
    lines    = lt_lines      " Text content
  EXCEPTIONS
    OTHERS   = 4.
```

This writes to STXH + STXL. Our dual-write fires AFTER this via BAdI.

---

## 3. Text Types for Purchase Orders

### 3.1 Header-Level Texts (TDOBJECT = 'EKKO')

These belong to the PO as a whole. EBELP = '00000' in ZPO_LONGTEXT.

| TDID | Description | Used For |
|---|---|---|
| F01 | PO Header General Note | Internal procurement note |
| F02 | PO Header Delivery Text | Delivery instructions to supplier |
| F03 | PO Header Terms of Payment | Payment condition notes |
| F06-F08 | Reminder texts | Expediting notes |

TDNAME in STXH = EBELN (10 chars)

### 3.2 Item-Level Texts (TDOBJECT = 'EKPO')

These belong to a specific PO line item. EBELP = actual item number.

| TDID | Description | Used For |
|---|---|---|
| F01 | PO Item General Note | Item-specific procurement note |
| F02 | PO Item Delivery Text | Item delivery instructions |
| F09 | PO Item GR Text | Goods receipt inspection note |

TDNAME in STXH = EBELN + ' ' + EBELP (e.g. `4500001234 00010`)

---

## 4. Migration Rules

### 4.1 Historic Migration (Phase 1 — One-Time)

- Run `ZPO_LONGTEXT_MIGRATE` once in TEST mode — verify counts
- Run in PRODUCTIVE mode with COMMIT every 1000 POs
- Expected volume: can be millions of rows for active systems
- Source = 'M' (Migration) in ZPO_LONGTEXT

### 4.2 Dual Write (Phase 2 — Ongoing)

- BAdI `ME_PROCESS_PO_CUST` fires on every ME21N/ME22N save
- Covers: new PO creation, text additions, text changes, text deletions
- Source = 'D' (Dual-write) in ZPO_LONGTEXT
- Uses DELETE + INSERT pattern — ensures deletions on STXH side are reflected

### 4.3 Text Deletion Handling

When a user deletes a long text in ME22N:
- SAP calls `DELETE_TEXT` → removes from STXH/STXL
- BAdI fires → READ_TEXT returns nothing (text deleted)
- Handler deletes from ZPO_LONGTEXT → both stay in sync

### 4.4 What Triggers Dual Write

| Action | BAdI Method Fired |
|---|---|
| Create new PO with header text | PROCESS_HEADER |
| Add text to existing PO header | PROCESS_HEADER |
| Change existing PO header text | PROCESS_HEADER |
| Delete PO header text | PROCESS_HEADER |
| Add item to PO with item text | PROCESS_ITEM |
| Change PO item text | PROCESS_ITEM |

---

## 5. Sales Order Parallel (VBAK/VBAP)

Exactly the same pattern applies. Only the object names differ:

| Aspect | PO | SO |
|---|---|---|
| Header table | EKKO | VBAK |
| Item table | EKPO | VBAP |
| TDOBJECT header | EKKO | VBAK |
| TDOBJECT item | EKPO | VBAP |
| TDNAME header | VBELN | VBELN |
| TDNAME item | EBELN+' '+EBELP | VBELN+POSNR |
| Persistence table | ZPO_LONGTEXT | ZSO_LONGTEXT |
| BAdI | ME_PROCESS_PO_CUST | userexit in VA01/VA02 |

The persistence table structure is identical — only TDOBJECT values change.

---

## 6. Known Constraints

| Constraint | Detail |
|---|---|
| Text line max length | 132 chars (TDLINE) — same as STXL |
| Not real-time for historic | Migration is batch — run once |
| BAdI timing | Fires after SAVE_TEXT — slight delay possible |
| Multi-language | Each language is a separate STXH row — handle all |
| SO10 standard texts | Not in scope — only document-specific texts |
| Archiving | If STXL is archived, migration must run before archive |
