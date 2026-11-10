#!/usr/bin/env python3
"""Export an editable, numbered Shady Forest metatile reference sheet.

Not a map or a replacement tileset. Porytiles can compile newly authored
layer PNGs after they are designed and approved.
"""
from pathlib import Path
import json
import struct
from PIL import Image,ImageDraw

root=Path(__file__).resolve().parents[1]
src=root/"data/tilesets/secondary/meridian_shady_forest"
stage=root/"build/meridian_shady_forest_staging"
dest=root/"build/meridian_authoring_tools"
dest.mkdir(parents=True,exist_ok=True)
metas=struct.unpack("<4096H",(src/"metatiles.bin").read_bytes())
raw=(stage/"tiles.4bpp").read_bytes()
assert len(raw)==512*32
primary=Image.open(root/"data/tilesets/primary/general/tiles.png").convert("P")
def palette(p):
    lines=p.read_text().splitlines()
    assert lines[0]=="JASC-PAL"
    return [tuple(map(int,x.split())) for x in lines[3:19]]
pal={}
for i in range(6):
    pal[i]=palette(root/f"data/tilesets/primary/general/palettes/{i:02d}.pal")
for i in range(6,16):
    p=stage/f"palettes/{i:02d}.pal"
    pal[i]=palette(p if p.exists() else stage/"palettes/06.pal")
def color(ref,x,y):
    tile=ref&1023
    if ref&0x400:x=7-x
    if ref&0x800:y=7-y
    p=(ref>>12)&15
    if tile<512:
        width=primary.width//8
        c=primary.getpixel(((tile%width)*8+x,(tile//width)*8+y))
    else:
        n=tile-512
        b=raw[n*32+y*4+x//2]
        c=(b>>(4*(x%2)))&15
    return pal[p][c] if c else None
sheet=Image.new("RGB",(16*48,32*48),(32,37,42))
draw=ImageDraw.Draw(sheet)
for n in range(512):
    x=(n%16)*48+8
    y=(n//16)*48+6
    for layer in range(2):
        for slot in range(4):
            ref=metas[n*8+layer*4+slot]
            for py in range(8):
                for px in range(8):
                    c=color(ref,px,py)
                    if c is not None:
                        sheet.putpixel((x+(slot%2)*8+px,y+(slot//2)*8+py),c)
    draw.text((x,y+19),str(512+n),fill=(255,255,255))
sheet.save(dest/"shady_forest_numbered_metatiles.png")
manifest={
 "source":"TeamAquasHideout/Team-Aquas-Asset-Repo Shady Forest Secondary",
 "engine_symbol":"gTileset_MeridianShadyForest",
 "primary":"gTileset_General",
 "available_secondary_metatiles":512,
 "output":"shady_forest_numbered_metatiles.png",
 "note":"Authoring reference only; IDs are engine metatile IDs, not new map placements",
 "credit_file":"build/meridian_shady_forest_staging/credits.md",
 "next_step":"Create editable layer PNGs and compile with Porytiles; validate with the existing pixel QA gates"
}
(dest/"authoring_manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
print(json.dumps(manifest,indent=2))
