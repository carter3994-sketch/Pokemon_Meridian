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
# Confirm every NPC can be approached from the debug arrival point, not
# merely that an isolated walkable tile exists beside the NPC.
from collections import deque
mask = json.loads((root / "data/meridian_plans/landing_camp_collision_draft.json").read_text())
arrival = json.loads((root / "data/meridian_plans/landing_camp_arrival.json").read_text())["landmarks"]["arrival"]
reachable = {tuple(arrival)}
queue = deque(reachable)
while queue:
    cx, cy = queue.popleft()
    for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
        nx, ny = cx + dx, cy + dy
        if (0 <= nx < mask["width"] and 0 <= ny < mask["height"]
                and mask["rows"][ny][nx] == "0" and (nx, ny) not in reachable):
            reachable.add((nx, ny))
            queue.append((nx, ny))

# Populate the test camp with three temporary, interactable characters.
# These use existing Emerald sprites until approved Meridian artwork is ready.
for x, y, gfx, script in (
    (14, 23, "OBJ_EVENT_GFX_SCIENTIST_1", "MeridianLandingCamp_EventScript_Researcher"),
    (20, 21, "OBJ_EVENT_GFX_FAT_MAN", "MeridianLandingCamp_EventScript_Quartermaster"),
    (16, 25, "OBJ_EVENT_GFX_SCIENTIST_1", "MeridianLandingCamp_EventScript_Kael"),
):
    if mask["rows"][y][x] != "0":
        raise SystemExit(f"Camp NPC location blocked: {x}, {y}")
    if not any(
        (x + dx, y + dy) in reachable
        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0))
    ):
        raise SystemExit(f"Camp NPC cannot be approached from arrival: {x}, {y}")
    area["object_events"].append({
        "graphics_id": gfx, "x": x, "y": y, "elevation": 3,
        "movement_type": "MOVEMENT_TYPE_FACE_DOWN",
        "movement_range_x": 0, "movement_range_y": 0,
        "trainer_type": "TRAINER_TYPE_NONE",
        "trainer_sight_or_berry_tree_id": "0",
        "script": script, "flag": "0",
    })
(map_dir / "map.json").write_text(json.dumps(area, indent=2) + "\n")
(map_dir / "scripts.inc").write_text("""MeridianLandingCampPrototype_MapScripts::
    .byte 0

MeridianLandingCamp_EventScript_Researcher::
    lock
    faceplayer
    msgbox MeridianLandingCamp_Text_Researcher, MSGBOX_DEFAULT
    release
    end

MeridianLandingCamp_EventScript_Quartermaster::
    lock
    faceplayer
    msgbox MeridianLandingCamp_Text_Quartermaster, MSGBOX_DEFAULT
    release
    end

MeridianLandingCamp_EventScript_Kael::
    lock
    faceplayer
    msgbox MeridianLandingCamp_Text_Kael, MSGBOX_DEFAULT
    release
    end

MeridianLandingCamp_Text_Kael:
    .string "My people call this land AEVOR.\\nIt was never empty.$"

MeridianLandingCamp_Text_Researcher:
    .string "Welcome to MERIDIAN. The natives call it AEVOR.$"

MeridianLandingCamp_Text_Quartermaster:
    .string "Supplies are limited. Stay near camp.$"
""")
# The engine's event assembly includes are explicit, not inferred from map_groups.
event_scripts_path = root / "data/event_scripts.s"
event_scripts = event_scripts_path.read_text()
include_line = '    .include "data/maps/MeridianLandingCampPrototype/scripts.inc"'
if include_line in event_scripts:
    raise SystemExit("Prototype event scripts already included")
event_scripts_path.write_text(event_scripts + "\n" + include_line + "\n")
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
