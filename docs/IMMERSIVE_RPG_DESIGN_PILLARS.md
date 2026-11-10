# Pokémon: Meridian — Immersive RPG design pillars

Status: USER-DIRECTED CANONICAL DESIGN REQUIREMENTS (2026-11-09)

## Vision
Meridian must feel like a deeply immersive, beautiful, colorful, exploration-heavy role-playing game. Routes are destinations, not short corridors. Player decisions must produce meaningful and persistent changes. Multiple narrative paths lead to genuinely different endings, and the selected ending fundamentally determines the postgame world and activities.

## Non-negotiable pillars
1. **Routes as adventures:** Distinct colorful biomes, visual landmarks, layered exploration, environmental storytelling, side areas, secrets, meaningful length, and pacing. No arbitrary padding or tedious backtracking.
2. **Branching exploration:** Alternative paths and optional discoveries; choices can open or close routes, alliances, quests, and access. Maintain fixed core gym/story milestones where required by existing canon without making the journey feel linear.
3. **Persistent consequences:** Track faction standing, companions, guardians, major quest decisions, and ecological/social impacts. Changes must be observable in NPC dialogue, world state, encounters, and available quests.
4. **Multiple credible endings:** The ancient dragon and humanity-versus-reset dilemma remains central, but earlier choices should influence ending variants and who survives, thrives, or opposes the player. No cosmetic choice-only endings.
5. **Ending-specific postgame:** Different world states, quests, encounters, NPCs, settlements, and conflicts after the credits. Design postgame branches alongside main story; do not bolt them on later.
6. **RPG character relationships:** Rival, Kael, native communities, refugees, and government liaison respond meaningfully to the player's actions.
7. **Technical discipline:** Plan GBA tile/palette/map constraints, save flags, branch testing, and performance from the outset. Validate all ending/postgame branches for reachability and softlocks.

## Design implications
- Define a world-state/choice-flag matrix before writing major quest scripts.
- Design route maps with multiple points of interest, optional loops, vistas, and meaningful rewards.
- Create a narrative branching diagram with main-story convergence points and multiple ending/postgame branches.
- For each consequential choice, specify: trigger, immediate feedback, later payoff, flags, and testing requirements.
- Keep the player's agency real; avoid claiming a decision matters if the game state does not change.
- The specific endings and postgame variants described in brainstorming are examples, not yet approved final canon.

## Acceptance tests
- Every major route has at least one meaningful optional exploration branch and distinct visual identity.
- Key decisions produce at least one persistent observable consequence.
- At least two substantively distinct endings lead to differentiated, playable postgame states.
- Branch combinations are tested for broken events, softlocks, missing NPCs, and inaccessible required content.
