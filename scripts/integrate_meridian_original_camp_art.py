#!/usr/bin/env python3
"""Compile Landing Camp art into dedicated primary and secondary GBA banks.

Environment metatiles use the primary bank; reference-based structures and
foliage use secondary. Registration is confined to the generated camp layout.
"""
from pathlib import Path
import json
import re
import struct
import xml.etree.ElementTree as ET
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
ART=ROOT/'build/meridian_camp_art'
OUT=ROOT/'build/meridian_candidate_review'
OUT.mkdir(parents=True,exist_ok=True)
DESTS=[ROOT/'data/tilesets/primary/meridian_camp_environment', ROOT/'data/tilesets/secondary/meridian_shady_forest']
manifest=json.loads((ART/'metatile_manifest.json').read_text())
names=list(manifest['metatiles'])
slots=manifest.get('tile_palettes',{})
atlas=Image.open(ART/'camp_original_metatiles_indexed.png')
assert atlas.mode=='P' and atlas.width%16==0 and atlas.height%16==0
assert len(names)<=512
root=ET.parse(ART/'camp_48x40_editable.tmx').getroot()
w,h=int(root.get('width')),int(root.get('height'))
assert (w,h)==(48,40)
def cells(layer):
    data=layer.find('data')
    assert data.get('encoding')=='csv'
    values=[int(v) for v in data.text.split(',') if v.strip()]
    assert len(values)==w*h
    return values
