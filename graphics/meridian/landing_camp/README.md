# Landing Camp production asset sources

`headquarters.png` is a 96 × 80 indexed source sprite adapted from the central HQ in the approved **Expedition Landing Camp – Aevor.png** reference. It retains the slate-blue roof wings, metal facade, gold windows, blue-and-gold compass banner, double entrance and satellite dish. Generation was guided by that exact reference; this is newly authored game art, not a pixel extraction.

The source uses transparent index 0, fourteen quantized building colors, and one reserved grass color. The map author composites transparency over grass. The converter assigns palette bank 7 and verifies every referenced 8 × 8 tile against its packed 4bpp encoding. The HQ door stays at (28, 10); roof/facade cells block movement and its entrance has `MB_NON_ANIMATED_DOOR`.

This is one implemented building asset. The surrounding legacy camp art and layout still fail the approved visual direction. This asset has not been verified in emulator gameplay; neither automated pixel equality nor a successful compilation establishes visual approval. The existing interior graphics remain temporary. Do not label the full camp production-ready.

`expedition_ship.png` is a 112 × 48 indexed adaptation of the approved modern metal expedition vessel, replacing the sailboat in the generated engine map. It uses palette bank 8, retains the gray hull, red waterline, blue windows, cargo and expedition banner, and remains on blocked water cells. Boarding events and final southwest harbor placement are not implemented.

`forest_conifer.png` is a 48 × 64 indexed conifer adaptation from the approved forest. It uses palette bank 9 and is composed across 3 × 4 metatiles in contiguous forest zones. Forest collision remains solid. The final dense forest composition, flowering trees and shoreline remain unfinished.

The original-art CI workflow assembles these assets into the real secondary tile bank and map blockdata, validates reachable doors and paired return warps, compiles a ROM, checks its header and runs mGBA until the first VBlank BIOS call. The startup smoke check does not test walking, interactions, interior transitions or saving.

Medical (48 × 48), research (48 × 64), supply (64 × 48), living quarters (48 × 32) and provision shop (48 × 48) indexed sprites replace the generic exterior slabs. Their palette banks are 10–14. The first four retain existing paired entrance locations; the provision storefront currently has no working interior entrance.

The converter now generates a dedicated `gTileset_MeridianCampEnvironment` primary bank for environment art and a secondary bank for imported structures and foliage. General is preserved for other maps. With these building assets, the primary bank uses 155 tiles and the secondary uses 356 tiles (each has a limit of 512). Flip-aware tile deduplication is verified by decoding every reference back to its authored pixels. The final map composition and remaining terrain are still unfinished.

Environment modules now include indexed cliff walls/lips, a waterfall, cave, ruins, stairs, expedition banner, shoreline and seamless ocean patch. Slots 0–4 have dedicated primary palettes. The ship retains true transparent pixels over an ocean underlay in the two GBA metatile layers; its rectangle is not painted with a flat water color.

The native-tileset CI artifact contains the actual two 4bpp tile banks, indexed PNGs, metatiles, behavior attributes, palettes and generated camp map files. The environment integration currently uses 254 primary tiles and 356 secondary tiles. Palette and per-layer pixel checks pass locally. These reusable assets are implemented; the existing map composition still needs reconstruction to match the approved reference, including a dense forest and complete waterfront. Waterfall animation, cave interior, provision-store entrance and final collision review remain unfinished.
