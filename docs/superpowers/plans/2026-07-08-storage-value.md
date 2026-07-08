# Storage-Pressure Warehouse Value Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:executing-plans. Single task.

**Goal:** Scale the warehouse term of `AI_buildingValue` by real storage pressure, human cities only.
**Spec:** `docs/superpowers/specs/2026-07-08-storage-value-design.md`

### Task 1: Rescale the storage block

**Files:** `Project Files/DLLSources/CvCityAI.cpp` (block at :1278-1310), `Assets/XML/GlobalDefinesAlt.xml` (one define). Both files already line-ending-normalized.

- [ ] **Step 1:** Restructure the three storage terms into `iStorageValue`; for human owners scale by `pressurePct = clamp01(max(percentFull, 100*HORIZON/max(HORIZON, turnsToFull)))` where `turnsToFull = freeSpace / max(1, netInflow)` and `netInflow` sums `max(0, rawProduced - rawConsumed)` over cargo yields excluding `YIELD_FOOD` (food fills the growth pool, not the warehouse). AI path arithmetic unchanged. Port x2 stays after, unchanged. Full code in the spec + this edit.
- [ ] **Step 2:** Add `AUTOMATION_STORAGE_PRESSURE_TURNS` = 20 to GlobalDefinesAlt.xml after `AUTOMATION_BUILD_MATERIAL_HORIZON`.
- [ ] **Step 3:** `tools/build.sh Assert` (EXIT 0), `xmllint --noout`, commit "Automation: warehouse value scales with real storage pressure", `tools/deploy.sh`, restore `AUTOMATION_LOGGING=1` in installed XML.
- [ ] **Step 4 (Steve):** low-goods city -> warehouse not recommended; full/high-throughput city -> still recommended.

Self-review: spec covered (formula, knob, gate, food exclusion documented in code comment); no placeholders; names consistent.
