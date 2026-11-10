# Meridian — Consequence systems and sequel continuity

Status: Canonical user-directed design requirements, 2026-11-09. Examples are design proposals until individually approved.

## Player agency must have material consequences
- NPCs can permanently die or survive based on decisions; later dialogue, quests, relationships, and scenes must reflect this.
- The player may be banned from settlements, facilities, shops, or faction territory. Ensure alternative routes for mandatory progression, or explicitly communicate an intentional ending/failed quest.
- Theft and other offenses can cause arrest, confiscation, fines, jail time, restitution, faction hostility, and escalating legal consequences. Imprisonment must have playable narrative and mechanical consequences, not a cosmetic cutscene; prevent infinite loops and accidental softlocks.
- Consequences may be delayed for hours of gameplay; establish foreshadowing and observable payoffs. Avoid random untelegraphed punishments.
- Faction relationships, companion trust, political standing, guardian treatment, and moral decisions persist in the save state.
- Player choices should not all collapse into one fixed path or one cosmetic ending.

## Architecture requirements
1. Define persistent world-state variables and event flags before major scripts.
2. Track faction reputation, crimes/wanted status, jail outcomes, access restrictions, companion survival, and quest branching.
3. Create a consequence matrix for every major choice: prerequisite, decision, immediate outcome, delayed outcome, altered map/NPC/dialogue/quest, save flags, ending impact, postgame impact, and sequel impact.
4. Validate all reachable branches, alternate progression, save/load, and recovery from prison or restricted areas.
5. Support multiple genuinely distinct endings and ending-dependent playable postgame states.

## Future second game
- Meridian I must conclude its main arc satisfyingly while revealing a credible future story hook.
- Preserve a compact, versioned endgame continuity record (ending ID, major choices, surviving characters, faction outcomes, key world states) that a future Meridian II could recognize.
- Do not canonize one ending merely to simplify the sequel. Plan for several continuity paths, with shared future threats/mysteries and differences in starting conditions.
- A future cross-game import mechanism is a design goal, not a currently implemented feature. Consider GBA save limitations and emulator support before selecting implementation.

## Illustrative scenario proposals (not yet approved final plot)
- Stealing expedition medical supplies can lead to arrest and loss of trust; a later shortage might change an NPC's fate.
- Betraying a village can close its gates and require a dangerous alternative passage.
- Saving one expedition party member may mean another cannot be rescued.
- Endings reveal different aspects of an unresolved threat that can support a second game.

## Story principle
The world must remember. Decisions should change who lives, where the player can go, what happens after the credits, and what legacy reaches the sequel.
