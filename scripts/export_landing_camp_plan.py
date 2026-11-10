#!/usr/bin/env python3
"""Export a reviewed ASCII map plan as machine-readable, non-playable map metadata.

No engine map files, tile graphics, elevations or warps are generated here.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source = ROOT / "docs/LANDING_CAMP_GRID_48x40_V03.md"
match = re.search(r"```text\n(.*?)\n```", source.read_text(), re.S)
if not match:
    raise SystemExit("Missing source grid")
rows = [line[3:] for line in match.group(1).splitlines()]
if len(rows) != 40 or any(len(row) != 48 for row in rows):
    raise SystemExit("Grid must be 48x40")
symbols = {
    ".": "natural_ground", "=": "dirt_path", "D": "dock", "+": "building_door",
    "A": "arrival", "F": "campfire", "1": "forest_exit", "2": "coastal_exit",
    "3": "cave_entrance", "4": "ruins_gate", "5": "north_trail",
    "M": "medical_building", "L": "research_building", "H": "headquarters",
    "S": "supply_building", "Q": "living_quarters", "R": "ancient_ruins",
    "C": "cliffside_cave", "T": "forest_blocker", "^": "cliff_blocker",
    "~": "water_blocker",
}
unknown = set("".join(rows)) - symbols.keys()
if unknown:
    raise SystemExit(f"Unknown symbols: {unknown}")
landmarks = {
    "medical_door": [18, 17], "research_door": [18, 11],
    "hq_door": [28, 10], "supply_door": [34, 14],
    "quarters_door": [38, 23], "arrival": [12, 23],
    "campfire": [28, 17], "forest_exit": [23, 39],
    "coastal_exit": [44, 29], "cave_entrance": [44, 10],
    "ruins_gate": [31, 4], "north_trail": [23, 0],
}
payload = {
    "schema": "meridian-map-plan-v1",
    "status": "unapproved-engineering-plan-not-playable",
    "area": "Expedition Landing Camp",
    "phase": "arrival",
    "width": 48,
    "height": 40,
    "coordinate_system": "zero-based top-left, x right, y down",
    "legend": symbols,
    "rows": rows,
    "landmarks": landmarks,
    "note": "Concept planning only. No tile IDs, elevation, collisions, scripts, warps or approved engine assets.",
}
out = ROOT / "data/meridian_plans/landing_camp_arrival.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
print(f"Exported {out.relative_to(ROOT)}")
