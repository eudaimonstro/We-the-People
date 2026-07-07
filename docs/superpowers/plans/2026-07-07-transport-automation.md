# Transport Automation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Automated transports (land wagons + coastal ships) haul usefully with zero configuration: virtual supply/demand routes, distance-aware scoring, pickup de-confliction, continuous overflow urgency - human players only.

**Architecture:** All behavior changes live in `CvSelectionGroupAI::AI_tradeRoutes()` (the shared per-turn transport brain), its scoring helper `CvPlayerAI::AI_transferYieldValue`, and a small demand helper on `CvCity`. Virtual routes are ephemeral stack objects appended to the existing candidate set in the `AUTOMATE_TRANSPORT_FULL` branch. Two gates: `bSmartHuman` (human + any transport automation: scoring fixes) and virtual synthesis (human + FULL mode only). AI players byte-identical.

**Tech Stack:** Same as citizen work: MSVC 2003 under Wine (`tools/build.sh`), XML knobs via `GC.getDefineINT` with in-code defaults, `gDLL->logMsg` diagnostics behind `AUTOMATION_LOGGING`.

**Spec:** `docs/superpowers/specs/2026-07-07-transport-automation-design.md`

**Build/test reality:** No unit-test harness exists; every task ends with a clean `tools/build.sh Assert` compile, and behavior is verified in-game per the protocol in the final task (same as the citizen plan).

**Line-endings ritual:** The repo's `.gitattributes` (`* text=auto`) LF-normalizes files stored with CRLF on first touch. For every file first touched by a task, commit a pure-normalization commit BEFORE the functional change (pattern established in the citizen work):

```bash
git show 8f7c5f4b:"<path>" > "<path>" && git add "<path>"
# repeat per file, then:
git commit -m "Normalize line endings in <files> per repo .gitattributes (no content change)"
# then restore/apply your edits and commit them separately
```

Files needing this here (not yet normalized): `Project Files/DLLSources/CvSelectionGroupAI.cpp`, `Project Files/DLLSources/CvPlayerAI.cpp`, `Project Files/DLLSources/CvGameCoreUtils.h`, `Project Files/DLLSources/CvGameCoreUtils.cpp`. Already normalized in earlier commits: CvCityAI.*, CvCity.*, GlobalDefinesAlt.xml.

**Key existing code (4.2.1 line numbers):**
- `CvSelectionGroupAI::AI_tradeRoutes` (CvSelectionGroupAI.cpp:909-1464); FULL-branch candidate build :952-1001; per-route value :1131-1206 (surplus at :1142); destination choice :1219-1286 (dest de-confliction :1241, coastal distance :1243-1272); load loop :1288-1387; empty-run comment :1126-1129
- `processTradeRoute` (:892), `estimateYieldsToLoad` (:1542), `AI_getYieldsLoaded` (:860)
- `CvPlayerAI::AI_transferYieldValue` (CvPlayerAI.cpp:9753): loading branch :9794-9817 (per-yield fullness factor + 90% total cliff), unloading branch :9818+
- `CvTradeRoute` (CvTradeRoute.h): `init(source, dest, yield)`; plain data, safe to stack-allocate
- `CvPlayerAI::AI_findBestPort(CvArea* = NULL, CvCity* = NULL) const` (CvPlayerAI.h:197)
- `CvPlayer::isYieldEuropeTradable(YieldTypes) const` (CvPlayer.h:520)
- `getAutomationDefine` currently file-local in CvCityAI.cpp (anonymous namespace near the top, added in citizen work)

---

### Task 1: Shared `getAutomationDefine` helper in CvGameCoreUtils

CvSelectionGroupAI.cpp and CvPlayerAI.cpp will need the XML-knob reader that currently lives in CvCityAI.cpp's anonymous namespace. Move it to CvGameCoreUtils.

