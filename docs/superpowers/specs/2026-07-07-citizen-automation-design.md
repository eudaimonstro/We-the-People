# Citizen Automation Fix - Design

**Date:** 2026-07-07
**Target:** We the People 4.2.1 (branch `automation-fix`, based on commit `8f7c5f4b`, content-identical to the installed 4.2.1 release)
**Goal:** Make the existing "automate this citizen" feature pick sensible work slots, so a player can leave citizens automated without the city misbehaving.

## Problem

Automated (non-locked) citizens are assigned by `CvCityAI::AI_assignWorkingPlots()` (CvCityAI.cpp:161), which greedily places each citizen via `AI_parallelAssignToBestJob` and then runs a pairwise swap pass (`AI_juggleColonist`). The live scoring function is `AI_citizenProfessionValue` (CvCityAI.cpp:3840). Confirmed defects:

1. **No starvation guard.** Food is scored as a plain commodity (XML base value 5). The old starvation-aware scorer (`AI_plotValue` / `AI_yieldValue(EnumMap)`) is dead code - its only caller `AI_juggleCitizens` returns immediately (CvCityAI.cpp:3169).
2. **Production chains scored on instantaneous, stockpile-polluted state.** The input guard (CvCityAI.cpp:3905-3912) treats `rawProduced + stored <= 0` as the only disqualifier, so one stored unit of sugar makes a distiller look fully employable. Values also mutate mid-pass as workers are cleared/placed, making scores order-dependent.
3. **No expert-specialty preference.** Expertise enters only through raw output size. `AI_getIdealProfession()` affects pool ordering, never the score, so expert/generalist arrangements score as near-ties and settle wrong.
4. **Churn.** Every "assign work dirty" event re-pools all unlocked citizens; displacement needs only a strictly-higher score and swaps need only sum-improvement > 0, so assignments oscillate.

The scorer has no `isHuman()` branch: human and AI cities share it. Human cities are re-optimized through a human-only path (`CvGameAI::AI_updateAssignWork`, CvGameAI.cpp:62 -> `CvCityAI::AI_updateAssignWork`, CvCityAI.cpp:363).

## Approach (chosen)

Surgical fix of the existing scorer and placement rules. Every behavioral change is gated on the city owner being human (`GET_PLAYER(getOwnerINLINE()).isHuman()`), so AI opponents' colony management is behaviorally unchanged. The alternative - a separate human-only assignment algorithm - was rejected as a much larger implementation that would need to re-handle edge cases (natives, slot limits, legality, displacement) the existing machinery already covers.

Out of scope (possible follow-ups): wiring the Emphasize buttons into the scorer; any change to AI players; UI changes.

## Changes

All in `Project Files/DLLSources/`, primarily `CvCityAI.cpp`.

### 1. Starvation guard

In `AI_citizenProfessionValue`, for human-owned cities:

- Compute the city's net food per turn (`getYieldRate(YIELD_FOOD)` minus consumption) as seen at scoring time, and the stored food.
- If net food is negative and stored food is below `deficit * AUTOMATION_FOOD_RESERVE_TURNS` (default 8), add an emergency bonus to food-producing candidate jobs, proportional to the shortfall and large enough to dominate cash-crop values until the deficit is covered.
- Boost food jobs rather than zeroing non-food jobs: a zero score in this path leads to ejection from the city (CvCityAI.cpp:332-360).

The greedy loop is self-correcting: once enough food workers are placed, the deficit disappears and the bonus fades for subsequent placements.

### 2. Sustained-input accounting for craftsmen

In the input-availability logic of `AI_citizenProfessionValue` (steps at CvCityAI.cpp:3905-3912 and 3961-3983), for human-owned cities:

- Usable input per turn for a consumed yield = max(0, net ongoing production) + stored / `AUTOMATION_STOCKPILE_HORIZON` (default 10 turns, integer math).
- Disqualify (score 0) when that usable-input figure is 0. This single rule replaces the old `rawProduced + stored <= 0` guard for human cities: a stale 1-5 unit stockpile no longer qualifies a craftsman, while a real stockpile or ongoing production does.
- The output-scaling fraction (`useInput / iYieldInput`) uses this sustained figure instead of the instantaneous one.

### 3. Expert-specialty bonus

In `AI_citizenProfessionValue`, for human-owned cities: if `kUnit.AI_getIdealProfession() == eProfession`, multiply the final value by `100 + AUTOMATION_EXPERT_BONUS_PERCENT` (default 50) / 100. This creates a decisive margin so the swap pass reliably seats experts in their specialty and moves generalists out.

### 4. Stickiness (anti-churn)

For human-owned cities:

