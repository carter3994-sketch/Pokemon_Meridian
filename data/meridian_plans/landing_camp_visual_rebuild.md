# Expedition Landing Camp — Visual Rebuild (P0)

Status: VISUAL QA FAILED. The November 9 Delta recording is the acceptance baseline for defects, not an approved appearance. No further player-facing build should be described as a visual milestone until the criteria below pass.

## Approved composition to preserve
48 x 40 metatile arrival map, including large expedition HQ, separate research and medical buildings, supply and living quarters, a separate Provision Store, a ship and dock, campfire plaza, tent market, waterfalls, dramatic cliffs, forests with pink flowering trees, ancient ruins, cave, northern trail and coastal/forest exits. Phase 1 arrival must leave room for camp growth in later phases.

Use the user-supplied **Expedition Landing Camp – Aevor / Playable Map Layout (v1.0)** board as the visual reference. The middle illustrated panel defines the landmark relationships below. Its perspective and labels are guide material. Exact tile positions and building door alignment need review against the next engine tile render.

| Region | Composition to match |
| --- | --- |
| Southwest waterfront | A broad, modern expedition ship moored below the camp cliffs. Its timber dock runs east to the south approach. |
| Central settlement | The largest structure is the blue-bannered metal HQ. Its entrance faces the circular stone fire plaza directly south. Keep the plaza legible on the approach from the dock and Route 1. |
| West of HQ | The research lab sits north of the medical center. Each has a distinct facade and entrance. Stairs between this cluster and HQ make the change in elevation visible. |
| East of HQ | The supply depot faces the plaza approach. The canvas living quarters form a fenced cluster southeast of it. |
| Northern terrace | Ruins occupy the northwest shelf. A stair leads toward the northern trail behind HQ. Scaffolding and the waterfall occupy the upper east, with the cave mouth farther east. |
| Southern and eastern exits | Route 1 leaves from the south near the dock junction. The coastal path follows the southeast cliffs around the quarters toward the cave branch. |
| Environment | Layered cliffs, dense forest with pink flowering accents, rocky blue surf, slate metal roofs, warm windows, and blue-and-gold expedition banners distinguish the camp from its surroundings. |

The checked-in V03 navigation sketch places the ruins east of center, splits the medical center and lab along one row, and sets the dock midway up a mostly straight western shoreline. Its generated art preview uses a sailboat and near-identical building silhouettes. The separate 30 x 20 terrain study has three tents and contains none of the main settlement landmarks. Use these renders as evidence of the gaps. Anchor the next layout and custom tileset to the board before changing the debug map or remapping the warps.

## Root cause
The current map generator assigns ONE metatile to each zone letter. A single wall or foliage metatile cannot render an entire building, tree, cliff face, ship or shore. The 2026-11-09 Delta review shows repeated roof/fence-like textures and discontinuous terrain. Changing the numeric ID for a zone is not a solution.

## P0 graphics implementation
1. Replace zone-to-single-metatile rendering with **coordinate-aware multi-metatile structures**: roof caps, roof edges, facade, doors, windows, walls and ground shadows for each building. The five existing interior warps must remain aligned to visible doors.
2. Implement a coherent ground palette and tile adjacency rules for grass-to-dirt, grass-to-sand, water-to-shore, cliffs-to-ground and path corners. Never place an isolated cliff or roof fragment as a generic ground filler.
3. Implement full-width dock and ship silhouettes, with walkable dock surface, shoreline and collision boundary. Ship graphics must be assembled from compatible multi-metatile assets, not substituted with water tiles.
4. Implement multi-tile trees and pink flowering accents, cliff and waterfall faces, cave opening and ruins. If the existing Emerald tilesets cannot support the approved composition, create a purpose-built indexed PNG tileset and matching metatiles/palettes/attributes instead of reusing unrelated tiles.
5. Produce a **pixel-accurate 48 x 40 map preview from the actual game tilesets**, with the same metatile IDs, palettes and tile ordering as the compiled ROM. The approved concept is the art direction; a generated concept illustration is not an engine preview.
6. Validate palette slots, tile bank boundaries, metatile behaviors, collisions, visible warp doors, NPC visibility, text pagination and map scrolling on hardware-compatible emulator output.

## Acceptance gates
- No zone uses one repeated roof/fence/wall fragment as a stand-in for a whole structure.
- HQ, research, medical, supply, living quarters and Provision Store are individually recognizable; ship, dock, campfire, waterfalls, cave and ruins have distinct graphics.
- Paths are connected, shorelines and cliff edges transition correctly, and trees are composed of complete crowns and trunks.
- All five existing indoor warps work in both directions; exterior door positions visually match warps.
- NPC dialogue fits the GBA message box and can be advanced to completion.
- Build passes GBA validation AND visual review; a green compile alone does not mean approved.
- User receives one directly importable .gba only after these checks, with an honest note on any remaining placeholders.

## Implementation constraint
The current Petalburg secondary tileset has 144 metatiles and is insufficient by itself to depict all of the approved expedition structures. A custom secondary tileset (and possibly primary environment additions) is the intended path. Do not represent this plan as already implemented.