**Files:**
- Modify: `Project Files/DLLSources/CvGameCoreUtils.h`, `Project Files/DLLSources/CvGameCoreUtils.cpp`
- Modify: `Project Files/DLLSources/CvCityAI.cpp` (delete local copy; no other change)

- [ ] **Step 1: Normalization commits for first-touched files**

```bash
cd /home/steve/workspace/wtp_automate/We-the-People
for f in "Project Files/DLLSources/CvGameCoreUtils.h" "Project Files/DLLSources/CvGameCoreUtils.cpp" "Project Files/DLLSources/CvSelectionGroupAI.cpp" "Project Files/DLLSources/CvPlayerAI.cpp"; do
  git show 8f7c5f4b:"$f" > "$f"; git add "$f"
done
git commit -m "Normalize line endings in transport-automation files per repo .gitattributes (no content change)"
```

(Doing all four now covers Tasks 1-6.)

- [ ] **Step 2: Declare in CvGameCoreUtils.h**

Near the other free-function declarations (e.g. after the `getUnit`/`getCity` declarations):

```cpp
// Citizen/transport automation fix: XML knob with default when the entry is missing or nonpositive.
int getAutomationDefine(const char* szName, int iDefault);
```

- [ ] **Step 3: Define in CvGameCoreUtils.cpp**

```cpp
int getAutomationDefine(const char* szName, int iDefault)
{
	const int iValue = GC.getDefineINT(szName);
	return iValue > 0 ? iValue : iDefault;
}
```

- [ ] **Step 4: Remove the local copy from CvCityAI.cpp**

Delete the whole `namespace { ... getAutomationDefine ... }` block added near the top of CvCityAI.cpp (below `#define YIELD_DISCOUNT_TURNS`), i.e. remove:

```cpp
namespace
{
	// XML knob with default when the entry is missing or nonpositive.
	int getAutomationDefine(const char* szName, int iDefault)
	{
		const int iValue = GC.getDefineINT(szName);
		return iValue > 0 ? iValue : iDefault;
	}
}
```

(CvCityAI.cpp includes CvGameCoreUtils.h transitively via the standard header set; if the compile disagrees, add `#include "CvGameCoreUtils.h"`.)

- [ ] **Step 5: Compile**

```bash
tools/build.sh Assert
```
Expected: EXIT 0, no `error C` lines.

- [ ] **Step 6: Commit**

```bash
git add "Project Files/DLLSources/CvGameCoreUtils.h" "Project Files/DLLSources/CvGameCoreUtils.cpp" "Project Files/DLLSources/CvCityAI.cpp"
git commit -m "Move getAutomationDefine to CvGameCoreUtils for shared use"
```

---

### Task 2: XML knobs

**Files:**
- Modify: `Assets/XML/GlobalDefinesAlt.xml`

- [ ] **Step 1: Add three defines** after the `AUTOMATION_JOIN_THRESHOLD_PERCENT` block:

```xml
	<Define>
		<DefineName>AUTOMATION_TRANSPORT_BUFFER_TURNS</DefineName>
		<iDefineIntVal>10</iDefineIntVal>
	</Define>
	<Define>
		<DefineName>AUTOMATION_TRANSPORT_MIN_HAUL</DefineName>
		<iDefineIntVal>10</iDefineIntVal>
	</Define>
	<Define>
		<DefineName>AUTOMATION_TRANSPORT_DISTANCE_TURNS</DefineName>
		<iDefineIntVal>2</iDefineIntVal>
	</Define>
```

- [ ] **Step 2: Validate and commit**

```bash
xmllint --noout Assets/XML/GlobalDefinesAlt.xml && git add Assets/XML/GlobalDefinesAlt.xml && git commit -m "Add transport automation tuning defines"
```

---

### Task 3: Production-feeding demand helper on CvCity

**Files:**
- Modify: `Project Files/DLLSources/CvCity.h` (already normalized)
- Modify: `Project Files/DLLSources/CvCity.cpp` (already normalized)

