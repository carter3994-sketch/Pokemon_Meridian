# Landing Camp art progress

## Terrain detail pass · 2026-11-10

The ground atlas adapts the approved **Expedition Landing Camp – Aevor** meadow swatch and the packed earth in the main courtyard. The first two 32 × 32 panels contain the dense meadow and its shorter grass variant. The last panel contains the dirt material. All three share the camp's 16-color material palette. No reference-project graphics were imported.

Reference review covered the actual primary tile graphics, palettes and metatile data from [Pokémon Emerald](https://github.com/pret/pokeemerald/tree/master/data/tilesets/primary/general), [FireRed](https://github.com/pret/pokefirered/tree/master/data/tilesets/primary/general), [Modern Emerald ORAS](https://github.com/lbsbezerra/pokeemerald-modern-oras/tree/master/data/tilesets/primary/general), and [Wishes of Tomorrow Route 224](https://github.com/jmaloney95/Wishes-Game/tree/master/data/tilesets/primary/route_224). The shared approach is to reuse ground art, use distinct edge and corner pieces, and compose foliage over a separate ground layer. [Tiled's terrain documentation](https://github.com/mapeditor/tiled/blob/master/docs/manual/terrain.rst) describes how edge and corner terrain matching fit together.

Meridian now uses rounded outer corners, recessed inner corners, and a grass rim with darker exposed soil. The campfire sits over the trail material and transparent trees sit over the meadow. The terrain stays cosmetic and the collision grid remains identical to playtest `49136383`.

The draft [Landing Camp PR](https://github.com/carter3994-sketch/Pokemon_Meridian/pull/10) records the build and emulator evidence. Final cliffside waterfront art and permanent interiors remain open.

## Waterfront, approach, and interiors

The southwest shoreline now has rock faces over the foamy waterline, two coves, offshore rocks and pier fittings. The cave approach is exterior-only. A plunge pool below the waterfall, a two-tile stair and a wider upper terrace frame the existing mouth.

The camp shrine has moved to a separate 24 × 20 wooded ruins map with a paved forecourt, fragmented pillars and rear court. The camp trail branches north to the ruins and has a paired return warp. The former shrine site is meadow and forest.

Six custom room layouts now have a dedicated expedition tileset and paired doors. Headquarters has a briefing station, research has capsule equipment, medical and quarters have beds, and the two supply rooms have separate shelving and counters. Provision uses the existing storefront door. These rooms are staged for the playtest and retain room for story, interactions and polish.
