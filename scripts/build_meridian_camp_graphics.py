#!/usr/bin/env python3
"""Author original 16-color, 16x16-pixel GBA-compatible camp metatile art.

This is a source-art workbench, not an installed engine tileset. It exports an
indexed PNG atlas and a map preview; integration into tilesets, palettes,
metatile attributes and map blocks is a separate acceptance gate.
"""
from pathlib import Path
import json
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "build/meridian_camp_art"
OUT.mkdir(parents=True, exist_ok=True)
PLAN = json.loads((ROOT / "data/meridian_plans/landing_camp_arrival.json").read_text())
W, H = PLAN["width"], PLAN["height"]
assert (W, H) == (48, 40)
# One 16-color palette; color 0 is reserved for transparency.
COLORS = [
    (0, 0, 0), (64, 111, 67), (84, 139, 78), (123, 163, 93),
    (180, 164, 109), (210, 190, 137), (111, 85, 69), (150, 108, 79),
    (193, 139, 96), (69, 92, 114), (91, 137, 156), (146, 185, 184),
    (75, 74, 88), (129, 127, 135), (220, 160, 174), (246, 207, 207),
]
ART = {}
def tile(name, ground, paint):
    im = Image.new("P", (16, 16), ground)
    im.putpalette([v for rgb in COLORS for v in rgb] + [0] * (768 - 48))
    d = ImageDraw.Draw(im)
    paint(d)
    ART[name] = im
