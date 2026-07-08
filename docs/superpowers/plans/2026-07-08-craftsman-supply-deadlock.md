# Craftsman Supply Deadlock Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:executing-plans. Single task.

**Goal:** Trade-supplied craftsmen get seated: transit cargo counts as supply, idle experts create transport demand, stockpile horizon 10 -> 5.
**Spec:** `docs/superpowers/specs/2026-07-08-craftsman-supply-deadlock-design.md`

### Task 1

**Files:** `Project Files/DLLSources/CvCityAI.cpp` (`AI_sustainedInputAvailable`), `Project Files/DLLSources/CvCity.cpp` (`getAutomationTransportDemand`), `Assets/XML/GlobalDefinesAlt.xml` (value 10 -> 5). All normalized already.

- [ ] **Step 1:** In `AI_sustainedInputAvailable`, change the return to amortize stored + in-transit cargo:

```cpp
	const int iHorizon = getAutomationDefine("AUTOMATION_STOCKPILE_HORIZON", 5);
	return iNet + (getYieldStored(eYield) + AI_getTransitYield(eYield)) / iHorizon;
```

- [ ] **Step 2:** In `CvCity::getAutomationTransportDemand`, replace the early-return on zero consumption with a potential-demand scan (idle expert whose specialty consumes the yield, building usable):

```cpp
	int iConsumed = getRawYieldConsumed(eYield);
	if (iConsumed <= 0)
	{
		// Potential demand: an idle expert whose specialty consumes this yield
		// and whose building is usable. Stocking the city before the expert
		// works lets the citizen automation seat them - breaks the deadlock
		// where no consumption means no deliveries means no consumption.
		for (uint i = 0; i < m_aPopulationUnits.size(); ++i)
		{
			CvUnit* const pUnit = m_aPopulationUnits[i];
			if (pUnit == NULL)
			{
				continue;
			}
			const ProfessionTypes eIdeal = pUnit->AI_getIdealProfession();
			if (eIdeal == NO_PROFESSION || pUnit->getProfession() == eIdeal)
			{
				continue;
			}
			const CvProfessionInfo& kIdeal = GC.getProfessionInfo(eIdeal);
			bool bConsumesYield = false;
			for (int j = 0; j < kIdeal.getNumYieldsConsumed(); ++j)
			{
				if ((YieldTypes)kIdeal.getYieldsConsumed(j) == eYield)
				{
					bConsumesYield = true;
					break;
				}
			}
			if (bConsumesYield && getProfessionOutput(eIdeal, pUnit) > 0)
			{
				iConsumed = getProfessionInput(eIdeal, pUnit);
				break;
			}
		}
		if (iConsumed <= 0)
		{
			return 0;
		}
	}
```

(The remainder of the function - buffer projection and import-limit clamp - is unchanged and now uses the actual-or-potential `iConsumed`.)

- [ ] **Step 3:** XML: `AUTOMATION_STOCKPILE_HORIZON` value 10 -> 5.
- [ ] **Step 4:** `tools/build.sh Assert` (EXIT 0), commit `"Automation: break craftsman supply deadlock (transit supply, idle-expert demand, softer horizon)"`, `tools/deploy.sh`, restore logging=1 in installed XML.
- [ ] **Step 5 (Steve):** spec tests 2-4.

Self-review: all three spec changes have steps; call-site gating claims verified (AI_sustainedInputAvailable only called under bHumanAutomation; getAutomationTransportDemand only from human-gated sites); `getAutomationTransportDemand` keeps its original variable names so the tail of the function needs no edits.
