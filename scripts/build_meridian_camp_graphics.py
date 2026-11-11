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
# Harbor construction: dedicated wood decking, posts, rope and sea spray.
tile("dock_post", 10, lambda d: (d.rectangle((5,0,10,15),fill=6),d.rectangle((5,0,10,3),fill=8),d.line((4,5,11,5),fill=5)))
tile("dock_rope", 10, lambda d: (d.line((0,7,4,9,9,8,15,5),fill=5),d.line((0,9,4,11,9,10,15,7),fill=6)))
tile("dock_plank", 6, lambda d: ([d.line((0,y,15,y),fill=8) for y in (0,5,11,15)],d.line((5,1,5,4),fill=7),d.line((12,6,12,10),fill=7)))
tile("foam", 10, lambda d: ([d.line((x,y,x+4,y),fill=15) for x,y in ((2,4),(9,10))],d.point((6,6),fill=11)))
tile("ship_cabin", 6, lambda d: (d.rectangle((1,2,14,15),fill=7),d.rectangle((4,5,11,10),fill=11),d.line((0,1,15,1),fill=8)))
tile("ship_pennant", 10, lambda d: (d.line((7,0,7,15),fill=6),d.polygon([(8,1),(15,4),(8,7)],fill=14)))
tile("ship_keel", 10, lambda d: (d.polygon([(0,1),(15,1),(11,12),(4,12)],fill=12),d.line((2,4,13,4),fill=8)))
# Ship is drawn as ONE 7x4 metatile silhouette, then cut into aligned tiles.
# This avoids the repeated hull-strip pattern visible in the November QA preview.
ship = Image.new("P",(112,64),10)
ship.putpalette([v for rgb in COLORS for v in rgb]+[0]*(768-48))
sd=ImageDraw.Draw(ship)
# Reflected water / wake.
sd.arc((0,43,111,61),0,180,fill=11,width=2)
sd.line((7,55,29,57),fill=15,width=2)
sd.line((84,57,106,54),fill=15,width=2)
# Single continuous hull with curved bow and stern.
sd.polygon([(4,40),(103,40),(95,55),(24,57),(11,51)],fill=6)
sd.line((5,40,103,40,95,55,24,57,11,51,5,40),fill=8,width=2)
sd.line((16,48,94,48),fill=7,width=2)
for xx in (26,42,58,74,90):
    sd.ellipse((xx,44,xx+3,47),fill=12)
# Deck and cabin.
sd.rectangle((22,33,90,40),fill=7)
sd.rectangle((68,24,87,34),fill=6)
sd.rectangle((72,27,83,32),fill=11)
sd.line((67,23,88,23),fill=8,width=2)
# Main mast and triangular sails.
sd.rectangle((53,3,56,40),fill=6)
sd.polygon([(52,6),(17,36),(52,36)],fill=15)
sd.polygon([(58,10),(88,36),(58,36)],fill=5)
sd.line((18,36,88,36),fill=8,width=2)
sd.line((54,3,54,40),fill=8)
sd.polygon([(57,3),(74,7),(57,11)],fill=14)
# Open-water ship cells need actual water movement rather than a flat fill.
for sy in range(4):
    for sx in range(7):
        region=ship.crop((sx*16,sy*16,sx*16+16,sy*16+16))
        if len(set(region.getdata()))==1:
            px=sx*16+3+((sx*3+sy)%6)
            py=sy*16+5+((sx+sy*2)%6)
            sd.line((px,py,px+5,py),fill=11)
            sd.point((px+2,py+2),fill=15)
for qy in range(4):
    for qx in range(7):
        ART[f"vessel_{qx}_{qy}"]=ship.crop((qx*16,qy*16,qx*16+16,qy*16+16))
