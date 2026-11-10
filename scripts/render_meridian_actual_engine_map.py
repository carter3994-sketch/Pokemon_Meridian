#!/usr/bin/env python3
"""Render the *compiled-map inputs* with the registered Shady Forest tileset.

This diagnostic uses real source 4bpp tiles, Gen 3 metatiles and map.bin,
rather than the separate hand-drawn concept preview.
"""
from pathlib import Path
from PIL import Image, ImageDraw
import json
import struct

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"build/meridian_candidate_review"
OUT.mkdir(parents=True,exist_ok=True)
stage=ROOT/"build/meridian_shady_forest_staging"
primary=Image.open(ROOT/"data/tilesets/primary/general/tiles.png").convert("P")
registered=ROOT/"data/tilesets/secondary/meridian_shady_forest"
secondary_image=Image.open(registered/"tiles.png").convert("P") if (registered/"tiles.png").exists() else None
secondary=(stage/"tiles.4bpp").read_bytes()
metas=[
 (ROOT/"data/tilesets/primary/general/metatiles.bin").read_bytes(),
 ((registered/"metatiles.bin") if (registered/"metatiles.bin").exists() else (stage/"metatiles.bin")).read_bytes()
]
metas=[struct.unpack("<"+"H"*(len(b)//2),b) for b in metas]
plan=json.loads((ROOT/"data/meridian_plans/landing_camp_arrival.json").read_text())
map_words=struct.unpack("<"+str(plan["width"]*plan["height"])+"H",
 (ROOT/"data/layouts/MeridianLandingCampPrototype/map.bin").read_bytes())
def pal_file(path):
 lines=path.read_text().splitlines()
 assert lines[0]=="JASC-PAL" and int(lines[2])==16
 return [tuple(map(int,x.split())) for x in lines[3:19]]
pals={}
for i in range(6):
 pals[i]=pal_file(ROOT/f"data/tilesets/primary/general/palettes/{i:02d}.pal")
for i in range(6,16):
 p=(registered/f"palettes/{i:02d}.pal") if (registered/f"palettes/{i:02d}.pal").exists() else (stage/f"palettes/{i:02d}.pal")
 pals[i]=pal_file(p if p.exists() else stage/"palettes/06.pal")
def pixel(tile,px,py):
 if tile<512:
  width=primary.width//8
  return primary.getpixel(((tile%width)*8+px,(tile//width)*8+py))
 index=tile-512
 if secondary_image is not None:
  return secondary_image.getpixel(((index%16)*8+px,(index//16)*8+py))
 if index>=len(secondary)//32:return 0
 b=secondary[index*32+py*4+px//2]
 return (b>>((px%2)*4))&15
image=Image.new("RGB",(plan["width"]*16,plan["height"]*16),(0,0,0))
draw=ImageDraw.Draw(image)
invalid=[]
for y in range(plan["height"]):
 for x in range(plan["width"]):
  map_id=map_words[y*plan["width"]+x]&1023
  bank=0 if map_id<512 else 1
  idx=map_id if bank==0 else map_id-512
  if idx*8+8>len(metas[bank]):
   invalid.append([x,y,map_id]);continue
  for layer in range(2):
   for slot in range(4):
    ref=metas[bank][idx*8+layer*4+slot]
    tile=ref&1023
    flipx=bool(ref&0x400);flipy=bool(ref&0x800)
    pal=(ref>>12)&15
    for py in range(8):
     for px in range(8):
      c=pixel(tile,7-px if flipx else px,7-py if flipy else py)
      if c:
       image.putpixel((x*16+(slot%2)*8+px,y*16+(slot//2)*8+py),pals[pal][c])
image.save(OUT/"landing_camp_actual_engine_tiles_preview.png")
report={"map_size":[plan["width"],plan["height"]],"map_metatile_ids":sorted(set(w&1023 for w in map_words)),
"invalid_metatile_references":invalid,
"preview":"landing_camp_actual_engine_tiles_preview.png",
"status":"rendered_from_real_engine_map_data_not_emulator_screenshot"}
(OUT/"actual_engine_map_preview_report.json").write_text(json.dumps(report,indent=2)+"\n")
assert not invalid,invalid
print(json.dumps(report,indent=2))
