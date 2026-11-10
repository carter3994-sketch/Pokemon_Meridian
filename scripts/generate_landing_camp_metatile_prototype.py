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
tiles = [base] * (width * height)
out = root / "build/meridian_prototypes"
out.mkdir(parents=True, exist_ok=True)
blockdata = out / "landing_camp_arrival_placeholder_map.bin"
blockdata.write_bytes(struct.pack(f"<{len(tiles)}H", *tiles))
manifest = {
    "status": "experimental-unregistered-nonplayable-placeholder",
    "width": width,
    "height": height,
    "bytes": len(tiles) * 2,
    "source_layout": "LAYOUT_LITTLEROOT_TOWN",
    "temporary_metatile_word": f"0x{base:04X}",
    "warning": "No mapped terrain variety, validated collision, event scripts, warps, map registration, or in-game testing.",
}
(out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
print(f"Wrote {blockdata} ({blockdata.stat().st_size} bytes)")