# Directional shoreline geometry: all four cardinal banks, not one generic
# repeated horizontal edge. These are tile art, not collision overrides.
tile("shore_north", 10, lambda d: (d.polygon([(0,0),(15,0),(15,5),(10,7),(5,5),(0,8)],fill=5),d.line((0,9,5,6,10,8,15,6),fill=11)))
tile("shore_south", 10, lambda d: (d.polygon([(0,9),(5,7),(10,9),(15,6),(15,15),(0,15)],fill=5),d.line((0,8,5,6,10,8,15,5),fill=11)))
tile("shore_west", 10, lambda d: (d.polygon([(0,0),(7,0),(9,5),(7,10),(10,15),(0,15)],fill=5),d.line((8,0,10,5,8,10,11,15),fill=11)))
tile("shore_east", 10, lambda d: (d.polygon([(9,0),(15,0),(15,15),(8,15),(6,10),(8,5)],fill=5),d.line((8,0,7,5,5,10,7,15),fill=11)))
tile("shore_nw", 10, lambda d: (d.polygon([(0,0),(15,0),(15,5),(9,7),(7,15),(0,15)],fill=5),d.arc((4,2,17,16),180,270,fill=11)))
tile("shore_ne", 10, lambda d: (d.polygon([(0,0),(15,0),(15,15),(8,15),(6,8),(0,5)],fill=5),d.arc((-2,2,11,16),270,360,fill=11)))
tile("shore_sw", 10, lambda d: (d.polygon([(0,0),(7,0),(9,7),(15,9),(15,15),(0,15)],fill=5),d.arc((4,-2,17,11),90,180,fill=11)))
tile("shore_se", 10, lambda d: (d.polygon([(8,0),(15,0),(15,15),(0,15),(0,9),(6,7)],fill=5),d.arc((-2,-2,11,11),0,90,fill=11)))
# Cliff strata and waterfall segments authored as contiguous vertical textures.
tile("cliff_crack", 12, lambda d: (d.line((4,0,7,5,5,9,10,15),fill=6,width=2),d.line((13,0,11,4,14,8),fill=13)))
tile("cliff_ledge", 12, lambda d: (d.polygon([(0,0),(15,0),(15,4),(10,6),(4,5),(0,7)],fill=4),d.line((0,7,4,5,10,6,15,4),fill=5)))
tile("cliff_moss", 12, lambda d: (d.polygon([(0,0),(7,0),(10,3),(6,6),(0,4)],fill=2),d.line((3,7,1,14),fill=6)))
tile("falls_top", 10, lambda d: (d.rectangle((2,0,13,15),fill=11),d.line((4,2,4,15),fill=15),d.line((10,0,9,15),fill=15)))
tile("falls_middle", 10, lambda d: (d.rectangle((2,0,13,15),fill=11),d.line((5,0,4,15),fill=15),d.line((10,0,11,15),fill=15)))
tile("falls_bottom", 10, lambda d: (d.rectangle((2,0,13,10),fill=11),d.line((5,0,4,10),fill=15),d.ellipse((0,8,15,15),fill=15),d.line((0,14,15,14),fill=11)))
# 3x3 irregular canopy pieces for the deep forest. Individual quadrants share
# a single master drawing so seams cannot split between adjacent tiles.
for bloom in (False, True):
    prefix="ancient_blossom" if bloom else "ancient_forest"
    crown=Image.new("P",(48,48),1)
    crown.putpalette([v for rgb in COLORS for v in rgb]+[0]*(768-48))
    d=ImageDraw.Draw(crown)
    d.rectangle((21,30,28,47),fill=6)
    d.line((23,31,23,47),fill=8,width=2)
    base=14 if bloom else 2
    light=15 if bloom else 3
    shade=7 if bloom else 1
    for bbox in ((3,16,27,38),(18,8,44,34),(7,3,32,28),(19,20,46,42)):
        d.ellipse(bbox,fill=shade)
    for bbox in ((4,12,29,34),(18,6,43,31),(9,2,32,26),(19,17,44,39)):
        d.ellipse(bbox,fill=base)
    for bbox in ((8,10,18,18),(23,9,33,17),(15,21,27,29),(29,24,39,31)):
        d.ellipse(bbox,fill=light)
    for xx,yy in ((5,26),(12,5),(30,4),(42,24),(23,38),(37,13)):
        d.rectangle((xx,yy,xx+2,yy+2),fill=light)
    for qy in range(3):
        for qx in range(3):
            ART[f"{prefix}_{qx}_{qy}"]=crown.crop((qx*16,qy*16,qx*16+16,qy*16+16))
