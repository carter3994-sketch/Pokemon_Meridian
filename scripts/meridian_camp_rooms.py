"""Native room and ruins layouts for the Landing Camp playtest."""

from collections import deque
from pathlib import Path
import re
import struct

from PIL import Image, ImageDraw


ROOMS = {
    "Headquarters": (16, 12, (
        (2, 2, "banner"), (4, 2, "radio"), (7, 2, "briefing"), (8, 2, "briefing"),
        (7, 3, "table"), (8, 3, "table"), (11, 2, "radio"), (13, 2, "banner"),
        (6, 5, "table"), (7, 5, "table"), (8, 5, "table"),
        (9, 5, "table"), (2, 8, "crate"), (13, 8, "crate"),
    )),
    "Medical": (14, 11, (
        (2, 2, "monitor"), (5, 2, "cabinet"), (8, 2, "cabinet"),
        (11, 2, "monitor"), (2, 4, "bed"), (2, 5, "bed_foot"),
        (5, 4, "bed"), (5, 5, "bed_foot"), (8, 4, "bed"),
        (8, 5, "bed_foot"), (11, 4, "bed"), (11, 5, "bed_foot"),
        (2, 8, "medical"), (11, 8, "medical"),
    )),
    "Research": (16, 12, (
        (2, 2, "radio"), (3, 2, "monitor"), (6, 2, "capsule"),
        (9, 2, "capsule"), (12, 2, "monitor"), (13, 2, "radio"),
        (4, 5, "table"), (5, 5, "monitor"), (10, 5, "monitor"),
        (11, 5, "table"), (2, 8, "cabinet"), (13, 8, "cabinet"),
    )),
    "Supply": (16, 12, (
        (2, 2, "shelf"), (3, 2, "shelf"), (5, 2, "shelf"),
        (10, 2, "shelf"), (12, 2, "shelf"), (13, 2, "shelf"),
        (3, 5, "crate"), (4, 5, "crate"), (4, 6, "crate"),
        (11, 5, "crate"), (12, 5, "crate"), (11, 6, "crate"),
        (2, 8, "table"), (13, 8, "table"),
    )),
    "Quarters": (14, 11, (
        (2, 2, "cabinet"), (11, 2, "cabinet"),
        (2, 4, "bed"), (2, 5, "bed_foot"), (4, 4, "bed"),
        (4, 5, "bed_foot"), (9, 4, "bed"), (9, 5, "bed_foot"),
        (11, 4, "bed"), (11, 5, "bed_foot"),
        (4, 8, "table"), (9, 8, "table"),
    )),
    "Provision": (14, 11, (
        (2, 2, "shelf"), (3, 2, "shelf"), (5, 2, "shelf"), (8, 2, "shelf"),
        (10, 2, "shelf"), (11, 2, "shelf"),
        (4, 5, "table"), (5, 5, "table"), (6, 5, "radio"),
        (7, 5, "table"), (8, 5, "table"), (9, 5, "table"),
        (2, 7, "crate"), (11, 7, "crate"),
    )),
}


def indexed(palette, color=0):
    image = Image.new("P", (16, 16), color)
    image.putpalette([channel for rgb in palette for channel in rgb])
    return image


