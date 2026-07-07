# Citizen Automation Fix Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make WTP 4.2.1's "automate this citizen" pick sensible work slots: no starvation, no phantom-stockpile craftsmen, experts in their specialty, no churn - for human cities only.

**Architecture:** All behavior changes live in `CvCityAI.cpp`'s live scoring function `AI_citizenProfessionValue` and the pass driver `AI_assignWorkingPlots`, gated on `GET_PLAYER(getOwnerINLINE()).isHuman()`. Because the displacement checks, the spin-loop invariant re-checks, and the juggle pass all call the same scorer, bonuses implemented *inside the scorer* stay consistent everywhere automatically. Tuning knobs come from `GlobalDefinesAlt.xml` via `GC.getDefineINT` with in-code defaults.

**Tech Stack:** MSVC 2003 toolkit + nmake/jom under Wine (WTP's official Compiler repo), Windows Strawberry Perl (portable) for build scripts, XML for tuning constants.

**Testing reality:** This 2003-era game DLL has no unit-test harness and only builds/runs inside the game. TDD is replaced by: (a) every task ends with a clean compile of the `Assert` target (FAsserts enabled, so invariant violations crash loudly instead of spinning), (b) a decision log verifies behavior in-game against a written protocol in the final task.

**Spec:** `docs/superpowers/specs/2026-07-07-citizen-automation-design.md`. One addition to the spec's constants table discovered during planning: `AUTOMATION_FOOD_EMERGENCY_MULTIPLIER` (default 5) - the spec's "large enough to dominate" food bonus needs an explicit knob.

**Paths:**
- Repo: `/home/steve/workspace/wtp_automate/We-the-People` (branch `automation-fix`)
- Installed mod: `/home/steve/.local/share/Steam/steamapps/common/Civilization IV Colonization/Mods/WeThePeople-4.2.1`
- Compiler repo (Task 1 clones it): `/home/steve/workspace/wtp_automate/Compiler`

**Key existing code (all in `Project Files/DLLSources/CvCityAI.cpp` unless noted):**
- `AI_assignWorkingPlots()` :161 - pass driver (pool build :203-249, greedy loop :254-296, juggle loop :306-319)
- `AI_findBestJob` :3276 - per-profession search incl. displacement validity checks (:3310, :3343)
- `AI_parallelAssignToBestJob` :3445 - parallel search + placement, spin-loop invariant re-checks (:3493-3504, :3517-3528)
- `AI_juggleColonist` :3715 - pairwise swap pass (swap accept test :3746-3747)
- `AI_citizenProfessionValue` :3840 - THE scorer (input gather :3868-3876, output build :3878-3898, input guard :3905-3912, per-yield valuation :3914-3990, combine :3992-3997)
- `CvCity::getProfessionActualOutput` (CvCity.cpp:3242) - output capped by `netProduced + stored` per input
- Helpers available on the city: `foodDifference()`, `getYieldStored(y)`, `getRawYieldProduced(y)`, `getRawYieldConsumed(y)`, `getProfessionInput(eProf, pUnit)`
- `CvUnit::AI_getIdealProfession() const` (virtual, CvUnit.h:814)

---

### Task 1: Toolchain - stock DLL builds under Wine

The riskiest task; do it before touching any source. Nothing here modifies mod behavior.

**Files:**
- Create: `Project Files/build.bat` (non-interactive build entry, replaces the `pause`-blocked `bin/Compile.bat`)
- Create: `tools/build.sh` (Linux wrapper)
- Modify: `Project Files/Makefile.settings` (generated file; add `PERL=` path - do NOT commit, it's machine-local; verify it's gitignored and if not, leave untracked)

- [ ] **Step 1: Clone the WTP Compiler repo**

```bash
cd /home/steve/workspace/wtp_automate
git clone https://github.com/We-the-People-civ4col-mod/Compiler.git
ls "Compiler/Microsoft Visual C++ Toolkit 2003/bin/" | head   # expect cl.exe, link.exe, nmake.exe
ls Compiler/lib/                                              # expect Boost-1.32.0, Python24
```

Expected: toolkit binaries and libs present. The repo's Makefile auto-discovers `..\..\Compiler` relative to `Project Files` (bin/Makefile_setup.pl:33), which resolves to this location.

- [ ] **Step 2: Install portable Strawberry Perl (Windows) for the build scripts**

The Makefile runs `perl` for its helper scripts (`PERL=perl`, Makefile:89) inside Windows processes, so a Windows perl must exist in the Wine prefix.

```bash
cd /home/steve/workspace/wtp_automate
wget -O strawberry.zip "https://github.com/StrawberryPerl/Perl-Dist-Strawberry/releases/download/SP_53822_64bit/strawberry-perl-5.38.2.2-64bit-portable.zip"
mkdir -p strawberry && cd strawberry && unzip -q ../strawberry.zip
wine perl/bin/perl.exe -e "print qq(perl works\n)"
```

Expected: `perl works`. If the 64-bit portable fails under this Wine prefix, retry with a 32-bit portable release (5.32.x line offers them).

- [ ] **Step 3: Point the Makefile at that perl**

Create `Project Files/Makefile.settings` (nmake syntax, backslash paths; `z:` is Wine's mapping of `/`):

```
CUSTOM_CFLAGS =
PERL="z:\home\steve\workspace\wtp_automate\strawberry\perl\bin\perl.exe"
```

- [ ] **Step 4: Create the non-interactive build entry point**

`Project Files/build.bat` (CRLF line endings; `unix2dos` after writing if needed):

```bat
@echo off
rem Non-interactive build. Usage: build.bat <Target>  (Debug|Release|FinalRelease|Assert|Profile)
SET PATH=%PATH%;..\..\Compiler\Microsoft Visual C++ Toolkit 2003\bin
set TARGET=%1
if "%TARGET%"=="" set TARGET=Release
bin\jom source_list /NOLOGO && nmake precompile /NOLOGO && bin\jom build
```

`tools/build.sh`:

```bash
#!/bin/bash
# Build the WTP DLL under Wine. Usage: tools/build.sh [Release|Assert|Debug|FinalRelease]
set -e
cd "$(dirname "$0")/../Project Files"
WINEDEBUG=-all wine cmd /c build.bat "${1:-Release}"
ls -la ../Assets/CvGameCoreDLL.dll
```

```bash
chmod +x tools/build.sh
```

- [ ] **Step 5: Stock build**

```bash
cd /home/steve/workspace/wtp_automate/We-the-People && tools/build.sh Release
```

Expected: compile of ~200 translation units (minutes), then `copy.pl` places `Assets/CvGameCoreDLL.dll` (Makefile:280). Verify:

```bash
file Assets/CvGameCoreDLL.dll   # expect: PE32 executable (DLL) ... Intel 80386
```

Debugging notes if it fails (work through in order, don't give up early):
- `jom.exe` parallelism can misbehave under Wine: fall back to `nmake source_list && nmake precompile && nmake build` in build.bat.
- Perl script failures: run the failing script manually - `wine .../perl.exe bin/<script>.pl` - to see its error; most scripts take no args and write into `temp_files/` or `autogenerated/`.
- Missing `tbb.lib`: check `Project Files/tbb/` in-repo and `Compiler/lib`; the Makefile references `$(TBB_PATH)` - grep `TBB_PATH` in Makefile to see its discovery chain.
- cl.exe "out of heap": lower `PRECOMPILE_MEMORY` in Makefile.settings (e.g. `/Zm100`).

- [ ] **Step 6: Game-load smoke test**

```bash
MOD="/home/steve/.local/share/Steam/steamapps/common/Civilization IV Colonization/Mods/WeThePeople-4.2.1"
cp "$MOD/Assets/CvGameCoreDLL.dll" "$MOD/Assets/CvGameCoreDLL.dll.stock"   # one-time backup
cp Assets/CvGameCoreDLL.dll "$MOD/Assets/"
```

Then ask Steve to launch the game (WTP mod) and load a save. Expected: loads and plays normally with the self-built stock DLL. This step needs Steve; pause here if he's not around and continue after confirmation.

- [ ] **Step 7: Commit**

```bash
git add "Project Files/build.bat" tools/build.sh
git commit -m "Add non-interactive Wine build entry points"
```

---

### Task 2: XML tuning knobs + deploy script

**Files:**
- Modify: `Assets/XML/GlobalDefinesAlt.xml`
- Create: `tools/deploy.sh`

- [ ] **Step 1: Add the six defines**

In `Assets/XML/GlobalDefinesAlt.xml`, immediately after the `MODS_SHOULD_OVERRIDE_GLOBAL_DEFINES_HERE` Define block, insert:

```xml
	<!-- Citizen automation fix (human cities only) - see docs/superpowers/specs/2026-07-07-citizen-automation-design.md -->
	<Define>
		<DefineName>AUTOMATION_FOOD_RESERVE_TURNS</DefineName>
		<iDefineIntVal>8</iDefineIntVal>
	</Define>
	<Define>
		<DefineName>AUTOMATION_FOOD_EMERGENCY_MULTIPLIER</DefineName>
		<iDefineIntVal>5</iDefineIntVal>
	</Define>
	<Define>
		<DefineName>AUTOMATION_STOCKPILE_HORIZON</DefineName>
		<iDefineIntVal>10</iDefineIntVal>
	</Define>
	<Define>
		<DefineName>AUTOMATION_EXPERT_BONUS_PERCENT</DefineName>
		<iDefineIntVal>50</iDefineIntVal>
	</Define>
	<Define>
		<DefineName>AUTOMATION_STICKINESS_PERCENT</DefineName>
		<iDefineIntVal>10</iDefineIntVal>
	</Define>
	<Define>
		<DefineName>AUTOMATION_LOGGING</DefineName>
		<iDefineIntVal>0</iDefineIntVal>
	</Define>
```

- [ ] **Step 2: Create the deploy script**

`tools/deploy.sh`:

```bash
#!/bin/bash
# Copy built DLL + automation XML into the installed WTP 4.2.1 mod.
# Usage: tools/deploy.sh            deploy built files (backs up originals once)
#        tools/deploy.sh --restore  put the stock files back
set -e
cd "$(dirname "$0")/.."
MOD="/home/steve/.local/share/Steam/steamapps/common/Civilization IV Colonization/Mods/WeThePeople-4.2.1"

if [ "$1" = "--restore" ]; then
  cp "$MOD/Assets/CvGameCoreDLL.dll.stock" "$MOD/Assets/CvGameCoreDLL.dll"
  cp "$MOD/Assets/XML/GlobalDefinesAlt.xml.stock" "$MOD/Assets/XML/GlobalDefinesAlt.xml"
  echo "Restored stock files."
  exit 0
fi

[ -f "$MOD/Assets/CvGameCoreDLL.dll.stock" ] || cp "$MOD/Assets/CvGameCoreDLL.dll" "$MOD/Assets/CvGameCoreDLL.dll.stock"
[ -f "$MOD/Assets/XML/GlobalDefinesAlt.xml.stock" ] || cp "$MOD/Assets/XML/GlobalDefinesAlt.xml" "$MOD/Assets/XML/GlobalDefinesAlt.xml.stock"
cp Assets/CvGameCoreDLL.dll "$MOD/Assets/CvGameCoreDLL.dll"
cp Assets/XML/GlobalDefinesAlt.xml "$MOD/Assets/XML/GlobalDefinesAlt.xml"
echo "Deployed. Restore originals with: tools/deploy.sh --restore"
```

After writing it: `chmod +x tools/deploy.sh`.

- [ ] **Step 3: Commit**

```bash
git add Assets/XML/GlobalDefinesAlt.xml tools/deploy.sh
git commit -m "Add automation tuning defines and deploy script"
```

---

### Task 3: Scaffolding - gate, define reader, sustained-input helper, pre-pass job memory

**Files:**
- Modify: `Project Files/DLLSources/CvCityAI.h` (declarations around line 100-121; member section near the other `m_` members at the bottom of the class)
- Modify: `Project Files/DLLSources/CvCityAI.cpp`

- [ ] **Step 1: Add declarations to CvCityAI.h**

Next to the `AI_citizenProfessionValue` declaration (CvCityAI.h:102):

```cpp
	// Citizen automation fix (human cities only)
	bool AI_isHumanAutomationCity() const;
	int AI_sustainedInputAvailable(YieldTypes eYield, ProfessionTypes eProfession,
		const CvUnit& kUnit, const CvUnit* pDisplaceUnit) const;
```

In the private member section (find `m_` members near the class bottom):

```cpp
	// Transient pre-pass job memory for automation stickiness; NOT saved to savegames.
	// unit ID -> (profession, plot worked or NULL). Rebuilt at the start of every
	// AI_assignWorkingPlots pass, read (const, concurrently) by AI_citizenProfessionValue.
	std::map<int, std::pair<ProfessionTypes, const CvPlot*> > m_automationPrevJob;
```

(`<map>` is already available through the shared precompiled header; if the compile says otherwise, `#include <map>` at the top of CvCityAI.h.)

- [ ] **Step 2: Add implementations to CvCityAI.cpp**

Directly above `AI_citizenProfessionValue` (:3840), add:

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

bool CvCityAI::AI_isHumanAutomationCity() const
{
	return GET_PLAYER(getOwnerINLINE()).isHuman();
}

// Per-turn availability of an input yield as the automation scorer should see it:
// ongoing net production - crediting back what this unit and the unit it would
// displace currently consume, since those slots are being re-decided - plus the
// stockpile amortized over AUTOMATION_STOCKPILE_HORIZON turns. A stale handful of
// stored goods no longer makes a craftsman look employable; a real stockpile does.
int CvCityAI::AI_sustainedInputAvailable(YieldTypes eYield, ProfessionTypes eProfession,
	const CvUnit& kUnit, const CvUnit* pDisplaceUnit) const
{
	int iNet = getRawYieldProduced(eYield) - getRawYieldConsumed(eYield);
	if (kUnit.getProfession() == eProfession)
	{
		iNet += getProfessionInput(eProfession, &kUnit);
	}
	if (pDisplaceUnit != NULL && pDisplaceUnit != &kUnit && pDisplaceUnit->getProfession() == eProfession)
	{
		iNet += getProfessionInput(eProfession, pDisplaceUnit);
	}
	if (iNet < 0)
	{
		iNet = 0;
	}
	const int iHorizon = getAutomationDefine("AUTOMATION_STOCKPILE_HORIZON", 10);
	return iNet + getYieldStored(eYield) / iHorizon;
}
```

- [ ] **Step 3: Populate the pre-pass job memory in AI_assignWorkingPlots**

In `AI_assignWorkingPlots` (:161), after the `jobMutex.unlock();` at :186 and before the algorithm comment block, add:

```cpp
	// Automation stickiness: remember every unlocked citizen's current job before
	// the pass shuffles anyone, so the scorer can favor the status quo.
	m_automationPrevJob.clear();
	if (AI_isHumanAutomationCity())
	{
		for (uint i = 0; i < m_aPopulationUnits.size(); ++i)
		{
			CvUnit* pUnit = m_aPopulationUnits[i];
			if (pUnit != NULL && !pUnit->isColonistLocked() && pUnit->getProfession() != NO_PROFESSION)
			{
				m_automationPrevJob[pUnit->getID()] =
					std::make_pair(pUnit->getProfession(), (const CvPlot*)getPlotWorkedByUnit(pUnit));
			}
		}
	}
```

- [ ] **Step 4: Compile**

```bash
tools/build.sh Assert
```

Expected: clean build (warnings identical to stock). No behavior change yet - nothing reads the new state.

- [ ] **Step 5: Commit**

```bash
git add "Project Files/DLLSources/CvCityAI.h" "Project Files/DLLSources/CvCityAI.cpp"
git commit -m "Add automation scaffolding: gate, define reader, sustained input, pre-pass job memory"
```

---

### Task 4: Sustained-input accounting (production chains)

**Files:**
- Modify: `Project Files/DLLSources/CvCityAI.cpp` - `AI_citizenProfessionValue` only

- [ ] **Step 1: Gate flag at the top of the scorer**

After the `pDisplaceUnit` parameter handling at the top of `AI_citizenProfessionValue` (right after the `kProfInfo` line at :3849), add:

```cpp
	const bool bHumanAutomation = AI_isHumanAutomationCity();
```

- [ ] **Step 2: Replace the input guard for human cities**

The guard at :3905-3912 currently reads:

```cpp
	// 6) multi-input guard: all inYields must be available this turn
	for (int i = 0; i < numIn; ++i)
	{
		YieldTypes y = inYields[i];
		int avail = getRawYieldProduced(y) + getYieldStored(y);
		if (avail <= 0)
			return 0;
	}
```

Change the body to:

```cpp
	// 6) multi-input guard: all inYields must be available this turn
	for (int i = 0; i < numIn; ++i)
	{
		YieldTypes y = inYields[i];
		int avail;
		if (bHumanAutomation)
		{
			// Sustained flow + amortized stockpile; a token leftover in the
			// warehouse no longer qualifies the job.
			avail = AI_sustainedInputAvailable(y, eProfession, kUnit, pDisplaceUnit);
		}
		else
		{
			avail = getRawYieldProduced(y) + getYieldStored(y);
		}
		if (avail <= 0)
			return 0;
	}
```

- [ ] **Step 3: Cap slot-worker output by sustained input for human cities**

In step 4 of the scorer (:3887-3896), the else-branch computes `int actual = getProfessionActualOutput(eProfession, *pUnit);`. Immediately after that line, add:

```cpp
			if (bHumanAutomation && actual > 0)
			{
				// getProfessionActualOutput capped by netProduced + full stockpile;
				// re-cap using the sustained figure so output the input flow cannot
				// sustain is not valued. (Same 1 input : 1 output convention as
				// getProfessionActualOutput.)
				for (int i = 0; i < kProfInfo.getNumYieldsConsumed(); ++i)
				{
					const YieldTypes yIn = (YieldTypes)kProfInfo.getYieldsConsumed(i);
					if (yIn != NO_YIELD)
					{
						const int iSustained = AI_sustainedInputAvailable(yIn, eProfession, kUnit, pDisplaceUnit);
						if (iSustained < actual)
						{
							actual = iSustained;
						}
					}
				}
				if (actual <= 0)
				{
					return 0;
				}
			}
```

Note: `numIn`/`inYields` are gathered in step 3 *before* step 4 in the current function layout, but this loop deliberately re-reads from `kProfInfo` so the edit is order-independent; keep it that way.

The input *cost* subtraction at :3961-3983 stays untouched: with output capped, a starved craftsman job nets low or negative (clamped to >= 0 at :3997), which is exactly the deprioritization we want without touching the fragile fraction math.

- [ ] **Step 4: Compile clean**

```bash
tools/build.sh Assert
```

- [ ] **Step 5: Commit**

```bash
git add "Project Files/DLLSources/CvCityAI.cpp"
git commit -m "Automation: value craftsmen by sustained input flow, not stale stockpiles"
```

---

### Task 5: Food emergency bonus (starvation guard)

**Files:**
- Modify: `Project Files/DLLSources/CvCityAI.cpp` - `AI_citizenProfessionValue` per-yield loop

- [ ] **Step 1: Add the emergency bonus**

In the per-yield loop, after the `iOutputValue`/`iInputValue` computation block ends (after :3984, before the `// g) final net` line at :3988), add:

```cpp
		// Food emergency (human automation): when the city is running a food
		// deficit and the warehouse cannot cover it for long, food-producing
		// jobs must dominate everything else. Additive so a zero score (which
		// gets citizens ejected from the city) cannot result from this path.
		if (bHumanAutomation && eY == YIELD_FOOD)
		{
			const int iNetFood = foodDifference();
			if (iNetFood < 0)
			{
				const int iDeficit = -iNetFood;
				const int iReserveTurns = getAutomationDefine("AUTOMATION_FOOD_RESERVE_TURNS", 8);
				if (getYieldStored(YIELD_FOOD) < iDeficit * iReserveTurns)
				{
					const int iEmergencyMult = getAutomationDefine("AUTOMATION_FOOD_EMERGENCY_MULTIPLIER", 5);
					const int iCovered = std::min(pv.iYieldOutput, iDeficit);
					iOutputValue += 100 * AI_estimateYieldValue(YIELD_FOOD, iCovered) * iEmergencyMult;
				}
			}
		}
```

Self-correcting by construction: the greedy loop places citizens one at a time and `foodDifference()` reflects each placement, so once enough food workers are seated the deficit disappears and the bonus stops applying to later evaluations. Within one unit's search the city state does not change, so the spin-loop invariant re-check (:3493-3504, :3517-3528) sees identical values.

- [ ] **Step 2: Compile clean**

```bash
tools/build.sh Assert
```

- [ ] **Step 3: Commit**

```bash
git add "Project Files/DLLSources/CvCityAI.cpp"
git commit -m "Automation: emergency food bonus prevents starving human cities"
```

---

### Task 6: Expert-specialty bonus

**Files:**
- Modify: `Project Files/DLLSources/CvCityAI.cpp` - end of `AI_citizenProfessionValue`

- [ ] **Step 1: Add the bonus at the combine step**

The function currently ends (:3992-3997):

```cpp
	// 8) combine multi-output: sum each net value
	int combined = 0;
	for (int j = 0; j < yieldsOut.count && j < MAX_OUTPUT_YIELDS; ++j)
		combined += vals[j].iNetValue;

	return std::max(0, combined);
```

Insert between the loop and the return:

```cpp
	// Expert-specialty bonus (human automation): expertise already raises raw
	// output, but without an explicit margin an expert-in-specialty vs.
	// generalist-in-specialty arrangement scores as a near-tie and the swap
	// pass settles wrong. This margin makes the correct seating decisive.
	if (bHumanAutomation && combined > 0)
	{
		if (kUnit.AI_getIdealProfession() == eProfession)
		{
			const int iExpertBonus = getAutomationDefine("AUTOMATION_EXPERT_BONUS_PERCENT", 50);
			combined = combined * (100 + iExpertBonus) / 100;
		}
	}
```

- [ ] **Step 2: Compile clean**

```bash
tools/build.sh Assert
```

- [ ] **Step 3: Commit**

```bash
git add "Project Files/DLLSources/CvCityAI.cpp"
git commit -m "Automation: experts get a decisive bonus for their specialty profession"
```

---

### Task 7: Stickiness (anti-churn)

**Files:**
- Modify: `Project Files/DLLSources/CvCityAI.cpp` - end of `AI_citizenProfessionValue` (same block as Task 6)

No comparison-site changes anywhere: the incumbency bonus lives inside the scorer, so `AI_findBestJob`'s displacement checks (:3310, :3343), the placement re-checks with the spin-loop traps (:3493-3504, :3517-3528), and `AI_juggleColonist`'s swap sums (:3738-3747) all see it consistently. A challenger now has to beat `incumbent * (100+stickiness)/100`, and a juggle swap must overcome both units' incumbency bonuses - the displacement margin and swap threshold fall out of one mechanism.

- [ ] **Step 1: Add the stickiness bonus**

In the same human-gated block added in Task 6, after the expert bonus, add:

```cpp
		// Stickiness: favor (a) the job the unit currently holds - which makes
		// displacing an incumbent require a real margin, and juggle swaps
		// require overcoming two margins - and (b) the job the unit held when
		// the current assignment pass started (its plot gets cleared during the
		// pass, so (a) alone cannot see it).
		bool bIncumbent = false;
		if (kUnit.getProfession() == eProfession)
		{
			if (kProfInfo.isWorkPlot())
			{
				bIncumbent = (pPlot != NULL && getPlotWorkedByUnit(&kUnit) == pPlot);
			}
			else
			{
				bIncumbent = true;
			}
		}
		if (!bIncumbent)
		{
			std::map<int, std::pair<ProfessionTypes, const CvPlot*> >::const_iterator it =
				m_automationPrevJob.find(kUnit.getID());
			if (it != m_automationPrevJob.end() && it->second.first == eProfession)
			{
				bIncumbent = kProfInfo.isWorkPlot() ? (it->second.second == pPlot)
				                                    : (it->second.second == NULL);
			}
		}
		if (bIncumbent)
		{
			const int iStickiness = getAutomationDefine("AUTOMATION_STICKINESS_PERCENT", 10);
			combined = combined * (100 + iStickiness) / 100;
		}
```

(This goes inside `if (bHumanAutomation && combined > 0)` - restructure that block so both the expert and stickiness bonuses live in it.)

- [ ] **Step 2: Compile clean**

```bash
tools/build.sh Assert
```

- [ ] **Step 3: Commit**

```bash
git add "Project Files/DLLSources/CvCityAI.cpp"
git commit -m "Automation: incumbency bonus stops assignment churn"
```

---

### Task 8: Decision logging

**Files:**
- Modify: `Project Files/DLLSources/CvCityAI.cpp` - `AI_assignWorkingPlots`

- [ ] **Step 1: Log placements**

In `AI_assignWorkingPlots`, right after the `CvUnit* const pOldUnit = AI_parallelAssignToBestJob(*pUnit);` call (:268), add:

```cpp
		if (AI_isHumanAutomationCity() && GC.getDefineINT("AUTOMATION_LOGGING") > 0)
		{
			const ProfessionTypes eNewProf = pUnit->getProfession();
			CvWString szProf = (eNewProf != NO_PROFESSION)
				? GC.getProfessionInfo(eNewProf).getDescription() : L"NONE";
			char buf[512];
			sprintf(buf, "%S: unit %d (%S) -> %S | netFood=%d storedFood=%d displaced=%d",
				getName().GetCString(), pUnit->getID(),
				pUnit->getNameKey() != NULL ? pUnit->getName().GetCString() : L"?",
				szProf.GetCString(),
				foodDifference(), getYieldStored(YIELD_FOOD),
				pOldUnit != NULL ? pOldUnit->getID() : -1);
			gDLL->logMsg("automation.log", buf);
		}
```

Also log pass boundaries - immediately after the pre-pass memory population added in Task 3:

```cpp
	if (AI_isHumanAutomationCity() && GC.getDefineINT("AUTOMATION_LOGGING") > 0)
	{
		char buf[256];
		sprintf(buf, "=== assign pass: %S (pop %d, netFood %d) ===",
			getName().GetCString(), getPopulation(), foodDifference());
		gDLL->logMsg("automation.log", buf);
	}
```

Notes: `gDLL->logMsg` writes to the game's `Logs/` directory (pattern from BetterBTSAI.cpp:15). `%S` is the MSVC wide-string-in-narrow-printf conversion, used elsewhere in this codebase. Logging requires `LoggingEnabled = 1` in the game's `CivilizationIV.ini` - note this in the verification protocol. Keep the count of reassignments visible: churn shows up as repeated `=== assign pass ===` blocks with movements despite nothing changing.

- [ ] **Step 2: Compile clean**

```bash
tools/build.sh Assert
```

- [ ] **Step 3: Commit**

```bash
git add "Project Files/DLLSources/CvCityAI.cpp"
git commit -m "Automation: optional decision logging (AUTOMATION_LOGGING)"
```

---

### Task 9: Build, deploy, in-game verification

- [ ] **Step 1: Build the Assert target and deploy**

```bash
tools/build.sh Assert && tools/deploy.sh
```

(Assert target first: FAsserts enabled means an invariant violation produces a visible assert instead of the release spin-loop hang. Play-testing happens on this build; the final build for daily play is `tools/build.sh Release`.)

- [ ] **Step 2: Enable logging for the test session**

In the installed mod copy of `GlobalDefinesAlt.xml`, set `AUTOMATION_LOGGING` to 1 (or edit repo + redeploy). Confirm `LoggingEnabled = 1` in `CivilizationIV.ini` (in the game's user directory).

- [ ] **Step 3: In-game verification protocol (needs Steve at the keyboard)**

Using a real save with at least one problem city:

1. **Starvation:** pick a city with negative food balance, automate all citizens ("automate all" button on the city screen). Expect: food plots get staffed until the balance is non-negative or all citizens are food-producing; over the next 5 turns the city does not starve. Check `Logs/automation.log` shows the emergency path (food jobs chosen while netFood < 0).
2. **Production chains:** find a city with a craftsman building, zero ongoing input production, and near-empty input stores. Automate. Expect: no citizen placed in that building; log shows the craftsman jobs scored out.
3. **Experts:** engineer a city where an expert (e.g. Expert Farmer) is automated while a generalist works its specialty slot. Expect: within one pass the expert holds the specialty slot and the generalist moved elsewhere.
4. **Churn:** with a fully automated city, end 5 turns changing nothing else. Expect: `automation.log` shows no reassignments in passes where nothing changed (passes may not even trigger - the dirty flag should stay clear).
5. **Hang guard:** during all of the above, no assert popups from the displacement invariant and no freeze during end-turn processing.
6. **AI regression:** open WorldBuilder, inspect 2-3 AI cities' citizen assignments before/after (or simply confirm AI turns process normally and AI colonies look sane). The gate keeps their path untouched; this is a sanity check, not a deep audit.

- [ ] **Step 4: Iterate on knob defaults if needed**

If behavior is directionally right but mis-tuned (e.g. experts too sticky to leave a bad slot), adjust the XML values in the installed mod, relaunch, retest. Fold final values back into the repo's `GlobalDefinesAlt.xml`.

- [ ] **Step 5: Final release build + commit**

```bash
tools/build.sh Release && tools/deploy.sh
git add -A && git commit -m "Automation fix: final tuning values"
git push -u origin automation-fix
```

---

## Self-review notes

- **Spec coverage:** starvation guard → Task 5; sustained input → Task 4; expert bonus → Task 6; stickiness (all three sub-mechanisms: retention via pre-pass memory, displacement margin, swap threshold) → Tasks 3+7 (one mechanism covers all three consistently - a deliberate simplification vs. the spec's three separate change sites, chosen because it keeps the spin-loop invariant safe by construction); XML knobs → Task 2; logging → Task 8; build/deploy → Tasks 1-2; testing → Task 9. Emphasize buttons: out of scope per spec.
- **Deviation from spec worth knowing:** the spec's "displacement margin" and "swap threshold" are not implemented as separate comparison-site edits; they emerge from the in-scorer incumbency bonus. Same observable behavior, strictly safer.
- **Type consistency:** `m_automationPrevJob` declared `std::map<int, std::pair<ProfessionTypes, const CvPlot*> >` in Task 3, read with the same type in Task 7. `AI_sustainedInputAvailable(YieldTypes, ProfessionTypes, const CvUnit&, const CvUnit*)` matches at declaration (Task 3) and both call sites (Task 4).
- **Placeholder scan:** clean; every code step shows complete code. Task 1 debugging notes are contingency guidance, not steps.
