#!/usr/bin/env python3
"""Install the experimental Landing Camp into a disposable checkout for CI.

This adds a debug New Game entry and registers the paired camp interiors.
Run in a disposable build checkout so the stock game entry stays intact.
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
# Create traversable, reversible camp building and vessel interiors. Reuse existing
# engine-compatible indoor layouts as temporary art until custom assets land.
# Each outside door and its indoor exit are paired by a stable warp index.
interiors = (
    ("Medical", "medical_door", "LittlerootTown_ProfessorBirchsLab", ((6, 12), (7, 12))),
    ("Research", "research_door", "LittlerootTown_ProfessorBirchsLab", ((6, 12), (7, 12))),
    ("Headquarters", "hq_door", "LittlerootTown_BrendansHouse_1F", ((9, 8), (8, 8))),
    ("Supply", "supply_door", "LittlerootTown_BrendansHouse_1F", ((9, 8), (8, 8))),
    ("Quarters", "quarters_door", "LittlerootTown_BrendansHouse_1F", ((9, 8), (8, 8))),
    ("Vessel", "ship_boarding", "SSTidalCorridor", ((16, 2),)),
)
landmarks = json.loads((root / "data/meridian_plans/landing_camp_arrival.json").read_text())["landmarks"]
for warp_id, (label, landmark, source_name, exits) in enumerate(interiors):
    x, y = landmarks[landmark]
    if mask["rows"][y][x] != "0":
        raise SystemExit(f"Blocked entrance for {label}")
    interior_name = "MeridianLandingCamp" + label
    interior_id = "MAP_MERIDIAN_LANDING_CAMP_" + label.upper()
    layout_id = "LAYOUT_MERIDIAN_LANDING_CAMP_" + label.upper()
    source_map = json.loads((maps / source_name / "map.json").read_text())
    source_layout = next(
        entry for entry in registry["layouts"]
        if entry["id"] == source_map["layout"]
    )
    source_block = root / source_layout["blockdata_filepath"]
    source_border = root / source_layout["border_filepath"]
    interior_layout = dict(source_layout)
    interior_layout.update({
        "id": layout_id,
        "name": interior_name + "_Layout",
        "blockdata_filepath": f"data/layouts/{interior_name}/map.bin",
        "border_filepath": f"data/layouts/{interior_name}/border.bin",
    })
    interior_layout_dir = layouts / interior_name
    interior_layout_dir.mkdir(parents=True, exist_ok=False)
    shutil.copyfile(source_block, interior_layout_dir / "map.bin")
    shutil.copyfile(source_border, interior_layout_dir / "border.bin")
    registry["layouts"].append(interior_layout)
    indoor = dict(source_map)
    indoor.update({
        "id": interior_id,
        "name": interior_name,
        "layout": layout_id,
        "object_events": [],
        "warp_events": [
            {"x": ix, "y": iy, "elevation": 0,
             "dest_map": area["id"], "dest_warp_id": str(warp_id)}
            for ix, iy in exits
        ],
        "coord_events": [],
        "bg_events": [],
    })
    interior_dir = maps / interior_name
    interior_dir.mkdir(parents=True, exist_ok=False)
    (interior_dir / "map.json").write_text(json.dumps(indoor, indent=2) + "\n")
    (interior_dir / "scripts.inc").write_text(
        f"{interior_name}_MapScripts::\n    .byte 0\n"
    )
    # Register each indoor script in the global event assembly, as required
    # by the generated map table's map-script pointer.
    event_scripts_path = root / "data/event_scripts.s"
    with event_scripts_path.open("a") as event_file:
        event_file.write(f'    .include "data/maps/{interior_name}/scripts.inc"\n')
    groups["gMapGroup_TownsAndRoutes"].append(interior_name)
    area["warp_events"].append({
        "x": x, "y": y, "elevation": 0,
        "dest_map": interior_id, "dest_warp_id": "0",
    })
(layouts_path).write_text(json.dumps(registry, indent=2) + "\n")
# Validate both directions of every building warp before attempting a ROM build.
if len(area["warp_events"]) != len(interiors):
    raise SystemExit("Expected five building entrances and the vessel gangway")
for index, (label, landmark, _, exits) in enumerate(interiors):
    x, y = landmarks[landmark]
    outdoor = area["warp_events"][index]
    indoor_name = "MeridianLandingCamp" + label
    indoor = json.loads((maps / indoor_name / "map.json").read_text())
    if (outdoor["x"], outdoor["y"]) != (x, y):
        raise SystemExit(f"{label}: exterior entrance moved")
    if outdoor["dest_map"] != indoor["id"] or outdoor["dest_warp_id"] != "0":
        raise SystemExit(f"{label}: exterior warp target mismatch")
    if len(indoor["warp_events"]) != len(exits):
        raise SystemExit(f"{label}: wrong exit tile count")
    if {(w["x"], w["y"]) for w in indoor["warp_events"]} != set(exits):
        raise SystemExit(f"{label}: interior exit coordinates mismatch")
    if any(w["dest_map"] != area["id"] or w["dest_warp_id"] != str(index)
           for w in indoor["warp_events"]):
        raise SystemExit(f"{label}: return warp mismatch")
    indoor_layout = next(item for item in registry["layouts"] if item["id"] == indoor["layout"])
    for w in indoor["warp_events"]:
        if not (0 <= w["x"] < indoor_layout["width"] and 0 <= w["y"] < indoor_layout["height"]):
            raise SystemExit(f"{label}: exit outside interior layout")
print("Verified paired building and ship warps and interior exit bounds")
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
    .string "Welcome to MERIDIAN.\\nThe natives call it AEVOR.$"

MeridianLandingCamp_Text_Quartermaster:
    .string "Supplies are limited.\\nStay near camp.$"
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
