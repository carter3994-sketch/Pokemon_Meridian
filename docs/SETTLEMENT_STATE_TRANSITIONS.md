# Meridian settlement state transition specification v0.1

Status: engineering design; event handlers NOT implemented.

## Canonical chapter clock
- Chapter 0: landing, initial camp (phase 0).
- Chapter 1–2: expedition surveys, small construction advances (phase 1 when conditions satisfied).
- Chapter 3–5: construction expansion, merchants, housing and new NPCs.
- Chapter 6–8: more permanent settlement (phase 2 when conditions satisfied).
- After ending: phase 3, branching by ending and settlement/faction choices.

These chapter numbers are provisional story milestones, not final gym assignment. All eight Gym Leaders remain mandatory milestone events, and not every settlement progresses at the same rate.

## State transition contract
Inputs: chapter, current camp phase, faction standings, major choices, ending ID.
Outputs: updated camp phase, available services, NPC roster, door/warp accessibility, construction tiles and quests.
- Phase never automatically regresses just because player re-enters a map.
- Choice-based destruction or abandonment is a distinct postgame state, not accidental regression.
- Every upgrade transition is idempotent and save-safe.
- Chapter advances only after explicit story milestone completion, never on map reload.
- A chapter increment cannot silently erase a previously saved criminal record or NPC death.
- At chapter transitions, use one central script/special to recalculate affected settlements, then update maps on load.
- Before introducing variable math, define exact numeric bounds for reputation, crime and choice flags.

## Visual phase approval gates
Phase 0 camp visual v2 approved; overall playable layout v1 approved; exact grid pending.
Phases 1, 2 and ending-specific phase 3 each require user review of materially changed visuals before final art implementation.

## QA matrix
| Scenario | Expected |
|---|---|
| New save | Chapter 0, phase 0 |
| Reenter camp | No duplicate construction or NPC spawns |
| Save/reload after upgrade | Upgraded map persists |
| High refugee reputation | Positive development branch available |
| Hostile refugee reputation | Different dialogue, services and construction |
| Theft arrest | Crime consequences persist through reload |
| Ending A/B | Distinct playable postgame maps and quests |
| Restart game | No state bleed between saves |

## Exact grid follow-up
Before making final map tiles, produce a 48x40 coordinate grid with collision codes, warp coordinates and height transitions for user review. Do not treat the current conceptual zone diagram as that grid.