- **Retention bonus:** capture each citizen's pre-pass assignment (profession + plot) in `AI_assignWorkingPlots` before plots are cleared; when the scorer evaluates that same job for that unit, multiply by `100 + AUTOMATION_STICKINESS_PERCENT` (default 10) / 100.
- **Displacement margin:** a challenger must beat an employed incumbent's score by the same percentage margin, not merely exceed it (AI_findBestJob / FindBestJob displacement checks, CvCityAI.cpp:3300-3313, 3332-3346).
- **Swap threshold:** `AI_juggleColonist` (CvCityAI.cpp:3715) executes a swap only if the summed improvement exceeds a threshold derived from the same constant, instead of > 0.

**Invariant caution:** `AI_parallelAssignToBestJob` contains `while(true)` spin-loops (CvCityAI.cpp:3499-3503, 3523-3527) that hang the game if a placed newcomer does not actually outscore the displaced worker. Every margin change must be applied consistently on both the selection side and the verification side of that invariant. This is a mandatory line-by-line review item during implementation and gets a dedicated test.

## Tuning constants

Read via `GC.getDefineINT()` from `Assets/XML/GlobalDefinesAlt.xml`, each with an in-code default so a missing entry is harmless:

| Define | Default | Meaning |
|---|---|---|
| `AUTOMATION_FOOD_RESERVE_TURNS` | 8 | Stored-food buffer (in turns of deficit) before the emergency food bonus kicks in |
| `AUTOMATION_STOCKPILE_HORIZON` | 10 | Turns over which a stored input stockpile is amortized into per-turn supply |
| `AUTOMATION_EXPERT_BONUS_PERCENT` | 50 | Score bonus for an expert working their specialty |
| `AUTOMATION_STICKINESS_PERCENT` | 10 | Retention bonus / displacement + swap margin |
| `AUTOMATION_KEEP_THRESHOLD_PERCENT` | 120 | Overpopulation: after a pass settles, an unlocked citizen whose job value is below (value of the food they eat x this percent) is ejected from the city as a map unit, via the existing NO_PROFESSION cleanup. Locked citizens and the last citizen are never ejected. Added 2026-07-07 after playtesting showed overpopulated cities kept net-negative workers in marginal slots. |
| `AUTOMATION_JOIN_THRESHOLD_PERCENT` | 150 | Garrison recruitment: the automate-all button also evaluates idle default-profession units standing on the city tile and joins them to the city when their best available job value is at least (value of the food they eat x this percent). Deliberately higher than the keep threshold so units do not flap in and out. Soldiers/scouts/etc. (non-default professions) are never recruited. Uses CvUnit::joinCity, so food-starvation and movement legality match the manual join button. Added 2026-07-07 per playtest feedback. |

Editing the XML and relaunching the game re-tunes behavior without recompiling.

## Diagnostics

A logging switch (`AUTOMATION_LOGGING`, default 0, same XML file). When enabled, each human-city assignment pass appends to a file in the game's Logs directory: city name, per-citizen chosen profession/plot with score, runner-up score, and which bonus/guard terms fired. Used to verify behavior against the four defects; costs nothing when disabled.

## Build & deploy

- Toolchain: WTP's official `Compiler` repo (pinned MSVC toolkit + Platform SDK), driven by the repo's `nmake` Makefile, run under Wine (installed). First milestone is a **stock** build that proves the toolchain before any source edits.
- Deploy script: back up the installed mod's `Assets/CvGameCoreDLL.dll` (once), then copy the freshly built DLL and the edited `GlobalDefinesAlt.xml` into the installed mod at `.../Mods/WeThePeople-4.2.1/`.
- **Savegame compatibility:** no new persistent fields, so existing saves load with the new DLL and saves made under it still load with the stock DLL. Worst-case rollback = restore the backed-up DLL/XML.

## Testing

1. **Toolchain sanity:** stock sources compile and the game runs with the self-built DLL.
2. **Unit-of-behavior checks** (with logging on, using a real save in a problem city):
   - Automate all citizens in a food-negative city: food jobs get staffed first; no starvation next turns.
   - City with a craftsman building and no ongoing input production and near-empty stores: craftsman job not chosen.
   - City with an idle expert and a generalist occupying the expert's slot: after one pass, expert holds the slot.
   - End 5+ turns with no city changes: zero reassignments logged.
3. **Hang guard:** extended play session (and end-turn spam) with no spin-loop hang; assert/logging confirms the displacement invariant holds with margins active.
4. **AI regression:** AI opponents' cities show unchanged assignments for identical game states (the gate keeps their path untouched); sanity-check by observing a few AI cities in WorldBuilder before/after.

## Risks

- **Wine build breakage:** the WTP toolchain is Windows-native (nmake + perl wrapper). Mitigation: milestone 0 proves the build before any code changes; if Wine fails, fall back to a Windows VM or ask WTP's CI to build.
- **Spin-loop hang:** covered above; mitigated by consistent margins plus a dedicated test.
- **Score-scale interactions:** bonuses are multiplicative on an opaque money-scale value; defaults may need tuning. Mitigated by XML knobs and the decision log.
