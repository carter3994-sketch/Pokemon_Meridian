# Pokémon: Meridian — Canonical design specification

## Narrative premise
Approximately a century after Pokémon Gold/Silver, Johto is collapsing. Starvation drives a government-backed expedition across the sea to a continent whose native inhabitants call **Aevor**. The expedition calls it **Meridian**. The story explores survival, displacement, trust, and whether saving one society justifies harming another.

## Required opening order
1. Character creation.
2. Expedition voyage and arrival.
3. First exploration and introduction to the native region.

## Characters and factions
- Player: from a struggling family of scientists/professors associated with the expedition.
- Rival: from a poor scientist family; proud and hot-headed, gradually becoming a close friend.
- Kael: young native companion, quietly watching over the expedition on behalf of his people; participates in camp scenes.
- Government liaison: well-intentioned but ethically compromised, privy to native secrets.
- Antagonists: a faction opposed to exploration that attempts to summon a destructive 'demon' Pokémon.
- Native guardians: powerful creatures distrustful of outsiders; rival captures and releases at least one.

## World and progression
- Semi-open exploration, with a fixed order of gyms and major plot triggers.
- Nightly camp / rest scenes advance character relationships.
- Each gym-linked area introduces one original catchable Pokémon; other wild encounters can draw from multiple generations.
- No Mega Evolution or Z-Moves in the initial design.

## Starter evolution families (all stages have Dragon as secondary type)
| Family | Typing | Approved visual direction |
|---|---|---|
| Bramblett → Thornval → Sylvaro | Grass/Dragon | Small quadrupedal forest creature growing into an armored, ancient bark-and-moss woodland beast |
| Pyrrak → Ignivar → Cinderaeth | Fire/Dragon | Low-slung obsidian-armored quadruped with magma seams; final winged volcanic dragon |
| Nereed → Marinys → Thaloris | Water/Dragon | Ocean-adapted lineage ending in a streamlined, legless abyssal sea serpent |

First evolution at level 16. Final evolution is story-triggered: two lines at one milestone, the third at a later revelation. Exact evolution events must be designed before implementation.

**Visual approval gate:** The previously approved starter artwork and sprite previews are authoritative. Production-ready GBA sprites require reference retrieval, palette/size conversion, and explicit review before insertion. Do not improvise replacement designs.

## Legendary choice
An ancient Dragon legendary anchors the climax. Capturing it saves the existing human civilization; refusing it allows a broader reset. This is a major ethical choice, not a simple villain defeat.

## Engineering principles
- Base engine: RHH pokeemerald-expansion, with upstream attribution.
- GBA target; source and assets must be included in the actual game repository before calling a build a Meridian build.
- Test compilation, intro flow, starter selection, saves, battles, and progression before packaging.
- Do not claim a playable build exists solely because a CI workflow file exists.
