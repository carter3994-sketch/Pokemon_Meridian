#!/usr/bin/env python3
"""Stage native Shady Forest tileset source files for engine integration.

Never replaces the game's active tileset without a reviewed map remap.
"""
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen
import json
import struct

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "build/meridian_shady_forest_staging"
BASE = "https://raw.githubusercontent.com/TeamAquasHideout/Team-Aquas-Asset-Repo/master/Tilesets/The Great Tileset Exchange/Full Tilesets/Shady Forest Secondary/"
FILES = ["tiles.4bpp", "metatiles.bin", "metatile_attributes.bin", "README.md", "credits.md"]
FILES += [f"palettes/{i:02d}.pal" for i in range(13)]

def fetch(path):
    url = quote(BASE + path, safe=":/")
    with urlopen(Request(url, headers={"User-Agent": "Pokemon-Meridian-Stage/1.0"}), timeout=35) as response:
        data = response.read(8_000_001)
    if len(data) > 8_000_000:
        raise ValueError(f"Asset exceeds limit: {path}")
    return data

for path in FILES:
    target = DEST / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(fetch(path))
tiles = (DEST / "tiles.4bpp").read_bytes()
metatiles = (DEST / "metatiles.bin").read_bytes()
attrs = (DEST / "metatile_attributes.bin").read_bytes()
assert len(tiles) % 32 == 0 and len(metatiles) % 16 == 0
tile_refs = struct.unpack("<" + "H" * (len(metatiles)//2), metatiles)
max_tile = max(x & 0x3FF for x in tile_refs)
palettes_used = sorted(set((x >> 12) & 0xF for x in tile_refs))
report = {
    "source": BASE,
    "status": "staged_native_source_not_installed_in_rom",
    "8x8_tile_count": len(tiles)//32,
    "16x16_metatile_count": len(metatiles)//16,
    "metatile_attribute_file_bytes": len(attrs),
    "max_referenced_8x8_tile_id": max_tile,
    "palette_indices_referenced": palettes_used,
    "palette_files": 13,
    "engine_tileset_symbol": "NOT_ASSIGNED",
    "map_metatile_remapping": "REQUIRED",
    "art_credit_file": "credits.md",
    "distribution_approval": "PENDING"
}
(DEST / "integration_report.json").write_text(json.dumps(report, indent=2)+"\n")
print(json.dumps(report, indent=2))
