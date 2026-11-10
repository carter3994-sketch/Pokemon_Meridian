#!/usr/bin/env python3
"""Render an annotated visual atlas of Landing Camp GBA metatiles.

Preview only: PNG source colors are used; final in-game palettes and animation
must be verified in-engine before a metatile is assigned to a map zone.
"""
from pathlib import Path
import struct
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "build/meridian_prototypes"
OUT.mkdir(parents=True, exist_ok=True)
SETS = [
    ("primary_general", "data/tilesets/primary/general"),
    ("secondary_petalburg", "data/tilesets/secondary/petalburg"),
]
COLS = 12
SCALE = 3
CELL_W, CELL_H = 16 * SCALE + 8, 16 * SCALE + 23

for label, rel in SETS:
    folder = ROOT / rel
    src = Image.open(folder / "tiles.png").convert("RGBA")
    raw = (folder / "metatiles.bin").read_bytes()
    if len(raw) % 16:
        raise ValueError(f"Invalid metatile length for {rel}")
    count = len(raw) // 16
    rows = (count + COLS - 1) // COLS
    sheet = Image.new("RGB", (COLS * CELL_W, rows * CELL_H + 22), "#eeeeee")
    draw = ImageDraw.Draw(sheet)
    draw.text((6, 4), f"{label}: {count} metatiles | visual preview only", fill="black")
    tiles_per_row = src.width // 8
    if tiles_per_row == 0 or src.height % 8:
        raise ValueError(f"Unexpected tile sheet dimensions: {src.size}")
    for idx in range(count):
        entries = struct.unpack_from("<8H", raw, idx * 16)
        tile = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
        for layer in range(2):
            for quadrant in range(4):
                word = entries[layer * 4 + quadrant]
                tile_id = word & 0x03FF
                tx, ty = (tile_id % tiles_per_row) * 8, (tile_id // tiles_per_row) * 8
                if ty + 8 > src.height:
                    continue
                patch = src.crop((tx, ty, tx + 8, ty + 8))
                if word & 0x0400:
                    patch = patch.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
                if word & 0x0800:
                    patch = patch.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
                x, y = (quadrant % 2) * 8, (quadrant // 2) * 8
                tile.alpha_composite(patch, (x, y))
        x = (idx % COLS) * CELL_W + 4
        y = (idx // COLS) * CELL_H + 22
        sheet.paste(tile.resize((16 * SCALE, 16 * SCALE), Image.Resampling.NEAREST), (x, y), tile.resize((16 * SCALE, 16 * SCALE), Image.Resampling.NEAREST))
        draw.text((x, y + 16 * SCALE + 2), f"{idx:03d} / 0x{idx:03X}", fill="black")
    dest = OUT / f"metatile_atlas_{label}.png"
    sheet.save(dest)
    print(f"Rendered {dest} ({count} metatiles)")
