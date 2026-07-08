# Material-Aware Building Recommendations Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** The production popup's "Recommended" building (and the automate-production pick) must have an obtainable material bill for human cities.

**Architecture:** One helper `CvCityAI::AI_isBuildingAffordable` + one human-gated `continue` in `AI_bestBuildingThreshold`'s candidate loop + one XML knob. AI players byte-identical.

**Tech Stack:** Same toolchain and patterns as the citizen/transport work (`tools/build.sh`, `getAutomationDefine`, Assert-then-Release).

**Spec:** `docs/superpowers/specs/2026-07-08-building-recommendation-design.md`

**Key code:** `AI_bestBuildingThreshold` candidate loop (CvCityAI.cpp:974-1043, current tree); gate goes after the stalled-build guard (:996-1000). APIs verified: `getYieldStored/getYieldRushed` (CvCity.h:387/390), `getRawYieldProduced/Consumed`, `getAutoMaintainThreshold`, `getYieldProductionNeeded(BuildingTypes, YieldTypes)`, `GC.getYieldInfo(y).isCargo()`, `firstCity/nextCity` iterators. CvCityAI.cpp and CvCityAI.h already line-ending-normalized.

---

### Task 1: Helper + gate + knob

**Files:**
- Modify: `Project Files/DLLSources/CvCityAI.h` (declaration next to the automation block ~line 100)
- Modify: `Project Files/DLLSources/CvCityAI.cpp` (helper impl + gate in AI_bestBuildingThreshold)
- Modify: `Assets/XML/GlobalDefinesAlt.xml` (one define)

- [ ] **Step 1: Declare in CvCityAI.h** (in the automation block added by earlier work):

```cpp
	bool AI_isBuildingAffordable(BuildingTypes eBuilding) const;
```

- [ ] **Step 2: Implement in CvCityAI.cpp** (next to `AI_isHumanAutomationCity`):

```cpp
// Material-aware recommendation gate: can this city plausibly cover the
// building's non-hammer material bill soon? Local stock, local net production
// over a horizon, and exportable surplus in the player's other cities count -
// the same supply the automated transports can actually deliver. Hammers are
// excluded: the existing turns-left gate already covers them.
bool CvCityAI::AI_isBuildingAffordable(BuildingTypes eBuilding) const
{
	const int iHorizon = getAutomationDefine("AUTOMATION_BUILD_MATERIAL_HORIZON", 15);
	const CvPlayer& kOwner = GET_PLAYER(getOwnerINLINE());

	for (int iYield = 0; iYield < NUM_YIELD_TYPES; ++iYield)
	{
		const YieldTypes eYield = (YieldTypes)iYield;
		if (eYield == YIELD_HAMMERS || !GC.getYieldInfo(eYield).isCargo())
		{
			continue;
		}
		const int iNeeded = getYieldProductionNeeded(eBuilding, eYield) - getYieldRushed(eYield);
		if (iNeeded <= 0)
		{
			continue;
		}

		int iObtainable = getYieldStored(eYield);
		const int iNetProduction = getRawYieldProduced(eYield) - getRawYieldConsumed(eYield);
		if (iNetProduction > 0)
		{
			iObtainable += iNetProduction * iHorizon;
		}
		if (iObtainable < iNeeded)
		{
			// exportable surplus elsewhere in the empire
			int iCityLoop;
			for (CvCity* pLoopCity = kOwner.firstCity(&iCityLoop); pLoopCity != NULL; pLoopCity = kOwner.nextCity(&iCityLoop))
			{
				if (pLoopCity != this)
				{
					iObtainable += std::max(0, pLoopCity->getYieldStored(eYield) - pLoopCity->getAutoMaintainThreshold(eYield));
				}
			}
		}
		if (iObtainable < iNeeded)
		{
			return false;
		}
	}
	return true;
}
```

- [ ] **Step 3: Gate in AI_bestBuildingThreshold** - directly after the stalled-build guard (`... !checkRequiredYields(ORDER_CONSTRUCT, eLoopBuilding, YIELD_HAMMERS)) continue;`), add:

```cpp
					// Material-aware recommendation (human cities only): do not
					// recommend a building whose material bill is not obtainable
					// soon; it would just stall with hammers sunk. Manual
					// construction remains fully available.
					if (GET_PLAYER(getOwnerINLINE()).isHuman() && !AI_isBuildingAffordable(eLoopBuilding))
					{
						continue;
					}
```

- [ ] **Step 4: XML knob** - after `AUTOMATION_TRANSPORT_DISTANCE_TURNS` in `Assets/XML/GlobalDefinesAlt.xml`:

```xml
	<Define>
		<DefineName>AUTOMATION_BUILD_MATERIAL_HORIZON</DefineName>
		<iDefineIntVal>15</iDefineIntVal>
	</Define>
```

- [ ] **Step 5: Compile, validate XML, commit**

```bash
tools/build.sh Assert   # expect EXIT 0
xmllint --noout Assets/XML/GlobalDefinesAlt.xml
git add "Project Files/DLLSources/CvCityAI.h" "Project Files/DLLSources/CvCityAI.cpp" Assets/XML/GlobalDefinesAlt.xml
git commit -m "Automation: recommended buildings must have an obtainable material bill"
```

### Task 2: Deploy + verify

- [ ] **Step 1:** `tools/build.sh Assert && tools/deploy.sh` (logging already handled; this feature logs nothing).
- [ ] **Step 2 (Steve):** open production choice in a hammer-rich, tool-less city: recommendation avoids tool-heavy buildings. Stockpile the missing material in another colony: recommendation may return. AI turns process normally.
- [ ] **Step 3:** After verification: `tools/build.sh Release && tools/deploy.sh`, push branch.

## Self-review notes

- Spec coverage: gate + helper + knob + human-only + both human paths (popup, automate-production) = Task 1; testing = Task 2. Out-of-scope items untouched.
- The remote-surplus loop only runs when local supply falls short (cheap common case).
- `getYieldProductionNeeded(BuildingTypes, YieldTypes)` is the CvCity wrapper (includes cost mods) - same one `checkRequiredYields` uses, so the gate and the actual completion check agree.
- Placeholder scan: clean. Type consistency: helper name matches at declaration, definition, and call site.
