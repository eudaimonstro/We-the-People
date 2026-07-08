# Storage-Pressure-Scaled Warehouse Value - Design

**Date:** 2026-07-08
**Target:** WTP 4.2.1, branch `automation-fix` (extends the building-recommendation work)
**Goal:** Storage buildings (warehouses) should be recommended in proportion to a city's actual storage pressure, not by an unconditional baseline.

## Problem

In `CvCityAI::AI_buildingValue` (CvCityAI.cpp:1278-1310), any building with `getYieldStorage() != 0` scores:

```
yieldStorage/3  (flat ~33)  +  percent-full (0..100)  +  10 x capacity/freespace (>=10)
then x2 if best port city
```

The flat `yieldStorage/3` baseline and the empty-city floor mean a warehouse scores ~40-90 (double in the port) even in a city storing and producing almost nothing. In small/poor cities where profession-based buildings score near zero (nothing to staff or feed them), the warehouse wins the recommendation by default. Playtest report 2026-07-08: warehouse recommended in a low-goods city.

## Design

Human-gated (city owner `isHuman()`), inside the same block; AI players keep the stock formula byte-identical.

For human cities, compute the stock three-term value, then scale it by **storage pressure** before the port doubling:

```
netInflow    = sum over cargo yields of max(0, getRawYieldProduced(y) - getRawYieldConsumed(y))
freeSpace    = max(1, capacity - totalStored)
turnsToFull  = freeSpace / max(1, netInflow)
pressureFromFill    = percentFull                                   (0..100)
pressureFromInflow  = 100 * HORIZON / max(HORIZON, turnsToFull)     (100 if fills within HORIZON turns)
pressurePct  = max(pressureFromFill, pressureFromInflow), clamped to 0..100
storageValue = stockThreeTermValue * pressurePct / 100
```

`HORIZON` = `AUTOMATION_STORAGE_PRESSURE_TURNS` (GlobalDefinesAlt.xml, default 20, `getAutomationDefine` pattern).

Consequences: a city already bulging (percentFull high) keeps full warehouse value; a city that will fill its warehouse within ~20 turns of net production keeps full value; an empty city with negligible goods flow scores ~0 and the recommendation moves to whatever actually helps. The best-port x2 multiplier stays, applied after scaling (a port under pressure doubles; a port without pressure doubles ~0).

Out of scope: rebalancing any other term of `AI_buildingValue`; AI players.

Safety: no state, deterministic, savegame-compatible; single-block change; same gating discipline as all prior work.

## Testing

1. Assert build clean.
2. Low-goods city: warehouse no longer recommended; a useful building is.
3. Near-full or high-throughput city (e.g. the port): warehouse still recommended.
4. AI regression: formula unchanged for AI cities.
