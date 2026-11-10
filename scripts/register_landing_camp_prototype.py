#!/usr/bin/env python3
"""Install the experimental Landing Camp into a disposable checkout for CI.

Never run this on the production branch without review: it adds a debug map
with temporary tiles, no events and no player entry point.
"""
import json
from pathlib import Path
import shutil

root = Path(__file__).resolve().parents[1]
stage = root / "build/meridian_prototypes"
layout = json.loads((stage / "layout_template.json").read_text())
area = json.loads((stage / "map_template.json").read_text())
maps = root / "data/maps"
layouts = root / "data/layouts"
group_path = maps / "map_groups.json"
layouts_path = layouts / "layouts.json"
groups = json.loads(group_path.read_text())
registry = json.loads(layouts_path.read_text())
if any(x["id"] == layout["id"] for x in registry["layouts"]):
    raise SystemExit("Prototype layout already registered")
if area["name"] in groups["gMapGroup_TownsAndRoutes"]:
    raise SystemExit("Prototype map already registered")
if len(area["warp_events"]) or len(area["coord_events"]):
    raise SystemExit("Prototype map must not contain live warps or triggers")
# Fail early if the new IDs collide with existing maps or layouts.
if any(x["name"] == layout["name"] for x in registry["layouts"]):
    raise SystemExit("Prototype layout name already registered")
if any(area["name"] in names for key, names in groups.items() if key != "group_order"):
    raise SystemExit("Prototype map name collides with another group")
if layout["width"] * layout["height"] * 2 != (stage / "landing_camp_arrival_placeholder_map.bin").stat().st_size:
    raise SystemExit("Invalid generated blockdata length")
dest = layouts / "MeridianLandingCampPrototype"
dest.mkdir(parents=True, exist_ok=False)
shutil.copyfile(stage / "landing_camp_arrival_placeholder_map.bin", dest / "map.bin")
shutil.copyfile(layouts / "LittlerootTown/border.bin", dest / "border.bin")
layout["border_filepath"] = "data/layouts/MeridianLandingCampPrototype/border.bin"
registry["layouts"].append(layout)
(layouts_path).write_text(json.dumps(registry, indent=2) + "\n")
map_dir = maps / area["name"]
map_dir.mkdir(parents=True, exist_ok=False)
(map_dir / "map.json").write_text(json.dumps(area, indent=2) + "\n")
(map_dir / "scripts.inc").write_text("MeridianLandingCampPrototype_MapScripts::\n    .byte 0\n")
# The engine's event assembly includes are explicit, not inferred from map_groups.
event_scripts_path = root / "data/event_scripts.s"
event_scripts = event_scripts_path.read_text()
include_line = '    .include "data/maps/MeridianLandingCampPrototype/scripts.inc"'
if include_line in event_scripts:
    raise SystemExit("Prototype event scripts already included")
event_scripts_path.write_text(event_scripts + "\\n" + include_line + "\\n")
groups["gMapGroup_TownsAndRoutes"].append(area["name"])
group_path.write_text(json.dumps(groups, indent=2) + "\n")
# Redirect only the disposable debug ROM's non-FRLG new-game spawn.
# This does not touch the checked-in game startup flow.
spawn_x, spawn_y = plan_spawn = json.loads((root / "data/meridian_plans/landing_camp_arrival.json").read_text())["landmarks"]["arrival"]
mask = json.loads((root / "data/meridian_plans/landing_camp_collision_draft.json").read_text())
if mask["rows"][spawn_y][spawn_x] != "0":
    raise SystemExit("Prototype arrival coordinate is blocked in collision plan")
if not any(0 <= spawn_x + dx < mask["width"] and 0 <= spawn_y + dy < mask["height"] and mask["rows"][spawn_y + dy][spawn_x + dx] == "0" for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0))):
    raise SystemExit("Prototype arrival has no open neighboring cell")
new_game_path = root / "src/new_game.c"
new_game = new_game_path.read_text()
original = "SetWarpDestination(MAP_GROUP(MAP_INSIDE_OF_TRUCK), MAP_NUM(MAP_INSIDE_OF_TRUCK), WARP_ID_NONE, -1, -1);"
replacement = f"SetWarpDestination(MAP_GROUP(MAP_MERIDIAN_LANDING_CAMP_PROTOTYPE), MAP_NUM(MAP_MERIDIAN_LANDING_CAMP_PROTOTYPE), WARP_ID_NONE, {spawn_x}, {spawn_y});"
if new_game.count(original) != 1:
    raise SystemExit("Could not safely locate unique default new-game warp")
new_game_path.write_text(new_game.replace(original, replacement))
print("Registered debug map and temporary new-game entrance in disposable checkout")