- [ ] **Step 1: Declare in CvCity.h**

Next to the trade-route methods (near `getMaxImportAmount`, around CvCity.h:1090-1105):

```cpp
	// Transport automation fix: how much of eYield this city wants delivered to keep
	// its working consumers (craftsmen) running for AUTOMATION_TRANSPORT_BUFFER_TURNS.
	int getAutomationTransportDemand(YieldTypes eYield) const;
```

- [ ] **Step 2: Define in CvCity.cpp**

Next to `getMaxImportAmount` (CvCity.cpp:12357 region):

```cpp
int CvCity::getAutomationTransportDemand(YieldTypes eYield) const
{
	const int iConsumed = getRawYieldConsumed(eYield);
	if (iConsumed <= 0)
	{
		return 0;
	}
	const int iBuffer = getAutomationDefine("AUTOMATION_TRANSPORT_BUFFER_TURNS", 10);
	// projected stock after the buffer horizon at current rates
	const int iProjected = getYieldStored(eYield)
		+ (getRawYieldProduced(eYield) - iConsumed) * iBuffer;
	if (iProjected >= 0)
	{
		return 0;
	}
	// never ask for more than the warehouse/import limit accepts
	return std::min(-iProjected, getMaxImportAmount(eYield));
}
```

- [ ] **Step 3: Compile, commit**

```bash
tools/build.sh Assert
git add "Project Files/DLLSources/CvCity.h" "Project Files/DLLSources/CvCity.cpp"
git commit -m "Automation: production-feeding transport demand helper on CvCity"
```

---

### Task 4: Virtual route synthesis in AI_tradeRoutes

**Files:**
- Modify: `Project Files/DLLSources/CvSelectionGroupAI.cpp` (function `AI_tradeRoutes`, plus `#include <deque>` if not already available via headers)

- [ ] **Step 1: Add gates and containers**

In `AI_tradeRoutes()` right after `const bool bIgnoreDanger = getIgnoreDangerStatus();` (:929), add:

```cpp
	// Transport automation fix (human cities only). bSmartHuman gates scoring
	// fixes for any automated human transport; virtual routes additionally
	// require FULL mode (the zero-config "automate transport" button).
	const bool bSmartHuman = isHuman() && isAutomated();
	const bool bVirtualRoutes = isHuman() && (getAutomateType() == AUTOMATE_TRANSPORT_FULL);
	// Ephemeral synthesized routes. deque: growth must not invalidate the
	// pointers pushed into `routes`, so no std::vector here. Function scope:
	// must outlive every use of `routes`.
	std::deque<CvTradeRoute> virtualRoutes;
	// demand class per synthesized route, for the decision log ('F' feed, 'P' port drain)
	std::map<const CvTradeRoute*, char> virtualRouteClass;
```

- [ ] **Step 2: Synthesize routes at the end of the FULL branch**

Inside the `if (!isHuman() || (getAutomateType() == AUTOMATE_TRANSPORT_FULL))` block, AFTER the existing `for (uint i = 0; i < aiRoutes.size(); ++i) { ... }` loop (i.e. just before the closing brace at :1002), add:

