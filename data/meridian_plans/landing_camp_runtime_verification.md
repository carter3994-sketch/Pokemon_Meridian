# Landing Camp runtime verification — November 10, 2026

## Tested build cb11fd70
GitHub original-art integration run 42911438868 completed successfully. Its ROM was downloaded and run in a locally built mGBA core. New-game character setup and the intro progressed to Landing Camp. Movement from arrival to HQ, the HQ entrance transition, and the return transition to camp were observed. The interior uses temporary Emerald house graphics.

The emulator exposed incorrect terrain/building colors despite a passing PNG-to-packed-graphics comparison. Root cause: the registered secondary palette array contained ten entries, but fieldmap.c reads entries 6–15. The registration fix supplies sixteen aligned entries and the engine-input validator now rejects an undersized array. A new compiled ROM must be tested before claiming correct in-game colors.

## Ship/conifer changes 367c74a8
Local 4bpp round trip, image comparison, repetition checks and five-door reachability/return-warp checks passed. The atlas contains 259 authored metatiles, with 378 used unique 8x8 tiles. This does not establish visual approval or gameplay coverage.

## Still incomplete
The final approved composition, remaining custom buildings, dense flowering forests, cliffs, waterfalls, ruins and cave remain unfinished. Ship boarding, all other interior transitions, collision sweep, saving/loading and final palette output still require gameplay verification. The standard map-integration workflow uses an older placeholder path and fails visual repetition gates; that failure must not be represented as a successful production build. The original-art integration workflow is the relevant asset build.
