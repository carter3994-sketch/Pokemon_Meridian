# Pokémon: Meridian

A GBA Pokémon fan-game project based on [RHH pokeemerald-expansion](https://github.com/rh-hideout/pokeemerald-expansion).

## Project status

The Emerald expansion engine is installed. `develop` builds original Landing Camp tiles, metatiles, palettes, collision blockdata and a playable verification ROM through the [original-art integration workflow](.github/workflows/meridian-art-engine-integration.yml).

Verified code checkpoint: [57457bb4](https://github.com/carter3994-sketch/Pokemon_Meridian/commit/57457bb40724d2948ec42e4a26ff35c968cbf638). Its ROM compiled, passed the GBA header/startup checks, and was tested in mGBA. Both 16 KiB tile banks and all 13 map palettes matched live emulator memory. HQ, research, medical, supply and living-quarters door round trips passed.

Original indexed artwork is in [graphics/meridian/landing_camp](graphics/meridian/landing_camp). The build exports native 4bpp banks, metatiles, behavior attributes, palettes and the actual 48 × 40 map as `meridian-landing-camp-native-tileset`. Architecture follows the approved **Expedition Landing Camp – Aevor.png** project reference.

The full approved camp composition, dense forest and waterfront layout, permanent interiors, provision-store/cave entrances, waterfall animation and final collision review remain unfinished. This is a development checkpoint, not a finished game release. See the [runtime verification record](docs/verification/landing_camp_57457bb4.json).

## Canonical setting

About 100 years after Gold/Silver, an expedition from a collapsing Johto arrives in a new region. The native inhabitants call it **Aevor**; the expedition calls it **Meridian**.

## Original starter families

- **Bramblett → Thornval → Sylvaro** — Grass/Dragon
- **Pyrrak → Ignivar → Cinderaeth** — Fire/Dragon
- **Nereed → Marinys → Thaloris** — Water/Dragon

Approved visual references are required for production sprites. Do not substitute newly invented designs.

## Planned technical foundation

- GBA engine: [pokeemerald-expansion](https://github.com/rh-hideout/pokeemerald-expansion)
- GitHub Actions builds and testing
- Changes reviewed and verified before release

This project credits Rom Hacking Hideout and upstream contributors. Do not commit proprietary ROM dumps or unauthorized copyrighted assets.
