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
border_names = manifest["border"]
border_ids = [names.index(name) for name in border_names]
used_ids = sorted({gid-1 for gid in gids} | set(border_ids))
layer_shift = int(re.search(r"#define METATILE_ATTR_LAYER_SHIFT\s+(\d+)",
                            (ROOT / "include/global.fieldmap.h").read_text()).group(1))
covered_layer = 1 << layer_shift
covered = set(manifest["covered"])
blank=(0,)*64
tiles=[[blank],[blank]]
caches=[{blank:0},{blank:0}]
# Animated graphics must occupy their own contiguous DMA range. Sharing
# frame-zero pixels with a static tile would animate unrelated scenery.
water = json.loads((ART/'water_animation.json').read_text())
water_tile_ids = {}
sequences = {}
water_start = len(tiles[0])
for name, frames in water['metatiles'].items():
    images = [bytes.fromhex(frame) for frame in frames]
    assert name in names and all(len(frame) == 256 for frame in images)
    assert all(max(frame) < 16 for frame in images)
    for slot,(sy,sx) in enumerate(((0,0),(0,8),(8,0),(8,8))):
        indices = tuple((sy+y)*16+sx+x for y in range(8) for x in range(8))
        sequence = tuple(tuple(frame[i] for i in indices) for frame in images)
        if all(frame == sequence[0] for frame in sequence):
            continue
        if sequence not in sequences:
            sequences[sequence] = len(tiles[0])
            tiles[0].append(sequence[0])
        water_tile_ids[name,slot] = sequences[sequence]
assert sequences and len(tiles[0]) <= 512