```cpp
		// Transport automation fix: synthesize virtual routes from real supply and
		// demand so the button works with zero Domestic Advisor configuration.
		// Player-configured routes always win: no virtual route is made where a
		// real (source, dest, yield) route already exists, and virtual deliveries
		// flow through the same import-limit / feeder checks as real ones.
		if (bVirtualRoutes)
		{
			const DomainTypes eDomain = getDomainType();
			CvCity* const pPortCity = kOwner.AI_findBestPort();
			int iCityLoop;
			for (CvCity* pSource = kOwner.firstCity(&iCityLoop); pSource != NULL; pSource = kOwner.nextCity(&iCityLoop))
			{
				// same reachability rules as real routes (:988-998)
				CvArea* const pSourceWaterArea = pSource->waterArea();
				if (eDomain == DOMAIN_SEA && pSourceWaterArea == NULL)
				{
					continue;
				}
				const int iSourceArea = (eDomain == DOMAIN_SEA) ? pSourceWaterArea->getID() : pSource->getArea();
				const bool bReachable = (eDomain == DOMAIN_SEA) ? plot()->isAdjacentToArea(iSourceArea)
					: ((iSourceArea == getArea())
						|| (plot()->getTerrainType() == TERRAIN_LARGE_RIVERS && plot()->isAdjacentToArea(pSource->getArea())));
				if (!bReachable)
				{
					continue;
				}

				for (YieldTypes eYield = FIRST_YIELD; eYield < NUM_YIELD_TYPES; ++eYield)
				{
					if (!GC.getYieldInfo(eYield).isCargo())
					{
						continue;
					}
					// a city the player flagged as importer of this yield never supplies it
					if (pSource->isImport(eYield))
					{
						continue;
					}
					const int iSurplus = pSource->getYieldStored(eYield) - pSource->getAutoMaintainThreshold(eYield);
					if (iSurplus <= 0)
					{
						continue;
					}

					int iDestLoop;
					for (CvCity* pDest = kOwner.firstCity(&iDestLoop); pDest != NULL; pDest = kOwner.nextCity(&iDestLoop))
					{
						if (pDest == pSource || pDest->isAutoImportStopped(eYield))
						{
							continue;
						}
						// player-configured route for this triple already exists? it wins.
						bool bHaveReal = false;
						for (uint r = 0; r < routes.size(); ++r)
						{
							if (routes[r]->getYield() == eYield
								&& routes[r]->getSourceCity() == pSource->getIDInfo()
								&& routes[r]->getDestinationCity() == pDest->getIDInfo())
							{
								bHaveReal = true;
								break;
							}
						}
						if (bHaveReal)
						{
							continue;
						}

						char cClass = 0;
						if (pDest->getAutomationTransportDemand(eYield) > 0)
						{
							cClass = 'F'; // keep craftsmen running
						}
						else if (pDest == pPortCity
							&& pSource != pPortCity
							&& kOwner.isYieldEuropeTradable(eYield)
							&& pDest->getMaxImportAmount(eYield) > 0)
						{
							cClass = 'P'; // drain sellable surplus to the port
						}
						if (cClass == 0)
						{
							continue;
						}

						virtualRoutes.push_back(CvTradeRoute());
						CvTradeRoute& kRoute = virtualRoutes.back();
						kRoute.init(pSource->getIDInfo(), pDest->getIDInfo(), eYield);
						virtualRouteClass[&kRoute] = cClass;
						processTradeRoute(&kRoute, cityValues, routes, routeValues, yieldsDelivered, yieldsToUnload);
					}
				}
			}
		}
```

Notes for the implementer:
- `FIRST_YIELD` and the `++eYield` enum increment are established WTP patterns (`FOREACH(Yield)` also exists; the explicit loop keeps the `isCargo` filter obvious). If `FIRST_YIELD` is unavailable here, use `(YieldTypes)0` and `eYield = (YieldTypes)(eYield + 1)`.
- `CvTradeRoute()` default-constructs with id -1; nothing in the FULL branch consults `getID()`.
- `firstCity`/`nextCity` are the standard CvPlayer city iterators used throughout the codebase.

- [ ] **Step 3: Compile, commit**

```bash
tools/build.sh Assert
git add "Project Files/DLLSources/CvSelectionGroupAI.cpp"
git commit -m "Automation: synthesize virtual transport routes from supply and demand"
```

---

### Task 5: Land distance penalty + empty-run value bar

**Files:**
- Modify: `Project Files/DLLSources/CvSelectionGroupAI.cpp` (destination-choice block :1219-1286)

- [ ] **Step 1: Land distance divisor**

In the destination-choice loop, the coastal block reads (:1243-1272) `if (bCoastalTransport) { ... }`. Add an `else if` directly after its closing brace:

