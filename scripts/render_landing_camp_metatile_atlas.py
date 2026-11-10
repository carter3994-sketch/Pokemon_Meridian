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
    src = Image.open(folder / "tiles.png")
    if src.mode != "P":
        raise ValueError(f"Expected indexed PNG for {rel}, got {src.mode}")
    def palette_for(palette_id):
        # Emerald primary palettes occupy slots 0-5; secondary palettes 6-15.
        palette_folder = folder if palette_id < 6 and label == "primary_general" or palette_id >= 6 and label == "secondary_petalburg" else None
        if palette_folder is None:
            palette_folder = ROOT / ("data/tilesets/primary/general" if palette_id < 6 else "data/tilesets/secondary/petalburg")
        palette_path = palette_folder / "palettes" / f"{palette_id:02d}.pal"
        if not palette_path.exists():
            raise ValueError(f"Missing palette {palette_path}")
        lines = palette_path.read_text().splitlines()
        if lines[0] != "JASC-PAL":
            raise ValueError(f"Unexpected palette format: {palette_path}")
        return [tuple(map(int, line.split())) for line in lines[3:19]]
    palettes = [palette_for(i) for i in range(16)]
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
                indices = src.crop((tx, ty, tx + 8, ty + 8))
                palette = palettes[(word >> 12) & 15]
                patch = Image.new("RGBA", (8, 8))
                patch.putdata([(*palette[pixel & 15], 0 if layer == 1 and (pixel & 15) == 0 else 255) for pixel in indices.getdata()])
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