def noop(d): pass
tile("grass", 2, lambda d: [d.point((x,y), fill=c) for x,y,c in [(2,3,3),(12,8,1),(7,12,3),(14,2,3)]])
tile("grass_dark", 1, lambda d: [d.line((x, y, x+2, y-2), fill=2) for x,y in [(3,7),(11,4),(7,14)]])
tile("path", 4, lambda d: [d.point((x,y), fill=5) for x,y in [(3,4),(11,9),(7,13),(14,2)]])
tile("shore", 5, lambda d: (d.polygon([(0,11),(5,9),(10,11),(15,8),(15,15),(0,15)],fill=10),d.line((0,10,5,8,10,10,15,7),fill=11)))
tile("water", 10, lambda d: [d.line((x,y,x+4,y),fill=11) for x,y in [(2,4),(9,11)]])
tile("dock", 6, lambda d: ([d.line((0,y,15,y),fill=8) for y in (0,7,15)], [d.line((x,1,x,6),fill=7) for x in (4,12)]))
tile("roof", 12, lambda d: ([d.line((0,y,15,y),fill=13) for y in (2,9)],d.line((0,15,15,15),fill=6)))
tile("roof_edge", 12, lambda d: (d.rectangle((0,10,15,15),fill=6),d.line((0,9,15,9),fill=8)))
tile("wall", 5, lambda d: (d.line((0,0,15,0),fill=8),d.line((0,15,15,15),fill=6),d.line((7,0,7,15),fill=4)))
tile("window", 5, lambda d: (d.rectangle((3,2,12,12),fill=6),d.rectangle((5,4,10,10),fill=11),d.line((7,4,7,10),fill=6)))
tile("door", 5, lambda d: (d.rectangle((3,0,12,15),fill=6),d.rectangle((5,2,10,15),fill=12),d.point((9,9),fill=8)))
tile("cliff", 12, lambda d: ([d.line((x,0,x-3,15),fill=13) for x in (4,12)],d.line((0,0,15,0),fill=4)))
tile("ruins", 13, lambda d: (d.rectangle((2,3,13,15),fill=12),d.line((3,7,12,7),fill=5),d.line((7,4,7,15),fill=5)))
tile("tree_top", 1, lambda d: (d.ellipse((0,0,15,15),fill=2),d.ellipse((3,2,12,11),fill=3)))
tile("tree_bloom", 1, lambda d: (d.ellipse((0,0,15,15),fill=14),d.ellipse((4,3,12,12),fill=15)))
tile("tree_trunk", 1, lambda d: (d.rectangle((6,0,10,15),fill=6),d.line((7,0,7,15),fill=8)))
tile("tent", 4, lambda d: (d.polygon([(0,14),(8,1),(15,14)],fill=13),d.line((8,1,8,14),fill=5)))
tile("fire", 4, lambda d: (d.ellipse((2,11,14,15),fill=6),d.polygon([(5,12),(8,2),(11,12)],fill=8),d.polygon([(7,12),(9,6),(10,12)],fill=5)))
tile("cave", 12, lambda d: (d.ellipse((1,0,14,15),fill=13),d.ellipse((4,4,12,15),fill=0)))
tile("ship_hull", 10, lambda d: (d.polygon([(0,4),(15,4),(12,14),(3,14)],fill=6),d.line((2,5,13,5),fill=8)))
tile("ship_deck", 6, lambda d: (d.line((0,0,15,0),fill=8),d.line((0,15,15,15),fill=12)))
tile("ship_sail", 10, lambda d: (d.polygon([(8,0),(8,15),(1,13)],fill=15),d.line((8,0,8,15),fill=6)))
names = list(ART)
atlas = Image.new("P", (16*8, 16*((len(names)+7)//8)), 0)
atlas.putpalette([v for rgb in COLORS for v in rgb] + [0]*(768-48))
for i,name in enumerate(names):
    atlas.paste(ART[name], ((i%8)*16,(i//8)*16))
atlas.save(OUT / "camp_original_metatiles_indexed.png")
(OUT / "metatile_manifest.json").write_text(json.dumps({"palette":COLORS,"metatiles":{n:i for i,n in enumerate(names)},"engine_integrated":False},indent=2)+"\\n")
# Render 48x40 preview using coordinate-aware buildings and landscape features.
grid = [["grass" for x in range(W)] for y in range(H)]
legend = {".":"grass","=":"path","D":"dock","+":"path","A":"path","F":"fire",
"M":"wall","L":"wall","H":"wall","S":"wall","Q":"wall","R":"ruins",
"C":"cave","T":"grass_dark","^":"cliff","~":"water",
"1":"path","2":"path","3":"path","4":"path","5":"path"}
for y,row in enumerate(PLAN["rows"]):
    for x,ch in enumerate(row):
        grid[y][x] = legend[ch]
# Connected zone roof geometry: top row roof, second roof, bottom wall;
# visible door coordinates remain untouched.
for code in "MLHSQ":
    coords = [(x,y) for y,row in enumerate(PLAN["rows"]) for x,ch in enumerate(row) if ch==code]
    if not coords: continue
    top = min(y for x,y in coords)
    bottom = max(y for x,y in coords)
    for x,y in coords:
        grid[y][x] = "roof" if y < bottom-1 else ("roof_edge" if y==bottom-1 else "wall")
for name in ("medical_door","research_door","hq_door","supply_door","quarters_door"):
    x,y = PLAN["landmarks"][name]
    grid[y][x] = "door"
for y,row in enumerate(PLAN["rows"]):
    for x,ch in enumerate(row):
        if ch=="T" and x%3==1 and y%3==1:
            grid[y][x]="tree_bloom" if (x+y)%7==0 else "tree_top"
        elif ch=="~" and any(0<=xx<W and PLAN["rows"][y][xx] not in "~" for xx in (x-1,x+1)):
            grid[y][x]="shore"
# Representative ship silhouette on water west of the camp arrival.
for x in range(2,9):
    for y in range(17,20):
        if PLAN["rows"][y][x]=="~":
            grid[y][x] = "ship_deck" if y==17 else "ship_hull"
for x,y in ((4,16),(5,16),(6,16)):
    if PLAN["rows"][y][x]=="~": grid[y][x]="ship_sail"
preview=Image.new("RGB",(W*16,H*16))
for y in range(H):
    for x in range(W):
        preview.paste(ART[grid[y][x]].convert("RGB"),(x*16,y*16))
preview.save(OUT/"camp_48x40_art_direction_preview.png")
print(f"Generated {len(names)} original indexed metatiles and {W}x{H} art preview in {OUT}")