# Ground details and connected path transitions. Keep all decoration passable.
tile("grass_flowers", 2, lambda d: (d.point((3,4),fill=15),d.point((4,4),fill=14),d.point((11,10),fill=15),d.point((12,10),fill=14),d.line((3,6,3,8),fill=1)))
tile("grass_ferns", 2, lambda d: (d.line((4,14,6,4,8,14),fill=1),d.line((6,8,2,6),fill=3),d.line((6,10,11,7),fill=3)))
tile("grass_pebbles", 2, lambda d: (d.ellipse((3,10,6,12),fill=4),d.ellipse((11,4,13,6),fill=5)))
tile("path_stones", 4, lambda d: (d.ellipse((2,2,5,4),fill=5),d.ellipse((10,10,14,12),fill=6),d.point((7,7),fill=5)))
tile("path_edge_left", 4, lambda d: (d.line((0,0,0,15),fill=3),d.line((2,0,2,15),fill=5),d.point((10,9),fill=5)))
tile("path_edge_right", 4, lambda d: (d.line((15,0,15,15),fill=3),d.line((13,0,13,15),fill=5),d.point((4,7),fill=5)))
tile("path_edge_top", 4, lambda d: (d.line((0,0,15,0),fill=3),d.line((0,2,15,2),fill=5)))
tile("path_edge_bottom", 4, lambda d: (d.line((0,15,15,15),fill=3),d.line((0,13,15,13),fill=5)))
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
        elif ch=="~":
            # Dock remains over water, but its edge should not become sand.
            land=lambda xx,yy: (0<=xx<W and 0<=yy<H and PLAN["rows"][yy][xx] not in "~D")
            n,south=land(x,y-1),land(x,y+1)
            west,east=land(x-1,y),land(x+1,y)
            if n and west: grid[y][x]="shore_nw"
            elif n and east: grid[y][x]="shore_ne"
            elif south and west: grid[y][x]="shore_sw"
            elif south and east: grid[y][x]="shore_se"
            elif n: grid[y][x]="shore_north"
            elif south: grid[y][x]="shore_south"
            elif west: grid[y][x]="shore_west"
            elif east: grid[y][x]="shore_east"
# Scatter non-repeating grass details only on ordinary ground; leave
# authored clearings, building footprints, forest and collision unchanged.
for y,row in enumerate(PLAN["rows"]):
    for x,ch in enumerate(row):
        if ch==".":
            selector=(x*17+y*31+x*y*3)%47
            if selector==0: grid[y][x]="grass_flowers"
            elif selector==7: grid[y][x]="grass_ferns"
            elif selector==19: grid[y][x]="grass_pebbles"
        elif ch=="=":
            neighbors=lambda xx,yy: 0<=xx<W and 0<=yy<H and PLAN["rows"][yy][xx] in "=+A12345"
            if (x*11+y*7)%13==0: grid[y][x]="path_stones"
            elif neighbors(x,y-1) and neighbors(x,y+1):
                if not neighbors(x-1,y): grid[y][x]="path_edge_left"
                elif not neighbors(x+1,y): grid[y][x]="path_edge_right"
            elif neighbors(x-1,y) and neighbors(x+1,y):
                if not neighbors(x,y-1): grid[y][x]="path_edge_top"
                elif not neighbors(x,y+1): grid[y][x]="path_edge_bottom"
# Compose 2x2 tree crowns from four matching quadrants, not isolated dots.
# Only replace forest cells; never overwrite roads, door approaches or warps.
for y in range(1,H-2,3):
    for x in range(1,W-2,3):
        if all(PLAN["rows"][yy][xx]=="T" for yy in (y,y+1) for xx in (x,x+1)):
            prefix = "blossom" if (x*3+y)%11==0 else "forest"
            for qy in range(2):
                for qx in range(2):
                    grid[y+qy][x+qx] = f"{prefix}_crown_{qx}_{qy}"
# Replace repetitive 2x2 circular crowns with large irregular 3x3 trees
# wherever the forest has a fully contiguous footprint.
for y in range(0,H-2,4):
    for x in range(0,W-2,4):
        if all(PLAN["rows"][yy][xx]=="T" for yy in range(y,y+3) for xx in range(x,x+3)):
            prefix="ancient_blossom" if (x*7+y)%13==0 else "ancient_forest"
            for qy in range(3):
                for qx in range(3):
                    grid[y+qy][x+qx]=f"{prefix}_{qx}_{qy}"
# Give cliff boundaries a distinct lip instead of a solid cliff texture.
for y in range(H):
    for x in range(W):
        if PLAN["rows"][y][x]=="^" and y>0 and PLAN["rows"][y-1][x]!="^":
            grid[y][x]="cliff_lip"
