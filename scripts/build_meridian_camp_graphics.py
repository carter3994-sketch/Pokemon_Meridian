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
# New coherent 2x2 tree canopies, shaded trunk bases and coastal rock edges.
for bloom in (False, True):
    prefix = "blossom" if bloom else "forest"
    crown = Image.new("P", (32, 32), 0)
    crown.putpalette([v for rgb in COLORS for v in rgb] + [0]*(768-48))
    d = ImageDraw.Draw(crown)
    d.ellipse((1,3,30,29), fill=14 if bloom else 1)
    d.ellipse((4,1,26,24), fill=15 if bloom else 2)
    d.ellipse((7,7,23,26), fill=14 if bloom else 3)
    for i,(x,y) in enumerate(((8,9),(21,6),(14,17),(25,20),(5,22))):
        d.rectangle((x,y,x+2,y+2), fill=(15 if i%2 else 14) if bloom else (2 if i%2 else 1))
    for qy in range(2):
        for qx in range(2):
            ART[f"{prefix}_crown_{qx}_{qy}"] = crown.crop((qx*16,qy*16,qx*16+16,qy*16+16))
tile("cliff_lip", 3, lambda d: (d.polygon([(0,8),(5,6),(10,9),(15,7),(15,15),(0,15)],fill=12),d.line((0,8,5,6,10,9,15,7),fill=5)))
tile("cliff_shadow", 12, lambda d: (d.rectangle((0,0,4,15),fill=13),d.line((8,1,5,14),fill=6)))
tile("waterfall", 10, lambda d: ([d.line((x,0,x-1,15),fill=11) for x in (3,8,13)],d.line((0,15,15,15),fill=15)))
tile("ship_bow", 10, lambda d: (d.polygon([(0,5),(15,1),(12,13),(3,15)],fill=6),d.line((0,5,15,1),fill=8)))
tile("ship_stern", 10, lambda d: (d.polygon([(0,1),(15,5),(12,15),(3,13)],fill=6),d.line((0,1,15,5),fill=8)))
tile("tent_roof", 4, lambda d: (d.polygon([(0,15),(8,0),(15,15)],fill=13),d.line((8,1,8,15),fill=8)))
# Cohesive expedition-building facade modules with shading and material seams.
tile("roof_ridge", 12, lambda d: (d.polygon([(0,10),(8,1),(15,10),(15,15),(0,15)],fill=13),d.line((0,10,8,1,15,10),fill=8)))
tile("roof_left", 12, lambda d: (d.polygon([(0,14),(15,2),(15,15),(0,15)],fill=13),d.line((0,14,15,2),fill=8)))
tile("roof_right", 12, lambda d: (d.polygon([(0,2),(15,14),(15,15),(0,15)],fill=13),d.line((0,2,15,14),fill=8)))
tile("facade_pillar", 5, lambda d: (d.rectangle((2,0,5,15),fill=7),d.line((2,0,2,15),fill=6),d.line((5,0,5,15),fill=8)))
tile("foundation", 12, lambda d: (d.rectangle((0,0,15,4),fill=6),d.line((0,5,15,5),fill=8),d.line((0,12,15,12),fill=13)))
tile("awning", 8, lambda d: (d.polygon([(0,2),(15,2),(13,12),(2,12)],fill=13),d.line((0,2,15,2),fill=5),d.line((2,12,13,12),fill=6)))
tile("ship_mast", 10, lambda d: (d.rectangle((7,0,9,15),fill=6),d.line((4,10,12,10),fill=8)))
tile("ship_rigging", 10, lambda d: (d.line((0,15,8,0,15,15),fill=5),d.line((8,0,8,15),fill=6)))
tile("water_edge_left", 10, lambda d: (d.polygon([(0,0),(6,0),(9,4),(7,9),(10,15),(0,15)],fill=5),d.line((6,0,9,4,7,9,10,15),fill=11)))
tile("water_edge_right", 10, lambda d: (d.polygon([(10,0),(15,0),(15,15),(8,15),(6,9),(9,4)],fill=5),d.line((10,0,9,4,6,9,8,15),fill=11)))
# Expedition architectural vocabulary: readable signage and structural depth.
tile("hq_banner", 5, lambda d: (d.rectangle((2,1,13,13),fill=12),d.rectangle((4,3,11,10),fill=8),d.line((7,3,7,10),fill=5)))
tile("research_emblem", 5, lambda d: (d.rectangle((2,1,13,13),fill=6),d.ellipse((4,3,11,10),outline=11),d.line((4,10,11,3),fill=11)))
tile("medical_cross", 5, lambda d: (d.rectangle((2,1,13,13),fill=15),d.rectangle((7,3,9,11),fill=14),d.rectangle((4,6,12,8),fill=14)))
tile("supply_crates", 5, lambda d: (d.rectangle((1,7,8,15),fill=7),d.rectangle((8,4,15,15),fill=6),d.line((8,4,15,15),fill=8)))
tile("quarters_lantern", 5, lambda d: (d.line((8,0,8,4),fill=6),d.rectangle((5,4,11,12),fill=8),d.rectangle((6,5,10,10),fill=5)))
tile("porch_floor", 6, lambda d: ([d.line((0,y,15,y),fill=8) for y in (4,10)],d.line((7,0,7,15),fill=7)))
tile("roof_gable", 12, lambda d: (d.polygon([(0,15),(8,1),(15,15)],fill=13),d.line((0,15,8,1,15,15),fill=8),d.line((3,13,12,13),fill=6)))
names = list(ART)
atlas = Image.new("P", (16*8, 16*((len(names)+7)//8)), 0)
atlas.putpalette([v for rgb in COLORS for v in rgb] + [0]*(768-48))
for i,name in enumerate(names):
    atlas.paste(ART[name], ((i%8)*16,(i//8)*16))
atlas.save(OUT / "camp_original_metatiles_indexed.png")
(OUT / "metatile_manifest.json").write_text(json.dumps({"palette":COLORS,"metatiles":{n:i for i,n in enumerate(names)},"engine_integrated":False},indent=2)+"\n")
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
# Art-direction pass: break up continuous walls with window bays and roof trim.
# Preserve exact door coordinates and the existing navigation grid.
for code in "MLHSQ":
    coords = [(x,y) for y,row in enumerate(PLAN["rows"]) for x,ch in enumerate(row) if ch==code]
    if not coords: continue
    xs = sorted({x for x,y in coords})
    top = min(y for x,y in coords)
    bottom = max(y for x,y in coords)
    for x,y in coords:
        if y == bottom and x in xs[2:-2] and (x-xs[0])%3==1:
            grid[y][x] = "window"
        if y == top and x in (xs[0],xs[-1]):
            grid[y][x] = "roof_edge"
# Distinguish roof ends and facade support bays using building geometry.
for code in "MLHSQ":
    coords = [(x,y) for y,row in enumerate(PLAN["rows"]) for x,ch in enumerate(row) if ch==code]
    if not coords: continue
    xs = sorted({x for x,y in coords})
    top = min(y for x,y in coords)
    bottom = max(y for x,y in coords)
    for x,y in coords:
        if y == top:
            if x == xs[0]: grid[y][x] = "roof_left"
            elif x == xs[-1]: grid[y][x] = "roof_right"
            elif (x-xs[0])%4 == 2: grid[y][x] = "roof_ridge"
        elif y == bottom and x in (xs[0],xs[-1]):
            grid[y][x] = "facade_pillar"
# Building-specific signs above entry doors; no warp coordinates are moved.
signs = {
    "medical_door":"medical_cross",
    "research_door":"research_emblem",
    "hq_door":"hq_banner",
    "supply_door":"supply_crates",
    "quarters_door":"quarters_lantern",
}
for name,sign in signs.items():
    x,y=PLAN["landmarks"][name]
    if y>0 and PLAN["rows"][y-1][x] in "MLHSQ":
        grid[y-1][x]=sign
# Readable gable roof centered above HQ, while leaving the entrance clear.
hq=[(x,y) for y,row in enumerate(PLAN["rows"]) for x,ch in enumerate(row) if ch=="H"]
if hq:
    y=min(y for x,y in hq)
    xs=sorted({x for x,yy in hq if yy==y})
    grid[y][xs[len(xs)//2]]="roof_gable"
# Expose provisional material count in the workbench metadata for review.
for name in ("medical_door","research_door","hq_door","supply_door","quarters_door"):
    x,y = PLAN["landmarks"][name]
    grid[y][x] = "door"
for y,row in enumerate(PLAN["rows"]):
    for x,ch in enumerate(row):
        if ch=="T" and x%3==1 and y%3==1:
            grid[y][x]="tree_bloom" if (x+y)%7==0 else "tree_top"
        elif ch=="~" and any(0<=xx<W and PLAN["rows"][y][xx] not in "~" for xx in (x-1,x+1)):
            grid[y][x]="shore"
# Compose 2x2 tree crowns from four matching quadrants, not isolated dots.
# Only replace forest cells; never overwrite roads, door approaches or warps.
for y in range(1,H-2,3):
    for x in range(1,W-2,3):
        if all(PLAN["rows"][yy][xx]=="T" for yy in (y,y+1) for xx in (x,x+1)):
            prefix = "blossom" if (x*3+y)%11==0 else "forest"
            for qy in range(2):
                for qx in range(2):
                    grid[y+qy][x+qx] = f"{prefix}_crown_{qx}_{qy}"
# Give cliff boundaries a distinct lip instead of a solid cliff texture.
for y in range(H):
    for x in range(W):
        if PLAN["rows"][y][x]=="^" and y>0 and PLAN["rows"][y-1][x]!="^":
            grid[y][x]="cliff_lip"
# Tent-market indicators only on free land adjacent to the central plaza.
for x,y in ((10,25),(22,26),(27,24)):
    if PLAN["rows"][y][x] in ".=":
        grid[y][x]="tent_roof"
# Representative ship silhouette on water west of the camp arrival.
for x in range(2,9):
    for y in range(17,20):
        if PLAN["rows"][y][x]=="~":
            grid[y][x] = "ship_deck" if y==17 else "ship_hull"
# Make the hull terminate in dedicated bow/stern tiles, not repeating rectangles.
for y in range(17,20):
    for x,graphic in ((2,"ship_stern"),(8,"ship_bow")):
        if PLAN["rows"][y][x]=="~":
            grid[y][x]=graphic
# Add a mast and a small ship silhouette without modifying collision.
for x,y in ((4,16),(5,16),(6,16)):
    if PLAN["rows"][y][x]=="~": grid[y][x]="ship_sail"
preview=Image.new("RGB",(W*16,H*16))
for y in range(H):
    for x in range(W):
        preview.paste(ART[grid[y][x]].convert("RGB"),(x*16,y*16))
preview.save(OUT/"camp_48x40_art_direction_preview.png")
# Export the same authored cells to Tiled, the widely used map editor.
# Tiled IDs are 1-based; this TMX is a review/editing asset, NOT GBA map.bin.
import xml.etree.ElementTree as ET
from xml.dom import minidom
collision = json.loads((ROOT / "data/meridian_plans/landing_camp_collision_draft.json").read_text())
assert len(collision["rows"]) == H and all(len(row) == W for row in collision["rows"])
tmx = ET.Element("map", {
    "version":"1.10","tiledversion":"1.11.2","orientation":"orthogonal",
    "renderorder":"right-down","width":str(W),"height":str(H),
    "tilewidth":"16","tileheight":"16","infinite":"0",
    "nextlayerid":"3","nextobjectid":"1"
})
tileset = ET.SubElement(tmx,"tileset",{"firstgid":"1","name":"MeridianCampOriginal",
    "tilewidth":"16","tileheight":"16","tilecount":str(len(names)),"columns":"8"})
ET.SubElement(tileset,"image",{"source":"camp_original_metatiles_indexed.png",
    "width":str(atlas.width),"height":str(atlas.height)})
def csv_layer(layer_id,name,values):
    layer=ET.SubElement(tmx,"layer",{"id":str(layer_id),"name":name,
        "width":str(W),"height":str(H),"visible":"0" if layer_id==2 else "1"})
    data=ET.SubElement(layer,"data",{"encoding":"csv"})
    data.text=chr(10)+(","+chr(10)).join(",".join(str(values[y*W+x]) for x in range(W)) for y in range(H))+chr(10)
csv_layer(1,"Artwork",[names.index(grid[y][x])+1 for y in range(H) for x in range(W)])
csv_layer(2,"Collision reference (1=blocked)",[int(collision["rows"][y][x]) for y in range(H) for x in range(W)])
(OUT/"camp_48x40_editable.tmx").write_bytes(minidom.parseString(ET.tostring(tmx)).toprettyxml(indent="  ",encoding="utf-8"))

print(f"Generated {len(names)} original indexed metatiles and {W}x{H} art preview in {OUT}")