def pack_tile(pixels):
    return bytes(pixels[i] | (pixels[i+1]<<4) for i in range(0,64,2))


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
    # Both layers of walkable deck cells must draw behind object sprites.
    if names[mid] in covered:
        attrs[bank][mid] = covered_layer
    underlay=manifest.get('underlays',{}).get(names[mid])
    sources=[(underlay,0),(names[mid],1)] if underlay else [(names[mid],0)]
    for source_name,layer in sources:
        source_mid=names.index(source_name)
        source_palette=slots.get(source_name,6)
        preferred_bank = 0 if source_palette == 6 or source_name.startswith("env_") else 1
        source_mx=(source_mid%(atlas.width//16))*16
        source_my=(source_mid//(atlas.width//16))*16
        for slot,(sy,sx) in enumerate(((0,0),(0,8),(8,0),(8,8))):
            pixels=tuple(atlas.getpixel((source_mx+sx+x,source_my+sy+y)) for y in range(8) for x in range(8))
            assert all(0<=c<16 for c in pixels)
            animated_id = water_tile_ids.get((source_name,slot))
            if animated_id is not None:
                assert pixels == tiles[0][animated_id]
                metas[bank][mid*8+layer*4+slot] = (source_palette<<12) | animated_id
                continue
            # A metatile may reference either graphics bank. Reuse existing
            # pixels before allocating into the preferred bank or its spare.
            source_bank = preferred_bank
            alternate = 1 - preferred_bank
            if pixels not in caches[source_bank] and (pixels in caches[alternate] or len(tiles[source_bank]) == 512):
                source_bank = alternate
            if pixels not in caches[source_bank]:
                index=len(tiles[source_bank])
                assert index < 512, f"Combined 1024-tile graphics budget exceeded at {source_name}"
                tiles[source_bank].append(pixels)
                for flip_y in (False,True):
                    for flip_x in (False,True):
                        oriented=tuple(pixels[(7-y if flip_y else y)*8+(7-x if flip_x else x)] for y in range(8) for x in range(8))
                        caches[source_bank].setdefault(oriented,index|(0x400 if flip_x else 0)|(0x800 if flip_y else 0))
            metas[bank][mid*8+layer*4+slot]=(source_palette<<12)|(source_bank*512)|caches[source_bank][pixels]
packed_banks=[]
for bank,dest in enumerate(DESTS):
    dest.mkdir(parents=True,exist_ok=True)
    sheet=Image.new('P',(128,256),0)
    sheet.putpalette([v for rgb in manifest['palette'] for v in rgb]+[0]*(768-48))
    packed=bytearray()
    for index in range(512):
        pixels=tiles[bank][index] if index<len(tiles[bank]) else blank
        packed.extend(pack_tile(pixels))
        for y in range(8):
            for x in range(8): sheet.putpixel(((index%16)*8+x,(index//16)*8+y),pixels[y*8+x])
    assert len(packed)==16384 and packed[:32]==bytes(32)
    packed_banks.append(packed)
    sheet.save(dest/'tiles.png')
    (dest/'tiles.4bpp').write_bytes(packed)
    (dest/'metatiles.bin').write_bytes(struct.pack('<4096H',*metas[bank]))
water_count = len(sequences)
water_steps = len(next(iter(sequences)))
assert all(len(sequence) == water_steps for sequence in sequences)
water_frames = [b"".join(pack_tile(sequence[step]) for sequence in sequences)
                for step in range(water_steps)]
assert all(water_frames[i] != water_frames[(i+1)%water_steps] for i in range(water_steps))
assert water_frames[0] == packed_banks[0][water_start*32:(water_start+water_count)*32]
(DESTS[0]/'water_frames.bin').write_bytes(b''.join(water_frames))
water_report = {
    "start_tile":water_start, "tile_count":water_count, "frame_count":water_steps,
    "frames_per_step":water["frames_per_step"], "animated_metatiles":sorted({name for name,_ in water_tile_ids}),
}
(DESTS[0]/'water_animation.json').write_text(json.dumps(water_report,indent=2)+'\n')

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
for key in ('medical_door','research_door','hq_door','supply_door','quarters_door','ship_boarding','provision_door','ruins_gate'):
    x,y=plan['landmarks'][key]
    assert collision[y*w+x]==0,('Blocked entrance',key)
    mid=gids[y*w+x]-1
    attrs[map_ids[mid]//512][mid]|=behaviors.index('MB_NON_ANIMATED_DOOR')
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
camp_layout = ROOT / 'data/layouts/MeridianLandingCampPrototype'
(camp_layout / 'map.bin').write_bytes(struct.pack('<1920H', *words))
(camp_layout / 'border.bin').write_bytes(struct.pack('<4H', *(map_ids[mid] for mid in border_ids)))
# Register a private primary bank: General is shared by the rest of Emerald
# and must never be overwritten to make room for camp art.
symbol='MeridianCampEnvironment'
base='data/tilesets/primary/meridian_camp_environment/'
water_bytes = water_count*32
(DESTS[0]/'water_animation.h').write_text(f'''// Generated by integrate_meridian_original_camp_art.py.
static const u16 ALIGNED(4) sMeridianWaterFrames[] = INCBIN_U16("{base}water_frames.bin");

static void TilesetAnim_MeridianWater(u16 timer)
{{
    if (timer % {water["frames_per_step"]} == 0)
    {{
        u16 frame = timer / {water["frames_per_step"]};
        AppendTilesetAnimToBuffer(sMeridianWaterFrames + frame * ({water_bytes} / sizeof(u16)),
                                  (u16 *)(BG_VRAM + TILE_OFFSET_4BPP({water_start})), {water_bytes});
    }}
}}

void InitTilesetAnim_MeridianWater(void)
{{
    sPrimaryTilesetAnimCounter = 0;
    sPrimaryTilesetAnimCounterMax = {water_steps*water["frames_per_step"]};
    sPrimaryTilesetAnimCallback = TilesetAnim_MeridianWater;
}}
''')
anim_source = ROOT/'src/tileset_anims.c'
anim_include = '#include "../'+base+'water_animation.h"'
source = anim_source.read_text()
if anim_include not in source:
    anchor = 'void InitTilesetAnim_General(void)'
    assert source.count(anchor) == 1
    anim_source.write_text(source.replace(anchor,anim_include+'\n\n'+anchor,1))
registrations={
    'src/data/tilesets/graphics.h':f'const u32 gTilesetTiles_{symbol}[] = INCGFX_U32("{base}tiles.png", ".4bpp.fastSmol", "-num_tiles 512 -Wnum_tiles");\n' + f'const u16 ALIGNED(4) gTilesetPalettes_{symbol}[][16] =\n{{\n' + ''.join(f'    INCGFX_U16("{base}palettes/{i:02d}.pal", ".gbapal"),\n' for i in range(6)) + '};\n',
    'src/data/tilesets/metatiles.h':f'const u16 gMetatiles_{symbol}[] = INCBIN_U16("{base}metatiles.bin");\nconst u16 gMetatileAttributes_{symbol}[] = INCBIN_U16("{base}metatile_attributes.bin");\n',
    'src/data/tilesets/headers.h':f'''void InitTilesetAnim_MeridianWater(void);

const struct Tileset gTileset_{symbol} =
{{
    .isCompressed = TRUE,
    .isSecondary = FALSE,
    .tiles = gTilesetTiles_{symbol},
    .palettes = gTilesetPalettes_{symbol},
    .metatiles = gMetatiles_{symbol},
    .metatileAttributes = gMetatileAttributes_{symbol},
    .callback = InitTilesetAnim_MeridianWater,
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
        'water_animation':water_report,'packed_tile_roundtrip':'passed','map_unique_metatile_ids':len({word & 1023 for word in words}),
        'collision_blocked':sum(collision),'primary_tileset':f'gTileset_{symbol}',
        'secondary_tileset':'gTileset_MeridianShadyForest',
        'note':'Requires compilation and emulator verification; visual approval remains separate'}
(OUT/'original_art_engine_integration.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
