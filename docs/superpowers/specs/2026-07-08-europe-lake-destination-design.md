# Europe Destination via Canal to Lake Cities - Design

**Date:** 2026-07-08
**Target:** WTP 4.2.1, branch `automation-fix`
**Goal:** A ship in Europe can return to a New World city on an inland lake when the player owns a canal city bridging ocean and lake and the ship can navigate lakes. Covers the manual Europe destination picker and human-automated sail-to-Europe returns.

## Problem (playtest 2026-07-08, screenshot: ocean -> canal city Trankebar -> lake city Frederiksberg)

The physical move already works: `CvUnit::canEnterArea` checks territory only (not water-area IDs), and a lake-capable small ship can move ocean -> canal/coastal city land tile -> lake -> lake city. But the destination eligibility is decided by a cheap geometry pre-filter that short-circuits before any pathfind:

- Manual picker `CvEuropeScreen.py:1248`: `city.isCoastal(MIN_WATER_SIZE_FOR_OCEAN) and city.isEuropeAccessable()`. A lake city fails both (its adjacent water area is smaller than ocean-min; lake terrain is never COAST/SHALLOW_COAST; the ocean-distance flood fill never crosses the land isthmus). The `generatePath` that would confirm the real route is never reached.
- Auto path `CvUnitAI::AI_bestDestinationPlot` (CvUnitAI.cpp:7440): gates on `pCityPlot->isEuropeAccessable()` before `findNearbyOceanPlot` + `generatePath`.

## Design

Relax both pre-filters to admit any city adjacent to navigable water, and let the existing `generatePath` (which uses the specific ship's movement rules) be the arbiter. This enforces "ship must be lake-capable through your own canal" automatically: a non-lake-capable ship's path fails, so it never sees the lake city; a lake city with no canal route fails the path; a landlocked city is not water-adjacent so is never even pathfound.

- Manual picker: `if (city.isCoastal(1)):` then the unchanged `generatePath(plotEast/plotWest, city.plot())`. The ship lands at a Europe-edge ocean plot (getBestCityPlot, unchanged) and its move-to-city mission routes through the canal.
- Auto path: `if (pCityPlot->isEuropeAccessable() || (isHuman() && pCityPlot->isCoastalLand(1)))`. `isHuman()`-gated so AI destination choice is byte-identical; human-automated ships gain lake-city returns, still confirmed by `findNearbyOceanPlot` + `generatePath`.

No new knobs. No new state. Savegame-safe. AI unchanged.

Deploy note: `tools/deploy.sh` now also syncs changed Python screens (CvEuropeScreen.py), not just the DLL and XML.

## Testing

1. Assert build clean.
2. In the screenshot save: a lake-capable sloop in Europe now lists the lake city (Frederiksberg) as a destination; selecting it lands the ship at the ocean edge and it sails through the canal city to the lake city.
3. A non-lake-capable ship does NOT list the lake city (its generatePath fails).
4. Normal coastal cities still listed exactly as before.
5. AI ships' Europe returns unchanged (gate is isHuman()).
