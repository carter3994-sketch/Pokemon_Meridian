#!/usr/bin/env python3
"""Generate a preliminary collision mask from the approved-direction map sketch.

This is a design diagnostic, NOT a GBA metatile collision export.
"""
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
source = root / "data/meridian_plans/landing_camp_arrival.json"
plan = json.loads(source.read_text())
rows = plan["rows"]
if len(rows) != plan["height"] or any(len(row) != plan["width"] for row in rows):
    raise SystemExit("Invalid grid dimensions")
walkable = set(".=D+AF12345")
blocked = set("MLHSQRTC^~")
if not set("".join(rows)) <= walkable | blocked:
    raise SystemExit("Unexpected terrain symbols")
collision = ["".join("0" if c in walkable else "1" for c in row) for row in rows]
landmarks = plan["landmarks"]
for name, (x, y) in landmarks.items():
    if not (0 <= x < plan["width"] and 0 <= y < plan["height"]):
        raise SystemExit(f"Out-of-bounds landmark: {name}")
    if collision[y][x] != "0":
        raise SystemExit(f"Blocked landmark: {name}")
result = {
    "schema": "meridian-collision-plan-v1",
    "status": "unapproved-abstract-collision-only",
    "width": plan["width"],
    "height": plan["height"],
    "rows": collision,
    "warnings": [
        "No GBA metatile behaviors, elevation, border connections or event warps are defined.",
        "Gated routes are marked walkable only for connectivity checks; gameplay access rules are pending.",
        "Door tiles are placeholders and require graphics and map event configuration.",
    ],
}
out = root / "data/meridian_plans/landing_camp_collision_draft.json"
out.write_text(json.dumps(result, indent=2) + "\n")
print(f"Validated and exported abstract collision mask: {out.relative_to(root)}")
