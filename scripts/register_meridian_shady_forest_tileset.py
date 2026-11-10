#!/usr/bin/env python3
"""Install a separate Shady Forest secondary tileset in the disposable CI checkout.

The first 512 metatiles are used to respect Emerald's 10-bit map tile IDs.
No files are committed by this script; run after staging external sources.
"""
from pathlib import Path
import json
import struct
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
STAGE = ROOT / "build/meridian_shady_forest_staging"
DEST = ROOT / "data/tilesets/secondary/meridian_shady_forest"
DEST.mkdir(parents=True, exist_ok=True)
raw = (STAGE / "tiles.4bpp").read_bytes()
assert len(raw) == 512 * 32, f"Expected 512 secondary 8x8 tiles, got {len(raw)//32}"
# Render native 4bpp tile indices into a standard indexed PNG for INCGFX.
im = Image.new("P", (128, 256))
im.putpalette([v for i in range(256) for v in ((i*17)%256,)*3])
for index in range(512):
    tx, ty = (index % 16) * 8, (index // 16) * 8
    tile = raw[index*32:(index+1)*32]
    for y in range(8):
        for x in range(8):
            byte = tile[y*4+x//2]
            im.putpixel((tx+x,ty+y), (byte >> (4*(x%2))) & 15)
im.save(DEST / "tiles.png")
meta = (STAGE / "metatiles.bin").read_bytes()
attrs = (STAGE / "metatile_attributes.bin").read_bytes()
assert len(meta) >= 512*16 and len(attrs) == 512*2
# The secondary map ID range is 512..1023; only 512 metatiles fit.
(DEST / "metatiles.bin").write_bytes(meta[:512*16])
(DEST / "metatile_attributes.bin").write_bytes(attrs)
pal = DEST / "palettes"
pal.mkdir(exist_ok=True)
# Emerald uses palettes 0..5 from primary General and 6..15 from secondary.
for i in range(6,16):
    src = STAGE / "palettes" / f"{i:02d}.pal"
    if src.exists():
        (pal / f"{i:02d}.pal").write_bytes(src.read_bytes())
    else:
        # Unused palette banks: copy an existing valid neutral secondary palette.
        (pal / f"{i:02d}.pal").write_bytes((STAGE / "palettes/06.pal").read_bytes())
base = "data/tilesets/secondary/meridian_shady_forest/"
graphics = ROOT / "src/data/tilesets/graphics.h"
metatiles = ROOT / "src/data/tilesets/metatiles.h"
headers = ROOT / "src/data/tilesets/headers.h"
externs = ROOT / "include/tilesets.h"
g = graphics.read_text()
marker = "#if !IS_FRLG"
assert marker in g and "gTilesetTiles_MeridianShadyForest" not in g
insert = ('const u32 gTilesetTiles_MeridianShadyForest[] = INCGFX_U32("'+base+'tiles.png", ".4bpp.fastSmol", "-num_tiles 512 -Wnum_tiles");\n'
          'const u16 ALIGNED(4) gTilesetPalettes_MeridianShadyForest[][16] =\n{\n'
          + "".join('    INCGFX_U16("data/tilesets/primary/general/'+f'palettes/{i:02d}.pal", ".gbapal"),\n' for i in range(6))
          + "".join('    INCGFX_U16("'+base+f'palettes/{i:02d}.pal", ".gbapal"),\n' for i in range(6,16))
          + '};\n\n')
graphics.write_text(g.replace(marker, marker+"\n\n"+insert,1))
m = metatiles.read_text()
assert marker in m and "gMetatiles_MeridianShadyForest" not in m
m_insert = ('const u16 gMetatiles_MeridianShadyForest[] = INCBIN_U16("'+base+'metatiles.bin");\n'
            'const u16 gMetatileAttributes_MeridianShadyForest[] = INCBIN_U16("'+base+'metatile_attributes.bin");\n\n')
metatiles.write_text(m.replace(marker,marker+"\n\n"+m_insert,1))
h = headers.read_text()
anchor = "const struct Tileset gTileset_Petalburg ="
assert anchor in h and "const struct Tileset gTileset_MeridianShadyForest =" not in h
definition = """const struct Tileset gTileset_MeridianShadyForest =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_MeridianShadyForest,
    .palettes = gTilesetPalettes_MeridianShadyForest,
    .metatiles = gMetatiles_MeridianShadyForest,
    .metatileAttributes = gMetatileAttributes_MeridianShadyForest,
    .callback = NULL,
};

"""
headers.write_text(h.replace(anchor,definition+anchor,1))
e = externs.read_text()
anchor = "extern const struct Tileset gTileset_Petalburg;"
assert anchor in e and "gTileset_MeridianShadyForest" not in e
externs.write_text(e.replace(anchor,"extern const struct Tileset gTileset_MeridianShadyForest;\n"+anchor,1))
layout = ROOT / "build/meridian_prototypes/layout_template.json"
obj = json.loads(layout.read_text())
assert obj["secondary_tileset"] == "gTileset_Petalburg"
obj["secondary_tileset"] = "gTileset_MeridianShadyForest"
layout.write_text(json.dumps(obj,indent=2)+"\n")
report = {
    "status": "engine_symbol_registered_in_disposable_build",
    "tileset": "gTileset_MeridianShadyForest",
    "tile_count": 512,
    "metatile_count": 512,
    "discarded_source_metatiles": len(meta)//16-512,
    "primary_dependency": "source metatiles reference primary General tiles; visual match NOT verified",
    "map_remapping": "NOT DONE; original provisional map metatile IDs retained",
    "credits": "build/meridian_shady_forest_staging/credits.md",
    "rom_visual_qa": "PENDING"
}
out = ROOT / "build/meridian_candidate_review"
out.mkdir(parents=True,exist_ok=True)
(out/"engine_registration_report.json").write_text(json.dumps(report,indent=2)+"\n")
print(json.dumps(report,indent=2))
