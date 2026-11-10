# Living world: settlement growth and time passage

Status: **canonical user-approved requirement**, 2026-11-09. Design plan, not yet implemented.

## Core rule
As the adventure advances, time must visibly pass and refugee settlements must develop. This is not merely a static backdrop or a single endgame swap. The Expedition Landing Camp visual v2 and overall layout v1 are approved, **with settlement growth as a required addition**. Precise tile-grid remains to be reviewed.

## Progression model
- Use story milestones / chapters as the primary clock so that growth occurs at plausible intervals and never requires idle real-time waiting.
- Optional day/night changes and dialogue can communicate passage of days, weeks and months, but progression should not be dependent on device clock.
- At minimum model four world states: Arrival; Expansion; Established; Ending-dependent Legacy. Not all settlements must reach the same phase or progress at the same speed.
- The camp initially has modern prefab HQ, research/medical facilities, dirt paths, temporary housing, docks and construction. As phases advance, add finished buildings, interiors, residents, merchants, roads, facilities and new quests.
- Refugee towns can start partially built. At least one central hub city must already be fully established when first visited. Native Aevor communities have their own histories and must not be portrayed as recently founded refugee outposts.
- All eight Gym Leaders and their milestone order remain intact.

## Consequences and branching
- Story progress and player decisions jointly determine settlement outcomes; some choices may delay, redirect, or prevent construction.
- Reputation, theft, exile, leadership decisions, NPC deaths and alliances can affect which buildings and services exist and who occupies them.
- Ending-specific postgame world states must be playable, with distinct map access, NPCs, quests and political conditions.
- Keep alternate paths to mandatory objectives to avoid softlocks.

## Engineering and QA requirements
- Introduce persistent chapter and per-settlement state variables, plus flags for critical construction/choice outcomes.
- Use dynamic object events, tile changes and map scripts where feasible; larger alterations may require alternate map layouts or warp destinations.
- Ensure changes survive save/load and revisiting areas. Test transitions at every phase and across all major endings.
- Keep map evolution compatible with GBA performance, graphics budgets and event limits.
- Maintain user approval gates for new major visual states: present visual concepts and layouts for significant transformations before final implementation.
