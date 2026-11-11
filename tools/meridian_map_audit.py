#!/usr/bin/env python3
"""Read-only map registry audit for Pokémon Meridian.

Run from the repository root: python3 tools/meridian_map_audit.py
No map, tileset, or ROM files are modified.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
groups = json.loads((ROOT / "data/maps/map_groups.json").read_text())
layouts = json.loads((ROOT / "data/layouts/layouts.json").read_text())
layout_by_id = {item["id"]: item for item in layouts["layouts"]}
errors = []
maps = []
map_definitions = {}
for group in groups["group_order"]:
    for name in groups[group]:
        path = ROOT / "data/maps" / name / "map.json"
        if not path.exists():
            errors.append(f"Missing map definition: {path.relative_to(ROOT)}")
            continue
        data = json.loads(path.read_text())
        map_definitions[data["id"]] = data
        layout_id = data.get("layout")
        layout = layout_by_id.get(layout_id)
        if not layout:
            errors.append(f"{name}: unknown layout {layout_id}")
        maps.append({
            "name": name,
            "group": group,
            "layout": layout_id,
            "width": layout.get("width") if layout else None,
            "height": layout.get("height") if layout else None,
            "primary_tileset": layout.get("primary_tileset") if layout else None,
            "secondary_tileset": layout.get("secondary_tileset") if layout else None,
            "events": {
                kind: len(data.get(kind, []))
                for kind in ("object_events", "warp_events", "coord_events", "bg_events")
            },
        })
connection_count = 0
warp_count = 0
dynamic_warp_count = 0
for map_id, data in map_definitions.items():
    # Porymap represents maps without connections as JSON null.
    for connection in data.get("connections") or []:
        connection_count += 1
        destination = connection.get("map", "")
        if destination not in map_definitions:
            errors.append(f"{map_id}: connection references unregistered map {destination}")
    for warp_id, warp in enumerate(data.get("warp_events", [])):
        warp_count += 1
        destination = warp.get("dest_map", "")
        # Engine dynamic warps resolve from saved state, not a static map ID.
        if destination == "MAP_DYNAMIC":
            dynamic_warp_count += 1
            continue
        target = map_definitions.get(destination)
        if target is None:
            errors.append(f"{map_id}: warp {warp_id} references unregistered map {destination}")
            continue
        raw_index = warp.get("dest_warp_id")
        # Porymap serializes indexes as decimal strings; integers are valid too.
        try:
            if isinstance(raw_index, bool) or not isinstance(raw_index, (str, int)):
                raise ValueError
            destination_index = int(raw_index)
        except (ValueError, TypeError):
            errors.append(f"{map_id}: warp {warp_id} has invalid destination warp index {raw_index!r}")
            continue
        if not 0 <= destination_index < len(target.get("warp_events", [])):
            errors.append(f"{map_id}: warp {warp_id} destination index {destination_index} outside {destination}")
candidates = [entry for entry in maps if any(word in entry["name"].lower() for word in ("landing", "camp", "meridian", "aevor"))]
report = {
    "total_registered_maps": len(maps),
    "total_layouts": len(layout_by_id),
    "total_connections": connection_count,
    "total_warps": warp_count,
    "dynamic_warps_not_statically_resolved": dynamic_warp_count,
    "landing_camp_candidates": candidates,
    "errors": errors,
    "maps": maps,
    "note": "Static registry, connection and warp destination audit only; dynamic warps require runtime verification. Does not prove collisions, tileset quality, gameplay or ROM compilation.",
}
out = ROOT / "build/meridian_map_audit"
out.mkdir(parents=True, exist_ok=True)
(out / "report.json").write_text(json.dumps(report, indent=2) + "\n")
print(f"Registered maps: {len(maps)}; layouts: {len(layout_by_id)}")
print(f"Landing Camp candidates: {len(candidates)}; registry errors: {len(errors)}")
for item in candidates:
    print(f"  {item['name']}: {item['layout']}")
for error in errors[:20]:
    print(f"ERROR: {error}")
raise SystemExit(bool(errors))
