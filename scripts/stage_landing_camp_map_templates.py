#!/usr/bin/env python3
"""Stage GBA map/layout JSON templates without registering unfinished assets.

Artifacts are intentionally excluded from the engine's active map tables.
"""
from pathlib import Path
import json

root = Path(__file__).resolve().parents[1]
plan = json.loads((root / "data/meridian_plans/landing_camp_arrival.json").read_text())
landmarks = plan["landmarks"]
out = root / "build/meridian_prototypes"
out.mkdir(parents=True, exist_ok=True)
layout = {
    "id": "LAYOUT_MERIDIAN_LANDING_CAMP_PROTOTYPE",
    "name": "MeridianLandingCampPrototype_Layout",
    "width": plan["width"],
    "height": plan["height"],
    "primary_tileset": "gTileset_General",
    "secondary_tileset": "gTileset_Petalburg",
    "border_filepath": "data/layouts/LittlerootTown/border.bin",
    "blockdata_filepath": "data/layouts/MeridianLandingCampPrototype/map.bin",
    "layout_version": "emerald",
}
area = {
    "id": "MAP_MERIDIAN_LANDING_CAMP_PROTOTYPE",
    "name": "MeridianLandingCampPrototype",
    "layout": layout["id"],
    "music": "MUS_LITTLEROOT",
    "region": "REGION_HOENN",
    "region_map_section": "MAPSEC_LITTLEROOT_TOWN",
    "requires_flash": False,
    "weather": "WEATHER_SUNNY",
    "map_type": "MAP_TYPE_TOWN",
    "allow_cycling": False,
    "allow_escaping": False,
    "allow_running": True,
    "show_map_name": False,
    "battle_scene": "MAP_BATTLE_SCENE_NORMAL",
    "connections": None,
    "object_events": [],
    "warp_events": [],
    "coord_events": [],
    "bg_events": [],
}
for name in ("medical_door", "research_door", "hq_door", "supply_door", "quarters_door"):
    x, y = landmarks[name]
    if plan["rows"][y][x] != "+":
        raise SystemExit(f"Door marker mismatch: {name}")
# Door and route targets are intentionally NOT added as live warp events:
# there are no destination maps yet, and fake warps would break gameplay.
for filename, value in (("layout_template.json", layout), ("map_template.json", area)):
    (out / filename).write_text(json.dumps(value, indent=2) + "\n")
print("Staged map and layout templates; no engine registration performed")
