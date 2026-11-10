# Landing Camp production asset sources

`headquarters.png` is a 96 × 80 indexed source sprite adapted from the central HQ in the approved **Expedition Landing Camp – Aevor.png** reference. It retains the slate-blue roof wings, metal facade, gold windows, blue-and-gold compass banner, double entrance and satellite dish. Generation was guided by that exact reference; this is newly authored game art, not a pixel extraction.

The source uses transparent index 0, fourteen quantized building colors, and one reserved grass color. The map author composites transparency over grass. The converter assigns palette bank 7 and verifies every referenced 8 × 8 tile against its packed 4bpp encoding. The HQ door stays at (28, 10); roof/facade cells block movement and its entrance has `MB_NON_ANIMATED_DOOR`.

This is one implemented building asset. The surrounding legacy camp art and layout still fail the approved visual direction. This asset has not been verified in emulator gameplay; neither automated pixel equality nor a successful compilation establishes visual approval. The existing interior graphics remain temporary. Do not label the full camp production-ready.
