#!/usr/bin/env python3
"""Audit existing GBA metatile candidates without assigning unverified visual meanings.

Outputs a JSON inventory. This does not alter game maps or claim that a
metatile is grass, a building, a cliff, or water.
"""
from collections import Counter
from pathlib import Path
import json
import struct

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/layouts/LittlerootTown/map.bin"
PLAN = ROOT / "data/meridian_plans/landing_camp_arrival.json"
OUT = ROOT / "build/meridian_prototypes/metatile_inventory.json"

def read_words(path):
    raw = path.read_bytes()
    if len(raw) % 2:
        raise SystemExit(f"Odd-sized blockdata: {path}")
    return struct.unpack(f"<{len(raw)//2}H", raw)

plan = json.loads(PLAN.read_text())
words = read_words(SOURCE)
if len(words) != 400:
    raise SystemExit("Expected 20x20 Littleroot map")
counts = Counter(word & 0x03FF for word in words)
primary = ROOT / "data/tilesets/primary/general/metatiles.bin"
secondary = ROOT / "data/tilesets/secondary/petalburg/metatiles.bin"
# Each metatile has 8 tile entries, each a 16-bit word.
def count_metatiles(path):
    size = path.stat().st_size
    if size % 16:
        raise SystemExit(f"Unexpected metatile binary size: {path}: {size}")
    return size // 16

inventory = {
    "status": "candidate-inventory-only-needs-visual-review",
    "source_layout": "LittlerootTown",
    "layout_dimensions": [20, 20],
    "target_dimensions": [plan["width"], plan["height"]],
    "primary_tileset": {"path": str(primary.relative_to(ROOT)), "metatile_count": count_metatiles(primary)},
    "secondary_tileset": {"path": str(secondary.relative_to(ROOT)), "metatile_count": count_metatiles(secondary)},
    "source_metatile_ids_by_frequency": [
        {"id": tile_id, "occurrences": count} for tile_id, count in counts.most_common()
    ],
    "warning": "Tile frequency cannot establish terrain identity. Visually inspect metatile art and palettes before selecting IDs; do not use this inventory as a finished tileset."
}
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(inventory, indent=2) + "\n")
print(f"Wrote {OUT} with {len(counts)} source metatile candidates")
