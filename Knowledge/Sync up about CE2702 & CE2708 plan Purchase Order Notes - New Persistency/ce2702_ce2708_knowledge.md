# CE2702 & CE2708 Plan — PO Notes New Persistency
## Sync-up Meeting Knowledge Extract

**Source:** Meeting "Sync up about CE2702 & CE2708 plan Purchase Order Notes — New Persistency"
**Date:** 2026-06-25
**Attendees:** Jess (Lift & Shift team), Rajesh (PO Product), Christopher (Architect),
Nils Hartmann (PO Product Owner), Olaf (Engineering), + procurement notes team
**Wiki:** PO Header & Item Notes Reuse — Modernization — S/4HANA Procurement Team WDF11

---

## 1. Context — What This Meeting Is About

The meeting is a planning sync for **CE2702 and CE2708** to decide the target architecture
for PO Header and Item Notes (long text) migration from the classic SAP Script framework
(STXH/STXL) to a **new persistency**. This directly impacts the `ZPO_LONGTEXT` approach
being developed in the Lift & Shift team.

**Key tension:** Three different approaches exist and no consensus has been reached yet.
This meeting is about understanding the options and agreeing on a phased plan.

---

## 2. Three Persistency Approaches Under Discussion

### Approach 1 — Generic Table (Basis / BCSRV Team)
**Table:** `SGBT_NTCEONT` (generic notes persistency table)
**Owner:** BCSRV component — Basis team

- Already provided wiki guidelines on how to use this
- Notes Reuse RAP Business Object team built architecture around this table
- Supplier Confirmation already uses this approach (completely new feature — no migration needed)
- **Drawback:** Less flexible — cannot add application-specific attributes
- **Drawback:** CDS views, C1 contract views owned by Basis — not by PO team
- **Drawback:** Extensibility limited — cannot add PO-specific fields
- **Question open:** Will Basis expose the CDS views for external consumption by customers/partners?

### Approach 2 — Application-Specific Own Table (Sales Team Approach)
**Table:** Custom table owned by each LOB (like `ZPO_LONGTEXT` in our current approach)
**Guideline provider:** SAP Script X team — explicitly asked all applications to move to own persistency

- Sales team already followed this approach successfully
- SAP Script X team provided migration guidelines — already used by Sales
- More flexible — can add application-specific attributes and joins
- Better performance — application controls the table design
- Better for AI and BDC access — plain SQL accessible
- **Drawback:** Each LOB must build and maintain their own table
- **Question open:** Is own-table approach compatible with RAP Notes Reuse component?

### Approach 3 — RAP Notes Reuse Business Object
**Component:** Notes Reuse RAP Business Subject
**Owner:** Notes Reuse team (separate from Basis and SAP Script X)

- Provides a reusable business object for notes across multiple applications
- Currently documented to work with generic table (`SGBT_NTCEONT`)
- **Problem:** Direct text references NOT supported in new persistency (confirmed)
- **Problem:** Notes not yet modelled in the new modernized PO OData V4 API at all
- **Question open:** Can Notes Reuse work with application-specific own table?
- **Question open:** Has Notes Reuse improved since Sales team evaluated and rejected it?

---

## 3. SDM — Silent Data Migration

**SDM = Silent Data Migration** — the SAP-standard mechanism for migrating data from old
to new format without customer downtime.

### How Sales Team Did It (Reference Pattern):
```
Phase 1 (CE2702 equivalent):
  → Write to BOTH old tables (STXH/STXL) AND new persistency simultaneously
  → Read still happens from OLD tables (application unchanged)
  → AI, BDC, new queries read from NEW table (new consumption path)
  → SDM migration reports run in background to migrate historic data

Phase 2 (CE2708 equivalent — after SDM complete):
  → Once all historic data migrated via SDM reports
  → Cut off READ from old tables
  → Switch completely to new persistency
  → Old tables become legacy / archived
```

### Key Insight from Christopher:
> *"They write to both tables. They read from only the old legacy tables and the execution
> of SDM reports was prerequisite so that they can cut off the read operation from the old ones."*

### PO Plan (Agreed Direction):
- **2702:** Write to BOTH old (STXH/STXL) AND new persistency simultaneously
- **2708:** After SDM complete — switch read to new persistency, cut off old tables
- Modern PO API (new OData V4): can write directly to new tables only (new POs)
- Legacy apps (ME21N/ME22N): continue writing to both until full migration

---

## 4. Open Questions — Must Be Resolved Before Architecture Decision

| # | Open Question | Who to Ask | Priority |
|---|---|---|---|
| 1 | Is application-specific own table compatible with RAP Notes Reuse Business Object? | Notes Reuse team + SAP Script X team | **CRITICAL — blocks all other decisions** |
| 2 | Has Notes Reuse improved since Sales evaluated it 1 year ago? | Notes Reuse team | High |
| 3 | Will Basis (BCSRV) expose CDS views and C1 contract views externally? | Basis / BCSRV team | High |
| 4 | What referencing scenarios exist for PO notes and how does Sales handle referencing? | Sales team | High |
| 5 | What is currently supported in public cloud for PO notes referencing? | PO team analysis | High |
| 6 | Can customers configure text referencing copy rules in public cloud? | PO team analysis | Medium |
| 7 | Which other business objects use EKKO/EKPO text objects and must be included? | Analysis task | Medium |
| 8 | Are there separate TDIDs per team or do teams reuse the same TDIDs? | Analysis task | Medium |
| 9 | Can customers create their own custom TDIDs in public cloud? | PO team | Low |
| 10 | Is migration possible at TDID level (not just text object level)? | Analysis task | Medium |

