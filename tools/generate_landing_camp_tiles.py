#!/usr/bin/env python3
"""Generate original 16x16 pixel-art terrain studies for Landing Camp.

This is a SOURCE ART atlas, not a game-integrated GBA tileset. Each 16x16
cell must be decomposed into 8x8 tiles, palette-reduced and assigned metatile
behavior before ROM use. No existing map assets are overwritten.
Requires Pillow: python3 -m pip install Pillow
"""
from pathlib import Path
from PIL import Image, ImageDraw
import random

OUT = Path("build/landing_camp_art")
SIZE = 16
COLS = 8
ROWS = 6
COLORS = {
    "grass": (72, 120, 72), "grass_light": (101, 149, 85),
    "grass_dark": (42, 89, 64), "moss": (123, 151, 83),
    "soil": (123, 91, 68), "soil_light": (165, 126, 87),
    "soil_dark": (86, 65, 58), "stone": (116, 124, 115),
    "stone_light": (157, 161, 139), "stone_dark": (78, 94, 91),
    "water": (43, 103, 142), "water_light": (79, 151, 170),
    "water_dark": (32, 75, 114), "wood": (129, 85, 59),
    "wood_light": (177, 126, 76), "wood_dark": (80, 57, 49),
    "canvas": (190, 171, 120), "canvas_light": (221, 202, 153),
    "canvas_dark": (137, 122, 92), "leaf": (49, 112, 73),
    "leaf_light": (95, 155, 84), "leaf_dark": (30, 72, 57),
    "flower": (232, 203, 134),
}
im = Image.new("RGB", (COLS * SIZE, ROWS * SIZE), COLORS["grass"])
draw = ImageDraw.Draw(im)
labels = []

