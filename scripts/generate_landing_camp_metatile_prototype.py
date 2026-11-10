#!/usr/bin/env python3
"""Produce an experimental 48x40 GBA metatile blockdata binary.

This is a buildable asset prototype, NOT a registered or playable map.
Tiles are temporary existing Littleroot metatiles; visual fidelity and
collision behavior must be reviewed before map registration.
"""
from collections import Counter
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
# The most common existing metatile is a temporary base for all map cells.
# We do not claim it is a correct grass, water, cliff or door tile.
base = Counter(words).most_common(1)[0][0]
distinct = [word for word, _ in Counter(words).most_common(12)]
if len(distinct) < 9:
    raise SystemExit("Not enough source metatile variety")
zone_words = {
    ".": distinct[0], "=": distinct[1], "D": distinct[2],
    "+": distinct[3], "A": distinct[1], "F": distinct[2],
    "1": distinct[1], "2": distinct[1], "3": distinct[1],
    "4": distinct[1], "5": distinct[1],
    "M": distinct[4], "L": distinct[4], "H": distinct[4],
    "S": distinct[4], "Q": distinct[4],
    "R": distinct[5], "C": distinct[5], "T": distinct[6],
    "^": distinct[7], "~": distinct[8],
}
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
    "reachable_walkable_cells": len(seen),
    "landmarks_reachable": len(plan["landmarks"]),
    "blocked_cells": sum(c == "1" for row in collision["rows"] for c in row),
    "zone_metatile_words": {k: f"0x{v:04X}" for k, v in zone_words.items()},
    "warning": "No mapped terrain variety, validated collision, event scripts, warps, map registration, or in-game testing.",
}
(out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
print(f"Wrote {blockdata} ({blockdata.stat().st_size} bytes)")