# Vary cliff faces by location, preserving continuous rock boundaries.
for y,row in enumerate(PLAN["rows"]):
    for x,ch in enumerate(row):
        if ch!="^": continue
        above = y>0 and PLAN["rows"][y-1][x]=="^"
        below = y+1<H and PLAN["rows"][y+1][x]=="^"
        if not above: grid[y][x]="cliff_ledge"
        elif not below: grid[y][x]="cliff_moss"
        elif (x*7+y*3)%11==0: grid[y][x]="cliff_crack"
        elif (x*5+y)%13==0: grid[y][x]="cliff_shadow"
# Waterfall art is reserved for actual water cells adjacent to rock.
# No invented waterfall is stamped over walkable terrain.
for x in range(1,W-1):
    spans=[]
    for y in range(1,H-1):
        if PLAN["rows"][y][x]=="~" and (PLAN["rows"][y][x-1]=="^" or PLAN["rows"][y][x+1]=="^"):
            spans.append(y)
    for i,y in enumerate(spans):
        if i and y!=spans[i-1]+1: continue
        if len(spans)<3: continue
        grid[y][x]="falls_top" if i==0 else ("falls_bottom" if i==len(spans)-1 else "falls_middle")
# Tent-market indicators only on free land adjacent to the central plaza.
for x,y in ((10,25),(22,26),(27,24)):
    if PLAN["rows"][y][x] in ".=":
        grid[y][x]="tent_roof"
# Ship occupies 14..17: rows 18..20 contain the dock. Never clip hull against
# the pier; assert the entire 7x4 footprint is open water.
# Place complete ship silhouette on the existing water area without altering
# gameplay collision, warp points or the source layout.
for qy in range(4):
    for qx in range(7):
        x,y=2+qx,14+qy
        assert PLAN["rows"][y][x]=="~", ("ship overlaps non-water",x,y)
        grid[y][x]=f"vessel_{qx}_{qy}"
# Coordinate-stable material variants: keep the original architectural modules
# intact, but prevent large uniform terrain and roof slabs. These are authored
# pixel variations, not duplicate metatile IDs or a relaxed QA threshold.
# The variation is keyed to map coordinates so incremental edits remain stable.
VARIANT_MATERIALS = {
    "grass", "grass_dark", "water", "cliff", "roof", "roof_edge",
    "path", "path_edge_top", "path_edge_bottom",
    "path_edge_left", "path_edge_right", "dock",
    "ruins", "cave", "cliff_ledge", "cliff_moss", "shore_east",
}
for base in sorted(VARIANT_MATERIALS):
    if base not in ART: continue
    source=ART[base]
    for v in range(1,5):
        im=source.copy()
        d=ImageDraw.Draw(im)
        # Small palette-consistent texture marks, always confined within the
        # tile (no visible discontinuity at neighboring tile boundaries).
        bx=2+((v*3)%9)
        by=2+((v*5)%9)
        background=source.getpixel((bx,by))
        if base.startswith("grass"):
            ink=3 if background!=3 else 1
        elif base=="water": ink=11
        elif base.startswith("path"): ink=5 if background!=5 else 6
        elif base.startswith("roof"): ink=13 if background!=13 else 12
        elif base=="dock": ink=8 if background!=8 else 7
        else: ink=13 if background!=13 else 6
        d.line((bx,by,bx+2,by),fill=ink)
        d.point((bx+1,by+1),fill=ink)
        ART[f"{base}_material_{v}"]=im
for y in range(H):
    for x in range(W):
        base=grid[y][x]
        if base in VARIANT_MATERIALS:
            # Four-phase checker with deterministic row offsets. No adjacent
            # tiles share the same source texture, including along roof runs.
            phase=(x+2*y)%5
            if phase: grid[y][x]=f"{base}_material_{phase}"
# Production HQ asset, adapted from the approved Aevor reference. Keep its
# own 15-color palette rather than forcing blue metal and gold into grass colors.
hq_image=Image.open(ROOT/"graphics/meridian/landing_camp/headquarters.png")
assert hq_image.mode=="P" and hq_image.size==(96,80)
hq_palette=[tuple(hq_image.getpalette()[i:i+3]) for i in range(0,48,3)]
# Composite sprite transparency over matching camp grass, not the BG backdrop.
hq_image.putdata([15 if value==0 else value for value in hq_image.getdata()])
for yy,row in enumerate(PLAN["rows"]):
    for xx,ch in enumerate(row):
        if ch=="H": grid[yy][xx]="grass" if (xx+2*yy)%5==0 else f"grass_material_{(xx+2*yy)%5}"
