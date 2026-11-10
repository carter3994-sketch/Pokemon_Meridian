# Area visual and layout approval gate

Status: mandatory user-directed production requirement (2026-11-09).

**The user must review and explicitly approve every major area before its final visual/map implementation.** This includes all routes, towns, villages, forests, caves, coasts, ruins, expedition camps, gyms, and important interiors.

## Workflow for each area
1. Present a visual concept preview showing intended colors, atmosphere, biome, architecture, landmarks, and environmental storytelling.
2. Present a readable playable-map layout preview identifying main path, optional loops, alternate routes, discoveries, NPC/quest locations, access restrictions, and connections.
3. Request explicit approval. Revise concepts and layouts until approved. Silence or approval of another area does not count.
4. Only then implement the approved area, using GBA-feasible tilesets and map dimensions.
5. Present an in-engine screenshot or emulator capture to verify implementation fidelity; correct mismatches.

## Tracking
Maintain an area-by-area approval register with fields: area ID, concept version, concept approval, layout version, layout approval, implementation commit, in-game verification, and outstanding change requests.

## Scope and exceptions
- Provisional engine/debug maps and temporary scaffolding must be clearly identified as such and are **not** approved Meridian area designs.
- Existing temporary Emerald truck interior is a technical placeholder, not a user-approved expedition location.
- Do not interpret approval of a starter sprite or a narrative description as approval of a map.
- Gameplay systems and engine infrastructure may continue independently while visual approval is pending.
- Every route should feel distinctive, colorful, substantial, explorable, and beautiful, with branching discoveries rather than filler.
