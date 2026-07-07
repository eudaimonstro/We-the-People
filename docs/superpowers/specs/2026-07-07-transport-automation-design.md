# Transport Automation Fix (Land + Domestic Sea) - Design

**Date:** 2026-07-07
**Target:** We the People 4.2.1, branch `automation-fix` (builds on the citizen automation work: same toolchain, deploy scripts, XML knob pattern, logging switch, and human-only gating discipline)
**Goal:** Make automated transports (wagon trains and coastal ships hauling between the player's own colonies) provide value with zero configuration: feed production chains, drain surpluses to the port, rescue goods before they rot - while the player's Domestic Advisor settings, where present, always win.

## Problem

The per-turn brain for all automated transports is `CvSelectionGroupAI::AI_tradeRoutes()` (CvSelectionGroupAI.cpp:909-1464), shared by land and sea, human-automated and AI-owned. Confirmed defects (file:line refs are to the 4.2.1 sources):

1. **Zero-config is zero-function.** A `CvTradeRoute` (source, dest, yield) only exists when the player flags the yield *export* in one city and *import* in another (`CvCity::addExport`/`addImport`, CvCity.cpp:12016/12161 auto-wire routes). No flags, no routes, nothing for automated wagons to do. Un-flagged surpluses decay every turn once storage exceeds capacity (CvCity.cpp:7431-7445); the "rescue nearby overflow" fallback exists only as an unimplemented comment (CvSelectionGroupAI.cpp:1079-1085).
2. **Distance is ignored for land wagons.** The turns-to-destination penalty is applied only to coastal transports (CvSelectionGroupAI.cpp:1243-1272). Land wagons pick far work over equal near work and make long, uncosted empty repositioning runs (empty runs are deliberate: comment at :1126-1129).
3. **Pickups are not de-conflicted.** Destination choice divides by transports already targeting the same plot (`AI_plotTargetMissionAIs`, :1241), but two empty wagons at different places both count the same source surplus and herd to it; the loser wastes its trip.
4. **Overflow urgency is a cliff.** Pickup value scales with total city storage and jumps ~2.25x at 90% total fullness (CvPlayerAI.cpp:9794-9815). A city at 89% gets no urgency; per-yield rot is invisible.

Human/AI split points already exist and are clean: `isHuman() || AUTOMATE_TRANSPORT_FULL` selects the all-routes branch (:952); human + `AUTOMATE_TRANSPORT_ROUTES` services only the group's manually assigned routes (:1003).

## Approach (chosen)

Virtual routes + scoring fixes, surgically inside `AI_tradeRoutes()` and its scoring helper `CvPlayerAI::AI_transferYieldValue` (CvPlayerAI.cpp:9753), gated on the group owner being human and the group being automated. Rejected alternatives: auto-configuring the Domestic Advisor via the AI's `AI_doTradeRoutes` (clobbers player settings, fixes no scoring defects) and a from-scratch player-level logistics planner (large, risky, replaces battle-tested movement code).

Mode semantics:
- **`AUTOMATE_TRANSPORT_FULL`** ("automate transport" button): configured routes + synthesized virtual routes. The zero-config smart mode.
- **`AUTOMATE_TRANSPORT_ROUTES`** (explicitly assigned routes): candidate set unchanged - the player's instructions - but scoring fixes apply.
- AI players: byte-identical behavior everywhere.

## Design

### 1. Virtual route synthesis (human + TRANSPORT_FULL only)

Each turn, when building the candidate route set, in addition to `kOwner.getTradeRoutes(...)`, synthesize ephemeral routes (stack-local objects, never added to the player's saved route list, never shown in UI) for each reachable pair of the player's cities (A, B) and each cargo yield Y:

**Supply(A, Y)** = `A->getYieldStored(Y) - A->getAutoMaintainThreshold(Y)`, if > 0. The auto-maintain threshold already folds in the player's maintain level and the city's build-queue needs, so virtual routes can never strip a city below what the player or its build queue requires. A city the player flagged as an importer of Y is never a virtual supplier of Y.

**Demand(B, Y)**, in priority order:
1. **Production feeding:** B consumes Y (`getRawYieldConsumed(Y) > 0`) faster than it produces it. Demand = `consumption x AUTOMATION_TRANSPORT_BUFFER_TURNS - (stored + netProduction x same horizon)`, if > 0.
2. **Player settings win:** if a real configured route (A, B, Y) exists, no virtual route is synthesized for that triple. Virtual deliveries respect `getMaxImportAmount` (import limits) and `isAutoImportStopped` (feeder satisfied) exactly like real ones - they flow through the same load/unload code paths.
3. **Port drain:** for Europe-sellable yields (`isYieldEuropeTradable`) with no reachable production demand, the inferred port city demands them up to warehouse headroom. Port = the existing `CvPlayerAI::AI_findBestPort` (CvPlayerAI.cpp:6023), already used as the wagon fallback destination. The port never virtually exports a yield it is draining, and A == port synthesizes nothing.

Reachability reuses the existing area checks for land (:988-998) and water-adjacency checks for coastal transports. No virtual Europe routes: domestic freight only (Europe/Africa/Port Royal runs are out of scope).

### 2. Scoring fixes (human automated, both modes)

1. **Land distance penalty:** apply the same turns-to-reach divisor to land wagons that coastal transports already get, in the destination-choice loop (:1219-1286). Empty repositioning runs must additionally clear a minimum value bar (`AUTOMATION_TRANSPORT_MIN_HAUL` converted to value) after the distance division, so wagons stop making long speculative empty runs.
2. **Continuous overflow urgency:** in `AI_transferYieldValue`'s loading branch (CvPlayerAI.cpp:9794-9815), for human cities replace the 90%-total-storage cliff with a continuous factor of total fullness, plus an explicit rot bonus when the city is past capacity and actively losing goods to decay.
3. **Pickup de-confliction:** when valuing a pickup at source S, subtract surplus already claimed by other automated transport groups of the same player whose current mission targets S, proportional to their free cargo capacity. Computed by scanning the player's selection groups' missions and cargo each evaluation - deterministic, derived entirely from existing state, nothing new saved.

### 3. Sea (domestic freight)

No sea-specific code: coastal transports run the same function and get virtual routes between water-connected colonies through the existing reachability checks, plus all scoring fixes. The existing human restrictions stay (no auto-hauling to allied cities, no auto-Europe).

### 4. Knobs

Same `GlobalDefinesAlt.xml` + `getAutomationDefine` pattern as the citizen work (in-code defaults, tune without rebuild):

| Define | Default | Meaning |
|---|---|---|
| `AUTOMATION_TRANSPORT_BUFFER_TURNS` | 10 | Production-feeding demand horizon: haul enough input to keep a consuming city's craftsmen running this many turns |
| `AUTOMATION_TRANSPORT_MIN_HAUL` | 10 | Minimum units of cargo that make a trip (or an empty repositioning run toward it) worthwhile |
| `AUTOMATION_TRANSPORT_DISTANCE_TURNS` | 2 | Free turns of travel before the distance divisor starts biting (matches the existing coastal tuning) |

Diagnostics reuse the existing `AUTOMATION_LOGGING` switch: per automated-transport turn, log chosen destination, cargo loaded/unloaded, and the demand class served (feed / player-setting / port / overflow rescue), plus the runner-up destination.

### 5. Safety

- **Gating:** every behavior change is behind `group owner isHuman() && group isAutomated()`. AI wagons and all AI economy code paths are untouched.
- **Savegame-safe both directions:** virtual routes are per-turn stack objects; no new persistent state. Saves made with this DLL load on stock and vice versa.
- **Determinism:** all new inputs (stored yields, thresholds, missions, cargo) are deterministic game state; no RNG. Safe for multiplayer sync and the existing rng-state asserts.
- **Lifetime caution:** the candidate-set loop consumes `CvTradeRoute*` pointers; synthesized routes must outlive the full evaluation (declare the container at function scope before the loop). This is a mandatory review item during implementation.

## Testing

1. Compile Assert target cleanly; play-test on Assert build first (same protocol as citizen work).
2. **Zero-config test:** 3+ city save with no Domestic Advisor flags: a raw-producer city, a craftsman city consuming that raw, and a port. Automate one wagon (full mode). Expect: raw hauled to the craftsman city sized to the buffer horizon, surplus sellables drained to the port, log shows demand classes. No idle parking while un-hauled surplus exists.
3. **Settings-override test:** set a maintain level and an import limit; confirm virtual hauling never violates either; configure an explicit route and confirm it takes precedence (no duplicate virtual route).
4. **Herding test:** two automated wagons, one big surplus pile; expect one wagon commits, the other finds different work (log shows discounted pickup value).
5. **Distance test:** equal surpluses near and far; wagon picks near.
6. **Sea test:** two coastal cities + coastal transport; same behaviors over water.
7. **AI regression:** AI opponents' wagons unchanged (gate untouched paths); their turns process normally.

## Risks

- **Candidate-set explosion:** cities x cities x yields per wagon per turn. At colony scale (~10 cities, ~40 cargo yields) with early filtering (skip zero-supply yields first), cost is trivial next to the existing per-route `generatePath` calls, but path generation stays only where it already happens (destination choice), not per virtual candidate.
- **Pointer lifetime** of ephemeral routes (see Safety).
- **Value-scale interactions** with `AI_transferYieldValue`'s opaque units - mitigated by knobs and the decision log, as with the citizen scorer.
- **The two human branches (:952 vs :1003) have already diverged upstream** (river-ford fallback exists only in the ROUTES branch); implementation must not entangle them further - virtual synthesis touches only the FULL branch.