for qy in range(5):
    for qx in range(6):
        name=f"headquarters_{qx}_{qy}"
        ART[name]=hq_image.crop((qx*16,qy*16,qx*16+16,qy*16+16))
        if set(ART[name].getdata())!={15}:
            grid[6+qy][25+qx]=name

# Replace the obsolete sailboat with the reference-based expedition vessel.
ship_image=Image.open(ROOT/"graphics/meridian/landing_camp/expedition_ship.png")
assert ship_image.mode=="P" and ship_image.size==(112,48)
ship_palette=[tuple(ship_image.getpalette()[i:i+3]) for i in range(0,48,3)]
# Ship index 0 stays transparent; packed metatiles use an ocean underlay.
for qy in range(4):
    for qx in range(7):
        xx,yy=2+qx,14+qy
        phase=(xx+2*yy)%5
        grid[yy][xx]="water" if phase==0 else f"water_material_{phase}"
for qy in range(3):
    for qx in range(7):
        name=f"expedition_ship_{qx}_{qy}"
        ART[name]=ship_image.crop((qx*16,qy*16,qx*16+16,qy*16+16))
        if set(ART[name].getdata())!={15}: grid[14+qy][2+qx]=name

# Dense forest: complete 3x4 conifers on contiguous forest footprints.
forest_image=Image.open(ROOT/"graphics/meridian/landing_camp/forest_conifer.png")
assert forest_image.mode=="P" and forest_image.size==(48,64)
forest_palette=[tuple(forest_image.getpalette()[i:i+3]) for i in range(0,48,3)]
forest_image.putdata([15 if value==0 else value for value in forest_image.getdata()])
for qy in range(4):
    for qx in range(3):
        ART[f"conifer_{qx}_{qy}"]=forest_image.crop((qx*16,qy*16,qx*16+16,qy*16+16))
for yy,row in enumerate(PLAN["rows"]):
    for xx,ch in enumerate(row):
        if ch=="T":
            phase=(xx+2*yy)%5
            grid[yy][xx]="grass_dark" if phase==0 else f"grass_dark_material_{phase}"
for yy in range(0,H-3,4):
    for xx in range(0,W-2,3):
        if all(PLAN["rows"][y][x]=="T" for y in range(yy,yy+4) for x in range(xx,xx+3)):
            for qy in range(4):
                for qx in range(3):
                    name=f"conifer_{qx}_{qy}"
                    if set(ART[name].getdata())!={15}: grid[yy+qy][xx+qx]=name

# Reference-based expedition modules. Placement and paired entrance coordinates
# follow the settlement arrangement encoded in the navigation source.
module_palettes={}
module_slots={}
module_specs=[
    ("medical_center",10,(17,15),"M"),
    ("research_lab",11,(17,8),"L"),
    ("supply_depot",12,(32,12),"S"),
    ("living_quarters",4,(37,22),"Q"),
    ("provision_store",5,(32,17),None),
]
for yy,row in enumerate(PLAN["rows"]):
    for xx,ch in enumerate(row):
        if ch in "MLSQ":
            phase=(xx+2*yy)%5
            grid[yy][xx]="grass" if phase==0 else f"grass_material_{phase}"