```cpp
					else if (bSmartHuman)
					{
						// Transport automation fix: land wagons finally pay for distance,
						// same shape as the coastal tuning above.
						const int iDistanceTurns = getAutomationDefine("AUTOMATION_TRANSPORT_DISTANCE_TURNS", 2);
						iValue /= std::max(1, iTurns - iDistanceTurns);
					}
```

- [ ] **Step 2: Empty-run minimum value bar**

Immediately after the destination-choice loop ends (after the `}` closing `for (std::map<IDInfo, int>::iterator it = cityValues.begin(); ...)`, before `if ((pPlotCity != NULL) && (kBestDestination.eOwner != NO_PLAYER))` at :1288), add:

```cpp
	// Transport automation fix: an EMPTY transport may reposition only when the
	// prize is worth a real haul; kills aimless long empty runs. Loaded
	// transports are exempt - cargo must reach a destination.
	if (bSmartHuman && bNoCargo && kBestDestination.eOwner != NO_PLAYER)
	{
		const int iMinHaul = getAutomationDefine("AUTOMATION_TRANSPORT_MIN_HAUL", 10);
		if (iBestDestinationValue < iMinHaul * 100)
		{
			kBestDestination = IDInfo(NO_PLAYER, -1);
		}
	}
```

(With no cargo and no destination, the function falls through to `return false` and the caller skips/retreats - the existing idle path.)

- [ ] **Step 3: Compile, commit**

```bash
tools/build.sh Assert
git add "Project Files/DLLSources/CvSelectionGroupAI.cpp"
git commit -m "Automation: land transports pay for distance; empty runs need a worthwhile prize"
```

---

### Task 6: Pickup de-confliction

**Files:**
- Modify: `Project Files/DLLSources/CvSelectionGroupAI.cpp` (route-value loop, surplus computation at :1142)

- [ ] **Step 1: Discount surplus claimed by transports already heading to the source**

In the route-value loop, after `int iAmount = pSourceCity->getYieldStored(eYield) - pSourceCity->getAutoMaintainThreshold(eYield);` (:1142), add:

```cpp
			// Transport automation fix: discount surplus that other automated
			// transports already heading to this source will grab first, so
			// empty wagons stop herding to the same pile. Approximation: each
			// inbound transport group claims one hold's worth.
			if (bSmartHuman && pSourceCity != pPlotCity)
			{
				const int iInbound = kOwner.AI_plotTargetMissionAIs(pSourceCity->plot(), MISSIONAI_TRANSPORT, this, 0);
				if (iInbound > 0)
				{
					iAmount -= iInbound * GC.getGameINLINE().getCargoYieldCapacity();
				}
			}
```

(`AI_plotTargetMissionAIs(plot, missionAI, skipGroup, range)` is exactly what the destination side already uses at :1241; the `this` argument excludes our own group. The same-plot exemption keeps a wagon already standing at the source from discounting itself.)

- [ ] **Step 2: Compile, commit**

```bash
tools/build.sh Assert
git add "Project Files/DLLSources/CvSelectionGroupAI.cpp"
git commit -m "Automation: transports discount surplus other wagons are already fetching"
```

---

### Task 7: Overflow urgency + production-feeding boost in AI_transferYieldValue

**Files:**
- Modify: `Project Files/DLLSources/CvPlayerAI.cpp` (function `AI_transferYieldValue`, :9753)

- [ ] **Step 1: Continuous overflow urgency (loading branch)**

The loading branch (:9794-9817) currently applies `iValue *= 50 + ((100 * iStored) / std::max(1, iMaxCapacity));` (per-yield fullness - keep it), then the 90%-total-storage cliff block:

```cpp
			int iMax = iMaxCapacity * 9 / 10;
			// ... iMax == 0 guard ...
			if (iTotalStored >= iMax)
			{
				iValue *= 125 + ((100 * iMax) / iMax);
				iValue /= 100;
			}
```

