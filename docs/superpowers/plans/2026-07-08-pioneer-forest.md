# Pioneer Forest Protection Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:executing-plans. Single task.

**Goal:** Automated builds honor Leave Forests and never chop a worked plot's feature when that hurts its worker. Human-only.
**Spec:** `docs/superpowers/specs/2026-07-08-pioneer-forest-design.md`

### Task 1: Guard block in AI_bestPlotBuild

**Files:** `Project Files/DLLSources/CvCityAI.cpp` only (already normalized). APIs verified: `CvCity::getUnitWorkingPlot(const CvPlot*)` (CvCity.h:444), `CvPlot::getYieldWithBuild(BuildTypes, YieldTypes, bool)` (CvPlot.h:435), `PLAYEROPTION_LEAVE_FORESTS` usage pattern (CvUnitAI.cpp:17188).

- [ ] **Step 1:** In `AI_bestPlotBuild` (CvCityAI.cpp:5741), inside the candidate loop's `if (bValid)` block, directly after `bRemoveFeature` is computed (:5905-5909), insert:

```cpp
			// Automation fix (human players only): forest protection for
			// automated builds.
			if (bRemoveFeature && GET_PLAYER(getOwnerINLINE()).isHuman())
			{
				// (a) The "Leave Forests" player option previously applied only
				// to fort placement; honor it for every automated build.
				if (GET_PLAYER(getOwnerINLINE()).isOption(PLAYEROPTION_LEAVE_FORESTS))
				{
					continue;
				}
				// (b) Never remove a feature out from under a citizen working
				// this plot when that would reduce the yield they harvest
				// (protects lumberjacks' forests; still allows upgrades that
				// keep the worker's yield intact).
				if (pPlot->isBeingWorked())
				{
					CvCity* const pWorkingCity = pPlot->getWorkingCity();
					CvUnit* const pWorkingUnit = (pWorkingCity != NULL) ? pWorkingCity->getUnitWorkingPlot(pPlot) : NULL;
					if (pWorkingUnit != NULL && pWorkingUnit->getProfession() != NO_PROFESSION)
					{
						const CvProfessionInfo& kWorkedProf = GC.getProfessionInfo(pWorkingUnit->getProfession());
						bool bHarmsWorker = false;
						for (int iP = 0; iP < kWorkedProf.getNumYieldsProduced() && !bHarmsWorker; ++iP)
						{
							const YieldTypes eWorkedYield = (YieldTypes)kWorkedProf.getYieldsProduced(iP);
							if (eWorkedYield != NO_YIELD
								&& pPlot->getYieldWithBuild(eBuild, eWorkedYield, true) < pPlot->getYield(eWorkedYield))
							{
								bHarmsWorker = true;
							}
						}
						if (bHarmsWorker)
						{
							continue;
						}
					}
				}
			}
```

(`continue` advances the enclosing build loop; the pattern is safe here because the insertion point is before any value bookkeeping for the candidate.)

- [ ] **Step 2:** `tools/build.sh Assert` (EXIT 0); commit `"Automation: automated pioneers honor Leave Forests and spare worked features"`; `tools/deploy.sh`; restore `AUTOMATION_LOGGING=1` in the installed XML.
- [ ] **Step 3 (Steve):** spec's tests 2-4 in-game.

Self-review: both spec rules implemented in one block at the specified site; downstream `AI_betterPlotBuild` note verified during implementation (its clear-swap only fires when the chosen build already clears); no placeholders; API names match verified headers.