for asset,slot,(ox,oy),zone in module_specs:
    sprite=Image.open(ROOT/f"graphics/meridian/landing_camp/{asset}.png")
    assert sprite.mode=="P" and sprite.width%16==0 and sprite.height%16==0
    module_palettes[str(slot)]=[tuple(sprite.getpalette()[i:i+3]) for i in range(0,48,3)]
    sprite.putdata([15 if value==0 else value for value in sprite.getdata()])
    for qy in range(sprite.height//16):
        for qx in range(sprite.width//16):
            name=f"{asset}_{qx}_{qy}"
            ART[name]=sprite.crop((qx*16,qy*16,qx*16+16,qy*16+16))
            module_slots[name]=slot
            if set(ART[name].getdata())!={15}: grid[oy+qy][ox+qx]=name

# Reference-based environment modules, with their own primary palette slots.
env_specs=[("env_cliff_wall",0),("env_cliff_lip",0),("env_waterfall",1),
           ("env_cave",2),("env_ruins",3),("env_stairs",0),("env_banner",7),("env_shore",1),("env_ocean",1)]
for asset,slot in env_specs:
    sprite=Image.open(ROOT/f"graphics/meridian/landing_camp/{asset}.png")
    assert sprite.mode=="P" and sprite.width%16==0 and sprite.height%16==0
    palette=[tuple(sprite.getpalette()[i:i+3]) for i in range(0,48,3)]
    if str(slot) in module_palettes: assert module_palettes[str(slot)]==palette
    module_palettes[str(slot)]=palette
    sprite.putdata([15 if value==0 else value for value in sprite.getdata()])
    for qy in range(sprite.height//16):
        for qx in range(sprite.width//16):
            name=f"{asset}_{qx}_{qy}"
            ART[name]=sprite.crop((qx*16,qy*16,qx*16+16,qy*16+16))
            module_slots[name]=slot
# Flip variants preserve the authored material while avoiding identical slabs.
for asset in ("env_cliff_wall_0_0","env_cliff_wall_0_1","env_cliff_lip_0_0"):
    ART[asset+"_flip"]=ART[asset].transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    module_slots[asset+"_flip"]=0
shore=ART["env_shore_0_0"]
for direction,rotation in (("north",None),("south",Image.Transpose.ROTATE_180),
                            ("east",Image.Transpose.ROTATE_270),("west",Image.Transpose.ROTATE_90)):
    ART[f"env_shore_{direction}"]=shore.copy() if rotation is None else shore.transpose(rotation)
    module_slots[f"env_shore_{direction}"]=1
# Four distinct ocean metatiles from the authored seamless water patch.
for phase in range(4):
    name=f"env_ocean_{phase}"
    ART[name]=ART[f"env_ocean_{phase%2}_{phase//2}"].copy()
    module_slots[name]=1
for direction in ("north","south","east","west"):
    name=f"env_shore_{direction}"
    ART[name+"_alt"]=ART[name].transpose(Image.Transpose.FLIP_LEFT_RIGHT if direction in ("north","south") else Image.Transpose.FLIP_TOP_BOTTOM)
    module_slots[name+"_alt"]=1
def dock_deck(name, phase, west, north, south):
    """Draw walkable decking with a short fascia above the water."""
    left = 3 if west else 0
    top = 2 if north else 0
    bottom = 11 if south else 15

    def paint(draw):
        draw.rectangle((left, top, 15, bottom), fill=7)
        for y in range(top, bottom + 1, 4):
            draw.line((left, y, 15, y), fill=8)
            if y + 3 <= bottom:
                draw.line((left, y + 3, 15, y + 3), fill=6)
            seam = 4 + (phase * 5 + y * 2) % 10
            if y + 2 <= bottom:
                draw.line((seam, y + 1, seam, y + 2), fill=6)
        if south:
            draw.rectangle((left, 12, 15, 13), fill=6)
            if west or phase == 0:
                post = left + 2
                draw.rectangle((post, 9, post + 2, 15), fill=6)
                draw.line((post, 9, post + 1, 9), fill=5)
        if west:
            draw.line((left, top, left, bottom), fill=6)
            draw.line((left + 1, top, left + 1, bottom), fill=8)

    tile(name, 0, paint)


def paint_campfire(draw):
    draw.ellipse((1, 7, 14, 15), fill=6)
    draw.ellipse((3, 8, 12, 13), fill=12)
    for x, y in ((2, 10), (4, 8), (11, 8), (12, 11), (10, 13), (5, 13)):
        draw.rectangle((x, y, x + 1, y + 1), fill=13)
        draw.point((x, y), fill=5)
    draw.line((5, 11, 10, 8), fill=7, width=2)
    draw.line((5, 9, 10, 12), fill=8, width=2)
    draw.polygon(((6, 11), (5, 6), (7, 7), (9, 1), (9, 6), (11, 5), (10, 11)), fill=8)
    draw.polygon(((7, 11), (7, 8), (9, 5), (9, 9), (10, 10), (9, 11)), fill=5)
    draw.point((7, 3), fill=8)


tile("campfire_ring", 4, paint_campfire)
underlays={}
for yy,row in enumerate(PLAN["rows"]):
    for xx,ch in enumerate(row):
        if ch in "^C":
            base="env_cliff_lip_0_0" if yy==0 or PLAN["rows"][yy-1][xx] not in "^C" else f"env_cliff_wall_0_{yy%2}"
            grid[yy][xx]=base+("_flip" if (xx+yy)%2 else "")
        elif ch=="R":
            phase=(xx+2*yy)%5
            grid[yy][xx]="grass" if phase==0 else f"grass_material_{phase}"
        elif ch=="D":
            west = xx == 0 or row[xx - 1] != "D"
            north = yy == 0 or PLAN["rows"][yy - 1][xx] != "D"
            south = yy + 1 == H or PLAN["rows"][yy + 1][xx] != "D"
            phase = (xx + 2 * yy) % 3
            ocean_phase = xx % 2 + 2 * (yy % 2)
            name = f"dock_deck_{phase}_{int(west)}{int(north)}{int(south)}"
            if west or north or south:
                name += f"_{ocean_phase}"
                underlays[name] = f"env_ocean_{ocean_phase}"
            if name not in ART:
                dock_deck(name, phase, west, north, south)
            grid[yy][xx] = name
        elif ch=="F":
            grid[yy][xx] = "campfire_ring"
        elif ch=="~" and grid[yy][xx].startswith("expedition_ship_"):
            underlays[grid[yy][xx]]=f"env_ocean_{xx%2+2*(yy%2)}"
        elif ch=="~":
            land=lambda x,y: 0<=x<W and 0<=y<H and PLAN["rows"][y][x] not in "~D"
            facing=next((direction for direction,x,y in (("north",xx,yy-1),("south",xx,yy+1),("east",xx+1,yy),("west",xx-1,yy)) if land(x,y)),None)
            grid[yy][xx]=(f"env_shore_{facing}"+("_alt" if (xx+yy)%2 else "")) if facing else f"env_ocean_{xx%2+2*(yy%2)}"
def env_stamp(asset,ox,oy,width,height):
    for qy in range(height):
        for qx in range(width): grid[oy+qy][ox+qx]=f"{asset}_{qx}_{qy}"
env_stamp("env_ruins",29,0,4,4)
env_stamp("env_cave",43,8,3,3)
for ox,oy in ((39,3),(39,11)):
    assert all(PLAN["rows"][y][x]=="^" for y in range(oy,oy+4) for x in range(ox,ox+2))
    env_stamp("env_waterfall",ox,oy,2,4)
env_stamp("env_stairs",41,12,1,2)
for ox in (24,31): env_stamp("env_banner",ox,11,1,2)

# Compose overlapping tree crowns at native resolution, then compile their
# real pixels into metatiles. Transparent corners preserve trees behind them.
# Only contiguous forest footprints qualify: paths and camp structures cannot
# be covered by a canopy or receive accidental forest collision.
forest_source=Image.open(ROOT/"graphics/meridian/landing_camp/forest_conifer.png")
forest_mask=Image.new("L",forest_source.size)
forest_mask.putdata([255 if value else 0 for value in forest_source.getdata()])
forest_canvas=Image.new("P",(W*16,H*16),0)
forest_canvas.putpalette(forest_source.getpalette())
forest_placements=[]
for ty in range(0,H-3,2):
    offset=1 if (ty//2)%2 else 0
    for tx in range(offset,W-2,2):
        if all(PLAN["rows"][y][x]=="T" for y in range(ty,ty+4) for x in range(tx,tx+3)):
            forest_canvas.paste(forest_source,(tx*16,ty*16),forest_mask)
            forest_placements.append([tx,ty])
for ty,row in enumerate(PLAN["rows"]):
    for tx,cell in enumerate(row):
        if cell!="T": continue
        phase=(tx+2*ty)%5
        grid[ty][tx]="grass_dark" if phase==0 else f"grass_dark_material_{phase}"
        part=forest_canvas.crop((tx*16,ty*16,tx*16+16,ty*16+16))
        if not any(part.getdata()): continue
        part.putdata([15 if value==0 else value for value in part.getdata()])
        name=f"env_dense_forest_{tx}_{ty}"
        ART[name]=part
        module_slots[name]=9
        grid[ty][tx]=name

# Identical forest cells share metatile IDs as well as pixel tiles. Preserve
# all building/door IDs independently so behavior cannot spread to a wall.
forest_signatures={}
forest_aliases={}
for name,image in ART.items():
    if name.startswith("env_dense_forest_"):
        forest_aliases[name]=forest_signatures.setdefault(tuple(image.getdata()),name)
for ty,row in enumerate(grid):
    for tx,name in enumerate(row): grid[ty][tx]=forest_aliases.get(name,name)

# Export only cells consumed by the actual map and its underlays. Retired
# studies should not consume metatile IDs in the native game asset export.
used_art={name for row in grid for name in row}|set(underlays.values())
names=[name for name in ART if name in used_art]
atlas=Image.new("P",(16*8,16*((len(names)+7)//8)),0)
atlas.putpalette([v for rgb in COLORS for v in rgb]+[0]*(768-48))
for i,name in enumerate(names):
    atlas.paste(ART[name],((i%8)*16,(i//8)*16))
atlas.save(OUT/"camp_original_metatiles_indexed.png")
(OUT/"metatile_manifest.json").write_text(json.dumps({"palette":COLORS,"palettes":{"6":COLORS,"7":hq_palette,"8":ship_palette,"9":forest_palette,**module_palettes},"tile_palettes":{n:7 if n.startswith("headquarters_") else (8 if n.startswith("expedition_ship_") else (9 if n.startswith("conifer_") else module_slots.get(n,6))) for n in names},"metatiles":{n:i for i,n in enumerate(names)},"underlays":underlays,"forest_placements":forest_placements,"engine_integrated":False},indent=2)+"\n")
preview=Image.new("RGB",(W*16,H*16))
for y in range(H):
    for x in range(W):
        name=grid[y][x]
        if name in underlays:
            preview.paste(ART[underlays[name]].convert("RGB"),(x*16,y*16))
            mask=Image.new("L",(16,16));mask.putdata([255 if value else 0 for value in ART[name].getdata()])
            preview.paste(ART[name].convert("RGB"),(x*16,y*16),mask)
        else:
            preview.paste(ART[name].convert("RGB"),(x*16,y*16))
preview.save(OUT/"camp_48x40_art_direction_preview.png")
# Export the same authored cells to Tiled, the widely used map editor.
# Tiled IDs are 1-based; this TMX is a review/editing asset, NOT GBA map.bin.
import xml.etree.ElementTree as ET
from xml.dom import minidom
collision = json.loads((ROOT / "data/meridian_plans/landing_camp_collision_draft.json").read_text())
assert len(collision["rows"]) == H and all(len(row) == W for row in collision["rows"])
collision["rows"]=[list(row) for row in collision["rows"]]
for yy,row in enumerate(PLAN["rows"]):
    for xx,ch in enumerate(row):
        if ch=="H": collision["rows"][yy][xx]="0"
for yy in range(6,11):
    for xx in range(25,31): collision["rows"][yy][xx]="1" if grid[yy][xx].startswith("headquarters_") else "0"
collision["rows"][10][28]="0"
for yy,row in enumerate(PLAN["rows"]):
    for xx,ch in enumerate(row):
        if ch in "MLSQ": collision["rows"][yy][xx]="0"
for yy in range(H):
    for xx in range(W):
        if grid[yy][xx] in module_slots: collision["rows"][yy][xx]="1"
for key in ("medical_door","research_door","supply_door","quarters_door"):
    dx,dy=PLAN["landmarks"][key]
    collision["rows"][dy][dx]="0"
# Environment footprint collisions: stairs and the ruins floor are traversable.
for yy,row in enumerate(PLAN["rows"]):
    for xx,ch in enumerate(row):
        if ch=="R": collision["rows"][yy][xx]="0"
for qy,row in enumerate(("1111","1001","1001","0000")):
    for qx,value in enumerate(row): collision["rows"][qy][29+qx]=value
for yy in (12,13): collision["rows"][yy][41]="0"
cx,cy=PLAN["landmarks"]["cave_entrance"];collision["rows"][cy][cx]="0"
fire_x, fire_y = PLAN["landmarks"]["campfire"]
collision["rows"][fire_y][fire_x] = "1"
assert PLAN["landmarks"]["hq_door"]==[28,10]
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
