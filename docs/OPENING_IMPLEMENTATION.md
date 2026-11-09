# Opening sequence implementation contract (Milestone 1)

## Mandatory event order

1. NEW GAME -> player appearance/gender choice.
2. Player naming screen -> name confirmation; declining returns to appearance choice.
3. Only after confirmation, the expedition prologue begins.
4. Establish that Johto is in collapse approximately a century after Gold/Silver; the scientific expedition carries civilians toward an unknown land.
5. The expedition reaches a coast. Native inhabitants call the continent **Aevor**; refugees have begun calling it **Meridian**.
6. A controlled first-playable landing area introduces movement, a camp checkpoint, and the first starter selection.
7. First rival encounter/battle; then unlock the next path. Save/load must preserve all flags.

## Character creation technical notes

Current expansion entry is `src/main_menu.c`, with `Task_NewGameBirchSpeech_*` state machine. It currently displays `gText_Birch_Welcome`, `gText_ThisIsAPokemon`, `gText_Birch_MainSpeech`, and `gText_Birch_AndYouAre` **before** gender/name selection. That ordering must be changed, not merely reworded. Existing gender and naming tasks can be reused; do not delete confirmation/return paths.

Existing source: `src/main_menu.c`, `src/new_game.c`, `src/intro.c`; new story event scripts and map data will be needed.

## Prologue text (draft, subject to in-game review)

**After** name confirmation:
- NARRATION: `A hundred years have passed since Johto's golden age.`
- NARRATION: `The harvests failed. The cities emptied. Every ship that could sail was sent to find a future.`
- EXPEDITION LEAD: `You're here because your family knows how to keep this mission alive. Out here, that matters more than money.`
- EXPEDITION LEAD: `The maps call this place Meridian. The people who live here call it Aevor.`
- EXPEDITION LEAD: `Remember that. We are visitors here.`

## First playable acceptance tests

- Selecting NEW GAME goes directly to character customization, with no expedition narrative shown beforehand.
- Both appearance choices work; naming and name rejection work.
- Only confirmed characters see the prologue.
- Scene progresses to a walkable landing map without freezing.
- Starter selection gives exactly one Pokémon; battle is possible; saving and reloading preserve the selection.
- No unapproved custom sprites are inserted as placeholders without explicit labeling.

## Dependencies

Build from the repository must pass before engine state-machine edits. Pin the imported upstream revision from `UPSTREAM_COMMIT`; do not replace the baseline source silently.
