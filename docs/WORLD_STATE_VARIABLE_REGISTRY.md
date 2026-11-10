# Meridian world-state variable registry v0.1

Status: engine constants committed; event scripts and map transformations not implemented.

## Reserved persistent variables
| Constant | Address | Proposed meaning |
|---|---|---|
| VAR_MERIDIAN_STORY_CHAPTER | 0x40F7 | Chapter/milestone clock, not real-time elapsed hours |
| VAR_MERIDIAN_LANDING_CAMP_PHASE | 0x40F8 | 0 arrival, 1 expansion, 2 established, 3 legacy |
| VAR_MERIDIAN_CENTRAL_CITY_PHASE | 0x40F9 | Central city evolution (begins already built) |
| VAR_MERIDIAN_NATIVE_RELATIONS | 0x40FA | Native-community standing (encoding TBD) |
| VAR_MERIDIAN_REFUGEE_RELATIONS | 0x40FB | Refugee standing (encoding TBD) |
| VAR_MERIDIAN_CRIME_HEAT | 0x40FC | Criminal notoriety (encoding TBD) |
| VAR_MERIDIAN_ENDING_ID | 0x40FD | Ending route selection (IDs TBD) |
| VAR_MERIDIAN_WORLD_CHOICE_BITS | 0x40FE | Compact choice bits (schema TBD) |
| VAR_MERIDIAN_POSTGAME_PHASE | 0x40FF | Postgame story phase |

All are aliases for vanilla pokeemerald-expansion unused permanent vars. Reserved does not mean implemented. Validate against upstream updates and any other mod features before reusing these addresses.

## Design safeguards
- 0 is the new-save default. Define explicit state IDs before scripts use each variable.
- Do not cram deaths, crimes, faction choices and all quests into one ambiguous bitfield; use additional permanent flags and clearly documented IDs.
- Values 0x40F7–0x40FF may be used elsewhere in future upstream engine updates; monitor collisions.
- Keep phase-specific collision, NPC and warp transitions consistent after save/load.
- Story-driven time advancement, not waiting on the device clock.
- All new area visuals and significant growth stages still require user approval.
- Add event-script unit/integration tests before considering any state transition complete.

## Landing Camp map status
Visual v2 approved. Overall layout v1 approved. Exact 48x40 proposed grid is not yet approved and no dedicated map has been created. Next map engineering task: produce a detailed coordinate/collision/warp review, then build approved art.
