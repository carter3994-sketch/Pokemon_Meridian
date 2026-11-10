#!/usr/bin/env python3
"""Read-only inspection of candidate Pokémon tileset PNGs (never imports art)."""
import argparse
import json
from collections import Counter
from pathlib import Path
from PIL import Image

def audit(path):
    with Image.open(path) as source:
        image = source.convert("RGBA")
        width, height = image.size
        colors = Counter(image.getdata())
        opaque = {rgba: count for rgba, count in colors.items() if rgba[3] > 0}
        partial = sum(count for rgba, count in colors.items() if 0 < rgba[3] < 255)
        return {
            "file": str(path), "source_mode": source.mode,
            "dimensions_px": [width, height],
            "grid_16px": [width // 16, height // 16] if width % 16 == 0 and height % 16 == 0 else None,
            "grid_32px": [width // 32, height // 32] if width % 32 == 0 and height % 32 == 0 else None,
            "opaque_colors": len(opaque), "partially_transparent_pixels": partial,
            "rgba_top_colors": [{"rgba": list(color), "pixels": count} for color, count in colors.most_common(8)],
            "gba_4bpp_single_palette_ready": len(opaque) <= 15 and partial == 0,
            "notes": "Color count is a preliminary screening metric, NOT a GBA tile-bank or palette assignment test."
        }

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("png", nargs="+", type=Path)
    parser.add_argument("--output", type=Path, help="Write JSON report")
    args = parser.parse_args()
    results = []
    for path in args.png:
        if path.suffix.lower() != ".png" or not path.is_file():
            parser.error(f"Not a readable PNG: {path}")
        results.append(audit(path))
    report = {"status": "inspection_only", "assets": results}
    output = json.dumps(report, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output + "\n")
    print(output)

if __name__ == "__main__":
    main()
