#!/usr/bin/env python3
"""Render multi-tile scenery over Landing Camp's existing terrain study.

Source-art preview only; not GBA metatiles or game collision definitions.
Run tools/generate_landing_camp_tiles.py first. Requires Pillow.
"""
from pathlib import Path
from PIL import Image, ImageDraw
import random
import json

ROOT = Path("build/landing_camp_art")
BASE = ROOT / "camp_scene_study.png"
if not BASE.exists():
    raise SystemExit("Missing terrain preview; run generate_landing_camp_tiles.py first")
im = Image.open(BASE).convert("RGB")
d = ImageDraw.Draw(im)
rng = random.Random(2047)
C = {
    "outline": "#273d39", "deep": "#315646", "leaf": "#487d52",
    "light": "#80a46a", "highlight": "#a4b77c",
    "bark": "#5c4b42", "wood": "#986f4d", "wood_light": "#c19866",
    "shadow": "#44564a", "canvas_dark": "#82755e",
    "canvas": "#b9a582", "canvas_light": "#e1cc9c",
    "earth": "#80664f", "water": "#326e92",
    "foam": "#93c2b5", "stone": "#8b9383",
}
placements = []

def pine(tx, ty, scale=1):
    x, y = tx*16, ty*16
    w, h = 28*scale, 43*scale
    # Broad canopy with readable layered silhouette and trunk.
    d.ellipse((x+2*scale,y+h-9*scale,x+w+6*scale,y+h+1*scale),fill=C["shadow"])
    d.rectangle((x+13*scale,y+23*scale,x+18*scale,y+41*scale),fill=C["bark"])
    d.line((x+15*scale,y+25*scale,x+15*scale,y+39*scale),fill=C["wood"])
    for i,(top,bottom,width) in enumerate(((1,21,13),(11,32,17),(22,40,19))):
        center=x+16*scale
        d.polygon([(center,y+top*scale),(center-width*scale,y+bottom*scale),
                   (center+width*scale,y+bottom*scale)],fill=C["outline"])
        d.polygon([(center,y+(top+2)*scale),(center-(width-3)*scale,y+(bottom-3)*scale),
                   (center+(width-3)*scale,y+(bottom-3)*scale)],fill=C["deep"])
        d.line((center-5*scale,y+(top+8)*scale,center+2*scale,y+(top+5)*scale),
               fill=C["light"],width=scale)
    placements.append({"type":"pine","x":tx,"y":ty,"scale":scale,"collision":"solid canopy/trunk footprint requires map authoring"})

def tent(tx,ty,scale=1):
    x,y=tx*16,ty*16
    s=scale
    # 48x48 px at scale 1: three-metatile wide tent with a legible entrance.
    d.ellipse((x+2*s,y+35*s,x+49*s,y+47*s),fill=C["shadow"])
    d.polygon([(x+1*s,y+34*s),(x+24*s,y+3*s),(x+47*s,y+34*s),
               (x+43*s,y+40*s),(x+5*s,y+40*s)],fill=C["outline"])
    d.polygon([(x+4*s,y+33*s),(x+24*s,y+6*s),(x+44*s,y+33*s),
               (x+40*s,y+37*s),(x+8*s,y+37*s)],fill=C["canvas"])
    d.polygon([(x+24*s,y+6*s),(x+44*s,y+33*s),(x+40*s,y+37*s),
               (x+24*s,y+30*s)],fill=C["canvas_dark"])
    d.line((x+24*s,y+7*s,x+24*s,y+38*s),fill=C["canvas_light"],width=s)
    d.polygon([(x+16*s,y+36*s),(x+24*s,y+20*s),(x+32*s,y+36*s)],fill=C["outline"])
    d.line((x+7*s,y+36*s,x+2*s,y+42*s),fill=C["wood_light"],width=s)
    d.line((x+41*s,y+36*s,x+47*s,y+42*s),fill=C["wood_light"],width=s)
    placements.append({"type":"tent","x":tx,"y":ty,"scale":scale,"collision":"solid tent body; entrance needs a passable event"})

def ground_transition():
    # Irregular shoreline foam and wet soil accents over the existing straight edge.
    for tx in range(18,30):
        x=tx*16
        offset=(tx*7)%5
        y=14*16+5+offset
        d.line((x+1,y,x+5,y-1,x+9,y+1,x+14,y),fill=C["foam"],width=1)
        d.point((x+((tx*3)%12),y+3),fill=C["water"])
    placements.append({"type":"shoreline_detail","region":"southeast","collision":"water impassability not yet authored"})

# Deliberate edge framing; keep a clear walkable corridor between tents.
for tx,ty,scale in ((0,1,1),(3,0,1),(7,1,1),(22,0,1),(26,1,1),
                    (0,11,1),(3,16,1),(25,12,1),(27,9,1)):
    pine(tx,ty,scale)
for tx,ty in ((7,5),(17,5),(19,10)):
    tent(tx,ty)
ground_transition()

# Small clustered stones and grass tufts, not random single-pixel noise.
for tx,ty in ((5,6),(13,3),(24,6),(4,13),(16,14),(22,13)):
    x,y=tx*16+5,ty*16+7
    d.ellipse((x,y,x+10,y+5),fill=C["shadow"])
    d.polygon([(x+1,y+2),(x+4,y-2),(x+9,y+1),(x+8,y+4)],fill=C["stone"])
for tx,ty in ((6,5),(15,5),(21,7),(4,10),(9,14),(17,13)):
    x,y=tx*16+6,ty*16+7
    d.line((x,y+6,x-2,y+1),fill=C["deep"])
    d.line((x+1,y+6,x+2,y),fill=C["light"])
    d.line((x+2,y+6,x+5,y+2),fill=C["deep"])

# The art is composited in RGB; enforce the same 16-color preview constraint.
im=im.quantize(colors=16,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE).convert("RGB")
im.save(ROOT/"camp_scene_quality_v2.png")
im.resize((im.width*2,im.height*2),Image.Resampling.NEAREST).save(ROOT/"camp_scene_quality_v2_2x.png")
(ROOT/"scene_quality_manifest.json").write_text(json.dumps({
    "status":"preview only; not integrated into GBA",
    "size_pixels":list(im.size),
    "colors":len(set(im.getdata())),
    "features":placements,
},indent=2)+"\n")
print("Rendered quality v2:",im.size,"palette colors:",len(set(im.getdata())))