Wrap the cliff in an AI-only else and add the human path (gate on `isHuman()` - `this` is the transport's owner):

```cpp
			if (isHuman())
			{
				// Transport automation fix: continuous total-fullness urgency
				// instead of a cliff at 90%, plus a rot bonus once the city is
				// past capacity and actively losing goods to decay.
				iValue *= 100 + (125 * iTotalStored) / std::max(1, iMaxCapacity);
				iValue /= 100;
				if (iTotalStored > iMaxCapacity)
				{
					iValue *= 2;
				}
			}
			else
			{
				int iMax = iMaxCapacity * 9 / 10;
				// WTP, ray, even if it should never happen, let us prevent iMax being 0 if iMaxCapacity for some reason is 1 above - START
				if (iMax == 0)
				{
					iMax = 270;
				}
				// WTP, ray, even if it should never happen, let us prevent iMax being 0 if iMaxCapacity for some reason is 1 above - END
				if (iTotalStored >= iMax)
				{
					iValue *= 125 + ((100 * iMax) / iMax);
					iValue /= 100;
				}
			}
```

- [ ] **Step 2: Production-feeding boost (unloading branch)**

At the end of the unloading branch, right after the existing feeder boost:

```cpp
			// transport feeder - start - Nightinggale
			if (pCity->getImportsMaintain(eYield))
			{
				iValue *= 2;
			}
			// transport feeder - end - Nightinggale
```

add:

```cpp
			// Transport automation fix: deliveries that keep working craftsmen
			// running outrank generic hauling and port drains.
			if (isHuman() && pCity->getAutomationTransportDemand(eYield) > 0)
			{
				iValue *= 2;
			}
```

- [ ] **Step 3: Compile, commit**

```bash
tools/build.sh Assert
git add "Project Files/DLLSources/CvPlayerAI.cpp"
git commit -m "Automation: continuous overflow urgency and craftsman-feeding delivery boost"
```

---

### Task 8: Decision logging

**Files:**
- Modify: `Project Files/DLLSources/CvSelectionGroupAI.cpp` (`AI_tradeRoutes`)

- [ ] **Step 1: Log destination decisions**

Right after the empty-run bar added in Task 5 Step 2, add:

```cpp
	if (bSmartHuman && GC.getDefineINT("AUTOMATION_LOGGING") > 0)
	{
		CvCity* const pLogDest = ::getCity(kBestDestination);
		char buf[512];
		sprintf(buf, "transport group %d at %S: dest=%S value=%d cargo=%d virtualRoutes=%d",
			getID(),
			pPlotCity != NULL ? pPlotCity->getName().GetCString() : L"(field)",
			pLogDest != NULL ? pLogDest->getName().GetCString() : L"(none)",
			iBestDestinationValue,
			(int)hasCargo(),
			(int)virtualRoutes.size());
		gDLL->logMsg("automation.log", buf);
	}
```

- [ ] **Step 2: Log loads with demand class**

In the load loop (Task 4's `routes[iBestRoute]`), right after `aiYieldsLoaded[routes[iBestRoute]->getYield()] += loaded;` (:1375), add:

```cpp
							if (bSmartHuman && GC.getDefineINT("AUTOMATION_LOGGING") > 0)
							{
								std::map<const CvTradeRoute*, char>::const_iterator itClass =
									virtualRouteClass.find(routes[iBestRoute]);
								const char cClass = (itClass != virtualRouteClass.end()) ? itClass->second : 'R';
								char buf[256];
								sprintf(buf, "  loaded %d %S [%c] for %S",
									loaded,
									GC.getYieldInfo(routes[iBestRoute]->getYield()).getDescription(),
									cClass,
									::getCity(kBestDestination) != NULL ? ::getCity(kBestDestination)->getName().GetCString() : L"?");
								gDLL->logMsg("automation.log", buf);
							}
```

('R' = player-configured route, 'F' = production feeding, 'P' = port drain.)

- [ ] **Step 3: Compile, commit**

```bash
tools/build.sh Assert
git add "Project Files/DLLSources/CvSelectionGroupAI.cpp"
git commit -m "Automation: transport decision logging"
```

---

### Task 9: Build, deploy, in-game verification

- [ ] **Step 1: Assert build + deploy with logging on**

```bash
tools/build.sh Assert && tools/deploy.sh
# then flip AUTOMATION_LOGGING to 1 in the INSTALLED mod's GlobalDefinesAlt.xml (not the repo):
python3 - "/home/steve/.local/share/Steam/steamapps/common/Civilization IV Colonization/Mods/WeThePeople-4.2.1/Assets/XML/GlobalDefinesAlt.xml" <<'EOF'
import sys, re
p = sys.argv[1]
s = open(p, 'rb').read().decode('ascii')
s2 = re.sub(r'(<DefineName>AUTOMATION_LOGGING</DefineName>\s*<iDefineIntVal>)0(</iDefineIntVal>)', r'\g<1>1\g<2>', s)
assert s2 != s
open(p, 'wb').write(s2.encode('ascii'))
EOF
```

- [ ] **Step 2: In-game protocol (Steve at the keyboard)**

1. **Zero-config:** save with a raw-producer city, a craftsman city consuming that raw, a port, no Domestic Advisor flags. Automate a wagon (full transport automation). Expect: raw hauled to the craftsman city, sellables drained to the port; log lines tagged [F] and [P]. No idle parking while un-hauled surplus exists.
2. **Settings override:** set a maintain level at the source and an import limit at a destination; confirm hauls never violate them. Add an explicit route for one triple; log shows [R] for it, no duplicate virtual route behavior.
3. **Herding:** two empty automated wagons, one big pile: log shows the second wagon valuing the discounted source lower and picking other work.
4. **Distance:** equal surpluses near and far: near wins.
5. **Sea:** coastal transport between two coastal cities does the same (virtual routes over water).
6. **Stability:** no new asserts (Assert build), no stuck wagons ping-ponging; AI opponents' wagons behave as before.

- [ ] **Step 3: Tune knobs if needed** (installed XML, relaunch - no rebuild), fold final values into the repo XML.

- [ ] **Step 4: Release build, deploy, push**

```bash
tools/build.sh Release && tools/deploy.sh
git push -u origin automation-fix
```

---

## Self-review notes

- **Spec coverage:** virtual synthesis (supply rule, demand classes F/P, player-settings precedence, reachability, no-Europe) → Task 4 + Task 3 helper; scoring fixes (land distance, empty-run bar, pickup de-confliction, continuous overflow, feeding boost) → Tasks 5-7; sea → falls out of Task 4/5 (same function, existing domain checks); knobs → Task 2; diagnostics → Task 8; safety/gating → `bSmartHuman`/`bVirtualRoutes` in Task 4 Step 1 used throughout; testing → Task 9.
- **Pointer lifetime:** `virtualRoutes` is a function-scope `std::deque` declared before any use of `routes`; deque growth preserves element addresses. Called out in Task 4 Step 1 comment.
- **Type consistency:** `getAutomationTransportDemand(YieldTypes) const` defined on CvCity (Task 3), used in Task 4 (`pDest->...`) and Task 7 (`pCity->...`). `getAutomationDefine(const char*, int)` moved to CvGameCoreUtils in Task 1, used in Tasks 3, 5, 6. `bSmartHuman`/`bVirtualRoutes`/`virtualRouteClass` declared Task 4 Step 1, used Tasks 5, 6, 8.
- **Placeholder scan:** clean; all code steps show full code.
- **One deliberate simplification vs spec:** de-confliction claims "proportional to their free cargo capacity"; implementation approximates one full hold per inbound group (Task 6 comment). Cheaper, deterministic, tunable later if needed.
