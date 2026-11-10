#!/usr/bin/env python3
"""Integrate original indexed camp art into a disposable Emerald secondary bank.

Runs after original art generation and Shady Forest engine registration.
Never modifies tracked binary art or silently promotes a ROM.
"""
from pathlib import Path
import json, struct, xml.etree.ElementTree as ET
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
ART=ROOT/"build/meridian_camp_art"
DEST=ROOT/"data/tilesets/secondary/meridian_shady_forest"
MAP=ROOT/"data/layouts/MeridianLandingCampPrototype/map.bin"
OUT=ROOT/"build/meridian_candidate_review"
OUT.mkdir(parents=True,exist_ok=True)
atlas=Image.open(ART/"camp_original_metatiles_indexed.png")
assert atlas.mode=="P" and atlas.width%16==0 and atlas.height%16==0
names=json.loads((ART/"metatile_manifest.json").read_text())["metatiles"]
assert len(names)<=512
tree=ET.parse(ART/"camp_48x40_editable.tmx").getroot()
w,h=int(tree.get("width")),int(tree.get("height"))
assert (w,h)==(48,40)
layers=tree.findall("layer")
assert len(layers)>=2
def cells(layer):
    data=layer.find("data")
    assert data.get("encoding")=="csv"
    result=[int(x.strip()) for x in data.text.split(",") if x.strip()]
    assert len(result)==w*h
    return result
gids=cells(layers[0])
collision=cells(layers[1])
assert all(1<=g<=len(names) for g in gids)
assert all(v in (0,1) for v in collision)
assert len(names)==(atlas.width//16)*(atlas.height//16)
# Build 512 unique 8x8 tiles maximum, padding with transparent tile 0.
tile_cache={}
tiles=[]
metas=[]
for mid in range(len(names)):
    mx=(mid%(atlas.width//16))*16
    my=(mid//(atlas.width//16))*16
    refs=[]
    for sy,sx in ((0,0),(0,8),(8,0),(8,8)):
        pixels=tuple(int(atlas.getpixel((mx+sx+x,my+sy+y))) for y in range(8) for x in range(8))
        assert all(0<=c<16 for c in pixels)
        if pixels not in tile_cache:
            tile_cache[pixels]=len(tiles)
            tiles.append(pixels)
        refs.append((6<<12)|(512+tile_cache[pixels]))
    metas.extend(refs+[0,0,0,0])
assert len(tiles)<=512, f"Original art requires {len(tiles)} secondary 8x8 tiles; maximum 512"
# Palette index 0 is transparent in the engine; the artwork uses it for cave openings.
# The engine renderer leaves transparent pixels black, matching index 0 in the
# original palette. Preserve the original atlas for exact pixel comparison.
sheet=Image.new("P",(128,256),0)
sheet.putpalette([v for rgb in json.loads((ART/"metatile_manifest.json").read_text())["palette"] for v in rgb]+[0]*(768-48))
for n,pixels in enumerate(tiles):
    tx=(n%16)*8;ty=(n//16)*8
    for y in range(8):
        for x in range(8):
            sheet.putpixel((tx+x,ty+y),pixels[y*8+x])
sheet.save(DEST/"tiles.png")
metas.extend([0]*((512-len(names))*8))
(DEST/"metatiles.bin").write_bytes(struct.pack("<4096H",*metas))
(DEST/"metatile_attributes.bin").write_bytes(bytes(1024))
colors=json.loads((ART/"metatile_manifest.json").read_text())["palette"]
(DEST/"palettes/06.pal").write_text("JASC-PAL\n0100\n16\n"+"".join(f"{r} {g} {b}\n" for r,g,b in colors))
words=[(512+gid-1)|(0x0C00 if blocked else 0)|0x3000 for gid,blocked in zip(gids,collision)]
MAP.write_bytes(struct.pack("<1920H",*words))
report={"status":"original_art_integrated_into_disposable_engine_checkout","map_size":[w,h],
 "authored_metatiles":len(names),"unique_secondary_8x8_tiles":len(tiles),
 "map_unique_metatile_ids":len(set(gids)),"collision_blocked":sum(collision),
 "engine_tileset":"gTileset_MeridianShadyForest",
 "source":"build/meridian_camp_art/camp_48x40_editable.tmx",
 "note":"Original art now supplies engine tiles and map words. Requires visual QA and ROM compile."}
(OUT/"original_art_engine_integration.json").write_text(json.dumps(report,indent=2)+"\n")
print(json.dumps(report,indent=2))