def indoor_art(palette):
    art = {}
    for phase in range(2):
        image = indexed(palette, 2)
        draw = ImageDraw.Draw(image)
        draw.line((0,0,15,0), fill=1)
        draw.line((0,1,15,1), fill=3)
        draw.line((phase*8,0,phase*8,15), fill=1)
        draw.point((13-phase*6,12), fill=3)
        art[f"floor_{phase}"] = image

    for name, base in (("wall",1),("panel",3),("mat",6),("threshold",6),
                       ("rug_edge",5),("rug_center",6)):
        image = indexed(palette, base)
        d = ImageDraw.Draw(image)
        if name in ("wall", "panel"):
            d.rectangle((0,0,15,2),fill=4)
            d.rectangle((1,4,14,11),fill=2)
            d.rectangle((2,5,13,10),outline=3)
            d.line((0,13,15,13),fill=1,width=2)
            d.point((3,8),fill=8)
            d.point((12,8),fill=8)
        elif name.startswith("rug_"):
            d.line((0,0,15,0),fill=7)
            d.line((0,15,15,15),fill=7)
            d.line((0,2,15,2),fill=9)
            d.line((0,13,15,13),fill=9)
            for x in (4,12):
                d.polygon(((x,4),(x+2,8),(x,11),(x-2,8)),outline=5 if base==6 else 6)
        else:
            d.rectangle((1,1,14,14),outline=5)
            d.rectangle((3,3,12,12),outline=7)
            if name == "threshold":
                d.polygon(((5,7),(10,7),(10,10),(12,10),(7,14),(3,10),(5,10)),fill=9)
            else:
                d.point((7,7),fill=7)
                d.point((8,8),fill=7)
        art[name] = image

    props = ("banner","radio","briefing","table","crate","monitor","cabinet",
             "bed","bed_foot","medical","capsule","shelf")
    for name in props:
        image = art["floor_0"].copy()
        d = ImageDraw.Draw(image)
        if name == "banner":
            d.polygon(((3,1),(12,1),(12,11),(7,15),(3,11)),fill=6)
            d.line((3,1,12,1),fill=9)
            d.line((7,4,7,10),fill=9)
            d.line((4,7,10,7),fill=9)
        elif name in ("radio","briefing","monitor","capsule"):
            d.rounded_rectangle((1,1,14,13),radius=2,fill=1,outline=4)
            d.rectangle((2,2,13,9),fill=6,outline=5)
            d.line((3,7,6,4,9,7,12,4),fill=7)
            if name == "briefing":
                d.polygon(((3,5),(7,3),(10,4),(12,7),(7,8),(4,7)),fill=10)
                d.point((7,6),fill=9)
                d.point((10,7),fill=9)
            if name == "capsule":
                d.ellipse((4,2,11,11),fill=7,outline=4)
                d.line((6,4,6,9),fill=13)
            else:
                d.rectangle((3,10,12,11),fill=3)
                d.point((10,11),fill=8)
        elif name in ("bed","bed_foot"):
            d.rectangle((2,0,13,15),fill=1)
            d.rectangle((3,0,12,14),fill=13 if name == "bed" else 5)
            if name == "bed":
                d.rectangle((4,3,11,7),fill=14)
                d.rectangle((3,9,12,15),fill=5)
            else:
                d.rectangle((3,12,12,13),fill=7)
            d.line((2,0,2,15),fill=4)
        else:
            d.rectangle((1,2,14,13),fill=11,outline=1)
            d.line((2,2,13,2),fill=9)
            d.line((2,12,13,12),fill=12)
            if name == "crate":
                d.rectangle((3,4,12,10),outline=12)
                d.line((3,4,12,10),fill=9)
            elif name == "shelf":
                for y in (5,9):
                    d.rectangle((3,y,12,y+1),fill=1)
                    for x,c in ((3,7),(6,8),(9,9)):
                        d.rectangle((x,y-1,x+1,y),fill=c)
            elif name == "medical":
                d.rectangle((3,4,12,11),fill=13)
                d.line((7,5,7,10),fill=15,width=2)
                d.line((5,7,10,7),fill=15,width=2)
            elif name == "cabinet":
                d.rectangle((3,4,12,11),fill=3,outline=4)
                d.point((6,8),fill=9)
                d.point((9,8),fill=9)
            else:
                d.rectangle((4,4,11,9),fill=2)
                d.line((5,8,10,5),fill=4)
        art[name] = image
    return art


