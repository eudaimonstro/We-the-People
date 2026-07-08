# Pioneer Automation Forest Protection - Design

**Date:** 2026-07-08
**Target:** WTP 4.2.1, branch `automation-fix`
**Goal:** Automated pioneers stop silently destroying forests the player wanted kept: honor the "Leave Forests" option everywhere, and never chop a feature out from under a working citizen.

## Problem (from 2026-07-08 code audit)

1. `PLAYEROPTION_LEAVE_FORESTS` is consulted only in `AI_fortTerritory` (CvUnitAI.cpp:17188). The main automated build path - `CvCityAI::AI_bestPlotBuild` (CvCityAI.cpp:5741), which fills the per-plot best-build cache that `AI_improveCity`/`AI_bestCityBuild` execute - never checks it. A player who enables the option and automates a pioneer still gets forests chopped.
2. A worked-but-unimproved forest can be selected for a feature-removing build whenever the post-clear improvement out-scores the forest's yields (`AI_plotYieldValue` gives worked plots only a 2x nudge). This destroys a lumberjack's job and the city's lumber supply. Author comment `//XXX update this once chops are saner` (CvCityAI.cpp:~6190 current tree) acknowledges the roughness.

## Design

One insertion in `AI_bestPlotBuild`'s candidate-build loop, immediately after `bRemoveFeature` is computed (current tree CvCityAI.cpp:5905-5909), applying only when the build would remove the plot's feature AND the owner is human:

1. **Leave Forests:** if `GET_PLAYER(getOwnerINLINE()).isOption(PLAYEROPTION_LEAVE_FORESTS)`, skip the build - exactly the semantics `AI_fortTerritory` already uses (any feature, any removing build).
2. **Worked-feature guard:** if the plot `isBeingWorked()`, find the working unit (`getWorkingCity()->getUnitWorkingPlot(pPlot)`); for each yield its profession produces, compare `pPlot->getYieldWithBuild(eBuild, y, true)` against `pPlot->getYield(y)`. If the build would lower any of them, skip the build. This is a "never make a worked plot worse for its worker" rule: it protects a lumberjack's forest (clearing drops lumber to zero) while still allowing upgrades that help the worker (better farm on a worked farm plot, added roads).

No knobs needed - rule 1 is controlled by the existing in-game option, rule 2 is unconditional protection. AI players unchanged (both rules inside `isHuman()`); no state; savegame-safe; deterministic.

Downstream note: `AI_betterPlotBuild` (CvUnitAI.cpp:17286) can only swap feature-clear builds when the base build already clears; with clears filtered upstream for protected plots, no change needed there. Verified during implementation.

## Testing

1. Assert build clean.
2. Leave Forests on + automated pioneer + forested city radius: no chop builds occur; pioneer improves non-forest plots.
3. Option off, lumberjack working an unimproved forest: pioneer does not clear that plot; may still improve it in ways that keep lumber intact.
4. Option off, unworked forest plot where a farm scores higher: chopping still allowed (vanilla behavior preserved for unworked plots).
5. AI regression: AI pioneers unchanged.
