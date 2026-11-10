#!/usr/bin/env python3
"""Check actual Landing Camp map blocks, door behavior and return warps.

Run after registration and art integration. This is a static engine-input
check, not an emulator gameplay test or visual approval.
"""
from collections import deque
from pathlib import Path
import json
import re
import struct

ROOT = Path(__file__).resolve().parents[1]
plan = json.loads((ROOT / "data/meridian_plans/landing_camp_arrival.json").read_text())
w, h = plan["width"], plan["height"]
words = struct.unpack(f"<{w*h}H", (ROOT / "data/layouts/MeridianLandingCampPrototype/map.bin").read_bytes())
bank = ROOT / "data/tilesets/secondary/meridian_shady_forest"
attrs = struct.unpack("<512H", (bank / "metatile_attributes.bin").read_bytes())
metas = struct.unpack("<4096H", (bank / "metatiles.bin").read_bytes())
# Emerald indexes secondary palettes at [NUM_PALS_IN_PRIMARY], so the
# C array must include all sixteen slots, including the first six.
graphics = (ROOT / "src/data/tilesets/graphics.h").read_text()
palette_array = graphics.split("gTilesetPalettes_MeridianShadyForest[][16]", 1)[1].split("};", 1)[0]
assert palette_array.count("INCGFX_U16(") == 16, "Secondary palette table must contain 16 slots"
raw = (bank / "tiles.4bpp").read_bytes()
assert len(raw) == 16384 and raw[:32] == bytes(32)
for word in words:
    mid = (word & 1023) - 512
    assert 0 <= mid < 512
    for ref in metas[mid*8:mid*8+8]:
        assert 512 <= (ref & 1023) < 1024
        assert (bank / f"palettes/{ref >> 12:02d}.pal").exists()

arrival = tuple(plan["landmarks"]["arrival"])
def walkable(x, y):
    return 0 <= x < w and 0 <= y < h and not words[y*w+x] & 0xC00
assert walkable(*arrival)
reachable, queue = {arrival}, deque([arrival])
while queue:
    x, y = queue.popleft()
    for nx, ny in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
        if walkable(nx, ny) and (nx, ny) not in reachable:
            reachable.add((nx, ny))
            queue.append((nx, ny))

enum_source = (ROOT / "include/constants/metatile_behaviors.h").read_text().split("};", 1)[0]
door_behavior = re.findall(r"\bMB_[A-Z0-9_]+\b", enum_source).index("MB_NON_ANIMATED_DOOR")
area = json.loads((ROOT / "data/maps/MeridianLandingCampPrototype/map.json").read_text())
checked = []
for landmark in ("medical_door", "research_door", "hq_door", "supply_door", "quarters_door"):
    x, y = plan["landmarks"][landmark]
    assert (x, y) in reachable, f"Unreachable {landmark}"
    assert attrs[(words[y*w+x] & 1023)-512] & 255 == door_behavior, landmark
    matches = [(i, warp) for i, warp in enumerate(area["warp_events"]) if (warp["x"],warp["y"]) == (x,y)]
    assert len(matches) == 1, f"Missing or ambiguous warp: {landmark}"
    warp_id, warp = matches[0]
    interiors = []
    for path in (ROOT / "data/maps").glob("MeridianLandingCamp*/map.json"):
        indoor = json.loads(path.read_text())
        if indoor["id"] == warp["dest_map"]:
            interiors.append(indoor)
    assert len(interiors) == 1, landmark
    indoor = interiors[0]
    assert 0 <= int(warp["dest_warp_id"]) < len(indoor["warp_events"])
    assert all(v["dest_map"] == area["id"] and int(v["dest_warp_id"]) == warp_id for v in indoor["warp_events"]), landmark
    checked.append(landmark)
report = {"checked_entrances": checked, "reachable_cells": len(reachable), "packed_bank_bytes": len(raw), "pass": True,
          "scope": "Static map, VRAM references, reachable door behavior and paired return warps; gameplay not tested"}
out = ROOT / "build/meridian_candidate_review/engine_asset_validation.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