def tile(n, label, base, decoration):
    x, y = (n % COLS) * SIZE, (n // COLS) * SIZE
    draw.rectangle((x, y, x + 15, y + 15), fill=COLORS[base])
    rng = random.Random(1079 + n * 7919)
    decoration(x, y, rng)
    labels.append({"index": n, "name": label, "x": x, "y": y})

def noise(base, accents, count=13):
    def paint(x, y, rng):
        for _ in range(count):
            px, py = rng.randrange(16), rng.randrange(16)
            draw.point((x + px, y + py), fill=COLORS[rng.choice(accents)])
    return paint

def path(x, y, rng):
    draw.polygon([(x, y+3), (x+7,y), (x+15,y+3), (x+15,y+13),
                  (x+8,y+15),(x,y+13)], fill=COLORS["soil"])
    for _ in range(16):
        px,py=rng.randrange(16),rng.randrange(16)
        if im.getpixel((x+px,y+py))==COLORS["soil"]:
            draw.point((x+px,y+py),fill=COLORS[rng.choice(["soil_light","soil_dark"])])

def water(x,y,rng):
    draw.rectangle((x,y,x+15,y+15),fill=COLORS["water"])
    for offset in (2,9,13):
        shift=rng.randrange(5)
        draw.line((x+shift,y+offset,x+shift+5,y+offset),fill=COLORS["water_light"])
    draw.line((x+1,y+6,x+6,y+6),fill=COLORS["water_dark"])

def shoreline(x,y,rng):
    water(x,y,rng)
    draw.polygon([(x,y),(x+15,y),(x+15,y+3),(x+11,y+5),
                  (x+7,y+3),(x+3,y+6),(x,y+4)],fill=COLORS["soil_light"])
    draw.line((x,y+5,x+3,y+7,x+7,y+4,x+11,y+6,x+15,y+4),
              fill=COLORS["stone_light"],width=1)

def cliff(x,y,rng):
    draw.rectangle((x,y,x+15,y+15),fill=COLORS["stone_dark"])
    draw.rectangle((x,y,x+15,y+3),fill=COLORS["grass"])
    draw.line((x,y+4,x+15,y+4),fill=COLORS["stone_light"])
    for i in (2,7,12):
        draw.line((x+i,y+6,x+i-1,y+12),fill=COLORS["stone"])
    draw.line((x+3,y+14,x+12,y+14),fill=COLORS["soil_dark"])

def tree(x,y,rng):
    draw.rectangle((x+6,y+9,x+9,y+15),fill=COLORS["wood_dark"])
    draw.rectangle((x+7,y+9,x+8,y+14),fill=COLORS["wood_light"])
    draw.ellipse((x+1,y+1,x+14,y+12),fill=COLORS["leaf_dark"])
    draw.ellipse((x+2,y+1,x+12,y+9),fill=COLORS["leaf"])
    for px,py in ((5,3),(9,4),(3,7),(11,8)):
        draw.rectangle((x+px,y+py,x+px+2,y+py+1),fill=COLORS["leaf_light"])

def tent(x,y,rng):
    draw.polygon([(x+1,y+12),(x+8,y+2),(x+15,y+12)],fill=COLORS["canvas_dark"])
    draw.polygon([(x+3,y+11),(x+8,y+3),(x+12,y+11)],fill=COLORS["canvas"])
    draw.line((x+8,y+3,x+8,y+12),fill=COLORS["canvas_light"])
    draw.polygon([(x+5,y+12),(x+8,y+7),(x+11,y+12)],fill=COLORS["wood_dark"])
    draw.line((x,y+13,x+15,y+13),fill=COLORS["soil_dark"])

def crate(x,y,rng):
    draw.rectangle((x+2,y+4,x+13,y+14),fill=COLORS["wood_dark"])
    draw.rectangle((x+3,y+5,x+12,y+12),fill=COLORS["wood"])
    draw.line((x+3,y+5,x+12,y+12),fill=COLORS["wood_light"])
    draw.line((x+12,y+5,x+3,y+12),fill=COLORS["wood_light"])

def reeds(x,y,rng):
    noise("grass",["grass_light","grass_dark"],5)(x,y,rng)
    for px in (3,7,12):
        draw.line((x+px,y+14,x+px-1,y+6),fill=COLORS["moss"])
        draw.line((x+px,y+12,x+px+2,y+8),fill=COLORS["grass_light"])

def flowers(x,y,rng):
    noise("grass",["grass_light","grass_dark"],8)(x,y,rng)
    for px,py in ((4,5),(11,10),(7,13)):
        draw.point((x+px,y+py),fill=COLORS["flower"])
        draw.point((x+px+1,y+py),fill=COLORS["canvas_light"])

def stump(x,y,rng):
    draw.ellipse((x+3,y+7,x+12,y+14),fill=COLORS["wood_dark"])
    draw.ellipse((x+3,y+4,x+12,y+10),fill=COLORS["wood"])
    draw.ellipse((x+5,y+6,x+10,y+8),outline=COLORS["wood_light"])

def boulder(x,y,rng):
    draw.polygon([(x+2,y+12),(x+3,y+6),(x+8,y+3),(x+13,y+7),
                  (x+14,y+13)],fill=COLORS["stone_dark"])
    draw.polygon([(x+4,y+7),(x+8,y+4),(x+12,y+7),(x+11,y+10),
                  (x+4,y+10)],fill=COLORS["stone"])
    draw.line((x+5,y+6,x+9,y+5),fill=COLORS["stone_light"])

families=[
    ("meadow", "grass", noise("grass",["grass_light","grass_dark"],12)),
    ("dense meadow","grass",noise("grass",["grass_light","moss","grass_dark"],25)),
    ("moss patch","moss",noise("moss",["grass","grass_dark"],19)),
    ("forest floor","grass_dark",noise("grass_dark",["grass","soil_dark"],22)),
    ("trampled path","grass",path),
    ("packed soil","soil",noise("soil",["soil_light","soil_dark"],20)),
    ("gravel","stone",noise("stone",["stone_light","stone_dark"],25)),
    ("dark gravel","stone_dark",noise("stone_dark",["stone","soil_dark"],20)),
    ("water","water",water),
    ("shore","water",shoreline),
    ("cliff","stone_dark",cliff),
    ("pine tree","grass",tree),
    ("expedition tent","grass",tent),
    ("supply crate","grass",crate),
    ("reeds","grass",reeds),
    ("flowers","grass",flowers),
    ("tree stump","grass",stump),
    ("boulder","grass",boulder),
]
for i in range(COLS*ROWS):
    label,base,fn=families[i%len(families)]
    # Later atlas rows are variations, not duplicates of the same bitmap.
    tile(i,f"{label} variation {i//len(families)+1}",base,fn)
OUT.mkdir(parents=True,exist_ok=True)
# Single shared 16-color study palette, including all terrain families.
# This is an early palette constraint, not yet a validated GBA tileset.
im = im.quantize(colors=16, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).convert("RGB")
im.save(OUT/"terrain_study.png")
import json
(OUT/"manifest.json").write_text(json.dumps({
    "purpose":"original pixel art terrain study; not ROM-integrated",
    "tile_size":16,"columns":COLS,"rows":ROWS,
    "palette_colors":len(set(im.getdata())),
    "tiles":labels,
},indent=2)+"\n")
print(f"Created {OUT/'terrain_study.png'} with {len(labels)} 16x16 studies and {len(set(im.getdata()))} colors")
