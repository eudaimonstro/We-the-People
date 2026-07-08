# Craftsman Supply Deadlock Fix - Design

**Date:** 2026-07-08
**Target:** WTP 4.2.1, branch `automation-fix`
**Goal:** Break the deadlock where an expert craftsman (e.g. Master Sail Maker) is never assigned to their specialty because the input arrives by trade rather than local production, and the transport system never delivers the input because nobody is consuming it.

## Problem (playtest report 2026-07-08)

A Master Sail Maker with ample stored hemp keeps getting assigned to mine raw materials. Cause is an interaction of two earlier automation changes:

1. `AI_sustainedInputAvailable` (CvCityAI.cpp, citizen work Task 3/4) counts only local net production plus `stored / AUTOMATION_STOCKPILE_HORIZON` (default 10). A trade-supplied city has zero local flow, so even a healthy stockpile (30-60) yields a low per-turn figure; the sail job's output is capped accordingly and loses to raw-yield plots despite the expert bonus.
2. `CvCity::getAutomationTransportDemand` (transport work Task 3) signals input demand only when `getRawYieldConsumed(eYield) > 0` - i.e. only when a craftsman is already working. Idle craftsman -> no demand -> wagons do not deliver -> supply never appears -> craftsman stays idle. Deadlock.

## Design (three coordinated changes, all human-gated by construction)

1. **Count inbound cargo as supply.** In `AI_sustainedInputAvailable`, amortize `getYieldStored(eYield) + AI_getTransitYield(eYield)` over the horizon instead of stored alone. `AI_getTransitYield` (virtual on CvCity, CvCity.h:734) is the same in-flight-cargo measure the unload scorer already uses - wagons en route count as supply, closing the timing gap between delivery cycles.

2. **Potential demand from idle experts.** In `CvCity::getAutomationTransportDemand`, when actual consumption of `eYield` is zero, scan the city's population for a unit whose `AI_getIdealProfession()` consumes `eYield` and for which `getProfessionOutput(eIdealProfession, pUnit) > 0` (the building exists and has capacity). If found, treat the profession's per-worker input (`getProfessionInput(eIdealProfession, pUnit)`) as the consumption rate and compute the buffer-horizon demand from it. Wagons then stock the city for the expert before they start working - which flips the citizen scorer's supply check positive, which seats the expert, which creates real consumption. The circle becomes virtuous.

3. **Soften the stockpile horizon.** Default `AUTOMATION_STOCKPILE_HORIZON` drops from 10 to 5 (XML and both in-code defaults): a stockpile covering 5 turns of full consumption now sustains full output value. The original 10 was over-conservative for trade-supplied cities; the guard's real job (reject craftsmen with a token 1-5 leftover units) still holds at 5.

No new knobs; no new state; savegame-safe; deterministic. AI players: change 1 and 3 live inside functions only called on human-gated paths (`AI_sustainedInputAvailable` is called only under `bHumanAutomation`); change 2 is called from `AI_tradeRoutes` virtual-route synthesis (human FULL mode only) and `AI_transferYieldValue`'s feeding boost (gated `isHuman()`) - verified call sites, AI unaffected.

## Addendum (2026-07-08, playtest: grapes-to-wine)

The expert-only input-cost discount left GENERALIST craftsmen with the full structural bias: a citizen evaluating winemaking pays full market price for grapes while plot jobs bank pure revenue, so nobody converts an abundant stockpile. Fix: input charge scales with local scarcity - 100% of market price when the stockpile is thin (protects supply chains from premature processing), sliding linearly to 25% once stored input covers `AUTOMATION_INPUT_ABUNDANCE_TURNS` (default 15) of the profession's consumption. The scarcest input governs multi-input professions. The expert-specialty discount (`AUTOMATION_EXPERT_INPUT_COST_PERCENT`) now multiplies on top of the abundance charge instead of replacing it.

## Addendum (2026-07-08, playtest: automate-all oscillation)

The congestion surcharge on the KEEP (ejection) bar created a self-driving feedback loop: a strained city ejected marginal workers at a high bar, which relieved the strain, which dropped the bar, which let recruitment re-add them, which restored the strain. The fixed-point loop could not damp it because ejection also runs in per-turn `AI_assignWorkingPlots` passes, outside the automate cycle. Fix: strain gates only RECRUITMENT (join bar = food upkeep + congestion surcharge), never ejection (keep bar = food upkeep only, strain-independent and stable across a cycle's population changes). Result: a miserable city stops growing (won't recruit) but does not shed the workers it already has for strain alone, so repeated automate-all clicks converge. Tradeoff: automation no longer actively shrinks an already-overgrown miserable city (that would require a proper population-equilibrium search); it prevents growth into misery, which was the original request.

## Testing

1. Assert build clean.
2. Steve's save: automate-all in the Sail Maker's city (with hemp stored or wagons running): the Sail Maker takes the sail-making job.
3. Deadlock-from-zero: city with idle expert, empty stores, hemp surplus in another colony, automated wagon: wagon delivers hemp (log tag [F]), then the next citizen pass seats the expert.
4. Guard still works: craftsman job with no ongoing supply and 3 stored units still scores 0.
