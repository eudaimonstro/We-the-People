# Material-Aware Building Recommendations - Design

**Date:** 2026-07-08
**Target:** We the People 4.2.1, branch `automation-fix` (builds on citizen + transport automation work: same toolchain, knob pattern, human-only gating)
**Goal:** The production popup's "Recommended" building must be one the city can realistically finish: its material bill (tools/stone/clay etc.) must be obtainable soon - from local stock, local production, or surplus sitting in the player's other colonies.

## Problem

The popup (`CvDLLButtonPopup::launchProductionPopup`, CvDLLButtonPopup.cpp:1776) highlights exactly one building chosen by `pCity->AI_bestBuilding(0, 50, true)` (:1929; the Python recommendation hooks are stubs). The scorer chain `AI_bestBuilding` -> `AI_bestBuildingThreshold` (CvCityAI.cpp:941/974) -> `AI_buildingValue` (:1246) is materials-blind:

- `AI_buildingValue` scores only what a building produces/enables; `getYieldCost` appears solely under `BUILDINGFOCUS_BUILD_ANYTHING`, a flag the popup call never sets.
- `canConstruct` (CvCity.cpp:1609) has no material check.
- The "within 50 turns" gate uses `getProductionTurnsLeft` (CvCity.cpp:2347), which is hammers-only (:2363, :2481) - a 20-hammer/200-tool building reports the same turns as a 20-hammer one.
- The single materials guard (`AI_bestBuildingThreshold` :996-1000) skips a candidate only when hammers are already fully accumulated and materials are missing, i.e. after the player has already sunk the hammers and the build has stalled (stall mechanics: `popOrder` -> `processRequiredYields` -> `checkRequiredYields`, CvCity.cpp:6648/6945/6847).

## Approach (chosen)

Affordability gate inside `AI_bestBuildingThreshold`'s candidate loop, human-gated. Rejected: making `getProductionTurnsLeft` material-aware (ripples into every UI turn display) and popup-only annotation (doesn't move the recommendation).

## Design

### Gate

In `AI_bestBuildingThreshold` (CvCityAI.cpp:974), in the candidate loop after the `canConstruct` check (:989) and before scoring, when `GET_PLAYER(getOwnerINLINE()).isHuman()`:

For each yield the building costs (`getYieldProductionNeeded(eLoopBuilding, eYield)` > 0, cargo yields only, excluding `YIELD_HAMMERS` which the existing turns gate covers), require:

```
needed - alreadyRushed
  <= cityStored(eYield)
   + max(0, cityNetProduction(eYield)) * AUTOMATION_BUILD_MATERIAL_HORIZON
   + sum over the player's OTHER cities of max(0, stored - autoMaintainThreshold)
```

- `cityStored` counts what is on hand; `getYieldRushed` credit mirrors `checkRequiredYields` (CvCity.cpp:6847).
- Local production term uses `getRawYieldProduced - getRawYieldConsumed` (net ongoing flow), floored at 0.
- The remote term is the exportable-surplus notion the transport system uses (stored above `getAutoMaintainThreshold`) - exactly the goods automated wagons can deliver. All of the player's cities count (no connectivity test: coastal + land transport reach everything in practice; over-optimism here only re-admits a borderline candidate, it never blocks a good one).
- If any costed yield fails, `continue` past the candidate. Manual construction is unaffected - the building still appears in the popup list, it just is not the starred recommendation.

Helper: `bool CvCityAI::AI_isBuildingAffordable(BuildingTypes eBuilding) const` in CvCityAI.cpp, so the gate is one readable call.

### Scope of effect

`AI_bestBuilding` serves: the human popup recommendation, the human "automate production" checkbox path (`doProduction` -> AI pick for `isProductionAutomated()` human cities), and AI players' choices. The `isHuman()` gate inside the helper means the first two get the fix and AI players are byte-identical. Both human paths improving is intended: automated production stops queueing stall-bound buildings for the same reason the star stops pointing at them.

### Knob

| Define | Default | Meaning |
|---|---|---|
| `AUTOMATION_BUILD_MATERIAL_HORIZON` | 15 | Turns of the city's own net production counted toward "obtainable soon" |

Same `GlobalDefinesAlt.xml` + `getAutomationDefine` pattern; no rebuild to tune.

### Out of scope

Europe purchases as a supply source (gold decisions belong to the player); changes to turn-count displays; AI build planning; multi-recommendation UI.

### Safety

Human-gated, no persistent state, savegame-compatible both directions, deterministic (city stores/production/thresholds only). The helper runs per candidate building over the player's city list - trivial cost next to `AI_buildingValue`'s existing work, and only on popup/automation evaluation, not per-turn-per-plot.

## Testing

1. Assert build compiles clean; play on Assert build.
2. City with hammers but no tools production, empty tool stores empire-wide: recommendation shifts away from tool-heavy buildings to an affordable one.
3. Stockpile 200 tools in another colony: tool-heavy building may return as recommended (remote surplus counts).
4. City already stalled on a building (hammers sunk, materials missing): existing behavior preserved (that guard already existed); recommendation does not point at another unaffordable building.
5. AI regression: AI cities' build choices unchanged (gate inside isHuman()).