gids,collision=[cells(layer) for layer in root.findall('layer')[:2]]
assert all(1<=gid<=len(names) for gid in gids)
assert all(value in (0,1) for value in collision)
used_ids=sorted({gid-1 for gid in gids})
blank=(0,)*64
tiles=[[blank],[blank]]
caches=[{blank:0},{blank:0}]
# Metatile IDs stay equal to atlas IDs within each bank. Neither reordering
# pixel tiles nor deduplication changes which metatile contains a warp.
metas=[[(6<<12)|base]*4096 for base in (0,512)]
attrs=[[0]*512,[0]*512]
map_ids={}
for mid in used_ids:
    palette=slots.get(names[mid],6)
    assert 0<=palette<int(re.search(r'#define NUM_PALS_TOTAL (\d+)',(ROOT/'include/fieldmap.h').read_text()).group(1)), 'Map palette exceeds engine limit'
    bank=0 if palette==6 or names[mid].startswith("env_") else 1
    base=bank*512
    map_ids[mid]=base+mid
    mx=(mid%(atlas.width//16))*16
    my=(mid//(atlas.width//16))*16
    # Ship and dock edge cells keep index-0 transparency and put ocean
    # pixels on the lower GBA background layer.
    underlay=manifest.get('underlays',{}).get(names[mid])
    sources=[(underlay,0),(names[mid],1)] if underlay else [(names[mid],0)]
    for source_name,layer in sources:
        source_mid=names.index(source_name)
        source_palette=slots.get(source_name,6)
        source_bank=0 if source_palette==6 or source_name.startswith('env_') else 1
        source_base=source_bank*512
        source_mx=(source_mid%(atlas.width//16))*16
        source_my=(source_mid//(atlas.width//16))*16
        for slot,(sy,sx) in enumerate(((0,0),(0,8),(8,0),(8,8))):
            pixels=tuple(atlas.getpixel((source_mx+sx+x,source_my+sy+y)) for y in range(8) for x in range(8))
            assert all(0<=c<16 for c in pixels)
            if pixels not in caches[source_bank]:
                index=len(tiles[source_bank])
                assert index<512, f'Bank {source_bank} exceeds 512 tiles'
                tiles[source_bank].append(pixels)
                for flip_y in (False,True):
                    for flip_x in (False,True):
                        oriented=tuple(pixels[(7-y if flip_y else y)*8+(7-x if flip_x else x)] for y in range(8) for x in range(8))
                        caches[source_bank].setdefault(oriented,index|(0x400 if flip_x else 0)|(0x800 if flip_y else 0))
            metas[bank][mid*8+layer*4+slot]=(source_palette<<12)|source_base|caches[source_bank][pixels]
packed_banks=[]
for bank,dest in enumerate(DESTS):
    dest.mkdir(parents=True,exist_ok=True)
    sheet=Image.new('P',(128,256),0)
    sheet.putpalette([v for rgb in manifest['palette'] for v in rgb]+[0]*(768-48))
    packed=bytearray()
    for index in range(512):
        pixels=tiles[bank][index] if index<len(tiles[bank]) else blank
        packed.extend(pixels[i]|(pixels[i+1]<<4) for i in range(0,64,2))
        for y in range(8):
            for x in range(8): sheet.putpixel(((index%16)*8+x,(index//16)*8+y),pixels[y*8+x])
    assert len(packed)==16384 and packed[:32]==bytes(32)
    packed_banks.append(packed)
    sheet.save(dest/'tiles.png')
    (dest/'tiles.4bpp').write_bytes(packed)
    (dest/'metatiles.bin').write_bytes(struct.pack('<4096H',*metas[bank]))
# Decode every visible layer reference, including flips, to source pixels.
for mid in used_ids:
    bank=map_ids[mid]//512
    underlay=manifest.get('underlays',{}).get(names[mid])
    sources=[(underlay,0),(names[mid],1)] if underlay else [(names[mid],0)]
    for source_name,layer in sources:
        source_mid=names.index(source_name)
        for slot in range(4):
            ref=metas[bank][mid*8+layer*4+slot]
            tile_bank=(ref&1023)//512
            index=ref&511
            decoded=[]
            for y in range(8):
                for x in range(8):
                    i=(7-y if ref&0x800 else y)*8+(7-x if ref&0x400 else x)
                    decoded.append((packed_banks[tile_bank][index*32+i//2]>>(4*(i%2)))&15)
            sx=(source_mid%(atlas.width//16))*16+(slot%2)*8
            sy=(source_mid//(atlas.width//16))*16+(slot//2)*8
            expected=[atlas.getpixel((sx+x,sy+y)) for y in range(8) for x in range(8)]
            assert decoded==expected,(mid,layer,slot)
plan=json.loads((ROOT/'data/meridian_plans/landing_camp_arrival.json').read_text())
behaviors=re.findall(r'\bMB_[A-Z0-9_]+\b',(ROOT/'include/constants/metatile_behaviors.h').read_text().split('};',1)[0])
for key in ('medical_door','research_door','hq_door','supply_door','quarters_door'):
    x,y=plan['landmarks'][key]
    assert collision[y*w+x]==0,('Blocked entrance',key)
    mid=gids[y*w+x]-1
    attrs[map_ids[mid]//512][mid]=behaviors.index('MB_NON_ANIMATED_DOOR')
for bank,dest in enumerate(DESTS):
    (dest/'metatile_attributes.bin').write_bytes(struct.pack('<512H',*attrs[bank]))
# Primary palette slots are private to the camp, with valid defaults for
# unused slots. Secondary slots 6..15 remain in the secondary table.
for slot in range(6):
    target=DESTS[0]/f'palettes/{slot:02d}.pal'
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_bytes((ROOT/f'data/tilesets/primary/general/palettes/{slot:02d}.pal').read_bytes())
# Replace unused secondary palette slots too; no staged external colors
# are needed by this original-art build.
for slot in range(6,16):
    target=DESTS[1]/f'palettes/{slot:02d}.pal'
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text('JASC-PAL\n0100\n16\n'+''.join(f'{r} {g} {b}\n' for r,g,b in manifest['palette']))
for slot,palette in manifest.get('palettes',{'6':manifest['palette']}).items():
    dest=DESTS[0 if int(slot)<6 else 1]/f'palettes/{int(slot):02d}.pal'
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text('JASC-PAL\n0100\n16\n'+''.join(f'{r} {g} {b}\n' for r,g,b in palette))
words=[map_ids[gid-1]|(0xC00 if blocked else 0)|0x3000 for gid,blocked in zip(gids,collision)]
(ROOT/'data/layouts/MeridianLandingCampPrototype/map.bin').write_bytes(struct.pack('<1920H',*words))
# Register a private primary bank: General is shared by the rest of Emerald
# and must never be overwritten to make room for camp art.
symbol='MeridianCampEnvironment'
base='data/tilesets/primary/meridian_camp_environment/'
registrations={
    'src/data/tilesets/graphics.h':f'const u32 gTilesetTiles_{symbol}[] = INCGFX_U32("{base}tiles.png", ".4bpp.fastSmol", "-num_tiles 512 -Wnum_tiles");\n' + f'const u16 ALIGNED(4) gTilesetPalettes_{symbol}[][16] =\n{{\n' + ''.join(f'    INCGFX_U16("{base}palettes/{i:02d}.pal", ".gbapal"),\n' for i in range(6)) + '};\n',
    'src/data/tilesets/metatiles.h':f'const u16 gMetatiles_{symbol}[] = INCBIN_U16("{base}metatiles.bin");\nconst u16 gMetatileAttributes_{symbol}[] = INCBIN_U16("{base}metatile_attributes.bin");\n',
    'src/data/tilesets/headers.h':f'''const struct Tileset gTileset_{symbol} =
{{
    .isCompressed = TRUE,
    .isSecondary = FALSE,
    .tiles = gTilesetTiles_{symbol},
    .palettes = gTilesetPalettes_{symbol},
    .metatiles = gMetatiles_{symbol},
    .metatileAttributes = gMetatileAttributes_{symbol},
    .callback = NULL,
}};
''',
}
for path,definition in registrations.items():
    target=ROOT/path
    source=target.read_text()
    if definition not in source:
        assert symbol not in source, f'Conflicting {path} registration'
        assert '#if !IS_FRLG' in source
        target.write_text(source.replace('#if !IS_FRLG','#if !IS_FRLG\n\n'+definition,1))
target=ROOT/'include/tilesets.h'
source=target.read_text()
declaration=f'extern const struct Tileset gTileset_{symbol};'
if declaration not in source:
    target.write_text(source.replace('extern const struct Tileset gTileset_General;',f'extern const struct Tileset gTileset_General;\n{declaration}',1))
target=ROOT/'data/layouts/layouts.json'
layouts=json.loads(target.read_text())
layout=next(v for v in layouts['layouts'] if v['id']=='LAYOUT_MERIDIAN_LANDING_CAMP_PROTOTYPE')
layout['primary_tileset']=f'gTileset_{symbol}'
target.write_text(json.dumps(layouts,indent=2)+'\n')
report={'status':'assets_integrated_into_real_engine_map_inputs','map_size':[w,h],
        'authored_metatiles':len(names),'unique_primary_8x8_tiles':len(tiles[0]),
        'unique_secondary_8x8_tiles':len(tiles[1]),'packed_4bpp_bytes':sum(map(len,packed_banks)),
        'packed_tile_roundtrip':'passed','map_unique_metatile_ids':len(set(words)),
        'collision_blocked':sum(collision),'primary_tileset':f'gTileset_{symbol}',
        'secondary_tileset':'gTileset_MeridianShadyForest',
        'note':'Requires compilation and emulator verification; visual approval remains separate'}
(OUT/'original_art_engine_integration.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
