# PO Long Text Persistency — Codebase Overview

## Project Overview

- **Name:** PO_LongText_Persistencey
- **Type:** SAP S/4HANA — New Persistency for PO Long Texts within MPOC/CPO
- **Domain:** Purchase Order Notes migration from classic text framework (STXH/STXL) to CDS-based Hub persistence table

## Tech Stack

- SAP S/4HANA ABAP (backend + Hub)
- CDS (Core Data Services) views — VDM layer pattern
- OData v2 service extension (MM_PUR_CNTRL_PO_MAI_SRV)
- SAP Fiori (UI5) — Notes tab in CPO app
- SAP Text Framework (STXH/STXL/READ_TEXT) — source system
- Communication Arrangement SAP_COM_0267 — Backend-to-Hub channel

## Key Objects

| Object | Type | Description |
|---|---|---|
| MMPUR_EXT_PO_TEXT | Hub Table | New persistence table for PO text lines |
| I_CntrlPurOrderText | CDS Basic View | Reads MMPUR_EXT_PO_TEXT |
| C_CntrlPurOrderTextTP | CDS Composite View | Exposes text via OData |
| CL_MMPUR_EXT_PO_TEXT_HUB | Class | Text extraction coordinator |
| CL_MMPUR_PO_TEXT_EXT_SRV | Class | OData caller to ERP via SAP_COM_0267 |
| CL_MMPUR_CPU_TEXT_DB_UTILITY | Class | Persistence save/delete logic |
| SAP_MM_PO_TEXT_EXTRACTION | App Job | Scheduled text extraction |

## Architecture Layers

1. ERP source: STXH + STXL (classic text framework)
2. Extraction pipeline: Hub job → Hub classes → SAP_COM_0267 → Backend extractor
3. New persistence: MMPUR_EXT_PO_TEXT (Hub table)
4. CDS layer: I_ Basic → C_ Composite
5. OData: MM_PUR_CNTRL_PO_MAI_SRV / CentralPurchaseOrderTextSet
6. Fiori UI: Notes tab in MM_CEN_PURORDS1 (F3292)

## Key Constraint

**EXTSOURCESYSTEM** is part of MMPUR_EXT_PO_TEXT primary key — always include in WHERE clauses.
**EBELP = '00000'** for header texts (TDOBJECT = 'EKKO').
**LINE_COUNTER** drives text line sequence — never re-order.
