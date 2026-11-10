# Meridian Landing Camp — external tileset evaluation

Status: SOURCING ONLY. No third-party artwork has been imported, licensed, or approved.

## Direction
Stop using the current procedural 16-color placeholder tiles as the final visual target. Prefer coherent, professionally authored Pokémon-style environmental art, then adapt and palette-reduce for pokeemerald with visual approval before implementation.

## Candidates to inspect
1. **SirMalo HGSS source art** — https://github.com/jls-dchrn/HGSS_pokemon_tileset — source artist credited as SirMalo on DeviantArt. Organized Nature, Buildings and Urban material; GitHub copies are formatted for RPG Maker XP (32px) and are not drop-in GBA metatiles. Check original author permission and art provenance before using.
2. **Pokémon Gaia compiled collection** — https://eeveeexpo.com/resources/1377/ — compiled by A.I.R, with original artist attribution including zetavares852. Page expressly warns that credits or permissions may be missing. Reference-only pending per-asset rights verification.
3. **Community Gen IV/V tile catalog** — https://steamcommunity.com/sharedfiles/filedetails/?id=2436216636 — indexes SailorVicious, Magiscarf, ChaoticCherryCake, KingLotus, Akirazu, etc. Follow original DeviantArt pages and verify each artist's actual terms, not the index's terms.
4. **Gen 3 tileset community collection** — https://www.reddit.com/r/PokemonROMhacks/comments/1l1thpl/ — community-maintained index with original sources. Index does not grant permission.

## Required approval and implementation gates
- Collect original artist page, exact asset, attribution, permission/terms, and source resolution for each asset. No assumption that 'public tiles' means unrestricted.
- Compare three consistent visual directions against the approved Landing Camp concept: coastal expedition architecture; forest/cliffs/waterfalls; dock and ship.
- Prefer GBA-native 8x8 graphics. RPG Maker XP 32x32 sheets must be adapted, never blindly downscaled.
- Check 4bpp palettes, primary/secondary graphics bank capacities, metatile behavior, border/shore transitions, and collision before integration.
- Create one 48x40 engine-faithful preview from the chosen asset set and obtain approval. Keep a clean attribution manifest.
- Do not deliver a ROM until the actual imported assets have passed compilation, visual QA, and on-device Delta testing.

## Immediate next engineering work
Build a candidate inventory with screenshot references and rights verification. Select one cohesive art base before authoring replacement tiles. The existing original-art workbench remains a technical prototype only.
