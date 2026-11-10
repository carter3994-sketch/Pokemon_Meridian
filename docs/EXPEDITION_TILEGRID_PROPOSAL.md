# Expedition Landing Camp — tile-grid engineering proposal v0.1

Status: TECHNICAL PLAN FOR REVIEW; NOT IMPLEMENTED OR APPROVED AS EXACT TILEMAP.
User approved visual direction v2 and overall layout v1. Dimensions and coordinates below are proposals.

## Geometry
- Proposed outdoor map: **48 x 40 metatiles**.
- Coordinates (x,y) start at upper-left, zero-based.
- Northwest (x 2–17, y 4–16): research lab and medical center, with separate interior warps.
- North center (x 18–31, y 6–18): expedition HQ and mission board.
- Northeast (x 32–45, y 5–17): construction, elevated trail, ruins/cave access.
- West-middle (x 2–15, y 17–30): landing dock and arrival scene, ramps to commons.
- Central commons (x 16–32, y 18–30): campfire, dirt-road loop, NPCs and noticeboard.
- East-middle (x 33–45, y 18–29): supply depot, living quarters, cliffside branch.
- South (x 15–34, y 31–39): main forest-route exit; coastal branch to southeast.
- Main dirt path at least two metatiles wide, dock → commons → HQ → forest exit. Add optional loops and sightlines.
- Ensure legal cliffs, shore, elevation, collision and bridges; keep active object counts manageable.

## Planned warps and events (concept IDs, not implemented)
ARRIVAL_DOCK_START, HQ_DOOR, LAB_DOOR, MEDICAL_DOOR, SUPPLY_DOOR, QUARTERS_DOOR, ROUTE1_EXIT, COASTAL_EXIT, CAVE_EXIT, RUINS_GATE, NORTHERN_TRAIL_GATE, CAMP_NOTICEBOARD.

## Persistent growth overlays
| State | Visual changes | Gameplay changes |
|---|---|---|
| Arrival | prefab cabins, dirt tracks, scaffolding, small dock | limited supplies and NPCs |
| Expansion | finished housing, depot extension, new paths | vendors and side quests |
| Established | enlarged port, permanent buildings, upgraded interiors | residents and services |
| Legacy | ending-specific buildings, security, closures | unique postgame quests and NPCs |

Progression depends on chapters and player decisions, not idle real-world time. Save/load must preserve it. Major future appearances require separate user approval.

## Implementation gates
1. Keep the currently compiling source and temporary Emerald opening as scaffolding.
2. After exact geometry review, create dedicated Meridian map ID, map layout, graphics and script data. Do not relabel Littleroot as final Aevor.
3. Change the initial warp only when the new scene and map compile and collision can be tested in an emulator.
4. Check player creation before narrative, all warps, walkability, save/load, story flags and phase changes.
5. Show real in-engine screenshots for user fidelity review. Build success alone is not proof of playability.

## Pending topology decisions
- Concept v1 depicts the forest exit at the south edge; final compass orientation and connections should be clarified.
- Coastal path access timing (immediate vs first mission) needs story design.