def room_grid(room, width, height, props):
    grid = [[f"floor_{(x+y)%2}" for x in range(width)] for y in range(height)]
    grid[0] = ["wall"] * width
    grid[1] = ["panel"] * width
    grid[-1] = ["wall"] * width
    for row in grid:
        row[0] = row[-1] = "wall"
    if room in {"Headquarters", "Quarters", "Provision"}:
        for y in (6,8):
            for x in range(width//2-2,width//2+2):
                grid[y][x] = "rug_edge" if x in (width//2-2,width//2+1) else "rug_center"
    for x,y,name in props:
        grid[y][x] = name
    center = width//2
    exits = ((center-1,height-1), (center,height-1))
    for x,y in exits:
        grid[y][x] = "threshold"
        grid[y-1][x] = "mat"
    return grid, exits


def ruins_area(root):
    """Expand the approved stone ruin into a separate wooded precinct."""
    assets = root / "graphics/meridian/landing_camp"
    shrine = Image.open(assets/"env_ruins.png")
    terrain = Image.open(assets/"terrain_materials.png")
    forest = Image.open(assets/"forest_conifer.png")
    ruin_palette = shrine.getpalette()[:48]
    grass_palette = terrain.getpalette()[:48]
    forest_palette = forest.getpalette()[:48]
    grass = {f"grass_{i}":terrain.crop((i%2*16,i//2*16,i%2*16+16,i//2*16+16)) for i in range(4)}
    art = {name:(image,7) for name,image in grass.items()}
    for qy in range(4):
        for qx in range(4):
            box = (qx*16,qy*16,qx*16+16,qy*16+16)
            tile = shrine.crop(box)
            tile.putdata([0 if value == 15 else value for value in tile.getdata()])
            art[f"shrine_{qx}_{qy}"] = (tile,8)
    for qy in range(4):
        for qx in range(3):
            tile = forest.crop((qx*16,qy*16,qx*16+16,qy*16+16))
            if tile.getbbox() is not None:
                art[f"conifer_{qx}_{qy}"] = (tile,9)
    rock_colors = [tuple(ruin_palette[i:i+3]) for i in range(0,48,3)]
    for name,base in (("ruin_stone",7),("ruin_cracked",10),("ruin_pillar",0),("ruin_exit",7)):
        image = indexed(rock_colors,base)
        d = ImageDraw.Draw(image)
        if name == "ruin_pillar":
            d.ellipse((3,11,14,14),fill=13)
            d.rectangle((4,3,11,12),fill=9)
            d.line((4,4,4,11),fill=5)
            d.polygon(((4,3),(6,1),(11,2),(13,4),(10,6),(4,5)),fill=2)
            d.line((5,8,8,7,11,8),fill=12)
        else:
            d.line((0,0,15,0),fill=9)
            d.line((0,15,15,15),fill=12)
            d.line((8,0,8,15),fill=9)
            for x,y in ((3,4),(13,6),(6,12),(10,10)):
                d.point((x,y),fill=2 if name=="ruin_stone" else 7)
            if name == "ruin_cracked":
                d.line((0,9,5,8,7,11,12,8,15,9),fill=12)
            if name == "ruin_exit":
                d.polygon(((5,7),(10,7),(10,10),(12,10),(7,14),(3,10),(5,10)),fill=1)
        art[name] = (image,8)

    width,height = 24,20
    grid = [[f"grass_{x%2+2*(y%2)}" for x in range(width)] for y in range(height)]
    for y in range(6,15):
        for x in range(6,18):
            grid[y][x] = "ruin_cracked" if (x*7+y*3)%7 in (0,1) else "ruin_stone"
    for y in range(3,6):
        for x in range(9,15):
            grid[y][x] = "ruin_cracked" if (x+y)%3==0 else "ruin_stone"
    for y in range(15,height-1):
        for x in (11,12):
            grid[y][x] = "ruin_stone"
    for x,y in ((6,7),(6,10),(6,13),(17,7),(17,10),(17,13),(8,5),(15,5),(8,15),(15,15),(9,4),(14,4),(8,16),(15,16)):
        grid[y][x] = "ruin_pillar"
    for qy in range(4):
        for qx in range(4):
            grid[7+qy][10+qx] = f"shrine_{qx}_{qy}"
    for x,y in ((0,0),(3,0),(6,0),(9,0),(12,0),(15,0),(18,0),(21,0),
                (0,4),(0,8),(0,12),(0,16),(21,4),(21,8),(21,12),(21,16),
                (3,16),(6,16),(15,16),(18,16),(3,5),(18,6)):
        for qy in range(4):
            for qx in range(3):
                name = f"conifer_{qx}_{qy}"
                if name in art:
                    grid[y+qy][x+qx] = name
    exits = ((11,19),(12,19))
    for x,y in exits:
        grid[y][x] = "ruin_exit"
    return grid, exits, art, {7:grass_palette,8:ruin_palette,9:forest_palette}


def build_camp_rooms(root):
    """Compile tiles, maps and a preview for each new destination."""
    indoor_palette = [
        (0,0,0),(37,40,53),(78,85,99),(111,121,130),(174,183,180),
        (64,100,155),(38,62,108),(100,192,221),(225,175,77),(238,205,133),
        (104,153,116),(144,106,79),(96,66,54),(205,211,212),(246,237,213),(192,63,70),
    ]
    art = {name:(tile,6) for name,tile in indoor_art(indoor_palette).items()}
    maps = {name:room_grid(name,*spec) for name,spec in ROOMS.items()}
    ruin_grid, ruin_exits, ruin_art, palettes = ruins_area(root)
    maps["Ruins"] = (ruin_grid,ruin_exits)
    art.update(ruin_art)
    walkable = {"floor_0","floor_1","mat","threshold","rug_edge","rug_center",
                "ruin_stone","ruin_cracked","ruin_exit"}
    walkable.update(name for name in art if name.startswith("grass_"))
    walkable.update(f"shrine_{x}_{y}" for y,x in ((1,1),(1,2),(2,1),(2,2),
                                                   (3,0),(3,1),(3,2),(3,3)))
    exit_types = {"threshold","ruin_exit"}
    enum = (root/"include/constants/metatile_behaviors.h").read_text().split("};",1)[0]
    warp_behavior = re.findall(r"\bMB_[A-Z0-9_]+\b",enum).index("MB_NON_ANIMATED_DOOR")
    fieldmap = (root/"include/global.fieldmap.h").read_text()
    shift = int(re.search(r"#define METATILE_ATTR_LAYER_SHIFT\s+(\d+)",fieldmap).group(1))
    covered = 1 << shift

    atlas = Image.new("P",(128,256))
    atlas.putpalette([channel for i in range(16) for channel in (17*i,)*3])
    tiles = {bytes(64):0}
    meta, attrs, ids = [], [], {}
    def pack_layer(image,slot):
        refs = []
        for qx,qy in ((0,0),(1,0),(0,1),(1,1)):
            quad = image.crop((qx*8,qy*8,qx*8+8,qy*8+8))
            key = quad.tobytes()
            if key not in tiles:
                tile_id = len(tiles)
                assert tile_id < 512
                tiles[key] = tile_id
                atlas.paste(quad,(tile_id%16*8,tile_id//16*8))
            refs.append((slot<<12) | 512 | tiles[key])
        return refs

    underlays = {name:"grass_0" for name in art
                 if name.startswith(("conifer_","shrine_")) or name == "ruin_pillar"}
    for name,(image,slot) in art.items():
        ids[name] = len(attrs)+512
        layer = pack_layer(image,slot)
        if name in underlays:
            meta.extend(pack_layer(*art[underlays[name]])+layer)
        else:
            meta.extend(layer+[512]*4)
        behavior = warp_behavior if name in exit_types else 0
        if name in underlays and name in walkable:
            behavior |= covered
        attrs.append(behavior)

    base = "data/tilesets/secondary/meridian_expedition_rooms/"
    dest = root/base
    (dest/"palettes").mkdir(parents=True,exist_ok=True)
    atlas.save(dest/"tiles.png")
    (dest/"metatiles.bin").write_bytes(struct.pack("<4096H",*(meta+[512]*(4096-len(meta)))))
    (dest/"metatile_attributes.bin").write_bytes(struct.pack("<512H",*(attrs+[0]*(512-len(attrs)))))
    palettes[6] = [channel for rgb in indoor_palette for channel in rgb]
    for slot in range(6,16):
        values = palettes.get(slot,palettes[6])
        lines = [" ".join(str(v) for v in values[i:i+3]) for i in range(0,48,3)]
        (dest/f"palettes/{slot:02d}.pal").write_text("JASC-PAL\n0100\n16\n"+"\n".join(lines)+"\n")

    register_room_tileset(root,base)
    result = {}
    review = root/"build/meridian_candidate_review/rooms"
    review.mkdir(parents=True,exist_ok=True)
    for name,(grid,exits) in maps.items():
        width,height = len(grid[0]),len(grid)
        open_tiles = {(x,y) for y,row in enumerate(grid) for x,tile in enumerate(row) if tile in walkable}
        reachable = {exits[0]}
        queue = deque(reachable)
        while queue:
            x,y = queue.popleft()
            for pt in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
                if pt in open_tiles and pt not in reachable:
                    reachable.add(pt)
                    queue.append(pt)
        assert open_tiles == reachable, (name,open_tiles-reachable)
        assert all(grid[y][x] in exit_types for x,y in exits)

        preview = Image.new("RGB",(width*16,height*16))
        words = []
        for y,row in enumerate(grid):
            for x,tile in enumerate(row):
                image = art[tile][0]
                pos = x*16,y*16
                if tile in underlays:
                    preview.paste(art[underlays[tile]][0].convert("RGB"),pos)
                    mask = Image.new("L",(16,16))
                    mask.putdata([255 if value else 0 for value in image.getdata()])
                    preview.paste(image.convert("RGB"),pos,mask)
                else:
                    preview.paste(image.convert("RGB"),pos)
                words.append(ids[tile] | 0x3000 | (0 if (x,y) in open_tiles else 0xC00))
        preview.save(review/f"{name.lower()}.png")
        layout_dir = root/f"data/layouts/MeridianLandingCamp{name}"
        layout_dir.mkdir(parents=True,exist_ok=True)
        (layout_dir/"map.bin").write_bytes(struct.pack(f"<{width*height}H",*words))
        border = ids["grass_0" if name == "Ruins" else "wall"]
        (layout_dir/"border.bin").write_bytes(struct.pack("<4H",*(border,)*4))
        result[name] = (width,height,exits)
    print(f"Compiled {len(result)} Meridian layouts with {len(tiles)} room tiles and reachable exits")
    return result


def register_room_tileset(root,base):
    symbol = "MeridianExpeditionRooms"
    palettes = [
        f'data/tilesets/primary/general/palettes/{i:02d}.pal' if i<6 else f'{base}palettes/{i:02d}.pal'
        for i in range(16)
    ]
    palette_rows = "".join(f'    INCGFX_U16("{path}", ".gbapal"),\n' for path in palettes)
    definitions = {
        "graphics.h": (
            f'const u32 gTilesetTiles_{symbol}[] = INCGFX_U32("{base}tiles.png", ".4bpp.fastSmol", "-num_tiles 512 -Wnum_tiles");\n'
            f'const u16 ALIGNED(4) gTilesetPalettes_{symbol}[][16] =\n{{\n{palette_rows}}};\n'
        ),
        "metatiles.h": (
            f'const u16 gMetatiles_{symbol}[] = INCBIN_U16("{base}metatiles.bin");\n'
            f'const u16 gMetatileAttributes_{symbol}[] = INCBIN_U16("{base}metatile_attributes.bin");\n'
        ),
        "headers.h": (
            f'const struct Tileset gTileset_{symbol} =\n{{\n'
            f'    .isCompressed = TRUE,\n    .isSecondary = TRUE,\n    .tiles = gTilesetTiles_{symbol},\n'
            f'    .palettes = gTilesetPalettes_{symbol},\n    .metatiles = gMetatiles_{symbol},\n'
            f'    .metatileAttributes = gMetatileAttributes_{symbol},\n    .callback = NULL,\n}};\n'
        ),
    }
    for file,text in definitions.items():
        path = root/"src/data/tilesets"/file
        original = path.read_text()
        if text not in original:
            assert symbol not in original and "#if !IS_FRLG" in original
            path.write_text(original.replace("#if !IS_FRLG",f"#if !IS_FRLG\n\n{text}",1))
    path = root/"include/tilesets.h"
    original = path.read_text()
    declaration = f"extern const struct Tileset gTileset_{symbol};"
    if declaration not in original:
        path.write_text(original.replace("extern const struct Tileset gTileset_General;",
                                         "extern const struct Tileset gTileset_General;\n"+declaration,1))