---

## 5. Teams Involved and Their Roles

| Team | Role | Contact | Status |
|---|---|---|---|
| **Lift & Shift / WDF11** | Leading analysis and POC for 2702 | Jess | Active |
| **PO Product / WDF11** | Architecture decisions, sign-off | Nils Hartmann, Rajesh | Active |
| **SAP Script X Team** | Provided guidelines to move to own persistency | Not yet confirmed | To contact |
| **Notes Reuse RAP Team** | Own the Notes Reuse Business Object and generic table architecture | Not yet confirmed | To contact |
| **Basis / BCSRV Team** | Own SGBT_NTCEONT generic table and CDS views | BC team contact | To contact |
| **Sales Team** | Already completed migration — reference implementation | Chris, Karen Fang | Consulted |
| **Procurement Notes Reuse Team** | BLR S4 team — must be kept in loop | BLR S4 team | To involve |
| **Modernized PO API Team (MEPO/Maple)** | Notes must be modelled in new OData V4 API | Nils + Maple team | For POC |

---

## 6. Delivery Timeline — CE2702 and CE2708 Plan

### CE2702 Plan (Analysis + POC)
Tasks agreed for 2702:

1. **Clarify open points with teams:**
   - Sync with SAP Script X team — understand their guideline and compatibility with Notes Reuse
   - Sync with Notes Reuse RAP team — understand generic table approach and own-table compatibility
   - Sync with Sales team — understand referencing approach and lessons learned
   - Sync with Basis/BCSRV — understand CDS view exposure for customers

2. **Analyze PO-specific open points:**
   - Identify all business objects using EKKO/EKPO text objects
   - Check referencing support in public cloud for PO notes
   - Understand copy rules for header and item texts

3. **Architecture/Concept Document:**
   - Produce a concept document or design document covering the chosen approach
   - Must be usable as base for other business objects (EKKO/EKPO affected objects)
   - Sign-off from: PO product team + relevant framework teams

4. **POC in DDCI system:**
   - POC goal: prove that notes can be written to new persistency via modernized PO OData V4 API
   - Write to BOTH old and new persistency simultaneously
   - Model CDS views on top of new persistency
   - POC in DDCI — does NOT disturb 2702 development landscape
   - Effort also needed from MEPO (Maple) rules side for modelling

### CE2708 Plan (Full Implementation)
- Plug notes into modernized PO OData V4 API (full, not just POC)
- Regression tests for all linked business objects
- Include other teams whose business objects use EKKO/EKPO text objects
- SDM migration reports execution
- Cut-off from old tables once SDM complete

---

## 7. Key Architecture Decisions Made / Agreed

| Decision | Status |
|---|---|
| Write to BOTH old and new persistency simultaneously during transition | Agreed — same as Sales pattern |
| Notes NOT in scope for CE2702 MBS (Minimum Business Scope) | Confirmed |
| Notes MUST be in CE2708 | Confirmed |
| POC in DDCI for 2702 — does not affect main development | Agreed |
| Lift & Shift team takes analysis ownership for 2702 | Agreed |
| No architecture decision without informed sign-off from all teams | Agreed |

---

## 8. Architecture Decision Still Open

**THE KEY OPEN DECISION:** Which persistency approach to use?

```
Option A: Generic table SGBT_NTCEONT (Basis/BCSRV)
  PRO:  Reuses existing infrastructure, no table to maintain
  PRO:  Already works with Notes Reuse RAP component
  CON:  Less flexible, no PO-specific attributes
  CON:  CDS views owned by Basis — not by PO team

Option B: Application-specific own table (Sales approach)
  PRO:  Full control, PO-specific attributes possible
  PRO:  Better performance, better for AI/BDC
  PRO:  SAP Script X team recommends this for all LOBs
  CON:  Own table to maintain
  CON:  UNKNOWN: compatible with Notes Reuse RAP component?

Rajesh's current leaning: Option B (own table like Sales)
  → "I'm tending towards how sales did it"
  → BUT: "open mind, talk to Notes Reuse first"

Christoph's view:
  → Keep door open for both
  → Check if Notes Reuse has improved since Sales evaluated
  → Make informed decision together
```

---

## 9. Relationship to ZPO_LONGTEXT Current Implementation

The `ZPO_LONGTEXT` table being developed by the Lift & Shift team is currently following
**Option B (application-specific own table)** — which is consistent with what Sales did and
what SAP Script X team recommends.

However the key question — whether this approach is compatible with the **Notes Reuse RAP
Business Object** — is still open. If the decision is to use the generic table (`SGBT_NTCEONT`),
then `ZPO_LONGTEXT` would be replaced by that generic table.

The **dual-write approach** (BAdI `ME_PROCESS_PO_CUST` writing to both STXH/STXL and the
new persistency) is correct regardless of which table is chosen — this pattern is confirmed
by the Sales team experience.

---

## 10. Contact Summary for Follow-Up

| Action | Contact | Purpose |
|---|---|---|
| Sync with Notes Reuse RAP team | TBD — not yet confirmed | Can own table be used? Has approach improved? |
| Sync with SAP Script X team | TBD — not yet confirmed | Confirm own-table guideline, migration at TDID level |
| Sync with Sales team | Chris, Karen Fang | Referencing approach, lessons learned from migration |
| Sync with Basis/BCSRV | BC team | CDS view exposure, SGBT_NTCEONT capabilities |
| Sync with Procurement Notes Reuse team | BLR S4 team | Keep in loop for architecture decisions |
| MEPO/Maple team | Nils + Maple team | Notes modelling in OData V4 API for POC |
