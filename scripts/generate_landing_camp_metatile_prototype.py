#!/usr/bin/env python3
"""Produce an experimental 48x40 GBA metatile blockdata binary.

This is a buildable asset prototype, NOT a registered or playable map.
Tiles are temporary existing Littleroot metatiles; visual fidelity and
collision behavior must be reviewed before map registration.
"""
from pathlib import Path
import json
import struct

root = Path(__file__).resolve().parents[1]
plan = json.loads((root / "data/meridian_plans/landing_camp_arrival.json").read_text())
collision = json.loads((root / "data/meridian_plans/landing_camp_collision_draft.json").read_text())
width, height = plan["width"], plan["height"]
if (width, height) != (48, 40) or len(plan["rows"]) != height:
    raise SystemExit("Unexpected grid dimensions")
if collision["width"] != width or collision["height"] != height:
    raise SystemExit("Collision grid mismatch")
source = (root / "data/layouts/LittlerootTown/map.bin").read_bytes()
if len(source) != 20 * 20 * 2:
    raise SystemExit(f"Unexpected Littleroot source blockdata size: {len(source)}")
words = struct.unpack("<400H", source)
# Explicit provisional metatile choices reviewed against the color atlases.
# Secondary metatile IDs begin at 512. Building silhouettes remain placeholders.
zone_words = {
    ".": 1,           # primary grass
    "=": 512 + 256,    # secondary sandy ground
    "D": 512 + 256,    # provisional dock approach
    "+": 512 + 256,    # door approach
    "A": 512 + 256,    # arrival clearing
    "F": 512 + 256,    # campfire not yet drawn
    "1": 512 + 256, "2": 512 + 256, "3": 512 + 256,
    "4": 512 + 256, "5": 512 + 256,
    "M": 512 + 180, "L": 512 + 180, "H": 512 + 180,
    "S": 512 + 180, "Q": 512 + 180,  # temporary wall segments
    "R": 512 + 220,  # secondary masonry
    "C": 112,        # primary rock
    "T": 512 + 116,    # secondary foliage
    "^": 112,        # primary rock
    "~": 41,         # primary water
}
if any(len(row) != width or any(ch not in zone_words for ch in row) for row in plan["rows"]):
    raise SystemExit("Invalid zone codes or row lengths")
base = zone_words["."]
primary_count = (root / "data/tilesets/primary/general/metatiles.bin").stat().st_size // 16
secondary_count = (root / "build/meridian_shady_forest_staging/metatiles.bin").stat().st_size // 16
if primary_count != 512:
    raise SystemExit(f"Unexpected primary metatile count: {primary_count}")
secondary_words = struct.unpack("<" + "H" * (secondary_count * 8), (root / "build/meridian_shady_forest_staging/metatiles.bin").read_bytes())
for code, tile_id in zone_words.items():
    if not (0 <= tile_id < primary_count or 512 <= tile_id < 512 + secondary_count):
        raise SystemExit(f"Invalid metatile for zone {code}: {tile_id}")
    if tile_id >= 512 and all(v == 0 for v in secondary_words[(tile_id-512)*8:(tile_id-511)*8]):
        raise SystemExit(f"Blank Shady Forest metatile selected for zone {code}: {tile_id}")

# Encode actual GBA map-grid collision bits from the draft mask.
# Metatile ID: bits 0-9; collision: bits 10-11; elevation: bits 12-15.
if len(collision["rows"]) != height or any(len(row) != width for row in collision["rows"]):
    raise SystemExit("Invalid collision row dimensions")
if any(value not in "01" for row in collision["rows"] for value in row):
    raise SystemExit("Collision rows must contain only 0 or 1")
tiles = [
    (zone_words[cell] & 0x03FF) | (0x0C00 if collision["rows"][y][x] == "1" else 0) | 0x3000
    for y, row in enumerate(plan["rows"])
    for x, cell in enumerate(row)
]
for y in range(height):
    for x in range(width):
        word = tiles[y * width + x]
        assert bool(word & 0x0C00) == (collision["rows"][y][x] == "1")
        assert (word & 0xF000) == 0x3000

# Check actual encoded map words, not merely the source collision JSON.
from collections import deque
arrival_x, arrival_y = plan["landmarks"]["arrival"]
def passable(x, y):
    return 0 <= x < width and 0 <= y < height and not (tiles[y * width + x] & 0x0C00)
if not passable(arrival_x, arrival_y):
    raise SystemExit("Encoded arrival point is blocked")
seen = {(arrival_x, arrival_y)}
queue = deque(seen)
while queue:
    x, y = queue.popleft()
    for nx, ny in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
        if passable(nx, ny) and (nx, ny) not in seen:
            seen.add((nx, ny))
            queue.append((nx, ny))
unreachable = {name: coords for name, coords in plan["landmarks"].items() if tuple(coords) not in seen}
if unreachable:
    raise SystemExit(f"Encoded map has unreachable landmarks: {unreachable}")
out = root / "build/meridian_prototypes"
out.mkdir(parents=True, exist_ok=True)
blockdata = out / "landing_camp_arrival_placeholder_map.bin"
blockdata.write_bytes(struct.pack(f"<{len(tiles)}H", *tiles))
manifest = {
    "status": "experimental-placeholder-with-encoded-mapgrid-collision",
    "width": width,
    "height": height,
    "bytes": len(tiles) * 2,
    "source_layout": "LAYOUT_LITTLEROOT_TOWN",
    "temporary_metatile_word": f"0x{base:04X}",
    "tile_selection": "explicit provisional atlas-reviewed metatiles",
    "reachable_walkable_cells": len(seen),
    "landmarks_reachable": len(plan["landmarks"]),
    "blocked_cells": sum(c == "1" for row in collision["rows"] for c in row),
    "zone_metatile_words": {k: f"0x{v:04X}" for k, v in zone_words.items()},
    "warning": "Terrain preview only; buildings, dock, campfire, and edge transitions remain placeholders. In-game verification required.",
}
(out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
print(f"Wrote {blockdata} ({blockdata.stat().st_size} bytes)")
